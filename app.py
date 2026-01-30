import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- [메일 설정 함수] ---
def send_email(subject, body, image_list=None):
    sender_email = "gaeposangnok@gmail.com" 
    receiver_email = "gaeposangnok@gmail.com, peterkim0525@naver.com" 
    password = "mhczsijqwwagvaoi"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.attach(MIMEText(body))

    # 사진 목록(image_list)에서 하나씩 꺼내서 메일에 붙임
    if image_list:
        for i, img_data in enumerate(image_list):
            img = MIMEImage(img_data, name=f"safety_photo_{i+1}.jpg")
            msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# --- [앱 화면] ---
st.set_page_config(page_title="안전제일: 위험성평가 참여 앱", layout="centered")
st.title("🚧 현장 위험성평가 참여")

user_name = st.text_input("성명")
department = st.selectbox("부서", ["시설팀", "관리팀", "미화팀", "경비팀"])
location = st.text_input("위험 장소")
hazard_desc = st.text_area("위험 요인 설명")

# [중요한 2번 부분!] 여러 장 허용 옵션 추가
uploaded_files = st.file_uploader("현장 사진 업로드 (여러 장 가능)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# --- [제출 로직] ---
if st.button("위험성평가 보고서 제출"):
    if user_name and location and hazard_desc:
        email_body = f"📢 신규 제보\n\n보고자: {user_name}\n장소: {location}\n내용: {hazard_desc}"
        
        # 올린 사진들을 몽땅 리스트에 담기
        img_bytes_list = []
        for f in uploaded_files:
            img_bytes_list.append(f.getvalue())
        
        try:
            send_email(f"⚠️ [위험제보] {location}", email_body, img_bytes_list)
            st.balloons()
            st.success(f"성공! 사진 {len(uploaded_files)}장이 전송되었습니다.")
        except Exception as e:
            st.error(f"전송 실패: {e}")

