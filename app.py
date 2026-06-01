import streamlit as st
from google import genai
import os
import time
import cv2

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

# 3. Technical Core Engines Configuration (Frame Extraction)
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
    elif not uploaded_file:
        st.warning("Please upload a local MP4 file to run the analysis pipeline.")
    else:
        video_path = "temp_video.mp4"
        try:
            client = genai.Client(api_key=api_key.strip())
            
            with st.spinner("📦 Staging uploaded video file onto server..."):
                with open(video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
            with st.spinner("🤖 Uploading asset to AI Sandbox..."):
                video_file = client.files.upload(file=video_path)
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = client.files.get(name=video_file.name)
                
                if video_file.state.name == "FAILED":
                    raise Exception("Multimodal processing pipeline failed inside AI Sandbox.")

            with st.spinner("📊 Extracting tactical video frames via OpenCV engine..."):
                frame_2s = extract_video_frame(video_path, 2)
                frame_5s = extract_video_frame(video_path, 5)

            with st.spinner("🧠 Analyzing audiovisual spectrum against Campaign Brief..."):
                system_prompt = """
                You are the Core AI Engine of the FansFormers Video Assessment Tool, an expert system specializing in YouTube video ad optimization based on FansFormers GAME Creative Best Practices. Your job is to analyze the provided video content (visual frames, audio, and transcript) against the FansFormers GAME Framework, while heavily adjusting your analysis weights based on the user's provided Campaign Brief and Cultural Context.

                STRICT OUTPUT STRUCTURING RULE:
                You MUST wrap each section of your response exactly within the specified delimiter tags so the frontend parser can separate them into dashboard tabs.

                Use these exact tags:
                ===OVERVIEW_START===
                [Your overall performance assessment, xGoal breakdown table, and metric summaries]
                ===OVERVIEW_END===

                ===CREATIVE_START===
                [Actionable tasks for the Creative / Copywriter]
                ===CREATIVE_END===

                ===EDITOR_START===
                [Actionable tasks for the Video Editor]
                ===EDITOR_END===

                ===MOTION_START===
                [Actionable tasks for the Motion & Graphic Designer]
                ===MOTION_END===

                ===PRODUCER_START===
                [Strategic takeaways for the Producer / Director for future shoots]
                ===PRODUCER_END===

                CRITICAL REPORT CONTENT REQUIREMENTS:
                1. All text must be in ENGLISH.
                2. Do NOT mention Google or ABCD framework. Always refer to this as the FansFormers GAME Framework.
                3. Under the ===OVERVIEW_START=== section, you MUST generate a "FansFormers Strategic Positioning & Stopwatch Table" tracking exactly:
                   - Branding Presence (Start-End timestamps, Total Duration, Screen Area % estimate, and Awareness Benchmark check).
                   - Call to Action (CTA) Presence (Start-End timestamps, Total Duration, Delivery style - text vs verbal, and Action Stage Benchmark check).
                4. CONTEXT INTEGRATION RULE: You must cross-reference the video execution against the user's Brief and Context. Evaluate whether the pacing, vocabulary, and imagery fit the requested cultural event (e.g., Mundial) or target demographic. If there is a mismatch, penalize the xGoal score and output a clear "Contextual Drift Warning".
                
                ### THE FansFormers GAME FRAMEWORK DEFINITIONS

                1. [G] GRAB ATTENTION
                - Quick Pacing (First 5s): Look for 5 or more shot changes/visual cuts within the first 5 seconds.
                - Tight Framing: Evaluate if subjects/products are tightly framed/zoomed-in (essential for vertical Shorts formats).
                - Audio Power: Confirm presence of Voice (VO/Dialogue), Music, and Sound Effects.
                - See & Say Supers: On-screen text must match the spoken words exactly in the same frame.

                2. [A] ANCHOR BRANDING
                - Brand Visual (3+ Times): Branding (logo, product, packaging) must appear on at least 3 non-consecutive frames.
                - Brand Logo (Large): Check if the logo takes up at least 10% of the screen area.
                - Brand Mention (First 5s): Brand or generic product category name must be heard in audio within the first 4.99 seconds.

                3. [M] MAKE CONNECTION
                - Presence of People (Close-up): A human or animated character must take up at least 30% of the frame.
                - Visible Face (First 5s): At least one human face must be present in the first 5 seconds.
                - Product Interaction & Context: Talent must physically interact with the product in a relatable setting.

                4. [E] EXECUTE DIRECTION
                - Call-to-Action: Detect specific CTA phrases in both Supers (text) and Audio (speech).
                - Path to Purchase: Presence of a visual Search Bar or explicit mention of how/where to buy.
                - Purchase Incentive / Urgency: Explicit mentions of limited time, scarcity, or special offers.
                """

                user_context = f"Selected Intent Level: {intent_level}. Campaign Brief & Cultural Context Provided by Brand Manager: '{campaign_context}'."

                # Automated Retry Loop for 503 Spikes
                response = None
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[video_file, system_prompt, user_context]
                        )
                        break
                    except Exception as model_error:
                        err_str = str(model_error)
                        if "503" in err_str or "UNAVAILABLE" in err_str:
                            if attempt < 2:
                                time.sleep(4)
                                st.toast(f"⚠️ Server heavily congested. Retrying analysis block (Attempt {attempt + 2}/3)...")
                                continue
                        raise model_error
                
                raw_report = response.text
                
                # Dynamic extraction
                overview_data = extract_section(raw_report, "===OVERVIEW_START===", "===OVERVIEW_END===")
                creative_data = extract_section(raw_report, "===CREATIVE_START===", "===CREATIVE_END===")
                editor_data = extract_section(raw_report, "===EDITOR_START===", "===EDITOR_END===")
                motion_data = extract_section(raw_report, "===MOTION_START===", "===MOTION_END===")
                producer_data = extract_section(raw_report, "===PRODUCER_START===", "===PRODUCER_END===")
                
                st.session_state['analysis_done'] = True
                st.session_state['overview_data'] = overview_data
                st.session_state['creative_data'] = creative_data
                st.session_state['editor_data'] = editor_data
                st.session_state['motion_data'] = motion_data
                st.session_state['producer_data'] = producer_data
                st.session_state['f2s'] = frame_2s
                st.session_state['f5s'] = frame_5s
                
                st.rerun()

        except Exception as e:
            st.error(f"Execution Error during analysis pipeline: {str(e)}")
            if os.path.exists(video_path):
                os.remove(video_path)

