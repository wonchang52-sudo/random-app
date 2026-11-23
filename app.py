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
    run_btn = st.button("결과 도출하기", type="primary", use_container_width=True)

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 4. 메인 화면
st.title("⚙️ 유압 압력장치 힘 계산 및 비교 프로그램")

top_left, top_right = st.columns([1.35, 1], gap="large")

with top_left:
    st.subheader("📐 실시간 피스톤 작동 모습")
    
    # 힘(force1)에 따른 피스톤 이동 및 화살표 크기 역동적 계산
    shift = (force1 / 100) * 40         # 최대 40px 이동
    piston1_y = 95 + shift               # 작은 피스톤 Y좌표 (아래로 이동)
    piston2_y = 135 - shift              # 큰 피스톤 Y좌표 (위로 이동)
    
    # 힘의 크기에 비례해 화살표 굵기와 길이 변화
    arrow1_width = 3 + (force1 / 100) * 4
    arrow2_width = min(4 + (ratio / 15) * 5, 10)
    anim_speed = max(2.2 - (force1 / 100) * 1.5, 0.4)  # 힘이 셀수록 유체 흐름이 빨라짐

    # 역동적인 SVG 피스톤 일러스트 (A1, A2 텍스트 위치 고정으로 절대 안 가려짐)
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
        .fluid-flow {{
          animation: flowRight {anim_speed}s infinite ease-in-out;
        }}
        .force-up {{
          animation: pulseForce 1s infinite ease-in-out;
        }}
      </style>

      <!-- 상단 고정 면적 라벨 (피스톤이 움직여도 절대 안 가려짐) -->
      <rect x="65" y="10" width="110" height="26" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
      <text x="120" y="28" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₁: {area1} cm²</text>

      <rect x="325" y="10" width="120" height="26" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
      <text x="385" y="28" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">면적 A₂: {area2} cm²</text>

      <!-- 실린더 외벽 -->
      <path d="M 75 80 L 75 275 L 480 275 L 480 80" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M 165 80 L 165 215 L 290 215 L 290 80" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/>

      <!-- 유압유 (피스톤 움직임에 따라 높이 연동) -->
      <path d="M 76.8 {piston1_y + 18} L 163.2 {piston1_y + 18} L 163.2 216.8 L 291.8 216.8 L 291.8 {piston2_y + 18} L 478.2 {piston2_y + 18} L 478.2 273.2 L 76.8 273.2 Z" fill="#bae6fd"/>

      <!-- 유압 전달 역동적 화살표 애니메이션 -->
      <g class="fluid-flow">
        <text x="120" y="248" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0284c7">⬇</text>
        <text x="230" y="250" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="#0284c7">➔ ➔ ➔</text>
        <text x="385" y="248" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0284c7">⬆</text>
      </g>

      <!-- [왼쪽] 작은 피스톤 및 로드 -->
      <rect x="76.8" y="{piston1_y}" width="86.4" height="18" rx="2" fill="#334155"/>
      <rect x="114" y="{piston1_y - 28}" width="12" height="28" fill="#64748b"/>
      
      <!-- [왼쪽] 누르는 힘 화살표 (힘 크기에 따라 굵기 변화) -->
      <line x1="120" y1="{piston1_y - 54}" x2="120" y2="{piston1_y - 34}" stroke="#dc2626" stroke-width="{arrow1_width}" stroke-linecap="round"/>
      <polygon points="112,{piston1_y - 38} 128,{piston1_y - 38} 120,{piston1_y - 27}" fill="#dc2626"/>
