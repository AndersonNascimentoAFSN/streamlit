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

@st.cache_data
def load_tickers_quotes():
    base_tickers = pd.read_csv(
      "data/IBOV.csv",
      sep=";",
      encoding='latin1',
      engine='python',
      skipinitialspace=True,  # Remove espaços extras
      on_bad_lines='skip'  # Ignora linhas mal formatadas
    )
    base_tickers.columns = base_tickers.columns.str.strip()
    first_column = base_tickers.iloc[:, 0].map(lambda x: x.strip() if isinstance(x, str) else x)
    tickers = list(first_column)
    tickers = [str(item) + ".SA" for item in tickers]
    return tickers

# "ITUB4.SA" SA = São Paulo
quotes = load_tickers_quotes()
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


# Cálculo de performance
text_performance_quotes = ""

if len(list_quotes_selected) == 0:
    list_quotes_selected = list(data.columns)
elif len(list_quotes_selected) == 1:
    data = data.rename(columns={"Close": unique_data})

wallet = [1000 for quotes in list_quotes_selected]
total_start_wallet = sum([item for item in wallet if pd.notna(item)])

for index, quotes in enumerate(list_quotes_selected):
    # Formatação de cor em markdown :color[text]
    performance_quotes = data[quotes].iloc[-1] / data[quotes].iloc[0] - 1
    performance_quotes = float(performance_quotes)

    wallet[index] = wallet[index] * (1 + performance_quotes)

    if performance_quotes > 0:
        text_performance_quotes = text_performance_quotes + f"{quotes}: :green[{performance_quotes:.1%}]  \n"
    elif performance_quotes < 0:
        text_performance_quotes = text_performance_quotes + f"{quotes}: :red[{performance_quotes:.1%}]  \n"
    else:
      text_performance_quotes = text_performance_quotes + f"{quotes}: {performance_quotes:.1%}  \n"

total_end_wallet = sum([item for item in wallet if pd.notna(item)])

wallet_performance = total_end_wallet / total_start_wallet  - 1

if wallet_performance > 0:
  text_performance_wallet = f"Performance da carteira com todos os ativos: :green[{wallet_performance:.1%}]  \n"
elif performance_quotes < 0:
  text_performance_wallet = f"Performance da carteira com todos os ativos: :red[{wallet_performance:.1%}]  \n"
else:
  text_performance_wallet = f"Performance da carteira com todos os ativos: {wallet_performance:.1%}  \n"

st.write(f"""
### Perfomance dos ativos
Essa foi a performance de cada ativo no período selecionado:  

{text_performance_quotes}

{text_performance_wallet}
""") # markdown
