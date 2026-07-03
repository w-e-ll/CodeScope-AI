#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import hashlib
import logging

from dataclasses import dataclass
from typing import Any

from codescope_ai.app.core.app_config import AppConfig
from codescope_ai.app.core.exceptions import (
    CodeChunkingError,
    PythonAnalysisError,
)
from codescope_ai.app.ingestion.source_file_reader import SourceFile

logger = logging.getLogger(__name__)


@dataclass
class CodeChunk:
    """Represents a retrievable source code chunk."""

    chunk_id: str
    relative_path: str
    file_name: str
    language: str
    symbol_type: str
    symbol_name: str
    start_line: int
    end_line: int
    content: str
    content_hash: str
    metadata: dict[str, Any]


class CodeChunker:
    """Creates semantic chunks from source files."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize code chunker."""

        self.config = config

    def chunk_files(self, source_files: list[SourceFile]) -> list[CodeChunk]:
        """Chunk multiple source files."""

        chunks = []

        for source_file in source_files:
            try:
                file_chunks = self.chunk_file(source_file)
                chunks.extend(file_chunks)

                logger.info(
                    f"File chunked: "
                    f"path={source_file.relative_path} "
                    f"chunks={len(file_chunks)}"
                )

            except CodeChunkingError:
                logger.exception(
                    f"Skipping file after chunking failure: "
                    f"{source_file.relative_path}"
                )

        logger.info(
            f"Chunking completed: total_chunks={len(chunks)}"
        )

        return chunks

    def chunk_file(self, source_file: SourceFile) -> list[CodeChunk]:
        """Chunk one source file."""

        try:
            if source_file.language == "python":
                return self._chunk_python_file(source_file)

            return self._chunk_text_file(source_file)

        except CodeChunkingError:
            raise

        except Exception as exc:
            logger.exception(
                f"Failed to chunk file: "
                f"{source_file.relative_path}"
            )

            raise CodeChunkingError(
                f"Failed to chunk file: "
                f"{source_file.relative_path}"
            ) from exc

    def _chunk_python_file(self, source_file: SourceFile) -> list[CodeChunk]:
        """Chunk Python file using AST symbols."""

        try:
            tree = ast.parse(source_file.content)

        except SyntaxError as exc:
            logger.warning(
                f"Python syntax error, fallback to text chunking: "
                f"{source_file.relative_path} "
                f"line={exc.lineno}"
            )

            return self._chunk_text_file(source_file)

        except Exception as exc:
            raise PythonAnalysisError(
                f"Failed to parse Python file: "
                f"{source_file.relative_path}"
            ) from exc

        chunks = []

        module_context = self._extract_module_context(
            source_file.content
        )

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                chunks.append(
                    self._build_python_chunk(
                        source_file=source_file,
                        node=node,
                        symbol_type="class",
                        module_context=module_context,
                    )
                )

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                chunks.append(
                    self._build_python_chunk(
                        source_file=source_file,
                        node=node,
                        symbol_type="function",
                        module_context=module_context,
                    )
                )

        if not chunks:
            logger.info(
                f"No Python symbols found, using text chunking: "
                f"{source_file.relative_path}"
            )

            return self._chunk_text_file(source_file)

        logger.info(
            f"Python file analyzed: "
            f"path={source_file.relative_path} "
            f"symbols={len(chunks)}"
        )

        return chunks

    def _build_python_chunk(
        self,
        source_file: SourceFile,
        node: ast.AST,
        symbol_type: str,
        module_context: str,
    ) -> CodeChunk:
        """Build a Python chunk from AST node."""

        lines = source_file.content.splitlines()

        start_line = getattr(
            node,
            "lineno",
            1,
        )

        end_line = getattr(
            node,
            "end_lineno",
            start_line,
        )

        symbol_name = getattr(
            node,
            "name",
            "unknown",
        )

        body = "\n".join(
            lines[
                start_line - 1:end_line
            ]
        )

        content = self._join_context(
            module_context,
            body,
        )

        metadata = {
            "docstring": ast.get_docstring(node),
            "imports": self._extract_imports(module_context),
            "decorators": self._extract_decorators(node),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        }

        return self._create_chunk(
            source_file=source_file,
            symbol_type=symbol_type,
            symbol_name=symbol_name,
            start_line=start_line,
            end_line=end_line,
            content=content,
            metadata=metadata,
        )

    def _chunk_text_file(self, source_file: SourceFile) -> list[CodeChunk]:
        """Chunk non-Python files by line windows."""

        lines = source_file.content.splitlines()

        if not lines:
            logger.warning(
                f"Skipping empty file: "
                f"{source_file.relative_path}"
            )

            return []

        chunks = []
        start_index = 0
        chunk_size = max(
            1,
            self.config.chunk_size,
        )
        overlap = max(
            0,
            self.config.chunk_overlap,
        )

        while start_index < len(lines):
            end_index = min(
                start_index + chunk_size,
                len(lines),
            )

            chunk_lines = lines[
                start_index:end_index
            ]

            content = "\n".join(chunk_lines)

            chunks.append(
                self._create_chunk(
                    source_file=source_file,
                    symbol_type="file_section",
                    symbol_name=f"lines_{start_index + 1}_{end_index}",
                    start_line=start_index + 1,
                    end_line=end_index,
                    content=content,
                    metadata={
                        "chunking_strategy": "line_window",
                    },
                )
            )

            if end_index == len(lines):
                break

            start_index = max(
                end_index - overlap,
                start_index + 1,
            )

        return chunks

    def _extract_module_context(self, content: str) -> str:
        """Extract imports and module docstring."""

        lines = content.splitlines()
        context_lines = []

        try:
            tree = ast.parse(content)

            module_docstring = ast.get_docstring(tree)

            if module_docstring:
                context_lines.append(
                    f'"""{module_docstring}"""'
                )

            for node in tree.body:
                if isinstance(
                    node,
                    (
                        ast.Import,
                        ast.ImportFrom,
                    ),
                ):
                    context_lines.append(
                        lines[node.lineno - 1]
                    )

        except Exception:
            logger.debug(
                "Module context extraction failed",
                exc_info=True,
            )

        return "\n".join(context_lines)

    def _extract_imports(self, module_context: str) -> list[str]:
        """Extract import lines from module context."""

        return [
            line
            for line in module_context.splitlines()
            if line.startswith("import ")
            or line.startswith("from ")
        ]

    def _extract_decorators(self, node: ast.AST) -> list[str]:
        """Extract decorator names from Python node."""

        decorators = []

        for decorator in getattr(
            node,
            "decorator_list",
            [],
        ):
            try:
                decorators.append(
                    ast.unparse(decorator)
                )

            except Exception:
                decorators.append(
                    "unknown"
                )

        return decorators

    def _join_context(self, module_context: str, body: str) -> str:
        """Join module context with symbol body."""

        if not module_context:
            return body

        return (
            f"{module_context}\n\n"
            f"{body}"
        )

    def _create_chunk(
        self,
        source_file: SourceFile,
        symbol_type: str,
        symbol_name: str,
        start_line: int,
        end_line: int,
        content: str,
        metadata: dict[str, Any],
    ) -> CodeChunk:
        """Create a stable code chunk."""

        content_hash = self._hash_content(content)

        chunk_key = (
            f"{source_file.relative_path}:"
            f"{symbol_type}:"
            f"{symbol_name}:"
            f"{start_line}:"
            f"{end_line}:"
            f"{content_hash}"
        )

        chunk_id = hashlib.sha256(
            chunk_key.encode("utf-8")
        ).hexdigest()

        return CodeChunk(
            chunk_id=chunk_id,
            relative_path=source_file.relative_path,
            file_name=source_file.file_name,
            language=source_file.language,
            symbol_type=symbol_type,
            symbol_name=symbol_name,
            start_line=start_line,
            end_line=end_line,
            content=content,
            content_hash=content_hash,
            metadata=metadata,
        )

    def _hash_content(self, content: str) -> str:
        """Create stable hash for chunk content."""

        return hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()
