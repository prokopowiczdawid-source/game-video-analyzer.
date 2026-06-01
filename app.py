import streamlit as st
import yt_dlp
import google.generativeai as genai
import os
import time

# 1. Konfiguracja wyglądu aplikacji
st.set_page_config(page_title="GAME Video Assessment", page_icon="⚽", layout="wide")

st.title("⚽ GAME Video Assessment & xGoal Dashboard")
st.subheader("Analityka kreacji wideo YouTube w oparciu o standardy Google ABCD")

# 2. Sidebar - Miejsce na klucz API oraz instrukcję
st.sidebar.header("🔑 Autoryzacja")
api_key = st.sidebar.text_input("Wklej swój Gemini API Key:", type="password")
st.sidebar.markdown("""
[Skąd wziąć klucz?](https://aistudio.google.com/)
Logujesz się na Google AI Studio, klikasz **'Get API Key'**, generujesz go i wklejasz tutaj.
""")

st.sidebar.divider()
st.sidebar.info("Aplikacja analizuje obraz, dźwięk i tekst z linku YouTube, dopasowując go do wybranego celu twórczego.")

# 3. Główny formularz aplikacji
col1, col2 = st.columns([2, 1])

with col1:
    video_url = st.text_input("🔗 Link do publicznego filmu YouTube (Standard lub Shorts):", 
                              placeholder="https://www.youtube.com/watch?v=...")

with col2:
    intent_level = st.selectbox(
        "🎯 Wybierz cel / intencję filmu (Objective):",
        [
            "🔥 Stop the Scroll (Awareness Focus)",
            "🧠 Win the Mind (Consideration Focus)",
            "🎯 Close the Deal (Action Focus)"
        ]
    )

# 4. Funkcja do bezpiecznego pobierania wideo (tylko niska rozdzielczość na potrzeby AI)
def download_youtube_video(url):
    ydl_opts = {
        'format': 'worst[ext=mp4]/worst',  # Pobieramy najmniejszy plik mp4 z dźwiękiem, by oszczędzać czas i RAM
        'outtmpl': 'temp_video.mp4',
        'overwrites': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "temp_video.mp4"

# 5. Logika po kliknięciu przycisku analizy
if st.button("🚀 Uruchom Analizę Meczu (Run Analysis)"):
    if not api_key:
        st.error("Proszę podać Gemini API Key w panelu bocznym!")
    elif not video_url:
        st.warning("Proszę wkleić poprawny link do filmu YouTube.")
    else:
        try:
            # Konfiguracja klucza dla Google AI
            genai.configure(api_key=api_key)
            
            with st.spinner("Step 1/3: Pobieranie wideo z YouTube... (Może to zająć chwilę)"):
                video_path = download_youtube_video(video_url)
                
            with st.spinner("Step 2/3: Wysyłanie pliku do analizy multimodalnej AI..."):
                video_file = genai.upload_file(path=video_path)
                
                # Czekamy, aż Google przetworzy plik wideo w chmurze
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name == "FAILED":
                    raise Exception("Przetwarzanie pliku wideo przez AI nie powiodło się.")

            with st.spinner("Step 3/3: Generowanie raportu taktycznego xGoal..."):
                # Główny prompt systemowy ze specyfikacją
                system_prompt = """
                You are the Core AI Engine of the GAME Video Assessment Tool, an expert system specializing in YouTube video ad optimization based on Google's ABCD Creative Best Practices. Your job is to analyze the provided video content (visual frames, audio, and transcript) against the GAME Framework and output a highly actionable, role-based "Match Report" with an Expected Goals (xGoal) probability score from 0 to 100.

                STRICT RULES:
                1. All outputs must be in ENGLISH.
                2. Rely strictly on the technical definitions provided below. Do not generalize.
                3. Every negative finding must be translated into a role-based action plan with a "Potential xGoal Lift".

                ### THE GAME FRAMEWORK DEFINITIONS (Based on abcd.pdf)

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

                # Kontekst wybranego celu biznesowego przekazany do modelu
                user_context = f"Selected Objective: {intent_level}. Adjust evaluation weights based on this intent: 'Stop the Scroll' focuses heavily on [G] and early branding; 'Win the Mind' focuses on [M] and product value; 'Close the Deal' focuses on [E] and persistent CTA urgency."

                # Uruchomienie najnowszego modelu multimodalnego Gemini 1.5 Flash
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content([video_file, system_prompt, user_context])
                
                # Wyświetlenie gotowego raportu na ekranie
                st.success("Analiza zakończona sukcesem! Oto Twój Match Report:")
                st.markdown(response.text)
                
                # Czyszczenie pliku z serwera lokalnego
                genai.delete_file(video_file.name)
                if os.path.exists(video_path):
                    os.remove(video_path)
                    
        except Exception as e:
            st.error(f"Wystąpił błąd podczas analizy: {str(e)}")
            if os.path.exists("temp_video.mp4"):
                os.remove("temp_video.mp4")
