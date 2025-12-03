# api_key_routes.py
"""
API routes for managing API keys
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

# Import only what we need to avoid circular imports
from api_key_system import (
    create_api_key,
    revoke_api_key,
    list_user_api_keys,
    get_current_user_from_api_key
)

router = APIRouter(prefix="/api/keys", tags=["API Keys"])


class CreateAPIKeyRequest(BaseModel):
    key_name: str
    expires_in_days: Optional[int] = None


class RevokeAPIKeyRequest(BaseModel):
    key_id: int


# ============= Web UI Routes =============

@router.get("/manage", response_class=HTMLResponse)
async def api_keys_page(request: Request, db: Session = Depends(lambda: None)):
    """Render API key management page"""
    try:
        # Import here to avoid circular dependency
        from fastapi_app import get_db, get_current_user, templates
        
        # Get actual db session
        db_gen = get_db()
        db = next(db_gen)
        
        try:
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
        finally:
            try:
                next(db_gen)
            except StopIteration:
                pass
    except Exception as e:
        import traceback
        error_detail = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ API Keys Management Error: {error_detail}")
        return HTMLResponse(
            content=f"<h1>Error Loading API Keys Page</h1><pre>{error_detail}</pre>",
            status_code=500
        )


# ============= API Routes =============

@router.post("/create")
async def create_new_api_key(
    request: Request,
    key_name: str = Form(...),
    expires_in_days: Optional[int] = Form(None),
    db: Session = Depends(lambda: None)
):
    """Create a new API key for the logged-in user"""
    # Import here to avoid circular dependency
    from fastapi_app import get_db, get_current_user
    
    # Get actual db session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        user = get_current_user(request, db)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        # Import APIKey from fastapi_app
        from fastapi_app import APIKey
        
        # Limit number of keys per user
        existing_keys = db.query(APIKey).filter_by(
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
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


@router.post("/revoke")
async def revoke_key(
    request: Request,
    key_id: int = Form(...),
    db: Session = Depends(lambda: None)
):
    """Revoke an API key"""
    from fastapi_app import get_db, get_current_user
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
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
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


@router.get("/list")
async def list_keys(
    request: Request,
    db: Session = Depends(lambda: None)
):
    """List all API keys for the current user"""
    from fastapi_app import get_db, get_current_user
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        user = get_current_user(request, db)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        keys = list_user_api_keys(db, user.id)
        
        return JSONResponse({
            "success": True,
            "api_keys": keys
        })
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


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
