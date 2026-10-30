"""Steps 2 and 5: cut the document into chunks the way RAG does.

Step 2 (fixed_size_chunks) is how most RAG tutorials start: ignore headings, slide a window of
N words over the text. Step 5 (section_chunks) keeps the structure instead.

Run:   pytest tests/test_step2_chunking.py      and later      pytest tests/test_step5_section_chunks.py
"""
from __future__ import annotations

from dataclasses import dataclass

from .doc import Section, leaves


@dataclass
class Chunk:
    id: int
    text: str
    section_ids: list[str]   # sections this chunk's words came from, most words first


def flatten(root: Section) -> list[tuple[str, str]]:
    """Every word of the document body, in order, tagged with the leaf section it came from.

    [("New", "1.1"), ("engineers", "1.1"), ..., ("Friday.", "4.5")]
    Use leaf.text.split(), so punctuation stays attached to words. Headings are NOT included:
    that's exactly the information naive chunking throws away.
    """
    raise NotImplementedError("Step 2: flatten")


def fixed_size_chunks(root: Section, size: int = 60, overlap: int = 15) -> list[Chunk]:
    """Slide a window of `size` words, moving forward `size - overlap` words each time.

    TODO:
    - Raise ValueError unless 0 <= overlap < size (otherwise the window never moves).
    - Each chunk's text is its words joined with spaces; ids are 0, 1, 2, ...
    - section_ids: the sections that appear in the window, the one with the most words first
      (break ties by whichever appears first). collections.Counter helps.
    - Stop once a window reaches the last word; don't emit an extra tiny chunk.

    Question to answer in NOTES.md: what happens to a sentence that sits on a chunk border?
    """
    raise NotImplementedError("Step 2: fixed_size_chunks")


def section_chunks(root: Section) -> list[Chunk]:
    """Step 5: one chunk per leaf section, text = its heading path + its body.

    Chunk(id, "Data pipelines > Load types > Full load. A full load replaces ...", ["2.2.1"])
    """
    raise NotImplementedError("Step 5: section_chunks")
