import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS
import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import nltk
from collections import Counter
import uvicorn

nltk.download('punkt')

# Create FastAPI instance
app = FastAPI()

# Function to scrape news articles
def scrape_news(company_name):
    search_url = f"https://news.google.com/search?q={company_name}&hl=en&gl=US&ceid=US:en"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    for item in soup.find_all('article')[:10]:  # Get top 10 news
        title_tag = item.find('h3')
        summary_tag = item.find('p')
        if title_tag and summary_tag:
            title = title_tag.text
            summary = summary_tag.text
            sentiment = analyze_sentiment(summary)
            articles.append({
                "title": title,
                "summary": summary,
                "sentiment": sentiment
            })
    return articles

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Function for comparative analysis
def comparative_analysis(articles):
    sentiment_counts = Counter([article['sentiment'] for article in articles])
    topic_counts = Counter()
    for article in articles:
        words = nltk.word_tokenize(article['summary'])
        topic_counts.update(words)
    common_topics = topic_counts.most_common(5)
    return {
        "Sentiment Distribution": sentiment_counts,
        "Common Topics": common_topics
    }

# Function to generate TTS in Hindi
def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text, lang='hi')
    tts.save(filename)
    return filename

# API Endpoint
class NewsRequest(BaseModel):
    company_name: str

@app.post("/fetch_news/")
def fetch_news(data: NewsRequest):
    articles = scrape_news(data.company_name)
    analysis = comparative_analysis(articles)
    return {
        "company": data.company_name,
        "articles": articles,
        "comparative_analysis": analysis
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Streamlit Web App UI
st.title("News Summarization and Sentiment Analysis")
company_name = st.text_input("Enter Company Name")
if st.button("Fetch News"):
    articles = scrape_news(company_name)
    analysis = comparative_analysis(articles)
    df = pd.DataFrame(articles)
    st.write(df)
    st.write("### Comparative Analysis")
    st.json(analysis)
    summary_text = " ".join([art['summary'] for art in articles])
    audio_file = generate_tts(summary_text)
    st.audio(audio_file)
