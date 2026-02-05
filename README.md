# AI Voice Detection API

A REST API system that detects whether voice samples are AI-generated or human-spoken. Supports **Tamil, English, Hindi, Malayalam, and Telugu**.

## 🚀 Features

- **Multi-language Support**: Tamil, English, Hindi, Malayalam, Telugu
- **Base64 Audio Processing**: Accepts MP3 audio in base64 format
- **Feature-based Detection**: Uses advanced audio feature analysis
- **Secure API**: API key authentication
- **JSON Response**: Structured output with classification and confidence scores

## 📋 API Specification

### Endpoint

```
POST /detect
```

### Authentication

Include API key in request headers:
```
X-API-Key: your-api-key-here
```

### Request Format

```json
{
  "audio": "base64_encoded_mp3_audio_here"
}
```

### Response Format

```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87
}
```

**Fields:**
- `classification`: Either `"AI_GENERATED"` or `"HUMAN"`
- `confidence`: Float between 0.0 and 1.0

### Example Using cURL

```bash
curl -X POST "https://your-api-url.com/detect" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "audio": "//uQxAAAAAAAAAAAA..."
  }'
```

### Example Using Python

```python
import requests
import base64

# Read and encode audio file
with open("sample.mp3", "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

# Make API request
response = requests.post(
    "https://your-api-url.com/detect",
    headers={
        "X-API-Key": "your-api-key-here",
        "Content-Type": "application/json"
    },
    json={"audio": audio_base64}
)

print(response.json())
# Output: {"classification": "AI_GENERATED", "confidence": 0.87}
```

## 🛠️ Local Development

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

1. **Clone/Navigate to project directory**
   ```bash
   cd voice-detection-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example env file
   copy .env.example .env
   
   # Edit .env and set your API key
   # API_KEY=your-secure-api-key-here
   ```

### Running Locally

```bash
# Start the server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

Test the API using the included test script:

```bash
python test_api.py
```

Or test manually:

```bash
# Health check
curl http://localhost:8000/health

# Test detection endpoint
curl -X POST http://localhost:8000/detect \
  -H "X-API-Key: hackathon-voice-detection-key-2026" \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## 🚢 Deployment

### Deploy to Render.com

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/voice-detection-api.git
   git push -u origin main
   ```

2. **Create new Web Service on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: voice-detection-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variable**
   - In Render dashboard, go to Environment
   - Add: `API_KEY=your-secure-api-key-here`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your API will be available at: `https://your-service.onrender.com`

### Alternative: Deploy to Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set environment variable**
   ```bash
   railway variables set API_KEY=your-api-key-here
   ```

## 🔬 How It Works

The system uses **feature-based audio analysis** to detect AI-generated voices:

1. **Audio Processing**: Converts base64 MP3 to audio array
2. **Feature Extraction**: Extracts multiple acoustic features:
   - MFCC (Mel-frequency cepstral coefficients)
   - Spectral centroid, rolloff, contrast
   - Zero crossing rate
   - Chroma features (pitch)
   - RMS energy
   - Tonnetz (harmonic features)

3. **Pattern Analysis**: Analyzes patterns that distinguish AI voices:
   - AI voices have more consistent MFCC patterns
   - More stable spectral characteristics
   - More regular energy distribution
   - Less natural temporal variation

4. **Classification**: Combines feature scores to determine if voice is AI-generated

## 📁 Project Structure

```
voice-detection-api/
├── main.py              # FastAPI application
├── detector.py          # AI voice detection logic
├── audio_processor.py   # Audio processing and feature extraction
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── test_api.py          # API testing script
├── .env.example         # Environment variable template
└── README.md            # This file
```

## 🔐 Security

- API key authentication required for all detection requests
- Secure header-based authentication (X-API-Key)
- Input validation and sanitization
- Error handling without exposing internal details

## 📊 Response Codes

- **200**: Successful detection
- **400**: Invalid request (bad audio data)
- **401**: Missing API key
- **403**: Invalid API key
- **500**: Internal server error

## 🌐 Supported Audio Format

- **Format**: MP3
- **Encoding**: Base64
- **Duration**: Up to 60 seconds recommended
- **Languages**: Tamil, English, Hindi, Malayalam, Telugu (language-agnostic features)

## 📝 License

This project is created for hackathon purposes.

## 🤝 Support

For issues or questions, please contact the development team.
