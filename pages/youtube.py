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
    
    return pd.DataFrame(comments)

# 불용어 리스트 (영어)
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his',
    'her', 'its', 'our', 'their', 'me', 'him', 'us', 'them', 'what',
    'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'not',
    'only', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now',
    'here', 'there', 'then', 'if', 'about', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'from', 'up', 'down', 'out',
    'off', 'over', 'under', 'again', 'further', 'once', 'video', 'like',
    'really', 'much', 'get', 'got', 'im', 'dont', 'cant', 'youre', 'hes',
    'shes', 'its', 'weve', 'theyre', 'ive', 'didnt', 'doesnt', 'wont',
    'br', 'http', 'https', 'www', 'com'
}

# 텍스트 전처리 함수
def clean_text(text):
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # 특수문자 제거, 소문자 변환
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    # 불용어 제거
    words = text.split()
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return ' '.join(words)

# 실행
if st.button("댓글 분석하기"):
    video_id = extract_video_id(url)
    
    if not video_id:
        st.error("올바른 YouTube 링크를 입력해주세요.")
    else:
        with st.spinner("댓글을 가져오는 중..."):
            try:
                df = get_comments(video_id)
                
                if df.empty:
                    st.warning("댓글을 찾을 수 없습니다.")
                else:
                    # 인기 댓글 Top 5
                    st.subheader("🔥 인기 댓글 Top 5")
                    top_comments = df.nlargest(5, 'likes')[['author', 'text', 'likes']]
                    st.dataframe(top_comments, use_container_width=True)
                    
                    # 워드클라우드
                    st.subheader("☁️ 워드클라우드")
                    all_text = ' '.join(df['text'].apply(clean_text))
                    
                    if all_text.strip():
                        wordcloud = WordCloud(
                            width=800,
                            height=400,
                            background_color='white',
                            colormap='viridis',
                            max_words=100
                        ).generate(all_text)
                        
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    else:
                        st.info("워드클라우드를 생성할 텍스트가 부족합니다.")
                    
                    # 통계
                    st.subheader("📊 댓글 통계")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("총 댓글 수", len(df))
                    col2.metric("총 좋아요", df['likes'].sum())
                    col3.metric("평균 좋아요", f"{df['likes'].mean():.1f}")
                    
            except Exception as e:
                st.error(f"오류 발생: {e}")

# 안내
st.divider()
st.markdown("🔑 **API 키 발급 방법**")
st.markdown("[Google Cloud Console](https://console.cloud.google.com/)에서 YouTube Data API v3를 활성화하세요.")
