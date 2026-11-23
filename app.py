import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", layout="wide")

# 2. 함수 정의 (파스칼의 원리 계산)
def caculate_p(area1, area2, force1):
    if area1 <= 0:
        area1 = 1.0
    pressure = force1 / area1
    force2 = pressure * area2
    ratio = area2 / area1
    return pressure, force2, ratio

# 3. 왼쪽 사이드바: 입력 설정
st.sidebar.header("1️⃣ 입력 설정")
area1 = st.sidebar.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
area2 = st.sidebar.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
force1 = st.sidebar.slider("작은 피스톤에 가하는 힘 F₁ (N)", min_value=1, max_value=100, value=40, step=1)
run_btn = st.sidebar.button("결과 도출하기")

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 4. 메인 화면
st.title("⚙️ 유압 압력장치 힘 계산 및 비교 프로그램")

top_left, top_right = st.columns([1.4, 1])

with top_left:
    st.subheader("📐 실시간 피스톤 작동 모습")
    
    # 힘에 따른 피스톤 이동 거리
    shift1 = (force1 / 100.0) * 55.0
    raw_shift2 = shift1 * (area1 / area2)
    shift2 = max(min(raw_shift2 * 2.5, 45.0), (force1 / 100.0) * 12.0)

    piston1_y = 115.0 + shift1
    piston2_y = 155.0 - shift2

    # 한 줄로 압축된 안전한 SVG 코드 (마크다운 파싱 에러 0%)
    svg_code = f'''<div style="background:#ffffff; border:2px solid #cbd5e1; border-radius:10px; padding:10px; text-align:center;"><svg width="100%" height="330" viewBox="0 0 640 330" xmlns="http://www.w3.org/2000/svg"><text x="125" y="185" font-size="13" font-weight="bold" text-anchor="end" fill="#334155">작은 피스톤</text><text x="125" y="205" font-size="14" font-weight="bold" text-anchor="end" fill="#0284c7">면적 A₁ = {area1} cm²</text><line x1="132" y1="192" x2="148" y2="192" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/><text x="515" y="185" font-size="13" font-weight="bold" text-anchor="start" fill="#334155">큰 피스톤</text><text x="515" y="205" font-size="14" font-weight="bold" text-anchor="start" fill="#0284c7">면적 A₂ = {area2} cm²</text><line x1="492" y1="192" x2="508" y2="192" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/><path d="M 150 95 L 150 285 L 490 285 L 490 95" fill="none" stroke="#1e293b" stroke-width="3.5"/><path d="M 230 95 L 230 225 L 330 225 L 330 95" fill="none" stroke="#1e293b" stroke-width="3.5"/><path d="M 151.8 {piston1_y + 18} L 228.2 {piston1_y + 18} L 228.2 226.8 L 331.8 226.8 L 331.8 {piston2_y + 18} L 488.2 {piston2_y + 18} L 488.2 283.2 L 151.8 283.2 Z" fill="#dbeafe"/><rect x="151.8" y="{piston1_y}" width="76.4" height="18" fill="#334155"/><rect x="184" y="{piston1_y - 30}" width="12" height="30" fill="#64748b"/><line x1="190" y1="{piston1_y - 62}" x2="190" y2="{piston1_y - 38}" stroke="#dc2626" stroke-width="4"/><polygon points="183,{piston1_y - 42} 197,{piston1_y - 42} 190,{piston1_y - 31}" fill="#dc2626"/><text x="190" y="{piston1_y - 70}" font-size="14" font-weight="bold" text-anchor="middle" fill="#dc2626">↓ 누르는 힘 {force1} N</text><rect x="331.8" y="{piston2_y}" width="156.4" height="18" fill="#334155"/><rect x="402" y="{piston2_y - 30}" width="16" height="30" fill="#64748b"/><line x1="410" y1="{piston2_y - 35}" x2="410" y2="{piston2_y - 60}" stroke="#059669" stroke-width="4"/><polygon points="403,{piston2_y - 55} 417,{piston2_y - 55} 410,{piston2_y - 67}" fill="#059669"/><text x="410" y="{piston2_y - 75}" font-size="14" font-weight="bold" text-anchor="middle" fill="#059669">↑ 출력 힘 {force2:.1f} N</text><text x="320" y="260" font-size="13" font-weight="bold" text-anchor="middle" fill="#1e40af">유압 전달 압력 P = {pressure:.2f} N/cm²</text></svg></div>'''
    st.markdown(svg_code, unsafe_allow_html=True)

with top_right:
    st.subheader("📊 계산 결과 요약")
    st.metric(label="전달 압력 (P)", value=f"{pressure:.2f} N/cm²")
    st.metric(label="큰 피스톤 출력 힘 (F₂)", value=f"{force2:.2f} N")
    st.metric(label="힘 증가 배수", value=f"{ratio:.2f} 배")

    # 5. 조건문(if-elif-else)
    if ratio >= 10:
        st.success(f"**[10배 이상]** 힘이 **{ratio:.2f}배** 증폭되었습니다.")
    elif ratio >= 5:
        st.info(f"**[5배 이상]** 힘이 **{ratio:.2f}배** 증폭되었습니다.")
    else:
        st.warning(f"**[5배 미만]** 힘이 **{ratio:.2f}배** 증가했습니다.")

st.markdown("---")

# 6. 리스트(p_force)와 반복문(for)을 활용한 표
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
