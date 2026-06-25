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
st.caption("안전한 레이아웃과 직접 입력 피드백 시스템이 통합된 버전입니다.")
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

# 4. 선생님 종합 피드백 자동 생성기 (화면 밀림 현상 완벽 방지 레이아웃 🛠️)
st.subheader("✍️ 4. 선생님 종합 피드백 설정")
st.info("학생의 특징을 선택하시거나 '✍️ 직접 입력하기'를 눌러 원하는 키워드를 적어보세요.")

# 키워드 사전 데이터
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

pos_text = ""
neg_text = ""

# 밀림 방지를 위해 칭찬 박스와 입력창을 순차적으로 배치
pos_choice = st.selectbox("👍 이번 달 칭찬/강점 키워드 선택", list(positive_keywords.keys()))
if pos_choice == "✍️ 직접 입력하기":
    custom_pos = st.text_input("💡 칭찬 키워드 직접 입력 (예: 과제 수행 완벽, 발표력 우수)", value="")
    if custom_pos:
        pos_text = f"이번 달 학습 과정에서 {custom_pos}(이)라는 긍정적인 변화와 뛰어난 성취를 보여주어 큰 칭찬을 해주고 싶습니다."
else:
    pos_text = positive_keywords[pos_choice]

st.markdown("") # 안전한 줄바꿈 공백

# 보완 박스 배치
neg_choice = st.selectbox("🌱 이번 달 보완/노력 키워드 선택", list(need_improvement_keywords.keys()))
if neg_choice == "✍️ 직접 입력하기":
    custom_neg = st.text_input("💡 보완 키워드 직접 입력 (예: 오답 노트 정리 필요, 글씨체 교정)", value="")
    if custom_neg:
        neg_text = f"다만 학습 과정에서 {custom_neg}(이)가 다소 아쉬운 부분으로 나타나, 이 점을 채울 수 있도록 세심하게 지도하겠습니다."
else:
    neg_text = need_improvement_keywords[neg_choice]

# 문장 자동 매칭 및 합성
generated_comment = "이번 달 월말 평가 결과 리포트 안내드립니다.\n\n"
if pos_text:
    generated_comment += pos_text + " "
if neg_text:
    generated_comment += neg_text + " "

generated_comment += f"\n\n앞으로도 {student_name} 학생이 영어에 흥미를 잃지 않고 꾸준히 성장할 수 있도록 YMS 학원에서 늘 아낌없이 격려하고 밀착 지도하겠습니다."

st.markdown("")
# 최종 편집창
teacher_feedback = st.text_area("📋 최종 완성된 코멘트 (여기서 추가 자유 수정 가능)", value=generated_comment, height=160)

st.markdown("---")

# 5. 결과지 출력 버튼 및 로직
if st.button("✨ 월말평가 결과지 생성하기", type="primary"):
    if not selected_subjects:
        st.error("평가 영역이 선택되지 않아 결과지를 생성할 수 없습니다.")
    else:
        st.subheader("📋 5. 생성된 결과지 확인 및 이미지 저장")
        st.success("아래 파란색 버튼을 누르면 결과지 영역만 깔끔하게 이미지(PNG) 파일로 다운로드됩니다.")
        
        # --- 데이터 처리 및 표 전송용 HTML 생성 ---
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

        # --- 그래프 동적 생성 ---
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

        # --- HTML 템플릿 출력 ---
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
                <tbody>
                    {df_html_rows}
                </tbody>
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