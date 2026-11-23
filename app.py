import streamlit as st
import pandas as pd

# 1. 함수 정의 (파스칼의 원리를 이용한 출력 힘 및 배수 계산)
# 요청하신 이름과 매개변수를 그대로 사용했습니다.
def caculate_p(area1, area2, force1):
    # 압력(P) = 힘(F1) / 면적(A1)
    pressure = force1 / area1
    # 큰 피스톤의 출력 힘(F2) = 압력(P) * 큰 면적(A2)
    force2 = pressure * area2
    # 힘의 증가 배수 = A2 / A1
    ratio = area2 / area1
    return pressure, force2, ratio

# 페이지 기본 설정
st.set_page_config(page_title="파스칼의 원리 유압 계산기", page_icon="⚙️", layout="centered")

st.title("⚙️ 유압 압력장치 힘 계산 및 비교 프로그램")
st.markdown("파스칼의 원리($P = \\frac{F_1}{A_1} = \\frac{F_2}{A_2}$)를 이용하여 피스톤의 힘 증가 비율을 계산합니다.")

# 2. 피스톤 구조 시각화 (SVG 그래픽으로 별도 이미지 파일 없이 바로 출력)
st.subheader("📐 유압 피스톤 작동 원리")
piston_svg = """
<div style="display: flex; justify-content: center; margin: 20px 0;">
<svg width="450" height="220" viewBox="0 0 450 220" xmlns="http://www.w3.org/2000/svg">
  <!-- 유압유 (파란색 액체) -->
  <path d="M 80 90 L 140 90 L 140 160 L 250 160 L 250 90 L 370 90 L 370 200 L 80 200 Z" fill="#3b82f6" opacity="0.3" stroke="#2563eb" stroke-width="2"/>
  
  <!-- 작은 피스톤 (F1, A1) -->
  <rect x="80" y="70" width="60" height="20" fill="#475569"/>
  <rect x="105" y="30" width="10" height="40" fill="#64748b"/>
  <!-- 누르는 화살표 -->
  <line x1="110" y1="5" x2="110" y2="25" stroke="#ef4444" stroke-width="4"/>
  <polygon points="103,22 117,22 110,30" fill="#ef4444"/>
  <text x="110" y="115" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e293b">면적 A₁</text>
  <text x="50" y="25" font-size="14" font-weight="bold" fill="#ef4444">입력 힘 F₁</text>

  <!-- 큰 피스톤 (F2, A2) -->
  <rect x="250" y="70" width="120" height="20" fill="#475569"/>
  <rect x="302" y="30" width="16" height="40" fill="#64748b"/>
  <!-- 올라가는 화살표 -->
  <line x1="310" y1="28" x2="310" y2="8" stroke="#10b981" stroke-width="4"/>
  <polygon points="303,12 317,12 310,3" fill="#10b981"/>
  <text x="310" y="115" font-size="14" font-weight="bold" text-anchor="middle" fill="#1e293b">면적 A₂</text>
  <text x="330" y="25" font-size="14" font-weight="bold" fill="#10b981">출력 힘 F₂</text>

  <!-- 압력 전달 표시 -->
  <text x="200" y="185" font-size="13" font-weight="bold" text-anchor="middle" fill="#1d4ed8">동일한 압력(P) 전달 →</text>
</svg>
</div>
"""
st.markdown(piston_svg, unsafe_allow_html=True)

st.divider()

# 3. 사용자 입력 구역
st.subheader("🔢 피스톤 규격 및 입력 힘 설정")
col1, col2, col3 = st.columns(3)

with col1:
    area1 = st.number_input("작은 피스톤 면적 (A₁, cm²)", min_value=1.0, value=5.0, step=1.0)
with col2:
    area2 = st.number_input("큰 피스톤 면적 (A₂, cm²)", min_value=1.0, value=50.0, step=1.0)
with col3:
    force1 = st.number_input("가하는 힘 (F₁, N)", min_value=1.0, value=20.0, step=5.0)

# 4. 도출 버튼 및 결과 출력
if st.button("🚀 결과 도출하기", use_container_width=True):
    # 함수 호출
    pressure, force2, ratio = caculate_p(area1, area2, force1)
    
    st.subheader("📊 계산 결과")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("전달되는 압력 (P)", f"{pressure:.2f} N/cm²")
    res_col2.metric("큰 피스톤 출력 힘 (F₂)", f"{force2:.2f} N")
    res_col3.metric("힘 증가 배수", f"{ratio:.2f} 배")
    
    # 5. 조건문(if-elif-else)을 활용한 힘의 배수 판별
    if ratio >= 10:
        st.success(f"🔥 **10배 이상** 증폭되었습니다! (현재 {ratio:.2f}배) - 매우 강력한 유압 증폭 효과입니다.")
    elif ratio >= 5:
        st.info(f"⚡ **5배 이상 (10배 미만)** 증폭되었습니다. (현재 {ratio:.2f}배) - 준수한 유압 증폭 효과입니다.")
    else:
        st.warning(f"💧 **5배 미만**입니다. (현재 {ratio:.2f}배) - 큰 피스톤의 면적을 더 넓히면 힘이 커집니다.")

    st.divider()

    # 6. 리스트(p_force)와 반복문(for)을 활용한 표 생성
    st.subheader("📋 기준 힘(10~50N) 적용 시 결과 비교표")
    p_force = [10, 20, 30, 40, 50]
    table_data = []

    for f in p_force:
        # 리스트의 각 힘을 함수에 대입하여 결과 계산
        p_val, f2_val, r_val = caculate_p(area1, area2, f)
        table_data.append({
            "가한 힘 F₁ (N)": f"{f} N",
            "전달 압력 P (N/cm²)": f"{p_val:.2f}",
            "출력 힘 F₂ (N)": f"{f2_val:.2f} N",
            "힘 증가 비율 (배수)": f"{r_val:.2f} 배"
        })

    # 데이터프레임으로 변환하여 표 출력
    df = pd.DataFrame(table_data)
    st.table(df)
