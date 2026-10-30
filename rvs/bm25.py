"""Step 3: BM25, the classic keyword ranking function, from scratch.

For a query q and document d:

    score(q, d) = sum over terms t in q of
                  idf(t) * f(t,d) * (k1 + 1) / ( f(t,d) + k1 * (1 - b + b * |d| / avgdl) )

    idf(t) = ln( 1 + (N - n(t) + 0.5) / (n(t) + 0.5) )

    f(t,d)  how many times t appears in d          N       number of documents
    |d|     length of d in tokens                  avgdl   average document length
    n(t)    number of documents containing t       k1, b   tuning knobs (1.5 and 0.75)

What each part does (write this in your own words in NOTES.md once it clicks):
- idf: rare words ("vault") matter more than common ones ("key").
- k1: term frequency saturates; the 10th "key" adds much less than the 1st.
- b: long documents are penalized a little, so they don't win just by having more words.

Run:   pytest tests/test_step3_bm25.py
"""
from __future__ import annotations

import math  # noqa: F401  (you'll need math.log)
from collections import Counter  # noqa: F401


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        """docs: already-tokenized documents. Precompute what score() needs:
        N, avgdl, a Counter of term frequencies per doc, and document frequency per term."""
        raise NotImplementedError("Step 3: BM25.__init__")

    def idf(self, term: str) -> float:
        raise NotImplementedError("Step 3: BM25.idf")

    def score(self, query: list[str], i: int) -> float:
        """BM25 score of document i for the tokenized query."""
        raise NotImplementedError("Step 3: BM25.score")

    def search(self, query: list[str], k: int = 5) -> list[tuple[int, float]]:
        """Top-k (doc index, score), best first, skipping documents that score 0.
        Break ties by lower index so results are deterministic."""
        raise NotImplementedError("Step 3: BM25.search")
