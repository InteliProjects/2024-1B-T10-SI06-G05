# Processamento de Linguagem Natural

## Moodfy

## Integrantes:
- <a href="https://www.linkedin.com/in/keylla-oliveira1206/">Keylla Oliveira</a>
- <a href="https://www.linkedin.com/in/nicollas-isaac/">Nicollas Isaac</a>
- <a href="https://www.linkedin.com/in/pedro-henrique-oliveira-lima-a6a766214/">Pedro Henrique Lima</a>
- <a href="https://www.linkedin.com/in/matheusmeendes/">Matheus Mendes</a>
- <a href="https://www.linkedin.com/in/michel-menahem-khafif-512791201/">Michel Khafif</a>
- <a href="https://www.linkedin.com/in/stefano-parente/">Stefano Parente</a>
- <a href="https://www.linkedin.com/in/samuel-martins-lopes-nascimento-7a805526a/">Samuel Lopes</a>

## Professores:

### Orientador
- Renato Penha
  
### Instrutores
- Ana Cristina
- Fabiana Martins de Oliveira
- Pedro Teberga
- Ricardo José Missori
- Victor Hayashi
  
## Descrição
Este projeto foi desenvolvido especificamente para a Uber e consiste em uma solução de Processamento de Linguagem Natural (NLP) para análise de sentimentos de comentários mencionando a empresa Uber em redes sociais. A implementação deste projeto é de extrema relevância para as estratégias de social listening da Uber, permitindo que a empresa monitore e analise as percepções do público de forma eficiente e em tempo real. O projeto foi construído ao longo de 10 semanas, período no qual foram aplicadas técnicas avançadas de NLP para garantir precisão e relevância nos insights gerados a partir dos dados coletados.

## Link de demonstração
_Coloque aqui o link para seu projeto publicado e link para vídeo de demonstração_

## Estrutura de Pastas

A estrutura do projeto é organizada da seguinte maneira para facilitar a navegação e o entendimento do código:

