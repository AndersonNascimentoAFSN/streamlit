# importar libs:
# import numpy as np
# import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

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
st.sidebar.header("Filtros")
st.sidebar.write("Selecione as ações e o período desejado")

# Filtros de ações:
list_quotes_selected = st.sidebar.multiselect("Selecione as ações que deseja visualizar", data.columns)

if list_quotes_selected:
    # data = data.filter(list_quotes_selected)
    data = data[list_quotes_selected]
    if len(list_quotes_selected) == 1:
      unique_data = list_quotes_selected[0]
      data = data.rename(columns={unique_data: "Close"})

# Filtros de datas:
start_date = data.index.min().to_pydatetime()
end_date = data.index.max().to_pydatetime()
date_interval = st.sidebar.slider(
  "Selecione o período", 
  min_value=start_date,
  max_value=end_date,
  value=(start_date, end_date),
  step=timedelta(days=1)
  # step=pd.DateOffset(years=1)
)

data = data.loc[date_interval[0]:date_interval[1]]

# Criar gráfico
st.line_chart(data)

