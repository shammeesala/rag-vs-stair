"""Ask one question and see what each retriever returns.

    python ask.py "how do we stop duplicate records?"
"""
import sys

from rvs.chunking import fixed_size_chunks
from rvs.doc import find, load
from rvs.rag import ChunkRetriever
from rvs.stair.model import StairLite


def main():
    q = " ".join(sys.argv[1:]) or input("question: ")
    root = load("data/handbook.md")
    rag = ChunkRetriever(fixed_size_chunks(root))
    print("\n--- RAG (top chunks) ---")
    for chunk, score in rag.search_chunks(q, k=3):
        print(f"[{score:5.2f}] sections {chunk.section_ids}: {chunk.text[:160]}...")
    print("\n--- STAIR-lite (decoded paths) ---")
    for p in StairLite().fit(root).predict(q, k=3):
        print(f"[{p.score:6.2f}] {p.section_id}  {' > '.join(p.path)}")
    best = StairLite().fit(root).predict(q, k=1)[0]
    print("\nSTAIR-lite answer section text:\n" + find(root, best.section_id).text)


if __name__ == "__main__":
    main()
