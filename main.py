# importar libs:
# import numpy as np
# import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import yfinance as yf

# Criar funções de carregamento de dados:
  # Cotações do Itau - ITUB4 - 2010 a 2024
@st.cache_data
def load_data(businesses):
    businesses_formatted = " ".join(businesses)
    data_action = yf.Tickers(businesses_formatted) 
    quotes_action = data_action.history(period="1d", start="2010-01-01", end="2024-07-01")
    quotes_action = quotes_action["Close"]
    return quotes_action

# "ITUB4.SA" SA = São Paulo
quotes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABV3.SA", "GGBR4.SA"]
data = load_data(quotes)

# Criar a interface do streamlit:
st.write("""
# App preço de Ações
O gráfico abaixo representa a evolução do preço das ações de várias empresas ao longo dos anos (2010 a 2024).  
""") # markdown

# Preparar as visualizações (filtros)
list_quotes_selected = st.multiselect("Selecione as ações que deseja visualizar", data.columns)

if list_quotes_selected:
    # data = data.filter(list_quotes_selected)
    data = data[list_quotes_selected]
    if len(list_quotes_selected) == 1:
      unique_data = list_quotes_selected[0]
      data = data.rename(columns={unique_data: "Close"})

# Criar gráfico
st.line_chart(data)

