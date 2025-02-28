# Create environment
pyenv install 3.11.6  # (Se ainda não tiver essa versão)
pyenv virtualenv 3.11.6 streamlit
pyenv activate streamlit

# outra opção: # pyenv virtualenv streamlit

# Install Dependencies
pip install -r requirements.txt

# Executar streamlit:
streamlit run main.py

# Classes:
## https://www.youtube.com/watch?v=NsjA-c8596k&t=515s
## https://www.youtube.com/watch?v=fUuBo759oqg
## https://www.youtube.com/watch?v=AbQxNUvjwv8
## https://www.youtube.com/watch?v=KPiYg4-kFzE