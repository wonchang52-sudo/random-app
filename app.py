import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 고대비 깔끔한 CSS (들여쓰기 없이 작성하여 마크다운 충돌 방지)
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

# 2. 함수 정의 (0으로 나누기 방지 포함)
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

top_left, top_right = st.columns([1.35, 1])

with top_left:
    st.subheader("📐 실시간 피스톤 작동 모습")
    
    # 힘에 따른 피스톤 이동 및 화살표 굵기 계산
    shift = (force1 / 100.0) * 40.0
    piston1_y = 95.0 + shift
    piston2_y = 135.0 - shift
    
    arrow1_width = 3.0 + (force1 / 100.0) * 4.0
    arrow2_width = min(4.0 + (ratio / 15.0) * 5.0, 10.0)
    anim_speed = max(2.2 - (force1 / 100.0) * 1.5, 0.4)

    # SVG 코드 (들여쓰기 제거하여 렌더링 오류 완벽 차단)
    piston_svg = f"""
<div style="background-color: #ffffff; border: 2px solid #cbd5e1; border-radius: 10px; padding: 12px; text-align: center;">
<svg width="100%" height="320" viewBox="0 0 560 320" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes flowRight {{
  0% {{ transform: translateX(-12px); opacity: 0.3; }}
  50% {{ opacity: 1; }}
  100% {{ transform: translateX(12px); opacity: 0.3; }}
}}
@keyframes pulseForce {{
  0%, 100% {{ transform: translateY(0px); }}
  50% {{ transform: translateY(-4px); }}
}}
.fluid-flow {{ animation: flowRight {anim_speed}s infinite ease-in-out; }}
.force-up {{ animation: pulseForce 1s infinite ease-in-out; }}
</style>

<rect x="65" y="10" width="110" height="26" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
<text x="120" y="28" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₁: {area1} cm²</text>

<rect x="325" y="10" width="120" height="26" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
<text x="385" y="28" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₂: {area2} cm²</text>

<path d="M 75 80 L 75 275 L 480 275 L 480 80" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 165 80 L 165 215 L 290 215 L 290 80" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/>

<path d="M 76.8 {piston1_y + 18} L 163.2 {piston1_y + 18} L 163.2 216.8 L 291.8 216.8 L 291.8 {piston2_y + 18} L 478.2 {piston2_y + 18} L 478.2 273.2 L 76.8 273.2 Z" fill="#bae6fd"/>

<g class="fluid-flow">
  <text x="120" y="248" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0284c7">⬇</text>
  <text x="230" y="250" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="#0284c7">➔ ➔ ➔</text>
  <text x="385" y="248" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0284c7">⬆</text>
</g>

<rect x="76.8" y="{piston1_y}" width="86.4" height="18" rx="2" fill="#334155"/>
<rect x="114" y="{piston1_y - 28}" width="12" height="28" fill="#64748b"/>

<line x1="120" y1="{piston1_y - 54}" x2="120" y2="{piston1_y - 34}" stroke="#dc2626" stroke-width="{arrow1_width}" stroke-linecap="round"/>
<polygon points="112,{piston1_y - 38} 128,{piston1_y - 38} 120,{piston1_y - 27}" fill="#dc2626"/>
<text x="120" y="{piston1_y - 60}" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#dc2626">↓ 누르는 힘 {force1} N</text>

<rect x="291.8" y="{piston2_y}" width="186.4" height="18" rx="2" fill="#334155"/>
<rect x="377" y="{piston2_y - 28}" width="16" height="28" fill="#64748b"/>

<g class="force-up">
  <line x1="385" y1="{piston2_y - 32}" x2="385" y2="{piston2_y - 56}" stroke="#059669" stroke-width="{arrow2_width}" stroke-linecap="round"/>
  <polygon points="375,{piston2_y - 50} 395,{piston2_y - 50} 385,{piston2_y - 64}" fill="#059669"/>
  <text x="385" y="{piston2_y - 70}" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="#059669">↑ 출력 힘 {force2:.1f} N</text>
</g>

<rect x="175" y="285" width="210" height="24" rx="5" fill="#f1f5f9"/>
<text x="280" y="302" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">전달 압력 P = {pressure:.2f} N/cm²</text>
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
