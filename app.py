import streamlit as st
import yt_dlp
from google import genai
import os
import time
import cv2

# 1. Premium Dashboard Layout & Style Configuration (FansFormers Branding)
st.set_page_config(page_title="FansFormers GAME Video Analytics", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 38px !important; font-weight: 800 !important; color: #0F172A; margin-bottom: 5px; }
    .sub-title { font-size: 16px !important; color: #475569; margin-bottom: 30px; }
    .stTabs [data-baseweb="tab"] { font-size: 15px !important; font-weight: 600 !important; padding: 12px 24px !important; }
    .metric-card { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ FansFormers GAME Video Assessment & xGoal Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Predictive AI Creative Analytics powered by FansFormers Proprietary Best Practices</div>', unsafe_allow_html=True)

# 2. Sidebar - Global Authentication & Business Benchmark
st.sidebar.header("🔑 Authentication")
api_key = st.sidebar.text_input("API Key:", type="password", help="Insert your product key from AI Studio.")
st.sidebar.markdown("[Get Free API Key here](https://aistudio.google.com/)")

st.sidebar.divider()
st.sidebar.subheader("📈 Verified Business Impact")
st.sidebar.info("""
**Framework Efficacy Data:**
Optimizing video assets with the FansFormers creative guidelines delivers an average of **+31% to +38% improvement in sales lift and ROAS** compared to non-optimized ads.
""")

# 3. Main Input Control Center
col1, col2 = st.columns([2, 1])

with col1:
    source_type = st.radio("Choose Media Source:", ["YouTube Link", "Upload Local Video (MP4)"], horizontal=True)
    if source_type == "YouTube Link":
        video_url = st.text_input("🔗 Paste YouTube Video or Shorts URL:", placeholder="https://www.youtube.com/watch?v=...")
        uploaded_file = None
    else:
        uploaded_file = st.file_uploader("📂 Drag & Drop Video File (.mp4):", type=["mp4"])
        video_url = None

with col2:
    intent_level = st.selectbox(
        "🎯 Select Campaign Intent (Objective):",
        [
            "🔥 Stop the Scroll (Awareness Focus)",
            "🧠 Win the Mind (Consideration Focus)",
            "🎯 Close the Deal (Action Focus)"
        ]
    )

# 4. Core Technical Functions (Video Fetching & Frame Extraction)
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
        if fps == 0: 
            fps = 30
        frame_id = int(fps * seconds)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cap.release()
            return frame_rgb
        cap.release()
    except Exception as e:
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

# 5. Pipeline Execution
if st.button("🚀 Run Match Analysis"):
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

                ===CREATIVE_START===
                [Actionable tasks for the Creative / Copywriter]
                ===CRECREATIVE_END===

                ===EDITOR_START===
                [Actionable tasks for the Video Editor]
                ===EDITOR_END===

                ===MOTION_START===
                [Actionable tasks for the Motion & Graphic Designer]
                ===MOTION_END===

                ===PRODUCER_START===
                [Strategic takeaways for the Producer / Director for future shoots]
                ===PRODUCER_END===

                CRITICAL CONTENT RULES:
                1. All text must be in ENGLISH.
                2. Rely strictly on technical metrics (e.g., Logo >10% area, Pacing 5 cuts in 5s, Visible Face first 5s).
                3. Use structured tables and bold numbers to make it look like a premium executive report.
                4. For each negative finding, clearly state the Gap, Impact, and Potential xGoal Lift (e.g., +15 xGoal Lift).
                5. Do NOT mention Google or ABCD framework. Always refer to this as the FansFormers GAME Framework.
                
                ### THE FansFormers GAME FRAMEWORK DEFINITIONS

                1. [G] GRAB ATTENTION
                - Quick Pacing (First 5s): Look for 5 or more shot changes/visual cuts within the first 5 seconds.
                - Tight Framing: Evaluate if subjects/products are tightly framed/zoomed-in (essential for YouTube Shorts).
                - Audio Power: Confirm presence of Voice (VO/Dialogue), Music, and Sound Effects.
                - See & Say Supers: On-screen text must match the spoken words exactly in the same frame.

                2. [A] ANCHOR BRANDING
                - Brand Visual (3+ Times): Branding (logo, product, packaging) must appear on at least 3 non-consecutive frames.
                - Brand Logo (Large): Check if the logo takes up at least 10% of the screen area.
                - Brand Mention (First 5s): Brand or generic product category name must be heard in audio within the first 4.99 seconds.
                - Product Focus: Ensure all audiovisual elements support the product/service narrative without distractions.

                Note: The primary goal for Awareness ("Stop the Scroll") is to get noticed so the brand/product are remembered. Third-party meta-analysis confirms FansFormers GAME optimization yields an average +31-38% lift in sales and ROAS.

                3. [M] MAKE CONNECTION
                - Presence of People (Close-up): A human or animated character must take up at least 30% of the frame.
                - Visible Face (First 5s): At least one human/animated face must be present in the first 5 seconds.
                - Product Interaction & Context: Talent must physically interact with the product in a relatable, real-world setting.
                - Expression of Benefit: Look for explicit verbal or visual demonstration of a tangible, problem-solving benefit.

                4. [E] EXECUTE DIRECTION
                - Call-to-Action: Detect specific CTA phrases in both Supers (text) and Audio (speech).
                - Path to Purchase: Presence of a visual Search Bar or explicit mention of how/where to buy.
                - Purchase Incentive / Urgency: Explicit mentions of limited time, scarcity, or special offers (excluding fine print).
                """

                user_context = f"Selected Strategy/Intent Level: {intent_level}."

                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[video_file, system_prompt, user_context]
                )
                
                raw_report = response.text
                
                # Parsing blocks
                overview_data = extract_section(raw_report, "===OVERVIEW_START===", "===OVERVIEW_END===")
                creative_data = extract_section(raw_report, "===CREATIVE_START===", "===CREATIVE_END===")
                editor_data = extract_section(raw_report, "===EDITOR_START===", "===EDITOR_END===")
                motion_data = extract_section(raw_report, "===MOTION_START===", "===MOTION_END===")
                producer_data = extract_section(raw_report, "===PRODUCER_START===", "===PRODUCER_END===")
                
                st.success("⚡ Match Analysis Completed Successfully!")
                
                # Creating Interactive Tab-Based Premium Dashboard
                tab_ov, tab_cr, tab_ed, tab_mo, tab_pr = st.tabs([
                    "📊 Match Overview", 
                    "✍️ Creative / Copywriter", 
                    "🎬 Video Editor", 
                    "🎨 Motion Designer", 
                    "📢 Producer / Director"
                ])
                
                with tab_ov:
                    st.markdown("### 🖼️ Visual Proofs (Extracted Kicks)")
                    col_f1, col_f2 = st.columns(2)
                    with col_f1:
                        if frame_2s is not None:
                            st.image(frame_2s, caption="The Hook Frame (00:02) - Pacing & Attention Check", use_container_width=True)
                    with col_f2:
                        if frame_5s is not None:
                            st.image(frame_5s, caption="The Identity Frame (00:05) - Early Branding & Face Check", use_container_width=True)
                    st.divider()
                    st.markdown(overview_data)
                    
                with tab_cr:
                    st.markdown(creative_data)
                with tab_ed:
                    st.markdown(editor_data)
                with tab_mo:
                    st.markdown(motion_data)
                with tab_pr:
                    st.markdown(producer_data)
                
                # Cleanup Storage Safely
                client.files.delete(name=video_file.name)
                if os.path.exists(video_path):
                    os.remove(video_path)
                    
        except Exception as e:
            st.error(f"Execution Error during analysis pipeline: {str(e)}")
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
