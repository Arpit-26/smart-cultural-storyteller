# video_creator.py
import os
import subprocess
from typing import List, Dict
import json
from video_compiler import create_video_from_images_and_audio  

def create_story_video(story_data: Dict, output_filename: str = "cultural_story_video.mp4") -> str:
    """
    Create a complete story video from story data containing images and audio.
    """
    try:
        images = story_data.get('images', [])
        audio_file = story_data.get('audio_file', '')
        story_scenes = story_data.get('story_scenes', [])

        
        if not images:
            return "Error: No images provided for video creation."
        
        if not audio_file or not os.path.exists(audio_file):
            return "Error: No valid audio file provided for video creation."
        
           # 🧠 Pass story_scenes for dynamic image duration calculation
        return create_video_from_images_and_audio(
            images=images,
            audio_file=audio_file,
            output_filename=output_filename,
            story_scenes=story_scenes  # 👈 new argument
        )
        
    except Exception as e:
        return f"Error creating story video: {e}"

def check_ffmpeg_installation() -> bool:
    """
    Check if FFmpeg is installed and available.
    """
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_info(video_path: str) -> Dict:
    """
    Get information about a created video file.
    """
    try:
        if not os.path.exists(video_path):
            return {"error": "Video file not found"}
        
        # Get video info using ffprobe
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', video_path
        ], capture_output=True, text=True, check=True)
        
        info = json.loads(result.stdout)
        
        # Extract useful information
        format_info = info.get('format', {})
        video_stream = next((s for s in info.get('streams', []) if s.get('codec_type') == 'video'), {})
        audio_stream = next((s for s in info.get('streams', []) if s.get('codec_type') == 'audio'), {})
        
        return {
            "filename": os.path.basename(video_path),
            "size_mb": round(float(format_info.get('size', 0)) / (1024*1024), 2),
            "duration": float(format_info.get('duration', 0)),
            "video_codec": video_stream.get('codec_name', 'unknown'),
            "audio_codec": audio_stream.get('codec_name', 'unknown'),
            "width": video_stream.get('width', 0),
            "height": video_stream.get('height', 0)
        }
        
    except Exception as e:
        return {"error": f"Error getting video info: {e}"}
