import streamlit as st
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="나의 자기소개 페이지", page_icon="👋")

# 1. 헤더 섹션
st.title("안녕하세요! 반갑습니다. 😊")
st.subheader("끊임없이 성장하는 개발자, [내 이름]입니다.")

# 2. 프로필 이미지 및 소개 (컬럼 레이아웃)
col1, col2 = st.columns([1, 2])

with col1:
    # 'profile.jpg' 파일이 코드와 같은 폴더에 있어야 합니다. 
    # 없다면 샘플 이미지를 불러옵니다.
    try:
        image = Image.open('profile.jpg')
        st.image(image, use_container_width=True)
    except:
        st.image("https://via.placeholder.com/150", caption="이미지를 등록해주세요.")

with col2:
    st.write("""
    ### About Me
    - **이름:** 홍길동
    - **역할:** 데이터 분석가 / 웹 개발자
    - **관심 분야:** 인공지능, 사용자 경험 최적화, 데이터 시각화
    - **좌우명:** "복잡한 것을 단순하게, 단순한 것을 유용하게!"
    """)

st.divider()

# 3. 기술 스택 섹션
st.header("My Skills")
st.write("사용 가능한 기술 스택입니다.")

skill_col1, skill_col2, skill_col3 = st.columns(3)
with skill_col1:
    st.markdown("#### Languages\n- Python\n- SQL\n- JavaScript")
with skill_col2:
    st.markdown("#### Frameworks\n- Streamlit\n- FastAPI\n- React")
with skill_col3:
    st.markdown("#### Tools\n- Git / GitHub\n- Docker\n- Figma")

st.divider()

# 4. 방명록 또는 연락처 섹션
st.header("Contact Me")
email = "example@email.com"
st.write(f"📧 이메일: {email}")

if st.button("응원 메시지 보내기"):
    st.balloons()
    st.success("응원해주셔서 감사합니다!")

# 사이드바 설정
st.sidebar.title("Contact Info")
st.sidebar.info(f"""
- GitHub: [github.com/myprofile](https://github.com)
- Blog: [myblog.com](https://tistory.com)
""")
