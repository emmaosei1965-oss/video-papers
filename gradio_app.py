"""
Gradio Web Interface for Picture to Video with Voice Cloning
User-friendly UI for the pipeline
"""

import gradio as gr
import os
import logging
from pathlib import Path
import tempfile

from config import *
from main import PictureToVideoProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize processor
processor = PictureToVideoProcessor()


def process_video(
    image_file,
    text_input,
    reference_voice_file,
    video_effect,
    video_duration
):
    """
    Process video with all inputs
    """
    try:
        logger.info("Starting processing...")
        
        # Create temporary paths
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            output_path = tmp.name
        
        # Run workflow
        success = processor.process_workflow(
            image_path=image_file.name,
            text_input=text_input,
            reference_voice_path=reference_voice_file.name,
            output_video_path=output_path,
            video_effect=video_effect,
            video_duration=video_duration
        )
        
        if success:
            return output_path, "✓ Video generated successfully!"
        else:
            return None, "✗ Error generating video"
            
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return None, f"✗ Error: {str(e)}"


def create_gradio_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="Picture to Video with Voice Cloning", theme=gr.themes.Soft()) as demo:
        
        gr.Markdown("""
        # 🎬 Picture to Video with Voice Cloning
        
        Transform your static images into videos with perfectly cloned voices!
        
        **How it works:**
        1. Upload an image
        2. Provide your text script
        3. Upload a reference voice sample (for voice cloning)
        4. Select animation effect
        5. Generate your video!
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📸 Input Image")
                image_input = gr.File(
                    label="Upload Image",
                    file_count="single",
                    file_types=["image"]
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 🎤 Reference Voice")
                voice_input = gr.File(
                    label="Upload Reference Voice (WAV, MP3)",
                    file_count="single",
                    file_types=["audio"]
                )
        
        gr.Markdown("### 📝 Script")
        text_input = gr.Textbox(
            label="Enter Text for Voice Synthesis",
            lines=4,
            placeholder="Type the text you want to be spoken in the video...",
            max_lines=10
        )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### ⚙️ Settings")
                effect_select = gr.Radio(
                    choices=["zoom", "pan", "static"],
                    value="zoom",
                    label="Animation Effect",
                    info="Choose how the image animates"
                )
            
            with gr.Column():
                duration_slider = gr.Slider(
                    minimum=1,
                    maximum=30,
                    value=5,
                    step=0.5,
                    label="Video Duration (seconds)"
                )
        
        with gr.Row():
            submit_btn = gr.Button("🚀 Generate Video", variant="primary", size="lg")
            clear_btn = gr.Button("🔄 Clear", size="lg")
        
        gr.Markdown("### 📹 Output Video")
        video_output = gr.Video(label="Generated Video")
        status_output = gr.Textbox(label="Status", interactive=False)
        
        # Event handlers
        submit_btn.click(
            fn=process_video,
            inputs=[image_input, text_input, voice_input, effect_select, duration_slider],
            outputs=[video_output, status_output]
        )
        
        clear_btn.click(
            fn=lambda: (None, "", None, "zoom", 5, None, ""),
            outputs=[image_input, text_input, voice_input, effect_select, duration_slider, video_output, status_output]
        )
        
        gr.Markdown("""
        ---
        ### 💡 Tips:
        - **Reference Voice**: Upload a clear audio sample (10-30 seconds) for best voice cloning quality
        - **Text**: Keep it concise for better synchronization
        - **Duration**: Should match approximately the length of your spoken text
        - **Effect**: 
          - **Zoom**: Smoothly zooms in on the image
          - **Pan**: Moves across the image
          - **Static**: Holds the image steady
        
        ### 🖥️ System Info:
        - Device: CUDA (RTX 5060)
        - RAM: 16GB
        - Max batch size: 2 frames
        - Voice Model: OpenVoice
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
