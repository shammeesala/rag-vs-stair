"""Step 7: STAIR-lite decodes a valid table-of-contents path."""
import pytest

from rvs.doc import leaves, load
from rvs.stair.model import StairLite


@pytest.fixture(scope="module")
def trained():
    import pathlib
    root = load(str(pathlib.Path(__file__).resolve().parents[1] / "data" / "handbook.md"))
    return root, StairLite().fit(root)


def test_one_classifier_per_branching_node(trained):
    root, model = trained
    branching = [n for n in [root] + list(_walk(root)) if len(n.children) > 1]
    assert set(model.models) == {n.id for n in branching}


def test_predictions_are_always_real_leaves(trained):
    root, model = trained
    valid = {s.id for s in leaves(root)}
    for q in ["completely unrelated question about pizza", "rotate keys", "dead letters"]:
        preds = model.predict(q, k=3)
        assert preds and all(p.section_id in valid for p in preds)   # no hallucinated sections


def test_scores_are_sorted_log_probs(trained):
    _, model = trained
    preds = model.predict("how do I avoid missing late rows?", k=3)
    scores = [p.score for p in preds]
    assert scores == sorted(scores, reverse=True)
    assert all(s <= 0 for s in scores)


def test_easy_questions(trained):
    _, model = trained
    assert model.rank_sections("upsert changed rows since the watermark", k=1) == ["2.2.2"]
    assert model.predict("write a blameless postmortem", k=1)[0].path == ["Operations", "Incident response", "Postmortems"]


def _walk(node):
    for c in node.children:
        yield c
        yield from _walk(c)
