#!/usr/bin/env python3
"""
Test script for Smart Cultural Storyteller system.
Tests the complete pipeline: Story → Image → Audio
"""

import requests
import json
import time
import os

API_BASE = "http://localhost:5000/api"

def test_health_check():
    """Test if the backend is running and healthy."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is healthy!")
            print(f"   Status: {data['status']}")
            print(f"   Features: {', '.join(data['features'])}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is Flask app running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_themes_and_languages():
    """Test themes and languages endpoints."""
    print("\n🎭 Testing themes and languages...")
    
    try:
        # Test themes
        themes_response = requests.get(f"{API_BASE}/themes", timeout=10)
        if themes_response.status_code == 200:
            themes = themes_response.json()["themes"]
            print(f"✅ Available themes: {list(themes.keys())}")
        else:
            print("❌ Failed to get themes")
            
        # Test languages
        languages_response = requests.get(f"{API_BASE}/languages", timeout=10)
        if languages_response.status_code == 200:
            languages = languages_response.json()["languages"]
            print(f"✅ Supported languages: {languages}")
        else:
            print("❌ Failed to get languages")
            
        return True
    except Exception as e:
        print(f"❌ Error testing themes/languages: {e}")
        return False

def test_basic_story():
    """Test basic story generation."""
    print("\n📚 Testing basic story generation...")
    
    payload = {
        "text": "Tell me a short story about a wise old tree in a magical forest",
        "language": "English"
    }
    
    try:
        print("   Generating story...")
        response = requests.post(f"{API_BASE}/story", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Basic story generated successfully!")
            print(f"   Story length: {len(result['story'])} characters")
            print(f"   Audio file: {result.get('audio', 'Not generated')}")
            print(f"   Image file: {result.get('image', 'Not generated')}")
            
            # Check if files exist
            if result.get('audio') and os.path.exists(result['audio']):
                print("✅ Audio file created successfully")
            else:
                print("⚠️ Audio file not found")
                
            if result.get('image') and os.path.exists(result['image']):
                print("✅ Image file created successfully")
            else:
                print("⚠️ Image file not found")
                
            return True
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ Basic story generation failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Error in basic story test: {e}")
        return False

def test_cultural_story():
    """Test cultural story generation."""
    print("\n🌍 Testing cultural story generation...")
    
    payload = {
        "theme": "folklore",
        "culture": "Indian",
        "language": "English"
    }
    
    try:
        print("   Generating cultural story...")
        response = requests.post(f"{API_BASE}/cultural-story", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Cultural story generated successfully!")
            print(f"   Story length: {len(result['story'])} characters")
            print(f"   Theme: {result.get('theme')}")
            print(f"   Culture: {result.get('culture')}")
            print(f"   Cultural fact: {result.get('cultural_fact', 'None')[:100]}...")
            print(f"   Audio file: {result.get('audio', 'Not generated')}")
            print(f"   Image file: {result.get('image', 'Not generated')}")
            
            # Check if files exist
            if result.get('audio') and os.path.exists(result['audio']):
                print("✅ Cultural audio file created successfully")
            else:
                print("⚠️ Cultural audio file not found")
                
            if result.get('image') and os.path.exists(result['image']):
                print("✅ Cultural image file created successfully")
            else:
                print("⚠️ Cultural image file not found")
                
            return True
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ Cultural story generation failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Error in cultural story test: {e}")
        return False

def test_themed_image():
    """Test themed image generation."""
    print("\n🖼️ Testing themed image generation...")
    
    payload = {
        "theme": "ancient temple",
        "culture": "Japanese"
    }
    
    try:
        print("   Generating themed image...")
        response = requests.post(f"{API_BASE}/themed-image", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Themed image generated successfully!")
            print(f"   Theme: {result.get('theme')}")
            print(f"   Culture: {result.get('culture')}")
            print(f"   Image file: {result.get('image', 'Not generated')}")
            
            if result.get('image') and os.path.exists(result['image']):
                print("✅ Themed image file created successfully")
            else:
                print("⚠️ Themed image file not found")
                
            return True
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"❌ Themed image generation failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Error in themed image test: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Smart Cultural Storyteller System Tests")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Themes & Languages", test_themes_and_languages),
        ("Basic Story", test_basic_story),
        ("Cultural Story", test_cultural_story),
        ("Themed Image", test_themed_image)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "="*60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Smart Cultural Storyteller is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        
    print("\n📋 Next Steps:")
    print("1. Start the Flask backend: python app.py")
    print("2. Start the Streamlit frontend: streamlit run frontend/streamlit_app.py")
    print("3. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()
