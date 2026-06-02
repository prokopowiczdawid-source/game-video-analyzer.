import streamlit as st
from google import genai
import os
import time
import cv2
from fpdf import FPDF
import io

# 1. Premium FansFormers Responsive Theme Configuration
st.set_page_config(page_title="FansFormers GAME Video Analytics", page_icon="⚽", layout="wide")

# Advanced CSS injection for custom enterprise styling
st.markdown("""
    <style>
    /* Responsive title styling with high contrast */
    .main-title { font-size: 38px !important; font-weight: 800 !important; color: #F8FAFC !important; margin-bottom: 5px; }
    .sub-title { font-size: 16px !important; color: #94A3B8 !important; margin-bottom: 25px; }
    
    /* Modern sleek tab navigation styling */
    .stTabs [data-baseweb="tab"] { font-size: 15px !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 6px 6px 0px 0px; }
    .stTabs [data-baseweb="tab"]:hover { color: #38BDF8 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #1E293B !important; color: #38BDF8 !important; border-bottom: 2px solid #38BDF8 !important; }
    
    /* Custom information card styling */
    .info-box { background-color: #1E293B; border-left: 4px solid #38BDF8; padding: 15px; border-radius: 0 8px 8px 0; margin-bottom: 20px; }
    .info-text { color: #E2E8F0 !important; font-size: 14px; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Branding & Global Token Configuration
st.sidebar.header("🔑 Strategic Access")
api_key = st.sidebar.text_input("FansFormers API Key:", type="password", help="Enter your product key from AI Studio.")
st.sidebar.markdown("[Get Free API Key here](https://aistudio.google.com/)")

st.sidebar.divider()
st.sidebar.subheader("📈 Verified Business Impact")
st.sidebar.info("""
**Framework Efficacy Data:**
Optimizing video assets with the FansFormers creative guidelines delivers an average of **+31% to +38% improvement in sales lift and ROAS** compared to non-optimized ads.
""")

# Main Screen Header - Forced High Contrast Texts
st.markdown('<div class="main-title">⚽ FansFormers GAME Video Assessment & xGoal Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Predictive AI Creative Analytics powered by FansFormers Proprietary Best Practices</div>', unsafe_allow_html=True)

# 2. Control Center Card Container (UX Box alignment)
with st.container(border=True):
    st.markdown("### 🛠️ Strategic Control Center")
    cc_col1, cc_col2 = st.columns([1, 1])
    
    with cc_col1:
        uploaded_file = st.file_uploader("📂 Drag & Drop Video File (.mp4):", type=["mp4"])
        intent_level = st.selectbox(
            "🎯 Select Campaign Intent (Objective):",
            [
                "🔥 Stop the Scroll (Awareness Focus)",
                "🧠 Win the Mind (Consideration Focus)",
                "🎯 Close the Deal (Action Focus)"
            ]
        )

    with cc_col2:
        campaign_context = st.text_area(
            "📝 Campaign Brief & Cultural Context:", 
            placeholder="e.g., Mundial 2026 campaign, Target: Gen-Z football fans, Tone: High energy, Fast-paced food delivery app promotion.",
            height=125
        )
    
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run FansFormers Analysis", use_container_width=True)

st.divider()

# 3. Heavy Duty Enterprise PDF Generation Engine (10 Evidence Screenshots + Advanced Formatting)
def generate_pdf_report(overview, creative, editor, motion, producer, intent, frames_data):
    def safe_text(t):
        if not t: return ""
        t = t.replace("✅", "[PASSED]").replace("❌", "[FAILED]").replace("🔥", "[FOCUS]").replace("🧠", "[INFO]").replace("🎯", "[TARGET]")
        t = t.replace("—", "-").replace("–", "-").replace("•", "*").replace("°", " deg ").replace("`", "'")
        t = t.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        t = t.replace("**", "").replace("###", "").replace("##", "")
        return t.encode('latin-1', 'ignore').decode('latin-1')

    pdf = FPDF()
    if not frames_data:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "FansFormers GAME Report (Timeline Processing Fault)", ln=True)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output

    pdf.add_page()
    
    # Page 1: Elegant Corporate Cover & High-Level Summary
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 41, 59) 
    pdf.cell(0, 15, "FansFormers GAME Strategy Report", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(2, 132, 199)
    pdf.cell(0, 8, f"CAMPAIGN OBJECTIVE: {safe_text(intent).upper()}", ln=True, align="C")
    
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, f"Proprietary Video Intelligence System | Generated: {time.strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.line(10, 42, 200, 42)
    pdf.ln(8)
    
    # Render First Grid of Visual Evidence (First 4 frames - The Crucial First 10 Seconds)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "I. Visual Timeline Audit - Initial Hook & Anchor Phase", ln=True)
    pdf.ln(3)
    
    saved_paths = []
    try:
        for idx, item in enumerate(frames_data[:4]):
            t_path = f"temp_pdf_frame_{idx}.png"
            cv2.imwrite(t_path, cv2.cvtColor(item['img'], cv2.COLOR_RGB2BGR))
            saved_paths.append(t_path)
            
        c_y = pdf.get_y()
        if len(saved_paths) >= 2:
            pdf.image(saved_paths[0], x=12, y=c_y, w=88)
            pdf.image(saved_paths[1], x=110, y=c_y, w=88)
            pdf.set_y(c_y + 51)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(92, 5, safe_text(frames_data[0]['label']), ln=False, align="C")
            pdf.cell(100, 5, safe_text(frames_data[1]['label']), ln=True, align="C")
            pdf.ln(2)
        
        if len(saved_paths) >= 4:
            c_y2 = pdf.get_y()
            pdf.image(saved_paths[2], x=12, y=c_y2, w=88)
            pdf.image(saved_paths[3], x=110, y=c_y2, w=88)
            pdf.set_y(c_y2 + 51)
            pdf.cell(92, 5, safe_text(frames_data[2]['label']), ln=False, align="C")
            pdf.cell(100, 5, safe_text(frames_data[3]['label']), ln=True, align="C")
        
    except Exception as e:
        pdf.cell(0, 5, f"[Visual Track Suppressed: {str(e)}]", ln=True)
        
    for p in saved_paths:
        if os.path.exists(p): os.remove(p)

    pdf.add_page()
    
    # Render Second Grid of Visual Evidence (Next 4 frames - Execution Phase)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "II. Visual Timeline Audit - Content Mapping & CTA Phase", ln=True)
    pdf.ln(3)
    
    saved_paths2 = []
    try:
        for idx, item in enumerate(frames_data[4:8]):
            t_path = f"temp_pdf_frame_b_{idx}.png"
            cv2.imwrite(t_path, cv2.cvtColor(item['img'], cv2.COLOR_RGB2BGR))
            saved_paths2.append(t_path)
            
        c_y = pdf.get_y()
        if len(saved_paths2) >= 2:
            pdf.image(saved_paths2[0], x=12, y=c_y, w=88)
            pdf.image(saved_paths2[1], x=110, y=c_y, w=88)
            pdf.set_y(c_y + 51)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(92, 5, safe_text(frames_data[4]['label']), ln=False, align="C")
            pdf.cell(100, 5, safe_text(frames_data[5]['label']), ln=True, align="C")
            pdf.ln(2)
        
        if len(saved_paths2) >= 4:
            c_y2 = pdf.get_y()
            pdf.image(saved_paths2[2], x=12, y=c_y2, w=88)
            pdf.image(saved_paths2[3], x=110, y=c_y2, w=88)
            pdf.set_y(c_y2 + 51)
            pdf.cell(92, 5, safe_text(frames_data[6]['label']), ln=False, align="C")
            pdf.cell(100, 5, safe_text(frames_data[7]['label']), ln=True, align="C")
        
    except Exception as e:
        pdf.cell(0, 5, f"[Visual Track B Suppressed: {str(e)}]", ln=True)
        
    for p in saved_paths2:
        if os.path.exists(p): os.remove(p)

    pdf.add_page()
    
    # Render Last Grid (Final 2 frames - Outro Matrix)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "III. Visual Timeline Audit - Final Closing Real Estate", ln=True)
    pdf.ln(3)
    
    saved_paths3 = []
    try:
        for idx, item in enumerate(frames_data[8:10]):
            t_path = f"temp_pdf_frame_c_{idx}.png"
            cv2.imwrite(t_path, cv2.cvtColor(item['img'], cv2.COLOR_RGB2BGR))
            saved_paths3.append(t_path)
            
        c_y = pdf.get_y()
        if len(saved_paths3) >= 2:
            pdf.image(saved_paths3[0], x=12, y=c_y, w=88)
            pdf.image(saved_paths3[1], x=110, y=c_y, w=88)
            pdf.set_y(c_y + 51)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(92, 5, safe_text(frames_data[8]['label']), ln=False, align="C")
            pdf.cell(100, 5, safe_text(frames_data[9]['label']), ln=True, align="C")
            pdf.ln(5)
    except Exception as e:
        pdf.cell(0, 5, f"[Visual Track C Suppressed: {str(e)}]", ln=True)
        
    for p in saved_paths3:
        if os.path.exists(p): os.remove(p)

    sections = [
        ("Strategic Match Overview & Core Diagnostics", overview),
        ("Creative & Copywriting Deep-Dive Report", creative),
        ("Video Editor Tactical Cuts Timeline Blueprint", editor),
        ("Motion & Graphic Design High-Impact Guidelines", motion),
        ("Producer & Director Executive Takeaways", producer)
    ]
    
    for title, text in sections:
        if pdf.get_y() > 220:
            pdf.add_page()
            
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(2, 132, 199) 
        pdf.cell(0, 12, title, ln=True)
        pdf.ln(3)
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 65, 85)
        
        clean_section_text = safe_text(text)
        pdf.multi_cell(0, 6, clean_section_text)
        pdf.ln(5)
        
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# 4. Multimodal High-Speed Frame Processing Unit (10 Tactical Benchmarks)
def extract_tactical_timeline(video_path):
    timestamps = [0, 2, 5, 8, 11, 14, 17, 20, 24, 28]
    labels = [
        "00:00 - Initial Entry / Hook Frame",
        "00:02 - Brand Anchor / Early ID Check",
        "00:05 - Connection Frame / Face Real Estate",
        "00:08 - Problem Mapping / Context Validation",
        "00:11 - Solution Introduction / Formulation",
        "00:14 - Functional Benefit / Active Animation",
        "00:17 - Authority Check / Trust Endorsement",
        "00:20 - Audience Retention / Mid-Ad Pace",
        "00:24 - Conversion Phase / CTA Entry Point",
        "00:28 - Closing Asset / Final Brand Impression"
    ]
    
    extracted_set = []
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / fps
        
        for t, label in zip(timestamps, labels):
            target_sec = t if t < duration_sec else (duration_sec - 0.5)
            if target_sec < 0: target_sec = 0
            
            frame_id = int(fps * target_sec)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                extracted_set.append({'time': t
