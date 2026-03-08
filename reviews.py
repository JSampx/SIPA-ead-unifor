# %%
import pandas as pd
path = "data/olist/" # caminho raiz até os arquivos *.csv
reviews = pd.read_csv(path + "olist_order_reviews_dataset.csv")
# %%
reviews
# %%
reviews['review_score'].describe()