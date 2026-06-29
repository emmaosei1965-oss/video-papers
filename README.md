# 🎬 Picture to Video with Voice Cloning

Transform static images into videos with perfectly cloned voices! Built for efficiency on RTX 5060 (16GB RAM).

## 🎯 Features

- **Voice Cloning**: Upload a reference voice and clone it for your text
- **Image to Video**: Convert static images into dynamic videos with effects
- **Audio Synchronization**: Perfectly sync generated audio with video
- **Multiple Effects**: Zoom, Pan, or Static animations
- **Optimized Performance**: Designed for RTX 5060 with 16GB RAM
- **Open Source**: 100% local processing, no cloud dependencies
- **Two Interfaces**: CLI for power users, Web UI for everyone

## 📋 Requirements

- **GPU**: NVIDIA RTX 5060 or similar (16GB VRAM)
- **RAM**: 16GB minimum
- **Python**: 3.8+
- **CUDA**: 12.1+
- **FFmpeg**: For audio/video processing

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/emmaosei1965-oss/video-papers
cd video-papers

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### 2. Prepare Input Files

```
video-papers/
├── input_images/
│   └── your_image.jpg
├── sample_voices/
│   └── reference_voice.wav
└── output_videos/
```

Upload your image and reference voice sample to respective directories.

### 3. Generate Video

**Option A: Command Line**
```bash
python main.py \
  --image input_images/photo.jpg \
  --text "Hello! This is your cloned voice" \
  --voice sample_voices/reference.wav \
  --effect zoom \
  --duration 5
```

**Option B: Web Interface**
```bash
python gradio_app.py
# Open http://localhost:7860 in your browser
```

## 📖 Detailed Usage

### Command Line Arguments

```
--image      : Path to input image (required)
--text       : Text to synthesize (required)
--voice      : Path to reference voice sample (required)
--output     : Path to output video (optional, auto-generated if not provided)
--effect     : Animation effect - zoom, pan, or static (default: zoom)
--duration   : Video duration in seconds (default: 5)
```

### Examples

**Simple Example**
```bash
python main.py \
  --image photo.jpg \
  --text "Welcome to my channel" \
  --voice my_voice.wav
```

**With Custom Effects**
```bash
python main.py \
  --image photo.jpg \
  --text "Check this out" \
  --voice voice_sample.wav \
  --effect pan \
  --duration 8 \
  --output custom_output.mp4
```

**Batch Processing**
```python
from main import PictureToVideoProcessor

processor = PictureToVideoProcessor()

pairs = [
    ("image1.jpg", "First text"),
    ("image2.jpg", "Second text"),
]

processor.process_batch(
    image_text_pairs=pairs,
    reference_voice_path="voice.wav",
    video_effect="zoom",
    video_duration=5
)
```

## 🎨 Animation Effects

### Zoom
Smoothly zooms in on the image (default effect)
- Good for: Portraits, focus on details
- Duration: Any length

### Pan
Moves across the image horizontally
- Good for: Landscapes, wide shots
- Duration: Any length

### Static
Holds the image steady
- Good for: Minimal motion preference
- Duration: Any length

## 🔊 Voice Cloning

### How It Works

1. **Reference Voice Upload**: Provide a clear audio sample (10-30 seconds)
2. **Feature Extraction**: System extracts unique voice characteristics
3. **Text Synthesis**: Converts your text to speech using the cloned voice
4. **Audio Sync**: Synchronizes audio perfectly with video timing

### Best Practices for Reference Voice

- ✅ Clear, high-quality audio
- ✅ 10-30 seconds in length
- ✅ Single speaker only
- ✅ Minimal background noise
- ✅ Natural speaking tone

- ❌ Avoid compressed audio (MP3 with low bitrate)
- ❌ Avoid multiple speakers
- ❌ Avoid heavy accents (for best results)
- ❌ Avoid very short samples (<5 seconds)

## 💾 Configuration

Edit `config.py` to customize:

```python
# Device settings
DEVICE = "cuda"              # GPU device
USE_HALF_PRECISION = True   # FP16 for memory efficiency
BATCH_SIZE = 2              # Reduced for 16GB VRAM

# Video settings
VIDEO_FPS = 24              # Frames per second
VIDEO_DURATION_SECONDS = 5  # Default duration
OUTPUT_RESOLUTION = (1024, 768)  # Width x Height

# Audio settings
AUDIO_SAMPLE_RATE = 22050   # Audio quality
```

## 📊 Performance Tips

### Memory Optimization (16GB RAM)
- ✓ Half precision (FP16) enabled by default
- ✓ Batch size limited to 2
- ✓ Gradient checkpointing available
- ✓ Smart memory allocation

