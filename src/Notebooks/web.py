import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import requests

# Configurações iniciais

st.set_page_config(
    page_title="Sensio",
    initial_sidebar_state="expanded"
)

# Função para calcular o status do sentimento baseado na porcentagem de comentários negativos
def get_status(negative_percentage):
    if negative_percentage > 80:
        return "Too Bad"
    elif negative_percentage > 60:
        return "Bad"
    elif negative_percentage > 40:
        return "Regular"
    elif negative_percentage > 20:
        return "Good"
    else:
        return "Great"

# Função para gerar nuvens de palavras
def get_trending_topics(comments, background_color='white'):
    comments = comments.dropna()
    all_words = ' '.join([text for text in comments['comment_processed']])
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color=background_color).generate(all_words)
    return wordcloud

# Sidebar

st.sidebar.title("Discover Sensio")
st.sidebar.divider()

st.sidebar.subheader("Comment Analysis")
st.sidebar.write("Users can input a comment, and the API (the system behind the dashboard) will preprocess, classify, and store the sentiment of the comment in the database. The classification result will be displayed alongside the input comment.")


st.sidebar.subheader("Database Visualization")
st.sidebar.write("Visualize the stored comments along with their sentiment classifications in a table format.")


st.sidebar.subheader("Sentiment Thermometer")
st.sidebar.write("The sentiment thermometer indicates the overall sentiment based on the percentage of negative comments out of the total. A higher percentage of negative comments indicates a poorer sentiment.")
st.sidebar.latex(r"""
\text{Sentiment Score} = \left( \frac{\text{Number of Negative Comments}}{\text{Total Comments}} \right) \times 100
                """)

st.sidebar.subheader("Sentiment Overview")
st.sidebar.write("Provides a breakdown of negative, neutral and positive comments, along with trending topics for each category.")


# Data da última atualização
last_update = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")
st.write(f"Last update: {last_update}")

# Configurar layout do Streamlit
st.title("Sensio - Sentiments Analysis")
st.write("""
This dashboard provides an overview of user sentiments regarding Uber services. It features a sentiment thermometer indicating overall sentiment status based on negative comment percentages, allows users to input and classify comments, displays the total number of negative, neutral and positive comments with trending topics for each category, and presents a table of all comments and their classified sentiments. This dashboard helps in understanding user feedback, identifying key issues, and improving service quality.
""")
st.divider()

# Input de uma frase a ser analisada
st.subheader("Input a Phrase to be Analyzed")
new_comment = st.text_input("Enter a phrase:")
if st.button("Analyze"):
    # Realiza o pré-processamento do texto para inserir no banco de dados junto com os demais dados
    preprocess_response = requests.post('http://127.0.0.1:5000/preprocessar_texto', json={'texto': new_comment})
    
    if preprocess_response.status_code == 200:
        texto_processado = preprocess_response.json().get('texto_processado')
        
        # Realiza a análise de sentimento
        response = requests.post('http://127.0.0.1:5000/sentiment_analiser', json={'texto': new_comment})
        if response.status_code == 200:
            sentiment = response.json().get('previsao')
            sentiment_label = ""
            st.write(f"The sentiment of the phrase is: {sentiment}")
            if int(sentiment) == -1:
                st.write(f"#### Classification: :red[Negative]")
                sentiment_label = -1
            elif int(sentiment) == 0:
                st.write(f"#### Classification: :gray[Neutral]")
                sentiment_label = 0
            elif int(sentiment) == 1:
                st.write(f"#### Classification: :green[Positive]")
                sentiment_label = 1
            else:
                st.write(f"Classification: No identify")
            
            # Adiciona o comentário, sentimento e texto processado ao banco de dados
            requests.post('http://127.0.0.1:5000/add', json={
                'comment': new_comment,
                'sentiment': sentiment_label,
                'comment_processed': texto_processado
            })
        else:
            st.write("Error analyzing the sentiment")
    else:
        st.write("Error preprocessing the text")

# Seção de upload de CSV
st.subheader("Upload CSV for Sentiment Analysis")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
        
        response = requests.post('http://127.0.0.1:5000/upload_csv', files={'file': uploaded_file})

        if response.status_code == 200:
            results = response.json()
            st.success("File uploaded and processed successfully!")

            df_results = pd.DataFrame(results['resultados'])
            st.dataframe(df_results)
        else:
            st.error("Error processing the CSV file")

st.divider()

# Visualização do banco e classificação de cada frase
st.subheader("View Database and Sentiment Classification")
try:
    response = requests.get('http://127.0.0.1:5000/find')
    if response.status_code == 200:
        docs = response.json()
        df = pd.DataFrame(docs)
        df['sentiment'] = df['sentiment'].replace({1: 'Positive', 0: 'Neutral', -1: 'Negative'})
        st.dataframe(df)
    else:
        st.write("Failed to retrieve data from the server")
