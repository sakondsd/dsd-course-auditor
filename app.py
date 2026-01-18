import streamlit as st
from src.ui import audit_page, admin_page

# 1. ตั้งค่า Page Config (ต้องทำเป็นบรรทัดแรกสุดของ app.py)
st.set_page_config(
    page_title="DSD Course Auditor", 
    page_icon="🛡️",
    layout="wide"
)

# 2. สร้าง Sidebar Navigation
st.sidebar.title("เมนูหลัก")
page = st.sidebar.radio(
    "เลือกฟังก์ชันการทำงาน", 
    ["🔍 ตรวจสอบหลักสูตร (Auditor)", "⚙️ จัดการฐานข้อมูล (Admin)"]
)

st.sidebar.markdown("---")
st.sidebar.caption("DSD AI Auditor System v1.0")

# 3. เรียกใช้หน้าจอตามที่เลือก
if page == "🔍 ตรวจสอบหลักสูตร (Auditor)":
    audit_page.render()
elif page == "⚙️ จัดการฐานข้อมูล (Admin)":
    admin_page.render()