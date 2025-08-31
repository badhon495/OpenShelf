#!/usr/bin/env python3
"""
Test script to verify Cloudinary credentials and API connectivity
"""
import os
import sys
import requests
import hashlib
import hmac
import time

# Set up Django environment
sys.path.append('/home/badhon/Documents/OpenShelf/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

def test_cloudinary_basic():
    """Test basic Cloudinary configuration"""
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    print("=== Cloudinary Configuration Test ===")
    print(f"Cloud Name: {cloud_name}")
    print(f"API Key: {api_key}")
    print(f"API Secret: {'*' * 10 if api_secret else 'NOT SET'}")
    
    if not all([cloud_name, api_key, api_secret]):
        print("❌ ERROR: Missing Cloudinary credentials!")
        return False
    
    print("✅ All credentials are set")
    return True

def test_cloudinary_signature():
    """Test signature generation"""
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    timestamp = str(int(time.time()))
    
    # Test with minimal parameters
    params = {
        'timestamp': timestamp
    }
    
    # Sort parameters and create string
    sorted_params = sorted(params.items())
    param_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    # Generate signature using SHA-1
    signature = hmac.new(
        api_secret.encode('utf-8'),
        param_string.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    
    print("\n=== Signature Generation Test ===")
    print(f"Parameters: {param_string}")
    print(f"Generated signature: {signature}")
    
    return signature

def test_cloudinary_api():
    """Test actual API call to Cloudinary"""
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    timestamp = str(int(time.time()))
    
    # Minimal parameters for testing
    params_for_signature = {
        'timestamp': timestamp
    }
    
    # Generate signature
    sorted_params = sorted(params_for_signature.items())
    param_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    signature = hmac.new(
        api_secret.encode('utf-8'),
        param_string.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    
    # Test with a simple text upload (no actual file)
    data = {
        'timestamp': timestamp,
        'api_key': api_key,
        'signature': signature
    }
    
    # Create a simple test file in memory
    test_content = b"Test image content"
    files = {'file': ('test.txt', test_content, 'text/plain')}
    
    upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/auto/upload"
    
    print("\n=== API Connectivity Test ===")
    print(f"Upload URL: {upload_url}")
    print(f"Timestamp: {timestamp}")
    print(f"Signature: {signature}")
    
    try:
        response = requests.post(upload_url, files=files, data=data, timeout=10)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ API call successful!")
            return True
        else:
            print("❌ API call failed")
            return False
            
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Cloudinary Configuration...\n")
    
    # Test 1: Basic configuration
    if not test_cloudinary_basic():
        sys.exit(1)
    
    # Test 2: Signature generation
    test_cloudinary_signature()
    
    # Test 3: API connectivity
    test_cloudinary_api()
    
    print("\n=== Test Complete ===")
