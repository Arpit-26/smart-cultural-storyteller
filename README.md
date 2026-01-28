# 🌍 Smart Cultural Storyteller

An AI-powered storytelling platform that generates culturally rich stories with multi-language narration and AI-generated imagery. Optimized for low-spec machines with lightweight, efficient components.

## ✨ Features

- 🧠 **Local Story Generation** - Uses Orca Mini 3B GGUF model (lightweight, no internet required)
- 🎙️ **Multi-language Narration** - ElevenLabs TTS with support for 10+ languages
- 🎨 **Free Image Generation** - Pollinations.ai API (no heavy local models)
- 🌍 **Cultural Themes** - Folklore, mythology, festivals, heroes, wisdom tales, and more
- 💡 **Cultural Facts** - Educational content about different cultures
- 📱 **User-friendly Interface** - Streamlit web app with intuitive design
- 💾 **Download Support** - Save generated audio and images
- 🎬 **Video Creation** - Generate story videos with multiple scenes and narration

## 🏗️ Project Structure

```
Smart Cultural Storyteller/
├── app.py                       # Flask API server
├── storyteller.py               # TTS & cultural logic
├── video_creator.py             # Video creation utilities
├── video_compiler.py            # Video compilation logic
├── tts_helper.py                # Text-to-speech helper
├── models/
│   ├── story_generator.py       # Orca Mini 3B integration
│   ├── image_generator.py       # Pollinations.ai API
│   └── q4_0-orca-mini-3b.gguf  # Local AI model (MANUAL DOWNLOAD REQUIRED)
├── frontend/
│   └── streamlit_app.py         # Web interface
├── static/                      # Generated files (images, audio, videos)
├── .env                         # API keys
├── requirements.txt             # Dependencies
└── test_system.py              # System tests
```

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **ElevenLabs API key** (for text-to-speech)
- **4GB+ RAM** (for Orca Mini 3B model)
- **FFmpeg** (for video creation - optional but recommended)

### Step 1: Download and Setup

1. **Download the project folder** to your local machine

2. **Navigate to the project directory:**
   ```bash
   cd "Smart Cultural Storyteller"
   ```

### Step 2: Install Python Dependencies

1. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   **Windows:**

   ```bash
   venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   source venv/bin/activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Download the Orca Mini Model (REQUIRED)

⚠️ **IMPORTANT:** The AI model file is NOT included in this project due to its large size (~2GB). You must download it manually.

#### Option A: Direct Download (Recommended)

1. **Go to the Hugging Face model page:**

   - Visit: https://huggingface.co/TheBloke/orca_mini_3B-GGUF

2. **Download the specific file:**

   - Look for the file: `q4_0-orca-mini-3b.gguf`
   - Click the download button next to this file
   - File size: ~2GB (download may take 10-30 minutes depending on your internet)

3. **Place the model file:**
   - Create the `models` folder if it doesn't exist: `mkdir models`
   - Move the downloaded `q4_0-orca-mini-3b.gguf` file to the `models/` directory
   - Final path should be: `models/q4_0-orca-mini-3b.gguf`

#### Option B: Using Git LFS (Alternative)

If you prefer using git:

```bash
# Install git-lfs if not already installed
git lfs install

# Clone the model repository
git clone https://huggingface.co/TheBloke/orca_mini_3B-GGUF models_temp

# Copy the model file
cp models_temp/q4_0-orca-mini-3b.gguf models/

# Clean up
rm -rf models_temp
```

#### Verify Installation

After downloading, verify the model is in the correct location:

```bash
# Check if the file exists
ls -la models/q4_0-orca-mini-3b.gguf

