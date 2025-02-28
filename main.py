# importar libs:
# import numpy as np
# import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import yfinance as yf

# Criar funções de carregamento de dados:
  # Cotações do Itau - ITUB4 - 2010 a 2024
@st.cache_data
def load_data(business):
    data_action = yf.Ticker(business) # "ITUB4.SA" SA = São Paulo
    quotes_action = data_action.history(period="1d", start="2010-01-01", end="2024-07-01")
    quotes_action = quotes_action[["Close"]]
    return quotes_action
    # data = yf.download('ITUB4.SA', start='2010-01-01', end='2024-01-01')

# Preparar as visualizações (operações)
data = load_data('ITUB4.SA')
print(data)


# Criar a interface do streamlit:
st.write("""
# App preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos (2010 a 2024).  
""") # markdown

# Criar gráfico
st.line_chart(data)

