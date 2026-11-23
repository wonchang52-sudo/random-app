import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (넓은 레이아웃 및 아이콘)
st.set_page_config(page_title="유압 압력 시뮬레이터", page_icon="💧", layout="centered")

# 2. 커스텀 CSS (디자인 대폭 개선)
st.markdown("""
<style>
    /* 전체 배경 및 폰트 스타일 */
    .main-title {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);
        margin-bottom: 25px;
    }
    .main-title h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .main-title p {
        margin: 8px 0 0 0;
        font-size: 15px;
        opacity: 0.9;
    }
    /* 결과 카드 디자인 */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    .card-label {
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .card-value {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
    }
    .card-unit {
        font-size: 14px;
        font-weight: 600;
        color: #3b82f6;
    }
    /* 버튼 스타일 */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        font-weight: 700;
        font-size: 17px;
        padding: 12px 24px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #1e40af);
        transform: scale(1.01);
    }
</style>
""", unsafe_allow_html=True)

# 3. 함수 정의 (파스칼의 원리 계산)
def caculate_p(area1, area2, force1):
    pressure = force1 / area1
    force2 = pressure * area2
    ratio = area2 / area1
    return pressure, force2, ratio

# 상단 타이틀 배너
st.markdown("""
<div class="main-title">
    <h1>💧 파스칼의 원리 유압 시뮬레이터</h1>
    <p>작은 힘으로 큰 힘을 만들어내는 유압 압력장치의 증폭 원리를 실험해 보세요</p>
</div>
""", unsafe_allow_html=True)

# 4. 고퀄리티 피스톤 일러스트 SVG
piston_svg = """
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin-bottom: 25px; display: flex; justify-content: center;">
<svg width="480" height="230" viewBox="0 0 480 230" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 유압유 그라데이션 -->
    <linearGradient id="fluidGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.9"/>
    </linearGradient>
    <!-- 금속 피스톤 그라데이션 -->
    <linearGradient id="metalGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>

  <!-- 실린더 외벽 (유리관 느낌) -->
  <path d="M 75 60 L 75 205 L 405 205 L 405 60" fill="none" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
  <path d="M 145 60 L 145 155 L 255 155 L 255 60" fill="none" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>

  <!-- 유압유 채우기 -->
  <path d="M 77 105 L 143 105 L 143 157 L 257 157 L 257 105 L 403 105 L 403 203 L 77 203 Z" fill="url(#fluidGrad)"/>

  <!-- 작은 피스톤 (A1) -->
  <rect x="78" y="85" width="64" height="20" rx="3" fill="url(#metalGrad)"/>
  <rect x="104" y="40" width="12" height="45" fill="#475569"/>
  <!-- 입력 힘 화살표 (F1) -->
  <line x1="110" y1="8" x2="110" y2="32" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
  <polygon points="101,28 119,28 110,40" fill="#ef4444"/>
  <rect x="35" y="10" width="62" height="24" rx="6" fill="#fee2e2"/>
  <text x="66" y="26" font-size="13" font-weight="bold" text-anchor="middle" fill="#dc2626">입력 힘 F₁</text>
  <text x="110" y="130" font-size="14" font-weight="bold" text-anchor="middle" fill="#ffffff">면적 A₁</text>

  <!-- 큰 피스톤 (A2) -->
  <rect x="258" y="85" width="144" height="20" rx="3" fill="url(#metalGrad)"/>
  <rect x="320" y="40" width="20" height="45" fill="#475569"/>
  <!-- 출력 힘 화살표 (F2) -->
  <line x1="330" y1="36" x2="330" y2="12" stroke="#10b981" stroke-width="5" stroke-linecap="round"/>
  <polygon points="321,16 339,16 330,4" fill="#10b981"/>
  <rect x="350" y="10" width="68" height="24" rx="6" fill="#d1fae5"/>
  <text x="384" y="26" font-size="13" font-weight="bold" text-anchor="middle" fill="#059669">출력 힘 F₂</text>
  <text x="330" y="130" font-size="14" font-weight="bold" text-anchor="middle" fill="#ffffff">면적 A₂</text>

  <!-- 내부 압력 전달 화살표 -->
  <text x="240" y="185" font-size="13" font-weight="bold" text-anchor="middle" fill="#ffffff">동일한 압력(P) 전달 ➔ ➔ ➔</text>
</svg>
</div>
"""
st.markdown(piston_svg, unsafe_allow_html=True)

# 5. 사용자 입력 컨트롤 영역 (박스 컨테이너로 깔끔하게 묶음)
with st.container(border=True):
    st.subheader("🎛️ 피스톤 규격 및 입력 힘 조절")
    col1, col2 = st.columns(2)
    with col1:
        area1 = st.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
    with col2:
        area2 = st.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
    
    st.write("") # 여백
    # 가하는 힘 슬라이더 적용
    force1 = st.slider("작은 피스톤에 가하는 힘 F₁ (N)", min_value=1, max_value=100, value=20, step=1)

st.write("")

# 6. 도출 버튼 및 결과 출력
if st.button("🚀 압력 및 증폭 결과 도출하기", use_container_width=True):
    pressure, force2, ratio = caculate_p(area1, area2, force1)
    
    st.write("")
    st.subheader("📊 실시간 계산 결과")
    
    # 커스텀 HTML 카드로 결과 출력
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label">전달되는 압력 (P)</div>
            <div class="card-value">{pressure:.2f} <span class="card-unit">N/cm²</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label">큰 피스톤 출력 힘 (F₂)</div>
            <div class="card-value">{force2:.2f} <span class="card-unit">N</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label">힘 증가 배수</div>
            <div class="card-value">{ratio:.2f} <span class="card-unit">배</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")

    # 7. 조건문(if-elif-else)을 활용한 배수 등급 판별
    if ratio >= 10:
        st.success(f"🔥 **[10배 이상 증폭]** 힘이 **{ratio:.2f}배** 강해졌습니다! 무거운 물체도 거뜬히 들어 올릴 수 있는 강력한 증폭입니다.")
    elif ratio >= 5:
        st.info(f"⚡ **[5배 이상 ~ 10배 미만 증폭]** 힘이 **{ratio:.2f}배** 강해졌습니다! 효율적인 힘의 증폭이 일어났습니다.")
    else:
        st.warning(f"💧 **[5배 미만 증폭]** 힘이 **{ratio:.2f}배** 증가했습니다. 더 큰 힘을 얻으려면 큰 피스톤 면적(A₂)을 넓혀보세요.")

    st.divider()

    # 8. 리스트(p_force)와 반복문(for)을 활용한 비교표 출력
    st.subheader("📋 기준 힘(10N ~ 50N) 구간별 출력 비교표")
    st.caption(f"현재 설정된 피스톤 면적 비율 (A₁={area1}cm², A₂={area2}cm²) 기준")
    
    p_force = [10, 20, 30, 40, 50]
    table_data = []

    for f in p_force:
        p_val, f2_val, r_val = caculate_p(area1, area2, f)
        table_data.append({
            "가하는 힘 F₁": f"{f} N",
            "전달 압력 P": f"{p_val:.2f} N/cm²",
            "출력되는 힘 F₂": f"{f2_val:.2f} N",
            "힘 증가 비율": f"{r_val:.2f} 배"
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
