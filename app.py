import streamlit as st
import yt_dlp
from google import genai
import os
import time
import cv2

# 1. Premium Dashboard Layout & Style Configuration (FansFormers Branding)
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
    st.markdown("### 🛠️ Control Center")
    cc_col1, cc_col2 = st.columns([2, 1])
    
    with cc_col1:
        source_type = st.radio("Choose Media Source Input:", ["YouTube Link", "Upload Local Video (MP4)"], horizontal=True)
        if source_type == "YouTube Link":
            video_url = st.text_input("🔗 Paste YouTube Video or Shorts URL:", placeholder="https://www.youtube.com/watch?v=...")
            uploaded_file = None
        else:
            uploaded_file = st.file_uploader("📂 Drag & Drop Video File (.mp4):", type=["mp4"])
            video_url = None

    with cc_col2:
        intent_level = st.selectbox(
            "🎯 Select Campaign Intent (Objective):",
            [
                "🔥 Stop the Scroll (Awareness Focus)",
                "🧠 Win the Mind (Consideration Focus)",
                "🎯 Close the Deal (Action Focus)"
            ]
        )
    
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Match Analysis", use_container_width=True)

st.divider()

# 3. Technical Core Engines Configuration
def download_youtube_video(url):
    ydl_opts = {
        'format': 'worst[ext=mp4]/worst',
        'outtmpl': 'temp_video.mp4',
        'overwrites': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "temp_video.mp4"

def extract_video_frame(video_path, seconds):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30
        frame_id = int(fps * seconds)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cap.release()
            return frame_rgb
        cap.release()
    except:
        pass
    return None

def extract_section(text, start_marker, end_marker):
    try:
        start_idx = text.find(start_marker)
        end_idx = text.find(end_marker)
        if start_idx != -1 and end_idx != -1:
            return text[start_idx + len(start_marker):end_idx].strip()
        return text
    except:
        return text

# 4. Interactive Tabs Setup (Handles both Empty State & Filled State)
tab_ov, tab_cr, tab_ed, tab_mo, tab_pr = st.tabs([
    "📊 Match Overview", 
    "✍️ Creative / Copywriter", 
    "🎬 Video Editor", 
    "🎨 Motion Designer", 
    "📢 Producer / Director"
])

# 5. Pipeline Logic Integration
if run_btn:
    if not api_key:
        st.error("Missing API Authentication. Please insert your API Key in the sidebar.")
    elif source_type == "YouTube Link" and not video_url:
        st.warning("Please enter a valid YouTube URL.")
    elif source_type == "Upload Local Video (MP4)" and not uploaded_file:
        st.warning("Please upload a local MP4 file.")
    else:
        video_path = None
        try:
            client = genai.Client(api_key=api_key.strip())
            
            if source_type == "YouTube Link":
                with st.spinner("📦 Fetching video stream from YouTube source..."):
                    video_path = download_youtube_video(video_url)
            else:
                with st.spinner("📦 Staging uploaded video file onto server..."):
                    video_path = "temp_video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
            with st.spinner("🤖 Uploading asset to AI Sandbox..."):
                video_file = client.files.upload(file=video_path)
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = client.files.get(name=video_file.name)
                
                if video_file.state.name == "FAILED":
                    raise Exception("Multimodal processing pipeline failed inside AI Sandbox.")

            with st.spinner("📊 Extracting video proof frames via OpenCV engine..."):
                frame_2s = extract_video_frame(video_path, 2)
                frame_5s = extract_video_frame(video_path, 5)

            with st.spinner("🧠 Analyzing audiovisual spectrum. Scoring xGoal metrics..."):
                system_prompt = """
                You are the Core AI Engine of the FansFormers Video Assessment Tool, an expert system specializing in YouTube video ad optimization based on FansFormers GAME Creative Best Practices. Your job is to analyze the provided video content (visual frames, audio, and transcript) against the FansFormers GAME Framework and output a highly actionable, role-based "Match Report" with an Expected Goals (xGoal) probability score from 0 to 100.

                STRICT OUTPUT STRUCTURING RULE:
                You MUST wrap each section of your response exactly within the specified delimiter tags so the frontend parser can separate them into dashboard tabs.

                Use these exact tags:
                ===OVERVIEW_START===
                [Your overall performance assessment, xGoal breakdown table, and metric summaries]
                ===OVERVIEW_END===

                ===
