# Voice Detection API - Test Examples

## Issue Analysis

Your 422 error occurs because the endpoint tester isn't sending the request body correctly. The API expects:

```json
{
  "audio": "base64_encoded_string_here"
}
```

## ✅ Correct Request Format

### Using cURL

```bash
curl -X POST https://voice-detection-api-c1j5.onrender.com/detect \
  -H "Content-Type: application/json" \
  -H "X-API-Key: hackathon-voice-detection-key-2026" \
  -d '{"audio":"SUQzBAAAAAECBVRTU0UAAAAOAAADTGF2ZjYwLjE2LjEwMA=="}'
```

### Using Python (requests library)

```python
import requests

response = requests.post(
    "https://voice-detection-api-c1j5.onrender.com/detect",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "hackathon-voice-detection-key-2026"
    },
    json={
        "audio": "SUQzBAAAAAECBVRTU0UAAAAOAAADTGF2ZjYwLjE2LjEwMA=="
    }
)
print(response.json())
```

### Using the Web Endpoint Tester

**If the tester has these fields:**

1. **URL**: `https://voice-detection-api-c1j5.onrender.com/detect`

2. **Headers**:
   - Name: `X-API-Key` (exactly this capitalization)
   - Value: `hackathon-voice-detection-key-2026`
   - Name: `Content-Type`
   - Value: `application/json`

3. **Request Body** (select "JSON" or "Raw" mode):
   ```json
   {
     "audio": "your_full_base64_audio_string_here"
   }
   ```

**⚠️ Common Issues with Endpoint Testers:**

- Some testers send URL-encoded form data instead of JSON
- Some don't properly handle the "audio" field name
- Some truncate long base64 strings

## 🧪 Test the API Locally

Run the Python test script:

```bash
cd C:\Users\Dr.Mohd.Mohinoddin\.gemini\antigravity\scratch\voice-detection-api
python test_endpoint.py
```

## 📋 Expected Response

**Success (200 OK):**
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87
}
```

or

```json
{
  "classification": "HUMAN",
  "confidence": 0.73
}
```

**Error Responses:**

- **401 Unauthorized**: Missing or wrong API key
- **400 Bad Request**: Invalid base64 or empty audio
- **422 Unprocessable Entity**: Missing "audio" field in request body
- **500 Internal Server Error**: Server-side processing error

## 🔑 API Key

**Default Key**: `hackathon-voice-detection-key-2026`

If you want to use your custom key `6a143d67e2a17d53bf9d9f2a9be89de3`, you need to:

1. Go to Render.com dashboard
2. Select your voice-detection-api service
3. Go to "Environment" tab
4. Add variable: `API_KEY` = `6a143d67e2a17d53bf9d9f2a9be89de3`
5. Save and redeploy

## 📝 Testing Checklist

- [x] URL is correct
- [ ] X-API-Key header is set correctly (capitalization matters!)
- [ ] Content-Type header is `application/json`
- [ ] Request body is valid JSON: `{"audio": "..."}`
- [ ] Audio string is valid base64
- [ ] Using POST method (not GET)
