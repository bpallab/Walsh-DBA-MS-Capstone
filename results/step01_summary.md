# Step 01 summary — 2026-10-18 04:34

## ServiceNow
- events: 141,712; incidents: 24,918; columns: 36
- opened_at range: 2016-02-29 01:16:00 to 2017-02-16 14:17:00

## Rabobank BPI 2014
- files found: ['Detail_Incident.csv', 'Detail_Interaction.csv', 'Detail_Incident_Activity.csv', 'Detail_Change.csv']
- incident: 46,809 rows x 28 cols; columns: ['ci_name_aff', 'ci_type_aff', 'ci_subtype_aff', 'service_component_wbs_aff', 'incident_id', 'status', 'impact', 'urgency', 'priority', 'category', 'km_number', 'alert_status', 'n_reassignments', 'open_time', 'reopen_time', 'resolved_time', 'close_time', 'handle_time_hours', 'closure_code', 'n_related_interactions', 'related_interaction', 'n_related_incidents', 'n_related_changes', 'related_change', 'ci_name_cby', 'ci_type_cby', 'ci_subtype_cby', 'servicecomp_wbs_cby']
- interaction: 147,004 rows x 17 cols; columns: ['ci_name_aff', 'ci_type_aff', 'ci_subtype_aff', 'service_comp_wbs_aff', 'interaction_id', 'status', 'impact', 'urgency', 'priority', 'category', 'km_number', 'open_time_first_touch', 'close_time', 'closure_code', 'first_call_resolution', 'handle_time_secs', 'related_incident']
- incident_activity: 466,737 rows x 7 cols; columns: ['incident_id', 'datestamp', 'incidentactivity_number', 'incidentactivity_type', 'assignment_group', 'km_number', 'interaction_id']
- change: 30,275 rows x 21 cols; columns: ['ci_name_aff', 'ci_type_aff', 'ci_subtype_aff', 'service_component_wbs_aff', 'change_id', 'change_type', 'risk_assessment', 'emergency_change', 'cab_approval_needed', 'planned_start', 'planned_end', 'scheduled_downtime_start', 'scheduled_downtime_end', 'actual_start', 'actual_end', 'requested_end_date', 'change_record_open_time', 'change_record_close_time', 'originated_from', 'n_related_interactions', 'n_related_incidents']

## Workload profile
|                                          |   ServiceNow |   Rabobank |
|:-----------------------------------------|-------------:|-----------:|
| incidents                                |     24918    |   46809    |
| mean friction count (teams per incident) |         1.94 |       2.13 |
| % incidents handled by >1 team           |        45.63 |      40.88 |
| % knowledge-base used                    |        14.25 |     nan    |
| % SLA met                                |        63.42 |     nan    |
| median resolution hours                  |        22.1  |      18.76 |
| % incidents linked to a change           |       nan    |       1.2  |

## sn_prof
| dataset           | variable                | dtype          |   missing_pct |   distinct | example             |
|:------------------|:------------------------|:---------------|--------------:|-----------:|:--------------------|
| ServiceNow events | number                  | str            |           0   |      24918 | INC0000045          |
| ServiceNow events | incident_state          | str            |           0   |          9 | New                 |
| ServiceNow events | active                  | bool           |           0   |          2 | True                |
| ServiceNow events | reassignment_count      | int64          |           0   |         28 | 0                   |
| ServiceNow events | reopen_count            | int64          |           0   |          9 | 0                   |
| ServiceNow events | sys_mod_count           | int64          |           0   |        115 | 0                   |
| ServiceNow events | made_sla                | bool           |           0   |          2 | True                |
| ServiceNow events | caller_id               | str            |           0   |       5244 | Caller 2403         |
| ServiceNow events | opened_by               | str            |           3.4 |        207 | Opened by  8        |
| ServiceNow events | opened_at               | datetime64[us] |           0   |      19849 | 2016-02-29 01:16:00 |
| ServiceNow events | sys_created_by          | str            |          37.5 |        185 | Created by 6        |
| ServiceNow events | sys_created_at          | datetime64[us] |          37.5 |      11552 | 2016-02-29 01:23:00 |
| ServiceNow events | sys_updated_by          | str            |           0   |        846 | Updated by 21       |
| ServiceNow events | sys_updated_at          | datetime64[us] |           0   |      50664 | 2016-02-29 01:23:00 |
| ServiceNow events | contact_type            | str            |           0   |          5 | Phone               |
| ServiceNow events | location                | str            |           0.1 |        224 | Location 143        |
| ServiceNow events | category                | str            |           0.1 |         58 | Category 55         |
| ServiceNow events | subcategory             | str            |           0.1 |        254 | Subcategory 170     |
| ServiceNow events | u_symptom               | str            |          23.3 |        525 | Symptom 72          |
| ServiceNow events | cmdb_ci                 | str            |          99.7 |         50 | cmdb_ci 31          |
| ServiceNow events | impact                  | str            |           0   |          3 | 2 - Medium          |
| ServiceNow events | urgency                 | str            |           0   |          3 | 2 - Medium          |
| ServiceNow events | priority                | str            |           0   |          4 | 3 - Moderate        |
| ServiceNow events | assignment_group        | str            |          10   |         78 | Group 56            |
| ServiceNow events | assigned_to             | str            |          19.4 |        234 | Resolver 89         |
| ServiceNow events | knowledge               | bool           |           0   |          2 | True                |
| ServiceNow events | u_priority_confirmation | bool           |           0   |          2 | False               |
| ServiceNow events | notify                  | str            |           0   |          2 | Do Not Notify       |
| ServiceNow events | problem_id              | str            |          98.4 |        252 | Problem ID  2       |
| ServiceNow events | rfc                     | str            |          99.3 |        181 | CHG0000404          |
| ServiceNow events | vendor                  | str            |          99.8 |          4 | code 8s             |
| ServiceNow events | caused_by               | str            |         100   |          3 | CHG0000132          |
| ServiceNow events | closed_code             | str            |           0.5 |         17 | code 5              |
| ServiceNow events | resolved_by             | str            |           0.2 |        216 | Resolved by 149     |
| ServiceNow events | resolved_at             | datetime64[us] |           2.2 |      18505 | 2016-02-29 11:29:00 |
| ServiceNow events | closed_at               | datetime64[us] |           0   |       2707 | 2016-03-05 12:00:00 |

