#!/bin/bash

# Setup script for Picture to Video with Voice Cloning
# Optimized for RTX 5060 (16GB RAM)

echo "================================================"
echo "Picture to Video with Voice Cloning - Setup"
echo "System: RTX 5060 (16GB RAM)"
echo "================================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install PyTorch with CUDA support (RTX 5060)
echo ""
echo "Installing PyTorch with CUDA 12.1 support..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Download models
echo ""
echo "Downloading required models..."
echo "This may take a few minutes..."

# Create models directory
mkdir -p models/openvoice

# Install TTS (Text-to-Speech)
echo "Installing TTS engine..."
pip install TTS

# Download OpenVoice models (if using)
# python -c "from openvoice import se_extractor; print('OpenVoice ready')"

echo ""
echo "================================================"
echo "✓ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Run CLI: python main.py --image <img> --text <text> --voice <sample.wav>"
echo "3. Or run Web UI: python gradio_app.py"
echo ""
echo "Example:"
echo "  python main.py --image photo.jpg --text 'Hello world' --voice voice_sample.wav"
echo ""
