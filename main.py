import streamlit as st

# 페이지 설정 (가장 상단에 위치해야 합니다)
st.set_page_config(
    page_title="✨ MBTI 진로 탐색 센터 ✨",
    page_icon="🚀",
    layout="wide"
)

# 커스텀 CSS로 디자인 입히기
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .mbti-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 정의 (예시 데이터)
mbti_jobs = {
    "INTJ": {"title": "용의주도한 전략가 🧠", "jobs": "데이터 과학자, 전략 기획자, 소프트웨어 아키텍트", "desc": "분석력이 뛰어나고 복잡한 문제를 해결하는 것을 즐깁니다."},
    "ENFP": {"title": "재기발랄한 활동가 🌈", "jobs": "홍보 전문가, 크리에이티브 디렉터, 상담사", "desc": "창의적이고 에너지가 넘치며 사람들과 소통하는 것을 좋아합니다."},
    "INFJ": {"title": "선의의 옹호자 🕊️", "jobs": "심리학자, 작가, 비영리 단체 운영자", "desc": "통찰력이 깊고 타인에게 영감을 주는 일에서 보람을 느낍니다."},
    "ESTP": {"title": "모험을 즐기는 사업가 🏎️", "jobs": "기업가, 소방관, 스포츠 마케터", "desc": "행동력이 빠르고 현실적인 문제를 해결하는 데 능숙합니다."},
    # ... 다른 MBTI 유형도 이와 같은 형식으로 추가 가능합니다.
}

# 헤더 부분
st.title("🚀 내 꿈을 찾는 MBTI 여행")
st.subheader("나의 MBTI를 선택하고 딱 맞는 직업을 추천받아 보세요! ✨")

# 레이아웃 나누기
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### 🔍 나의 유형 선택")
    selected_mbti = st.selectbox(
        "당신의 MBTI는 무엇인가요?",
        ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
         "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    )
    
    btn = st.button("추천 직업 보기! 🎈")

with col2:
    if btn:
        # 화려한 효과 추가
        st.balloons()
        
        if selected_mbti in mbti_jobs:
            data = mbti_jobs[selected_mbti]
            
            st.markdown(f"""
            <div class="mbti-card">
                <h2>{selected_mbti}: {data['title']}</h2>
                <hr>
                <h4>🌟 추천 직업</h4>
                <p style="font-size: 1.2em;"><b>{data['jobs']}</b></p>
                <h4>📝 특징</h4>
                <p>{data['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"💡 {selected_mbti} 유형은 자신의 강점을 살릴 때 가장 빛이 납니다!")
        else:
            st.warning("아직 상세 데이터가 준비 중인 유형입니다. 곧 업데이트될 예정이에요! 🛠️")
    else:
        st.write("👈 왼쪽에서 MBTI를 선택하고 버튼을 눌러주세요!")

# 하단 장식
st.divider()
st.caption("© 2024 MBTI Career Guide - 여러분의 꿈을 응원합니다! 🌠")
