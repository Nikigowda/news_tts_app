# News Summarization and TTS App

This application fetches news articles for a given company, performs sentiment analysis, comparative analysis, and generates Hindi speech output.

## Features
- Extracts news articles from Google News
- Analyzes sentiment as Positive, Negative, or Neutral
- Provides comparative analysis based on sentiment distribution and common topics
- Converts summarized news into Hindi speech
- Offers an API using FastAPI
- Simple Streamlit web interface

## Setup
```sh
pip install -r requirements.txt
python app.py
streamlit run app.py
```

## API Usage
- `POST /fetch_news/` with `{ "company_name": "Tesla" }` to fetch news and sentiment analysis.

## Deployment
This application is designed for deployment on Hugging Face Spaces.
