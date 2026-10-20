import sys, json, time, numpy as np, pandas as pd, pyarrow.parquet as pq, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from statsmodels.stats.proportion import proportion_confint
import xgboost as xgb
IN, OUT = Path(sys.argv[1]), Path(sys.argv[2]); (OUT/'figures').mkdir(parents=True, exist_ok=True)
SEED, N = 640, 385; rng = np.random.default_rng(SEED)
files = sorted(IN.glob('*.parquet'))
LIGHT = ['repository','key','project','issuetype','priority','resolution','created','resolutiondate','components','assignee','n_comments','n_links','has_duplicate_link','n_assignee_changes','n_component_changes','n_priority_changes','n_type_changes']
df = pd.concat([pd.read_parquet(f, columns=LIGHT) for f in files], ignore_index=True)
for c in ('created','resolutiondate'): df[c] = pd.to_datetime(df[c], errors='coerce', utc=True)
df['resolution_hours'] = (df['resolutiondate']-df['created']).dt.total_seconds()/3600
df['month'] = df['created'].dt.tz_localize(None).dt.to_period('M')
nr = lambda s: round(100*s.mean(), 1)
ov = {'rows': len(df), 'columns': 24, 'repositories': df['repository'].value_counts().to_dict(), 'projects': int(df.groupby('repository')['project'].nunique().sum()),
      'first': str(df['created'].min())[:10], 'last': str(df['created'].max())[:10],
      'duplicate_link_pct': nr(df['has_duplicate_link']), 'resolution_duplicate_pct': nr(df['resolution'].isin(['Duplicate','Duplicate Issue'])),
      'with_components_pct': nr(df['components'] != '[]'), 'with_assignee_pct': nr(df['assignee'].notna()),
      'median_resolution_h': round(float(df['resolution_hours'].median()), 1),
      'assignee_changed_pct': nr(df['n_assignee_changes'] > 0), 'priority_changed_pct': nr(df['n_priority_changes'] > 0),
      'type_changed_pct': nr(df['n_type_changes'] > 0), 'component_changed_pct': nr(df['n_component_changes'] > 0),
      'issuetype_classes': int(df['issuetype'].nunique()), 'priority_classes': int(df['priority'].nunique()),
      'top_issuetypes_pct': (100*df['issuetype'].value_counts(normalize=True).head(5)).round(1).to_dict(),
      'missing_pct': {c: round(100*df[c].isna().mean(), 1) for c in ['issuetype','priority','created','resolutiondate','assignee']}}
monthly = df.groupby(['repository','month']).size().unstack(0).fillna(0).sort_index()
def longest(s):
    best = cur = 0
    for v in (s >= 200): cur = cur + 1 if v else 0; best = max(best, cur)
    return best
ov['longest_dense_run_months'] = {r: longest(monthly[r]) for r in monthly}
fig, ax = plt.subplots(figsize=(8, 3.2)); m = monthly[monthly.index >= pd.Period('2008-01', 'M')]
for r, col in zip(m, ['#2b6cb0', '#38a169', '#c05621']): ax.plot(m.index.to_timestamp(), m[r], label=r, lw=1.2, color=col)
ax.axhline(200, ls='--', c='grey', lw=.8); ax.text(m.index.to_timestamp()[2], 230, '200 per month', fontsize=8, color='grey')
ax.set_title('Jira: resolved issues created per month, by repository'); ax.legend(fontsize=8); ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig(OUT/'figures/jira_monthly.png', dpi=200); plt.close()
# correction signals by repo
corr = df.groupby('repository')[['n_assignee_changes','n_priority_changes','n_type_changes','n_component_changes']].apply(lambda x: (x > 0).mean()*100).round(1)
corr.to_csv(OUT/'jira_correction_signals.csv')
# --- time split thresholds on the whole set ---
ct = df['created'].dropna().sort_values().reset_index(drop=True)
q70, q80 = ct.iloc[int(.7*len(ct))], ct.iloc[int(.8*len(ct))]
ov['split'] = {'train_until': str(q70)[:10], 'test_from': str(q80)[:10]}
del df
# --- sample text rows: ~70k training rows from <q70, ~6k test pool from >=q80 ---
cols = ['repository','created','issuetype','priority','summary','description']
tr_parts, te_parts = [], []
for f in files:
    pf = pq.ParquetFile(f)
    for b in pf.iter_batches(batch_size=50000, columns=cols):
        x = b.to_pandas(); x['created'] = pd.to_datetime(x['created'], errors='coerce', utc=True)
        a = x[x['created'] < q70]; t = x[x['created'] >= q80]
        tr_parts.append(a[rng.random(len(a)) < 0.035]); te_parts.append(t[rng.random(len(t)) < 0.03])
tr_all, te_pool = pd.concat(tr_parts, ignore_index=True), pd.concat(te_parts, ignore_index=True)
for z in (tr_all, te_pool): z['text'] = (z['summary'].fillna('') + ' ' + z['description'].fillna('')).str.slice(0, 2000)
print('train sample', len(tr_all), 'test pool', len(te_pool))
rows = []
for label, task in [('issuetype', 'D1 classify (issue type)'), ('priority', 'D1 classify (priority)')]:
    tr = tr_all.dropna(subset=[label]); te = te_pool.dropna(subset=[label]).sample(n=N, random_state=SEED)
    top = tr[label].value_counts().index[:10].tolist()
    mapc = lambda s: s.where(s.isin(top), 'Other')
    ytr_l, y = mapc(tr[label]), mapc(te[label]).values
    vec = TfidfVectorizer(max_features=15000, ngram_range=(1, 2), min_df=3, sublinear_tf=True)
    Xtr = vec.fit_transform(tr['text']); Xte = vec.transform(te['text'])
    classes = ytr_l.value_counts().index.tolist(); cmap = {c: i for i, c in enumerate(classes)}; ytr = ytr_l.map(cmap).values
    preds, secs = {'Majority class': np.array([classes[0]]*N)}, {'Majority class': 0}
    t0 = time.time(); lr = LogisticRegression(max_iter=400, C=4).fit(Xtr, ytr); preds['I1 TF-IDF + logistic regression'] = np.array(classes)[lr.predict(Xte)]; secs['I1 TF-IDF + logistic regression'] = time.time()-t0
    t0 = time.time(); xg = xgb.XGBClassifier(n_estimators=60, max_depth=6, learning_rate=.3, tree_method='hist', n_jobs=2, random_state=SEED).fit(Xtr, ytr)
    preds['I1 TF-IDF + XGBoost'] = np.array(classes)[xg.predict(Xte)]; secs['I1 TF-IDF + XGBoost'] = time.time()-t0
    for mname, p in preds.items():
        k = int((p == y).sum()); lo, hi = proportion_confint(k, N, method='wilson')
        rows.append({'Dataset': 'Jira', 'Decision': task, 'Model': mname, 'Train rows': len(tr), 'Test rows': N, 'Classes': f'{len(classes)} (top 10 + other)',
                     'Accuracy %': round(100*k/N, 1), '95% CI (Wilson)': f'{100*lo:.1f}–{100*hi:.1f}', 'Macro-F1': round(f1_score(y, p, average='macro', zero_division=0), 3), 'Train+predict s': round(secs[mname], 1)})
    print(task, 'done')
perf = pd.DataFrame(rows); perf.to_csv(OUT/'rq1_jira_baseline_metrics.csv', index=False)
json.dump(ov, open(OUT/'jira_overview.json', 'w'), indent=1, default=str)
print(json.dumps(ov, indent=1, default=str)); print(corr.to_string()); print(perf.to_string())
