import logging
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
import pandas as pd
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta


app = Flask(__name__)
swagger = Swagger(app)

# Configurar a conexão com o MongoDB Atlas
client = MongoClient("mongodb+srv://keyllabispo:1eu1YGU9f5r9z1NM@cluster0.6xcane1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Configurar o token do Slack
os.environ['SLACK_BOT_TOKEN'] = 'xoxb-7222170554023-7318378558976-Ia2Pr4x1aWh6cH6Siva5Hy6L'

# Configurações de alerta
NUM_COMENTARIOS_NEGATIVOS = 10
TEMPO_ALERTA_HORAS = 1

def send_slacks_alert(channel, text):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        
        if "message" in response and "text" in response["message"] and response["message"]["text"] == text:
            app.logger.info(f"Alerta enviado para o canal {channel} com sucesso.")
            return True
        else:
            app.logger.warning("Falha ao enviar alerta para o Slack.")
            return False
            
    except SlackApiError as e:
        app.logger.error(f"Erro ao enviar mensagem para o Slack: {e.response['error']}")
        return False

def verificar_comentarios_negativos():
    uma_hora_atras = datetime.now() - timedelta(hours=1)
    query = {
        "sentiment": -1,
        "timestamp": {"$gte": uma_hora_atras}
    }
    num_negativos = collection.count_documents(query)
    app.logger.info(f"Comentários negativos na última hora: {num_negativos}")
    
    return num_negativos

# Importar as funções do notebook
from notebook_final import pipeline_test, fazer_previsao, loaded_vectorizer, loaded_model, preprocessar_texto, classificacao_sentimento_modelo, vetorizar_texto

# Selecionar o banco de dados e a coleção
db = client.dados_uber
collection = db.uber


@app.route('/add', methods=['POST'])
def adicionar_documento():
    """
    Adiciona um novo documento na coleção e envia um alerta se houver mais de 10 comentários negativos nas últimas 2 horas.
    ---
    tags:
      - Documentos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            comment:
              type: string
            sentiment:
              type: integer
    responses:
      200:
        description: Documento adicionado
        schema:
          type: object
          properties:
            _id:
              type: string
    """
    data = request.json
    data['timestamp'] = datetime.now()  # Adiciona um timestamp ao documento
    result = collection.insert_one(data)
    
    app.logger.info("Documento adicionado. Verificando comentários negativos...")
    num_negativos = verificar_comentarios_negativos()
    
    # Verificar se há mais de 10 comentários negativos
    if num_negativos >= NUM_COMENTARIOS_NEGATIVOS:
        texto = f'⚠️ Alert: {num_negativos} negative comments in {TEMPO_ALERTA_HORAS} hour(s). For more information, visit: http://localhost:8501/'
        send_slacks_alert('#projeto-de-pln', texto)
    
    return jsonify({"_id": str(result.inserted_id)})
  

@app.route('/find', methods=['GET'])
def achar_documento():
    """
    Retorna todos os documentos da coleção.
    ---
    tags:
      - Documentos
    responses:
      200:
        description: Lista de documentos
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
              comment:
                type: string
              sentiment:
                type: integer
              comment_processed:
                type: string
    """
    docs = collection.find()
    return jsonify([{"_id": str(doc["_id"]), "comment": doc.get("comment"), "sentiment": doc.get("sentiment"), "comment_processed": doc.get("comment_processed")} for doc in docs])

@app.route('/update/<id>', methods=['PUT'])
def atualizar_documento(id):
    """
    Atualiza um documento existente na coleção.
    ---
    tags:
      - Documentos
    parameters:
      - name: id
        in: path
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            comment:
              type: string
            sentiment:
              type: integer
    responses:
      200:
        description: Contagem de documentos modificados
        schema:
          type: object
          properties:
            modified_count:
              type: integer
    """
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"modified_count": result.modified_count})

@app.route('/delete/<id>', methods=['DELETE'])
def deletar_documento(id):
    """
    Exclui um documento da coleção.
    ---
    tags:
      - Documentos
    parameters:
      - name: id
        in: path
        required: true
        type: string
    responses:
      200:
        description: Contagem de documentos excluídos
        schema:
          type: object
          properties:
            deleted_count:
              type: integer
    """
    result = collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"deleted_count": result.deleted_count})

@app.route('/preprocessar_texto', methods=['POST'])
def preprocessar_texto_route():
    """
    Preprocessa o texto fornecido e armazena o texto processado na coleção.
    ---
    tags:
      - Funções Modelo
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            texto:
              type: string
    responses:
      200:
        description: Texto processado
        schema:
          type: object
          properties:
            texto_processado:
              type: string
    """
    try:
        data = request.get_json()
        texto = data['texto']
        texto_processado = pipeline_test(texto)
        return jsonify({'texto_processado': texto_processado})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/vetorizar_texto', methods=['POST'])
