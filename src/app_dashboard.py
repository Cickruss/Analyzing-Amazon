from init import app
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Configurações
nltk.download('stopwords')
ENGLISH_STOP_WORDS = set(stopwords.words('english'))

url_light = dbc.themes.MINTY
url_dark = dbc.themes.DARKLY

def get_plotly_template(theme):
    return 'plotly_dark' if theme == 'dark' else 'plotly_white'

# Importação e tratamento de dados
df_reviews = pd.read_csv('assets/Amazon_Reviews.csv', lineterminator='\n')

# Transformação de datas para formato datetime
df_reviews['Review Date'] = pd.to_datetime(df_reviews['Review Date'], errors='coerce')

# Criar coluna de ano de lançamento para análise
df_reviews['Year'] = df_reviews['Review Date'].dt.year

# Pré-processamento do texto e análise de sentimento
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuações
    text = re.sub(r'\d+', '', text)  # Remove números
    text = ' '.join([word for word in text.lower().split() if word not in ENGLISH_STOP_WORDS])
    return text

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Retorna o valor da polaridade

# Limpar texto das avaliações
df_reviews['cleaned_text'] = df_reviews['Review Text'].fillna('').apply(clean_text)

# Calcular sentimento
df_reviews['Sentiment'] = df_reviews['cleaned_text'].apply(get_sentiment)

# Filtrando dados para dashboard interativo
country_options = [{'label': country, 'value': country} for country in df_reviews['Country'].unique() if pd.notna(country)]

# Layout do site
app.layout = dbc.Container([
    html.Title('Analyzing Amazon'),
    dbc.Row([dbc.Col([ThemeSwitchAIO(aio_id='theme', themes=[url_light, url_dark])])]),
    dbc.Row([
        dbc.Col([html.H3('Análise de Avaliações de Produtos da Amazon')], width='auto'),
        dbc.Col([dcc.Dropdown(
            id='country-dropdown',
            value=country_options[0]['value'],
            multi=False,
            options=country_options,
            style={'color': '#000000'}
        )])
    ]),
    dbc.Row([dbc.Col([dcc.Graph(id='rating-distribution')])]),
    dbc.Row([dbc.Col([dcc.Graph(id='sentiment-word-frequency-positive')]), dbc.Col([dcc.Graph(id='sentiment-word-frequency-negative')])]),
    dbc.Row([dbc.Col([dcc.Graph(id='review-trend')])]),
])

# Callbacks das funções

# Distribuição de Ratings
@app.callback(
    Output('rating-distribution', 'figure'),
    Input('country-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_rating_distribution(selected_country, theme):
    plotly_template = get_plotly_template('light' if theme else 'dark')
    df_filtered = df_reviews[df_reviews['Country'] == selected_country]

    fig = px.histogram(
        df_filtered,
        x='Rating',
        title='Distribuição de Ratings por País',
        template=plotly_template
    )
    return fig

# Gráfico de Palavras Mais Frequentes por Sentimento
@app.callback(
    Output('sentiment-word-frequency-positive', 'figure'),
    Output('sentiment-word-frequency-negative', 'figure'),
    Input('country-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_sentiment_word_frequency(selected_country, theme):
    plotly_template = get_plotly_template('light' if theme else 'dark')
    df_filtered = df_reviews[df_reviews['Country'] == selected_country]

    # Filtrar textos positivos e negativos
    text_positive = ' '.join(df_filtered[df_filtered['Sentiment'] > 0]['cleaned_text'])
    text_negative = ' '.join(df_filtered[df_filtered['Sentiment'] < 0]['cleaned_text'])

    # Contar palavras mais frequentes
    word_freq_positive = Counter(text_positive.split())
    word_freq_negative = Counter(text_negative.split())

    # Criar DataFrames para as 10 palavras mais frequentes
    df_positive = pd.DataFrame(word_freq_positive.most_common(10), columns=['word', 'count'])
    df_negative = pd.DataFrame(word_freq_negative.most_common(10), columns=['word', 'count'])

    # Gráfico de barras para palavras positivas
    fig_positive = px.bar(df_positive, x='word', y='count', title='Análise de Palavras - Sentimento Positivo', template=plotly_template)

    # Gráfico de barras para palavras negativas
    fig_negative = px.bar(df_negative, x='word', y='count', title='Análise de Palavras - Sentimento Negativo', template=plotly_template)

    return fig_positive, fig_negative

# Tendência de Avaliações ao longo do Tempo
@app.callback(
    Output('review-trend', 'figure'),
    Input('country-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_review_trend(selected_country, theme):
    plotly_template = get_plotly_template('light' if theme else 'dark')
    df_filtered = df_reviews[df_reviews['Country'] == selected_country]

    trend = df_filtered.groupby(df_filtered['Review Date'].dt.to_period('M')).size().reset_index(name='counts')
    trend['Review Date'] = trend['Review Date'].astype(str)

    fig = px.line(
        trend,
        x='Review Date',
        y='counts',
        title='Tendência de Avaliações ao Longo do Tempo',
        template=plotly_template
    )
    return fig