import streamlit as st
import pandas as pd

# 1. 와이드 레이아웃 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 2. 한 화면에 쏙 들어오도록 여백과 높이를 압축한 고대비 CSS
st.markdown("""
<style>
/* 스트림릿 기본 상하 여백 축소 (스크롤 방지) */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
    max-width: 1350px;
}

/* 상단 컴팩트 헤더 */
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

/* 섹션 소제목 */
.sec-title {
    font-size: 15px;
    font-weight: 800;
    color: #1e293b !important;
    margin-bottom: 8px;
}

/* 컴팩트 결과 카드 */
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

/* 컴팩트 배수 판정 배지 */
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

/* 슬림하고 깔끔한 비교표 */
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

# 4. 왼쪽 사이드바: 입력 설정
st.sidebar.markdown("### 🎛️ 시뮬레이션 입력")
st.sidebar.caption("피스톤 면적과 힘을 조절하세요.")
st.sidebar.markdown("---")

area1 = st.sidebar.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
area2 = st.sidebar.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
force1 = st.sidebar.slider("가하는 힘 F₁ (N)", min_value=1, max_value=100, value=40, step=1)
run_btn = st.sidebar.button("🚀 결과 도출하기", use_container_width=True)

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 5. 메인 상단 컴팩트 헤더
st.markdown("""
<div class="app-header">
    <div class="app-title">⚙️ 유압 압력장치 힘 계산 및 비교 시뮬레이터</div>
    <div class="app-subtitle">파스칼의 원리 (P = F₁/A₁ = F₂/A₂)</div>
</div>
""", unsafe_allow_html=True)

# 6. 상단 영역: 좌측(움직이는 피스톤 도면) + 우측(핵심 결과 카드)
top_left, top_right = st.columns([1.3, 1])

with top_left:
    st.markdown('<div class="sec-title">📐 실시간 피스톤 작동 모습</div>', unsafe_allow_html=True)
    
    # 피스톤 이동 거리 계산 (컴팩트 높이 265px 기준 최적화)
    shift1 = (force1 / 100.0) * 42.0
    raw_shift2 = shift1 * (area1 / area2)
    shift2 = max(min(raw_shift2 * 2.5, 35.0), (force1 / 100.0) * 10.0)

    piston1_y = 92.0 + shift1
    piston2_y = 122.0 - shift2

    # 한 줄 압축 SVG 도면 (높이 265px)
    svg_code = f'''<div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:8px; text-align:center; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);"><svg width="100%" height="265" viewBox="0 0 640 275" xmlns="http://www.w3.org/2000/svg"><text x="125" y="150" font-size="13" font-weight="600" text-anchor="end" fill="#64748b">작은 피스톤</text><text x="125" y="170" font-size="15" font-weight="800" text-anchor="end" fill="#0284c7">A₁ = {area1} cm²</text><line x1="132" y1="158" x2="148" y2="158" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/><text x="515" y="150" font-size="13" font-weight="600" text-anchor="start" fill="#64748b">큰 피스톤</text><text x="515" y="170" font-size="15" font-weight="800" text-anchor="start" fill="#0284c7">A₂ = {area2} cm²</text><line x1="492" y1="158" x2="508" y2="158" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/><path d="M 150 75 L 150 245 L 490 245 L 490 75" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/><path d="M 230 75 L 230 190 L 330 190 L 330 75" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/><path d="M 151.8 {piston1_y + 16} L 228.2 {piston1_y + 16} L 228.2 191.8 L 331.8 191.8 L 331.8 {piston2_y + 16} L 488.2 {piston2_y + 16} L 488.2 243.2 L 151.8 243.2 Z" fill="#dbeafe"/><rect x="151.8" y="{piston1_y}" width="76.4" height="16" rx="2" fill="#334155"/><rect x="184" y="{piston1_y - 24}" width="12" height="24" fill="#64748b"/><line x1="190" y1="{piston1_y - 50}" x2="190" y2="{piston1_y - 30}" stroke="#dc2626" stroke-width="4" stroke-linecap="round"/><polygon points="183,{piston1_y - 34} 197,{piston1_y - 34} 190,{piston1_y - 24}" fill="#dc2626"/><text x="190" y="{piston1_y - 57}" font-size="14" font-weight="800" text-anchor="middle" fill="#dc2626">↓ 누르는 힘 {force1} N</text><rect x="331.8" y="{piston2_y}" width="156.4" height="16" rx="2" fill="#334155"/><rect x="402" y="{piston2_y - 24}" width="16" height="24" fill="#64748b"/><line x1="410" y1="{piston2_y - 28}" x2="410" y2="{piston2_y - 50}" stroke="#059669" stroke-width="4" stroke-linecap="round"/><polygon points="403,{piston2_y - 45} 417,{piston2_y - 45} 410,{piston2_y - 56}" fill="#059669"/><text x="410" y="{piston2_y - 62}" font-size="15" font-weight="800" text-anchor="middle" fill="#059669">↑ 출력 힘 {force2:.1f} N</text><rect x="210" y="208" width="220" height="22" rx="5" fill="#eff6ff"/><text x="320" y="223" font-size="13" font-weight="700" text-anchor="middle" fill="#1d4ed8">전달 압력 P = {pressure:.2f} N/cm²</text></svg></div>'''
    st.markdown(svg_code, unsafe_allow_html=True)

with top_right:
    st.markdown('<div class="sec-title">📊 핵심 도출 결과</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
<div class="stat-card card-blue">
    <div class="stat-label">전달 압력 (P)</div>
    <div class="stat-value">{pressure:.2f}<span class="stat-unit">N/cm²</span></div>
    <div class="stat-desc">유체 내부 동일 압력</div>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class="stat-card card-purple">
    <div class="stat-label">힘 증가 배수</div>
    <div class="stat-value">{ratio:.2f}<span class="stat-unit">배</span></div>
    <div class="stat-desc">면적 비율 (A₂ ÷ A₁)</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="stat-card card-green">
    <div class="stat-label">큰 피스톤 최종 출력 힘 (F₂)</div>
    <div class="stat-value" style="color:#059669 !important; font-size:28px;">{force2:.2f}<span class="stat-unit">N</span></div>
    <div class="stat-desc">입력 힘 <b>{force1} N</b> 대비 <b>+{force2 - force1:.1f} N</b> 증폭됨</div>
</div>
""", unsafe_allow_html=True)

    # 7. 조건문(if-elif-else)을 활용한 배수 등급 카드
    if ratio >= 10:
        st.markdown(f"""
<div class="badge-box badge-high">
    <div class="badge-title">🔥 10배 이상 고출력 증폭 ({ratio:.2f}배)</div>
    <div class="badge-text">매우 강력한 유압 증폭 상태입니다. 무거운 물체도 거뜬히 들어 올립니다.</div>
</div>
""", unsafe_allow_html=True)
    elif ratio >= 5:
        st.markdown(f"""
<div class="badge-box badge-mid">
    <div class="badge-title">⚡ 5배 이상 표준 증폭 ({ratio:.2f}배)</div>
    <div class="badge-text">안정적이고 효율적인 유압 힘 증폭이 이루어지고 있습니다.</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="badge-box badge-low">
    <div class="badge-title">💧 5배 미만 저배율 ({ratio:.2f}배)</div>
    <div class="badge-text">더 큰 출력을 원하시면 큰 피스톤 면적(A₂)을 넓혀보세요.</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# 8. 하단 영역: 리스트(p_force)와 반복문(for)을 활용한 컴팩트 비교표
st.markdown('<div class="sec-title">📋 기준 힘(10N ~ 50N) 구간별 출력 비교표</div>', unsafe_allow_html=True)

p_force = [10, 20, 30, 40, 50]
rows_html = ""

for f in p_force:
    p_val, f2_val, r_val = caculate_p(area1, area2, f)
    rows_html += f"""
<tr>
    <td class="td-bold">{f} N</td>
    <td>{p_val:.2f} N/cm²</td>
    <td class="td-green">{f2_val:.2f} N</td>
    <td class="td-blue">{r_val:.2f} 배</td>
</tr>
"""

table_html = f"""
<table class="styled-table">
    <thead>
        <tr>
            <th>가하는 힘 F₁ (↓)</th>
            <th>유압 전달 압력 P</th>
            <th>큰 피스톤 출력 힘 F₂ (↑)</th>
            <th>힘 증가 비율</th>
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>
"""
st.markdown(table_html, unsafe_allow_html=True)
