"""Step 4: retrieval metrics.

- Recall@k: did the right section show up in the top k? (1 or 0 per question, then averaged)
- MRR (mean reciprocal rank): 1 if it's first, 1/2 if second, 1/3 if third, 0 if missing.
  It rewards putting the right answer near the top, not just somewhere in the list.

Run:   pytest tests/test_step4_eval.py
"""
from __future__ import annotations

from typing import Callable


def recall_at_k(ranked: list[str], gold: str, k: int) -> float:
    raise NotImplementedError("Step 4: recall_at_k")


def reciprocal_rank(ranked: list[str], gold: str) -> float:
    raise NotImplementedError("Step 4: reciprocal_rank")


def evaluate(rank_fn: Callable[[str], list[str]], questions: list[dict], ks=(1, 3)) -> dict:
    """Run rank_fn on every {"q": ..., "gold": ...} question and average the metrics.

    Return {"R@1": ..., "R@3": ..., "MRR": ..., "misses": [...]} where misses lists
    {"q", "gold", "got": top 3} for every question whose first result is wrong.
    Reading the misses is where most of the learning happens.
    """
    raise NotImplementedError("Step 4: evaluate")
