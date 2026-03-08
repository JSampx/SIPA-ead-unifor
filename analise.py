from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

import json

path = "data/olist/"
dataset = pd.read_csv(path + "merged/olist_merged_dataset.csv")
customers = pd.read_csv(path + "olist_customers_dataset.csv")

colunas = ['order_purchase_timestamp',
           'order_approved_at', 'order_delivered_carrier_date',
           'order_delivered_customer_date', 'order_estimated_delivery_date',
           'shipping_limit_date', 'review_creation_date', 'review_answer_timestamp']
dataset[colunas] = dataset[colunas].apply(pd.to_datetime)

st.set_page_config(layout="wide")
st.write("""
# SIPA - Sistema de """)
st.sidebar.header("ADS Unifor")

st.title("Dataset do e-commerce Olist 2016/2017/2018")

st.dataframe(dataset)

col1, col2, col3 = st.columns(3)
pedidos_total = dataset['price'].sum()
fretes_total = dataset['freight_value'].sum()
with col1:
    st.write(f"""
                * R$ {pedidos_total:,.2f} foi o total de pedidos no período
                * R$ {fretes_total:,.2f} foi o valor de frete dos pedidos
                * R$ {pedidos_total+fretes_total:,.2f} foi o total de pedidos


""")