## bpi_prof
| dataset                    | variable                  | dtype          |   missing_pct |   distinct | example                  |
|:---------------------------|:--------------------------|:---------------|--------------:|-----------:|:-------------------------|
| Rabobank incident          | ci_name_aff               | str            |           0.4 |       3019 | SUB000508                |
| Rabobank incident          | ci_type_aff               | str            |           0.4 |         13 | subapplication           |
| Rabobank incident          | ci_subtype_aff            | str            |           0.4 |         65 | Web Based Application    |
| Rabobank incident          | service_component_wbs_aff | str            |           0.4 |        274 | WBS000162                |
| Rabobank incident          | incident_id               | str            |           0.4 |      46606 | IM0000004                |
| Rabobank incident          | status                    | str            |           0.4 |          2 | Closed                   |
| Rabobank incident          | impact                    | float64        |           0.4 |          5 | 4.0                      |
| Rabobank incident          | urgency                   | str            |           0.4 |          6 | 4                        |
| Rabobank incident          | priority                  | float64        |           0.4 |          5 | 4.0                      |
| Rabobank incident          | category                  | str            |           0.4 |          4 | incident                 |
| Rabobank incident          | km_number                 | str            |           0.4 |       1825 | KM0000553                |
| Rabobank incident          | alert_status              | str            |           0.4 |          1 | closed                   |
| Rabobank incident          | n_reassignments           | float64        |           0.4 |         41 | 26.0                     |
| Rabobank incident          | open_time                 | datetime64[us] |           0.4 |      46336 | 2012-02-05 13:32:57      |
| Rabobank incident          | reopen_time               | str            |          95.1 |       2282 | 02/12/2013 12:31:02      |
| Rabobank incident          | resolved_time             | datetime64[us] |           4.2 |      44603 | 2013-11-04 13:50:27      |
| Rabobank incident          | close_time                | datetime64[us] |           0.4 |      46376 | 2013-11-04 13:51:17      |
| Rabobank incident          | handle_time_hours         | float64        |           0.4 |      31376 | 3871.691111              |
| Rabobank incident          | closure_code              | str            |           1.4 |         14 | Other                    |
| Rabobank incident          | n_related_interactions    | float64        |           0.7 |         49 | 1.0                      |
| Rabobank incident          | related_interaction       | str            |           0.4 |      43060 | SD0000007                |
| Rabobank incident          | n_related_incidents       | float64        |          97.4 |         24 | 2.0                      |
| Rabobank incident          | n_related_changes         | float64        |          98.8 |          4 | 1.0                      |
| Rabobank incident          | related_change            | str            |          98.8 |        232 | C00000056                |
| Rabobank incident          | ci_name_cby               | str            |           0.4 |       3652 | SUB000508                |
| Rabobank incident          | ci_type_cby               | str            |           0.4 |         14 | subapplication           |
| Rabobank incident          | ci_subtype_cby            | str            |           0.4 |         63 | Web Based Application    |
| Rabobank incident          | servicecomp_wbs_cby       | str            |           0.4 |        275 | WBS000162                |
| Rabobank interaction       | ci_name_aff               | str            |           0   |       4153 | SBA000243                |
| Rabobank interaction       | ci_type_aff               | str            |           0   |         14 | application              |
| Rabobank interaction       | ci_subtype_aff            | str            |           0   |         67 | Server Based Application |
| Rabobank interaction       | service_comp_wbs_aff      | str            |           0   |        289 | WBS000125                |
| Rabobank interaction       | interaction_id            | str            |           0   |     147004 | SD0000001                |
| Rabobank interaction       | status                    | str            |           0   |          2 | Closed                   |
| Rabobank interaction       | impact                    | int64          |           0   |          5 | 5                        |
| Rabobank interaction       | urgency                   | str            |           0   |          6 | 4                        |
| Rabobank interaction       | priority                  | int64          |           0   |          5 | 4                        |
| Rabobank interaction       | category                  | str            |           0   |          6 | incident                 |
| Rabobank interaction       | km_number                 | str            |           0   |       2360 | KM0000987                |
| Rabobank interaction       | open_time_first_touch     | datetime64[us] |           0   |      65848 | 2011-09-09 09:23:00      |
| Rabobank interaction       | close_time                | datetime64[us] |           0   |      64727 | 2014-02-14 09:05:00      |
| Rabobank interaction       | closure_code              | str            |           0.3 |         24 | Other                    |
| Rabobank interaction       | first_call_resolution     | str            |           0   |          2 | N                        |
| Rabobank interaction       | handle_time_secs          | int64          |           0   |       3064 | 239                      |
| Rabobank interaction       | related_incident          | str            |          64.1 |      46088 | IM0000001                |
| Rabobank incident_activity | incident_id               | str            |           0   |      46616 | IM0000004                |
| Rabobank incident_activity | datestamp                 | str            |           0   |     273401 | 07-01-2013 08:17:17      |
| Rabobank incident_activity | incidentactivity_number   | str            |           0   |     466737 | 001A3689763              |
| Rabobank incident_activity | incidentactivity_type     | str            |           0   |         39 | Reassignment             |
| Rabobank incident_activity | assignment_group          | str            |           0   |        242 | TEAM0001                 |
| Rabobank incident_activity | km_number                 | str            |           0   |       1825 | KM0000553                |
| Rabobank incident_activity | interaction_id            | str            |           0   |      46444 | SD0000007                |
| Rabobank change            | ci_name_aff               | str            |           0   |      10193 | HMD000002                |
| Rabobank change            | ci_type_aff               | str            |           0   |         13 | hardware                 |
| Rabobank change            | ci_subtype_aff            | str            |           0   |         74 | MigratieDummy            |
| Rabobank change            | service_component_wbs_aff | str            |           0   |        286 | WBS000195                |
| Rabobank change            | change_id                 | str            |           0   |      18000 | C00000003                |
| Rabobank change            | change_type               | str            |           0   |        240 | Release Type 11          |
| Rabobank change            | risk_assessment           | str            |           0   |          3 | Minor Change             |
| Rabobank change            | emergency_change          | str            |           0   |          2 | N                        |
| Rabobank change            | cab_approval_needed       | str            |           0   |          2 | N                        |
| Rabobank change            | planned_start             | datetime64[us] |           0   |      11774 | 2012-08-30 07:00:00      |
| Rabobank change            | planned_end               | datetime64[us] |           0.1 |       8905 | 2013-12-26 00:00:00      |
| Rabobank change            | scheduled_downtime_start  | str            |          97.5 |        297 | 11-10-2013 9:00          |
| Rabobank change            | scheduled_downtime_end    | str            |          97.5 |        307 | 11-10-2013 15:00         |
| Rabobank change            | actual_start              | datetime64[us] |          10.8 |      13100 | 2013-12-18 14:00:00      |
| Rabobank change            | actual_end                | datetime64[us] |          10.8 |      13780 | 2013-12-18 16:15:00      |
| Rabobank change            | requested_end_date        | datetime64[us] |           0   |       6642 | 2012-06-01 00:00:00      |
| Rabobank change            | change_record_open_time   | datetime64[us] |           0   |      15066 | 2011-09-01 09:13:00      |
| Rabobank change            | change_record_close_time  | datetime64[us] |           0   |      15549 | 2013-12-18 16:16:00      |
| Rabobank change            | originated_from           | str            |           0   |          3 | Problem                  |
| Rabobank change            | n_related_interactions    | float64        |         100   |          2 | 5.0                      |
| Rabobank change            | n_related_incidents       | float64        |          93.6 |         57 | 48.0                     |

