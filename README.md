# RAG vs STAIR: chunk retrieval vs structure-aware retrieval

A small, from-scratch project comparing two ways to find the part of a document that answers
a question:

- **RAG-style retrieval:** split the text into chunks, rank chunks with BM25 (built from scratch).
- **STAIR-lite:** learn the document's table of contents and decode a valid section path for each
  question, inspired by STAIR (arXiv:2609.03874).

I'm building this step by step to learn how retrieval works under the hood. The learning path is
in [LEARNING.md](LEARNING.md) and my running notes are in [NOTES.md](NOTES.md).

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                          # tests for every step
python compare.py --misses      # compare all retrievers on 42 held-out questions
python ask.py "how do we stop duplicate records?"
```

## Results

<!-- Fill this in yourself after Step 7, from `python compare.py`. -->

| Method | R@1 | R@3 | MRR |
| --- | --- | --- | --- |
| RAG: fixed 60-word chunks + BM25 | | | |
| RAG: section chunks + BM25 | | | |
| STAIR-lite | | | |

## What I learned

<!-- 3–5 bullets in your own words, written after Step 8. -->

## Project layout

```
data/handbook.md            sample structured document (made up)
data/eval_questions.jsonl   42 questions + the section that answers each
rvs/doc.py                  Markdown -> section tree
rvs/chunking.py             fixed-size and section chunks
rvs/bm25.py                 BM25 ranking
rvs/rag.py                  chunk retriever -> ranked sections
rvs/metrics.py              Recall@k, MRR, evaluation loop
rvs/stair/queries.py        synthetic training questions
rvs/stair/model.py          STAIR-lite: per-node classifiers + beam search over the ToC
compare.py, ask.py          command-line tools
tests/                      one test file per step
```
