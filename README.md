# Create environment
pyenv install 3.11.6  # (Se ainda não tiver essa versão)
pyenv virtualenv 3.11.6 streamlit
pyenv activate streamlit

# outra opção: # pyenv virtualenv streamlit

# Install Dependencies
pip install -r requirements.txt

# Executar streamlit:
streamlit run main.py

