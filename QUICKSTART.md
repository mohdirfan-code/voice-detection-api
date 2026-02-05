# AI Voice Detection API - Quick Setup Guide

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
cd C:\Users\Dr.Mohd.Mohinoddin\.gemini\antigravity\scratch\voice-detection-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
# Create .env file
copy .env.example .env

# Edit .env and set your API key (or use the default for testing)
# API_KEY=hackathon-voice-detection-key-2026
```

### Step 3: Run the API
```bash
python main.py
```

The API will be available at: http://localhost:8000

### Step 4: Test the API
Open a new terminal and run:
```bash
python test_api.py
```

Or visit the interactive docs: http://localhost:8000/docs

## 📡 API Endpoint

**POST** `/detect`

**Headers:**
```
X-API-Key: hackathon-voice-detection-key-2026
Content-Type: application/json
```

**Request:**
```json
{
  "audio": "base64_encoded_mp3_audio"
}
```

**Response:**
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87
}
```

## 🌐 Deploy to Cloud

### Option 1: Render.com (Recommended)
1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Connect GitHub repo
5. Set environment variable: `API_KEY=your-key`
6. Deploy!

### Option 2: Railway.app
```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway variables set API_KEY=your-key
```

## 🧪 Testing with Real Audio

```bash
# Test with your own MP3 file
python test_api.py sample.mp3

# Test deployed endpoint
python test_api.py sample.mp3 https://your-api.onrender.com your-api-key
```

## 📝 API Key

**Default for local testing:** `hackathon-voice-detection-key-2026`

For production, generate a secure key:
```python
import secrets
print(secrets.token_urlsafe(32))
```

## ⚡ Features

✅ Multi-language support (Tamil, English, Hindi, Malayalam, Telugu)
✅ Base64 MP3 audio processing
✅ Feature-based AI detection
✅ JSON response format
✅ API key authentication
✅ FastAPI with auto-generated docs
✅ Ready for deployment

## 🎯 Hackathon Submission

When submitting, provide:
1. **API Endpoint URL**: Your deployed URL (e.g., `https://your-api.onrender.com/detect`)
2. **API Key**: The key you set in environment variables
3. **Test**: Use the hackathon's endpoint tester to verify

## 📞 Support

Check `README.md` for detailed documentation.
