# %%
import pandas as pd
import plotly.express as px
import streamlit as st
# %%
path = "data/olist/"  # caminho raiz até os arquivos *.csv
customers = pd.read_csv(path + "olist_customers_dataset.csv")
# %%
st.write(f"""
    # Número de clientes por estado
    
    ### Total de clientes: {len(customers)}
""")


# %%
agrupado = (customers.groupby('customer_state').size().reset_index(name="quantidade"))
agrupado._to_dict_of_blocks()
# %%
from pathlib import Path
import json

arquivo = Path("data/br_states.json")

with arquivo.open("r", encoding="utf-8") as resp:
    br_states = json.load(resp)

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