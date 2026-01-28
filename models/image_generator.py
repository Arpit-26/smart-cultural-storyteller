# models/image_generator.py
import requests
import os
from urllib.parse import quote
import re
import nltk

# Ensure tokenizers are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')



def generate_image(prompt: str, filename="story_image.png", style="fantasy", width=512, height=512) -> str:
    """
    Generate image using Pollinations.ai API - free and lightweight.
    No heavy models needed, perfect for low-spec machines.
    """
    try:
        # Clean and enhance the prompt for better image generation
        enhanced_prompt = f"{prompt}, {style} art style, detailed, high quality"
        
        # URL encode the prompt
        encoded_prompt = quote(enhanced_prompt)
        
        # Pollinations.ai API endpoint
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed=-1"
        print(f"🖼️  Pollinations request: {api_url[:200]}...")  # Log first 200 chars of URL

        response = requests.get(api_url, timeout=60)

        # Log HTTP response for debugging
        print(f"🔍 Pollinations status: {response.status_code}")



        # Make request to generate image
        response = requests.get(api_url, timeout=200)
        response.raise_for_status()
        
        # Save the image
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename
        
    except requests.exceptions.RequestException as e:
        return f"Error generating image: Network error - {e}"
    except Exception as e:
        return f"Error generating image: {e}"

def generate_cultural_image(story_text: str, culture: str = None, filename="cultural_story_image.png") -> str:
    """
    Generate culturally appropriate image based on story content.
    """
    # Extract key visual elements from story
    cultural_context = f", {culture} cultural elements" if culture else ""
    
    # Create enhanced prompt for cultural imagery
    image_prompt = f"Illustration of: {story_text[:200]}... cultural storytelling scene{cultural_context}, traditional art style"
    
    return generate_image(image_prompt, filename, style="traditional cultural")

def generate_themed_image(theme: str, culture: str = None, filename="themed_image.png") -> str:
    """
    Generate image based on cultural theme.
    """
    cultural_style = f"{culture} " if culture else ""
    prompt = f"{cultural_style}{theme}, cultural illustration, traditional elements, storytelling art"
    
    return generate_image(prompt, filename, style="cultural traditional")


# def generate_multiple_images(story_text: str, culture: str = None) -> list:
#     """
#     Generate multiple images from different parts of the story for video creation.
#     Optimized for 6-line stories - one image per line.
#     """
#     try:
#         # Split story into lines (for 6-line stories)
#         lines = [line.strip() for line in story_text.split('\n') if line.strip()]
        
#         # If we don't have enough lines, split by sentences
#         if len(lines) < num_images:
#             sentences = story_text.split('. ')
#             sentences = [s.strip() + '.' if not s.endswith('.') else s.strip() for s in sentences if s.strip()]
#             lines = sentences
        
#         # Ensure we have exactly the number of images requested
#         if len(lines) > num_images:
#             lines = lines[:num_images]
#         elif len(lines) < num_images:
#             # Duplicate some lines to reach the target
#             while len(lines) < num_images:
#                 lines.append(lines[-1] if lines else story_text[:100])
        
#         # Generate images for each line/scene
#         image_files = []
#         cultural_context = f", {culture} cultural style" if culture else ""
        
#         for i, line in enumerate(lines[:num_images]):
#             # Create unique filename for each scene
#             filename = f"static/scene_{i+1:02d}.png"
            
#             # Create detailed image prompt for each scene
#             scene_prompt = f"Scene {i+1}: {line[:200]}{cultural_context}, detailed illustration, storytelling art, high quality"
            
#             print(f"Generating image {i+1}/{num_images}: {scene_prompt[:50]}...")
            
#             # Generate image with retry logic
#             result = generate_image(scene_prompt, filename, style="storytelling illustration", width=1024, height=576)
            
#             if not result.startswith("Error") and os.path.exists(result):
#                 image_files.append(result)
#                 print(f"✅ Scene {i+1} image generated successfully")
#             else:
#                 print(f"⚠️ Failed to generate scene {i+1}, using fallback")
#                 # Create a fallback image with simpler prompt
#                 fallback_prompt = f"Story illustration, {culture} style" if culture else "Story illustration"
#                 fallback_result = generate_image(fallback_prompt, filename, style="simple illustration")
#                 if not fallback_result.startswith("Error"):
#                     image_files.append(fallback_result)
        
#         print(f"Generated {len(image_files)} images for video")
#         return image_files
        
#     except Exception as e:
#         print(f"Error in generate_multiple_images: {e}")
#         return [f"Error generating multiple images: {e}"]




