# Analyzing-Amazon

Este projeto visa analisar e visualizar avaliações de produtos da Amazon, proporcionando insights valiosos sobre a experiência do usuário e as tendências de sentimento ao longo do tempo. Utilizando Dash e Plotly, criamos um dashboard interativo que permite a exploração de dados de forma dinâmica.

## Funcionalidades

- **Análise de Sentimento**: Avaliações de produtos são processadas para determinar o sentimento (positivo, neutro ou negativo) usando técnicas de processamento de linguagem natural (PNL).
  
- **Visualizações Interativas**:
  - **Distribuição de Ratings**: Um gráfico que mostra a distribuição das classificações dadas pelos usuários, filtradas por país.
  - **Tendência de Avaliações**: Um gráfico que ilustra como o número de avaliações mudou ao longo do tempo.
  - **Frequência de Palavras**: Um gráfico que exibe as palavras mais comuns nas avaliações, separadas por sentimento (positivo e negativo).

## Tecnologias Utilizadas

- **Dash**: Uma estrutura de aplicativo web para Python que facilita a criação de visualizações interativas.
- **Plotly**: Biblioteca para gráficos interativos.
- **Pandas**: Biblioteca de manipulação de dados que permite o tratamento e a análise de grandes volumes de dados.
- **TextBlob**: Biblioteca para processamento de texto e análise de sentimentos.
- **NLTK**: Biblioteca para o processamento de linguagem natural em Python.

## Como Usar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git

2. **Instale as dependencias**:
   ```bash
   pip install -r requirements.txt

1. **Execute o aplicativo**:
   ```bash
   python app.py
