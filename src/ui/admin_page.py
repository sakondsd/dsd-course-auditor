import streamlit as st
import os
import time
import PyPDF2
# ✅ ต้อง Import จาก ai_auditor (เพราะเราเปลี่ยนชื่อไฟล์ใน Project ใหม่)
from src.logic.ai_auditor import extract_rules_from_pdf_text as extract_rules_from_text
from src.logic.data_manager import rebuild_knowledge_base

KB_FOLDER = "knowledge_base"
ADMIN_PASSWORD = "12345"  # 🔑 รหัสผ่าน (เปลี่ยนได้)

def render():
    st.header("🛠️ Admin Panel: จัดการกฎระเบียบ")

    # =========================================
    # 🔐 0. ส่วนตรวจสอบรหัสผ่าน (Password Check)
    # =========================================
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.info("🔒 หน้านี้จำกัดสิทธิ์เฉพาะผู้ดูแลระบบ")
        col1, col2 = st.columns([3, 1])
        with col1:
            password_input = st.text_input("กรุณาใส่รหัสผ่าน:", type="password", label_visibility="collapsed")
        with col2:
            if st.button("เข้าสู่ระบบ"):
                if password_input == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("เข้าสู่ระบบสำเร็จ!")
                    st.rerun()
                else:
                    st.error("❌ รหัสผ่านไม่ถูกต้อง")
        return 

    # ปุ่ม Logout (แสดงมุมขวาบน)
    col_logout = st.columns([8, 2])
    with col_logout[1]:
        if st.button("ออกจากระบบ (Logout)", type="secondary"):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.divider()

    # =========================================
    # 1. ✨ เพิ่มกฎใหม่ (AI Extractor)
    # =========================================
    st.subheader("1. ✨ เพิ่มกฎใหม่ (AI Extractor)")
    st.info("เริ่มที่นี่! อัปโหลดไฟล์ PDF/TXT เพื่อให้ AI แกะเป็นกฎ แล้วบันทึกลงระบบ")
    
    uploaded_file = st.file_uploader("เลือกไฟล์ต้นฉบับ", type=["pdf", "txt"], key="rule_extractor")
    
    if uploaded_file:
        if uploaded_file.size == 0:
            st.error("⚠️ ไฟล์ว่างเปล่า")
        else:
            file_type = uploaded_file.name.split('.')[-1].lower()
            if st.button(f"✨ แปลงไฟล์ {file_type.upper()} เป็นกฎ"):
                with st.spinner("AI กำลังอ่านและแกะกฎ..."):
                    raw_text = ""
                    try:
                        # กรณี PDF
                        if file_type == 'pdf':
                            reader = PyPDF2.PdfReader(uploaded_file)
                            raw_text = "".join([p.extract_text() for p in reader.pages])
                        
                        # กรณี TXT
                        elif file_type == 'txt':
                            bytes_data = uploaded_file.getvalue()
                            try: 
                                raw_text = bytes_data.decode("utf-8")
                            except: 
                                raw_text = bytes_data.decode("cp874") # รองรับภาษาไทย Windows
                        
                        if raw_text:
                            # เรียกใช้ AI Extract Rule
                            rules = extract_rules_from_text(raw_text)
                            st.session_state["draft_rules"] = rules
                            st.session_state["draft_filename"] = f"กฎ_{uploaded_file.name}.txt"
                            st.success("✅ แกะกฎสำเร็จ! กรุณาตรวจสอบและกดบันทึกด้านล่าง")
                        else:
                            st.warning("อ่านไฟล์ได้ แต่ไม่พบข้อความข้างใน")

                    except Exception as e:
                        st.error(f"Error: {e}")

    # ส่วนตรวจสอบและบันทึก (แสดงต่อจากข้อ 1 ทันทีเมื่อมีข้อมูลใน Session)
    if "draft_rules" in st.session_state:
        st.markdown("#### 📝 ตรวจสอบและบันทึก")
        edited_rules = st.text_area("เนื้อหากฎ (แก้ไขได้):", st.session_state["draft_rules"], height=300)
        
        # ลบ .txt ซ้ำซ้อนออกถ้ามี
        default_name = st.session_state.get("draft_filename", "rules.txt").replace(".txt.txt", ".txt")
        save_name = st.text_input("ตั้งชื่อไฟล์ที่จะบันทึก:", value=default_name)

        if st.button("💾 บันทึกลงระบบ"):
            if not save_name.endswith('.txt'): save_name += ".txt"
            
            if not os.path.exists(KB_FOLDER): os.makedirs(KB_FOLDER)
            
            save_path = os.path.join(KB_FOLDER, save_name)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(edited_rules)
            
            st.toast(f"บันทึกไฟล์ {save_name} เรียบร้อย!", icon="✅")
            time.sleep(1)
            
            # ล้างค่า session เพื่อให้พร้อมทำไฟล์ต่อไป
            del st.session_state["draft_rules"]
            if "draft_filename" in st.session_state: del st.session_state["draft_filename"]
            st.rerun()

    st.markdown("---")

    # =========================================
    # 2. 📂 จัดการไฟล์กฎระเบียบ
    # =========================================
    st.subheader("2. 📂 จัดการไฟล์กฎระเบียบ")
    
    if not os.path.exists(KB_FOLDER): os.makedirs(KB_FOLDER)
    files = [f for f in os.listdir(KB_FOLDER) if f.endswith(".txt")]

    if not files:
        st.warning("ยังไม่มีไฟล์กฎระเบียบในระบบ")
    else:
        st.write(f"มีไฟล์ทั้งหมด {len(files)} ไฟล์ (กดลบไฟล์ที่ไม่ต้องการได้ที่นี่):")
        
        # แสดงรายการไฟล์แบบตารางย่อยๆ
        for f in files:
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.text(f"📄 {f}")
            with col2:
                if st.button("🗑️ ลบ", key=f"del_{f}"):
                    try:
                        os.remove(os.path.join(KB_FOLDER, f))
                        st.toast(f"ลบไฟล์ {f} เรียบร้อย!", icon="✅")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"ลบไม่สำเร็จ: {e}")

    st.markdown("---")

    # =========================================
    # 3. 🧠 อัปเดตสมอง AI
    # =========================================
    st.subheader("3. 🧠 อัปเดตสมอง AI")
    st.info("⚠️ ขั้นตอนสุดท้าย! เมื่อเพิ่มหรือลบไฟล์เสร็จแล้ว ต้องกดปุ่มนี้เสมอเพื่อให้ AI จดจำข้อมูลล่าสุด")
    
    if st.button("🔄 Re-index Knowledge Base (Sync)", type="primary"):
        with st.spinner("กำลังอ่านไฟล์ทั้งหมดและสร้างสมองใหม่..."):
            msg = rebuild_knowledge_base()
            if "✅" in msg:
                st.success(msg)
            else:
                st.error(msg)