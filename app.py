import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import streamlit.components.v1 as components
import io
import base64
import os
import urllib.request
import google.generativeai as genai

# ==========================================
# 🎨 [원장님 전용] 학원 로고 및 테마 색상 세팅존
# ==========================================
LOGO_COLOR = "#1A3263"  
LOGO_LIGHT_BG = "#F4F6F9" 
# ==========================================

# --- [서버용 한글 폰트 강제 다운로드 및 설정] ---
@st.cache_resource
def load_korean_font():
    font_dir = "fonts"
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    font_path = os.path.join(font_dir, "NanumGothic.ttf")
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        try: urllib.request.urlretrieve(url, font_path)
        except: pass
    if os.path.exists(font_path):
        import matplotlib.font_manager as fm
        fm.fontManager.addfont(font_path)
        prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=prop.get_name())
    else:
        plt.rc('font', family='sans-serif')
    matplotlib.rcParams['axes.unicode_minus'] = False

load_korean_font()

# --- [로고 이미지 로드] ---
logo_html = ""
if os.path.exists("logo.jpg"):
    with open("logo.jpg", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    logo_html = f'<img src="data:image/jpeg;base64,{encoded_logo}" style="width:75px; height:75px; border-radius:50%; margin-right:15px; border:2px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'

# --- [AI 구글 API 연동 설정] ---
if "GEMINI_API_KEY" in st.secrets:
    raw_key = st.secrets["GEMINI_API_KEY"]
    clean_key = raw_key.strip().replace('"', '').replace("'", "")
    genai.configure(api_key=clean_key)
    ai_available = True
else:
    ai_available = False

# 웹페이지 기본 설정 및 로고 테마 색상 강제 매칭 디자인 주입
st.set_page_config(page_title="YMS English Monthly Test", layout="centered")

st.markdown(f"""
    <style>
    div.stButton > button:first-child {{
        background-color: {LOGO_COLOR} !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #2c4a85 !important;
        color: white !important;
        box-shadow: 0 5px 10px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }}
    h1, h2, h3 {{
        color: {LOGO_COLOR} !important;
        font-weight: 700;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("📝 YMS English Monthly Test 생성기")
st.caption("원장님의 제미나이 2.5 진짜 AI 엔진과 수학과 레이아웃 헤더가 결합된 최종 무결점 버전입니다.")
st.markdown("---")

# 1. 학생 기본 정보 입력
st.subheader("👤 1. 학생 기본 정보")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("학생 이름", value="김YMS")
    evaluation_month = st.selectbox("평가월", ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"], index=5)
with col2:
    current_book = st.text_input("현재 교재", value="English Stars Level 2")
    school_type = st.radio("과정 선택", ["초등부", "중등부"], horizontal=True)
    if school_type == "초등부":
        student_level = st.selectbox("학년 선택", ["초등 1학년", "초등 2학년", "초등 3학년", "초등 4학년", "초등 5학년", "초등 6학년"], index=3)
    else:
        student_level = st.selectbox("학년 선택", ["중등 1학년", "중등 2학년", "중등 3학년"])

st.markdown("---")

# 2. 이번 달 평가 영역 선택
st.subheader("🎯 2. 이번 달 평가 영역 선택")
st.info("다섯 가지 영역 중 이번 달에 시험을 치른 영역을 모두 체크해 주세요.")
all_subjects = ["어휘 (Vocabulary)", "독해 (Reading)", "쓰기 (Writing)", "문법 (Grammar)", "듣기 (Listening)"]
selected_subjects = []
cols = st.columns(5)
for idx, subj_name in enumerate(all_subjects):
    with cols[idx]:
        is_checked = subj_name in ["어휘 (Vocabulary)", "독해 (Reading)", "쓰기 (Writing)"]
        if st.checkbox(subj_name.split()[0], value=is_checked, key=f"chk_{idx}"):
            selected_subjects.append(subj_name)

st.markdown("---")

# 3. 영역별 성적 입력
st.subheader("📊 3. 영역별 성적 입력")
past_scores = []
current_scores = []
if not selected_subjects:
    st.warning("⚠️ 평가 영역을 선택해 주세요.")
else:
    for subj in selected_subjects:
        col_subj1, col_subj2 = st.columns(2)
        with col_subj1:
            past = st.number_input(f"[{subj}] 지난달 점수", min_value=0, max_value=100, value=80, key=f"past_{subj}")
            past_scores.append(past)
        with col_subj2:
            curr = st.number_input(f"[{subj}] 이번달 점수", min_value=0, max_value=100, value=90, key=f"curr_{subj}")
            current_scores.append(curr)

st.markdown("---")

# 4. 원장님 사양 제미나이 2.5 진짜 AI 엔진 가동
st.subheader("✍️ 4. AI 명품 종합 의견 생성")
if not ai_available:
    st.error("⚠️ Streamlit 설정창에 GEMINI_API_KEY가 등록되지 않았습니다. 기본 양식으로 작동합니다.")
    teacher_feedback = st.text_area("종합 의견 입력", value="학습 전반에 걸쳐 좋은 성취를 보였습니다.")
else:
    st.success("🤖 구글 제미나이 2.5 진짜 AI 엔진이 성적 분석 및 실시간 창작 모드로 활성화되었습니다.")
    
    custom_pos = st.text_input("👍 이번 달 학생의 칭찬/강점 키워드 입력", value="문법 점수가 많이 오름")
    custom_neg = st.text_input("🌱 이번 달 학생의 보완/노력 키워드 입력", value="수업 집중도 주춤함")
    
    if st.button("🤖 AI에게 실시간 5문장 창작 추천받기", type="secondary"):
        with st.spinner("AI가 학생의 점수 변화와 키워드를 분석하여 5문장 코멘트를 생성하고 있습니다..."):
            try:
                score_summary = ""
                for idx, subj in enumerate(selected_subjects):
                    score_summary += f"-
