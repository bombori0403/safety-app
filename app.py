import streamlit as st
import pandas as pd
from datetime import datetime

# 앱 제목 및 설정
st.set_page_config(page_title="안전제일: 위험성평가 참여 앱", layout="centered")

st.title("🚧 현장 위험성평가 참여")
st.write("현장의 위험 요인을 발견하면 즉시 등록해 주세요.")

# 1. 사용자 정보 입력
with st.expander("👤 보고자 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("성명")
    with col2:
        department = st.selectbox("부서", ["제조팀", "물류팀", "공무팀", "안전환경팀"])

# 2. 위험 요인 등록
st.divider()
st.subheader("📍 위험 요인 상세")

location = st.text_input("위험 장소 (예: A라인 세척기 근처)")
hazard_desc = st.text_area("위험 요인 설명", placeholder="어떤 상황이 위험한가요?")

# 사진 첨부
uploaded_file = st.file_uploader("현장 사진 업로드", type=["jpg", "png", "jpeg"])

# 3. 위험성 계산 (L x S)
st.divider()
st.subheader("📊 위험도 자가 평가")

col3, col4 = st.columns(2)
with col3:
    frequency = st.slider("발생 빈도(L)", 1, 5, 3)
with col4:
    severity = st.slider("사고 강도(S)", 1, 5, 3)

risk_score = frequency * severity

# 결과 출력
if risk_score >= 15:
    st.error(f"위험 점수: {risk_score}점 (고위험 - 즉시 조치 필요)")
elif risk_score >= 8:
    st.warning(f"위험 점수: {risk_score}점 (중위험 - 개선 권고)")
else:
    st.success(f"위험 점수: {risk_score}점 (저위험 - 주의)")

# 4. 제출 버튼
if st.button("위험성평가 보고서 제출"):
    if user_name and location and hazard_desc:
        st.balloons()
        st.success("성공적으로 접수되었습니다. 안전한 현장을 만들어주셔서 감사합니다!")
    else:
        st.error("성명, 장소, 내용은 필수 입력 사항입니다.")
