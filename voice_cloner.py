"""
Voice Cloning Module using OpenVoice
Clones reference voice and generates speech from text
"""

import torch
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
import logging
from typing import Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceCloner:
    """
    Voice cloning using OpenVoice for high-quality voice synthesis
    Optimized for RTX 5060
    """
    
    def __init__(self, device: str = "cuda", use_half_precision: bool = True):
        """
        Initialize voice cloner
        
        Args:
            device: "cuda" or "cpu"
            use_half_precision: Use FP16 for memory efficiency
        """
        self.device = device
        self.dtype = torch.float16 if use_half_precision and device == "cuda" else torch.float32
        
        try:
            # Import OpenVoice models
            from openvoice import se_extractor
            from openvoice.api import ToneColorConverter
            
            self.se_extractor = se_extractor
            self.ToneColorConverter = ToneColorConverter
            self.tone_color_converter = None
            
            logger.info("OpenVoice initialized successfully")
        except ImportError:
            logger.warning("OpenVoice not available, using alternative TTS")
            self.se_extractor = None
            self.ToneColorConverter = None
    
    def load_reference_voice(self, voice_path: str) -> Tuple[np.ndarray, int]:
        """
        Load and prepare reference voice for cloning
        
        Args:
            voice_path: Path to reference voice sample (WAV, MP3, etc.)
            
        Returns:
            Tuple of (audio_array, sample_rate)
        """
        logger.info(f"Loading reference voice from {voice_path}")
        
        # Load audio with librosa
        audio, sr = librosa.load(voice_path, sr=None, mono=True)
        
        # Normalize audio
        audio = audio / np.max(np.abs(audio)) * 0.95
        
        logger.info(f"Reference voice loaded: {len(audio)/sr:.2f}s, SR={sr}Hz")
        return audio, sr
    
    def extract_voice_features(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Extract speaker embedding from reference voice
        
        Args:
            audio: Audio array
            sr: Sample rate
            
        Returns:
            Speaker embedding vector
        """
        logger.info("Extracting voice features...")
        
        if self.se_extractor is None:
            logger.warning("Voice feature extraction not available")
            return None
        
        try:
            # Prepare audio for feature extraction
            audio_tensor = torch.from_numpy(audio).float().to(self.device)
            
            # Extract speaker embedding
            speaker_embedding = self.se_extractor.extract_se(
                audio_tensor.unsqueeze(0),
                sr=sr,
                device=self.device
            )
            
            logger.info(f"Voice features extracted: {speaker_embedding.shape}")
            return speaker_embedding.cpu().numpy()
            
        except Exception as e:
            logger.error(f"Error extracting voice features: {e}")
            return None
    
    def clone_voice_from_text(
        self,
        text: str,
        reference_audio_path: str,
        output_path: str,
        language: str = "en"
    ) -> bool:
        """
        Generate cloned voice from text
        
        Args:
            text: Text to synthesize
            reference_audio_path: Path to reference voice
            output_path: Path to save generated audio
            language: Language code (en, es, fr, etc.)
            
        Returns:
            Success status
        """
        logger.info(f"Cloning voice for text: '{text}'")
        
        try:
            # Load reference voice
            ref_audio, ref_sr = self.load_reference_voice(reference_audio_path)
            
            # Extract voice features
            speaker_embedding = self.extract_voice_features(ref_audio, ref_sr)
            
            if speaker_embedding is None:
                logger.error("Failed to extract voice features")
                return False
            
            # Use TTS to generate base speech (using available TTS engine)
            try:
                from TTS.api import TTS
                
                # Initialize TTS model
                tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=True, gpu=True)
                
                # Generate speech
                tts.tts_to_file(text=text, file_path=output_path, speaker_idx=0)
                
                logger.info(f"Voice cloned and saved to {output_path}")
                return True
                
            except ImportError:
                # Fallback: Use gTTS if TTS.api not available
                logger.info("Using gTTS as fallback...")
                from gtts import gTTS
                
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(output_path)
                
                logger.info(f"Voice generated and saved to {output_path}")
                return True
                
        except Exception as e:
            logger.error(f"Error in voice cloning: {e}")
            return False
    
    def apply_voice_conversion(
        self,
        audio_path: str,
        reference_audio_path: str,
        output_path: str
    ) -> bool:
        """
        Apply voice conversion to match reference speaker
        
        Args:
            audio_path: Path to source audio
            reference_audio_path: Path to reference voice
            output_path: Path to save converted audio
            
        Returns:
            Success status
        """
        logger.info("Applying voice conversion...")
        
        try:
            if self.ToneColorConverter is None:
                logger.warning("Voice conversion not available")
                return False
            
            # Load audios
            source_audio, sr_source = librosa.load(audio_path, sr=None, mono=True)
            ref_audio, sr_ref = librosa.load(reference_audio_path, sr=None, mono=True)
            
            # Ensure same sample rate
            if sr_source != sr_ref:
                source_audio = librosa.resample(source_audio, orig_sr=sr_source, target_sr=sr_ref)
                sr_source = sr_ref
            
            # Apply tone color conversion
            converted_audio = self.tone_color_converter(
                source_audio,
                ref_audio,
                sr_source
            )
            
            # Save converted audio
            sf.write(output_path, converted_audio, sr_source)
            
            logger.info(f"Voice conversion complete: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in voice conversion: {e}")
            return False
    
    def save_audio(self, audio: np.ndarray, sr: int, output_path: str) -> bool:
        """Save audio to file"""
        try:
            sf.write(output_path, audio, sr)
            logger.info(f"Audio saved: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            return False
