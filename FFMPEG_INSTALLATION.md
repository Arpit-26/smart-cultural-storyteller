# FFmpeg Installation Guide for Video Creation

The Video Story feature requires FFmpeg to combine multiple images with audio into MP4 videos. Here are the installation options:

## 🪟 Windows Installation

### Option 1: Manual Installation (Recommended)

1. **Download FFmpeg:**

   - Go to https://ffmpeg.org/download.html
   - Click "Windows" → "Windows builds by BtbN"
   - Download the latest release (ffmpeg-master-latest-win64-gpl.zip)

2. **Extract and Install:**

   - Extract the zip file to `C:\ffmpeg`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH:**

   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path", click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click "OK" on all dialogs

4. **Verify Installation:**
   - Open Command Prompt (cmd)
   - Type: `ffmpeg -version`
   - You should see FFmpeg version information

### Option 2: Using Chocolatey

If you have Chocolatey installed:

```bash
choco install ffmpeg
```

### Option 3: Using Scoop

If you have Scoop installed:

```bash
scoop install ffmpeg
```

### Option 4: Using Winget

```bash
winget install ffmpeg
```

## 🐧 Linux Installation

### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

### CentOS/RHEL/Fedora:

```bash
sudo dnf install ffmpeg
# or for older versions:
sudo yum install ffmpeg
```

## 🍎 macOS Installation

### Using Homebrew:

```bash
brew install ffmpeg
```

### Using MacPorts:

```bash
sudo port install ffmpeg
```

## ✅ Verification

After installation, restart your terminal/IDE and run:

```bash
ffmpeg -version
```

You should see output like:

```
ffmpeg version 4.4.2 Copyright (c) 2000-2021 the FFmpeg developers
built with gcc 10.3.0 (GCC)
...
```

## 🔧 Troubleshooting

### Windows Issues:

- **"ffmpeg is not recognized"**: PATH not set correctly

  - Restart Command Prompt/PowerShell after adding to PATH
  - Verify PATH contains `C:\ffmpeg\bin`

- **Permission errors**: Run as Administrator when adding to PATH

### General Issues:

- **Old version**: Update FFmpeg to latest version
- **Missing codecs**: Download full build, not minimal

## 🎬 After Installation

Once FFmpeg is installed:

1. Restart your Flask backend (`python app.py`)
2. Refresh the Streamlit frontend
3. The "Video Story" option will be fully enabled
4. You can create videos with multiple images and audio!

## 📋 Features Enabled with FFmpeg

- **Video Story Generation**: Complete story videos with multiple images
- **Professional MP4 output**: Compatible with all devices
- **Automatic timing**: Images synchronized with audio duration
- **High quality encoding**: H.264 video, AAC audio
- **Downloadable videos**: Save and share your cultural stories

---

**Note**: All other features (Basic Story, Cultural Story, Hindi Story) work without FFmpeg. Only the Video Story feature requires it.