#  GEnerate story video frames
def generate_video_frames(story_text: str, culture: str = None) -> dict:
    """
    Generate scene-wise images from story text for video creation.
    Each scene becomes a frame with culturally relevant illustration prompts.
    """

    # print(story_text)
    
    try:
        print(f"🔍 Generating video frames for story... {story_text[:200]}")  # slice for long stories

        story_text = clean_story_text(story_text)

         # Step 1: Split story into logical scenes
        scenes = split_story_into_scenes(story_text)
        if not scenes:
            return {"error": "No scenes could be generated"}

        print(f"🧩 {len(scenes)} scenes detected")


        # Step 2: Build culturally enriched prompts
        image_files = []
        frame_durations = []
        words_per_second = 2.0  
        for i, scene in enumerate(scenes):
            filename = f"static/scene_{i+1:02d}.png"

            # Enhance scene with cultural + visual details
            # scene_prompt = (
            #     f"Scene {i+1}: {scene}. "
            #     f"A detailed storybook illustration, "
            #     f"rich colors, cinematic lighting, 16:9 aspect ratio, high quality digital art."
            # )

            scene_prompt =f"Scene {i+1}: {sanitize_prompt(scene)}. Cultural theme: Indian, art style: storybook illustration, high quality."

            print(f"🎨 Generating image {i+1}/{len(scenes)}: {scene_prompt[:80]}...")

            result = generate_image(
                prompt=scene_prompt,
                filename=filename,
                style="storybook illustration",
                width=1280,
                height=720
            )

            if not result.startswith("Error") and os.path.exists(result):
                image_files.append(result)
                print("===============================================")
                print(f"✅ Scene {i+1} image generated successfully")
            else:
                print(f"⚠️ Failed to generate scene {i+1}, using fallback")
                fallback_prompt = f"Generic cultural illustration {culture if culture else ''}"
                fallback_result = generate_image(fallback_prompt, filename, style="simple illustration")
                if not fallback_result.startswith("Error") and os.path.exists(fallback_result):
                    image_files.append(fallback_result)

        for i, s in enumerate(scenes):
            print(f"Scene {i+1}:", s)    

        # Step 3: Timing (longer per frame since images are richer)
        for i, scene in enumerate(scenes):
            # generate image ...
            # calculate frame duration for this scene
            word_count = len(scene.split())
            frame_time = max(3.0, word_count / words_per_second)
            frame_durations.append(frame_time)

         # Step 3: Compute total duration
        total_duration = sum(frame_durations)


        print(f"📽️ Generated {len(image_files)} valid frames, total duration: {total_duration:.1f}s")

        return {
            "images": image_files,
            "frame_durations": frame_durations,
            "total_duration": total_duration,
            "num_frames": len(image_files),
            "culture": culture,
            "story_scenes": scenes
        }

    except Exception as e:
        print(f"❌ Error in generate_video_frames: {e}")
        return {"error": f"Error generating video frames: {e}"}




def sanitize_prompt(text):
    return re.sub(r'[^a-zA-Z0-9\s,.\'-]', '', text)[:500]  # limit to 500 chars


def clean_story_text(story_text: str) -> str:
    if not story_text:
        return ""
    story_text = story_text.strip()
    # Remove any AI-style prefixes like “Sure!” or “Here’s an example”
    bad_phrases = [
        "Sure!", "I'd love to help you", "Here is an example", 
        "1. Setting:", "2. Characters:", "3. Conflict:", "4. Resolution:"
    ]
    for phrase in bad_phrases:
        story_text = story_text.replace(phrase, "")
    return story_text




#STORY SPLITTING LOGIC
def split_story_into_scenes(story_text):
    if not story_text:
        print("❌ Warning: Empty or None story_text passed to split_story_into_scenes")
        return []

    # Ensure sentence tokenizer available
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    story_text = story_text.strip()

    # Step 1: Split into sentences (works for most languages)
    sentences = nltk.sent_tokenize(story_text)

    # Step 2: Clean up and filter
    scenes = [s.strip() for s in sentences if len(s.strip()) > 3]

    # Step 3: Optional fallback if tokenizer fails (Hindi or mixed text)
    if len(scenes) <= 1:
        scenes = re.split(r'(?<=[।.!?])\s+', story_text)
        scenes = [s.strip() for s in scenes if len(s.strip()) > 3]

    print(f"🎞️ Story split into {len(scenes)} scenes (one per sentence).")
    return scenes

















# def split_story_into_scenes(story_text):
#     if not story_text:
#         print("❌ Warning: Empty or None story_text passed to split_story_into_scenes")
#         return []


#     # Step 1: Normalize text
#     story_text = story_text.strip()

#     # Step 2: Split by paragraph or story transition words
#     potential_scenes = re.split(
#         r'\n+|(?<=\.)\s+(?=(Then|Meanwhile|After|Suddenly|One day|Later|Soon|Finally|At that moment))',
#         story_text
#     )

#     print(f"Initial split into {len(potential_scenes)} potential scenes")   
#     print(potential_scenes)
#     # Clean empty items
#     potential_scenes = [s.strip() for s in potential_scenes if s and s.strip()]

#     # Step 3: Merge short sentences into the next scene
#     scenes = []
#     buffer = ""
#     for scene in potential_scenes:
#         word_count = len(scene.split())
#         if word_count < 12:  # too short, merge with next
#             buffer += " " + scene
#         else:
#             if buffer:
#                 scene = buffer.strip() + " " + scene
#                 buffer = ""
#             scenes.append(scene.strip())

#     if buffer:
#         scenes.append(buffer.strip())

#     # Step 4: Return scenes list
#     return scenes
