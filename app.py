import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# 1. 와이드 레이아웃 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 고대비 깔끔한 CSS
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
    shift1 = (force1 / 100.0) * 55.0
    raw_shift2 = shift1 * (area1 / area2)
    shift2 = max(min(raw_shift2 * 2.5, 45.0), (force1 / 100.0) * 12.0)

    base_y1 = 115.0
    base_y2 = 155.0
    
    piston1_y = base_y1 + shift1   # 작은 피스톤 (아래로 이동)
    piston2_y = base_y2 - shift2   # 큰 피스톤 (위로 이동)

    # components.html 전용 HTML+SVG 코드 (스트림릿이 절대 차단하지 않음)
    piston_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{
        margin: 0;
        padding: 0;
        background-color: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }}
      .canvas-box {{
        background-color: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        box-sizing: border-box;
      }}
      .smooth-move {{
        transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
      }}
    </style>
    </head>
    <body>
      <div class="canvas-box">
        <svg width="100%" height="330" viewBox="0 0 640 330" xmlns="http://www.w3.org/2000/svg">
          <!-- [고정 텍스트] 왼쪽 피스톤 옆에 가만히 있는 면적 설명 -->
          <text x="125" y="185" font-size="13" font-weight="bold" text-anchor="end" fill="#334155">작은 피스톤</text>
          <text x="125" y="205" font-size="14" font-weight="bold" text-anchor="end" fill="#0284c7">면적 A₁ = {area1} cm²</text>
          <line x1="132" y1="192" x2="148" y2="192" stroke="#94a3b8
