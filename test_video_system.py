#!/usr/bin/env python3
"""
Test script specifically for video generation functionality.
Tests the complete pipeline: 6-line Story → Multiple Images → Audio → Video
"""

import requests
import json
import time
import os
from video_creator import check_ffmpeg_installation

API_BASE = "http://localhost:5000/api"

def test_ffmpeg_availability():
    """Test if FFmpeg is available for video creation."""
    print("🔧 Testing FFmpeg availability...")
    
    if check_ffmpeg_installation():
        print("✅ FFmpeg is installed and available")
        return True
    else:
        print("❌ FFmpeg is not available")
        print("   Please install FFmpeg to enable video creation")
        print("   See FFMPEG_INSTALLATION.md for instructions")
        return False

def test_6_line_story_generation():
    """Test optimized 6-line story generation."""
    print("\n📚 Testing 6-line story generation...")
    
    payload = {
        "theme": "folklore",
        "culture": "Indian",
        "language": "English"
    }
    
    try:
        print("   Generating 6-line cultural story...")
        response = requests.post(f"{API_BASE}/cultural-story", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            story = result['story']
            lines = [line.strip() for line in story.split('\n') if line.strip()]
            
            print("✅ 6-line story generated successfully!")
            print(f"   Story has {len(lines)} lines")
            print("   Story preview:")
            for i, line in enumerate(lines[:6], 1):
                print(f"   {i}. {line[:80]}{'...' if len(line) > 80 else ''}")
            
            return result
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ 6-line story generation failed: {error_msg}")
            return None
            
    except Exception as e:
        print(f"❌ Error in 6-line story test: {e}")
        return None

def test_video_story_generation():
    """Test complete video story generation with images per scene."""
    print("\n🎬 Testing video story generation...")
    
    payload = {
        "theme": "folklore",
        "culture": "Indian", 
        "language": "English",
        "region": "North Indian",
        "num_frames": 6
    }
    
    try:
        print("   Generating complete video story (this may take a few minutes)...")
        response = requests.post(f"{API_BASE}/video-story", json=payload, timeout=300)  # 5 minute timeout
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Video story generated successfully!")
            print(f"   Story: {len(result['story'])} characters")
            print(f"   Audio file: {result.get('audio_file', 'Not generated')}")
            print(f"   Video file: {result.get('video_file', 'Not generated')}")
            print(f"   Number of images: {result.get('num_frames', 0)}")
            
            # Check if files exist
            video_file = result.get('video_file', '')
            if video_file and os.path.exists(video_file):
                file_size = os.path.getsize(video_file) / (1024 * 1024)  # Size in MB
                print(f"✅ Video file created: {os.path.basename(video_file)} ({file_size:.2f} MB)")
            else:
                print("⚠️ Video file not found")
            
            audio_file = result.get('audio_file', '')
            if audio_file and os.path.exists(audio_file):
                print(f"✅ Audio file created: {os.path.basename(audio_file)}")
            else:
                print("⚠️ Audio file not found")
            
            # Check images
            image_files = result.get('image_files', [])
            valid_images = [img for img in image_files if os.path.exists(img)]
            print(f"✅ {len(valid_images)}/{len(image_files)} images created successfully")
            
            if result.get('video_info'):
                video_info = result['video_info']
                print(f"   Video info: {video_info.get('width', 0)}x{video_info.get('height', 0)}, {video_info.get('duration', 0):.1f}s")
            
            return result
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ Video story generation failed: {error_msg}")
            return None
            
    except Exception as e:
        print(f"❌ Error in video story test: {e}")
        return None

def test_multiple_images_generation():
    """Test multiple image generation for video scenes."""
    print("\n🖼️ Testing multiple images generation...")
    
    # First generate a story
    story_result = test_6_line_story_generation()
    if not story_result:
        print("❌ Cannot test images without story")
        return None
    
    payload = {
        "story_text": story_result['story'],
        "culture": "Indian",
        "num_images": 6
    }
    
    try:
        print("   Generating multiple images from story...")
        response = requests.post(f"{API_BASE}/multiple-images", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Multiple images generated successfully!")
            print(f"   Generated {result.get('num_generated', 0)} images")
            
            # Check if image files exist
            image_files = result.get('image_files', [])
            valid_images = 0
            for i, img_file in enumerate(image_files, 1):
                if os.path.exists(img_file):
                    valid_images += 1
                    file_size = os.path.getsize(img_file) / 1024  # Size in KB
                    print(f"   ✅ Image {i}: {os.path.basename(img_file)} ({file_size:.1f} KB)")
                else:
                    print(f"   ⚠️ Image {i}: Missing - {img_file}")
            
            print(f"   Total valid images: {valid_images}/{len(image_files)}")
            return result
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ Multiple images generation failed: {error_msg}")
            return None
            
    except Exception as e:
        print(f"❌ Error in multiple images test: {e}")
        return None

def main():
    """Run video system tests."""
    print("🎬 Starting Video System Tests for Smart Cultural Storyteller")
    print("=" * 70)
    
    tests = [
        ("FFmpeg Availability", test_ffmpeg_availability),
        ("6-Line Story Generation", test_6_line_story_generation),
        ("Multiple Images Generation", test_multiple_images_generation),
        ("Complete Video Story", test_video_story_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*25} {test_name} {'='*25}")
        result = test_func()
        if result is not None and not (isinstance(result, bool) and not result):
            passed += 1
        time.sleep(2)  # Brief pause between tests
    
    print("\n" + "="*70)
    print(f"🏁 Video System Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All video system tests passed!")
        print("   Your Smart Cultural Storyteller video generation is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        
    print("\n📋 Next Steps:")
    print("1. Ensure FFmpeg is installed (see FFMPEG_INSTALLATION.md)")
    print("2. Start the Flask backend: python app.py")
    print("3. Test video generation via API or frontend")
    print("4. Generated videos will be saved in the 'static' folder")

if __name__ == "__main__":
    main()
