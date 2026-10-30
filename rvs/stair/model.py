"""Step 7: STAIR-lite. Learn the table of contents, then decode a valid path for a question.

The real STAIR fine-tunes a language model to *generate* a path such as
"Data pipelines > Load types > Incremental merge", one level at a time, and only lets it pick
headings that actually exist (constrained decoding). That is why it almost never invents a
section.

STAIR-lite keeps the same shape with small, fast models:
- one classifier per node that has 2+ children: "given this question, which child?"
- predict() walks the tree from the root with beam search, multiplying the probabilities
  along each path (adding log-probabilities), and keeps the best `beam` partial paths.
Because it can only move to real children, every prediction is a real section.

Run:   pytest tests/test_step7_stair.py
"""
from __future__ import annotations

import math  # noqa: F401
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline, make_union

from ..doc import Section, leaves  # noqa: F401
from .queries import synthesize_queries  # noqa: F401


@dataclass
class Prediction:
    section_id: str
    score: float          # log-probability of the whole path (0 is certain, more negative is less sure)
    path: list[str]       # titles along the decoded path


def make_classifier():
    """Provided: word 1-2 grams + character 3-5 grams (so "encrypted" still matches "encrypt"),
    fed into logistic regression. You can swap this later (that's a good experiment)."""
    features = make_union(
        TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english"),
        TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True),
    )
    return make_pipeline(features, LogisticRegression(C=10, max_iter=2000))


class StairLite:
    def __init__(self, beam: int = 4):
        self.beam = beam
        self.models: dict[str, object] = {}   # node id -> fitted classifier
        self.root: Section | None = None

    def fit(self, root: Section) -> "StairLite":
        """Train one classifier for every node with 2+ children. Return self.

        TODO for each such node:
        - X = synthesized queries of every leaf under child 0, child 1, ...
        - y = the child's index (0, 1, ...) repeated for each of those queries
        - self.models[node.id] = make_classifier().fit(X, y)
        Then recurse into the children. Nodes with exactly one child need no model.
        """
        raise NotImplementedError("Step 7: StairLite.fit")

    def child_probs(self, node: Section, question: str) -> list[tuple[Section, float]]:
        """(child, probability) pairs for one node, most likely first.

        A node with one child returns [(that child, 1.0)]. Otherwise use
        self.models[node.id].predict_proba([question])[0]; the i-th probability is child i.
        """
        raise NotImplementedError("Step 7: StairLite.child_probs")

    def predict(self, question: str, k: int = 3) -> list[Prediction]:
        """Beam search from the root down to leaves; return the k best Predictions.

        TODO:
        - beams = [(self.root, 0.0)]   # (node, total log-prob)
        - while any beam is not a leaf: expand every non-leaf beam into its top `self.beam`
          children (adding math.log(p)), keep finished leaves as they are, sort by score and
          keep the best `self.beam`.
        - Build Prediction(node.id, score, node.path()) for the best k.
        Guard against log(0) with max(p, 1e-12).
        """
        raise NotImplementedError("Step 7: StairLite.predict")

    def rank_sections(self, question: str, k: int = 3) -> list[str]:
        """Provided: just the section ids, so compare.py can evaluate it like RAG."""
        return [p.section_id for p in self.predict(question, k=k)]
