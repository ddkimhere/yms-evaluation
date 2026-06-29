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
                    score_summary += f"- {subj}: 지난달 {past_scores[idx]}점 -> 이번달 {current_scores[idx]}점\\n"

                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                너는 영어 전문 학원인 'YMS 영어학원'의 전문적이고 따뜻한 원장 선생님이야.
                아래 학생의 영역별 실제 점수 변화 데이터와 원장님이 적어준 키워드를 종합적으로 분석하여, 학부모님께 보낼 '월말 성취도 평가 종합 의견'을 완전히 새로운 줄글로 창작해줘.

                [학생 정보]
                - 이름: {student_name}
                - 평가월: {evaluation_month}
                - 이번 달 칭찬 및 강점 키워드: {custom_pos}
                - 이번 달 보완 및 노력할 점 키워드: {custom_neg}

                [영역별 성적 추이 데이터]
                {score_summary}

                [작성 조건 - 반드시 누락 없이 지킬 것]
                1. 전체 줄글은 처음부터 끝까지 끊김 없이 딱 '5문장'으로만 제한해서 짧고 강렬하게 완성해줘. 문장 중간이나 끝에 (1), (2) 같은 숫자는 절대 포함하지마.
                2. 단순히 점수를 숫자로 나열하지 말고, 네가 점수를 직접 비교해서 '지난달 대비 실력이 부쩍 성장했다'라거나 '상위권 성적을 안정적이고 탄탄하게 유지 중이다'와 같이 교육 전문가의 시선에서 자연스럽게 풀어써줘.
                3. 담임선생님이 입력한 키워드들이 기계적으로 문장에 꽂힌 느낌이 들지 않게 자연스러운 연결 어미를 사용해줘.
                4. "안녕하세요 항상 지지해주셔서 감사합니다", "앞으로 영어 흥미를 잃지 않게 지도하겠습니다" 같은 상투적이고 뻔한 오프닝/클로징 고정 문구는 절대 쓰지마. 대신 이번 성적 흐름과 칭찬 테마에 딱 들어맞는 신선한 도입문과 담임선생님으로서의 새로운 다짐 문장을 즉석에서 창작해줘.
                5. 정중하고 따뜻한 어조 (~합니다 체)를 쓰고, 이모티콘은 넣지마.
                6. YMS영어학원 이란 말 너무 많이 쓰지마.
                7. 문장 너무 길게 쓰지마. 
                """
                response = model.generate_content(prompt)
                st.session_state["ai_comment"] = response.text
            except Exception as e:
                st.error(f"AI 호출 중 오류가 발생했습니다: {e}")

    default_text = st.session_state.get("ai_comment", "위의 버튼을 누르면 점수 추이를 분석한 진짜 AI 코멘트가 자동으로 창작됩니다.")
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
            diff_color = "#1e88e5" if diff > 0 else ("#e53935" if diff < 0 else "#333333")
            df_html_rows += f"""
            <tr style="border-bottom: 1px solid #f1f1f1;">
                <td style="padding: 12px; border-right: 1px solid #f1f1f1; font-weight: bold; background-color: #fbfbfb; font-family: sans-serif; color:#333;">{subj}</td>
                <td style="padding: 12px; border-right: 1px solid #f1f1f1; font-family: sans-serif; color:#666;">{past_scores[i]}점</td>
                <td style="padding: 12px; border-right: 1px solid #f1f1f1; font-weight: bold; color: {LOGO_COLOR}; font-family: sans-serif; font-size:14px;">{current_scores[i]}점</td>
                <td style="padding: 12px; font-weight: bold; color: {diff_color}; font-family: sans-serif;">{diff_str}</td>
            </tr>
            """

        fig_width = max(5, len(selected_subjects) * 1.5)
        fig, ax = plt.subplots(figsize=(fig_width, 3.5))
        x_indices = range(len(selected_subjects))
        bar_width = 0.35
        rects1 = ax.bar([x - bar_width/2 for x in x_indices], past_scores, bar_width, label='지난달', color='#B0C4DE')
        rects2 = ax.bar([x + bar_width/2 for x in x_indices], current_scores, bar_width, label='이번달', color=LOGO_COLOR)
        ax.set_ylabel('점수 (점)')
        ax.set_title(f'{student_name} 학생의 영역별 성적 비교', fontsize=12, fontweight='bold', pad=10, color=LOGO_COLOR)
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

        # html_layout 정의 및 자바스크립트 내 이중 중괄호 처리 안정화 구조 유지
        html_layout = f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js" crossorigin="anonymous"></script>
        <div style="margin-bottom: 25px;">
            <button onclick="takeScreenshot()" style="background-color: {LOGO_COLOR}; color: white; border: none; padding: 14px 24px; font-size: 15px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.15); font-family: sans-serif; transition: all 0.2s;">
                📸 카톡 전송용 결과지 이미지(PNG) 다운로드하기
            </button>
        </div>
        <div id="capture-area" style="padding: 35px; background-color: {LOGO_COLOR}; border-radius: 12px; font-family: 'Malgun Gothic', sans-serif; color: white; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 18px;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 55px; height: 55px; background: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <span style="color: {LOGO_COLOR}; font-weight: 900; font-size: 18px; letter-spacing: -0.5px;">YMS</span>
                    </div>
                    <div style="text-align: left;">
                        <h1 style="color: white !important; margin: 0; font-size: 23px; font-family: sans-serif; font-weight: bold; letter-spacing: 0.5px;">와이엠에스 영어과</h1>
                        <p style="color: rgba(255,255,255,0.6) !important; margin: 2px 0 0 0; font-size: 11px; font-family: sans-serif; font-weight: bold; letter-spacing: 1px;">YMS ENGLISH · 부송관</p>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; font-weight: bold; color: #E5A93C; letter-spacing: 0.5px;">Your Mastery Solution</div>
                    <div style="font-size: 10px; color: rgba(255,255,255,0.7); margin-top: 4px; font-style: italic; font-family: serif;">True learning builds the bridge from effort to excellence.</div>
                </div>
            </div>
            
            <div style="font-size: 28px; font-weight: bold; text-align: left; margin-bottom: 5px; color: white; letter-spacing: 0.5px;">YMS Monthly Test Report</div>
            <div style="font-size: 13px; color: rgba(255,255,255,0.75); text-align: left; margin-bottom: 25px;">2026년 {evaluation_month} 정기 평가</div>
            
            <div style="background: white; border-radius: 8px; padding: 30px; color: #333333; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px; font-size: 14.5px; font-family: sans-serif; background:#f8f9fa; padding:10px 15px; border-radius:6px; color:#444;">
                    <div><b>이름:</b> <span style="color:#111; font-weight:600;">{student_name}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>학년:</b> <span style="color:#111; font-weight:600;">{student_level}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>교재:</b> <span style="color:#111; font-weight:600;">{current_book}</span></div>
                </div>
                <h3 style="margin-top: 25px; font-size: 16px; color: {LOGO_COLOR} !important; font-family: sans-serif; font-weight:700; border-left: 4px solid {LOGO_COLOR}; padding-left: 8px; margin-bottom: 12px;">📈 영역별 성취 레벨</h3>
                <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; margin-bottom: 30px; font-family: sans-serif; border: 1px solid #eaeaea;">
                    <thead>
                        <tr style="background-color: #f8f9fa; font-weight: bold; border-bottom: 1px solid #eaeaea; color:#555;">
                            <td style="padding: 12px; width: 35%;">평가 영역</td>
                            <td style="padding: 12px;">지난달 점수</td>
                            <td style="padding: 12px;">이번달 점수</td>
                            <td style="padding: 12px;">변화량</td>
                        </tr>
                    </thead>
                    <tbody>{df_html_rows}</tbody>
                </table>
                <h3 style="font-size: 16px; color: {LOGO_COLOR} !important; margin-bottom: 15px; font-family: sans-serif; font-weight:700; border-left: 4px solid {LOGO_COLOR}; padding-left: 8px;">📊 지난달 대비 성적 추이</h3>
                <div style="text-align: center; margin-bottom: 30px; background:#fafafa; padding:15px; border-radius:8px; border:1px solid #f1f1f1;">
                    <img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: auto;" />
                </div>
                <h3 style="font-size: 16px; color: {LOGO_COLOR} !important; margin-bottom: 12px; font-family: sans-serif; font-weight:700; border-left: 4px solid {LOGO_COLOR}; padding-left: 8px;">💌 선생님 종합 의견</h3>
                <div style="background-color: {LOGO_LIGHT_BG}; border-left: 5px solid {LOGO_COLOR}; padding: 18px; border-radius: 6px; font-size: 13.5px; line-height: 1.65; text-align: left; font-family: sans-serif; color: #111111;">
                    {teacher_feedback.replace('\\n', '<br>')}
                </div>
            </div>
        </div>
        
        <script>
        function takeScreenshot() {{
            if (typeof html2canvas === 'undefined') {{
                alert("라이브러리를 불러오는 중입니다. 1초 뒤에 다시 눌러주세요!");
                return;
            }}
            
            const element = document.getElementById("capture-area");
            
            html2canvas(element, {{
                scale: 2,
                useCORS: true,
                backgroundColor: null,
                logging: false
            }}).then(canvas => {{
                canvas.toBlob(function(blob) {{
                    const link = document.createElement('a');
                    link.download = "{evaluation_month}_{student_name}_Monthly_Test.png";
                    link.href = URL.createObjectURL(blob);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }}, 'image/png');
            }}).catch(err => {{
                alert("이미지 캡처 중 오류가 발생했습니다.");
            }});
        }}
        </script>
        """
        components.html(html_layout, height=1120, scrolling=True)