# Check file size (should be around 2GB)
du -h models/q4_0-orca-mini-3b.gguf
```

**Expected output:**

```
-rw-r--r-- 1 user user 2.0G [date] models/q4_0-orca-mini-3b.gguf
```

### Step 4: Configure API Keys

1. **Create a `.env` file** in the project root directory

2. **Add your ElevenLabs API key:**

   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

   **How to get ElevenLabs API key:**

   - Go to https://elevenlabs.io/
   - Sign up for a free account
   - Go to your profile settings
   - Copy your API key

### Step 5: Install FFmpeg (Optional - for video creation)

**Windows:**

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to PATH, or follow the detailed guide in `FFMPEG_INSTALLATION.md`

**macOS:**

```bash
brew install ffmpeg
```

**Linux:**

```bash
sudo apt update
sudo apt install ffmpeg
```

### Step 6: Run the Application

1. **Start the backend server:**

   ```bash
   python app.py
   ```

   - The API will be available at `http://localhost:5000`
   - Keep this terminal window open

2. **Start the frontend (in a new terminal):**

   ```bash
   streamlit run frontend/streamlit_app.py
   ```

   - The web interface will open at `http://localhost:8501`
   - Your browser should open automatically

3. **Test the system (optional):**
   ```bash
   python test_system.py
   ```

## 🎯 Usage

### Web Interface

1. Open your browser to `http://localhost:8501`
2. Choose your preferred mode:
   - **Basic Story**: Simple story generation
   - **Cultural Story**: Themed stories with cultural context
   - **Video Story**: Create videos with multiple scenes
3. Select language, culture, and theme
4. Generate and download your content

### API Endpoints

- `POST /api/story` - Generate basic story with audio and image
- `POST /api/cultural-story` - Generate culturally-themed story
- `POST /api/video-story` - Generate story with video
- `GET /api/themes` - Get available cultural themes
- `GET /api/languages` - Get supported languages
- `GET /api/health` - Health check

### Example API Usage

```python
import requests

# Generate a cultural story
payload = {
    "theme": "folklore",
    "culture": "Indian",
    "language": "English"
}

response = requests.post("http://localhost:5000/api/cultural-story", json=payload)
result = response.json()

print(f"Story: {result['story']}")
print(f"Audio: {result['audio']}")
print(f"Image: {result['image']}")
print(f"Cultural Fact: {result['cultural_fact']}")
```

## 📋 System Requirements

### Minimum Requirements

- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free space
- **Python**: 3.8+ (3.9+ recommended)
- **Internet**: Required for ElevenLabs API and image generation

### Recommended Requirements

- **RAM**: 8GB+
- **Storage**: 10GB free space
- **Python**: 3.9+
- **FFmpeg**: For video creation features

## 🌍 Supported Features

### Cultural Themes

- **Folklore** - Traditional folk tales and legends
- **Mythology** - Ancient myths and divine stories
- **Festivals** - Cultural celebrations and traditions
- **Heroes** - Cultural heroes and legendary figures
- **Wisdom** - Traditional wisdom and moral tales
- **Nature** - Stories about nature and animals
- **Family** - Family values and relationships
- **Adventure** - Cultural adventures and journeys

### Supported Languages

English, Spanish, French, German, Italian, Portuguese, Hindi, Chinese, Japanese, Korean

### Cultural Contexts

Indian, Chinese, Japanese, African, European, Native American, Middle Eastern, Latin American

## 🔧 Configuration

### Model Settings

The Orca Mini 3B model is configured for optimal performance on low-spec machines:

- Max tokens: 400-500 (adjustable)
- Temperature: 0.7 (creative but coherent)
- Top-p: 0.9 (diverse vocabulary)

### Image Generation

Pollinations.ai settings:

- Default size: 512x512
- Styles: fantasy, traditional cultural, etc.
- Free tier: No API key required

### Audio Generation

ElevenLabs configuration:

- Model: eleven_multilingual_v2
- Format: MP3 44.1kHz 128kbps
- Voice: Configurable per language

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

This tests:

- Backend health and connectivity
- Theme and language endpoints
- Basic story generation
- Cultural story generation
- Image generation
- File creation and accessibility

## 📊 Performance Optimization

### For Low-Spec Machines:

- **Removed heavy dependencies**: No PyTorch, Transformers, or local Stable Diffusion
- **Lightweight model**: Orca Mini 3B (quantized) instead of larger models
- **API-based images**: Pollinations.ai instead of local generation
- **Efficient memory usage**: Model loaded once and cached
- **Reasonable token limits**: Prevents memory overflow

