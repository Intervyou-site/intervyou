"""Test the API keys route directly"""
import sys
import traceback

try:
    print("Testing API keys route...")
    from fastapi.testclient import TestClient
    from fastapi_app import app
    
    client = TestClient(app)
    
    print("\n1. Testing /api/keys/manage endpoint...")
    response = client.get("/api/keys/manage")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response length: {len(response.text)} chars")
    
    if response.status_code == 500:
        print(f"\n❌ ERROR Response:")
        print(response.text[:500])
    elif response.status_code == 200:
        print(f"✅ Success! Page loaded")
        if "Internal Server Error" in response.text:
            print("⚠️  But page contains 'Internal Server Error' text")
        elif "Login" in response.text or "login" in response.text:
            print("✅ Correctly redirected to login page")
    
    print("\n2. Testing /api/keys/test endpoint...")
    response2 = client.get("/api/keys/test")
    print(f"   Status Code: {response2.status_code}")
    print(f"   Response: {response2.json()}")
    
except Exception as e:
    print(f"\n❌ Error occurred:")
    print(f"   {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
