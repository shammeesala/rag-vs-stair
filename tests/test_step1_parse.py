"""Step 1: parse Markdown headings into a section tree."""
from rvs.doc import find, leaves, load, parse_markdown


def test_root_and_chapters(small_doc):
    root = parse_markdown(small_doc)
    assert root.title == "Tiny Doc"
    assert [c.id for c in root.children] == ["1", "2"]
    assert [c.title for c in root.children] == ["Alpha", "Beta"]


def test_nesting_and_parents(small_doc):
    root = parse_markdown(small_doc)
    bananas = root.children[1].children[0]
    assert bananas.id == "2.1"
    assert [c.id for c in bananas.children] == ["2.1.1", "2.1.2"]
    assert bananas.children[0].parent is bananas


def test_text_belongs_to_its_own_heading(small_doc):
    root = parse_markdown(small_doc)
    assert root.children[0].text == "Alpha intro text."
    assert find(root, "1.1").text == "Apples are red. Apples grow on trees."


def test_leaves_in_document_order(small_doc):
    root = parse_markdown(small_doc)
    assert [s.id for s in leaves(root)] == ["1.1", "1.2", "2.1.1", "2.1.2"]


def test_path(small_doc):
    root = parse_markdown(small_doc)
    assert find(root, "2.1.2").path() == ["Beta", "Bananas", "Green bananas"]


def test_handbook(handbook_path):
    root = load(handbook_path)
    assert len(root.children) == 4
    assert len(leaves(root)) == 19
    assert find(root, "2.2.2").title == "Incremental merge"
