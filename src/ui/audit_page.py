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
    # CSS — โทนสี DSD: Navy Blue + Gold
    # ===============================================================
    st.markdown("""
    <style>
    /* ===== พื้นหลังหน้าจอหลัก ===== */
    .stApp {
        background-color: #f0f4f8;
    }

    /* ===== Hero Section รวมภาพ + ข้อความในกล่องเดียว ===== */
    .hero-section {
        width: 100%;
        height: 240px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 28px 32px;
        box-sizing: border-box;
        background-image:
            linear-gradient(to top, rgba(7,26,55,0.88) 0%, rgba(7,26,55,0.45) 55%, rgba(0,0,0,0.05) 100%),
            url("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=1400&auto=format&fit=crop");
        background-size: cover;
        background-position: center 35%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        border-left: 5px solid #c8a94a;
    }
    .hero-section h2 {
        color: #ffffff !important;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    .hero-section p {
        color: #dde8f8 !important;
        font-size: 0.92rem;
        margin: 0;
        text-shadow: 0 1px 4px rgba(0,0,0,0.4);
    }

    /* ===== ป้ายหัว section ===== */
    .section-header {
        background: linear-gradient(90deg, #0d2b55, #1a4a8a);
        color: #ffffff !important;
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 14px;
        display: inline-block;
        width: 100%;
        box-sizing: border-box;
    }

    /* ===== กล่องตัวอย่าง ===== */
    .example-box {
        background: #fff8e6;
        border: 1px solid #c8a94a;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 14px;
    }
    .example-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #7a5c00;
        margin-bottom: 8px;
    }

    /* ===== ปุ่มตัวอย่าง ===== */
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
        background-color: #ffffff !important;
        color: #0d2b55 !important;
        border: 2px solid #0d2b55 !important;
        border-radius: 24px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
        background-color: #0d2b55 !important;
        color: #ffffff !important;
    }

    /* ===== ปุ่ม primary (เริ่มตรวจสอบ) ===== */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0d2b55 0%, #1a4a8a 100%) !important;
        border: none !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #c8a94a 0%, #e8c96a 100%) !important;
        color: #0d2b55 !important;
    }

    /* ===== Input fields ===== */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        border: 1.5px solid #b0bfd0 !important;
        border-radius: 8px !important;
        background: #ffffff !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: #1a4a8a !important;
        box-shadow: 0 0 0 2px rgba(26,74,138,0.15) !important;
    }

    /* ===== label สี navy ===== */
    label[data-testid="stWidgetLabel"] p {
        color: #0d2b55 !important;
        font-weight: 600 !important;
    }

    /* ===== Divider ===== */
    hr {
        border-color: #c8a94a !important;
        opacity: 0.4;
    }

    /* ===== Responsive ===== */
    @media (max-width: 768px) {
        .hero-section { height: 160px; border-radius: 10px; }
        .hero-section h2 { font-size: 1.1rem; }
        .hero-section p { font-size: 0.78rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ===============================================================
    # Hero Section — รวมภาพ + ชื่อไว้ในกล่องเดียวกัน
    # ===============================================================
    st.markdown("""
    <div class="hero-section">
        <h2>🛡️ ระบบ AI ผู้ตรวจสอบหลักสูตร (Auditor)</h2>
        <p>ตรวจสอบความสอดคล้องของหัวข้อวิชา ตามกฎระเบียบและมาตรฐานฝีมือแรงงาน กรมพัฒนาฝีมือแรงงาน</p>
    </div>
    """, unsafe_allow_html=True)

    # ===============================================================
    # ส่วนตัวอย่าง
    # ===============================================================
    st.markdown('<div class="example-box"><div class="example-label">💡 ทดลองด้วยข้อมูลตัวอย่าง — กดเพื่อเติมข้อมูลอัตโนมัติ</div></div>', unsafe_allow_html=True)
    ex1, ex2, ex3 = st.columns(3)
    if ex1.button("❄️ ช่างแอร์", use_container_width=True):
        load_example("air"); st.rerun()
    if ex2.button("⚡ ช่างไฟฟ้า", use_container_width=True):
        load_example("electric"); st.rerun()
    if ex3.button("🔧 ช่างเชื่อม", use_container_width=True):
        load_example("weld"); st.rerun()

    st.divider()

    # ===============================================================
    # ส่วนที่ 1: ข้อมูลหลักสูตร
    # ===============================================================
    st.markdown('<div class="section-header">1. ข้อมูลหลักสูตร</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="section-header">2. หัวข้อวิชาที่ต้องการตรวจสอบ</div>', unsafe_allow_html=True)

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