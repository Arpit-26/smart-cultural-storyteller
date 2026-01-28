import streamlit as st
import requests
import json
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Smart Cultural Storyteller",
    page_icon="📚",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:5000/api"

def main():
    st.title("🌍 Smart Cultural Storyteller")
    st.markdown("*Generate culturally rich stories with AI-powered narration and imagery*")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Fetch available themes and languages
        try:
            themes_response = requests.get(f"{API_BASE}/themes")
            languages_response = requests.get(f"{API_BASE}/languages")
            
            if themes_response.status_code == 200:
                themes = themes_response.json().get("themes", {})
            else:
                themes = {"folklore": "Traditional folk tales"}
                
            if languages_response.status_code == 200:
                languages = languages_response.json().get("languages", [])
            else:
                languages = ["English"]
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Backend server not running. Please start the Flask app first.")
            st.stop()
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
            themes = {"folklore": "Traditional folk tales"}
            languages = ["English"]
        
        # Story type selection
        story_type = st.radio(
            "Story Type",
            ["Basic Story", "Cultural Story", "Video Story"]
        )
        
        # Language selection (only Hindi and English)
        hindi_english_languages = ["English", "Hindi"]
        selected_language = st.selectbox(
            "Narration Language",
            hindi_english_languages,
            index=0  # Default to Hindi
        )
        
        # Regional accent selection for Indian stories
        if (story_type == "Video Story" and selected_language == "Hindi" ) or (story_type == "Cultural Story" and selected_language == "Hindi"):
            indian_regions = [
                "None","Punjabi","Tamil", "Telugu", "Gujarati", "Bihari"
            ]
            selected_region = st.selectbox(
                "Indian Region/Accent",
                indian_regions
            )
            if selected_region == "None":
                selected_region = None
        else:
            selected_region = None
        
        if story_type in ["Cultural Story", "Video Story"]:
            # Theme selection
            selected_theme = st.selectbox(
                "Cultural Theme",
                list(themes.keys()),
                format_func=lambda x: f"{x.title()} - {themes[x]}"
            )
            
            # # Culture selection
            # cultures = [
            #     "Indian", "Chinese", "Japanese", "African", 
            #     "European", "Native American", "Middle Eastern", "Latin American"
            # ]
            
            # selected_culture = st.selectbox(
            #     "Culture",
            #     cultures,
            #     index=0  # Default to Indian
            # )
        
        # Video-specific options
        if story_type == "Video Story":
            # Check FFmpeg availability
            try:
                health_response = requests.get(f"{API_BASE}/health")
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    ffmpeg_available = health_data.get("ffmpeg_available", False)
                else:
                    ffmpeg_available = False
            except:
                ffmpeg_available = False
            
            if not ffmpeg_available:
                st.warning("⚠️ **FFmpeg Required for Video Creation**")
                st.markdown("""
                **To enable video creation, please install FFmpeg:**
                
                **Windows:**
                1. Download FFmpeg from: https://ffmpeg.org/download.html
                2. Extract to `C:\\ffmpeg`
                3. Add `C:\\ffmpeg\\bin` to your PATH environment variable
                4. Restart your terminal/IDE
                
                **Alternative (using Chocolatey):**
                ```
                choco install ffmpeg
                ```
                
                **Alternative (using Scoop):**
                ```
                scoop install ffmpeg
                ```
                """)
                st.info("💡 You can still use other story types (Basic, Cultural) without FFmpeg!")
            else:
                st.success("✅ FFmpeg is available - Video creation enabled!")
            
            # num_frames = st.slider(
            #     "Number of Images for Video",
            #     min_value=6,
            #     max_value=20,
            #     value=8,
            #     help="More images create longer, more detailed videos",
            #     disabled=not ffmpeg_available
            # )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Story Input")

        
        if story_type == "Basic Story":
            user_input = st.text_area(
                "Enter your story prompt:",
                placeholder="Tell me a story about a brave knight...",
                height=100
            )
        else:
            use_custom = st.checkbox("Use custom prompt instead of theme")
            if use_custom:
                user_input = st.text_area(
                    "Enter your custom story prompt:",
                    placeholder="Tell me a cultural story about...",
                    height=100
                )
            else:
                user_input = None
                st.info(f"Will generate a {selected_theme} story" )
        
        # Generate button
        if st.button("🎭 Generate Story", type="primary"):
            if story_type == "Basic Story" and not user_input:
                st.error("Please enter a story prompt")
                return
                
            with st.spinner("🎨 Creating your cultural story..."):
                try:
                    if story_type == "Basic Story":
                        # Basic story generation
                        payload = {
                            "text": user_input,
                            "language": selected_language
                        }
                        response = requests.post(f"{API_BASE}/story", json=payload)
                       
                    
                    
                    elif story_type == "Video Story":
                        # Video story generation
                        payload = {
                            "theme": selected_theme,
                            "language": selected_language,
                            "region": selected_region,
                            # "num_frames": num_frames
                        }
                        with st.spinner("🎬 Generating video story... This may take a few minutes ⏳"):
                         response = requests.post(f"{API_BASE}/video-story", json=payload, timeout=800)
                    
                    else:
                        # Cultural story generation
                        payload = {
                            "theme": selected_theme,
                            "region":selected_region,
                            "language": selected_language
                        }
                        if use_custom and user_input:
                            payload["custom_prompt"] = user_input
                            
                        response = requests.post(f"{API_BASE}/cultural-story", json=payload)
                    
                       
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display story
                        st.header("📖 Generated Story")
                        st.write(result["story"])
                        
                        # Display cultural fact if available
                        if "cultural_fact" in result and result["cultural_fact"]:
                            st.info(f"🌟 Cultural Fact: {result['cultural_fact']}")
                        
                        # Display video if available (for Video Story type)
                        if result.get("video") and not result["video"].startswith("Error"):
                            st.header("📺 Story Video")
                            st.video(result["video"])
                            
                            # Display video info
                            if result.get("video_info"):
                                video_info = result["video_info"]
                                st.info(f"📊 Video Info: {video_info.get('duration', 0):.1f}s, "
                                       f"{video_info.get('size_mb', 0)}MB, "
                                       f"{video_info.get('num_frames', 0)} frames")
                        
                        # Display multiple images if available (for Video Story type)
                        if result.get("images") and len(result["images"]) > 1:
                            st.header("🖼️ Story Image Sequence")
                            cols = st.columns(min(3, len(result["images"])))
                            for i, img_url in enumerate(result["images"]):
                                with cols[i % 3]:
                                    if not img_url.startswith("Error"):
                                        st.image(img_url, caption=f"Frame {i+1}")
                        
                        # Display single image if available
                        elif result.get("image") and not result["image"].startswith("Error"):
                            st.header("🖼️ Story Illustration")
                            if result["image"].startswith("http"):
                                # Use HTTP URL for display
                                st.image(result["image"], caption="AI-generated illustration")
                            elif result.get("image_file") and os.path.exists(result["image_file"]):
                                # Fallback to local file
                                st.image(result["image_file"], caption="AI-generated illustration")
                        
                        # Display audio player if available
                        if result.get("audio") and not result["audio"].startswith("Error"):
                            st.header("🎵 Story Narration")
                            if result["audio"].startswith("http"):
                                # Use HTTP URL for audio
                                st.audio(result["audio"], format="audio/mp3")
                            elif result.get("audio_file") and os.path.exists(result["audio_file"]):
                                # Fallback to local file
                                with open(result["audio_file"], "rb") as audio_file:
                                    st.audio(audio_file.read(), format="audio/mp3")
                        
                        # Display regional accent info for Video stories
                        if story_type == "Video Story" and result.get("language"):
                            detected_accent = result.get("language", "Hindi")
                            if detected_accent != "Hindi":
                                st.success(f"🗣️ Regional Accent: {detected_accent}")
                        
                        # Store result in session state for download
                        st.session_state.last_result = result
                        
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend server. Please ensure Flask app is running.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
    with col2:
        st.header("ℹ️ About")
        st.markdown("""
        **Smart Cultural Storyteller** uses:
        
        🧠 **Orca Mini 3B** - Local story generation  
        🎙️ **ElevenLabs** - Multi-language narration  
        🎨 **Pollinations.ai** - Free image generation  
        
        **Features:**
        - 🌍 Multi-cultural themes
        - 🗣️ Multi-language support
        - 🖼️ AI-generated illustrations
        - 🎵 Audio narration
        - 💡 Cultural facts
        """)
        
        # Health check
        try:
            health_response = requests.get(f"{API_BASE}/health")
            if health_response.status_code == 200:
                st.success("✅ Backend is healthy")
            else:
                st.warning("⚠️ Backend issues detected")
        except:
            st.error("❌ Backend not accessible")
        
        # Download section
        if hasattr(st.session_state, 'last_result'):
            st.header("💾 Downloads")
            result = st.session_state.last_result
            
            # Use audio_file path for download (local file path)
            audio_path = result.get("audio_file") or result.get("audio")
            if audio_path and os.path.exists(audio_path) and not audio_path.startswith("Error"):
                with open(audio_path, "rb") as f:
                    st.download_button(
                        "🎵 Download Audio",
                        f.read(),
                        file_name="story_narration.mp3",
                        mime="audio/mp3"
                    )
            
            # Use image_file path for download (local file path)
            image_path = result.get("image_file") or result.get("image")
            if image_path and os.path.exists(image_path) and not image_path.startswith("Error"):
                with open(image_path, "rb") as f:
                    st.download_button(
                        "🖼️ Download Image",
                        f.read(),
                        file_name="story_illustration.png",
                        mime="image/png"
                    )
            
            # Video download for Video Story type
            video_path = result.get("video_file")
            if video_path and os.path.exists(video_path) and not video_path.startswith("Error"):
                with open(video_path, "rb") as f:
                    st.download_button(
                        "🎬 Download Video",
                        f.read(),
                        file_name="cultural_story_video.mp4",
                        mime="video/mp4"
                    )

if __name__ == "__main__":
    main()
