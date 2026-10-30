"""Step 6: make training questions for each section from the document itself.

Real STAIR (and DSI, the method it builds on) fine-tunes a model so the document lives in the
model's weights. To train it you need (question -> section) pairs. Nobody labels those by hand,
so you generate them from the text. This is a tiny version of "doc2query".

The rule that matters: training questions come ONLY from the document. The evaluation
questions in data/eval_questions.jsonl must never be used for training (a test checks this).

Run:   pytest tests/test_step6_queries.py
"""
from __future__ import annotations

import re  # noqa: F401

from ..doc import Section
from ..text import tokenize  # noqa: F401


def split_sentences(text: str) -> list[str]:
    """Split on whitespace that follows . ! or ?   ("One. Two?" -> ["One.", "Two?"])."""
    raise NotImplementedError("Step 6: split_sentences")


def synthesize_queries(section: Section) -> list[str]:
    """Pseudo-questions a user might ask that this section answers. No duplicates.

    Start with these, run the tests, then experiment (and record what changed in NOTES.md):
    - the title, and the full heading path joined with spaces
    - every sentence of the section
    - short keyword versions of each sentence (e.g. the first and second half of its tokens),
      because real questions are short and don't repeat whole sentences
    - the section's most frequent keywords

    Ideas to try later: templates like f"how do I {title}", dropping random words, or, if you
    have an API key, asking an LLM to write 5 questions per section.
    """
    raise NotImplementedError("Step 6: synthesize_queries")
