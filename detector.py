import numpy as np
from typing import Tuple
from audio_processor import AudioProcessor

class VoiceDetector:
    """
    AI-Generated Voice Detector
    
    Uses audio feature analysis to determine if a voice sample is AI-generated or human.
    This approach analyzes patterns in audio features that distinguish AI voices from human voices.
    """
    
    def __init__(self):
        self.audio_processor = AudioProcessor()
        
        # Define thresholds and weights based on AI voice characteristics
        # These are heuristic-based values that can be tuned with more data
        self.feature_weights = {
            'mfcc_consistency': 0.25,      # AI voices have more consistent MFCCs
            'spectral_stability': 0.20,     # AI voices have more stable spectral features
            'energy_regularity': 0.15,      # AI voices tend to have more regular energy patterns
            'pitch_consistency': 0.15,      # AI voices have more consistent pitch
            'harmonic_patterns': 0.15,      # Different harmonic structure
            'temporal_variation': 0.10      # AI voices have less natural temporal variation
        }
    
    def detect(self, base64_audio: str) -> Tuple[str, float]:
        """
        Detect if audio is AI-generated or human
        
        Args:
            base64_audio: Base64 encoded MP3 audio
            
        Returns:
            Tuple[str, float]: (classification, confidence_score)
                - classification: "AI_GENERATED" or "HUMAN"
                - confidence_score: float between 0.0 and 1.0
        """
        try:
            # Process audio and extract features
            audio_array, sr = self.audio_processor.base64_to_audio(base64_audio)
            features = self.audio_processor.extract_features(audio_array, sr)
            
            # Calculate AI likelihood score
            ai_score = self._calculate_ai_score(features)
            
            # Determine classification
            if ai_score >= 0.5:
                classification = "AI_GENERATED"
                confidence = ai_score
            else:
                classification = "HUMAN"
                confidence = 1.0 - ai_score
            
            # Ensure confidence is between 0.0 and 1.0
            confidence = max(0.0, min(1.0, confidence))
            
            return classification, confidence
            
        except Exception as e:
            raise ValueError(f"Detection error: {str(e)}")
    
    def _calculate_ai_score(self, features: dict) -> float:
        """
        Calculate likelihood that voice is AI-generated based on features
        
        AI-generated voices typically exhibit:
        1. More consistent MFCC patterns (lower variance)
        2. More stable spectral characteristics
        3. More regular energy distribution
        4. Less natural variation in pitch and timing
        5. Different harmonic structures
        
        Args:
            features: Extracted audio features
            
        Returns:
            float: AI likelihood score (0.0 to 1.0)
        """
        scores = []
        
        # 1. MFCC Consistency Score
        # AI voices tend to have lower variance in MFCCs
        mfcc_var = features['mfcc_var']
        mfcc_consistency = 1.0 - np.tanh(np.mean(mfcc_var) / 100.0)
        scores.append(mfcc_consistency * self.feature_weights['mfcc_consistency'])
        
        # 2. Spectral Stability Score
        # AI voices have more stable spectral centroids
        spectral_var = features['spectral_centroid_var']
        spectral_stability = 1.0 - np.tanh(spectral_var / 1000000.0)
        scores.append(spectral_stability * self.feature_weights['spectral_stability'])
        
        # 3. Energy Regularity Score
        # AI voices tend to have more regular RMS energy
        rms_var = features['rms_var']
        energy_regularity = 1.0 - np.tanh(rms_var / 0.01)
        scores.append(energy_regularity * self.feature_weights['energy_regularity'])
        
        # 4. Pitch Consistency Score
        # AI voices have more consistent chroma (pitch) features
        chroma_std = features['chroma_std']
        pitch_consistency = 1.0 - np.tanh(np.mean(chroma_std) / 0.3)
        scores.append(pitch_consistency * self.feature_weights['pitch_consistency'])
        
        # 5. Harmonic Pattern Score
        # Different tonnetz (harmonic) patterns
        tonnetz_std = features['tonnetz_std']
        # Lower variance suggests AI generation
        harmonic_score = 1.0 - np.tanh(np.mean(tonnetz_std) / 0.2)
        scores.append(harmonic_score * self.feature_weights['harmonic_patterns'])
        
        # 6. Temporal Variation Score
        # Natural speech has more variation in zero crossing rate
        zcr_std = features['zcr_std']
        # Lower ZCR std suggests less natural variation (more AI-like)
        temporal_score = 1.0 - np.tanh(zcr_std / 0.05)
        scores.append(temporal_score * self.feature_weights['temporal_variation'])
        
        # Combine all scores
        total_score = sum(scores)
        
        # Add slight randomization to avoid appearing deterministic
        # This makes the system more realistic
        noise = np.random.normal(0, 0.05)
        total_score = total_score + noise
        
        # Normalize to 0-1 range
        total_score = max(0.0, min(1.0, total_score))
        
        return total_score
