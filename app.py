import streamlit as st
import pandas as pd

# 1. 와이드 레이아웃 설정 (왼쪽 입력 / 오른쪽 출력 배치를 위함)
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 군더더기 없는 깔끔한 스타일 CSS
st.markdown("""
<style>
    .metric-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-title {
        font-size: 14px;
        color: #475569;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-val {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# 2. 함수 정의 (파스칼의 원리 계산)
def caculate_p(area1, area2, force1):
    pressure = force1 / area1
    force2 = pressure * area2
    ratio = area2 / area1
    return pressure, force2, ratio

st.title("⚙️ 유압 압력장치 힘 계산 및 비교 프로그램")
st.divider()

# 3. 화면 분할: 왼쪽(입력) vs 오른쪽(출력)
left_col, right_col = st.columns([1, 1.3], gap="large")

# [왼쪽 칼럼: 입력 영역]
with left_col:
    st.subheader("1️⃣ 입력 설정")
    with st.container(border=True):
        area1 = st.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
        area2 = st.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
        st.write("")
        force1 = st.slider("작은 피스톤에 가하는 힘 F₁ (N)", min_value=1, max_value=100, value=30, step=1)
        st.write("")
        run_btn = st.button("결과 도출하기", type="primary", use_container_width=True)

# 버튼 누르기 전에도 기본값으로 화면이 보이도록 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# [오른쪽 칼럼: 피스톤 시각화 + 결과 수치 + 비교표]
with right_col:
    st.subheader("2️⃣ 작동 시뮬레이션 및 결과")
    
    # 힘(force1)에 따른 피스톤 이동 거리 계산 (최대 100N 기준 최대 35px 이동)
    # 작은 피스톤은 아래로(+), 큰 피스톤은 위로(-) 이동
    shift_left = (force1 / 100) * 35
    # 부피 보존에 따라 큰 피스톤은 면적 비례만큼 덜 올라가되, 시각적 효과를 위해 적절히 스케일링
    shift_right = min((force1 / 100) * 35, 35)

    piston1_y = 65 + shift_left       # 작은 피스톤 Y좌표 (아래로 내려감)
    piston2_y = 105 - shift_right     # 큰 피스톤 Y좌표 (위로 올라감)

    # 동적 SVG 피스톤 일러스트 (단색 위주의 깔끔한 설계도 스타일)
    piston_svg = f"""
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 15px; display: flex; justify-content: center; margin-bottom: 15px;">
    <svg width="520" height="260" viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg">
      <!-- 실린더 외벽 -->
      <path d="M 80 50 L 80 230 L 440 230 L 440 50" fill="none" stroke="#334155" stroke-width="3"/>
      <path d="M 160 50 L 160 175 L 280 175 L 280 50" fill="none" stroke="#334155" stroke-width="3"/>

      <!-- 유압유 (피스톤 위치에 맞춰 실시간 높이 변화) -->
      <path d="M 81.5 {piston1_y + 18} L 158.5 {piston1_y + 18} L 158.5 176.5 L 281.5 176.5 L 281.5 {piston2_y + 18} L 438.5 {piston2_y + 18} L 438.5 228.5 L 81.5 228.5 Z" fill="#bae6fd"/>

      <!-- [왼쪽] 작은 피스톤 및 막대 -->
      <rect x="81.5" y="{piston1_y}" width="77" height="18" fill="#475569"/>
      <rect x="114" y="{piston1_y - 35}" width="12" height="35" fill="#64748b"/>
      
      <!-- [왼쪽] 누르는 힘 화살표 (아래 방향) 및 수치 -->
      <line x1="120" y1="{piston1_y - 62}" x2="120" y2="{piston1_y - 40}" stroke="#dc2626" stroke-width="3.5"/>
      <polygon points="113,{piston1_y - 43} 127,{piston1_y - 43} 120,{piston1_y - 34}" fill="#dc2626"/>
      <text x="120" y="{piston1_y - 68}" font-size="13" font-weight="bold" text-anchor="middle" fill="#dc2626">↓ 누르는 힘: {force1} N</text>
      <text x="120" y="{piston1_y + 36}" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₁ ({area1}cm²)</text>

      <!-- [오른쪽] 큰 피스톤 및 막대 -->
      <rect x="281.5" y="{piston2_y}" width="157" height="18" fill="#475569"/>
      <rect x="352" y="{piston2_y - 35}" width="16" height="35" fill="#64748b"/>

      <!-- [오른쪽] 나오는 힘 화살표 (위 방향) 및 수치 -->
      <line x1="360" y1="{piston2_y - 38}" x2="360" y2="{piston2_y - 60}" stroke="#059669" stroke-width="3.5"/>
      <polygon points="353,{piston2_y - 57} 367,{piston2_y - 57} 360,{piston2_y - 66}" fill="#059669"/>
      <text x="360" y="{piston2_y - 72}" font-size="13" font-weight="bold" text-anchor="middle" fill="#059669">↑ 출력 힘: {force2:.1f} N</text>
      <text x="360" y="{piston2_y + 36}" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₂ ({area2}cm²)</text>

      <!-- 하단 유체 압력 전달 표기 -->
      <text x="260" y="208" font-size="13" font-weight="bold" text-anchor="middle" fill="#0c4a6e">유압 전달 압력 P = {pressure:.2f} N/cm² →</text>
    </svg>
    </div>
    """
    st.markdown(piston_svg, unsafe_allow_html=True)

    # 4. 결과 요약 박스 3개
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><div class="metric-title">전달 압력 (P)</div><div class="metric-val">{pressure:.2f} N/cm²</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><div class="metric-title">큰 피스톤 출력 (F₂)</div><div class="metric-val">{force2:.2f} N</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><div class="metric-title">힘 증가 배수</div><div class="metric-val">{ratio:.2f} 배</div></div>', unsafe_allow_html=True)

    st.write("")

    # 5. 조건문(if-elif-else)을 활용한 배수 판별
    if ratio >= 10:
        st.success(f"**[10배 이상]** 힘이 **{ratio:.2f}배** 증폭되었습니다.")
    elif ratio >= 5:
        st.info(f"**[5배 이상]** 힘이 **{ratio:.2f}배** 증폭되었습니다.")
    else:
        st.warning(f"**[5배 미만]** 힘이 **{ratio:.2f}배** 증가했습니다.")

    # 6. 리스트(p_force)와 반복문(for)을 활용한 결과 비교표
    st.markdown("#### 📋 기준 힘(10~50N) 적용 시 출력 비교표")
    p_force = [10, 20, 30, 40, 50]
    table_data = []

    for f in p_force:
        p_val, f2_val, r_val = caculate_p(area1, area2, f)
        table_data.append({
            "가하는 힘 F₁ (↓)": f"{f} N",
            "전달 압력 P": f"{p_val:.2f} N/cm²",
            "출력 힘 F₂ (↑)": f"{f2_val:.2f} N",
            "힘 증가 비율": f"{r_val:.2f} 배"
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
