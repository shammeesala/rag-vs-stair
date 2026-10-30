"""Step 4: a chunk retriever that answers "which section?" so it can be compared with STAIR.

RAG returns chunks; STAIR returns sections. To compare them fairly we turn the ranked chunks
into a ranked list of sections.

Run:   pytest tests/test_step4_eval.py
"""
from __future__ import annotations

from .bm25 import BM25
from .chunking import Chunk
from .text import tokenize


class ChunkRetriever:
    def __init__(self, chunks: list[Chunk]):
        """Provided: index each chunk's tokenized text with your BM25."""
        self.chunks = chunks
        self.index = BM25([tokenize(c.text) for c in chunks])

    def search_chunks(self, question: str, k: int = 5) -> list[tuple[Chunk, float]]:
        """Provided: the top-k chunks with their BM25 scores."""
        return [(self.chunks[i], s) for i, s in self.index.search(tokenize(question), k)]

    def rank_sections(self, question: str, k: int = 3) -> list[str]:
        """Section ids ranked by their best chunk, without duplicates, at most k.

        TODO: search all chunks, walk them best-first, take each chunk's main section
        (section_ids[0]) and keep it if it isn't in the list yet. Stop at k.
        """
        raise NotImplementedError("Step 4: rank_sections")
