"""
Configuration settings for Picture to Video with Voice Cloning
Optimized for RTX 5060 (16GB RAM)
"""

import os

# Device settings
DEVICE = "cuda"  # Use GPU
USE_HALF_PRECISION = True  # FP16 for memory efficiency
BATCH_SIZE = 2  # Reduced for 16GB VRAM

# Model settings
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
OPENVOICE_MODEL_DIR = os.path.join(MODELS_DIR, "openvoice")

# Input/Output
INPUT_DIR = "input_images"
OUTPUT_DIR = "output_videos"
TEMP_DIR = "temp"
SAMPLE_VOICES_DIR = "sample_voices"

# Video settings
VIDEO_FPS = 24
VIDEO_DURATION_SECONDS = 5
OUTPUT_RESOLUTION = (1024, 768)  # Width x Height

# Audio settings
AUDIO_SAMPLE_RATE = 22050
VOICE_CLONING_QUALITY = "high"  # high, medium, low

# Model configs
OPENVOICE_VOICE_CONVERSION = True
WHISPER_MODEL = "base"  # base, small, medium, large

# Memory optimization
ENABLE_MEMORY_EFFICIENT = True
GRADIENT_CHECKPOINTING = False

# Directories to create
DIRS_TO_CREATE = [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, SAMPLE_VOICES_DIR, MODELS_DIR, OPENVOICE_MODEL_DIR]
