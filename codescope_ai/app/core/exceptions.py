#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CodeScopeAIError(Exception):
    """Base exception for CodeScope AI application errors."""


class ConfigError(CodeScopeAIError):
    """Raised when application configuration is invalid or missing."""


class LoggingSetupError(CodeScopeAIError):
    """Raised when logging cannot be initialized."""


class RetryError(CodeScopeAIError):
    """Raised when a retryable operation fails after all attempts."""


class ArchiveLoaderError(CodeScopeAIError):
    """Raised when an uploaded archive cannot be processed."""


class ArchiveSecurityError(CodeScopeAIError):
    """Raised when an archive contains unsafe paths or unsupported content."""


class RepositoryRootError(CodeScopeAIError):
    """Raised when the repository root cannot be detected."""


class FileDiscoveryError(CodeScopeAIError):
    """Raised when source file discovery fails."""


class SourceFileReadError(CodeScopeAIError):
    """Raised when a source file cannot be read safely."""


class UnsupportedFileError(CodeScopeAIError):
    """Raised when a file type is not supported for ingestion."""


class CodeChunkingError(CodeScopeAIError):
    """Raised when source code chunking fails."""


class PythonAnalysisError(CodeScopeAIError):
    """Raised when Python AST analysis fails."""


class EmbeddingClientError(CodeScopeAIError):
    """Raised when embeddings cannot be generated."""


class VectorStoreError(CodeScopeAIError):
    """Raised when vector storage operations fail."""


class RetrievalError(CodeScopeAIError):
    """Raised when relevant context cannot be retrieved."""


class PromptBuildError(CodeScopeAIError):
    """Raised when an LLM prompt cannot be built."""


class LLMClientError(CodeScopeAIError):
    """Raised when the LLM request fails."""


class AnswerGenerationError(CodeScopeAIError):
    """Raised when the assistant cannot generate an answer."""


class DocumentationGenerationError(CodeScopeAIError):
    """Raised when documentation generation fails."""


class UIWorkflowError(CodeScopeAIError):
    """Raised when a UI workflow fails."""
