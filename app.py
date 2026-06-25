import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import streamlit.components.v1 as components
import io
import base64
import os
import urllib.request

# --- [서버용 한글 폰트 강제 다운로드 및 설정] ---
@st.cache_resource
def load_korean_font():
    font_dir = "fonts"
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    font_path = os.path.join(font_dir, "NanumGothic.ttf")
    
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        try:
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            pass
            
    if os.path.exists(font_path):
        import matplotlib.font_manager as fm
        fm.fontManager.addfont(font_path)
        prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=prop.get_name())
    else:
        plt.rc('font', family='sans-serif')
        
    matplotlib.rcParams['axes.unicode_minus'] = False

load_korean_font()

# --- [로고 이미지 로컬 파일 로드 로직] ---
logo_html = ""
if os.path.exists("logo.jpg"):
    with open("logo.jpg", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    logo_html = f'<img src="data:image/jpeg;base64,{encoded_logo}" style="width:75px; height:75px; border-radius:50%; margin-right:15px; border:2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'

# 웹페이지 기본 설정
st.set_page_config(page_title="YMS English Monthly Test", layout="centered")

st.title("📝 YMS English Monthly Test 생성기")
st.caption("키워드 직접 입력 시스템과 공식 로고가 탑재된 통합 대시보드입니다.")
st.markdown("---")

# 1. 학생 기본 정보 입력
st.subheader("👤 1. 학생 기본 정보")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("학생 이름", value="김YMS")
    evaluation_month = st.selectbox("평가월", ["6월", "7월", "8월", "9월", "10월", "11월", "12월"])

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

# 3. 선택된 영역별 성적 입력
st.subheader("📊 3. 영역별 성적 입력 (100점 만점)")

past_scores = []
current_scores = []

if not selected_subjects:
    st.warning("⚠️ 최소 한 개 이상의 평가 영역을 선택하셔야 점수를 입력할 수 있습니다.")
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

# --- [수정 포인트] 4. 키워드 기반 선생님 종합 피드백 자동 생성기 (직접 입력 진화) ---
st.subheader("✍️ 4. 선생님 종합 피드백 설정")
st.info("학생의 특징을 선택하시거나 '직접 입력'을 활용해 보세요.")

# 키워드 사전 정의
positive_keywords = {
    "선택 안 함": "",
    "✍️ 직접 입력하기": "CUSTOM",
    "성실한 수업 참여": "이번 달 학원 수업에 매우 긍정적이고 성실한 태도로 참여하여 모범이 되었습니다.",
    "어휘 암기 우수": "주어진 필수 단어 암기 과제를 매번 성실하게 수행하여 높은 단어 시험 통과율을 보여주고 있습니다.",
    "독해력 향상": "문장 구조를 파악하는 힘이 단단해져 길고 복잡한 지문도 스스로 차분하게 끊어 읽으며 정답률을 높이고 있습니다.",
    "문법 개념 이해도 상승": "까다로운 문법 규칙과 핵심 개념을 정확하게 이해하고 문제 풀이에 잘 적용하고 있습니다.",
    "듣기 집중력 우수": "듣기 평가 시 고도의 집중력을 발휘하여 세부 정보와 핵심 내용을 정확하게 캐치해내는 강점이 있습니다."
}

need_improvement_keywords = {
    "선택 안 함": "",
    "✍️ 직접 입력하기": "CUSTOM",
    "주의력 보완": "다만 듣기나 문제를 풀 때 사소한 실수를 줄이기 위해 끝까지 집중력을 유지하는 연습이 조금 더 필요합니다.",
    "어휘 복습 필요": "다만 누적되는 단어량이 많아지면서 헷갈려하는 경우가 있어, 가정에서도 꾸준한 반복 복습을 독려해 주시면 좋겠습니다.",
    "쓰기 꼼꼼함 요구": "다만 문장을 작성할 때 구두점(마침표 등)이나 대소문자 표기 등 사소한 디테일을 놓치지 않도록 세심한 피드백을 진행하고 있습니다.",
    "적극적인 질문 필요": "다만 모르는 문형이 나왔을 때 조금 더 적극적으로 질문하고 해결하려는 자신감을 가질 수 있도록 지도하겠습니다."
}

col_kw1, col_kw2 = st.columns(2)
pos_text = ""
neg_text = ""

with col_kw1:
    pos_choice = st.selectbox("👍 이번 달 칭찬/강점 키워드 선택", list(positive_keywords.keys()))
    if pos_choice == "✍️ 직접 입력하기":
        custom_pos