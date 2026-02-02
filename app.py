import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- [메일 설정: 본인 정보로 수정] ---
def send_email(subject, body, image_data=None):
    sender_email = "gaeposangnok@gmail.com" 
    receiver_email = "gaeposangnok@gmail.com" 
    password = "mhczsijqwwagvaoi"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.attach(MIMEText(body))

    if image_data:
        # 사진 첨부 부분
        img = MIMEImage(image_data, name="safety_photo.jpg")
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# --- [앱 화면 구성] ---
st.set_page_config(page_title="안전제일: 위험성평가 참여 앱", layout="centered")

st.title("🚧 현장 위험성평가 참여")
st.write("현장의 위험 요인을 발견하면 즉시 등록해 주세요.")

with st.expander("👤 보고자 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("성명")
    with col2:
        department = st.selectbox("부서", ["시설팀", "관리팀", "경비팀", "미화팀"])

st.divider()
st.subheader("📍 위험 요인 상세")
location = st.text_input("위험 장소 (예: A라인 세척기 근처)")
hazard_desc = st.text_area("위험 요인 설명", placeholder="어떤 상황이 위험한가요?")

# 사진을 여러 장 선택할 수 있게 'accept_multiple_files=True'를 추가합니다.
uploaded_files = st.file_uploader("현장 사진 업로드 (여러 장 가능)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
st.divider()
st.subheader("📊 위험도 자가 평가")
col3, col4 = st.columns(2)
with col3:
    frequency = st.slider("발생 빈도(L)", 1, 5, 3)
with col4:
    severity = st.slider("사고 강도(S)", 1, 5, 3)
risk_score = frequency * severity

# --- [3. 제출 버튼 클릭 부분 - 여기를 확인하세요!] ---
if st.button("위험성평가 보고서 제출"):
    if user_name and location and hazard_desc:
        # 메일 본문 내용 정리
        email_body = (
            f"📢 신규 위험성평가 제보\n\n"
            f"보고자: {user_name} ({department})\n"
            f"장소: {location}\n"
            f"내용: {hazard_desc}\n"
            f"위험 점수: {risk_score}점\n"
            f"접수 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # 사진 데이터 가져오기
        img_bytes = None
        if uploaded_file is not None:
            img_bytes = uploaded_file.getvalue()
        
        try:
            send_email(f"⚠️ [위험제보] {location} - {user_name}님", email_body, img_bytes)
            st.balloons()
            st.success("사진과 함께 보고서가 관리자 메일로 전송되었습니다!")
        except Exception as e:
            st.error(f"전송 중 오류가 발생했습니다: {e}")
    else:
        st.error("성명, 장소, 내용은 필수 입력 사항입니다.")



