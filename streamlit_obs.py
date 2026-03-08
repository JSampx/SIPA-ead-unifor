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
st.sidebar.subheader("ADS Unifor")

st.title("Dataset do e-commerce Olist 2016/2017/2018")

# st.dataframe(dataset)

agrupado = (customers.groupby('customer_state').size().reset_index(name="quantidade"))
agrupado._to_dict_of_blocks()
geojson = Path("data/br_states.json")

with geojson.open("r", encoding="utf-8") as resp:
    br_states = json.load(resp)

st.title("Distribuição clientes por estado")

fig = px.choropleth_map(agrupado,
                        geojson=br_states,
                        locations='customer_state',
                        featureidkey="id",
                        color="quantidade",
                        color_continuous_scale="blues",
                        map_style="carto-positron",
                        zoom=3,
                        center={"lat": -14.235, "lon": -51.925},
                        opacity=0.7
                        )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Quantidade (escala log)"
    )
)

st.plotly_chart(fig, width="stretch")

st.write("""
       # Total de pedidos por ano
       """)
ano = st.sidebar.selectbox("Ano", sorted(dataset["order_purchase_timestamp"].dt.year.unique()))

st.write("""
       # Status dos pedidos por ano
       """)

# tabela = (
#     df_filtrado["categoria"]
#     .value_counts()
#     .reset_index()
# )
status = st.multiselect(
    "Status do pedido",
    options=sorted(dataset["order_status"].unique()),
    default=dataset["order_status"].unique()
)

df_filtrado = dataset[
    (dataset["order_purchase_timestamp"].dt.year == ano) &
    (dataset["order_status"].isin(status))
    ]
tabela_status = (
    df_filtrado["order_status"]
    .value_counts()
    .reset_index(name="quantidade")
)

tabela_status.columns = ["order_status", "quantidade"]

# gráfico
fig = px.bar(
    tabela_status,
    x="order_status",
    y="quantidade",
    text="quantidade",
    title=f"Status dos pedidos em {ano}"
)

st.plotly_chart(fig, width='stretch')
st.dataframe(tabela_status)
