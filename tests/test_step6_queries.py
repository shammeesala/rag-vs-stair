"""Step 6: training questions generated from each section."""
from rvs.doc import find, load
from rvs.stair.queries import split_sentences, synthesize_queries


def test_split_sentences():
    assert split_sentences("One. Two? Three!") == ["One.", "Two?", "Three!"]


def test_queries_cover_title_and_sentences(handbook_path):
    sec = find(load(handbook_path), "3.4")
    qs = synthesize_queries(sec)
    assert any("Idempotency" in q for q in qs)
    assert any("event identifier" in q for q in qs)
    assert len(qs) >= 5
    assert len(qs) == len(set(qs)), "no duplicates"


def test_no_leakage_from_eval_questions(handbook_path):
    import json, pathlib
    evalq = {json.loads(l)["q"] for l in open(pathlib.Path(handbook_path).with_name("eval_questions.jsonl"))}
    root = load(handbook_path)
    from rvs.doc import leaves
    for leaf in leaves(root):
        assert not evalq & set(synthesize_queries(leaf)), "training queries must come from the document only"
