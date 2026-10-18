# Step 03 summary - 2026-10-18 04:46

## Human-correction signals (RQ4)
{"category_changed_%": 4.62, "group_changed_%": 38.68, "group_missing_at_creation_%": 3.64, "rabobank_team_changed_%": 78.56}

## RQ1 preliminary: I1 baselines on the held-out test sets
| Dataset    | Decision                            | Model            |   Train rows |   Test rows |   Classes |   Accuracy % | 95% CI (Wilson)   |   Macro-F1 |   Train+predict s |   Unseen test classes % |
|:-----------|:------------------------------------|:-----------------|-------------:|------------:|----------:|-------------:|:------------------|-----------:|------------------:|------------------------:|
| ServiceNow | D1 classify (category)              | Majority class   |        17437 |         385 |        52 |         11.9 | 9.1–15.6          |      0.007 |               0   |                     1.6 |
| ServiceNow | D1 classify (category)              | I1 Random Forest |        17437 |         385 |        52 |         27.8 | 23.6–32.5         |      0.136 |               3   |                     1.6 |
| ServiceNow | D1 classify (category)              | I1 XGBoost       |        17437 |         385 |        52 |         39.2 | 34.5–44.2         |      0.228 |               8.4 |                     1.6 |
| ServiceNow | D5 assign team                      | Majority class   |        15932 |         385 |        70 |         50.9 | 45.9–55.9         |      0.016 |               0   |                     0.3 |
| ServiceNow | D5 assign team                      | I1 Random Forest |        15932 |         385 |        70 |         47.5 | 42.6–52.5         |      0.334 |               3.8 |                     0.3 |
| ServiceNow | D5 assign team                      | I1 XGBoost       |        15932 |         385 |        70 |         61   | 56.1–65.8         |      0.361 |              15.4 |                     0.3 |
| Rabobank   | D5 assign team                      | Majority class   |        32624 |         385 |       196 |          9.9 | 7.3–13.3          |      0.003 |               0   |                     0.3 |
| Rabobank   | D5 assign team                      | I1 Random Forest |        32624 |         385 |       196 |         22.6 | 18.7–27.0         |      0.16  |               3.4 |                     0.3 |
| Rabobank   | D5 assign team                      | I1 XGBoost       |        32624 |         385 |       196 |         29.4 | 25.0–34.1         |      0.197 |              63   |                     0.3 |
| Rabobank   | D4 next action (closure code proxy) | Majority class   |        32302 |         385 |        14 |         33   | 28.5–37.8         |      0.05  |               0   |                     0   |
| Rabobank   | D4 next action (closure code proxy) | I1 Random Forest |        32302 |         385 |        14 |         41.8 | 37.0–46.8         |      0.27  |               2.4 |                     0   |
| Rabobank   | D4 next action (closure code proxy) | I1 XGBoost       |        32302 |         385 |        14 |         57.4 | 52.4–62.2         |      0.304 |               5   |                     0   |

## Test sets
{"sn_D1": 385, "sn_D5": 385, "rb_D5": 385, "rb_D4": 385}

## Cost
| Dataset    | Decision                            | Model            |   Train+predict s |   USD per 1,000 tickets (train+predict, upper bound) |
|:-----------|:------------------------------------|:-----------------|------------------:|-----------------------------------------------------:|
| ServiceNow | D1 classify (category)              | I1 Random Forest |               3   |                                              0.00042 |
| ServiceNow | D1 classify (category)              | I1 XGBoost       |               8.4 |                                              0.00116 |
| ServiceNow | D5 assign team                      | I1 Random Forest |               3.8 |                                              0.00053 |
| ServiceNow | D5 assign team                      | I1 XGBoost       |              15.4 |                                              0.00213 |
| Rabobank   | D5 assign team                      | I1 Random Forest |               3.4 |                                              0.00047 |
| Rabobank   | D5 assign team                      | I1 XGBoost       |              63   |                                              0.00873 |
| Rabobank   | D4 next action (closure code proxy) | I1 Random Forest |               2.4 |                                              0.00033 |
| Rabobank   | D4 next action (closure code proxy) | I1 XGBoost       |               5   |                                              0.00069 |

## RQ2 preliminary: risk-coverage (XGBoost)
| Dataset/decision   |   Accuracy % (all) |   Coverage % at 98% precision (automate) |   Coverage % at 90% precision (recommend) |   ECE |
|:-------------------|-------------------:|-----------------------------------------:|------------------------------------------:|------:|
| ServiceNow D5      |               61   |                                      2.3 |                                      27.3 | 0.103 |
| ServiceNow D1      |               39.2 |                                     18.7 |                                      22.6 | 0.109 |
| Rabobank D5        |               29.4 |                                      6.8 |                                      10.6 | 0.231 |
| Rabobank D4        |               57.4 |                                     13   |                                      20.8 | 0.046 |

## RQ4 preview: compiled rules from history
| Dataset/decision   | Rule key                                       |   Rules (automate) |   Test coverage % (automate) |   Test precision % (automate) |   Rules (recommend) |   Test coverage % (recommend) |   Test precision % (recommend) |
|:-------------------|:-----------------------------------------------|-------------------:|-----------------------------:|------------------------------:|--------------------:|------------------------------:|-------------------------------:|
| ServiceNow D5      | first_category + subcategory_first + u_symptom |                  2 |                          0   |                           nan |                  11 |                          15.3 |                           94.9 |
| Rabobank D5        | ci_name_aff + service_component_wbs_aff        |                  0 |                          0   |                           nan |                  11 |                           2.9 |                          100   |
| Rabobank D4        | ci_name_aff + service_component_wbs_aff        |                  3 |                          4.2 |                           100 |                  13 |                           9.4 |                           94.4 |