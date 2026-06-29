"""
Video Generation Module
Converts static images to videos with motion and audio sync
"""

import cv2
import numpy as np
import torch
import librosa
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image
import imageio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoGenerator:
    """
    Generate videos from static images with motion effects
    Optimized for RTX 5060
    """
    
    def __init__(
        self,
        fps: int = 24,
        resolution: Tuple[int, int] = (1024, 768),
        device: str = "cuda"
    ):
        """
        Initialize video generator
        
        Args:
            fps: Frames per second
            resolution: Output resolution (width, height)
            device: "cuda" or "cpu"
        """
        self.fps = fps
        self.resolution = resolution
        self.device = device
        
        logger.info(f"VideoGenerator initialized: {fps}fps, {resolution}, device={device}")
    
    def load_image(self, image_path: str) -> np.ndarray:
        """Load and prepare image"""
        logger.info(f"Loading image: {image_path}")
        
        image = Image.open(image_path)
        
        # Resize to target resolution
        image = image.resize(self.resolution, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image_array = np.array(image)
        logger.info(f"Image loaded: {image_array.shape}")
        
        return image_array
    
    def create_zoom_effect(
        self,
        image: np.ndarray,
        duration_seconds: float,
        zoom_factor: float = 1.2
    ) -> List[np.ndarray]:
        """
        Create zoom effect animation
        
        Args:
            image: Input image
            duration_seconds: Duration in seconds
            zoom_factor: How much to zoom (1.2 = 20% zoom)
            
        Returns:
            List of frames
        """
        logger.info(f"Creating zoom effect ({zoom_factor}x zoom)")
        
        num_frames = int(duration_seconds * self.fps)
        frames = []
        
        h, w = self.resolution
        
        for i in range(num_frames):
            # Calculate current zoom level
            progress = i / num_frames
            current_zoom = 1.0 + (zoom_factor - 1.0) * progress
            
            # Calculate crop dimensions
            crop_h = int(h / current_zoom)
            crop_w = int(w / current_zoom)
            
            # Calculate crop position (center)
            y_start = (h - crop_h) // 2
            x_start = (w - crop_w) // 2
            
            # Crop image
            cropped = image[y_start:y_start+crop_h, x_start:x_start+crop_w]
            
            # Resize back to resolution
            frame = cv2.resize(cropped, self.resolution)
            frames.append(frame)
        
        return frames
    
    def create_pan_effect(
        self,
        image: np.ndarray,
        duration_seconds: float,
        direction: str = "left_to_right"
    ) -> List[np.ndarray]:
        """
        Create pan effect animation
        
        Args:
            image: Input image
            duration_seconds: Duration in seconds
            direction: "left_to_right", "right_to_left", "top_to_bottom", "bottom_to_top"
            
        Returns:
            List of frames
        """
        logger.info(f"Creating pan effect: {direction}")
        
        num_frames = int(duration_seconds * self.fps)
        frames = []
        
        h, w = self.resolution
        pan_distance = int(w * 0.1)  # 10% of width
        
        for i in range(num_frames):
            progress = i / num_frames
            
            if direction == "left_to_right":
                offset = int(pan_distance * progress)
                frame = np.roll(image, offset, axis=1)
            elif direction == "right_to_left":
                offset = int(pan_distance * progress)
                frame = np.roll(image, -offset, axis=1)
            elif direction == "top_to_bottom":
                offset = int(pan_distance * progress)
                frame = np.roll(image, offset, axis=0)
            elif direction == "bottom_to_top":
                offset = int(pan_distance * progress)
                frame = np.roll(image, -offset, axis=0)
            else:
                frame = image
            
            frames.append(frame)
        
        return frames
    
    def create_fade_effect(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        duration_seconds: float
    ) -> List[np.ndarray]:
        """
        Create crossfade between two images
        
        Args:
            image1: First image
            image2: Second image
            duration_seconds: Duration in seconds
            
        Returns:
            List of frames
        """
        logger.info("Creating fade effect")
        
        num_frames = int(duration_seconds * self.fps)
        frames = []
        
        for i in range(num_frames):
            alpha = i / num_frames
            frame = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            frames.append(frame)
        
        return frames
    
    def create_static_frames(
        self,
        image: np.ndarray,
        duration_seconds: float
    ) -> List[np.ndarray]:
        """
        Create static image frames
        
        Args:
            image: Input image
            duration_seconds: Duration in seconds
            
        Returns:
            List of identical frames
        """
        num_frames = int(duration_seconds * self.fps)
        return [image.copy() for _ in range(num_frames)]
    
    def sync_audio_to_video(
        self,
        audio_path: str,
        video_path: str,
        output_path: str
    ) -> bool:
        """
        Sync audio with video
        
        Args:
            audio_path: Path to audio file
            video_path: Path to video file
            output_path: Path to save final video
            
        Returns:
            Success status
        """
        logger.info("Syncing audio with video...")
        
        try:
            import subprocess
            
            # Use ffmpeg to combine video and audio
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output_path,
                '-y'  # Overwrite output file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Audio synced successfully: {output_path}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error syncing audio: {e}")
            return False
    
    def generate_video_from_frames(
        self,
        frames: List[np.ndarray],
        output_path: str,
        codec: str = "mp4v"
    ) -> bool:
        """
        Save frames as video file
        
        Args:
            frames: List of frames (numpy arrays)
            output_path: Path to save video
            codec: Video codec ("mp4v", "h264", etc.)
            
        Returns:
            Success status
        """
        logger.info(f"Generating video: {output_path} ({len(frames)} frames)")
        
        try:
            # Use imageio for video writing
            writer = imageio.get_writer(output_path, fps=self.fps, codec=codec)
            
            for i, frame in enumerate(frames):
                if i % 100 == 0:
                    logger.info(f"Writing frame {i}/{len(frames)}")
                
                # Convert BGR to RGB if needed
                if len(frame.shape) == 3 and frame.shape[2] == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                writer.append_data(frame.astype(np.uint8))
            
            writer.close()
            logger.info("Video generation complete")
            return True
            
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return False
    
    def create_video_from_image(
        self,
        image_path: str,
        duration_seconds: float,
        effect: str = "zoom",
        output_path: str = None
    ) -> Optional[str]:
        """
        Create video from single image with effect
        
        Args:
            image_path: Path to image
            duration_seconds: Video duration
            effect: Animation effect ("zoom", "pan", "static")
            output_path: Path to save video
            
        Returns:
            Path to generated video or None on error
        """
        logger.info(f"Creating video from image with {effect} effect")
        
        try:
            # Load image
            image = self.load_image(image_path)
            
            # Create frames with effect
            if effect == "zoom":
                frames = self.create_zoom_effect(image, duration_seconds)
            elif effect == "pan":
                frames = self.create_pan_effect(image, duration_seconds)
            else:
                frames = self.create_static_frames(image, duration_seconds)
            
            # Generate video
            if output_path is None:
                output_path = image_path.replace(".jpg", "_video.mp4").replace(".png", "_video.mp4")
            
            if self.generate_video_from_frames(frames, output_path):
                return output_path
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return None
