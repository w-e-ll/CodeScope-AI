#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import logging
import tempfile

from pathlib import Path

import streamlit as st

from codescope_ai.app.core.app_config import load_yaml_config
from codescope_ai.app.core.exceptions import CodeScopeAIError
from codescope_ai.app.core.setup_logger import setup_logger
from codescope_ai.app.documentation.project_documenter import ProjectDocumenter
from codescope_ai.app.ingestion.archive_loader import ArchiveLoader
from codescope_ai.app.ingestion.code_chunker import CodeChunker
from codescope_ai.app.ingestion.file_discovery import FileDiscovery
from codescope_ai.app.ingestion.source_file_reader import SourceFileReader
from codescope_ai.app.rag.answer_service import AnswerService
from codescope_ai.app.rag.embedding_client import EmbeddingClient
from codescope_ai.app.rag.llm_client import LLMClient
from codescope_ai.app.rag.prompt_builder import PromptBuilder
from codescope_ai.app.rag.retriever import Retriever
from codescope_ai.app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


def init_services(config_path: str) -> dict:
    """Initialize application services."""

    config = load_yaml_config(config_path)

    setup_logger(
        logfile=str(Path(config.log_dir) / "codescope_ai.log"),
        stdout=True,
    )

    embedding_client = EmbeddingClient(config)
    vector_store = VectorStore(config)
    retriever = Retriever(config, embedding_client, vector_store)
    prompt_builder = PromptBuilder(config)
    llm_client = LLMClient(config)

    return {
        "config": config,
        "archive_loader": ArchiveLoader(config),
        "file_discovery": FileDiscovery(config),
        "source_file_reader": SourceFileReader(config),
        "code_chunker": CodeChunker(config),
        "embedding_client": embedding_client,
        "vector_store": vector_store,
        "retriever": retriever,
        "prompt_builder": prompt_builder,
        "llm_client": llm_client,
        "answer_service": AnswerService(
            config,
            retriever,
            prompt_builder,
            llm_client,
        ),
        "project_documenter": ProjectDocumenter(
            config,
            retriever,
            prompt_builder,
            llm_client,
        ),
    }


def save_uploaded_archive(uploaded_file) -> str:
    """Save uploaded ZIP archive to a temporary file."""

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
    ) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return temp_file.name


def index_repository(services: dict, archive_path: str) -> dict:
    """Extract, analyze, chunk, embed, and index a repository."""

    repo_root = services["archive_loader"].extract_archive(
        archive_path
    )

    files = services["file_discovery"].discover_files(
        str(repo_root)
    )

    source_files = services["source_file_reader"].read_files(
        files,
        str(repo_root),
    )

    chunks = services["code_chunker"].chunk_files(
        source_files
    )

    embeddings = services["embedding_client"].embed_chunks(
        chunks
    )

    services["vector_store"].upsert_chunks(
        chunks,
        embeddings,
    )

    return {
        "repo_root": str(repo_root),
        "files": files,
        "source_files": source_files,
        "chunks": chunks,
        "chunk_count": len(chunks),
        "file_count": len(source_files),
    }


def render_citations(citations: list[dict]) -> None:
    """Render answer citations."""

    if not citations:
        st.info("No citations available.")
        return

    for citation in citations:
        st.markdown(
            f"- `{citation.get('file_path')}` "
            f"lines {citation.get('start_line')}-"
            f"{citation.get('end_line')} "
            f"`{citation.get('symbol_type')}:"
            f"{citation.get('symbol_name')}`"
        )


def render_debug_matches(matches: list[dict]) -> None:
    """Render retrieved context matches."""

    if not matches:
        st.info("No retrieval matches.")
        return

    for index, match in enumerate(matches, start=1):
        metadata = match.get("metadata", {})

        with st.expander(
            f"Match #{index} | "
            f"{metadata.get('relative_path')} | "
            f"score={match.get('score')}"
        ):
            st.caption(
                f"Lines {metadata.get('start_line')}-"
                f"{metadata.get('end_line')} | "
                f"{metadata.get('symbol_type')}:"
                f"{metadata.get('symbol_name')}"
            )

            st.code(
                match.get("content", ""),
                language=metadata.get("language", "text"),
            )


