# %%
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")
st.title("Pedidos")
st.subheader("Base de dados do e-commerce do Olist entre os anos 2016 a 2018")

path = "data/olist/" # caminho raiz até os arquivos *.csv
orders = pd.read_csv(path + "olist_orders_dataset.csv")

# %%
colunas = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
orders[colunas] = orders[colunas].apply(pd.to_datetime)

anos_list = sorted(orders["order_purchase_timestamp"].dt.year.unique())
ano = st.sidebar.multiselect("Ano", anos_list,
                             placeholder="Selecione o(s) ano(s)",
                             default=anos_list)

from products import products
from items import items
df_mesclado1  = orders.merge(items, on="order_id")
df_mesclado2 = products.merge(df_mesclado1, on="product_id")
# df_mesclado2.columns

df_com_filtros = df_mesclado2[(df_mesclado2['order_purchase_timestamp'].dt.year.isin(ano))]
# df_mesclado2
st.dataframe(df_com_filtros)

# %%
# orders['order_status'].describe()
# %%
agrupado = orders.groupby('order_status').size()
col1, col2, col3 = st.columns(3)
# %%
### TEMPO DE ENTREGA REALIZADO - ESTIMADO ###
entregues = orders.loc[orders["order_status"] == "delivered"].copy()

entregues["delivered_in_days"] = (
    entregues["order_estimated_delivery_date"]
    - entregues["order_delivered_customer_date"]
).dt.days

entregues['delivered_in_days'].describe()
# %%
mins = entregues.loc[entregues['delivered_in_days'] < 0]
med = entregues[(entregues['delivered_in_days'] > 0) & (entregues['delivered_in_days'] < 12)]
a=(entregues["delivered_in_days"] < 0).mean() * 100
num_pedidos = len(entregues)
num_pedidos_antes = len(mins)
num_pedidos_prazo = len(med)
with col1:
    st.write(f""" 
    * Foram realizados {len(orders)} pedidos entre {anos_list[0]} e {anos_list[-1]}
    * O tempo médio de entregas é de {entregues["delivered_in_days"].mean():.1f} dias
    * A entrega com menor tempo foi de {mins["delivered_in_days"].max()} dias

""")


with col2:
    st.write (f"""
    #### {num_pedidos_antes/num_pedidos:.2%} de pedidos entregues antes do prazo  \n
    #### {num_pedidos_prazo/num_pedidos:.2%} de pedidos entregues no prazo  \n
    #### {(num_pedidos - (num_pedidos_antes + num_pedidos_prazo))/num_pedidos * 100:.2f} % de pedidos atrasados""")
# %%


fig = px.histogram(
    entregues,
    x="delivered_in_days",  # atraso em dias
    nbins=100,
    title="Tempo de entrega dos pedidos em dias (Estimado - Realizado)"
)
with col2:
    st.plotly_chart(fig)

# %%
top_10_atrasos = entregues['delivered_in_days'].to_frame()
top_10_atrasos.describe()
# %%
### PEDIDOS NÃO ENTREGUES ###
nao_entregues = orders[orders['order_status'] != "delivered"]
with col3:
    st.write(f"""### {len(nao_entregues)} pedidos não foram entregues""")
# %%
# ### MAIORES 20 CLIENTES  ###
# top_10_custormers = orders['customer_id'].value_counts()[:20]
# top_10_custormers
# %%
agrupado = orders['customer_id'].describe()
agrupado

# %%
orders_per_month_year = (
    orders
    .assign(
        ano=orders["order_purchase_timestamp"].dt.year,
        mes=orders["order_purchase_timestamp"].dt.month
    )
    .groupby(["ano", "mes"], as_index=False)
    .size()
    .rename(columns={"size": "quantidade"})
)

orders_per_month_year
# %%
# datetime mensal
orders_per_month_year["data"] = pd.to_datetime(
    orders_per_month_year["ano"].astype(str) + "-" +
    orders_per_month_year["mes"].astype(str) + "-01"
)

# agregado por ano
por_ano = (
    orders_per_month_year
    .groupby("ano", as_index=False)["quantidade"]
    .sum()
)

# agregado por mês (todos os anos juntos)
por_mes = (
    orders_per_month_year
    .groupby("mes", as_index=False)["quantidade"]
    .sum()
)

from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=1,
    cols=3,
    subplot_titles=[
        "Evolução Mensal",
        "Total por Ano",
        "Distribuição por Mês"
    ]
)

# 1️⃣ Evolução mensal
fig.add_trace(
    go.Scatter(
        x=orders_per_month_year["data"],
        y=orders_per_month_year["quantidade"],
        mode="lines+markers",
        name="Mensal"
    ),
    row=1, col=1
)

# 2️⃣ Total por ano
fig.add_trace(
    go.Bar(
        x=por_ano["ano"],
        y=por_ano["quantidade"],
        name="Ano"
    ),
    row=1, col=2
)

# 3️⃣ Distribuição por mês
fig.add_trace(
    go.Bar(
        x=por_mes["mes"],
        y=por_mes["quantidade"],
        name="Mês"
    ),
    row=1, col=3
)

fig.update_layout(
    height=450,
    showlegend=False,
    title_text="Análise Temporal de Pedidos",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig)