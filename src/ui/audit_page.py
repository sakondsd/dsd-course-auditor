import streamlit as st
from src.logic import data_manager, ai_auditor, doc_generator

def render():
    # ภาพปก Hero Section
    st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=1200&auto=format&fit=crop", use_container_width=True)
    st.title("🛡️ ระบบ AI ผู้ตรวจสอบหลักสูตร (Auditor)")
    st.caption("ตรวจสอบความสอดคล้องของหัวข้อวิชา ตามกฎระเบียบและมาตรฐานฝีมือแรงงาน")

    # --- ส่วนที่ 1: ข้อมูลหลักสูตร ---
    st.subheader("1. ข้อมูลหลักสูตร")
    
    with st.expander("📝 โหลดข้อมูลตัวอย่างสำหรับทดสอบ"):
        ex1, ex2, ex3 = st.columns(3)
        if ex1.button("❄️ ช่างแอร์", use_container_width=True):
            st.session_state['course_name_input'] = "การติดตั้งเครื่องปรับอากาศภายในบ้านและการพาณิชย์"
            st.session_state['job_title_input'] = "ช่างเครื่องปรับอากาศในบ้านและการพาณิชย์ขนาดเล็ก"
            st.session_state['duration_input'] = 18
            example_topics = ["ความปลอดภัยในการใช้สารทำความเย็น", "การใช้เครื่องมือทางไฟฟ้าและช่างแอร์", "การติดตั้งคอยล์เย็นและคอยล์ร้อน", "การบานแฟร์และการเชื่อมท่อทองแดง", "การทำระบบสุญญากาศและการเติมน้ำยาแอร์"]
            st.session_state['topic_list'] = example_topics
            for i, t in enumerate(example_topics): st.session_state[f"topic_input_{i}"] = t
            st.rerun()
            
        if ex2.button("⚡ ช่างไฟฟ้า", use_container_width=True):
            st.session_state['course_name_input'] = "การเดินสายไฟฟ้าภายในอาคารด้วยท่อร้อยสาย"
            st.session_state['job_title_input'] = "ช่างไฟฟ้าภายในอาคาร ระดับ 1"
            st.session_state['duration_input'] = 30
            example_topics = ["ความปลอดภัยและกฎหมายที่เกี่ยวข้อง", "การเลือกใช้สายไฟและท่อร้อยสาย", "การตัด ดัด และติดตั้งท่อร้อยสายไฟ", "การร้อยสายและต่อสายไฟ", "การตรวจสอบและทดสอบวงจร"]
            st.session_state['topic_list'] = example_topics
            for i, t in enumerate(example_topics): st.session_state[f"topic_input_{i}"] = t
            st.rerun()
            
        if ex3.button("🔧 ช่างเชื่อม", use_container_width=True):
            st.session_state['course_name_input'] = "การเชื่อมอาร์กโลหะด้วยมือ (SMAW)"
            st.session_state['job_title_input'] = "ช่างเชื่อมอาร์กโลหะด้วยมือ ระดับ 1"
            st.session_state['duration_input'] = 24
            example_topics = ["ความปลอดภัยในการเชื่อม", "หลักการเชื่อมอาร์กโลหะด้วยมือ", "การปรับตั้งกระแสไฟและเลือกใช้ลวดเชื่อม", "เทคนิคการเชื่อมท่าราบและท่าขนานจาน", "การตรวจสอบรอยเชื่อมเบื้องต้น"]
            st.session_state['topic_list'] = example_topics
            for i, t in enumerate(example_topics): st.session_state[f"topic_input_{i}"] = t
            st.rerun()
    
    # กำหนดค่าเริ่มต้นให้กับ duration หากยังไม่มี
    if "duration_input" not in st.session_state:
        st.session_state["duration_input"] = 6

    # ✅ ปรับ Layout ใหม่: ชื่อหลักสูตรอยู่บนสุด (เต็มความกว้าง)
    course_name = st.text_input(
        "ชื่อหลักสูตร (Course Name)", 
        key="course_name_input",
        placeholder="เช่น การติดตั้งระบบไฟฟ้าเบื้องต้น สำหรับอาคารพาณิชย์และโรงงานอุตสาหกรรมขนาดเล็ก"
    )

    # บรรทัดที่ 2: แบ่งคอลัมน์สำหรับ ตำแหน่ง และ ชั่วโมง
    col1, col2 = st.columns([2, 1])
    with col1:
        job_title = st.text_input("ตำแหน่งผู้เข้าฝึก (Job Title)", key="job_title_input", placeholder="เช่น ช่างไฟฟ้าภายในอาคาร")
    with col2:
        duration = st.number_input("จำนวนชั่วโมงฝึก (Hours)", key="duration_input", min_value=1, step=1)

    # --- ส่วนที่ 2: หัวข้อวิชา (Dynamic List) ---
    st.subheader("2. หัวข้อวิชาที่ต้องการตรวจสอบ")

    # เริ่มต้น Session State สำหรับเก็บรายการหัวข้อ ถ้ายังไม่มี
    if 'topic_list' not in st.session_state:
        st.session_state['topic_list'] = ["ความปลอดภัยในการทำงาน", ""] # ค่าเริ่มต้น

    # วนลูปแสดงช่องกรอกตามจำนวนที่มีใน List
    topics_to_remove = []
    
    for i, topic in enumerate(st.session_state['topic_list']):
        c1, c2 = st.columns([6, 1])
        with c1:
            st.session_state['topic_list'][i] = st.text_input(
                f"หัวข้อที่ {i+1}", 
                value=topic, 
                key=f"topic_input_{i}",
                placeholder="กรอกชื่อหัวข้อวิชา..."
            )
        with c2:
            # ปุ่มลบ (ถ้ามีหัวข้อเดียวจะไม่ให้ลบ)
            if len(st.session_state['topic_list']) > 1:
                # ปรับ margin ปุ่มลบให้ตรงกับช่องกรอก (เพื่อความสวยงาม)
                st.write("") 
                st.write("") 
                if st.button("🗑️", key=f"del_btn_{i}", help="ลบหัวข้อนี้"):
                    topics_to_remove.append(i)

    # ลบรายการที่ถูกกดปุ่มลบ
    if topics_to_remove:
        for index in sorted(topics_to_remove, reverse=True):
            st.session_state['topic_list'].pop(index)
        st.rerun()

    # ปุ่มเพิ่มหัวข้อใหม่
    if st.button("➕ เพิ่มหัวข้อวิชา"):
        st.session_state['topic_list'].append("")
        st.rerun()

    st.markdown("---")

    # --- ส่วนที่ 3: ปุ่มสั่งงาน ---
    if st.button("🚀 เริ่มการตรวจสอบ (Start Audit)", type="primary"):
        # กรองหัวข้อว่างทิ้งไปก่อนส่ง
        clean_topics = [t.strip() for t in st.session_state['topic_list'] if t.strip()]

        if not job_title or not course_name or not clean_topics:
            st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน (ชื่อหลักสูตร, ตำแหน่ง และหัวข้อวิชา)")
        else:
            with st.spinner("🔍 AI กำลังค้นหากฎและตรวจสอบความถูกต้อง..."):
                # แปลง list หัวข้อเป็น string เพื่อใช้ค้นหา
                topics_str = "\n".join([f"- {t}" for t in clean_topics])
                
                # 1. ค้นหากฎที่เกี่ยวข้อง
                query = f"{job_title} {course_name} {topics_str}"
                related_rules = data_manager.search_rules(query)
                
                if not related_rules:
                    st.error("❌ ไม่พบกฎที่เกี่ยวข้องใน Database (กรุณาไปที่เมนู Admin เพื่อเพิ่มกฎก่อน)")
                else:
                    # 2. ส่งให้ AI ตรวจสอบ
                    result_text = ai_auditor.audit_course_structure(
                        job_title, 
                        course_name,
                        duration,
                        topics_str,
                        related_rules
                    )
                    
                    # 3. แสดงผลลัพธ์
                    st.markdown(result_text)
                    
                    # 4. ปุ่มดาวน์โหลด
                    doc_file = doc_generator.create_verification_report(result_text)
                    st.download_button(
                        label="📥 ดาวน์โหลดรายงาน (.docx)",
                        data=doc_file,
                        file_name=f"Audit_{course_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )