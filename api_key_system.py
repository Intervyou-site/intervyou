# api_key_system.py
"""
API Key Management System for FastAPI
Allows users to generate and manage API keys for programmatic access
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi_app import Base, get_db, User

# Security header for API key authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class APIKey(Base):
    """Model for storing user API keys"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    key_name = Column(String(100), nullable=False)  # User-friendly name
    key_hash = Column(String(128), nullable=False, unique=True)  # Hashed API key
    key_prefix = Column(String(10), nullable=False)  # First 8 chars for identification
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    
    # Relationship
    user = relationship("User", backref="api_keys")


def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a secure API key
    Returns: (full_key, key_hash, key_prefix)
    """
    # Generate random key: iv_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    random_part = secrets.token_urlsafe(32)
    full_key = f"iv_{random_part}"
    
    # Hash the key for storage (never store plain keys)
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    
    # Store prefix for user identification
    key_prefix = full_key[:8]
    
    return full_key, key_hash, key_prefix


def create_api_key(
    db: Session,
    user_id: int,
    key_name: str,
    expires_in_days: Optional[int] = None
) -> tuple[APIKey, str]:
    """
    Create a new API key for a user
    Returns: (APIKey object, plain_key_string)
    """
    full_key, key_hash, key_prefix = generate_api_key()
    
    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    api_key = APIKey(
        user_id=user_id,
        key_name=key_name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        expires_at=expires_at
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    return api_key, full_key


def verify_api_key(api_key_string: str, db: Session) -> Optional[User]:
    """
    Verify an API key and return the associated user
    Returns None if invalid
    """
    if not api_key_string or not api_key_string.startswith("iv_"):
        return None
    
    # Hash the provided key
    key_hash = hashlib.sha256(api_key_string.encode()).hexdigest()
    
    # Look up in database
    api_key = db.query(APIKey).filter(
        APIKey.key_hash == key_hash,
        APIKey.is_active == True
    ).first()
    
    if not api_key:
        return None
    
    # Check expiration
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        return None
    
    # Update last used timestamp
    api_key.last_used = datetime.utcnow()
    db.commit()
    
    # Return the user
    return db.query(User).filter(User.id == api_key.user_id).first()


def get_current_user_from_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency to get current user from API key
    Use this in your protected endpoints
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Include 'X-API-Key' header."
        )
    
    user = verify_api_key(api_key, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired API key"
        )
    
    return user


def revoke_api_key(db: Session, key_id: int, user_id: int) -> bool:
    """
    Revoke (deactivate) an API key
    Returns True if successful
    """
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == user_id
    ).first()
    
    if not api_key:
        return False
    
    api_key.is_active = False
    db.commit()
    return True


def list_user_api_keys(db: Session, user_id: int) -> list[dict]:
    """
    List all API keys for a user (without exposing full keys)
    """
    keys = db.query(APIKey).filter(APIKey.user_id == user_id).all()
    
    return [
        {
            "id": key.id,
            "name": key.key_name,
            "prefix": key.key_prefix,
            "is_active": key.is_active,
            "created_at": key.created_at.isoformat(),
            "last_used": key.last_used.isoformat() if key.last_used else None,
            "expires_at": key.expires_at.isoformat() if key.expires_at else None
        }
        for key in keys
    ]
