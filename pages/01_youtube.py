import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

st.title("💬 YouTube 댓글 분석기")

# API 키 (secrets.toml에서 불러오기)
API_KEY = st.secrets["YOUTUBE_API_KEY"]

# 유튜브 링크 입력
url = st.text_input(
    "YouTube 영상 링크를 입력하세요",
    value="https://www.youtube.com/watch?v=d95J8yzvjbQ"
)

# 영상 ID 추출 함수
def extract_video_id(url):
    patterns = [
        r'v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'embed/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# 댓글 가져오기 함수
@st.cache_data
def get_comments(video_id, max_results=100):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=min(max_results, 100),
        order='relevance'  # 인기 댓글 순
    )
    
    response = request.execute()
    
    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append({
            'author': comment['authorDisplayName'],
            'text': comment['textDisplay'],
            'likes': comment['likeCount'],
            'date': comment['publishedAt'][:10]
        })
    