### Memory Usage:

- Orca Mini 3B: ~2-3GB RAM
- Flask backend: ~100-200MB
- Streamlit frontend: ~50-100MB
- **Total**: ~3-4GB RAM (suitable for most modern computers)

## 🛠️ Development

### Adding New Cultural Themes

Edit `storyteller.py`:

```python
CULTURAL_THEMES = {
    "your_theme": "Description of your theme",
    # ... existing themes
}
```

### Adding New Languages

Update the voice mapping in `storyteller.py`:

```python
VOICE_MAPPING = {
    "YourLanguage": "elevenlabs_voice_id",
    # ... existing languages
}
```

### Adding Cultural Facts

Extend the cultural facts dictionary in `storyteller.py`:

```python
cultural_facts = {
    "YourCulture": "Interesting fact about the culture",
    # ... existing cultures
}
```

## 🐛 Troubleshooting

### Common Issues:

1. **"ELEVENLABS_API_KEY is missing"**

   - Ensure `.env` file exists in the project root directory
   - Check that the API key is correctly formatted
   - Verify the file is not named `.env.txt` (should be just `.env`)

2. **"Cannot connect to backend"**

   - Start Flask app first: `python app.py`
   - Check if port 5000 is available
   - Ensure you're in the correct directory when running commands

3. **"Model file not found" or "q4_0-orca-mini-3b.gguf not found"**

   - **This is the most common issue!** The model file must be downloaded manually
   - Go to: https://huggingface.co/TheBloke/orca_mini_3B-GGUF
   - Download `q4_0-orca-mini-3b.gguf` (about 2GB)
   - Place it in the `models/` directory
   - Ensure the file path is exactly: `models/q4_0-orca-mini-3b.gguf`

4. **"Image generation failed"**

   - Check internet connection (Pollinations.ai requires internet)
   - Verify the API endpoint is accessible
   - Try again after a few minutes (rate limiting)

5. **"Video creation failed" or "FFmpeg not found"**

   - Install FFmpeg following the instructions in Step 5
   - Ensure FFmpeg is added to your system PATH
   - Check the detailed guide in `FFMPEG_INSTALLATION.md`

6. **Memory issues or "Out of memory"**

   - Close other applications to free RAM
   - The model requires at least 4GB RAM
   - Consider upgrading RAM if possible

7. **"Module not found" errors**

   - Ensure you've activated your virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

8. **Streamlit not opening**
   - Check if port 8501 is available
   - Try: `streamlit run frontend/streamlit_app.py --server.port 8502`
   - Ensure the backend is running first

## 📝 License

This project is open source. Please ensure you comply with:

- ElevenLabs API terms of service
- Pollinations.ai usage terms
- Orca Mini model license
- Any other third-party service terms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ✅ Quick Setup Checklist

Before running the application, ensure you have completed all these steps:

- [ ] **Python 3.8+ installed**
- [ ] **Project folder downloaded**
- [ ] **Virtual environment created and activated**
- [ ] **Dependencies installed** (`pip install -r requirements.txt`)
- [ ] **Orca Mini model downloaded** (`q4_0-orca-mini-3b.gguf` in `models/` folder)
- [ ] **ElevenLabs API key obtained and added to `.env` file**
- [ ] **FFmpeg installed** (optional, for video features)
- [ ] **Backend server started** (`python app.py`)
- [ ] **Frontend started** (`streamlit run frontend/streamlit_app.py`)

## 📞 Support

For issues and questions:

1. **Check the troubleshooting section above**
2. **Run the test suite:** `python test_system.py`
3. **Check API health:** Visit `http://localhost:5000/api/health`
4. **Verify model file:** Ensure `models/q4_0-orca-mini-3b.gguf` exists
5. **Check logs:** Look at terminal output for error messages

## 🎉 What's Next?

Once everything is set up, you can:

- Generate stories in multiple languages
- Create culturally-themed content
- Produce story videos with multiple scenes
- Download audio, images, and videos
- Explore different cultural themes and contexts

---

**Happy Storytelling! 🎭📚✨**

_Built with ❤️ for cultural preservation and storytelling_
