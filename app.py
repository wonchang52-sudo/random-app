import streamlit as st

# 1. 와이드 레이아웃 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 2. 한 화면 압축 & 고대비 디자인 CSS
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
    max-width: 1350px;
}
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 14px;
}
.app-title {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a !important;
    letter-spacing: -0.5px;
}
.app-subtitle {
    font-size: 13px;
    font-weight: 500;
    color: #64748b !important;
}
.sec-title {
    font-size: 15px;
    font-weight: 800;
    color: #1e293b !important;
    margin-bottom: 8px;
}
.stat-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    margin-bottom: 10px;
}
.card-blue { border-top: 3.5px solid #3b82f6; }
.card-green { border-top: 3.5px solid #10b981; }
.card-purple { border-top: 3.5px solid #8b5cf6; }

.stat-label {
    font-size: 12px;
    font-weight: 700;
    color: #64748b !important;
    margin-bottom: 4px;
}
.stat-value {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a !important;
    line-height: 1.1;
}
.stat-unit {
    font-size: 13px;
    font-weight: 500;
    color: #94a3b8 !important;
    margin-left: 3px;
}
.stat-desc {
    font-size: 12px;
    font-weight: 400;
    color: #475569 !important;
    margin-top: 4px;
}
.badge-box {
    padding: 10px 14px;
    border-radius: 10px;
    margin-top: 4px;
}
.badge-high { background-color: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46 !important; }
.badge-mid  { background-color: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af !important; }
.badge-low  { background-color: #fffbeb; border: 1px solid #fde68a; color: #92400e !important; }

.badge-title { font-size: 14px; font-weight: 800; margin-bottom: 2px; }
.badge-text  { font-size: 12px; font-weight: 400; opacity: 0.95; }

.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.styled-table thead tr {
    background-color: #1e293b;
    color: #ffffff !important;
    font-weight: 700;
}
.styled-table th, .styled-table td {
    padding: 8px 14px;
    text-align: center;
}
.styled-table tbody tr {
    border-bottom: 1px solid #e2e8f0;
    background-color: #ffffff;
    color: #334155 !important;
}
.styled-table tbody tr:nth-of-type(even) {
    background-color: #f8fafc;
}
.styled-table tbody tr:hover {
    background-color: #f1f5f9;
}
.td-bold { font-weight: 800; color: #0f172a !important; }
.td-green { font-weight: 800; color: #059669 !important; }
.td-blue { font-weight: 700; color: #2563eb !important; }
</style>
""", unsafe_allow_html=True)

# 3. 함수 정의 (파스칼의 원리 계산)
def caculate_p(area1, area2, force1):
    if area1 <= 0:
        area1 = 1.0
    pressure = force1 / area1
    force2 = pressure * area2
    ratio = area2 / area1
    return pressure, force2, ratio

# 4. 왼쪽 사이드바: 입력 설정 (구버전 에러 유발 옵션 제거)
st.sidebar.markdown("### 🎛️ 시뮬레이션 입력")
st.sidebar.caption("피스톤 면적과 힘을 조절하세요.")
st.sidebar.markdown("---")

area1 = st.sidebar.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
area2 = st.sidebar.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
force1 = st.sidebar.slider("가하는 힘 F₁ (N)", min_value=1, max_value=100, value=40, step=1)
run_btn = st.sidebar.button("🚀 결과 도출하기")

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 5. 메인 상단 헤더
st.markdown("""
<div class="app-header">
    <div class="app-title">⚙️ 유압 압력장치 힘 계산 및 비교 시뮬레이터</div>
    <div class="app-subtitle">파스칼의 원리 (P = F₁/A₁ = F₂/A₂)</div>
</div>
""", unsafe_allow_html=True)

# 6. 중단: 좌측(움직이는 피스톤 도면) + 우측(핵심 결과 카드)
top_left, top_right = st.columns([1.3, 1])

with top_left:
    st.markdown('<div class="sec-title">📐 실시간 피스톤 작동 모습</div>', unsafe_allow_html=True)
