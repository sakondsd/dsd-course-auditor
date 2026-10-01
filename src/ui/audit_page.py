import streamlit as st
from src.logic import data_manager, ai_auditor, doc_generator

# ข้อมูลตัวอย่างทั้ง 3 หลักสูตร
EXAMPLES = {
    "air": {
        "label": "❄️ ช่างแอร์",
        "course_name": "การติดตั้งเครื่องปรับอากาศภายในบ้านและการพาณิชย์",
        "job_title": "ช่างเครื่องปรับอากาศในบ้านและการพาณิชย์ขนาดเล็ก",
        "duration": 18,
        "topics": [
            "ความปลอดภัยในการใช้สารทำความเย็น",
            "การใช้เครื่องมือทางไฟฟ้าและช่างแอร์",
            "การติดตั้งคอยล์เย็นและคอยล์ร้อน",
            "การบานแฟร์และการเชื่อมท่อทองแดง",
            "การทำระบบสุญญากาศและการเติมน้ำยาแอร์"
        ]
    },
    "electric": {
        "label": "⚡ ช่างไฟฟ้า",
        "course_name": "การเดินสายไฟฟ้าภายในอาคารด้วยท่อร้อยสาย",
        "job_title": "ช่างไฟฟ้าภายในอาคาร ระดับ 1",
        "duration": 30,
        "topics": [
            "ความปลอดภัยและกฎหมายที่เกี่ยวข้อง",
            "การเลือกใช้สายไฟและท่อร้อยสาย",
            "การตัด ดัด และติดตั้งท่อร้อยสายไฟ",
            "การร้อยสายและต่อสายไฟ",
            "การตรวจสอบและทดสอบวงจร"
        ]
    },
    "weld": {
        "label": "🔧 ช่างเชื่อม",
        "course_name": "การเชื่อมอาร์กโลหะด้วยมือ (SMAW)",
        "job_title": "ช่างเชื่อมอาร์กโลหะด้วยมือ ระดับ 1",
        "duration": 24,
        "topics": [
            "ความปลอดภัยในการเชื่อม",
            "หลักการเชื่อมอาร์กโลหะด้วยมือ",
            "การปรับตั้งกระแสไฟและเลือกใช้ลวดเชื่อม",
            "เทคนิคการเชื่อมท่าราบและท่าขนานจาน",
            "การตรวจสอบรอยเชื่อมเบื้องต้น"
        ]
    }
}


def load_example(key: str):
    """โหลดข้อมูลตัวอย่างลงใน session state"""
    ex = EXAMPLES[key]
    st.session_state['course_name_input'] = ex["course_name"]
    st.session_state['job_title_input']   = ex["job_title"]
    st.session_state['duration_input']    = ex["duration"]
    st.session_state['topic_list']        = ex["topics"]
    for i, t in enumerate(ex["topics"]):
        st.session_state[f"topic_input_{i}"] = t


def render():
    # ===============================================================
    # CSS สำหรับ Layout ที่สวยงาม
    # ===============================================================
    st.markdown("""
    <style>
    /* Hero banner — เต็มความกว้าง ความสูงคงที่ */
    .hero-banner {
        width: 100%;
        height: 220px;
        object-fit: cover;
        object-position: center 40%;
        border-radius: 14px;
        display: block;
        margin-bottom: 0px;
    }
    /* Card style สำหรับส่วนฟอร์ม */
    .section-card {
        background: #f8fafd;
        border: 1px solid #e0e7ef;
        border-radius: 12px;
        padding: 20px 24px 10px 24px;
        margin-bottom: 18px;
    }
    /* หัว section แต่ละการ์ด */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1a3a5c;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    /* ปุ่ม example — ดูเหมือน chip */
    div[data-testid="stButton"] > button[kind="secondary"] {
        border-radius: 20px !important;
        font-size: 0.88rem !important;
    }
    /* ปุ่มหลัก */
    div[data-testid="stButton"] > button[kind="primary"] {
        border-radius: 10px !important;
        font-size: 1rem !important;
        padding: 0.6rem 2rem !important;
    }
    /* ลด padding หน้าจอเล็ก */
    @media (max-width: 768px) {
        .hero-banner { height: 140px; border-radius: 10px; }
        .section-card { padding: 14px 14px 6px 14px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ===============================================================
    # Hero Banner
    # ===============================================================
    st.markdown(
        '<img src="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158'
        '?q=80&w=1400&auto=format&fit=crop" class="hero-banner" alt="DSD Course Auditor">',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.title("🛡️ ระบบ AI ผู้ตรวจสอบหลักสูตร")
    st.caption("ตรวจสอบความสอดคล้องของหัวข้อวิชา ตามกฎระเบียบและมาตรฐานฝีมือแรงงาน กรมพัฒนาฝีมือแรงงาน")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ===============================================================
    # ส่วนตัวอย่าง
    # ===============================================================
    st.markdown("#### 💡 ทดลองด้วยข้อมูลตัวอย่าง")
    ex1, ex2, ex3 = st.columns(3)
    if ex1.button("❄️ ช่างแอร์", use_container_width=True):
        load_example("air"); st.rerun()
    if ex2.button("⚡ ช่างไฟฟ้า", use_container_width=True):
        load_example("electric"); st.rerun()
    if ex3.button("🔧 ช่างเชื่อม", use_container_width=True):
        load_example("weld"); st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.divider()

    # ===============================================================
    # ส่วนที่ 1: ข้อมูลหลักสูตร
    # ===============================================================
    st.markdown("### 1. ข้อมูลหลักสูตร")

    # กำหนดค่าเริ่มต้น duration
    if "duration_input" not in st.session_state:
        st.session_state["duration_input"] = 6

    course_name = st.text_input(
        "ชื่อหลักสูตร (Course Name)",
        key="course_name_input",
        placeholder="เช่น การติดตั้งระบบไฟฟ้าเบื้องต้น สำหรับอาคารพาณิชย์และโรงงานอุตสาหกรรมขนาดเล็ก"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        job_title = st.text_input(
            "ตำแหน่งผู้เข้าฝึก (Job Title)",
            key="job_title_input",
            placeholder="เช่น ช่างไฟฟ้าภายในอาคาร ระดับ 1"
        )
    with col2:
        duration = st.number_input(
            "ชั่วโมงฝึก (Hours)",
            key="duration_input",
            min_value=1,
            step=1
        )

    st.divider()

    # ===============================================================
    # ส่วนที่ 2: หัวข้อวิชา
    # ===============================================================
    st.markdown("### 2. หัวข้อวิชาที่ต้องการตรวจสอบ")

    if 'topic_list' not in st.session_state:
        st.session_state['topic_list'] = ["ความปลอดภัยในการทำงาน", ""]

    topics_to_remove = []
    for i, topic in enumerate(st.session_state['topic_list']):
        c1, c2 = st.columns([10, 1])
        with c1:
            st.session_state['topic_list'][i] = st.text_input(
                f"หัวข้อที่ {i+1}",
                value=topic,
                key=f"topic_input_{i}",
                placeholder="กรอกชื่อหัวข้อวิชา..."
            )
        with c2:
            if len(st.session_state['topic_list']) > 1:
                st.write(""); st.write("")
                if st.button("🗑️", key=f"del_btn_{i}", help="ลบหัวข้อนี้"):
                    topics_to_remove.append(i)

    if topics_to_remove:
        for index in sorted(topics_to_remove, reverse=True):
            st.session_state['topic_list'].pop(index)
        st.rerun()

    if st.button("➕ เพิ่มหัวข้อวิชา"):
        st.session_state['topic_list'].append("")
        st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ===============================================================
    # ส่วนที่ 3: ปุ่มตรวจสอบ
    # ===============================================================
    if st.button("🚀 เริ่มการตรวจสอบ (Start Audit)", type="primary", use_container_width=True):
        clean_topics = [t.strip() for t in st.session_state['topic_list'] if t.strip()]

        if not job_title or not course_name or not clean_topics:
            st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน: ชื่อหลักสูตร, ตำแหน่ง และหัวข้อวิชา")
        else:
            with st.spinner("🔍 AI กำลังค้นหากฎและตรวจสอบความถูกต้อง..."):
                topics_str = "\n".join([f"- {t}" for t in clean_topics])
                query = f"{job_title} {course_name} {topics_str}"
                related_rules = data_manager.search_rules(query)

                if not related_rules:
                    st.error("❌ ไม่พบกฎที่เกี่ยวข้องใน Database (กรุณาไปที่เมนู Admin เพื่อเพิ่มกฎก่อน)")
                else:
                    result_text = ai_auditor.audit_course_structure(
                        job_title, course_name, duration, topics_str, related_rules
                    )
                    st.markdown(result_text)

                    doc_file = doc_generator.create_verification_report(result_text)
                    st.download_button(
                        label="📥 ดาวน์โหลดรายงาน (.docx)",
                        data=doc_file,
                        file_name=f"Audit_{course_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )