"""Local RAG plugin using LangChain + Chroma when available, with offline fallback."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from visionforall.core.events import KBAnswer, KBSource
from visionforall.core.plugin_base import KBPlugin


@dataclass(slots=True)
class DocChunk:
    source: str
    text: str


class LocalRAGKBPlugin(KBPlugin):
    """Offline KB plugin with no network calls by default."""

    name = "local_rag"

    def __init__(self, kb_root: Path, vector_store_dir: Path) -> None:
        self.kb_root = kb_root
        self.vector_store_dir = vector_store_dir
        self.vector_store_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.vector_store_dir / "chunks.txt"

    def ingest(self, path: Path) -> int:
        files = self._collect_files(path)
        chunks: list[DocChunk] = []
        for file in files:
            text = file.read_text(encoding="utf-8", errors="ignore")
            for block in [b.strip() for b in text.split("\n\n") if b.strip()]:
                chunks.append(DocChunk(source=file.name, text=block))

        if self._can_use_langchain():
            return self._ingest_langchain(chunks)

        self.index_file.write_text(
            "\n---\n".join(f"{c.source}\n{c.text}" for c in chunks),
            encoding="utf-8",
        )
        return len(chunks)

    def ask(self, question: str) -> KBAnswer:
        if self._can_use_langchain() and self._chroma_has_content():
            return self._ask_langchain(question)

        if not self.index_file.exists():
            return KBAnswer(
                answer="KB index not found. Run `visionforall ingest-kb <path>` first.",
                sources=[],
            )

        chunks = self._load_chunks()
        ranked = sorted(chunks, key=lambda c: self._score(question, c.text), reverse=True)[:3]

        if not ranked:
            return KBAnswer(answer="No relevant context found.", sources=[])

        summary = " ".join(c.text[:220] for c in ranked)
        sources = [KBSource(filename=c.source, snippet=c.text[:160]) for c in ranked]
        answer = f"Best local answer (heuristic): {summary}"
        return KBAnswer(answer=answer, sources=sources)

    def _collect_files(self, path: Path) -> list[Path]:
        allowed = {".md", ".txt"}
        return [p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in allowed]

    def _load_chunks(self) -> list[DocChunk]:
        content = self.index_file.read_text(encoding="utf-8")
        blocks = [b.strip() for b in content.split("\n---\n") if b.strip()]
        chunks: list[DocChunk] = []
        for block in blocks:
            lines = block.splitlines()
            if not lines:
                continue
            source = lines[0].strip()
            text = "\n".join(lines[1:]).strip()
            if text:
                chunks.append(DocChunk(source=source, text=text))
        return chunks

    @staticmethod
    def _score(query: str, chunk: str) -> int:
        q_terms = {t.lower() for t in query.split() if t.strip()}
        c_lower = chunk.lower()
        return sum(1 for t in q_terms if t in c_lower)

    @staticmethod
    def _can_use_langchain() -> bool:
        import importlib.util

        required = ["langchain", "chromadb", "sentence_transformers"]
        return all(importlib.util.find_spec(name) is not None for name in required)

    def _ingest_langchain(self, chunks: list[DocChunk]) -> int:
        from langchain.schema import Document
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        from langchain_community.vectorstores import Chroma

        docs = [
            Document(page_content=chunk.text, metadata={"source": chunk.source})
            for chunk in chunks
        ]
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        store = Chroma(
            collection_name="visionforall_kb",
            embedding_function=embeddings,
            persist_directory=str(self.vector_store_dir),
        )
        store.add_documents(docs)
        store.persist()
        return len(chunks)

    def _ask_langchain(self, question: str) -> KBAnswer:
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        from langchain_community.vectorstores import Chroma

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        store = Chroma(
            collection_name="visionforall_kb",
            embedding_function=embeddings,
            persist_directory=str(self.vector_store_dir),
        )
        docs = store.similarity_search(question, k=3)
        if not docs:
            return KBAnswer(answer="No relevant context found.", sources=[])

        combined = " ".join(doc.page_content[:220] for doc in docs)
        sources = [
            KBSource(
                filename=str(doc.metadata.get("source", "unknown")),
                snippet=doc.page_content[:160],
            )
            for doc in docs
        ]
        return KBAnswer(answer=f"Best local answer (retrieved): {combined}", sources=sources)

    def _chroma_has_content(self) -> bool:
        chroma_dir = self.vector_store_dir / "chroma.sqlite3"
        return chroma_dir.exists()
