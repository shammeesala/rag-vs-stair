"""Step 4: metrics, and turning chunk hits into section rankings."""
import pytest

from rvs.chunking import Chunk
from rvs.metrics import evaluate, reciprocal_rank, recall_at_k
from rvs.rag import ChunkRetriever


def test_recall_at_k():
    assert recall_at_k(["a", "b", "c"], "b", 1) == 0.0
    assert recall_at_k(["a", "b", "c"], "b", 2) == 1.0


def test_reciprocal_rank():
    assert reciprocal_rank(["a", "b", "c"], "c") == pytest.approx(1 / 3)
    assert reciprocal_rank(["a"], "z") == 0.0


def test_evaluate_averages():
    qs = [{"q": "x", "gold": "a"}, {"q": "y", "gold": "b"}]
    res = evaluate(lambda q: ["a", "b"], qs, ks=(1, 2))
    assert res["R@1"] == pytest.approx(0.5)
    assert res["R@2"] == pytest.approx(1.0)
    assert res["MRR"] == pytest.approx(0.75)
    assert len(res["misses"]) == 1


def test_rank_sections_dedupes_and_uses_primary_section():
    chunks = [
        Chunk(0, "rotate the vault key", ["4.4", "4.3"]),
        Chunk(1, "key rotation for vendor key files", ["2.4"]),
        Chunk(2, "vault key again rotate", ["4.4"]),
    ]
    ranked = ChunkRetriever(chunks).rank_sections("rotate vault key", k=3)
    assert ranked[0] == "4.4"
    assert ranked.count("4.4") == 1
    assert set(ranked) <= {"4.4", "2.4"}
