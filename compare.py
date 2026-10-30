"""Run every retriever on the same questions and print a comparison table.

    python compare.py                  # default settings
    python compare.py --size 40 --overlap 10 --misses
"""
import argparse
import json

from rvs.chunking import fixed_size_chunks, section_chunks
from rvs.doc import load
from rvs.metrics import evaluate
from rvs.rag import ChunkRetriever


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", default="data/handbook.md")
    ap.add_argument("--questions", default="data/eval_questions.jsonl")
    ap.add_argument("--size", type=int, default=60, help="words per fixed-size chunk")
    ap.add_argument("--overlap", type=int, default=15)
    ap.add_argument("--misses", action="store_true", help="show questions each method got wrong")
    args = ap.parse_args()

    try:
        root = load(args.doc)
    except NotImplementedError:
        print("Finish Step 1 (rvs/doc.py) first: pytest tests/test_step1_parse.py")
        return
    questions = [json.loads(l) for l in open(args.questions, encoding="utf-8") if l.strip()]
    methods = {}

    def add(name, build):
        try:
            methods[name] = build()
        except NotImplementedError as e:
            print(f"- skipping {name}: not implemented yet ({e})")

    add(f"RAG: fixed {args.size}-word chunks + BM25",
        lambda: ChunkRetriever(fixed_size_chunks(root, args.size, args.overlap)).rank_sections)
    add("RAG: section chunks + BM25", lambda: ChunkRetriever(section_chunks(root)).rank_sections)

    def stair():
        from rvs.stair.model import StairLite
        return StairLite().fit(root).rank_sections
    add("STAIR-lite: learned ToC paths", stair)

    print(f"\n{len(questions)} questions\n")
    print(f"{'method':45} {'R@1':>6} {'R@3':>6} {'MRR':>6}")
    results = {}
    for name, fn in methods.items():
        try:
            r = evaluate(fn, questions)
        except NotImplementedError as e:
            print(f"{name:45} not implemented yet ({e})")
            continue
        results[name] = r
        print(f"{name:45} {r['R@1']:6.2f} {r['R@3']:6.2f} {r['MRR']:6.2f}")
    if args.misses:
        for name, r in results.items():
            print(f"\n== {name}: {len(r['misses'])} misses at rank 1")
            for m in r["misses"]:
                print(f"  gold {m['gold']:6} got {m['got']}  | {m['q']}")


if __name__ == "__main__":
    main()
