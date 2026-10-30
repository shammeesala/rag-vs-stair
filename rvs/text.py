"""Tokenizing helpers shared by every retriever (provided, nothing to implement)."""
import re

STOPWORDS = set("""a an and are as at be by can do does for from has have how i if in is it its
my of on or our should so that the their them then there these this to us was we what when where
which who why will with you your""".split())


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens without stopwords: "How do I rotate keys?" -> ["rotate", "keys"]."""
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]
