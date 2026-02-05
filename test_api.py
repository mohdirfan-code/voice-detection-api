import requests
import base64
import json
import sys

def test_api(base_url="http://localhost:8000", api_key="hackathon-voice-detection-key-2026"):
    """
    Test the AI Voice Detection API
    
    Args:
        base_url: API base URL
        api_key: API authentication key
    """
    
    print("=" * 60)
    print("AI Voice Detection API - Test Suite")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n[TEST 1] Health Check")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200, "Health check failed"
        print("✓ Health check passed")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
    
    # Test 2: Root Endpoint
    print("\n[TEST 2] Root Endpoint")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200, "Root endpoint failed"
        print("✓ Root endpoint passed")
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
    
    # Test 3: Missing API Key
    print("\n[TEST 3] Missing API Key (should fail)")
    print("-" * 60)
    try:
        response = requests.post(
            f"{base_url}/detect",
            json={"audio": "dummy_base64_string"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 401, "Should return 401 for missing API key"
        print("✓ Missing API key test passed")
    except Exception as e:
        print(f"✗ Missing API key test failed: {e}")
    
    # Test 4: Invalid API Key
    print("\n[TEST 4] Invalid API Key (should fail)")
    print("-" * 60)
    try:
        response = requests.post(
            f"{base_url}/detect",
            headers={"X-API-Key": "invalid-key"},
            json={"audio": "dummy_base64_string"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 401, "Should return 401 for invalid API key"
        print("✓ Invalid API key test passed")
    except Exception as e:
        print(f"✗ Invalid API key test failed: {e}")
    
    # Test 5: Empty Audio
    print("\n[TEST 5] Empty Audio (should fail)")
    print("-" * 60)
    try:
        response = requests.post(
            f"{base_url}/detect",
            headers={"X-API-Key": api_key},
            json={"audio": ""}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400, "Should return 400 for empty audio"
        print("✓ Empty audio test passed")
    except Exception as e:
        print(f"✗ Empty audio test failed: {e}")
    
    # Test 6: Valid Request with Sample Audio
    print("\n[TEST 6] Valid Detection Request")
    print("-" * 60)
    print("NOTE: This test uses a minimal valid MP3 sample")
    print("For real testing, use actual voice samples")
    
    # Create a minimal valid MP3 (ID3 header + minimal audio frame)
    # This is just for testing the API flow
    minimal_mp3 = b'\xff\xfb\x90\x00' * 100  # Minimal MP3 frames
    sample_audio_base64 = base64.b64encode(minimal_mp3).decode('utf-8')
    
    try:
        response = requests.post(
            f"{base_url}/detect",
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            },
            json={"audio": sample_audio_base64}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            # Validate response structure
            assert "classification" in result, "Missing classification field"
            assert "confidence" in result, "Missing confidence field"
            assert result["classification"] in ["AI_GENERATED", "HUMAN"], "Invalid classification"
            assert 0.0 <= result["confidence"] <= 1.0, "Confidence out of range"
            print(f"\n✓ Detection successful!")
            print(f"  Classification: {result['classification']}")
            print(f"  Confidence: {result['confidence']:.2f}")
        else:
            print(f"Note: Detection may fail with minimal MP3. Use real audio for actual testing.")
            print(f"Error: {result}")
    except Exception as e:
        print(f"Note: {e}")
        print("Use a real MP3 audio file for complete testing")
    
    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)
    print("\nTo test with real audio:")
    print("1. Get a sample MP3 file")
    print("2. Convert to base64:")
    print("   python -c \"import base64; print(base64.b64encode(open('sample.mp3','rb').read()).decode())\"")
    print("3. Use the base64 string in API request")

def test_with_audio_file(audio_file_path, base_url="http://localhost:8000", api_key="hackathon-voice-detection-key-2026"):
    """
    Test API with actual audio file
    
    Args:
        audio_file_path: Path to MP3 audio file
        base_url: API base URL
        api_key: API authentication key
    """
    print(f"\nTesting with audio file: {audio_file_path}")
    print("-" * 60)
    
    try:
        # Read and encode audio file
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Make API request
        response = requests.post(
            f"{base_url}/detect",
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            },
            json={"audio": audio_base64}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            print(f"\n✓ Detection successful!")
            print(f"  Classification: {result['classification']}")
            print(f"  Confidence: {result['confidence']:.2f}")
        else:
            print(f"✗ Detection failed: {result}")
            
    except FileNotFoundError:
        print(f"✗ Audio file not found: {audio_file_path}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    # Default testing
    if len(sys.argv) == 1:
        test_api()
    elif len(sys.argv) == 2:
        # Test with audio file
        test_with_audio_file(sys.argv[1])
    elif len(sys.argv) == 3:
        # Test with custom URL
        test_api(base_url=sys.argv[1], api_key=sys.argv[2])
    elif len(sys.argv) == 4:
        # Test audio file with custom URL and API key
        test_with_audio_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage:")
        print("  python test_api.py                              # Test local API")
        print("  python test_api.py <audio.mp3>                  # Test with audio file")
        print("  python test_api.py <url> <api_key>              # Test custom endpoint")
        print("  python test_api.py <audio.mp3> <url> <api_key>  # Test file with custom endpoint")
