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
    color: #3341
