"""Step 1: turn a Markdown document into a tree of sections (its table of contents).

STAIR's whole idea is that a document already has structure: chapters, sections, subsections.
Before we can use that structure we need it as data. That is this file.

Run the tests for this step with:   pytest tests/test_step1_parse.py
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

# Matches a heading line like "### 2.2.1 Full load":
#   group(1) = "###"     -> level 3
#   group(2) = "2.2.1"   -> section id (may be missing, e.g. the document title)
#   group(3) = "Full load"
HEADING = re.compile(r"^(#{1,6})\s+(?:(\d+(?:\.\d+)*)\s+)?(.+?)\s*$")


@dataclass
class Section:
    id: str                      # "2.2.1"; the root (document title) uses ""
    title: str                   # "Full load"
    level: int                   # number of "#" in the heading (root = 1)
    text: str = ""               # body text directly under this heading (not its children's)
    children: list[Section] = field(default_factory=list)
    parent: Optional[Section] = field(default=None, repr=False)

    @property
    def is_leaf(self) -> bool:
        return not self.children

    def path(self) -> list[str]:
        """Titles from the top chapter down to this section, root excluded.

        find(root, "2.2.1").path() == ["Data pipelines", "Load types", "Full load"]

        TODO: walk up through .parent until you reach the root (the node whose parent is None),
        collecting titles, then reverse the list.
        """
        titles = []
        current = self

        while current.parent is not None:
            titles.append(current.title)
            current = current.parent

        return titles[::-1]
        # raise NotImplementedError("Step 1: Section.path")


def parse_markdown(md: str) -> Section:
    """Build the section tree and return the root (the "# Title" line).

    TODO:
    - Go line by line. Use HEADING.match(line) to spot headings.
    - The first heading becomes the root.
    - Keep a stack of open sections. For a new heading at level L, pop the stack until the
      top has a level smaller than L; that top is the new section's parent.
      (Draw this on paper for "## 1", "### 1.1", "### 1.2", "## 2" before coding it.)
    - Non-heading, non-blank lines are body text: append them (space-separated, stripped) to
      the .text of the section currently on top of the stack.
    - Raise ValueError if the document has no headings.
    """

    root = None
    stack = []

    # a list fo strings 
    for line in md.splitlines():
        line = line.strip()

        # Check whether this line is a heading
        match = HEADING.match(line)

        if match:
            level = len(match.group(1))  # Number of # symbols
            section_id = match.group(2) or ""
            title = match.group(3)

            section = Section(
                id=section_id,
                title=title,
                level=level
            )

            # The first heading becomes the root
            if root is None:
                root = section
                stack.append(section)
                continue

            # Remove headings at the same or deeper level
            while stack and stack[-1].level >= level:
                stack.pop()

            if not stack:
                raise ValueError("Heading has no parent")

            parent = stack[-1]
            section.parent = parent
            parent.children.append(section)

            stack.append(section) # New section becomes current

        # Add non-empty body text to the current section
        elif line and stack:
            # Add body text to the current section
            current = stack[-1]

            if current.text:
                current.text += " "

            current.text += line

    if root is None:
        raise ValueError("Document has no headings")

    return root


    # raise NotImplementedError("Step 1: parse_markdown")


def leaves(root: Section) -> list[Section]:
    """All sections without children, in document order (recursion is the easy way)."""

    """Return all leaf sections in document order."""

    result = []

    def visit(section):
        if not section.children:
            result.append(section)  # Found a leaf
            return

        for child in section.children:
            visit(child)  # Explore children in order

    visit(root)
    return result

    # raise NotImplementedError("Step 1: leaves")


def find(root: Section, section_id: str) -> Section:
    """The section with this id anywhere in the tree. Raise KeyError if it doesn't exist."""

    if root.id == section_id:
        return root  # Found the section

    for child in root.children:
        try:
            return find(child, section_id)  # Search child subtree
        except KeyError:
            continue  # Not found here, try next child

    raise KeyError(section_id)

    #raise NotImplementedError("Step 1: find")


def load(path: str) -> Section:
    """Read a Markdown file and parse it (provided)."""
    with open(path, encoding="utf-8") as f:
        return parse_markdown(f.read())
