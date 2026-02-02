import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- [1. 메일 설정: 본인 정보로 꼭 수정!] ---
def send_email(subject, body, image_list=None):
    sender_email = "gaeposangnok@gmail.com" 
    receiver_email = "ks525@kakao.com.com, get004@naver.com" # 여러 명 쉼표로 구분
    password = "mhczsijqwwagvaoi"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.attach(MIMEText(body))

    if image_list:
        for i, img_data in enumerate(image_list):
            img = MIMEImage(img_data, name=f"safety_photo_{i+1}.jpg")
            msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# --- [2. 앱 화면 구성] ---
st.set_page_config(page_title="안전제일: 위험성평가 참여 앱", page_icon="⛑️", layout="centered")

st.title("🚧 현장 위험성평가 참여")
st.write("현장의 위험 요인을 발견하면 즉시 등록해 주세요.")

# 보고자 정보
with st.expander("👤 보고자 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("성명")
    with col2:
        # 부서 목록 수정 반영
        department = st.selectbox("부서", ["시설팀", "관리팀", "미화팀", "경비팀"])

# 위험 상세 정보
st.divider()
st.subheader("📍 위험 요인 상세")
location = st.text_input("위험 장소 (예: A라인 세척기 근처)")
hazard_desc = st.text_area("위험 요인 설명", placeholder="어떤 상황이 위험한가요?")
uploaded_files = st.file_uploader("현장 사진 업로드 (여러 장 가능)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# --- [3. 다시 추가한 위험도 계산기] ---
st.divider()
st.subheader("📊 위험도 자가 평가")
st.info("빈도(L)와 강도(S)를 선택하면 위험 점수가 자동으로 계산됩니다.")

col3, col4 = st.columns(2)
with col3:
    frequency = st.slider("발생 빈도(L)", 1, 5, 3) # 1~5점 사이 선택
with col4:
    severity = st.slider("사고 강도(S)", 1, 4, 3)  # 1~5점 사이 선택

risk_score = frequency * severity # 점수 계산

# 위험도에 따른 경고 메시지 표시
if risk_score >= 15:
    st.error(f"⚠️ 현재 위험 점수: {risk_score}점 (고위험 - 즉시 조치 필요)")
elif risk_score >= 8:
    st.warning(f"⚠️ 현재 위험 점수: {risk_score}점 (중위험 - 개선 권고)")
else:
    st.success(f"✅ 현재 위험 점수: {risk_score}점 (저위험 - 주의)")

# --- [4. 제출 버튼 및 메일 발송] ---
if st.button("위험성평가 보고서 제출"):
    if user_name and location and hazard_desc:
        # 이메일에 들어갈 내용 정리
        email_body = (
            f"📢 신규 위험성평가 제보가 접수되었습니다.\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 보고자: {user_name} ({department})\n"
            f"📍 장소: {location}\n"
            f"📝 내용: {hazard_desc}\n\n"
            f"📊 위험도 평가 결과\n"
            f"- 발생 빈도(L): {frequency}점\n"
            f"- 사고 강도(S): {severity}점\n"
            f"🔥 최종 위험 점수: {risk_score}점\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"접수 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        img_bytes_list = []
        for f in uploaded_files:
            img_bytes_list.append(f.getvalue())
        
        try:
            send_email(f"⚠️ [위험제보] {location} - {user_name}님", email_body, img_bytes_list)
            st.balloons()
            st.success("성공적으로 접수되었습니다! 위험도 점수까지 관리자에게 전송되었습니다.")
        except Exception as e:
            st.error(f"전송 중 오류가 발생했습니다: {e}")
    else:
        st.error("성명, 장소, 내용은 필수 입력 사항입니다.")