- **docs/**: Contém toda a documentação relacionada ao projeto, incluindo análises e detalhes adicionais.
  - **assets/**: Armazena arquivos de mídia e outros recursos utilizados na documentação.
  - **documentacao.md**: Documentação detalhada do projeto.
  - **README.md**: Links para cada artefato do projeto.

- **src/**: Diretório principal que contém o código fonte do projeto.
  - **Notebooks/**: Pasta que contém notebooks Jupyter para análise de dados e experimentação.
    - **dados.csv**: Conjunto de dados utilizado nos notebooks.
    - **notebook.ipynb**: Notebook Jupyter principal com a lógica de análise de dados.
    - **pipeline_comments.csv**: Dados específicos utilizados para processos no pipeline de dados.

- **requirements.txt**: Arquivo que lista todas as bibliotecas necessárias para executar o projeto acompanhado com as versões corretas.

- **README.md**: Arquivo de texto com instruções básicas sobre o projeto, como configurá-lo e executá-lo.


## Configuração para desenvolvimento e execução do código

### Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes pré-requisitos instalados em sua máquina:

- **Python**: Uma versão atualizada do Python deve estar instalada. Você pode baixar a última versão do Python do [site oficial](https://www.python.org/downloads/).

- **IDE ou editor de texto**: Recomenda-se o uso de uma IDE ou editor de texto adequado para programação em Python, como Visual Studio Code, PyCharm, ou Jupyter Notebook.

### Instalação

1. **Clonar o repositório**: Primeiramente, você precisará clonar o repositório do projeto para sua máquina local. Abra o terminal e digite o seguinte comando:
   ```
   git clone [https://github.com/Inteli-College/2024-1B-T10-SI06-G05]
   ```

2. **Instalar as dependências**: Navegue até a pasta do projeto clonado e instale as dependências necessárias executando:
   ```
   pip install -r requirements.txt
   ```
   Esse comando irá instalar todas as bibliotecas necessárias listadas no arquivo `requirements.txt`.

### Execução
1. **Abrir o projeto**: Abra a pasta do projeto no seu editor de texto ou IDE preferido.

2. **Abrir o notebook**: Navegue até a pasta `notebooks` dentro do projeto. Abra o notebook nomeado como `notebook_completo` (com extensão `.ipynb`) usando Jupyter Notebook ou outro software que suporte notebooks.

3. **Executar o notebook**: Execute todas as células do `notebook_completo` para gerar os arquivos `.pkl` necessários para o funcionamento da API.

4. **Executar a API**: Certifique-se de estar na pasta `notebooks` dentro do projeto, após concluída a verificação, digite o seguinte comando no terminal: 

   ```
   python app.py
   ```
   O mesmo iniciará a execução da API e você verá um endpoint localhost como este: `https://127.0.0.1:5000/`

5. **Endpoint**: Após executar a API, e com a aplicação localhost funcionando, navega até o Endpoint desejado: pré processamento, vetorização, classificação com modelo ou rota geral. Para mais detalhes acerca dos endpoints, veja a seção <a href="https://github.com/Inteli-College/2024-1B-T10-SI06-G05/blob/main/docs/documentacao.md#c4"> 4</a> da documentação.

Essas etapas garantirão que você consiga configurar e rodar o projeto de análise de sentimentos para a Uber em sua máquina local.


## Histórico de lançamentos
* 0.1.0 - 26/04/2024
    *Artefatos: Entendimento do Negócio e Entendimento da Experiência do Usuário
* 0.2.0 - 10/05/2024
    *Artefatos: Modelo de Bag of Words (IPYNB) e Documentação do Modelo de Bag of Words
* 0.3.0 - 24/05/2024
    *Artefatos: Modelo utilizando Word2Vec (IPYNB) e Documentação do Modelo de Bag of Words
* 0.4.0 - 07/06/2024
    *Artefatos: Implementação da API (IPYNB) e Documentação da API
* 0.5.0 - 21/06/2024
    *Artefatos: Apresentação Final, Deploy do melhor modelo e Documentação da Solução
  
## Tecnologias Utilizadas

Este projeto integra uma variedade de tecnologias para realizar o processamento de linguagem natural, desenvolver uma API funcional e criar uma interface interativa. Abaixo estão as principais tecnologias utilizadas:

Python: Linguagem de programação amplamente usada para desenvolvimento de scripts de processamento de dados e modelos de machine learning, utilizando bibliotecas como Pandas, NumPy, NLTK, entre outras.

Jupyter Notebook: Ambiente interativo que facilita o desenvolvimento e a execução de código Python, muito usado em análise de dados e construção de modelos.

Flask: Microframework web em Python que simplifica o desenvolvimento de APIs leves e eficientes.

Swagger: Conjunto de ferramentas que ajudam a projetar, construir, documentar e consumir APIs RESTful.

Streamlit: Ferramenta Python para criar aplicativos web interativos e compartilháveis com facilidade, ideal para data science e machine learning.

Slack: Plataforma de colaboração usada para integrar notificações e interações com a aplicação.

TensorFlow: biblioteca para deep learning, essenciais na construção e treinamento de redes neurais complexas.

MongoDB: Banco de dados NoSQL orientado a documentos, ideal para armazenar dados não estruturados e semiestruturados.

## Licença/License
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1">
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Inteli-College/2024-1B-T10-SI06-G03">MODELO GIT INTELI</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://www.inteli.edu.br/">Inteli, <a href="https://github.com/keylla-oliveira1206">Keylla Oliveira</a>, <a href="https://github.com/nicollas-isaac">Nicollas Isaac</a>, <a href="https://github.com/pedro-henrique-oliveira-lima">Pedro Henrique Lima</a>, <a href="https://github.com/matheusmeendes">Matheus Mendes</a>, <a href="https://github.com/michel-menahem-khafif">Michel Khafif</a>, <a href="https://github.com/stefano-parente">Stefano Parente</a>, <a href="https://github.com/samuel-martins-lopes-nascimento">Samuel Lopes</a> is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
