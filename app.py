import streamlit as st
from utils.ocr import extract_text
from utils.sentiment import analyze_genre  # Changed import
from utils.music import search_tracks

# --- Configuration ---
st.set_page_config(page_title="Page2Playlist", page_icon="📚", layout="centered")

# --- CSS (Dark Mode Black) ---
st.markdown("""
    <style>
        .stApp { background-color: #000000; color: #ffffff; }
        div.stVerticalBlock > div.stVerticalBlock {
            background-color: #121212; border: 1px solid #333;
            padding: 2rem; border-radius: 15px;
        }
        h1 { color: #ffffff !important; text-align: center; }
        p, label { color: #cccccc !important; text-align: center; }
        
        /* Button */
        div.stButton > button {
            background: linear-gradient(90deg, #1DB954 0%, #1ed760 100%); /* Spotify Green-ish */
            color: black; border: none; padding: 0.6rem 1rem;
            border-radius: 8px; font-weight: 700;
        }
        div.stButton > button:hover { transform: scale(1.02); color: black; }

        /* Track Card */
        .track-card {
            background-color: #1E1E1E; border-radius: 8px; padding: 15px;
            margin-bottom: 12px; border-left: 4px solid #1DB954;
            border: 1px solid #333;
        }
        .track-title { font-weight: bold; font-size: 1.1em; color: #ffffff; }
        .track-artist { font-size: 0.9em; color: #aaaaaa; }
        a { text-decoration: none; color: #1DB954 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- App Content ---

st.title("📚 Page2Playlist")
st.markdown("Scan a page. We'll detect the genre and match the score.")

uploaded_file = st.file_uploader("Upload Page", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Scanned Page", use_container_width=True)
    
    if st.button("✨ Detect Genre & Play", use_container_width=True):
        
        with st.spinner("📖 Reading content..."):
            try:
                bytes_data = uploaded_file.getvalue()
                text = extract_text(bytes_data)
                
                # Using the new Genre Analyzer
                genre = analyze_genre(text)
                tracks = search_tracks(genre)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        st.markdown("---")
        
        # Display Genre
        st.markdown(f"<h3 style='text-align: center; color: white;'>Genre: <span style='color: #1DB954; text-shadow: 0 0 10px #1DB954;'>{genre.value.upper()}</span></h3>", unsafe_allow_html=True)
        
        with st.expander("Read extracted text"):
            st.caption(text if text else "No text found.")

        st.markdown("#### 🎧 Cinematic Background")
        
        for track in tracks:
            st.markdown(f"""
            <div class="track-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="track-title">{track['name']}</div>
                        <div class="track-artist">{track['artist']}</div>
                    </div>
                    <a href="{track['url']}" target="_blank">Play ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if track['preview_url']:
                st.audio(track['preview_url'])
            else:
                st.caption("No preview available")