except requests.exceptions.RequestException as e:
    st.write(f"An error occurred: {e}")

st.divider()

# Calcular métricas para o termômetro
try:
    response = requests.get('http://127.0.0.1:5000/find')
    if response.status_code == 200:
        docs = response.json()
        df = pd.DataFrame(docs)

        negative_comments = df[df['sentiment'] == -1]
        neutral_comments = df[df['sentiment'] == 0]
        positive_comments = df[df['sentiment'] == 1]

        total_comments = len(df)
        negative_percentage = (len(negative_comments) / total_comments) * 100
        current_status = get_status(negative_percentage)
    else:
        st.write('Failed to retrieve data from the server')
except requests.exceptions.RequestException as e:
    st.write(f"An error occurred: {e}")

st.header("User Sentiment Thermometer")

# Visualização do termômetro
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = negative_percentage,
    title = {'text': "Uber Status"},
    gauge = {
        'axis': {'range': [0, 100]},
        'bar': {'color': 'black'},        
        'steps': [
            {'range': [0, 20], 'color': "darkgreen"},
            {'range': [20, 40], 'color': "lightgreen"},
            {'range': [40, 60], 'color': "yellow"},
            {'range': [60, 80], 'color': "orange"},
            {'range': [80, 100], 'color': "red"}],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': negative_percentage}}))

col1, col2, col3 = st.columns([2, 0.5, 1])

with col1:
    st.plotly_chart(fig)

with col2:
    st.empty()

with col3:
    st.markdown("#### Feelings about Uber:")
    st.markdown("<div style='font-size:20px;'><span style='color:darkgreen'>⬤</span> 0-20: Great</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:20px;'><span style='color:lightgreen'>⬤</span> 21-40: Good</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:20px;'><span style='color:yellow'>⬤</span> 41-60: Regular</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:20px;'><span style='color:orange'>⬤</span> 61-80: Bad</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:20px;'><span style='color:red'>⬤</span> 81-100: Too Bad</div>", unsafe_allow_html=True)

col4, col5, col6, col7, col8 = st.columns(5)

with col4: 
    st.empty()

with col5:
    st.metric("Status", current_status)

with col6: 
    st.empty()

with col7: 
    st.metric("Negative Percentage", f"{negative_percentage:.2f}%")

with col8:
    st.empty()

st.divider()

# Quantidade total de comentários
col9, col10, col11 = st.columns([1.5, 1, 1])

with col9:
    st.empty()

with col10:
    st.metric("# Total comments", total_comments)

with col11:
    st.empty()

# Gráfico de barras para quantidade de comentários por categoria

fig_bar = go.Figure(data=[
    go.Bar(name='Negative', x=['Negative'], y=[len(negative_comments)], marker_color='red'),
    go.Bar(name='Neutral', x=['Neutral'], y=[len(neutral_comments)], marker_color='gray'),
    go.Bar(name='Positive', x=['Positive'], y=[len(positive_comments)], marker_color='green')
])
fig_bar.update_layout(barmode='group', title="Comments by Category")
st.plotly_chart(fig_bar)

st.divider()

# Determinando os comentários processados
try:
    response = requests.get('http://127.0.0.1:5000/find')
    if response.status_code == 200:
        docs = response.json()
        df_pipeline_datas = pd.DataFrame(docs)

        negative_comments_pipeline = df_pipeline_datas[df_pipeline_datas['sentiment'] == -1]
        neutral_comments_pipeline = df_pipeline_datas[df_pipeline_datas['sentiment'] == 0]
        positive_comments_pipeline = df_pipeline_datas[df_pipeline_datas['sentiment'] == 1]

        # Comentários negativos + trending topics
        st.subheader("Negative Comments + Trending Topics")
        st.write(f"#### Total: {len(negative_comments)}")
        negative_wordcloud = get_trending_topics(negative_comments_pipeline)
        st.image(negative_wordcloud.to_array(), use_column_width=True)

        st.divider()

        # Comentários neutros + trending topics
        st.subheader("Neutral Comments + Trending Topics")
        st.write(f"#### Total: {len(neutral_comments)}")
        neutral_wordcloud = get_trending_topics(neutral_comments_pipeline)
        st.image(neutral_wordcloud.to_array(), use_column_width=True)

        st.divider()

        # Comentários positivos + trending topics
        st.subheader("Positive Comments + Trending Topics")
        st.write(f"#### Total: {len(positive_comments)}")
        positive_wordcloud = get_trending_topics(positive_comments_pipeline)
        st.image(positive_wordcloud.to_array(), use_column_width=True)

    else:
        st.write('Failed to retrive data from the server')
except requests.exceptions.RequestException as e:
    st.write(f"An error occurred: {e}")
