#!/usr/bin/env python
# coding: utf-8

# # Notebook Final
# 
# Neste arquivo, encontra-se o modelo escolhido para compor a entrega final do projeto. O algoritmo apresentado foi selecionado com base em seus resultados, que se destacaram entre todos os modelos testados, considerando nossas métricas de avaliação (accuracy, precision, recall e F1-score).
# 
# Vale ressaltar que o modelo presente neste arquivo é o que está integrado em nossa API e realiza a classificação de sentimentos. O arquivo está dividido nas seguintes etapas:
# 
# - Importação de bibliotecas
# - Pré-processamento dos dados
# - Vetorização dos dados
# - Modelo de Machine Learning
# - Exportação do modelo
# 
# O conteúdo abrange apenas os elementos essenciais para nossa API e o projeto como um todo.

# ### Importação das bibliotecas

# A importação de bibliotecas é o primeiro passo em um projeto de machine learning. Consiste em trazer para o ambiente de trabalho os pacotes e módulos necessários que contêm funções e ferramentas pré-construídas. Essas bibliotecas facilitam a manipulação de dados, a construção de modelos, a análise estatística e a visualização de resultados.

# In[2]:


import pandas as pd
import nltk
import re
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from nltk.corpus import wordnet
from nltk import pos_tag
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag
from spellchecker import SpellChecker

# Baixar os recursos necessários do NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")


# ### Pré-Processamento dos dados

# O pré-processamento dos dados envolve a preparação dos dados brutos para que possam ser usados de maneira eficaz pelo modelo de machine learning. O objetivo é melhorar a qualidade dos dados, utilizando de técnicas como, remoção de stopwords, tokenização, entre outras, o que, por sua vez, melhora o desempenho do modelo.

# ##### Tokenização

# In[15]:


def tokenize_text(text):
    """
    Tokeniza o DataFrame em uma lista de tokens.

    Args:
    text (DataFrame): Comentários a serem tokenizados.

    Returns:
    list: Lista de tokens.
    """
    tokens = word_tokenize(text.lower())
    return tokens

def filter_empty_tokens(tokens):
    """
    Remove listas vazias ou com espaços vazios.

    Args:
    tokens (list): Lista de tokens.

    Returns:
    list: Lista de tokens não vazios.
    """
    return [token for token in tokens if token.strip()]


# ##### Lemmatização

# In[14]:


def get_wordnet_pos(treebank_tag):
    """
    Retorna o tag correspondente do WordNet para o tag do Treebank do Penn.
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN 

def lemmatize_tokens_with_pos(tokens):
    """
    Lemmatiza uma lista de tokens baseando-se em sua parte do discurso.

    Args:
    tokens (list of str): Tokens a serem lematizados.

    Returns:
    list: Lista de lemas das palavras.
    """
    # Criar um Doc do spaCy a partir dos tokens
    doc = nlp(" ".join(tokens))

    # Lemmatiza usando o spaCy
    lemmas = [token.lemma_ for token in doc]
    return lemmas


# ##### Remoção de pontuação

# In[13]:


def remove_punctuation_from_tokens(tokens):
    """
    Remove pontuações de uma lista de tokens e exclui os tokens que consistem exclusivamente de caracteres de pontuação.

    Args:
    tokens (list): Lista de tokens a serem processados.

    Returns:
    list: Lista de tokens sem pontuações.
    """
    # Regex para identificar pontuações
    regex_punctuation = re.compile('[%s]' % re.escape(string.punctuation))

    # Remove pontuações de cada token e filtra tokens que ficaram vazios ou são apenas pontuações
    tokens_no_punct = [regex_punctuation.sub('', token) for token in tokens]
    tokens_no_punct = [token for token in tokens_no_punct if token.strip() != '']

    return tokens_no_punct


# ##### Remoção de números

# In[12]:


def remove_numbers_from_tokens(tokens):
    """
    Remove todos os dígitos de uma lista de tokens e remove os tokens que consistem exclusivamente de números.

    Args:
    tokens (list): Lista de tokens a serem processados.

    Returns:
    list: Lista de tokens sem números.
    """
    # Remover dígitos de cada token e depois filtrar os tokens que são apenas números ou ficaram vazios
    tokens_no_numbers = [re.sub(r'\d+', '', token) for token in tokens]
    tokens_no_numbers = [token for token in tokens_no_numbers if token.strip() != '']
    return tokens_no_numbers


# ##### Remoção de Stop Words

# In[11]:


def remove_stopwords_preserve_adverbs_conjunctions(tokens):
    """
    Remove stopwords from a list of tokens while preserving all adverbs and conjunctions, 
    which are crucial for maintaining the logical flow and structure of sentences.

    Args:
    tokens (list): List of tokens to be processed.

    Returns:
    list: List of tokens without stopwords, with all adverbs and conjunctions preserved.
    """
    if not isinstance(tokens, list):
        raise TypeError("Input tokens must be a list")
    
    # Loading stopwords
    stop_words = set(stopwords.words('english'))
    
    # Classifying tokens by parts of speech
    tagged_tokens = pos_tag(tokens)
    
    # Filtering tokens to remove stopwords but keep adverbs (tagged as 'RB') and conjunctions (tagged as 'CC' for coordinating, 'IN' for subordinating)
    filtered_tokens = [
        word for word, tag in tagged_tokens 
        if word.lower() not in stop_words 
        or tag.startswith('RB')  # Adverbs
        or tag in ('CC', 'IN')  # Conjunctions
    ]

    return filtered_tokens


# ##### Remoção de URL's

# In[10]:


# Definir a função para remover URLs
def remove_urls(text):
    """
    Remove URLs de um texto fornecido.

    Args:
    texto (list): O texto de entrada contendo URLs.

    Returns:
    list: Lista de tokens com URLs removidas.
    """
    return re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE)


# ##### Correção de texto

# In[9]:


from spellchecker import SpellChecker

def spell_checker(words):
    """
    Corrige a ortografia de uma lista de palavras usando pyspellchecker,
    com exceções para palavras específicas. Garante que nenhum valor None seja retornado.

    Args:
        words (list of str): Lista de palavras a serem corrigidas.

    Returns:
        str: Texto com a ortografia corrigida.
    """
    spell = SpellChecker()
    exceptions = {'uber', 'unsafe'}
    corrected_words = []

    for word in words:
        # Asegurar que a palavra não é None
        if word is None:
            corrected_words.append('')
        elif word.lower() in exceptions:
            corrected_words.append(word)
        else:
            # Obter a melhor sugestão de correção
            corrected_word = spell.correction(word) if word else ''
            corrected_words.append(corrected_word if corrected_word else '')

    # Assegurar que todos os elementos sejam strings
    corrected_words = [w if w is not None else '' for w in corrected_words]
    corrected_text = ' '.join(corrected_words)
    return corrected_text


# ##### Balanceamento dos dados

# In[8]:


def remove_outliers_balance_negatives_and_multiply_positives(df):
    """
    Remove outliers do comprimento dos comentários para a classe de sentimentos negativos (-1),
    baseando-se nos quartis da própria classe negativa, e remove aleatoriamente 40% dos dados negativos
    restantes para ajudar no balanceamento das classes. Multiplica os dados da classe positiva (1) por 2,5 vezes
    para aumentar sua representatividade no dataset.

    Args:
        df (DataFrame): DataFrame contendo as colunas 'sentiment', 'comment', e 'comment_length'.

    Returns:
        DataFrame: DataFrame com outliers removidos da classe negativa, redução estratégica de 40% dos negativos,
                    e multiplicação dos dados positivos por 2,5 vezes.
    """
    # Adiciona a coluna 'comment_length' ao DataFrame se não existir
    if 'comment_length' not in df.columns:
        df['comment_length'] = df['comment'].apply(len)

    # Adiciona a coluna 'word_count'
    df['word_count'] = df['comment'].apply(lambda x: len(x.split()))
    
    # Filtra os dados para a classe negativa (-1)
    negativos = df[df['sentiment'] == -1]
    
    # Calcula os quartis apenas para a classe negativa
    Q1 = negativos['comment_length'].quantile(0.25)
    Q3 = negativos['comment_length'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR

    # Filtra os outliers na classe negativa baseado no limite calculado
    negativos_filtrados = negativos[negativos['comment_length'] <= upper_bound]
    
    # Amostragem aleatória para remover 25% dos dados negativos filtrados
    negativos_reduzidos = negativos_filtrados.sample(frac=0.80, random_state=42)

    # Multiplica os dados da classe positiva (1) por 2,5 vezes
    positivos = df[df['sentiment'] == 1]
    positivos_multiplicados = pd.concat([positivos] * 2 + [positivos.sample(frac=0.5, random_state=42)], ignore_index=True)
    
    # Combina os dados reduzidos de sentimentos negativos com as outras classes
    df_final = pd.concat([negativos_reduzidos, df[df['sentiment'] == 0], positivos_multiplicados], ignore_index=True)

    return df_final


# ##### Contrações

# In[7]:


def expand_contractions(text):
    """
    Expande contrações em um texto dado com base em um mapeamento fornecido.

    Args:
        text (str): Texto que contém contrações.
        contraction_mapping (dict): Um dicionário mapeando contrações para suas formas expandidas.

    Returns:
        str: Texto com todas as contrações expandidas de acordo com o mapeamento.
    """
    contraction_map = {
    "can't": "can not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "won't": "will not",
    "wouldn't": "would not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't've": "cannot have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "could've": "could have",
    "could've": "could have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "i'm": "i am",
    "you're": "you are",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "we're": "we are",
    "they're": "they are",
    "i've": "i have",
    "you've": "you have",
    "we've": "we have",
    "they've": "they have",
    "i'd": "i would",
    "you'd": "you would",
    "he'd": "he would",
    "she'd": "she would",
    "we'd": "we would",
    "they'd": "they would",
    "i'll": "i will",
    "you'll": "you will",
    "he'll": "he will",
    "she'll": "she will",
    "we'll": "we will",
    "they'll": "they will",
}
    
    for contraction, expansion in contraction_map.items():
        text = text.replace(contraction, expansion)
    return text


# ### Exportação do modelo

# In[6]:


def pipeline_test(text):
    text = remove_urls(text)
    tokens = tokenize_text(text)
    tokens = lemmatize_tokens_with_pos(tokens)
    tokens = remove_punctuation_from_tokens(tokens)
    tokens = remove_numbers_from_tokens(tokens)
    tokens = remove_stopwords_preserve_adverbs_conjunctions(tokens)
    tokens = filter_empty_tokens(tokens)
    tokens = spell_checker(tokens)
    return tokens


# In[1]:


import pickle

modelo_path = 'stack_model.pkl'
vectorizer_path = 'vectorizer.pkl'

with open(modelo_path, 'rb') as file:
    loaded_model = pickle.load(file)

with open(vectorizer_path, 'rb') as file:
    loaded_vectorizer = pickle.load(file)

def preprocessar_texto(texto):
    """
    Preprocessa o texto usando uma pipeline de processamento definida.

    Args:
    texto (str): Texto a ser processado.

    Returns:
    str: Texto processado.
    """
    # Supondo que 'pipeline_test' seja uma função definida em outro lugar que processa o texto
    return pipeline_test(texto)

def vetorizar_texto(texto):
    """
    Transforma o texto em vetor bigrams.

    Args:
    texto (str): Texto a ser vetorizado.

    Returns:
    list: Vetor como lista de listas.
    """
    comentario_vetorizado = loaded_vectorizer.transform([texto])
    return comentario_vetorizado.toarray().tolist()

def classificacao_sentimento_modelo(comentario_vetorizado):
    """
    Faz uma previsão usando o vetor.

    Args:
    comentario_vetorizado (np.array): Vetor de comentário, deve ser um array 1D.

    Returns:
    int: Previsão de sentimento.
    """
    # Verifica se o array é 1D e o reformata para 2D
    if comentario_vetorizado.ndim == 1:
        comentario_vetorizado = comentario_vetorizado.reshape(1, -1)

    previsao = loaded_model.predict(comentario_vetorizado)
    return int(previsao[0])  # Converte para int, garantindo compatibilidade com JSON

def fazer_previsao(comentario):
    """
    Faz previsão de um comentário usando o modelo e o vetorizador carregados.

    Args:
    comentario (str): Comentário para o qual se deseja fazer a previsão.

    Returns:
    str: Previsão do modelo para o comentário.
    """
    texto_processado = preprocessar_texto(comentario)
    comentario_vetorizado = loaded_vectorizer.transform([texto_processado])
    previsao = loaded_model.predict(comentario_vetorizado)
    return previsao[0]