def main() -> None:
    """Run Streamlit application."""

    st.set_page_config(
        page_title="CodeScope AI",
        page_icon="🧠",
        layout="wide",
    )

    st.title("🧠 CodeScope AI")
    st.caption(
        "Code Documentation Assistant with RAG, citations, "
        "logging, and observable retrieval."
    )

    config_path = st.sidebar.text_input(
        "Config path",
        value="etc/codescope_ai_config.yml",
    )

    if "services" not in st.session_state:
        try:
            st.session_state.services = init_services(
                config_path
            )
            st.sidebar.success("Services initialized")

        except Exception as exc:
            st.sidebar.error(f"Initialization failed: {exc}")
            return

    services = st.session_state.services

    tab_upload, tab_chat, tab_docs, tab_debug = st.tabs(
        [
            "Upload & Index",
            "Chat With Codebase",
            "Generate Docs",
            "Retrieval Debug",
        ]
    )

    with tab_upload:
        st.subheader("Upload repository ZIP")

        uploaded_file = st.file_uploader(
            "Upload GitHub repository ZIP",
            type=["zip"],
        )

        reset_collection = st.checkbox(
            "Reset vector collection before indexing",
            value=True,
        )

        if st.button("Index Repository", type="primary"):
            if not uploaded_file:
                st.warning("Upload a ZIP archive first.")
                return

            try:
                with st.spinner("Indexing repository..."):
                    archive_path = save_uploaded_archive(
                        uploaded_file
                    )

                    if reset_collection:
                        services["vector_store"].reset_collection()

                    result = index_repository(
                        services,
                        archive_path,
                    )

                    st.session_state.index_result = result

                st.success("Repository indexed successfully")

                col1, col2, col3 = st.columns(3)
                col1.metric("Files", result["file_count"])
                col2.metric("Chunks", result["chunk_count"])
                col3.metric(
                    "Vector records",
                    services["vector_store"].count(),
                )

                st.code(result["repo_root"])

            except CodeScopeAIError as exc:
                logger.exception("Indexing failed")
                st.error(f"Application error: {exc}")

            except Exception as exc:
                logger.exception("Unexpected indexing failure")
                st.error(f"Unexpected error: {exc}")

    with tab_chat:
        st.subheader("Ask questions about the codebase")

        question = st.text_area(
            "Question",
            placeholder="Where is logging configured?",
            height=120,
        )

        top_k = st.slider(
            "Top K retrieved chunks",
            min_value=1,
            max_value=20,
            value=5,
        )

        if st.button("Ask CodeScope AI", type="primary"):
            try:
                with st.spinner("Retrieving context and generating answer..."):
                    response = services["answer_service"].answer(
                        question=question,
                        top_k=top_k,
                    )

                    st.session_state.last_response = response

                st.markdown("### Answer")
                st.write(response["answer"])

                st.markdown("### Citations")
                render_citations(response["citations"])

            except CodeScopeAIError as exc:
                logger.exception("Question answering failed")
                st.error(f"Application error: {exc}")

            except Exception as exc:
                logger.exception("Unexpected answer failure")
                st.error(f"Unexpected error: {exc}")

    with tab_docs:
        st.subheader("Generate project documentation")

        if st.button("Generate Project Documentation"):
            try:
                with st.spinner("Generating documentation..."):
                    result = services["project_documenter"].generate()

                st.markdown(result["documentation"])

                st.markdown("### Citations")
                render_citations(result["citations"])

            except CodeScopeAIError as exc:
                logger.exception("Documentation generation failed")
                st.error(f"Application error: {exc}")

            except Exception as exc:
                logger.exception("Unexpected documentation failure")
                st.error(f"Unexpected error: {exc}")

    with tab_debug:
        st.subheader("Retrieval Debug")

        response = st.session_state.get("last_response")

        if not response:
            st.info("Ask a question first to see retrieved context.")
        else:
            render_debug_matches(
                response.get("matches", [])
            )


if __name__ == "__main__":
    main()
