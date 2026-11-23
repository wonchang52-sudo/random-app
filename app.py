import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="유압 압력장치 시뮬레이터", page_icon="⚙️", layout="wide")

# 2. 가독성과 디자인을 살리는 고대비 커스텀 CSS (글씨 굵기·크기 계층화 + 표 스타일링)
st.markdown("""
<style>
/* 상단 헤더 스타일 */
.app-header {
    padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 24px;
}
.app-title {
    font-size: 30px;
    font-weight: 900;
    color: #0f172a !important;
    letter-spacing: -0.5px;
    margin: 0;
}
.app-subtitle {
    font-size: 15px;
    font-weight: 400;
    color: #64748b !important;
    margin-top: 4px;
}

/* 섹션 소제목 */
.sec-title {
    font-size: 18px;
    font-weight: 800;
    color: #1e293b !important;
    margin-bottom: 12px;
}

/* 결과 카드 (상단 포인트 컬러 + 글씨 굵기 대비) */
.stat-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    margin-bottom: 14px;
}
.card-blue { border-top: 4px solid #3b82f6; }
.card-green { border-top: 4px solid #10b981; }
.card-purple { border-top: 4px solid #8b5cf6; }

.stat-label {
    font-size: 13px;
    font-weight: 600;
    color: #64748b !important;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
}
.stat-value {
    font-size: 30px;
    font-weight: 900;
    color: #0f172a !important;
    line-height: 1.1;
}
.stat-unit {
    font-size: 15px;
    font-weight: 500;
    color: #94a3b8 !important;
    margin-left: 4px;
}
.stat-desc {
    font-size: 13px;
    font-weight: 400;
    color: #475569 !important;
    margin-top: 8px;
}

/* 배수 판정 배지 박스 */
.badge-box {
    padding: 16px 20px;
    border-radius: 12px;
    margin-top: 6px;
}
.badge-high { background-color: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46 !important; }
.badge-mid  { background-color: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af !important; }
.badge-low  { background-color: #fffbeb; border: 1px solid #fde68a; color: #92400e !important; }

.badge-title { font-size: 16px; font-weight: 800; margin-bottom: 4px; }
.badge-text  { font-size: 14px; font-weight: 400; opacity: 0.9; }

/* 커스텀 예쁜 비교표 스타일 */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 15px;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.styled-table thead tr {
    background-color: #1e293b;
    color: #ffffff !important;
    text-align: center;
    font-weight: 700;
}
.styled-table th, .styled-table td {
    padding: 14px 18px;
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
st.sidebar.caption("피스톤 면적과 가하는 힘을 조절해 보세요.")
st.sidebar.markdown("---")

area1 = st.sidebar.number_input("작은 피스톤 면적 A₁ (cm²)", min_value=1.0, max_value=100.0, value=5.0, step=1.0)
area2 = st.sidebar.number_input("큰 피스톤 면적 A₂ (cm²)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
st.sidebar.write("")
force1 = st.sidebar.slider("작은 피스톤에 가하는 힘 F₁ (N)", min_value=1, max_value=100, value=40, step=1)
st.sidebar.write("")
run_btn = st.sidebar.button("🚀 결과 도출하기", use_container_width=True)

# 계산 실행
pressure, force2, ratio = caculate_p(area1, area2, force1)

# 5. 메인 상단 헤더
st.markdown("""
<div class="app-header">
    <div class="app-title">⚙️ 유압 압력장치 힘 계산 및 비교 시뮬레이터</div>
    <div class="app-subtitle">파스칼의 원리(P = F₁/A₁ = F₂/A₂)를 활용한 피스톤 힘 증폭 분석 대시보드</div>
</div>
""", unsafe_allow_html=True)

# 6. 중단: 좌측(움직이는 피스톤 도면) + 우측(입체 결과 카드)
top_left, top_right = st.columns([1.35, 1])

with top_left:
    st.markdown('<div class="sec-title">📐 실시간 피스톤 작동 모습</div>', unsafe_allow_html=True)
    
    # 힘에 따른 피스톤 이동 거리
    shift1 = (force1 / 100.0) * 55.0
    raw_shift2 = shift1 * (area1 / area2)
    shift2 = max(min(raw_shift2 * 2.5, 45.0), (force1 / 100.0) * 12.0)

    piston1_y = 115.0 + shift1
    piston2_y = 155.0 - shift2

    # 깔끔하고 선명한 한 줄 압축 SVG 도면
    svg_code = f'''<div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:12px; padding:14px; text-align:center; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);"><svg width="100%" height="340" viewBox="0 0 640 340" xmlns="http://www.w3.org/2000/svg"><text x="125" y="185" font-size="13" font-weight="600" text-anchor="end" fill="#64748b">작은 피스톤</text><text x="125" y="206" font-size="15" font-weight="800" text-anchor="end" fill="#0284c7">A₁ = {area1} cm²</text><line x1="132" y1="192" x2="148" y2="192" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/><text x="515" y="185" font-size="13" font-weight="600" text-anchor="start" fill="#64748b">큰 피스톤</text><text x="515" y="206" font-size="15" font-weight="800" text-anchor="start" fill="#0284c7">A₂ = {area2} cm²</text><line x1="492" y1="192" x2="508" y2="192" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/><path d="M 150 95 L 150 285 L 490 285 L 490 95" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/><path d="M 230 95 L 230 225 L 330 225 L 330 95" fill="none" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round"/><path d="M 151.8 {piston1_y + 18} L 228.2 {piston1_y + 18} L 228.2 226.8 L 331.8 226.8 L 331.8 {piston2_y + 18} L 488.2 {piston2_y + 18} L 488.2 283.2 L 151.8 283.2 Z" fill="#dbeafe"/><rect x="151.8" y="{piston1_y}" width="76.4" height="18" rx="2" fill="#334155"/><rect x="184" y="{piston1_y - 30}" width="12" height="30" fill="#64748b"/><line x1="190" y1="{piston1_y - 62}" x2="190" y2="{piston1_y - 38}" stroke="#dc2626" stroke-width="4" stroke-linecap="round"/><polygon points="183,{piston1_y - 42} 197,{piston1_y - 42} 190,{piston1_y - 31}" fill="#dc2626"/><text x="190" y="{piston1_y - 70}" font-size="14" font-weight="800" text-anchor="middle" fill="#dc2626">↓ 누르는 힘 {force1} N</text><rect x="331.8" y="{piston2_y}" width="156.4" height="18" rx="2" fill="#334155"/><rect x="402" y="{piston2_y - 30}" width="16" height="30" fill="#64748b"/><line x1="410" y1="{piston2_y - 35}" x2="410" y2="{piston2_y - 60}" stroke="#059669" stroke-width="4" stroke-linecap="round"/><polygon points="403,{piston2_y - 55} 417,{piston2_y - 55} 410,{piston2_y - 67}" fill="#059669"/><text x="410" y="{piston2_y - 75}" font-size="15" font-weight="800" text-anchor="middle" fill="#059669">↑ 출력 힘 {force2:.1f} N</text><rect x="210" y="244" width="220" height="24" rx="6" fill="#eff6ff"/><text x="320" y="260" font-size="13" font-weight="700" text-anchor="middle" fill="#1d4ed8">전달 압력 P = {pressure:.2f} N/cm²</text></svg></div>'''
    st.markdown(svg_code, unsafe_allow_html=True)

with top_right:
    st.markdown('<div class="sec-title">📊 핵심 도출 결과</div>', unsafe_allow_html=True)
    
    # 2열 미니 카드 (전달 압력 & 힘 증가 배수)
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

    # 메인 강조 카드 (큰 피스톤 출력 힘)
    st.markdown(f"""
<div class="stat-card card-green">
    <div class="stat-label">큰 피스톤 최종 출력 힘 (F₂)</div>
    <div class="stat-value" style="color:#059669 !important; font-size:34px;">{force2:.2f}<span class="stat-unit">N</span></div>
    <div class="stat-desc">입력 힘 <b>{force1} N</b> 대비 <b>+{force2 - force1:.1f} N</b> 추가 증폭됨</div>
</div>
""", unsafe_allow_html=True)

    # 7. 조건문(if-elif-else)을 활용한 배수 등급 카드
    if ratio >= 10:
        st.markdown(f"""
<div class="badge-box badge-high">
    <div class="badge-title">🔥 10배 이상 고출력 증폭 ({ratio:.2f}배)</div>
    <div class="badge-text">매우 강력한 유압 증폭 상태입니다. 무거운 하중도 쉽게 들어 올립니다.</div>
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
st.markdown("---")

# 8. 하단: 리스트(p_force)와 반복문(for)을 활용한 디자인 표
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