## Cleaning log
| Issue             | Dataset    | Variables Affected         | Detection Method                                                |   Count |   % of records | Treatment Applied                                                                                   | Rationale                                        |
|:------------------|:-----------|:---------------------------|:----------------------------------------------------------------|--------:|---------------:|:----------------------------------------------------------------------------------------------------|:-------------------------------------------------|
| Duplicates        | ServiceNow | all columns                | Exact duplicate event rows                                      |       0 |           0    | Dropped                                                                                             | Repeated audit rows add no information           |
| Missing values    | ServiceNow | all 36 columns ("?" codes) | Cells coded "?" (unknown) in the source                         |  894597 |          17.54 | Read as missing; per-variable rule in data dictionary; caused_by (100%) and cmdb_ci (99.7%) dropped | Follows dataset documentation; % is of all cells |
| Missing values    | ServiceNow | resolved_at                | Null after reduction                                            |    1556 |           6.24 | Resolution time left missing; incident kept                                                         | Incident still valid for D1/D5                   |
| Missing values    | ServiceNow | assignment_group           | Null after reduction                                            |    2157 |           8.66 | Excluded from D5 only                                                                               | No ground truth for assignment                   |
| Impossible values | ServiceNow | resolved_at < opened_at    | Negative duration                                               |       0 |           0    | Resolution time set to missing                                                                      | Timestamp error                                  |
| Outliers          | ServiceNow | resolution_hours           | IQR rule (> Q3 + 3·IQR = 593 h)                                 |    1449 |           5.82 | Kept; flagged; medians reported                                                                     | Long-running incidents are real, not errors      |
| Duplicates        | Rabobank   | incident_id                | Duplicate keys                                                  |     202 |           0.43 | Kept first record                                                                                   | One row per incident                             |
| Format errors     | Rabobank   | Detail_Incident.csv        | Mixed date formats and comma separator after re-saving in Excel |   46809 |         100    | File re-downloaded from source; never opened in Excel                                               | Excel swapped day/month and dropped fields       |
| Format errors     | Rabobank   | handle_time_hours          | Decimal comma (European format)                                 |   46605 |          99.56 | Parsed with decimal=","                                                                             | Correct numeric values                           |
| Missing values    | Rabobank   | open_time / resolved_time  | Null or unparseable                                             |    1983 |           4.24 | Resolution time not computed                                                                        | Incident still valid for D1/D5                   |
| Missing values    | Rabobank   | closure_code               | Null                                                            |     663 |           1.42 | Set to "unknown"; excluded from D4                                                                  | No ground truth                                  |
| Impossible values | Rabobank   | resolved < opened          | Negative duration                                               |       0 |           0    | Resolution time set to missing                                                                      | Timestamp error                                  |
| Outliers          | Rabobank   | resolution_hours           | IQR rule (> Q3 + 3·IQR = 379 h)                                 |    2884 |           6.16 | Kept; flagged; medians reported                                                                     | Long-running incidents are real                  |

