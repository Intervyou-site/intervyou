"""
API Input Validators
Pydantic models and validators for all API endpoints
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


class UserRegistrationRequest(BaseModel):
    """Validate user registration input"""
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=254)
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: Optional[str] = Field(None, min_length=8, max_length=128)
    
    @validator('name')
    def validate_name(cls, v):
        # Remove extra whitespace
        v = ' '.join(v.split())
        
        # Check for dangerous characters
        if re.search(r'[<>"\'/\\;]', v):
            raise ValueError('Name contains invalid characters')
        
        return v
    
    @validator('email')
    def validate_email(cls, v):
        v = v.strip().lower()
        
        # Email format validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        
        return v
    
    @root_validator
    def check_passwords_match(cls, values):
        pw = values.get('password')
        confirm = values.get('confirm_password')
        
        if confirm is not None and pw != confirm:
            raise ValueError('Passwords do not match')
        
        return values


class UserLoginRequest(BaseModel):
    """Validate user login input"""
    email: str = Field(..., min_length=5, max_length=254)
    password: str = Field(..., min_length=1, max_length=128)
    remember_me: Optional[bool] = False
    
    @validator('email')
    def validate_email(cls, v):
        return v.strip().lower()


class QuestionSubmissionRequest(BaseModel):
    """Validate question submission"""
    question: str = Field(..., min_length=5, max_length=5000)
    answer: str = Field(..., min_length=10, max_length=50000)
    category: Optional[str] = Field(None, max_length=50)
    difficulty: Optional[str] = Field('intermediate', max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    
    @validator('question', 'answer')
    def sanitize_text(cls, v):
        # Remove null bytes
        v = v.replace('\x00', '')
        
        # Normalize whitespace
        v = ' '.join(v.split())
        
        return v.strip()
    
    @validator('category')
    def validate_category(cls, v):
        if v is None:
            return v
        
        allowed_categories = [
            'Behavioral', 'Technical', 'System Design', 'Coding',
            'Leadership', 'HR Interview', 'Case Study', 'General'
        ]
        
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        
        return v
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        allowed = ['beginner', 'intermediate', 'advanced', 'expert']
        
        if v.lower() not in allowed:
            raise ValueError(f'Difficulty must be one of: {", ".join(allowed)}')
        
        return v.lower()


class BookmarkRequest(BaseModel):
    """Validate bookmark/save question request"""
    question: str = Field(..., min_length=5, max_length=5000)
    company: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=2000)
    tags: Optional[List[str]] = Field(default_factory=list)
    difficulty: Optional[str] = Field(None, max_length=20)
    priority: Optional[int] = Field(0, ge=0, le=5)
    
    @validator('tags')
    def validate_tags(cls, v):
        if not v:
            return []
        
        # Limit number of tags
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        
        # Validate each tag
        validated_tags = []
        for tag in v:
            tag = tag.strip()
            if len(tag) > 50:
                raise ValueError('Tag too long (max 50 characters)')
            if re.search(r'[<>"\'/\\;]', tag):
                raise ValueError('Tag contains invalid characters')
            validated_tags.append(tag)
        
        return validated_tags


class CodeExecutionRequest(BaseModel):
    """Validate code execution request"""
    code: str = Field(..., min_length=1, max_length=100000)
    language: str = Field(..., min_length=1, max_length=20)
    input_data: Optional[str] = Field('', max_length=10000)
    
    @validator('language')
    def validate_language(cls, v):
        allowed_languages = [
            'python', 'javascript', 'java', 'cpp', 'c',
            'go', 'rust', 'typescript', 'ruby', 'php'
        ]
        
        v = v.lower()
        if v not in allowed_languages:
            raise ValueError(f'Language must be one of: {", ".join(allowed_languages)}')
        
        return v
    
    @validator('code')
    def validate_code(cls, v):
        # Remove null bytes
        v = v.replace('\x00', '')
        
        return v
    
    @validator('input_data')
    def validate_input(cls, v):
        if v is None:
            return ''
        
        # Remove null bytes
        v = v.replace('\x00', '')
        
        return v


class ResumeGenerationRequest(BaseModel):
    """Validate resume generation request"""
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=254)
    phone: Optional[str] = Field(None, max_length=20)
    summary: Optional[str] = Field(None, max_length=2000)
    experience: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    education: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    skills: Optional[List[str]] = Field(default_factory=list)
    template: Optional[str] = Field('modern', max_length=50)
    
    @validator('email')
    def validate_email(cls, v):
        v = v.strip().lower()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        
        # Remove common formatting characters
        v = re.sub(r'[\s\-\(\)\.]+', '', v)
        
        # Check if it's a valid phone number (digits and + only)
        if not re.match(r'^\+?[0-9]{10,15}$', v):
            raise ValueError('Invalid phone number format')
        
        return v
    
    @validator('skills')
    def validate_skills(cls, v):
        if not v:
            return []
        
        if len(v) > 50:
            raise ValueError('Maximum 50 skills allowed')
        
        validated_skills = []
        for skill in v:
            skill = skill.strip()
            if len(skill) > 100:
                raise ValueError('Skill name too long')
            validated_skills.append(skill)
        
        return validated_skills


class SearchRequest(BaseModel):
    """Validate search request"""
    query: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=50)
    limit: Optional[int] = Field(10, ge=1, le=100)
    
    @validator('query')
    def validate_query(cls, v):
        v = v.strip()
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b',
            r'(--|#|/\*|\*/)',
            r'(\bOR\b.*=.*|1=1)',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Query contains invalid patterns')
        
        return v


class PaginationRequest(BaseModel):
    """Validate pagination parameters"""
    page: int = Field(1, ge=1, le=10000)
    limit: int = Field(10, ge=1, le=100)
    sort_by: Optional[str] = Field('timestamp', max_length=50)
    order: Optional[str] = Field('desc', max_length=4)
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        if v is None:
            return 'timestamp'
        
        # Only allow alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Invalid sort field')
        
        return v
    
    @validator('order')
    def validate_order(cls, v):
        if v is None:
            return 'desc'
        
        v = v.lower()
        if v not in ['asc', 'desc']:
            raise ValueError('Order must be asc or desc')
        
        return v


class FilterRequest(BaseModel):
    """Validate filter parameters"""
    category: Optional[str] = Field(None, max_length=50)
    company: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, max_length=20)
    tags: Optional[str] = Field(None, max_length=500)  # Comma-separated
    search: Optional[str] = Field(None, max_length=200)
    
    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return v
        
        # Split and validate tags
        tags = [t.strip() for t in v.split(',') if t.strip()]
        
        if len(tags) > 10:
            raise ValueError('Maximum 10 tags in filter')
        
        for tag in tags:
            if len(tag) > 50:
                raise ValueError('Tag too long')
        
        return ','.join(tags)


class AptitudeSubmissionRequest(BaseModel):
    """Validate aptitude question submission"""
    question: Dict[str, Any] = Field(...)
    user_answer: str = Field(..., max_length=500)
    time_taken: int = Field(..., ge=0, le=3600)
    
    @validator('user_answer')
    def validate_answer(cls, v):
        v = v.strip()
        
        # Remove dangerous characters
        if re.search(r'[<>"\'/\\;]', v):
            raise ValueError('Answer contains invalid characters')
        
        return v


class MCQSubmissionRequest(BaseModel):
    """Validate MCQ submission"""
    category: str = Field(..., max_length=50)
    question: str = Field(..., max_length=2000)
    options: List[str] = Field(..., min_items=2, max_items=6)
    user_answer: str = Field(..., max_length=500)
    correct_answer: str = Field(..., max_length=500)
    difficulty: Optional[str] = Field('intermediate', max_length=20)
    time_taken: int = Field(0, ge=0, le=3600)
    
    @validator('options')
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 options required')
        
        validated = []
        for opt in v:
            opt = opt.strip()
            if len(opt) > 500:
                raise ValueError('Option too long')
            validated.append(opt)
        
        return validated


class VideoUploadMetadata(BaseModel):
    """Validate video upload metadata"""
    question: Optional[str] = Field(None, max_length=2000)
    duration: Optional[int] = Field(None, ge=1, le=600)  # Max 10 minutes
    
    @validator('question')
    def validate_question(cls, v):
        if v is None:
            return v
        
        v = v.strip()
        
        # Remove dangerous characters
        if re.search(r'[<>"\'/\\;]', v):
            raise ValueError('Question contains invalid characters')
        
        return v


class AdminUserUpdateRequest(BaseModel):
    """Validate admin user update"""
    user_id: int = Field(..., ge=1)
    role: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    
    @validator('role')
    def validate_role(cls, v):
        if v is None:
            return v
        
        allowed_roles = ['user', 'admin', 'moderator']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        
        return v


# Export all validators
__all__ = [
    'UserRegistrationRequest',
    'UserLoginRequest',
    'QuestionSubmissionRequest',
    'BookmarkRequest',
    'CodeExecutionRequest',
    'ResumeGenerationRequest',
    'SearchRequest',
    'PaginationRequest',
    'FilterRequest',
    'AptitudeSubmissionRequest',
    'MCQSubmissionRequest',
    'VideoUploadMetadata',
    'AdminUserUpdateRequest',
]
