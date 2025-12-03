#!/usr/bin/env python3
"""
Test script for API key system
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_key_system():
    print("🧪 Testing API Key System\n")
    print("=" * 50)
    
    # Step 1: Login first (you need to be logged in to create API keys)
    print("\n1. Please login to your account first")
    print(f"   Visit: {BASE_URL}/login")
    print("   Then visit: {BASE_URL}/api/keys/manage")
    print("   Create an API key and copy it")
    
    # Step 2: Test with API key
    api_key = input("\n2. Paste your API key here: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    print(f"\n3. Testing API key: {api_key[:15]}...")
    
    headers = {"X-API-Key": api_key}
    
    try:
        # Test the API key
        response = requests.get(f"{BASE_URL}/api/keys/test", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Key is valid!")
            print(f"   User: {data.get('user_email')}")
            print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ API Key test failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure your server is running:")
        print("   python start.py")

if __name__ == "__main__":
    test_api_key_system()
