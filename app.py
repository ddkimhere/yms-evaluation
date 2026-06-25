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
    logo_html = f'<img src="data:image/jpeg;base64,{encoded_logo}" style="width:75px; height:75px; border-radius:50%; margin-right:15px; border:2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'

# --- [AI 구글 Gemini API 연동 설정] ---
if "GEMINI_API_KEY" in st.secrets:
    raw_key = st.secrets["GEMINI_API_KEY"]
    clean_key = raw_key.strip().replace('"', '').replace("'", "")
    genai.configure(api_key=clean_key)
    ai_available = True
else:
    ai_available = False

# 웹페이지 기본 설정
st.set_page_config(page_title="YMS English Monthly Test", layout="centered")

st.title("📝 YMS English Monthly Test 생성기")
st.caption("구형 인프라 호환성 검증을 전면 통과한 실시간 AI 문장 창작 버전입니다.")
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

# 4. 실시간 AI 생각 가동망 구축 (구형 인프라 전용 완벽 대응 패치 🛠️)
st.subheader("✍️ 4. AI 명품 종합 의견 생성")
if not ai_available:
    st.error("⚠️ Streamlit 설정창에 GEMINI_API_KEY가 등록되지 않았습니다. 기본 양식으로 작동합니다.")
    teacher_feedback = st.text_area("종합 의견 입력", value="학습 전반에 걸쳐 좋은 성취를 보였습니다.")
else:
    st.success("🤖 구글 제미나이 AI 실시간 창작망이 활성화되었습니다.")
    
    custom_pos = st.text_input("👍 이번 달 학생의 칭찬/강점 키워드 입력", value="문법 점수가 많이 오름")
    custom_neg = st.text_input("🌱 이번 달 학생의 보완/노력 키워드 입력", value="수업 집중도 주춤함")
    
    if st.button("🤖 AI에게 실시간 5문장 창작 추천받기", type="secondary"):
        with st.spinner("AI가 단어들을 연결하여 정교한 5문장 코멘트를 지어내고 있습니다..."):
            try:
                # [핵심 변경] v1beta 서버망이 유일하게 인식하는 정식 구형 모델 경로로 최종 고정
                model = genai.GenerativeModel('models/gemini-pro')
                
                prompt = f"""
                너는 프리미엄 영어 학원인 'YMS 영어학원'의 전문적이고 따뜻한 원장 선생님이야.
                아래 정보를 바탕으로 학부모님께 보낼 '월말 성취도 리포트 종합 의견'을 완벽한 한글 문맥으로 창작해줘.

                [학생 정보]
                - 이름: {student_name}
                - 평가월: {evaluation_month}
                - 이번 달 칭찬 키워드: {custom_pos}
                - 이번 달 보완 키워드: {custom_neg}

                [작성 조건 - 절대로 위배하지 말 것]
                1. 전체 글은 정확히 '5문장'의 짧고 깔끔한 줄글 형태로만 생성해줘. 문단 구분이나 (1), (2) 같은 숫자는 절대 포함하지마.
                2. 원장님이 단편적으로 입력한 키워드들이 기계적으로 문장에 꽂힌 느낌이 들지 않게 해줘. 예컨대 '문법 점수가 많이 오름'을 입력했다면 '문법 점수가 대폭 상승하는 뜻깊은 결과를 거두었으며'와 같이 완벽한 어미/조사 처리를 거쳐 문맥에 녹여내야 해.
                3. "안녕하세요 항상 지지해주셔서 감사합니다", "앞으로 영어 흥미를 잃지 않게" 같은 고정된 오프닝/클로징 상투어구는 절대 쓰지마. 대신 이번 달 학생의 칭찬 키워드 테마(성적 상승, 수업 태도 등)에 어울리는 새로운 도입문과 원장으로서의 새로운 다짐 문장을 즉석에서 창작해줘.
                4. 정중하고 따뜻한 어조 (~합니다 체)를 쓰고, 이모티콘은 1~2개만 자연스럽게 매칭해줘.
                """
                response = model.generate_content(prompt)
                st.session_state["ai_comment"] = response.text
            except Exception as e:
                st.error(f"AI 호출 중 오류가 발생했습니다: {e}")

    default_text = st.session_state.get("ai_comment", "위의 버튼을 누르면 진짜 AI가 문장을 자동으로 창작해 줍니다.")
    teacher_feedback = st.text_area("📋 최종 완성된 코멘트 (마우스로 언제든 직접 편집 가능)", value=default_text, height=180)

st.markdown("---")

# 5. 결과지 출력 및 이미지 다운로드
if st.button("✨ 월말평가 결과지 생성하기", type="primary"):
    if not selected_subjects:
        st.error("평가 영역이 선택되지 않았습니다.")
    else:
        st.subheader("📋 5. 생성된 결과지 확인 및 이미지 저장")
        
        df_html_rows = ""
        for i, subj in enumerate(selected_subjects):
            diff = current_scores[i] - past_scores[i]
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            diff_color = "#2e7d32" if diff >= 0 else "#c62828"
            df_html_rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background-color: #fafafa; font-family: sans-serif;">{subj}</td>
                <td style="padding: 10px; border: 1px solid #ddd; font-family: sans-serif;">{past_scores[i]}점</td>
                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #4A90E2; font-family: sans-serif;">{current_scores[i]}점</td>
                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: {diff_color}; font-family: sans-serif;">{diff_str}</td>
            </tr>
            """

        fig_width = max(5, len(selected_subjects) * 1.5)
        fig, ax = plt.subplots(figsize=(fig_width, 3.5))
        x_indices = range(len(selected_subjects))
        bar_width = 0.35
        rects1 = ax.bar([x - bar_width/2 for x in x_indices], past_scores, bar_width, label='지난달', color='#A0C4FF')
        rects2 = ax.bar([x + bar_width/2 for x in x_indices], current_scores, bar_width, label='이번달', color='#FFADAD')
        ax.set_ylabel('점수 (점)')
        ax.set_title(f'{student_name} 학생의 영역별 성적 비교', fontsize=12, fontweight='bold', pad=10)
        ax.set_xticks(x_indices)
        short_labels = [s.split()[0] for s in selected_subjects]
        ax.set_xticklabels(short_labels, fontsize=9)
        ax.set_ylim(0, 110)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        html_layout = f"""
        <script src="
