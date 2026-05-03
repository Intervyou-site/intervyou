#!/usr/bin/env python3
"""
IntervYou HTTPS Start Script
This script starts IntervYou with HTTPS enabled for camera/microphone access.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_certificates():
    """Check if SSL certificates exist"""
    cert_exists = Path("cert.pem").exists()
    key_exists = Path("key.pem").exists()
    
    if not cert_exists or not key_exists:
        print("❌ SSL certificates not found!")
        print("   Generating certificates now...")
        try:
            subprocess.run([sys.executable, "generate_cert.py"], check=True)
            print("✅ Certificates generated successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to generate certificates")
            print("   Run: python generate_cert.py")
            sys.exit(1)
    else:
        print("✅ SSL certificates found")
    
    return True

def start_https_server():
    """Start the FastAPI server with HTTPS"""
    print("\n🚀 Starting IntervYou with HTTPS...")
    print("   Server will be available at: https://localhost:8000")
    print("   ⚠️  You'll need to accept the self-signed certificate warning in your browser")
    print("   Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "fastapi_app_cleaned:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--ssl-keyfile", "key.pem",
            "--ssl-certfile", "cert.pem"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup routine"""
    print_header("IntervYou HTTPS Server")
    
    # Check certificates
    check_certificates()
    
    # Start HTTPS server
    start_https_server()

if __name__ == "__main__":
    main()
