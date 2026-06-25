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

# 웹페이지 기본 설정
st.set_page_config(page_title="YMS English Monthly Test", layout="centered")

st.title("📝 YMS English Monthly Test 생성기")
st.caption("고성능 자체 문장 자연어 조립 엔진이 탑재되어 지연과 에러 없는 안정적인 버전입니다.")
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

# 4. 고성능 로컬 명품 문장 생성 엔진 (에러율 0% + 자연어 최적화 🛠️)
st.subheader("✍ " + f"4. {student_name} 학생 맞춤형 명품 코멘트 생성")
st.success("✨ 입력하신 단어가 학부모용 고급 문장 스타일로 자동 가공되는 버전입니다.")

custom_pos = st.text_input("👍 이번 달 학생의 칭찬/강점 키워드 입력", value="to부정사 동명사 파트 어려운데 이해 잘함")
custom_neg = st.text_input("🌱 이번 달 학생의 보완/노력 키워드 입력", value="과제 성실도 떨어짐")

if st.button("📝 5~10문장 명품 의견 즉시 완성하기", type="secondary"):
    pos_keyword = custom_pos.strip()
    neg_keyword = custom_neg.strip()
    
    # 조사가 중복되거나 어색하게 꼬이는 현상을 방지하기 위한 스마트 자연어 필터링
    if "파트" in pos_keyword and "학습했는데" not in pos_keyword:
        pos_processed = f"학생들이 대개 까다로워하는 {pos_keyword}을(를) 집중적으로 공부했는데, 핵심 개념을 아주 명쾌하게 파악하고"
    else:
        pos_processed = f"학습 과정 중 '{pos_keyword}' 부분에서 대단히 뛰어난 집중력을 발휘해 주었으며, 관련 개념을 올바르게 파악하고"

    if "과제" in neg_keyword or "숙제" in neg_keyword:
        neg_processed = f"최근 들어 {neg_keyword}는 경향을 다소 보여 학업의 연속성 면에서 약간의 아쉬움이 남습니다. 학원 수업 내용을 완벽히 살로 만들려면 철저한 이행이 필수적인 만큼"
    else:
        neg_processed = f"일상 학습 중 '{neg_keyword}' 측면에서 다소 기복이나 보완이 필요한 타이밍입니다. 배운 내용을 완벽히 본인의 무기로 만들기 위해서는"

    # 군더더기를 걷어내고 딱 좋은 분량(7문장 내외)으로 완성되는 고정 프리미엄 템플릿
    text_blocks = [
        f"안녕하세요, YMS 영어학원입니다. 항상 학원의 교육 방향을 믿고 소중한 자녀를 믿고 맡겨주시는 학부모님께 깊은 감사를 드립니다. 😊\n\n",
        f"이번 {evaluation_month} 학습 과정에서 {student_name} 학생은 기본 영어 역량을 단단히 다지기 위해 대단히 열정적인 모습으로 수업에 임해 주었습니다. ",
        f"{pos_processed} 교재 지문을 막힘없이 분석해 내는 훌륭한 성취 레벨을 보여주었습니다. 어려운 문형 규칙을 스스로 분석해 내는 힘이 크게 성장한 만큼, 이 성과에 대해 아낌없는 칭찬을 꼭 전하고 싶습니다. 👍\n\n",
        f"다만, {neg_processed}, 가정에서도 규칙적인 학습 루틴을 채워나갈 수 있도록 지속적인 격려와 지도 협조를 함께 연계해 주시면 감사하겠습니다. \n\n",
        f"체계적인 흐름을 잘 유지하여 다음 달에는 학업 성취도가 더욱 단단하게 다져질 수 있도록 세심하게 밀착 클리닉과 개별 지도를 진행하겠습니다. ",
        f"앞으로도 {student_name} 학생이 영어에 대한 흥미를 잃지 않고 자신감 있게 대형 성장을 이어갈 수 있도록, 저희 YMS 학원 강사진 일동이 언제나 부모님과 같은 마음으로 밀착 마크하고 정성껏 지도하겠습니다. 감사합니다. 💙"
    ]
    
    st.session_state["local_comment"] = "".join(text_blocks)

default_text = st.session_state.get("local_comment", "위의 버튼을 누르면 원장님의 키워드를 분석해 5~10문장 사이의 명품 완성본 글을 즉시 만들어 줍니다.")
teacher_feedback = st.text_area("📋 최종 완성된 코멘트 (마우스로 언제든 직접 추가 수정 가능)", value=default_text, height=220)

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
