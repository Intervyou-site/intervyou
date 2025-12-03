"""
FastAPI routes for Online IDE
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from .code_executor import CodeExecutor
from .language_configs import LANGUAGE_CONFIGS, CODING_CHALLENGES

router = APIRouter(prefix="/ide", tags=["IDE"])
executor = CodeExecutor()


class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    input_data: Optional[str] = ""


class CodeAnalysisRequest(BaseModel):
    code: str
    language: str


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {
                "id": lang_id,
                "name": config["name"],
                "version": config["version"],
                "template": config["template"]
            }
            for lang_id, config in LANGUAGE_CONFIGS.items()
        ]
    }


@router.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    """
    Execute code and return results with AI-powered error analysis
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language not in LANGUAGE_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
    
    result = executor.execute_code(
        code=request.code,
        language=request.language,
        input_data=request.input_data
    )
    
    return result


@router.post("/analyze")
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code quality and provide suggestions
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language not in LANGUAGE_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
    
    analysis = executor.analyze_code_quality(
        code=request.code,
        language=request.language
    )
    
    return analysis


@router.get("/challenges")
async def get_challenges():
    """Get coding challenges for practice"""
    return {"challenges": CODING_CHALLENGES}


@router.get("/challenges/{challenge_id}")
async def get_challenge(challenge_id: int):
    """Get specific coding challenge"""
    challenge = next((c for c in CODING_CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge


@router.get("/template/{language}")
async def get_template(language: str):
    """Get code template for a language"""
    if language not in LANGUAGE_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    
    return {
        "language": language,
        "template": LANGUAGE_CONFIGS[language]["template"]
    }
