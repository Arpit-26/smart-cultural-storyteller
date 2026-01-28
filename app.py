from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from storyteller import (
    generate_audio, 
    generate_audio_with_accent,
    detect_regional_accent,
    get_cultural_themes, 
    get_supported_languages, 
    generate_cultural_facts
)
from models.story_generator import generate_story, generate_cultural_story
from models.image_generator import (
    generate_image, 
    generate_cultural_image, 
    generate_themed_image,
    # generate_multiple_images,
    generate_video_frames
)
from video_creator import create_story_video, check_ffmpeg_installation, get_video_info
import os

app = Flask(__name__)
CORS(app)


# Ensure static directory exists for generated files
os.makedirs("static", exist_ok=True)

# Serve static files (images, audio) to frontend
@app.route("/static/<filename>")
def serve_static_file(filename):
    """Serve generated static files (images, audio) to frontend."""
    return send_from_directory("static", filename)


# 1 BASIC STORY MODE
@app.route("/api/story", methods=["POST"])
def create_story():
    """Generate a basic story with audio and image."""
    data = request.get_json()
    text = data.get("text", "")
    language = data.get("language", "English")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate story text in English first
        english_story = generate_story(text)
        
        # Translate to Hindi if Hindi language is selected
        if language == "Hindi" or "Hindi" in language:
            from models.story_generator import translate_to_hindi
            story_text = translate_to_hindi(english_story)
        else:
            story_text = english_story

        # Generate narration with language support
        audio_file = generate_audio(story_text, filename="static/story_audio.mp3", language=language)

        # Generate image
        # image_file = generate_image(english_story, filename="static/story_image.png")
        image_file=generate_cultural_image(
            english_story,  
            culture="Indian",
            filename="static/story_image.png"
        )

        
        return jsonify({
            "story": story_text,
            "audio": f"http://localhost:5000/static/{os.path.basename(audio_file)}" if not audio_file.startswith("Error") else audio_file,
            "image": f"http://localhost:5000/static/{os.path.basename(image_file)}" if not image_file.startswith("Error") else image_file,
            "audio_file": audio_file,  # Keep original path for download
            "image_file": image_file,  # Keep original path for download
            "language": language
        })
    
    except Exception as e:
        return jsonify({"error": f"Story generation failed: {str(e)}"}), 500


# 2 CULTURAL STORY MODE
@app.route("/api/cultural-story", methods=["POST"])
def create_cultural_story():
    """Generate a culturally-themed story with enhanced features."""
    data = request.get_json()
    theme = data.get("theme", "folklore")
    culture = data.get("culture", None)
    region = data.get("region", None)
    language = data.get("language", "English")
    custom_prompt = data.get("custom_prompt", "")
    
    if not theme and not custom_prompt:
        return jsonify({"error": "Theme or custom prompt required"}), 400

    try:
        # Generate cultural story
        if custom_prompt:
            story_text = generate_story(custom_prompt)
        else:
            story_text,eng_story = generate_cultural_story(theme, language)

        # Generate cultural facts
        cultural_fact = generate_cultural_facts(culture) if culture else ""

        # Generate culturally appropriate image
        image_file = generate_cultural_image(
            eng_story, 
            culture, 
            filename="static/cultural_story_image.png"
        )

        # Generate narration
        audio_file = generate_audio_with_accent(
            story_text, 
            culture,
            region=region, 
            filename="static/cultural_story_audio.mp3", 
        )

        return jsonify({
            "story": story_text,
            "audio": f"http://localhost:5000/static/{os.path.basename(audio_file)}" if not audio_file.startswith("Error") else audio_file,
            "image": f"http://localhost:5000/static/{os.path.basename(image_file)}" if not image_file.startswith("Error") else image_file,
            "audio_file": audio_file,  # Keep original path for download
            "image_file": image_file,  # Keep original path for download
            "theme": theme,
            "culture": culture,
            "language": language,
            "cultural_fact": cultural_fact
        })
    
    except Exception as e:
        return jsonify({"error": f"Cultural story generation failed: {str(e)}"}), 500

# @app.route("/api/themed-image", methods=["POST"])
# def create_themed_image():
#     """Generate themed image for cultural storytelling."""
#     data = request.get_json()
#     theme = data.get("theme", "")
#     culture = data.get("culture", None)
    
#     if not theme:
#         return jsonify({"error": "Theme required"}), 400

#     try:
#         image_file = generate_themed_image(
#             theme, 
#             culture, 
#             filename="static/themed_image.png"
#         )
        
#         return jsonify({
#             "image": image_file,
#             "theme": theme,
#             "culture": culture
#         })
    
#     except Exception as e:
#         return jsonify({"error": f"Image generation failed: {str(e)}"}), 500

@app.route("/api/themes", methods=["GET"])
def get_themes():
    """Get available cultural themes."""
    return jsonify({
        "themes": get_cultural_themes()
    })

@app.route("/api/languages", methods=["GET"])
def get_languages():
    """Get supported languages for narration."""
    return jsonify({
        "languages": get_supported_languages()
    })

