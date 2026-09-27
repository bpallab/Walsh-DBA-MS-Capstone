# Data

## Why these three datasets
The study needs **real** enterprise IT service data (not synthetic) that covers the whole chain of ticket decisions. No single public dataset does that, so three complementary ones are combined:

| Need | Rabobank (BPI 2014) | ServiceNow (UCI) | Jira (MSR 2022) |
|---|---|---|---|
| Real enterprise ITSM process (ITIL) | ✅ bank | ✅ IT company | partly (engineering) |
| Links from incidents to the changes that caused them | ✅ | – | partly ("causes" links) |
| Team handoffs and reassignments (friction) | ✅ | ✅ | ✅ (assignee history) |
| Free-text ticket descriptions for language models | – | – | ✅ |
| Real duplicate links | – | – | ✅ |
| Long history for month-by-month replay | – | – | ✅ (many years) |

## 1. Rabobank ITSM log (BPI Challenge 2014)
**What it is:** an extract from the IT service management tool (HP Service Manager) of Rabobank Group ICT, the IT function of a large Dutch bank. Four linked files follow the ITIL process:
- **interactions:** calls and e-mails to the service desk
- **incidents:** escalated when the desk cannot resolve at first contact
- **incident activities:** each step taken on an incident
- **changes:** planned changes to IT systems

**In an enterprise setting:** this is how a bank's IT operations actually runs. A user reports a problem, the service desk logs it, the incident moves between support teams, and some incidents turn out to have been caused by a recent change. Rabobank released the data to learn how changes drive service-desk workload.

**Why chosen:** one of very few real ITSM extracts from a **bank**, matching the BFSI (banking, financial services and insurance) focus of the research. It is the only public source that links incidents to their **causing changes**, the ground truth for cause identification (D6). Its reassignment counts and first-call-resolution flags measure friction and service-desk (L1) workload.

**Limitation:** anonymised, 2013–2014, no free-text descriptions.

## 2. ServiceNow incident event log (UCI 498)
**What it is:** an anonymised audit log from the ServiceNow platform of a real IT company: 141,712 events for 24,918 incidents. Every update to a ticket is a row, recording state, category, priority, assigned team, reassignments, knowledge-base use and whether the service-level target was met.

**In an enterprise setting:** ServiceNow is the most widely used enterprise ITSM platform. The log shows the full lifecycle of an incident as a CIO's operations team sees it.

**Why chosen:** real data from the platform most enterprises use. It supplies labels for classification (D1), team assignment (D5) and knowledge use (D3), and its reassignment and SLA fields quantify the cost of wrong first decisions. It is also a second, independent enterprise, so findings do not rest on one organisation.

**Limitation:** category and team codes are anonymised; no ticket text.

## 3. The Public Jira Dataset (v7, 2025)
**What it is:** 2.7 million real issues from 16 public Jira instances run by organisations such as Apache, Red Hat and MongoDB, with 9 million comments, 1 million issue links and full change histories. Personal information has been anonymised by the authors.

**In an enterprise setting:** Jira holds the engineering side of IT operations: defects, tasks and problems that reach second- and third-level (L2/L3) support, where assignment, duplicate detection and root-cause work cost the most.

**Why chosen:** the only large, real, public source of **ticket text** with **real outcomes** (type, priority, component, assignee, resolution, and explicit duplicate and "causes" links). That is what language-model, retrieval and knowledge-graph instruments need to be tested fairly. Its years of history allow the month-by-month replay of the intelligence compiler (RQ4).

**Limitation:** an engineering issue tracker, not an end-user service desk.

## Full data vs. samples in this repository
- **Full data** stays with the original publishers and is downloaded by `notebooks/01_data_acquisition_and_profile.ipynb`. It is not redistributed here.
- **Samples** (`data/samples/`): cleaned random extracts, 500 cases per dataset with a fixed random seed, so readers can see real records. Person-level fields are removed and free text is screened for e-mail addresses, phone numbers and IP addresses.

| Sample | File | Status |
|---|---|---|
| Rabobank incidents | [rabobank_incident_sample.csv]() | to be added |
| Rabobank changes | [rabobank_change_sample.csv]() | to be added |
| ServiceNow incidents | [servicenow_sample.csv]() | to be added |
| Jira issues | [jira_sample.csv]() | to be added |
| Sampling and cleaning notes | [SAMPLE_NOTES.md]() | to be added |

## Sources and licences
| Dataset | Citation | Licence |
|---|---|---|
| Rabobank | van Dongen, B. F. (2014). *BPI Challenge 2014*. 4TU.ResearchData. https://data.4tu.nl/collections/_/5065469/1 | to be confirmed on 4TU page |
| ServiceNow | Amaral, C., Fantinato, M., & Peres, S. (2018). *Incident management process enriched event log*. UCI Machine Learning Repository. https://doi.org/10.24432/C57S4H | CC BY 4.0 |
| Jira | Montgomery, L., Lüders, C., & Maalej, W. (2022). An alternative issue tracking dataset of public Jira repositories. MSR 2022. https://zenodo.org/records/15719919 | CC BY 4.0 |
