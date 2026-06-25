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
    # 인터넷 서버에 폰트 폴더 생성
    font_dir = "fonts"
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    font_path = os.path.join(font_dir, "NanumGothic.ttf")
    
    # 나눔고딕 폰트 파일이 없으면 인터넷에서 다운로드
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        try:
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            pass
            
    # matplotlib에 다운로드한 한글 폰트 등록
    if os.path.exists(font_path):
        import matplotlib.font_manager as fm
        fm.fontManager.addfont(font_path)
        prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=prop.get_name())
    else:
        plt.rc('font', family='sans-serif')
        
    matplotlib.rcParams['axes.unicode_minus'] = False

# 폰트 로드 함수 실행
load_korean_font()

# 웹페이지 기본 설정
st.set_page_config(page_title="YMS 부송관 초등부 월말평가 결과지", layout="centered")

st.title("📝 초등부 월말평가 결과지 생성기")
st.caption("학생의 성적을 입력하면 깔끔한 웹 리포트와 그래프를 생성합니다.")
st.markdown("---")

# 1. 학생 기본 정보 입력
st.subheader("👤 1. 학생 기본 정보")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("학생 이름", value="김초등")
    evaluation_month = st.selectbox("평가월", ["6월", "7월", "8월", "9월", "10월", "11월", "12월"])
with col2:
    current_book = st.text_input("현재 교재", value="English Stars Level 2")
    student_level = st.text_input("레벨 (학년)", value="초등 4학년")

st.markdown("---")

# 2. 영역별 성적 입력 (지난달 vs 이번달 비교용)
st.subheader("📊 2. 영역별 성적 입력 (100점 만점)")
st.info("지난달 점수와 이번달 점수를 비교하여 성장 그래프를 그립니다.")

subjects = ["단어 (Vocabulary)", "독해 (Reading)", "듣기 (Listening)", "말하기/쓰기 (Output)"]
past_scores = []
current_scores = []

# 입력 폼을 그리드로 배치
for subj in subjects:
    col_subj1, col_subj2 = st.columns(2)
    with col_subj1:
        past = st.number_input(f"[{subj}] 지난달 점수", min_value=0, max_value=100, value=80, key=f"past_{subj}")
        past_scores.append(past)
    with col_subj2:
        curr = st.number_input(f"[{subj}] 이번달 점수", min_value=0, max_value=100, value=90, key=f"curr_{subj}")
        current_scores.append(curr)

st.markdown("---")

# 3. 종합 피드백 입력
st.subheader("✍️ 3. 선생님 종합 피드백")
teacher_feedback = st.text_area(
    "학부모님께 보낼 피드백을 적어주세요.", 
    value="이번 달에는 단어 영역에서 눈에 띄는 성장이 있었습니다! 독해할 때 문장 구조를 파악하는 힘도 좋아졌으나, 듣기 평가 시 집중력을 조금 더 유지하면 다음 달에는 더욱 좋은 결과가 있을 것 같습니다. 학원에서 늘 밝은 모습으로 열심히 참여하는 멋진 학생입니다."
)

st.markdown("---")

# 4. 결과지 출력 버튼 및 로직
if st.button("✨ 월말평가 결과지 생성하기", type="primary"):
    
    st.subheader("📋 4. 생성된 결과지 확인 및 이미지 저장")
    st.success("아래 파란색 버튼을 누르면 결과지 영역만 깔끔하게 이미지(PNG) 파일로 다운로드됩니다.")
    
    # --- 데이터 처리 및 표 전송용 HTML 생성 ---
    df_html_rows = ""
    for i, subj in enumerate(subjects):
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

    # --- matplotlib 그래프 생성 및 이미지 주입 처리 ---
    fig, ax = plt.subplots(figsize=(7, 3.5))
    x_indices = range(len(subjects))
    bar_width = 0.35
    
    rects1 = ax.bar([x - bar_width/2 for x in x_indices], past_scores, bar_width, label='지난달', color='#A0C4FF')
    rects2 = ax.bar([x + bar_width/2 for x in x_indices], current_scores, bar_width, label='이번달', color='#FFADAD')
    
    ax.set_ylabel('점수 (점)')
    ax.set_title(f'{student_name} 학생의 영역별 성적 비교', fontsize=12, fontweight='bold', pad=10)
    ax.set_xticks(x_indices)
    ax.set_xticklabels(subjects, fontsize=9)
    ax.set_ylim(0, 110)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    plt.tight_layout()

    # 메모리에 그래프 이미지 임시 보관
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # --- HTML 템플릿의 폰트 설정을 시스템 기본 고딕(sans-serif)으로 강제 적용 ---
    html_layout = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <div style="margin-bottom: 20px;">
        <button onclick="takeScreenshot()" style="background-color: #4A90E2; color: white; border: none; padding: 12px 24px; font-size: 15px; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.15); font-family: sans-serif;">
            📸 카톡 전송용 결과지 이미지(PNG) 다운로드하기
        </button>
    </div>

    <div id="capture-area" style="padding: 25px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; font-family: sans-serif; color: #333333;">
        
        <div style="background-color:#4A90E2; padding:15px; border-radius:10px; text-align:center; margin-bottom: 20px;">
            <h1 style="color:white; margin:0; font-size: 24px; font-family: sans-serif; font-weight: bold;">YMS 부송관 월말 성취도 평가</h1>
            <p style="color:white; margin:5px 0 0 0; font-size: 14px; font-family: sans-serif;">초등부 학업 성취도 리포트</p>
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
            link.download = "{evaluation_month}_{student_name}_월말평가.png";
            link.href = canvas.toDataURL('image/png');
            link.click();
        }});
    }}
    </script>
    """

    components.html(html_layout, height=950, scrolling=True)