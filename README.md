# Walsh-DBA-MS-Capstone
My AI-ML masters capstone project, on Enterprise Agentic Intelligence.

## Choosing the Right Intelligence for Each Decision

**QM640 Data Analytics Capstone · Walsh College · Pallab Bhattacharya · Fall 2026**

A cost–accuracy comparison of traditional machine learning, small language models and large language models across the chain of IT ticket decisions, using **real, public IT service management data**. The study ends with an *allocation decision tree* that recommends which intelligence instrument to use for each kind of decision, and tests how the answer shifts as validated decisions are compiled into business rules over time.

## Research questions
| RQ | Question | Main tests |
|---|---|---|
| RQ1 | Can low-cost instruments (traditional ML, fast decision model, small LMs) match large LLMs on routine ticket decisions at a fraction of the cost? | Cochran's Q, McNemar (Holm), non-inferiority |
| RQ2 | Does "cheapest instrument first, escalate when unsure" routing cut cost without reducing accuracy? | Paired non-inferiority, bootstrap CI, risk–coverage |
| RQ3 | Does company history (similar-ticket search, knowledge graph) let cheaper instruments match expensive ones? | Two-way ANOVA / Friedman |
| RQ4 | Replayed month by month, how fast do compiled rules grow and cost per ticket fall? | Log–log regression, Kaplan–Meier |

## Decisions and instruments
**Decisions:** D1 classify · D2 duplicate · D3 knowledge · D4 next action · D5 assign team · D6 cause · D7 resolution summary
**Instruments:** I1 TF-IDF + XGBoost/Random Forest · I2 similar-ticket search (RAG) · I3 knowledge graph · I4 Jev fast decision model · I5 small LM · I6 fine-tuned small LM (LoRA) · I7 medium LLM · I8 large LLM · **C** compiled business rules (start empty, grow over time)

## Data (all real and public)
| Dataset | Source | Licence |
|---|---|---|
| ServiceNow incident event log (141,712 events, 24,918 incidents) | [UCI ML Repository #498](https://archive.ics.uci.edu/dataset/498) | CC BY 4.0 |
| Rabobank ITSM log, BPI Challenge 2014 | [4TU.ResearchData](https://data.4tu.nl/collections/_/5065469/1) | see 4TU record |
| The Public Jira Dataset v7 (2.7M issues, anonymised) | [Zenodo 15719919](https://zenodo.org/records/15719919) | CC BY 4.0 |

The ServiceNow and Rabobank files are included in full under `data/raw/` (both public). The 5.8 GB Jira archive is too large for GitHub; `notebooks/02_jira_subset.ipynb` downloads it from Zenodo and extracts the subset used. See [`data/README.md`](data/README.md) and the [data dictionary](data/data_dictionary.md).

## How to reproduce
1. Open a notebook in Google Colab (File → Open notebook → GitHub → `bpallab/Walsh-DBA-MS-Capstone`).
2. Run all cells. Notebooks mount Google Drive and read/write `MyDrive/Walsh DBA/Doctoral Research/QM640/Data` (copy `data/raw/` there first, or let notebook 01 download ServiceNow).

| Notebook | Purpose | Status |
|---|---|---|
| 00_sample_size | Power / confidence-interval calculations | ✅ |
| 01_data_profile | Load, clean, profile; data dictionary, cleaning log, EDA figures and insights | ✅ |
| 02_jira_subset | Download the Jira dump and extract Apache, Red Hat, MongoDB issues | ✅ built, running |
| 03_split_baselines | Time-based split, 385-ticket test sets, I1 baselines (RQ1), risk–coverage (RQ2), rule preview (RQ4) | ✅ |
| 04_jira_testsets_i1 | Jira test sets for D1, D2, D4, D5, D6 and full I1 baseline (TF-IDF classifiers and lexical search) | ✅ |
| 04b_jira_d2_d6 | Jira duplicate (D2) and cause (D6) test sets and I1 search, low-memory | ✅ |
| 05_i2_i3_context | I2 embeddings and similar-ticket search, I3 knowledge graph, hybrid search, RQ3 context files (T4 GPU) | ✅ |
| 06_i5_i6_slm | I5 Qwen3-4B as is and I6 LoRA fine-tune; RQ3 context runs (L4 GPU) | ✅ |
| 08_i4_jev | Instrument I4 (Jev): RQ1 test sets, consistency check, re-ranking, bulk run for RQ2/RQ4 | ✅ |
| 07, 09–10 | Language-model instruments, RQ2 cascade, RQ3 context, RQ4 replay, allocation tree | in progress |

## Repository layout
```
├── data/raw/             ServiceNow (zip) and Rabobank BPI 2014 (4 CSV files), as published
├── data/processed/       incident-level Parquet tables and held-out test-set ids
├── notebooks/            numbered analysis notebooks (Colab)
├── src/capstone/         data loaders, Jira dump reader, instruments, router, compiler, evaluation
├── configs/prices.yaml   dated price table for cost of ownership
├── results/              tables (CSV, summaries) and figures produced by the notebooks
└── requirements.txt
```

## Cost policy
Core experiments use Google Colab, open models and the Gemini API free tier. Paid calls (Jev API; a small commercial frontier-model cross-check sample) are estimated and approved before each run, and raw responses are stored.

## Licence
Code: MIT. Data: the licence of each source dataset applies; cite the sources listed above.
