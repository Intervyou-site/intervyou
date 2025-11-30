# schemas.py
from typing import List, Optional, Any
from pydantic import BaseModel, Field, constr, conint, HttpUrl

ShortStr = constr(min_length=1, max_length=200)
MediumStr = constr(min_length=1, max_length=2000)
LongStr = constr(min_length=1, max_length=10000)

class MessageOut(BaseModel):
    success: bool = True
    message: Optional[str] = None

# /evaluate_answer
class EvaluateRequest(BaseModel):
    question_id: Optional[str] = Field(None, description="Optional question id from generator")
    question_text: Optional[MediumStr] = Field(None, description="Optional explicit question text")
    answer: LongStr = Field(..., description="User answer text (1..10000 chars)")
    user_id: Optional[int] = Field(None)

class EvaluationResult(BaseModel):
    summary: Optional[str] = None
    improvements: Optional[List[str]] = None
    grammar: Optional[str] = None
    fillers: Optional[str] = None
    score: Optional[float] = None
    audio_feedback_url: Optional[HttpUrl] = None

class EvaluateResponse(BaseModel):
    evaluation: Optional[EvaluationResult]
    plagiarism_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    matches: Optional[List[Any]] = None

# /save_question
class SaveQuestionRequest(BaseModel):
    question: MediumStr

class SaveQuestionResponse(BaseModel):
    id: Optional[int]
    message: Optional[str]

# /generate_questions
class GenerateQuestionsRequest(BaseModel):
    category: Optional[ShortStr] = Field("General")
    count: Optional[conint(ge=1, le=50)] = Field(5)

class GeneratedItem(BaseModel):
    id: Optional[str]
    prompt: ShortStr

class GenerateQuestionsResponse(BaseModel):
    created: List[GeneratedItem]

# /plagiarism_check
class PlagiarismRequest(BaseModel):
    text: MediumStr

class PlagiarismMatch(BaseModel):
    source: Optional[str]
    id: Optional[Any]
    sim: float
    excerpt: Optional[str]

class PlagiarismResponse(BaseModel):
    plagiarism_score: float = Field(0.0, ge=0.0, le=1.0)
    matches: List[PlagiarismMatch] = []

# /voice
class VoiceUploadResponse(BaseModel):
    result: Optional[str]
    duration_seconds: Optional[float]
