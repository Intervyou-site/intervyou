# api_key_routes.py
"""
API routes for managing API keys
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from fastapi_app import get_db, get_current_user, templates
from api_key_system import (
    create_api_key,
    revoke_api_key,
    list_user_api_keys,
    get_current_user_from_api_key,
    APIKey
)
import api_key_system

router = APIRouter(prefix="/api/keys", tags=["API Keys"])


class CreateAPIKeyRequest(BaseModel):
    key_name: str
    expires_in_days: Optional[int] = None


class RevokeAPIKeyRequest(BaseModel):
    key_id: int


# ============= Web UI Routes =============

@router.get("/manage", response_class=HTMLResponse)
async def api_keys_page(request: Request, db: Session = Depends(get_db)):
    """Render API key management page"""
    user = get_current_user(request, db)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Please login to manage API keys"
        })
    
    keys = list_user_api_keys(db, user.id)
    
    return templates.TemplateResponse("api_keys.html", {
        "request": request,
        "user": user,
        "api_keys": keys
    })


# ============= API Routes =============

@router.post("/create")
async def create_new_api_key(
    request: Request,
    key_name: str = Form(...),
    expires_in_days: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new API key for the logged-in user"""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Limit number of keys per user
    existing_keys = db.query(api_key_system.APIKey).filter_by(
        user_id=user.id,
        is_active=True
    ).count()
    
    if existing_keys >= 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 active API keys allowed per user"
        )
    
    api_key_obj, plain_key = create_api_key(
        db=db,
        user_id=user.id,
        key_name=key_name,
        expires_in_days=expires_in_days
    )
    
    return JSONResponse({
        "success": True,
        "message": "API key created successfully",
        "api_key": plain_key,  # Only shown once!
        "key_id": api_key_obj.id,
        "key_name": api_key_obj.key_name,
        "key_prefix": api_key_obj.key_prefix,
        "warning": "Save this key now! It won't be shown again."
    })


@router.post("/revoke")
async def revoke_key(
    request: Request,
    key_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Revoke an API key"""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    success = revoke_api_key(db, key_id, user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return JSONResponse({
        "success": True,
        "message": "API key revoked successfully"
    })


@router.get("/list")
async def list_keys(
    request: Request,
    db: Session = Depends(get_db)
):
    """List all API keys for the current user"""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    keys = list_user_api_keys(db, user.id)
    
    return JSONResponse({
        "success": True,
        "api_keys": keys
    })


# ============= Example Protected API Endpoint =============

@router.get("/test")
async def test_api_key(
    user = Depends(get_current_user_from_api_key)
):
    """
    Example endpoint that requires API key authentication
    Test with: curl -H "X-API-Key: your_key_here" http://localhost:8000/api/keys/test
    """
    return {
        "success": True,
        "message": f"Hello {user.name}! Your API key works.",
        "user_id": user.id,
        "user_email": user.email
    }
