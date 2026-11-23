import streamlit as st
import pandas as pd

# 1. 와이드 레이아웃 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 텍스트가 선명하게 보이도록 고대비 깔끔한 CSS 적용 (다크모드에서도 글씨 깨짐/안보임 방지)
st.markdown("""
<style>
    /* 결과 요약 카드 */
    .metric-card {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-label {
        font-size: 14px;
        color: #475569 !important;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .metric-number {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. 함수 정의 (파스칼의 원리 계산)
def caculate_p(area1, area2, force1):
    pressure = force1 / area1
    force2 = pressure * area2
    ratio = area2 / area1
    return pressure, force2, ratio

# 3. 왼쪽 사이드바로 입력 부분 완전히 분리 (메인 화면 공간 확보)
with st.sidebar:
    st.header("1️⃣ 입력 설정")
    st.markdown("피스톤의 면적과 가하는 힘을 조절하세요.")
    st.divider()
    
    area1 = st.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
    area2 = st.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
    
    st.write("")
    force1 = st.slider("작은 피스톤에 가하는 힘 F₁ (N)", min_value=1, max_value=100, value=30, step=1)
    
    st.write("")
    run_btn = st.button("결과 도출하기", type="primary", use_container_width=True)

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 4. 메인 화면 (오른쪽 넓은 영역 전체 사용)
st.title("⚙️ 유압 압력장치 힘 계산 및 비교 프로그램")

# 상단: 피스톤 시각화 (왼쪽) + 핵심 결과 요약 (오른쪽)
top_left, top_right = st.columns([1.3, 1], gap="large")

with top_left:
    st.subheader("📐 실시간 피스톤 작동 모습")
    
    # 힘(force1)에 따른 피스톤 이동 거리 (작은 피스톤은 아래로, 큰 피스톤은 위로)
    shift = (force1 / 100) * 35
    piston1_y = 85 + shift       # 작은 피스톤 위치 (아래로 이동)
    piston2_y = 125 - shift      # 큰 피스톤 위치 (위로 이동)

    # 글자가 절대 겹치거나 잘리지 않도록 여백과 좌표를 넉넉히 잡은 SVG
    piston_svg = f"""
    <div style="background-color: #ffffff; border: 2px solid #cbd5e1; border-radius: 10px; padding: 10px; text-align: center;">
    <svg width="100%" height="290" viewBox="0 0 540 290" xmlns="http://www.w3.org/2000/svg">
      <!-- 실린더 외벽 -->
      <path d="M 70 70 L 70 255 L 470 255 L 470 70" fill="none" stroke="#1e293b" stroke-width="3"/>
      <path d="M 160 70 L 160 195 L 290 195 L 290 70" fill="none" stroke="#1e293b" stroke-width="3"/>

      <!-- 유압유 (피스톤 움직임에 따라 높이 연동) -->
      <path d="M 71.5 {piston1_y + 18} L 158.5 {piston1_y + 18} L 158.5 196.5 L 291.5 196.5 L 291.5 {piston2_y + 18} L 468.5 {piston2_y + 18} L 468.5 253.5 L 71.5 253.5 Z" fill="#e0f2fe"/>

      <!-- [왼쪽] 작은 피스톤 -->
      <rect x="71.5" y="{piston1_y}" width="87" height="18" fill="#334155"/>
      <rect x="109" y="{piston1_y - 30}" width="12" height="30" fill="#64748b"/>
      
      <!-- [왼쪽] 누르는 힘 방향 및 텍스트 -->
      <line x1="115" y1="{piston1_y - 58}" x2="115" y2="{piston1_y - 36}" stroke="#dc2626" stroke-width="4"/>
      <polygon points="108,{piston1_y - 40} 122,{piston1_y - 40} 115,{piston1_y - 30}" fill="#dc2626"/>
      <text x="115" y="{piston1_y - 66}" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#dc2626">↓ 누르는 힘: {force1} N</text>
      <text x="115" y="{piston1_y + 38}" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₁ ({area1}cm²)</text>

      <!-- [오른쪽] 큰 피스톤 -->
      <rect x="291.5" y="{piston2_y}" width="177" height="18" fill="#334155"/>
      <rect x="372" y="{piston2_y - 30}" width="16" height="30" fill="#64748b"/>

      <!-- [오른쪽] 나오는 힘 방향 및 텍스트 -->
      <line x1="380" y1="{piston2_y - 34}" x2="380" y2="{piston2_y - 56}" stroke="#059669" stroke-width="4"/>
      <polygon points="373,{piston2_y - 52} 387,{piston2_y - 52} 380,{piston2_y - 62}" fill="#059669"/>
      <text x="380" y="{piston2_y - 70}" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#059669">↑ 출력 힘: {force2:.1f} N</text>
      <text x="380" y="{piston2_y + 38}" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₂ ({area2}cm²)</text>

      <!-- 하단 전달 압력 텍스트 -->
      <text x="270" y="232" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#0f172a">전달 압력 P = {pressure:.2f} N/cm² ➔</text>
    </svg>
    </div>
    """
    st.markdown(piston_svg, unsafe_allow_html=True)

with top_right:
    st.subheader("📊 계산 결과 요약")
    
    # 카드 3개를 깔끔하게 배치
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">전달 압력 (P)</div><div class="metric-number">{pressure:.2f} N/cm²</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">힘 증가 배수</div><div class="metric-number">{ratio:.2f} 배</div></div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown(f'<div class="metric-card"><div class="metric-label">큰 피스톤 출력 힘 (F₂)</div><div class="metric-number" style="color:#059669 !important;">{force2:.2f} N</div></div>', unsafe_allow_html=True)
    st.write("")

    # 5. 조건문(if-elif-else)을 활용한 배수 판별
    if ratio >= 10:
        st.success(f"**[10배 이상]** 힘이 **{ratio:.2f}배** 증폭되었습니다.")
    elif ratio >= 5:
        st.info(f"**[5배 이상]** 힘이 **{ratio:.2f}배** 증폭되었습니다.")
    else:
        st.warning(f"**[5배 미만]** 힘이 **{ratio:.2f}배** 증가했습니다.")

st.divider()

# 6. 하단 전체 너비: 리스트(p_force)와 반복문(for)을 활용한 표 (스크롤 없이 한눈에 들어옴)
st.subheader("📋 기준 힘(10N ~ 50N) 적용 시 결과 비교표")
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
