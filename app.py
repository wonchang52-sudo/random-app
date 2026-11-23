import streamlit as st
import pandas as pd

# 1. 와이드 레이아웃 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 깔끔하고 선명한 고대비 CSS
st.markdown("""
<style>
.metric-card {
    background-color: #ffffff;
    border: 2px solid #cbd5e1;
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
    if area1 <= 0:
        area1 = 1.0
    pressure = force1 / area1
    force2 = pressure * area2
    ratio = area2 / area1
    return pressure, force2, ratio

# 3. 왼쪽 사이드바: 입력 설정
with st.sidebar:
    st.header("1️⃣ 입력 설정")
    st.markdown("피스톤 면적과 힘을 조절하세요.")
    st.divider()
    
    area1 = st.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
    area2 = st.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
    
    st.write("")
    force1 = st.slider("작은 피스톤에 가하는 힘 F₁ (N)", min_value=1, max_value=100, value=40, step=1)
    
    st.write("")
    run_btn = st.button("결과 도출하기", type="primary")

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 4. 메인 화면
st.title("⚙️ 유압 압력장치 힘 계산 및 비교 프로그램")

top_left, top_right = st.columns([1.4, 1])

with top_left:
    st.subheader("📐 실시간 피스톤 작동 모습")
    
    # 힘(force1)에 따른 피스톤 이동 거리 계산
    # 작은 피스톤(왼쪽)은 최대 55px 아래로 내려감
    shift1 = (force1 / 100.0) * 55.0
    
    # 큰 피스톤(오른쪽)은 면적 비율(부피 보존)에 따라 올라가되, 시각적으로 움직임이 잘 보이도록 보정
    raw_shift2 = shift1 * (area1 / area2)
    shift2 = max(min(raw_shift2 * 2.5, 45.0), (force1 / 100.0) * 12.0)

    # 기준 Y좌표 (위쪽 여백을 넉넉히 두어 텍스트가 절대 겹치지 않음)
    base_y1 = 115.0
    base_y2 = 155.0
    
    piston1_y = base_y1 + shift1   # 아래로 내려감
    piston2_y = base_y2 - shift2   # 위로 올라감

    # 깔끔하고 정돈된 기계 도면 스타일 SVG
    piston_svg = f"""
<div style="background-color: #ffffff; border: 2px solid #cbd5e1; border-radius: 10px; padding: 12px; text-align: center;">
<svg width="100%" height="340" viewBox="0 0 640 340" xmlns="http://www.w3.org/2000/svg">
<style>
.smooth-move {{
  transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
}}
</style>

<!-- [고정 텍스트] 왼쪽 피스톤 옆에 가만히 있는 면적 설명 -->
<text x="125" y="185" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="end" fill="#334155">작은 피스톤</text>
<text x="125" y="205" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="end" fill="#0284c7">면적 A₁ = {area1} cm²</text>
<line x1="132" y1="192" x2="148" y2="192" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>

<!-- [고정 텍스트] 오른쪽 피스톤 옆에 가만히 있는 면적 설명 -->
<text x="515" y="185" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="start" fill="#334155">큰 피스톤</text>
<text x="515" y="205" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="start" fill="#0284c7">면적 A₂ = {area2} cm²</text>
<line x1="492" y1="192" x2="508" y2="192" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>

<!-- 실린더 외벽 (고정) -->
<path d="M 150 95 L 150 285 L 490 285 L 490 95" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 230 95 L 230 225 L 330 225 L 330 95" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/>

<!-- 유압유 (피스톤 움직임에 맞춰 높이 변화) -->
<path class="smooth-move" d="M 151.8 {piston1_y + 18} L 228.2 {piston1_y + 18} L 228.2 226.8 L 331.8 226.8 L 331.8 {piston2_y + 18} L 488.2 {piston2_y + 18} L 488.2 283.2 L 151.8 283.2 Z" fill="#dbeafe"/>

<!-- [움직이는 그룹 1] 작은 피스톤 + 누르는 힘 화살표 + 힘 텍스트 -->
<g class="smooth-move">
  <!-- 피스톤 헤드 및 로드 -->
  <rect x="151.8" y="{piston1_y}" width="76.4" height="18" rx="2" fill="#334155"/>
  <rect x="184" y="{piston1_y - 30}" width="12" height="30" fill="#64748b"/>
  <!-- 아래로 누르는 화살표 -->
  <line x1="190" y1="{piston1_y - 62}" x2="190" y2="{piston1_y - 38}" stroke="#dc2626" stroke-width="4" stroke-linecap="round"/>
  <polygon points="183,{piston1_y - 42} 197,{piston1_y - 42} 190,{piston1_y - 31}" fill="#dc2626"/>
  <!-- 피스톤을 따라 움직이는 힘 텍스트 -->
  <text x="190" y="{piston1_y - 70}" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#dc2626">↓ 누르는 힘 {force1} N</text>
</g>

<!-- [움직이는 그룹 2] 큰 피스톤 + 출력 힘 화살표 + 힘 텍스트 -->
<g class="smooth-move">
  <!-- 피스톤 헤드 및 로드 -->
  <rect x="331.8" y="{piston2_y}" width="156.4" height="18" rx="2" fill="#334155"/>
  <rect x="402" y="{piston2_y - 30}" width="16" height="30" fill="#64748b"/>
  <!-- 위로 밀어 올리는 화살표 -->
  <line x1="410" y1="{piston2_y - 35}" x2="410" y2="{piston2_y - 60}" stroke="#059669" stroke-width="4" stroke-linecap="round"/>
  <polygon points="403,{piston2_y - 55} 417,{piston2_y - 55} 410,{piston2_y - 67}" fill="#059669"/>
  <!-- 피스톤을 따라 움직이는 힘 텍스트 -->
  <text x="410" y="{piston2_y - 75}" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#059669">↑ 출력 힘 {force2:.1f} N</text>
</g>

<!-- 하단 유체 압력 표기 (고정) -->
<text x="320" y="260" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#1e40af">유압 전달 압력 P = {pressure:.2f} N/cm²</text>
</svg>
</div>
"""
    st.markdown(piston_svg, unsafe_allow_html=True)

with top_right:
    st.subheader("📊 계산 결과 요약")
    
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

# 6. 하단: 리스트(p_force)와 반복문(for)을 활용한 표
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
st.table(df)
