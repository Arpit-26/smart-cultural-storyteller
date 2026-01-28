import os
import json
import subprocess
from typing import List, Optional


def create_video_from_images_and_audio(
    images: List[str], 
    audio_file: str, 
    output_filename: str = "story_video.mp4", 
    story_scenes: Optional[List[str]] = None
) -> str:
    """
    Create a video by combining multiple images with a single narration audio.
    Each image duration is proportional to its scene text length relative to the full story.
    """
    try:
        print(f"🎬 Creating video with {len(images)} scenes and 1 narration audio...")

        # --- Verify FFmpeg ---
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ FFmpeg is available")
        except Exception:
            return "Error: FFmpeg not found. Please install FFmpeg."

        # --- Validate input files ---
        valid_images = [img for img in images if os.path.exists(img)]
        if not valid_images:
            return "Error: No valid images found."

        if not os.path.exists(audio_file):
            return f"Error: Audio file not found: {audio_file}"

        # --- Get total audio duration ---
        try:
            result = subprocess.run([
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", audio_file
            ], capture_output=True, text=True, check=True)
            audio_info = json.loads(result.stdout)
            audio_duration = float(audio_info["format"]["duration"])
            print(f"🎧 Audio duration: {audio_duration:.2f} seconds")
        except Exception as e:
            print(f"⚠️ Could not get audio duration, defaulting to 5s/image: {e}")
            audio_duration = len(valid_images) * 5.0

        # --- Calculate proportional durations ---
        if story_scenes and len(story_scenes) == len(valid_images):
            text_lengths = [len(s.strip()) for s in story_scenes]
            total_length = sum(text_lengths) if sum(text_lengths) > 0 else len(valid_images)
            durations = [
                max(2.0, (len(s.strip()) / total_length) * audio_duration)
                for s in story_scenes
            ]
        else:
            # fallback - equal duration for all images
            duration_per_image = max(2.0, audio_duration / len(valid_images))
            durations = [duration_per_image] * len(valid_images)

        print("🕐 Calculated durations per scene:")
        for i, d in enumerate(durations):
            print(f"  Scene {i+1}: {d:.2f} seconds")

        # --- Create FFmpeg file list ---
        filelist_path = "static/temp_filelist.txt"
        os.makedirs("static", exist_ok=True)
        with open(filelist_path, "w", encoding="utf-8") as f:
            for i, img in enumerate(valid_images):
                abs_path = os.path.abspath(img).replace("\\", "/")
                f.write(f"file '{abs_path}'\n")
                f.write(f"duration {durations[i]:.2f}\n")
            # Repeat last image for smooth ending
            f.write(f"file '{os.path.abspath(valid_images[-1]).replace('\\', '/')}'\n")

        # --- Run FFmpeg to create video ---
        output_path = f"static/{output_filename}"
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", filelist_path,
            "-i", audio_file,
            "-c:v", "libx264", "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-r", "25",
            "-shortest",
            "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,"
                   "pad=1280:720:(ow-iw)/2:(oh-ih)/2",
            output_path
        ]

        print("🚀 Running FFmpeg command...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ FFmpeg error:\n{result.stderr}")
            return f"Error creating video: {result.stderr}"

        # --- Cleanup ---
        if os.path.exists(filelist_path):
            os.remove(filelist_path)

        if os.path.exists(output_path):
            print(f"✅ Video created successfully: {output_path}")
            return output_path
        else:
            return "❌ Error: Video not created."

    except Exception as e:
        print(f"❌ Exception in video creation: {e}")
        return f"Error creating video: {e}"






# def create_video_from_images_and_audio(images: List[str], audio_file: str, output_filename: str = "story_video.mp4") -> str:
#     """
#     Create a video by combining multiple images with audio using FFmpeg.
#     Optimized for 6-scene storytelling videos.
#     """
#     try:
#         print(f"Creating video with {len(images)} images and audio: {audio_file}")
        
