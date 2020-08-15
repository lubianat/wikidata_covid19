# %%
from wikidata2df import wikidata2df
import pandas as pd

# %%
with open("query_template.rq", "r") as q:
    query_template = q.read()

with_dash_query = query_template.replace("TITLE_FILTER", "sars-cov-2")
no_dash_query = query_template.replace("TITLE_FILTER", "sars-cov2")

# %%
no_subj_papers = pd.concat([wikidata2df(with_dash_query), wikidata2df(no_dash_query)])

# %%
with open("update_cov2_papers.rq", "w") as qs:
    for _, row in no_subj_papers.iterrows():
        row_qs = f"{row['item']}|P921|Q82069695\n"
        qs.write(row_qs)
