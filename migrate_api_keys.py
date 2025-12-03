#!/usr/bin/env python3
"""
Database migration script to add API keys table
Run this once to create the api_keys table in your database
"""

import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text

# Get database URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")

print(f"🔄 Migrating database: {DATABASE_URL}")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    sql = """
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        key_name VARCHAR(100) NOT NULL,
        key_hash VARCHAR(128) NOT NULL UNIQUE,
        key_prefix VARCHAR(10) NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP,
        expires_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    """
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    sql = """
    CREATE TABLE IF NOT EXISTS api_keys (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        key_name VARCHAR(100) NOT NULL,
        key_hash VARCHAR(128) NOT NULL UNIQUE,
        key_prefix VARCHAR(10) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP,
        expires_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES "user"(id)
    )
    """

# Create table
try:
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("✅ API keys table created successfully!")
    print("\nYou can now:")
    print("1. Visit http://localhost:8000/api/keys/manage to manage your API keys")
    print("2. Use the API key in your requests with header: X-API-Key: your_key_here")
except Exception as e:
    print(f"❌ Error creating table: {e}")
    print("\nIf the table already exists, this is normal. You can proceed.")
    exit(0)
