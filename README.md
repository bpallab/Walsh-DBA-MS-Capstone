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

Raw data is **not** stored in this repository; `notebooks/01_data_acquisition_and_profile.ipynb` downloads it. See [`data/README.md`](data/README.md) and the [data dictionary](data/data_dictionary.md).

## How to reproduce
1. Open a notebook in Google Colab (File → Open notebook → GitHub → `bpallab/Walsh-DBA-MS-Capstone`).
2. Run all cells. Notebook 01 clones this repo, installs `requirements.txt`, mounts Google Drive and stores raw data under `MyDrive/Walsh DBA/QM640 Capstone/data`.

| Notebook | Purpose | Status |
|---|---|---|
| 00_sample_size | Power / confidence-interval calculations (Table 4) | ✅ |
| 01_data_acquisition_and_profile | Download, clean, profile; friction and time-to-action measures | ✅ |
| 02_rq1_model_comparison | Train/run instruments on the 385-ticket test set | planned (weeks 4–5) |
| 03_rq2_routing | Cascade thresholds, cost analysis, risk–coverage | planned (week 6) |
| 04_rq3_context | Instrument × context experiment | planned (week 7) |
| 05_rq4_replay_compiler | Month-by-month replay with rule compiler | planned (weeks 8–9) |
| 06_allocation_tree | CART allocation decision tree | planned (week 9) |

## Repository layout
```
├── data/                 README, data dictionary (raw data downloaded, not committed)
├── notebooks/            numbered analysis notebooks
├── src/capstone/         data loaders, instruments, router, compiler, evaluation
├── configs/prices.yaml   model prices used for commercial-equivalent cost
├── results/              tables and figures produced by the notebooks
└── requirements.txt
```

## Cost policy
No paid API spending: small and fine-tuned models run on Google Colab; commercial models are called through existing subscriptions (Claude plan, Gemini API free tier), with several tickets per request.

## Licence
Code: MIT. Data: the licence of each source dataset applies; cite the sources listed above.
