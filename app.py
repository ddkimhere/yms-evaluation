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

# --- [AI 구글 API 연동 설정] ---
if "GEMINI_API_KEY" in st.secrets:
    raw_key = st.secrets["GEMINI_API_KEY"]
    clean_key = raw_key.strip().replace('"', '').replace("'", "")
    genai.configure(api_key=clean_key)
    ai_available = True
else:
    ai_available = False

st.set_page_config(page_title="YMS English Monthly Test", layout="centered")

st.markdown(f"""
    <style>
    div.stButton > button:first-child {{ background-color: {LOGO_COLOR} !important; color: white !important; border-radius: 8px; border: none; padding: 0.6rem 1.8rem; font-weight: 600; }}
    h1, h2, h3 {{ color: {LOGO_COLOR} !important; font-weight: 700; }}
    </style>
""", unsafe_allow_html=True)

st.title("📝 YMS English Monthly Test 생성기")
st.caption("이번 달 성적 집중 분석 버전")
st.markdown("---")

# 1. 학생 기본 정보
st.subheader("👤 1. 학생 기본 정보")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("학생 이름", value="김YMS")
    evaluation_month = st.selectbox("평가월", ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"], index=5)
with col2:
    current_book = st.text_input("현재 교재", value="English Stars Level 2")
    student_level = st.selectbox("학년 선택", ["초등 1학년", "초등 2학년", "초등 3학년", "초등 4학년", "초등 5학년", "초등 6학년", "중등 1학년", "중등 2학년", "중등 3학년"], index=3)

# 2. 영역 선택
st.subheader("🎯 2. 이번 달 평가 영역")
all_subjects = ["어휘 (Vocabulary)", "독해 (Reading)", "쓰기 (Writing)", "문법 (Grammar)", "듣기 (Listening)"]
selected_subjects = st.multiselect("평가 영역을 선택하세요", all_subjects, default=["어휘 (Vocabulary)", "독해 (Reading)", "쓰기 (Writing)"])

# 3. 성적 입력
st.subheader("📊 3. 이번 달 성적 입력")
current_scores = {}
for subj in selected_subjects:
    current_scores[subj] = st.number_input(f"{subj} 점수", min_value=0, max_value=100, value=90)

# 4. AI 의견
st.subheader("✍️ 4. AI 종합 의견 생성")
if ai_available:
    custom_pos = st.text_input("강점 키워드", value="성실한 단어 암기")
    custom_neg = st.text_input("보완 키워드", value="문장 구조 파악 노력 필요")
    if st.button("🤖 AI 의견 생성"):
        model = genai.GenerativeModel('gemini-2.5-flash')
        score_txt = "\n".join([f"- {s}: {current_scores[s]}점" for s in selected_subjects])
        prompt = f"학생 {student_name}의 성적({score_txt})과 강점({custom_pos}), 보완점({custom_neg})을 바탕으로 학부모님께 보낼 5문장 코멘트를 작성해줘. 이모티콘 없이 정중하고 전문적인 어조로 작성해줘."
        st.session_state["ai_comment"] = model.generate_content(prompt).text

teacher_feedback = st.text_area("최종 의견", value=st.session_state.get("ai_comment", ""))

# 5. 결과지 생성
if st.button("✨ 결과지 생성하기"):
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(list(current_scores.keys()), list(current_scores.values()), color=LOGO_COLOR)
    ax.set_ylim(0, 110)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    
    # HTML 테이블
    table_rows = "".join([f"<tr><td style='padding:10px;'>{s}</td><td style='padding:10px; font-weight:bold;'>{current_scores[s]}점</td></tr>" for s in current_scores])
    
    html_layout = f"""
    <div id='capture-area' style='padding:30px; background:white; border:2px solid {LOGO_COLOR}; border-radius:10px;'>
        <h2 style='color:{LOGO_COLOR};'>YMS Monthly Report</h2>
        <p><b>{student_name}</b> 학생의 {evaluation_month} 평가 결과입니다.</p>
        <table style='width:100%; text-align:center;'>
            <tr style='background:{LOGO_LIGHT_BG};'><th>영역</th><th>점수</th></tr>
            {table_rows}
        </table>
        <div style='margin-top:20px;'><img src='data:image/png;base64,{img_base64}' style='width:100%;'/></div>
        <h3 style='margin-top:20px;'>선생님 의견</h3>
        <p style='line-height:1.6;'>{teacher_feedback.replace('\\n', '<br>')}</p>
    </div>
    """
    components.html(html_layout, height=800)
