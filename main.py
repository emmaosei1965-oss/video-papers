"""
Main Pipeline: Picture to Video with Voice Cloning
Complete workflow for creating videos with cloned voices
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional
import argparse

from config import *
from voice_cloner import VoiceCloner
from video_generator import VideoGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PictureToVideoProcessor:
    """
    Main processor for converting pictures to videos with voice cloning
    """
    
    def __init__(self):
        """Initialize the processor"""
        self.setup_directories()
        
        # Initialize components
        self.voice_cloner = VoiceCloner(
            device=DEVICE,
            use_half_precision=USE_HALF_PRECISION
        )
        
        self.video_generator = VideoGenerator(
            fps=VIDEO_FPS,
            resolution=OUTPUT_RESOLUTION,
            device=DEVICE
        )
        
        logger.info("PictureToVideoProcessor initialized")
    
    def setup_directories(self):
        """Create required directories"""
        for dir_path in DIRS_TO_CREATE:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ready: {dir_path}")
    
    def process_workflow(
        self,
        image_path: str,
        text_input: str,
        reference_voice_path: str,
        output_video_path: str,
        video_effect: str = "zoom",
        video_duration: float = 5.0
    ) -> bool:
        """
        Complete workflow: Text → Audio → Video → Audio Sync
        
        Args:
            image_path: Path to input image
            text_input: Text to synthesize
            reference_voice_path: Path to reference voice sample
            output_video_path: Path to save final video
            video_effect: Animation effect for video
            video_duration: Duration of video in seconds
            
        Returns:
            Success status
        """
        logger.info("=" * 60)
        logger.info("Starting Picture to Video with Voice Cloning Pipeline")
        logger.info("=" * 60)
        
        try:
            # Step 1: Clone voice from text
            logger.info("\n[Step 1/4] Voice Cloning...")
            cloned_audio_path = os.path.join(TEMP_DIR, "cloned_voice.wav")
            
            if not self.voice_cloner.clone_voice_from_text(
                text=text_input,
                reference_audio_path=reference_voice_path,
                output_path=cloned_audio_path
            ):
                logger.error("Failed to clone voice")
                return False
            
            logger.info(f"✓ Voice cloned: {cloned_audio_path}")
            
            # Step 2: Generate video from image
            logger.info("\n[Step 2/4] Generating Video from Image...")
            temp_video_path = os.path.join(TEMP_DIR, "temp_video.mp4")
            
            temp_video = self.video_generator.create_video_from_image(
                image_path=image_path,
                duration_seconds=video_duration,
                effect=video_effect,
                output_path=temp_video_path
            )
            
            if temp_video is None:
                logger.error("Failed to generate video")
                return False
            
            logger.info(f"✓ Video generated: {temp_video}")
            
            # Step 3: Sync audio with video
            logger.info("\n[Step 3/4] Syncing Audio with Video...")
            
            if not self.video_generator.sync_audio_to_video(
                audio_path=cloned_audio_path,
                video_path=temp_video,
                output_path=output_video_path
            ):
                logger.error("Failed to sync audio")
                return False
            
            logger.info(f"✓ Audio synced with video: {output_video_path}")
            
            # Step 4: Cleanup temp files
            logger.info("\n[Step 4/4] Cleaning up temporary files...")
            import shutil
            for temp_file in [cloned_audio_path, temp_video]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            logger.info("=" * 60)
            logger.info("✓ Pipeline Complete!")
            logger.info(f"Final video saved: {output_video_path}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            return False
    
    def process_batch(
        self,
        image_text_pairs: list,
        reference_voice_path: str,
        output_dir: str = OUTPUT_DIR,
        video_effect: str = "zoom",
        video_duration: float = 5.0
    ) -> bool:
        """
        Process multiple image-text pairs
        
        Args:
            image_text_pairs: List of tuples (image_path, text)
            reference_voice_path: Path to reference voice
            output_dir: Directory to save videos
            video_effect: Animation effect
            video_duration: Duration per video
            
        Returns:
            Success status
        """
        logger.info(f"Processing {len(image_text_pairs)} image-text pairs...")
        
        for idx, (image_path, text) in enumerate(image_text_pairs, 1):
            logger.info(f"\n[{idx}/{len(image_text_pairs)}] Processing: {image_path}")
            
            output_name = f"video_{idx:03d}.mp4"
            output_path = os.path.join(output_dir, output_name)
            
            if not self.process_workflow(
                image_path=image_path,
                text_input=text,
                reference_voice_path=reference_voice_path,
                output_video_path=output_path,
                video_effect=video_effect,
                video_duration=video_duration
            ):
                logger.warning(f"Failed to process: {image_path}")
                continue
        
        return True


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="Picture to Video with Voice Cloning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --image input.jpg --text "Hello world" --voice sample.wav
  python main.py --image input.jpg --text "Hello" --voice sample.wav --effect pan --duration 3
  python main.py --image input.jpg --text "Test" --voice sample.wav --output my_video.mp4
        """
    )
    
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--text", required=True, help="Text for voice synthesis")
    parser.add_argument("--voice", required=True, help="Path to reference voice sample")
    parser.add_argument("--output", default=None, help="Path to output video (optional)")
    parser.add_argument("--effect", choices=["zoom", "pan", "static"], default="zoom",
                       help="Video animation effect (default: zoom)")
    parser.add_argument("--duration", type=float, default=5.0,
                       help="Video duration in seconds (default: 5)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.image):
        logger.error(f"Image not found: {args.image}")
        sys.exit(1)
    
    if not os.path.exists(args.voice):
        logger.error(f"Reference voice not found: {args.voice}")
        sys.exit(1)
    
    # Set output path
    if args.output is None:
        image_name = Path(args.image).stem
        args.output = os.path.join(OUTPUT_DIR, f"{image_name}_video.mp4")
    
    # Create processor and run
    processor = PictureToVideoProcessor()
    
    success = processor.process_workflow(
        image_path=args.image,
        text_input=args.text,
        reference_voice_path=args.voice,
        output_video_path=args.output,
        video_effect=args.effect,
        video_duration=args.duration
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
