import base64
import io
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from config import config

class AudioProcessor:
    """Handles audio processing and feature extraction"""
    
    def __init__(self):
        self.sample_rate = config.SAMPLE_RATE
        
    def base64_to_audio(self, base64_string: str) -> tuple:
        """
        Convert base64 encoded audio to numpy array
        
        Args:
            base64_string: Base64 encoded MP3 audio
            
        Returns:
            tuple: (audio_array, sample_rate)
        """
        try:
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(base64_string)
            
            # Load audio using pydub (handles MP3)
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
            
            # Convert to numpy array
            samples = np.array(audio_segment.get_array_of_samples())
            
            # Convert to float32 and normalize
            if audio_segment.sample_width == 2:  # 16-bit audio
                samples = samples.astype(np.float32) / 32768.0
            elif audio_segment.sample_width == 4:  # 32-bit audio
                samples = samples.astype(np.float32) / 2147483648.0
                
            # Handle stereo by averaging channels
            if audio_segment.channels == 2:
                samples = samples.reshape((-1, 2)).mean(axis=1)
            
            original_sr = audio_segment.frame_rate
            
            # Resample to target sample rate if needed
            if original_sr != self.sample_rate:
                samples = librosa.resample(samples, orig_sr=original_sr, target_sr=self.sample_rate)
            
            return samples, self.sample_rate
            
        except Exception as e:
            raise ValueError(f"Error processing audio: {str(e)}")
    
    def extract_features(self, audio_array: np.ndarray, sr: int) -> dict:
        """
        Extract audio features for AI voice detection
        
        Args:
            audio_array: Audio signal as numpy array
            sr: Sample rate
            
        Returns:
            dict: Extracted features
        """
        features = {}
        
        try:
            # 1. MFCC (Mel-frequency cepstral coefficients)
            # AI voices often have more consistent MFCC patterns
            mfcc = librosa.feature.mfcc(
                y=audio_array, 
                sr=sr, 
                n_mfcc=config.N_MFCC,
                hop_length=config.HOP_LENGTH
            )
            features['mfcc_mean'] = np.mean(mfcc, axis=1)
            features['mfcc_std'] = np.std(mfcc, axis=1)
            features['mfcc_var'] = np.var(mfcc, axis=1)
            
            # 2. Spectral Centroid
            # AI voices tend to have different spectral characteristics
            spectral_centroids = librosa.feature.spectral_centroid(
                y=audio_array, 
                sr=sr,
                hop_length=config.HOP_LENGTH
            )[0]
            features['spectral_centroid_mean'] = np.mean(spectral_centroids)
            features['spectral_centroid_std'] = np.std(spectral_centroids)
            features['spectral_centroid_var'] = np.var(spectral_centroids)
            
            # 3. Zero Crossing Rate
            # Measures how often the signal changes sign
            zcr = librosa.feature.zero_crossing_rate(
                audio_array,
                hop_length=config.HOP_LENGTH
            )[0]
            features['zcr_mean'] = np.mean(zcr)
            features['zcr_std'] = np.std(zcr)
            
            # 4. Spectral Rolloff
            # Frequency below which a certain percentage of spectral energy is contained
            rolloff = librosa.feature.spectral_rolloff(
                y=audio_array, 
                sr=sr,
                hop_length=config.HOP_LENGTH
            )[0]
            features['spectral_rolloff_mean'] = np.mean(rolloff)
            features['spectral_rolloff_std'] = np.std(rolloff)
            
            # 5. Chroma Features
            # Pitch class profiles
            chroma = librosa.feature.chroma_stft(
                y=audio_array, 
                sr=sr,
                hop_length=config.HOP_LENGTH
            )
            features['chroma_mean'] = np.mean(chroma, axis=1)
            features['chroma_std'] = np.std(chroma, axis=1)
            
            # 6. RMS Energy
            # Root mean square energy
            rms = librosa.feature.rms(
                y=audio_array,
                hop_length=config.HOP_LENGTH
            )[0]
            features['rms_mean'] = np.mean(rms)
            features['rms_std'] = np.std(rms)
            features['rms_var'] = np.var(rms)
            
            # 7. Mel Spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=audio_array, 
                sr=sr,
                hop_length=config.HOP_LENGTH
            )
            features['mel_spec_mean'] = np.mean(mel_spec)
            features['mel_spec_std'] = np.std(mel_spec)
            
            # 8. Spectral Contrast
            # Difference between peaks and valleys in spectrum
            contrast = librosa.feature.spectral_contrast(
                y=audio_array, 
                sr=sr,
                hop_length=config.HOP_LENGTH
            )
            features['spectral_contrast_mean'] = np.mean(contrast, axis=1)
            features['spectral_contrast_std'] = np.std(contrast, axis=1)
            
            # 9. Tonnetz (Tonal Centroid Features)
            # Harmonic features
            tonnetz = librosa.feature.tonnetz(
                y=audio_array, 
                sr=sr
            )
            features['tonnetz_mean'] = np.mean(tonnetz, axis=1)
            features['tonnetz_std'] = np.std(tonnetz, axis=1)
            
            return features
            
        except Exception as e:
            raise ValueError(f"Error extracting features: {str(e)}")
    
    def flatten_features(self, features: dict) -> np.ndarray:
        """
        Flatten feature dictionary into a single array
        
        Args:
            features: Dictionary of features
            
        Returns:
            np.ndarray: Flattened feature vector
        """
        feature_list = []
        
        for key in sorted(features.keys()):
            value = features[key]
            if isinstance(value, np.ndarray):
                feature_list.extend(value.flatten())
            else:
                feature_list.append(value)
        
        return np.array(feature_list)
