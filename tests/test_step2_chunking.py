"""Step 2: fixed-size chunks, the way most RAG systems start."""
import pytest

from rvs.chunking import fixed_size_chunks, flatten
from rvs.doc import parse_markdown


def test_flatten_keeps_section_of_every_word(small_doc):
    words = flatten(parse_markdown(small_doc))
    assert words[0] == ("Apples", "1.1")
    assert words[-1] == ("starchy.", "2.1.2")
    assert len(words) == 25


def test_chunk_sizes_and_overlap(small_doc):
    chunks = fixed_size_chunks(parse_markdown(small_doc), size=10, overlap=3)
    words = [c.text.split() for c in chunks]
    assert all(len(w) <= 10 for w in words)
    assert words[0][-3:] == words[1][:3]          # overlap carried into the next chunk
    assert chunks[-1].text.endswith("starchy.")   # nothing dropped at the end
    assert [c.id for c in chunks] == list(range(len(chunks)))


def test_chunk_crossing_sections_lists_majority_first(small_doc):
    chunks = fixed_size_chunks(parse_markdown(small_doc), size=10, overlap=3)
    first = chunks[0]   # 8 words of 1.1 + 2 words of 1.2
    assert first.section_ids == ["1.1", "1.2"]


def test_bad_overlap(small_doc):
    with pytest.raises(ValueError):
        fixed_size_chunks(parse_markdown(small_doc), size=5, overlap=5)
