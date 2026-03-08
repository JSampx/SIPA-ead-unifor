import streamlit as st

# Paginação da visualização
main_page = st.Page("orders.py", title="Pedidos", )
page_2 = st.Page("reviews.py", title="Reviews", )
page_3 = st.Page("products.py", title="Produtos", )
page_4 = st.Page("customers.py", title="Clientes", )

# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4])

# Run the selected page
pg.run()