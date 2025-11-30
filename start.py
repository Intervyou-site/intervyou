#!/usr/bin/env python3
"""
IntervYou Quick Start Script
This script helps you get IntervYou up and running quickly.
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

def check_python_version():
    """Ensure Python 3.9+ is being used"""
    if sys.version_info < (3, 9):
        print("❌ Error: Python 3.9 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️  .env file not found")
        if Path(".env.example").exists():
            print("   Creating .env from .env.example...")
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created")
            print("   ⚠️  IMPORTANT: Edit .env and add your API keys!")
            return False
        else:
            print("❌ .env.example not found. Cannot create .env")
            return False
    else:
        print("✅ .env file exists")
        return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def initialize_database():
    """Initialize the database"""
    try:
        print("Initializing database...")
        from fastapi_app import Base, engine
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def check_api_keys():
    """Check if critical API keys are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    issues = []
    
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key or secret_key == "dev-only-change-in-production":
        issues.append("SECRET_KEY not set or using default")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        issues.append("OPENAI_API_KEY not set (AI features will use fallback)")
    
    if issues:
        print("⚠️  Configuration warnings:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ API keys configured")
        return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting IntervYou server...")
    print("   Server will be available at: http://localhost:8000")
    print("   Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "fastapi_app:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup routine"""
    print_header("IntervYou Quick Start")
    
    # Check Python version
    check_python_version()
    
    # Check .env file
    env_exists = check_env_file()
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        print("\n❌ Please install dependencies first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check API keys
    keys_ok = check_api_keys()
    
    # Initialize database
    db_ok = initialize_database()
    if not db_ok:
        print("\n❌ Database initialization failed")
        sys.exit(1)
    
    # Final check
    if not env_exists or not keys_ok:
        print("\n⚠️  Configuration incomplete!")
        print("   Please edit .env and add your API keys, then run this script again.")
        response = input("\n   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("   Exiting. Configure .env and try again.")
            sys.exit(0)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
