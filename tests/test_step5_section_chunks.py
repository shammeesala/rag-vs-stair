"""Step 5: keep the structure: one chunk per section, prefixed with its heading path."""
from rvs.chunking import section_chunks
from rvs.doc import load, parse_markdown


def test_one_chunk_per_leaf(small_doc):
    chunks = section_chunks(parse_markdown(small_doc))
    assert [c.section_ids for c in chunks] == [["1.1"], ["1.2"], ["2.1.1"], ["2.1.2"]]


def test_heading_path_is_in_the_text(small_doc):
    c = section_chunks(parse_markdown(small_doc))[3]
    assert "Beta" in c.text and "Green bananas" in c.text and "starchy" in c.text


def test_handbook_sections(handbook_path):
    assert len(section_chunks(load(handbook_path))) == 19
