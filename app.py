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
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ai_available = True
else:
    ai_available = False

# 웹페이지 기본 설정
st.set_page_config(page_title="YMS English Monthly Test", layout="centered")

st.title("📝 YMS English Monthly Test 생성기")
st.caption("v1beta 서버 환경 맞춤형 AI 명품 코멘트 자동 생성 정식 버전입니다.")
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

# 4. 스마트 AI 피드백 문장 생성기 (v1beta 완벽 호환 세팅)
st.subheader("✍️ 4. AI 명품 종합 의견 생성")
if not ai_available:
    st.error("⚠️ Streamlit 설정창에 GEMINI_API_KEY가 등록되지 않았습니다. 기본 양식으로 작동합니다.")
    teacher_feedback = st.text_area("종합 의견 입력", value="학습 전반에 걸쳐 좋은 성취를 보였습니다.")
else:
    st.success("🤖 AI 자동 문장 생성 엔진이 정상 가동 중입니다.")
    
    custom_pos = st.text_input("👍 이번 달 학생의 칭찬/강점 키워드 입력", value="to부정사 동명사 파트 어려운데 이해 잘함")
    custom_neg = st.text_input("🌱 이번 달 학생의 보완/노력 키워드 입력", value="과제 성실도 떨어짐")
    
    if st.button("🤖 AI에게 5~10문장 명품 의견 추천받기", type="secondary"):
        with st.spinner("AI가 학부모님용 명품 피드백을 정성스럽게 작성하고 있습니다..."):
            try:
                # [수정포인트 🛠️] v1beta API 버전 환경에서 완벽히 연동되는 고유 모델명 선언
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                prompt = f"""
                너는 프리미엄 영어 학원인 'YMS 영어학원'의 전문적이고 따뜻한 원장 선생님이야.
                아래 정보를 바탕으로 학부모님께 카카오톡으로 보낼 '월말 성취도 평가 종합 의견'을 정중하고 신뢰감 넘치는 어조(~합니다 체)로 작성해줘.

                [학생 정보]
                - 이름: {student_name}
                - 과정: {school_type} {student_level}
                - 이번 달 칭찬 및 강점: {custom_pos}
                - 이번 달 보완 및 노력할 점: {custom_neg}

                [작성 조건 - 반드시 지킬 것]
                1. 전체 문장 개수는 반드시 '5문장 이상, 10문장 이하'로 제한해줘.
                2. 인사말로 시작하고, 칭찬 키워드와 보완 키워드를 아주 자연스럽고 매끄러운 교육 전문가적 문장으로 살을 붙여서 풀어 써줘. (절대 조사나 단어가 꼬여서 어색하게 조립된 느낌이 들면 안 됨)
                3. 마지막은 "앞으로도 {student_name} 학생이 영어에 흥미를 잃지 않고 꾸준히 성장할 수 있도록 YMS 학원에서 늘 아낌없이 격려하고 밀착 지도하겠습니다."라는 취지의 따뜻한 다짐으로 마무리해줘.
                4. 이모티콘은 적절히 1~2개만 섞어서 친근하게 작성해줘.
                """
                # v1beta 버전에 맞춰 명시적인 콘텐츠 생성 호출
                response = model.generate_content(prompt)
                st.session_state["ai_comment"] = response.text
            except Exception as e:
                st.error(f"AI 호출 중 오류가 발생했습니다: {e}")

    default_text = st.session_state.get("ai_comment", "위의 버튼을 누르면 AI가 문장을 자동으로 완성해 줍니다.")
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
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <div style="margin-bottom: 20px;">
            <button onclick="takeScreenshot()" style="background-color: #4A90E2; color: white; border: none; padding: 12px 24px; font-size: 15px; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.15); font-family: sans-serif;">
                📸 카톡 전송용 결과지 이미지(PNG) 다운로드하기
            </button>
        </div>
        <div id="capture-area" style="padding: 25px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; font-family: sans-serif; color: #333333;">
            <div style="background-color:#4A90E2; padding:15px; border-radius:10px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                {logo_html}
                <div style="text-align: left;">
                    <h1 style="color:white; margin:0; font-size: 26px; font-family: sans-serif; font-weight: bold; letter-spacing: 0.5px;">YMS English Monthly Test</h1>
                    <p style="color:white; margin:4px 0 0 0; font-size: 14px; font-family: sans-serif; opacity: 0.9;">{school_type} 학업 성취도 리포트</p>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px; font-family: sans-serif;">
                <div><b>이름:</b> {student_name} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>과정/학년:</b> {student_level}</div>
                <div><b>평가월:</b> {evaluation_month}</div>
            </div>
            <div style="font-size: 14px; margin-bottom: 20px; font-family: sans-serif;"><b>현재 사용 교재:</b> {current_book}</div>
            <hr style="border: 0; border-top: 1px solid #eeeeee; margin-bottom: 20px;">
            <h3 style="margin-top: 0; font-size: 16px; color: #111; font-family: sans-serif;">📈 영역별 성취 레벨</h3>
            <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; margin-bottom: 25px; font-family: sans-serif;">
                <thead>
                    <tr style="background-color: #f2f2f2; font-weight: bold; border-top: 2px solid #4A90E2; border-bottom: 1px solid #ddd;">
                        <td style="padding: 10px; border: 1px solid #ddd;">평가 영역</td>
                        <td style="padding: 10px; border: 1px solid #ddd;">지난달 점수</td>
                        <td style="padding: 10px; border: 1px solid #ddd;">이번달 점수</td>
                        <td style="padding: 10px; border: 1px solid #ddd;">변화량</td>
                    </tr>
                </thead>
                <tbody>{df_html_rows}</tbody>
            </table>
            <h3 style="font-size: 16px; color: #111; margin-bottom: 10px; font-family: sans-serif;">📊 지난달 대비 성적 추이</h3>
            <div style="text-align: center; margin-bottom: 25px;">
                <img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: auto;" />
            </div>
            <hr style="border: 0; border-top: 1px solid #eeeeee; margin-bottom: 20px;">
            <h3 style="font-size: 16px; color: #111; margin-bottom: 10px; font-family: sans-serif;">💌 선생님 종합 의견</h3>
            <div style="background-color: #e8f4fd; border-left: 5px solid #4A90E2; padding: 15px; border-radius: 4px; font-size: 13px; line-height: 1.6; text-align: left; font-family: sans-serif; color: #2b5797;">
                {teacher_feedback.replace('\n', '<br>')}
            </div>
        </div>
        <script>
        function takeScreenshot() {{
            const element = document.getElementById("capture-area");
            html2canvas(element, {{ scale: 2, useCORS: true }}).then(canvas => {{
                const link = document.createElement('a');
                link.download = "{evaluation_month}_{student_name}_Monthly_Test.png";
                link.href = canvas.toDataURL('image/png');
                link.click();
            }});
        }}
        </script>
        """
        components.html(html_layout, height=970, scrolling=True)