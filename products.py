# %%
import pandas as pd
import streamlit as st

path = "data/olist/" # caminho raiz até os arquivos *.csv
products = pd.read_csv(path + "olist_products_dataset.csv")
categorias = products.groupby("product_category_name").size()
st.write(
         f"""
         # Produtos
         
         ### {len(products)} produtos em {len(categorias)} categorias
         
         """)
products.shape
# %%
