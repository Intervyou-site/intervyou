#!/usr/bin/env python3
"""
Database migration script to add API keys table
Run this once to create the api_keys table in your database
"""

import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from api_key_system import Base, APIKey

# Get database URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")

print(f"🔄 Migrating database: {DATABASE_URL}")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    print("✅ API keys table created successfully!")
    print("\nYou can now:")
    print("1. Visit http://localhost:8000/api/keys/manage to manage your API keys")
    print("2. Use the API key in your requests with header: X-API-Key: your_key_here")
except Exception as e:
    print(f"❌ Error creating table: {e}")
    exit(1)
