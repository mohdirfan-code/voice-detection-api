from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
from detector import VoiceDetector
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="Detects whether a voice sample is AI-generated or human-spoken. Supports Tamil, English, Hindi, Malayalam, and Telugu.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector
detector = VoiceDetector()

# Request/Response Models
class DetectionRequest(BaseModel):
    audio: str = Field(
        ...,
        description="Base64-encoded MP3 audio file",
        example="//uQx...base64_encoded_audio_here..."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "audio": "//uQxAAAAAAAAAAAAAAAAAAAAAAAA..."
            }
        }

class DetectionResponse(BaseModel):
    classification: str = Field(
        ...,
        description="Classification result: 'AI_GENERATED' or 'HUMAN'",
        example="AI_GENERATED"
    )
    confidence: float = Field(
        ...,
        description="Confidence score between 0.0 and 1.0",
        ge=0.0,
        le=1.0,
        example=0.87
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "classification": "AI_GENERATED",
                "confidence": 0.87
            }
        }

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# Authentication middleware
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key from request headers"""
    if not x_api_key:
        logger.warning("Request received without API key")
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Provide X-API-Key in request headers."
        )
    
    if x_api_key != config.API_KEY:
        logger.warning(f"Invalid API key attempted: {x_api_key[:10]}...")
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    
    return x_api_key

# Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI Voice Detection API",
        "version": "1.0.0",
        "description": "Detects AI-generated vs human voice in audio samples",
        "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
        "endpoints": {
            "detect": "/detect",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-voice-detection"}

@app.post("/detect", response_model=DetectionResponse)
async def detect_voice(
    request: DetectionRequest,
    api_key: str = Header(None, alias="X-API-Key")
):
    """
    Detect if a voice sample is AI-generated or human-spoken
    
    **Authentication**: Requires X-API-Key header
    
    **Request Body**:
    - audio: Base64-encoded MP3 audio file
    
    **Response**:
    - classification: "AI_GENERATED" or "HUMAN"
    - confidence: Confidence score (0.0 to 1.0)
    
    **Supported Languages**: Tamil, English, Hindi, Malayalam, Telugu
    """
    # Verify API key
    if not api_key or api_key != config.API_KEY:
        logger.warning("Unauthorized access attempt to /detect")
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid API key. Provide X-API-Key in request headers."
        )
    
    try:
        logger.info("Processing voice detection request")
        
        # Validate input
        if not request.audio or len(request.audio.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Audio field cannot be empty"
            )
        
        # Perform detection
        classification, confidence = detector.detect(request.audio)
        
        logger.info(f"Detection complete: {classification} (confidence: {confidence:.2f})")
        
        return DetectionResponse(
            classification=classification,
            confidence=round(confidence, 2)
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during voice detection"
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "error": "An unexpected error occurred",
        "detail": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
