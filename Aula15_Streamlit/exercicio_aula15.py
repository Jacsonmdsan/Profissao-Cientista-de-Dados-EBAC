import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime # Importar para usar st.date_input e st.time_input

# --- Configuração e Carregamento de Dados ---
st.title('Exemplos Diversos de Utilização do Streamlit')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data # 1. Uso de st.cache_data para otimização de carregamento de dados
def load_data(nrows):
    data_load_state = st.text('Loading data...')
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data_load_state.text('Loading data...done!')
    return data

# 2. Exibindo um spinner enquanto os dados são carregados
data = load_data(10000)

# --- Exibição de Dados e Elementos Básicos ---
st.header('Exibição de Dados Brutos e Interativos')

# 3. Exibindo dados brutos com st.write
st.subheader('Dados Brutos da Uber (primeiras 10.000 linhas)')
st.write(data.head()) # Mostra apenas as primeiras linhas para melhor visualização

# 4. Usando st.checkbox para exibir/ocultar dados
if st.checkbox('Mostrar todos os dados brutos'):
    st.subheader('Todos os Dados Brutos')
    st.dataframe(data) # st.dataframe é melhor para exibir DataFrames

# --- Gráficos e Visualizações ---
st.header('Gráficos e Visualizações')

# 5. Gráfico de barras com st.bar_chart
st.subheader('Número de Corridas por Hora')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# 6. Mapa com st.map
st.subheader('Mapa de Corridas')
st.map(data)

# 7. Filtrando dados e exibindo no mapa
hour_to_filter = st.slider('Selecione a Hora', 0, 23, 17) # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Mapa de Corridas às {hour_to_filter}:00')
st.map(filtered_data)

# --- Widgets de Entrada ---
st.header('Widgets de Entrada de Usuário')

# 8. st.text_input para entrada de texto
user_name = st.text_input('Qual é o seu nome?', 'Visitante')
st.write(f'Olá, {user_name}!')

# 9. st.number_input para entrada de números
age = st.number_input('Qual a sua idade?', min_value=0, max_value=120, value=30)
st.write(f'Você tem {age} anos.')

# 10. st.selectbox para seleção de uma opção
options = ['Opção A', 'Opção B', 'Opção C']
selected_option = st.selectbox('Escolha uma opção', options)
st.write(f'Você escolheu: {selected_option}')

# 11. st.multiselect para seleção de múltiplas opções
multi_options = ['Maçã', 'Banana', 'Laranja', 'Uva']
selected_fruits = st.multiselect('Quais frutas você gosta?', multi_options, ['Maçã', 'Banana'])
st.write(f'Suas frutas favoritas são: {", ".join(selected_fruits)}')

# 12. st.radio para seleção de uma opção em grupo
gender = st.radio('Qual o seu gênero?', ('Masculino', 'Feminino', 'Outro'))
st.write(f'Seu gênero selecionado: {gender}')

# 13. st.button para acionar uma ação
if st.button('Clique-me!'):
    st.success('Botão clicado!')

# --- Elementos Diversos e Layout ---
st.header('Elementos Diversos e Layout')

# 14. st.image para exibir uma imagem
st.subheader('Exemplo de Imagem')
# Usando uma imagem de exemplo de automóvel do "picsum.photos"
st.image('https://picsum.photos/seed/cars/400/200', caption='Exemplo de Imagem')

# 15. st.file_uploader para upload de arquivos
st.subheader('Exemplo de Upload de Arquivo')
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv', 'txt'])
if uploaded_file is not None:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("Conteúdo do arquivo carregado:")
        st.dataframe(df_uploaded.head())
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

# 16. download de dados
st.subheader('Exemplo de Download de Dados')
# Criando um DataFrame simples para download
df_to_download = pd.DataFrame({
    'ID': [1, 2, 3],
    'Nome': ['Alice', 'Bob', 'Charlie'],
    'Idade': [25, 30, 35]
})
csv_data = df_to_download.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Baixar Dados de Exemplo",
    data=csv_data,
    file_name="dados_exemplo.csv",
    mime="text/csv",
    help="Clique para baixar um arquivo CSV de exemplo."
)

# 17. criar um layout com colunas
st.subheader('Layout com Colunas')
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Esta é a coluna 1')
    st.button('Botão na Coluna 1')
with col2:
    st.write('Esta é a coluna 2')
    st.checkbox('Checkbox na Coluna 2')
with col3:
    st.write('Esta é a coluna 3')
    st.text_input('Input na Coluna 3', 'Olá')

st.header('Mais Widgets de Entrada e Layout Avançado')

# 18. seleção de datas
st.subheader('Seleção de Data')
today = datetime.date.today()
d = st.date_input("Quando é o seu aniversário?", today)
st.write('Seu aniversário é:', d)

# 19. seleção de horários
st.subheader('Seleção de Hora')
t = st.time_input('Qual a hora da sua reunião?', datetime.time(8, 45))
st.write('Sua reunião é às', t)

# --- Organização com st.sidebar ---
st.sidebar.header(' Elementos na Barra Lateral ')
st.sidebar.write('Esta é a barra lateral. Use-a para filtros ou navegação.')

# 20. organizar widgets na barra lateral
st.sidebar.slider('Escolha um valor na sidebar', 0, 100, 50)
st.sidebar.button('Botão na Sidebar')
st.sidebar.info('Este é um widget dentro da sidebar.')


# --- Progresso e Mensagens ---
st.header('Progresso e Mensagens')

# 21. exibir uma barra de progresso
st.subheader('Barra de Progresso')
progress_text = "Operação em progresso. Por favor, aguarde."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
st.success('Operação concluída!')

# 22. st.info, st.warning, st.error, st.success 
st.subheader('Tipos de Mensagens')
st.info('Esta é uma mensagem informativa.')
st.warning('Esta é uma mensagem de aviso.')
st.error('Esta é uma mensagem de erro.')
st.success('Esta é uma mensagem de sucesso!')

# 23. conteúdo recolhível 
st.header('Conteúdo Recolhível')
with st.expander("Clique para expandir o conteúdo extra"):
    st.write("""
        Aqui está um conteúdo que o usuário pode optar por ver ou ocultar.
    """)
    st.dataframe(pd.DataFrame({'col1': [1,2,3], 'col2': ['a','b','c']}))

st.markdown("---")
st.write("Fim dos exemplos do Streamlit. Experimente modificar e explorar cada um!")