@app.route("/api/cultural-facts/<culture>", methods=["GET"])
def get_cultural_facts_endpoint(culture):
    """Get cultural facts for a specific culture."""
    fact = generate_cultural_facts(culture)
    return jsonify({
        "culture": culture,
        "fact": fact
    })

# 3 video STORY MODE
@app.route("/api/video-story", methods=["POST"])
def create_video_story():
    """Generate a story with multiple images and create a video."""
    data = request.get_json()
    theme = data.get("theme", "folklore")
    culture = data.get("culture", "Indian")
    language = data.get("language", "Hindi")
    region = data.get("region", None)
    # num_frames = data.get("num_frames", 8)

    print(f"the input is data: {data}, theme: {theme}, language: {language}, region: {region}")
    
    try:
        # Check if FFmpeg is available
        if not check_ffmpeg_installation():
            return jsonify({
                "error": "FFmpeg not installed. Video creation requires FFmpeg.",
                "install_note": "Please install FFmpeg to enable video creation feature."
            }), 400
        
        # Generate story using cultural story function
        story_text, eng_story = generate_cultural_story(theme, language)
        print("===============================================APP.PY story_text===============================================")
        print("Generated story for video:", story_text)
        print("===============================================APP.PY eng_story===============================================")
        print("Generated English story for video:", eng_story)
        # Generate audio narration
        audio_file = None
        try:
            if language == "Hindi" or "Hindi" in language:
                # Generate audio with accent
                audio_file = generate_audio_with_accent(
                    story_text, 
                    culture="Indian",        # fixed default culture
                    region=region,           # region from frontend
                    filename="static/video_story_audio.mp3"
                )
            else:
                # Generate audio without accent
                audio_file = generate_audio(
                    story_text, 
                    filename="static/video_story_audio.mp3", 
                    language=language
                )
        except Exception as e:
            print(f"⚠️ Audio generation failed: {e}")
            audio_file = None



        # Generate multiple images for video
        video_frames = generate_video_frames(eng_story, culture)
        
        if "error" in video_frames:
            return jsonify({"error": video_frames["error"]}), 500
        
        # Create video
        video_file = create_story_video({
            "images": video_frames["images"],
            "audio_file": audio_file,
            "story_scenes": video_frames["story_scenes"]
        }, "cultural_story_video.mp4")
        
        if video_file.startswith("Error"):
            return jsonify({"error": video_file}), 500
        
        # Get video info
        video_info = get_video_info(video_file)
        
        return jsonify({
            "story": story_text,
            "audio": f"http://localhost:5000/static/{os.path.basename(audio_file)}" if not audio_file.startswith("Error") else audio_file,
            "video": f"http://localhost:5000/static/{os.path.basename(video_file)}",
            "images": [f"http://localhost:5000/static/{os.path.basename(img)}" for img in video_frames["images"]],
            "audio_file": audio_file,
            "video_file": video_file,
            "image_files": video_frames["images"],
            "video_info": video_info,
            "theme": theme,
            "culture": culture,
            "language": language,
            "region": region,
            "num_frames": len(video_frames["images"]),
            "cultural_fact": generate_cultural_facts(culture)
        })
        
    except Exception as e:
        return jsonify({"error": f"Video story generation failed: {str(e)}"}), 500

# @app.route("/api/multiple-images", methods=["POST"])
# def create_multiple_images():
#     """Generate multiple images from a story for video creation."""
#     data = request.get_json()
#     story_text = data.get("story_text", "")
#     culture = data.get("culture", None)
#     num_images = data.get("num_images", 5)
    
#     if not story_text:
#         return jsonify({"error": "Story text required"}), 400
    
#     try:
#         # Generate multiple images
#         image_files = generate_multiple_images(story_text, culture, num_images)
        
#         # Filter out errors
#         valid_images = [img for img in image_files if not img.startswith("Error")]
#         errors = [img for img in image_files if img.startswith("Error")]
        
#         return jsonify({
#             "images": [f"http://localhost:5000/static/{os.path.basename(img)}" for img in valid_images],
#             "image_files": valid_images,
#             "num_generated": len(valid_images),
#             "errors": errors if errors else None
#         })
        
#     except Exception as e:
#         return jsonify({"error": f"Multiple image generation failed: {str(e)}"}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    ffmpeg_available = check_ffmpeg_installation()
    
    return jsonify({
        "status": "healthy",
        "message": "Smart Cultural Storyteller API is running",
        "features": [
            "Story Generation (Orca Mini 3B)",
            "Hindi & English Support",
            "Regional Indian Accents",
            "Multi-language TTS (ElevenLabs)",
            "Image Generation (Pollinations.ai)",
            "Multiple Images for Video",
            "Video Creation (FFmpeg)" if ffmpeg_available else "Video Creation (FFmpeg Not Available)",
            "Cultural Themes",
            "Cultural Facts"
        ],
        "ffmpeg_available": ffmpeg_available
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True,
        debug=True,
        use_reloader=False
    )
