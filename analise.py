from pathlib import Path

import pandas as pd
import streamlit as st
# import plotly.express as px
#
# import json

path = "data/olist/"
dataset = pd.read_csv(path + "merged/olist_merged_dataset.csv")
customers = pd.read_csv(path + "olist_customers_dataset.csv")

colunas = ['order_purchase_timestamp',
           'order_approved_at', 'order_delivered_carrier_date',
           'order_delivered_customer_date', 'order_estimated_delivery_date',
           'shipping_limit_date', 'review_creation_date', 'review_answer_timestamp']
dataset[colunas] = dataset[colunas].apply(pd.to_datetime)

anos_list = sorted(dataset["order_purchase_timestamp"].dt.year.unique())
anos = st.sidebar.multiselect("Ano", anos_list,
                             placeholder="Selecione o(s) ano(s)",
                             default=anos_list)

categorias_list = dataset['product_category_name'].unique().tolist()
categorias = st.sidebar.selectbox("Categoria", ['Todas as categorias'] + categorias_list)
lista_categorias = []
if categorias == 'Todas as categorias':
    lista_categorias = categorias_list
else:
    lista_categorias.append(categorias)

from customers import customers
estados_list = sorted(customers['customer_state'].unique().tolist())
estados = st.sidebar.selectbox("Estado", ['Todos os estados'] + estados_list)
lista_estados = list()
if estados == 'Todos os estados':
    lista_estados = estados_list
else:
    lista_estados.append(estados)


st.set_page_config(layout="wide")
st.write("""
# SIPA - Sistema de """)
st.sidebar.header("ADS Unifor")

st.title("Dataset do e-commerce Olist 2016/2017/2018")

dataset_com_filtros=dataset[(dataset['order_purchase_timestamp'].dt.year.isin(anos)) &
                            (dataset['customer_state'].isin(lista_estados)) &
                            (dataset['product_category_name'].isin(lista_categorias))]

st.dataframe(dataset_com_filtros)
dataset_com_filtros.head()

col1, col2, col3 = st.columns(3)
pedidos_total = dataset_com_filtros['price'].sum()
fretes_total = dataset_com_filtros['freight_value'].sum()
with col1:
    st.write(f"""
                * R$ {pedidos_total:,.2f} foi o total de pedidos no período para {estados}
                * R$ {fretes_total:,.2f} foi o valor de frete dos pedidos
                * R$ {pedidos_total+fretes_total:,.2f} foi o total de pedidos


""")

# sem_categoria = dataset[dataset['product_category_name'].isna()]
# sem_categoria
