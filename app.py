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

# 웹페이지 기본 설정
st.set_page_config(page_title="YMS 부송관 초등부 월말평가 결과지", layout="centered")

st.title("📝 초등부 월말평가 결과지 생성기")
st.caption("시험 본 영역을 선택하고 성적을 입력하면 맞춤형 웹 리포트를 생성합니다.")
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

# --- [수정 포인트] 영역 선택 체크박스 추가 ---
st.subheader("🎯 2. 이번 달 평가 영역 선택")
st.info("다섯 가지 영역 중 이번 달에 시험을 치른 영역을 모두 체크해 주세요.")

all_subjects = ["어휘 (Vocabulary)", "독해 (Reading)", "쓰기 (Writing)", "문법 (Grammar)", "듣기 (Listening)"]

# 화면에 체크박스를 가로로 예쁘게 배치
selected_subjects = []
cols = st.columns(5)
for idx, subj_name in enumerate(all_subjects):
    with cols[idx]:
        # 기본값으로 어휘, 독해, 듣기 정도만 체크되어 있게 설정
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
    # 선택된 영역만 반복문을 돌며 입력창 생성
    for subj in selected_subjects:
        col_subj1, col_subj2 = st.columns(2)
        with col_subj1:
            past = st.number_input(f"[{subj}] 지난달 점수", min_value=0, max_value=100, value=80, key=f"past_{subj}")
            past_scores.append(past)
        with col_subj2:
            curr = st.number_input(f"[{subj}] 이번달 점수", min_value=0, max_value=100, value=90, key=f"curr_{subj}")
            current_scores.append(curr)

st.markdown("---")

# 4. 종합 피드백 입력
st.subheader("✍️ 4. 선생님 종합 피드백")
teacher_feedback = st.text_area(
    "학부모님께 보낼 피드백을 적어주세요.", 
    value="이번 달에는 선택하신 영역 중 단어와 독해 영역에서 눈에 띄는 성장이 있었습니다! 학원에서 늘 밝은 모습으로 열심히 참여하는 멋진 학생입니다."
)

st.markdown("---")

# 5. 결과지 출력 버튼 및 로직
if st.button("✨ 월말평가 결과지 생성하기", type="primary"):
    if not selected_subjects:
        st.error("평가 영역이 선택되지 않아 결과지를 생성할 수 없습니다.")
    else:
        st.subheader("📋 5. 생성된 결과지 확인 및 이미지 저장")
        st.success("아래 파란색 버튼을 누르면 결과지 영역만 깔끔하게 이미지(PNG) 파일로 다운로드됩니다.")
        
        # --- 선택된 데이터로만 HTML 표 행 생성 ---
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

        # --- 선택된 영역의 수에 맞게 그래프 동적 생성 ---
        # 영역 개수에 따라 그래프 너비를 유연하게 조절 (1개일 때 너무 뚱뚱해지지 않게)
        fig_width = max(5, len(selected_subjects) * 1.5)
        fig, ax = plt.subplots(figsize=(fig_width, 3.5))
        x_indices = range(len(selected_subjects))
        bar_width = 0.35
        
        rects1 = ax.bar([x - bar_width/2 for x in x_indices], past_scores, bar_width, label='지난달', color='#A0C4FF')
        rects2 = ax.bar([x + bar_width/2 for x in x_indices], current_scores, bar_width, label='이번달', color='#FFADAD')
        
        ax.set_ylabel('점수 (점)')
        ax.set_title(f'{student_name} 학생의 영역별 성적 비교', fontsize=12, fontweight='bold', pad=10)
        ax.set_xticks(x_indices)
        # 긴 이름 대신 '어휘', '독해' 등 앞글자만 따서 깔끔하게 그래프 축에 노출
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