### Speed Improvements
- Use shorter videos (5-10 seconds)
- Lower resolution if needed: `OUTPUT_RESOLUTION = (512, 384)`
- Use "static" effect for fastest processing
- Batch process multiple videos

### Quality Settings
- Keep `VIDEO_FPS = 24` for balanced quality/speed
- Increase `AUDIO_SAMPLE_RATE` for better audio (higher = slower)
- Use high-quality reference voice samples
- Provide clear text input (avoid very long sentences)

## 🛠️ Troubleshooting

### Out of Memory Error
```
Solution 1: Reduce resolution
config.py: OUTPUT_RESOLUTION = (512, 384)

Solution 2: Reduce video duration
python main.py ... --duration 3

Solution 3: Use CPU (slower)
config.py: DEVICE = "cpu"
```

### Voice Cloning Quality Issues
```
- Ensure reference voice is clear and 10-30 seconds
- Try different reference voice samples
- Check text doesn't exceed 100 characters
- Verify sample rate is 22050 Hz
```

### FFmpeg Not Found
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Video Codec Issues
```
Try alternative codec in config.py:
CODEC = "libx264"  # Or "mpeg4", "libxvpq"
```

## 📁 Directory Structure

```
video-papers/
├── config.py              # Configuration settings
├── main.py                # CLI entry point
├── gradio_app.py          # Web UI
├── voice_cloner.py        # Voice cloning module
├── video_generator.py     # Video generation module
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── README.md             # This file
├── input_images/         # Input images
├── sample_voices/        # Reference voice samples
├── output_videos/        # Generated videos
├── temp/                 # Temporary files
└── models/               # Downloaded models
    └── openvoice/        # OpenVoice model cache
```

## 🔑 Key Technologies

- **PyTorch**: Deep learning framework
- **OpenVoice**: Advanced voice cloning
- **FFmpeg**: Audio/video processing
- **Librosa**: Audio analysis
- **OpenCV**: Image processing
- **Gradio**: Web interface framework

## 📝 Voice Cloning Methods

### Method 1: OpenVoice (Recommended)
- Best quality voice cloning
- Handles different accents well
- Requires more GPU memory

### Method 2: TTS + Voice Conversion
- Fallback if OpenVoice unavailable
- Lower quality but still good
- More memory efficient

### Method 3: gTTS (Fallback)
- Simple text-to-speech
- No voice cloning
- Used if other methods fail

## 🎓 Advanced Usage

### Custom Voice Effects
```python
from voice_cloner import VoiceCloner

cloner = VoiceCloner(device="cuda")
cloner.apply_voice_conversion(
    audio_path="generated.wav",
    reference_audio_path="reference.wav",
    output_path="converted.wav"
)
```

### Programmatic API
```python
from main import PictureToVideoProcessor

processor = PictureToVideoProcessor()
processor.process_workflow(
    image_path="photo.jpg",
    text_input="Your text here",
    reference_voice_path="voice.wav",
    output_video_path="output.mp4",
    video_effect="zoom",
    video_duration=5.0
)
```

## 🐛 Known Limitations

1. **16GB VRAM Constraint**: Large batch processing not possible
2. **Single Speaker**: Only one voice can be cloned per session
3. **Audio Length**: Keep text under 100 characters for best results
4. **Frame Rate**: Limited to 24-30 FPS for smooth performance
5. **Resolution**: Keep under 1024x768 for memory efficiency

## 📈 Future Improvements

- [ ] Multi-speaker support
- [ ] Real-time preview
- [ ] Batch UI processing
- [ ] Additional animation effects
- [ ] Video effects (filters, transitions)
- [ ] Subtitle generation
- [ ] Multi-language support

## 📄 License

This project is open source and available under MIT License.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 💬 Support

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Check README and code comments

## ⚠️ System Requirements

**Minimum:**
- GPU: RTX 5060 or similar (>8GB VRAM)
- RAM: 16GB
- Python: 3.8+

**Recommended:**
- GPU: RTX 4060 Ti or better (12GB+ VRAM)
- RAM: 32GB
- SSD with 50GB free space

## 🎬 Example Workflow

1. Take a photo → `input_images/photo.jpg`
2. Record voice sample → `sample_voices/my_voice.wav`
3. Create script: `"Welcome to my presentation"`
4. Run: `python main.py --image input_images/photo.jpg --text "Welcome to my presentation" --voice sample_voices/my_voice.wav`
5. Check result: `output_videos/photo_video.mp4`

---

**Made with ❤️ for content creators using RTX 5060**

*Transform your images into engaging videos with your own cloned voice - no subscriptions, no limitations!*
