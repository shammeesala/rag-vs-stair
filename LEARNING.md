# Learning path: RAG vs STAIR, built one step at a time

Each step has four parts: **learn** (the idea), **build** (functions to fill in), **check** (tests
that pass when you're done), and **reflect** (what to write in `NOTES.md`). Commit after every
step so the history shows how the project grew.

Rules for yourself:
- Write the code yourself. If you ask an AI for help, ask it to *explain* or give a *hint*, not
  to write the function. Note in `NOTES.md` when you did.
- Run the step's tests before moving on. Red tests are information, not failure.
- Read the misses. The numbers tell you *what* happened; the misses tell you *why*.

The sample document is `data/handbook.md`, a made-up engineering handbook (4 chapters,
19 sections). `data/eval_questions.jsonl` has 42 questions with the section that answers each one,
written in different words from the handbook on purpose.

---

## Step 0: Set up (15 min)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                     # everything fails with NotImplementedError. That's the starting line.
git init && git add . && git commit -m "Step 0: project skeleton, data and tests"
```

Read `data/handbook.md` once. Pick three questions from `eval_questions.jsonl` and find the
answer section by hand. Notice how you used the headings to get there. That's STAIR's whole
idea.

## Step 1: The document as a tree (`rvs/doc.py`)

**Learn.** A document's table of contents is a tree. Retrieval can target a *node in that
tree* instead of an arbitrary slice of text.

**Build.** `Section.path`, `parse_markdown`, `leaves`, `find`. Draw the heading stack on paper
for `## 1`, `### 1.1`, `### 1.2`, `## 2` before coding.

**Check.** `pytest tests/test_step1_parse.py`

**Reflect.** What would break if a document had no numbered headings? Or a PDF with no headings?

`git commit -m "Step 1: parse markdown into a section tree"`

## Step 2: Naive chunking (`rvs/chunking.py`: `flatten`, `fixed_size_chunks`)

**Learn.** Most RAG pipelines cut text into fixed windows (say 60 words with 15 overlap) and
index each window. Simple and works for any text, but it ignores headings, and a window can
straddle two topics.

**Build.** `flatten` and `fixed_size_chunks`.

**Check.** `pytest tests/test_step2_chunking.py`

**Reflect.** Print the chunks for the handbook. Find one that mixes two sections. What would
an LLM do with that chunk as context?

`git commit -m "Step 2: fixed-size chunking with overlap"`

## Step 3: BM25 from scratch (`rvs/bm25.py`)

**Learn.** BM25 ranks documents by keyword overlap, weighting rare words more and
stopping repeated words from dominating. It's still a strong baseline and part of most
"hybrid" search systems (including Azure AI Search).

**Build.** The `BM25` class. The formula is at the top of the file.

**Check.** `pytest tests/test_step3_bm25.py`

**Reflect.** In your own words: what do `idf`, `k1` and `b` each do? Why does BM25 fail on
"when do budget alerts fire?" if the text says "Budgets alert the team"? (Hint: tokens.)

`git commit -m "Step 3: BM25 ranking from scratch"`

## Step 4: Measure it (`rvs/metrics.py`, `rvs/rag.py`)

**Learn.** Without an evaluation set you can't tell if a change helped. Recall@k and MRR are
the standard retrieval metrics.

**Build.** `recall_at_k`, `reciprocal_rank`, `evaluate`, `ChunkRetriever.rank_sections`.

**Check.** `pytest tests/test_step4_eval.py`, then your first real result:

```bash
python compare.py --misses
```

**Reflect.** Copy the numbers into `NOTES.md`. Pick three misses and explain each one.

`git commit -m "Step 4: retrieval metrics and fixed-chunk RAG baseline"`

## Step 5: Keep the structure (`section_chunks`)

**Learn.** A cheap way to use structure *inside* RAG: chunk by section, and put the heading
path into the chunk text so the headings' words are searchable too.

**Build.** `section_chunks`.

**Check.** `pytest tests/test_step5_section_chunks.py` and `python compare.py --misses`

**Reflect.** How much did R@1 move? Which earlier misses got fixed, and why?

`git commit -m "Step 5: section-aware chunks"`

## Step 6: Training questions (`rvs/stair/queries.py`)

**Learn.** STAIR stores the document in a model's weights, so it needs (question → section)
training pairs. These are generated from the document, never from the test questions.
Mixing them up ("data leakage") would make your results meaningless.

**Build.** `split_sentences`, `synthesize_queries`.

**Check.** `pytest tests/test_step6_queries.py`

**Reflect.** Print the queries for section 3.4. Would a real person ask any of them?

`git commit -m "Step 6: synthetic training queries per section"`

## Step 7: STAIR-lite (`rvs/stair/model.py`)

**Learn.** STAIR generates a table-of-contents path one level at a time and can only choose
headings that exist. You'll do the same with one small classifier per branching node, and
beam search to keep the few best partial paths.

**Build.** `fit`, `child_probs`, `predict`.

**Check.** `pytest tests/test_step7_stair.py`, then `python compare.py --misses` and
`python ask.py "how do we stop duplicate records?"`

**Reflect.** Does STAIR-lite ever return a section that doesn't exist? Why not? When it's
wrong, is it wrong at the chapter level or deeper? (Print `predict(...).path` for the misses.)

`git commit -m "Step 7: STAIR-lite with constrained beam search over the ToC"`

## Step 8: Experiments (pick at least three)

Each one gets a short entry in `NOTES.md` (what you changed, the numbers, what you learned)
and its own commit.

1. Chunk size: `python compare.py --size 30 --overlap 5` vs `--size 120 --overlap 30`.
2. Add a stemmer or simple plural stripping to `rvs/text.py`. Which method improves most?
3. Change `synthesize_queries`. Which kinds of training queries help STAIR-lite most?
4. **Updates:** add a new section to the handbook. RAG only needs re-indexing; STAIR-lite needs
   retraining. Time both. This is STAIR's main real-world cost.
5. Beam width 1 vs 4 vs 8. When does a wrong early choice (wrong chapter) hurt?
6. Write 10 more evaluation questions of your own, especially hard ones. Do the rankings
   between methods still hold?

## Step 9 (stretch)

- Add an embedding retriever (e.g. `sentence-transformers`) and a hybrid BM25 + embeddings
  ranker with reciprocal rank fusion.
- Generate the final answer with an LLM using the retrieved section as context, and compare
  answers when the context is a straddling chunk vs a whole section.
- Add a GitHub Actions workflow that runs `pytest` on every push.
- Try a real document with structure (a public handbook or RFC) and compare again.

## Reference

STAIR: *STructure Aware Information Retriever: A novel dataset and LLM based retriever for
document structure augmentation*, arXiv:2609.03874 (2026). It fine-tunes a Differentiable Search
Index model to generate table-of-contents paths and reports 82.6% Recall@1 on its SearchTome
benchmark (18 books), compared with 68.7% for DPR and 59.5% for BM25.
STAIR-lite here is a teaching version of the same idea, not a reproduction of the paper.