## EDA insights
| Figure/Table Reference     | What it Shows                                        | Key Insight                                                                                  | Why it Matters (Link to RQ/objective)                                                                                                     | Decision/Next Step                                                    |
|:---------------------------|:-----------------------------------------------------|:---------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| eda_monthly_volume         | Incidents opened per month                           | ServiceNow has 4 months with >100 incidents; Rabobank has 7                                  | RQ4 needs 25 monthly windows; neither log alone gives 25 dense months                                                                     | Use Jira for the 25-month replay; logs for workload profile           |
| eda_class_imbalance        | Category and priority distribution                   | 52 categories; top 5 = 54% of incidents; one priority level = 94%                            | Strong class imbalance: accuracy alone would flatter a model that predicts the majority class (RQ1)                                       | Report macro-F1; stratified test sample                               |
| eda_sla_by_friction        | SLA and resolution vs teams involved                 | SLA met 78% with one team vs 28% with 3+ teams; median resolution 1 h vs 103 h               | Each misrouting hand-off costs time and SLA: an accurate first assignment (D5) has direct business value (RQ1–RQ2)                        | Weight D5 errors by hand-off cost in the cost model                   |
| eda_resolution_by_priority | Resolution time by priority                          | 1 - Critical: 80 h; 2 - High: 38 h; 3 - Moderate: 22 h; 4 - Low: 5 h                         | Priority is a risk feature for the allocation tree (error cost differs by priority)                                                       | Include priority as a decision-risk feature                           |
| eda_knowledge              | Resolution time with and without a knowledge article | Knowledge used in 14% of incidents; median 78 h with vs 12 h without                         | Knowledge articles are used mostly on harder, longer incidents (selection effect, not a causal slowdown); RQ3 must compare like with like | RQ3 compares instruments on the same tickets with and without context |
| workload_profile           | Workload profile (Table)                             | Rabobank: 64% of service-desk contacts resolved at first call; 41% of incidents need >1 team | Shows decision volumes the instruments would serve                                                                                        | Weight costs by real volumes                                          |

## Python / package versions
- pandas 3.0.2, numpy 2.4.4