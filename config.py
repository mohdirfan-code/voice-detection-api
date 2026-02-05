import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    API_KEY = os.getenv("API_KEY", "hackathon-voice-detection-key-2026")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Audio Processing Settings
    SAMPLE_RATE = 22050  # Standard sample rate for audio processing
    MAX_AUDIO_DURATION = 60  # Maximum duration in seconds
    
    # Model Settings
    AI_THRESHOLD = 0.5  # Threshold for AI detection
    
    # Feature extraction parameters
    N_MFCC = 13
    HOP_LENGTH = 512
    N_FFT = 2048

config = Config()
