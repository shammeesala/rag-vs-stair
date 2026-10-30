"""Step 3: BM25 from scratch."""
import math

import pytest

from rvs.bm25 import BM25

DOCS = [
    ["retry", "timeout", "backoff"],
    ["encrypt", "file", "vendor", "key"],
    ["rotate", "key", "vault", "secret", "key"],
    ["alert", "page", "oncall"],
]


def test_idf_rare_terms_weigh_more():
    bm = BM25(DOCS)
    assert bm.idf("key") < bm.idf("vault")
    assert bm.idf("vault") == pytest.approx(math.log(1 + (4 - 1 + 0.5) / (1 + 0.5)))


def test_score_zero_without_overlap():
    assert BM25(DOCS).score(["banana"], 0) == 0.0


def test_search_ranks_best_match_first():
    hits = BM25(DOCS).search(["rotate", "key"], k=2)
    assert hits[0][0] == 2
    assert hits[1][0] == 1
    assert hits[0][1] > hits[1][1] > 0


def test_term_frequency_saturates():
    bm = BM25([["key"] * 1, ["key"] * 10, ["other"]], k1=1.2, b=0.0)
    one, ten = bm.score(["key"], 0), bm.score(["key"], 1)
    assert ten > one
    assert ten < 2 * one     # 10x the words is NOT 10x the score


def test_search_skips_zero_scores():
    assert BM25(DOCS).search(["banana"]) == []