def vetorizar_texto_route():
    """
    Vetoriza o texto fornecido.
    ---
    tags:
      - Funções Modelo
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            texto:
              type: string
    responses:
      200:
        description: Vetor processado
        schema:
          type: object
          properties:
            vetor:
              type: array
              items:
                type: array
                items:
                  type: number
    """
    try:
        data = request.get_json()
        texto = data['texto']
        vetor = vetorizar_texto(texto)
        return jsonify({'vetor': vetor.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/classificar_sentimento', methods=['POST'])
def classificar_sentimento_route():
    """
    Classifica o sentimento de um vetor fornecido.
    ---
    tags:
      - Funções Modelo
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            vetor:
              type: array
              items:
                type: number
    responses:
      200:
        description: Previsão de sentimento
        schema:
          type: object
          properties:
            sentimento:
              type: integer
    """
    data = request.get_json()
    vetor = data['vetor']
    if not isinstance(vetor, list):
        return jsonify({'error': 'Invalid input format, expected a list of numbers'}), 400
    vetor_np = np.array(vetor)
    sentimento = classificacao_sentimento_modelo(vetor_np)
    return jsonify({'sentimento': sentimento})

@app.route('/sentiment_analiser', methods=['POST'])
def sentiment_analiser():
    """
    Faz uma previsão do sentimento do texto fornecido.
    ---
    tags:
      - Rota geral do modelo
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            texto:
              type: string
    responses:
      200:
        description: Previsão de sentimento
        schema:
          type: object
          properties:
            previsao:
              type: string
    """
    try:
        data = request.get_json()
        app.logger.info(f"Dados recebidos: {data}")

        if not data or 'texto' not in data:
            return jsonify({'error': 'O campo "texto" é obrigatório'}), 400

        texto = data['texto']
        previsao = fazer_previsao(texto)
        return jsonify({'previsao': str(previsao)}) 
    except Exception as e:
        app.logger.error(f"Erro ao processar a requisição: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """
    Faz upload de um arquivo CSV e armazena os comentários na coleção do MongoDB.
    Envia um alerta para o Slack se houver mais de 10 comentários negativos na última hora.
    ---
    tags:
      - Documentos
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: O arquivo CSV a ser enviado
    responses:
      200:
        description: Resultados do upload e processamento dos comentários
        schema:
          type: object
          properties:
            resultados:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: string
                  comment:
                    type: string
                  sentiment:
                    type: integer
                  comment_processed:
                    type: string
      400:
        description: Erro no arquivo enviado
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Erro ao processar o arquivo CSV
        schema:
          type: object
          properties:
            error:
              type: string
    """
    file = request.files['file']
    if not file:
        return jsonify({'error': 'Nenhum arquivo fornecido'}), 400
    
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': f'Erro ao ler o arquivo CSV: {str(e)}'}), 500
    
    if 'comment' not in df.columns:
        return jsonify({'error': 'Coluna "comment" não encontrada no arquivo CSV'}), 400

    resultados = []
    for index, row in df.iterrows():
        texto = row['comment']
        
        try:
            # Preprocessar o texto
            comment_processed = preprocessar_texto(texto)
            
            # Vetorizar o texto
            vetor = vetorizar_texto(comment_processed)
            
            # Classificar o sentimento
            sentimento = classificacao_sentimento_modelo(np.array(vetor))
            
            timestamp = datetime.now()
            
            doc = {
                'comment': texto,
                'sentiment': int(sentimento),
                'comment_processed': comment_processed,
                'timestamp': timestamp
            }
            result = collection.insert_one(doc)
            
            resultados.append({
                '_id': str(result.inserted_id),
                'comment': texto,
                'sentiment': int(sentimento),
                'comment_processed': comment_processed
            })
        
        except Exception as e:
            app.logger.error(f"Erro ao processar linha {index + 1} do CSV: {str(e)}")
            resultados.append({
                'error': f"Erro ao processar linha {index + 1} do CSV: {str(e)}"
            })
    
    num_negativos = verificar_comentarios_negativos()
    if num_negativos >= NUM_COMENTARIOS_NEGATIVOS:
        texto = f'⚠️ Alert: {num_negativos} negative comments in {TEMPO_ALERTA_HORAS} hour(s). For more information, visit: http://localhost:8501/'
        if not send_slacks_alert('#projeto-de-pln', texto):
            app.logger.warning("Falha ao enviar alerta para o Slack.")
    
    return jsonify({'resultados': resultados})


if __name__ == '__main__':
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