# 6. Render Layout according to State (Empty State UX Solution)
if st.session_state.get('analysis_done', False):
    with tab_ov:
        st.markdown("### 🖼️ Visual Proofs (Extracted Kicks)")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.session_state['f2s'] is not None:
                st.image(st.session_state['f2s'], caption="The Hook Frame (00:02) - Pacing & Attention Check", use_container_width=True)
        with col_f2:
            if st.session_state['f5s'] is not None:
                st.image(st.session_state['f5s'], caption="The Identity Frame (00:05) - Early Branding & Face Check", use_container_width=True)
        st.divider()
        st.markdown(st.session_state['overview_data'])
        
    with tab_cr: st.markdown(st.session_state['creative_data'])
    with tab_ed: st.markdown(st.session_state['editor_data'])
    with tab_mo: st.markdown(st.session_state['motion_data'])
    with tab_pr: st.markdown(st.session_state['producer_data'])
else:
    msg = "<div class='info-box'><p class='info-text'><strong>No match analysis loaded yet.</strong> Please configure your access key, select a video asset source above, and hit <b>'Run FansFormers Analysis'</b> to generate your proprietary tactical dashboard report.</p></div>"
    with tab_ov: st.markdown(msg, unsafe_allow_html=True)
    with tab_cr: st.markdown(msg, unsafe_allow_html=True)
    with tab_ed: st.markdown(msg, unsafe_allow_html=True)
    with tab_mo: st.markdown(msg, unsafe_allow_html=True)
    with tab_pr: st.markdown(msg, unsafe_allow_html=True)