#         # Check if FFmpeg is available
#         try:
#             subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
#             print("✅ FFmpeg is available")
#         except (subprocess.CalledProcessError, FileNotFoundError):
#             return "Error: FFmpeg not found. Please install FFmpeg to create videos."
        
#         # Filter out error messages and ensure all images exist
#         valid_images = []
#         for i, img in enumerate(images):
#             if not img.startswith("Error") and os.path.exists(img):
#                 valid_images.append(img)
#                 print(f"✅ Image {i+1} valid: {os.path.basename(img)}")
#             else:
#                 print(f"⚠️ Image {i+1} invalid/missing: {img}")
        
#         if not valid_images:
#             return "Error: No valid images found for video creation."
        
#         if not os.path.exists(audio_file):
#             return f"Error: Audio file not found: {audio_file}"
        
#         print(f"Using {len(valid_images)} valid images for video")
        
#         # Get audio duration
#         try:
#             result = subprocess.run([
#                 'ffprobe', '-v', 'quiet', '-print_format', 'json', 
#                 '-show_format', audio_file
#             ], capture_output=True, text=True, check=True)
            
#             audio_info = json.loads(result.stdout)
#             audio_duration = float(audio_info['format']['duration'])
#             print(f"Audio duration: {audio_duration:.2f} seconds")
#         except Exception as e:
#             print(f"Could not get audio duration, using default: {e}")
#             # Default duration for 6-line story (4 seconds per scene)
#             audio_duration = len(valid_images) * 4.0
        
#         # Calculate duration per image (ensure minimum 2 seconds per image)
#         image_duration = max(2.0, audio_duration / len(valid_images))
#         print(f"Duration per image: {image_duration:.2f} seconds")
        
#         # Create a temporary file list for FFmpeg
#         filelist_path = "static/temp_filelist.txt"
#         try:
#             with open(filelist_path, 'w') as f:
#                 for i, img in enumerate(valid_images):
#                     abs_path = os.path.abspath(img).replace('\\', '/')
#                     f.write(f"file '{abs_path}'\n")
#                     f.write(f"duration {image_duration}\n")
#                 # Add the last image again for proper ending
#                 if valid_images:
#                     abs_path = os.path.abspath(valid_images[-1]).replace('\\', '/')
#                     f.write(f"file '{abs_path}'\n")
            
#             print(f"Created filelist: {filelist_path}")
#         except Exception as e:
#             return f"Error creating filelist: {e}"
        
#         # Output path
#         output_path = f"static/{output_filename}"
        
#         # FFmpeg command to create video with better quality
#         cmd = [
#             'ffmpeg', '-y',  # -y to overwrite output file
#             '-f', 'concat',
#             '-safe', '0',
#             '-i', filelist_path,
#             '-i', audio_file,
#             '-c:v', 'libx264',
#             '-c:a', 'aac',
#             '-pix_fmt', 'yuv420p',
#             '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2',  # Scale to 720p
#             '-r', '25',  # 25 fps for smoother video
#             '-shortest',  # End video when shortest stream ends
#             '-movflags', '+faststart',  # Optimize for web playback
#             output_path
#         ]
        
#         print("Running FFmpeg command...")
#         print(" ".join(cmd))
        
#         # Run FFmpeg command
#         result = subprocess.run(cmd, capture_output=True, text=True)
        
#         # Clean up temporary file
#         if os.path.exists(filelist_path):
#             os.remove(filelist_path)
        
#         if result.returncode == 0 and os.path.exists(output_path):
#             file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
#             print(f"✅ Video created successfully: {output_path} ({file_size:.2f} MB)")
#             return output_path
#         else:
#             error_msg = result.stderr if result.stderr else "Unknown FFmpeg error"
#             print(f"❌ FFmpeg error: {error_msg}")
#             return f"Error creating video: {error_msg}"
            
#     except Exception as e:
#         print(f"❌ Exception in create_video_from_images_and_audio: {e}")
#         return f"Error creating video: {e}"
