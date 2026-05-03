"""
Security Module
Comprehensive input validation and sanitization
"""

from .input_validator import InputValidator, QueryParameterValidator, FormValidator
from .secure_db import SecureQueryBuilder, SecureDBOperations
from .secure_upload import SecureFileUpload
from .secure_code_execution import CodeSecurityValidator, CommandInjectionPrevention
from .api_validators import (
    UserRegistrationRequest,
    UserLoginRequest,
    QuestionSubmissionRequest,
    BookmarkRequest,
    CodeExecutionRequest,
    ResumeGenerationRequest,
    SearchRequest,
    PaginationRequest,
    FilterRequest,
    AptitudeSubmissionRequest,
    MCQSubmissionRequest,
    VideoUploadMetadata,
    AdminUserUpdateRequest,
)

__all__ = [
    # Input Validators
    'InputValidator',
    'QueryParameterValidator',
    'FormValidator',
    
    # Database Security
    'SecureQueryBuilder',
    'SecureDBOperations',
    
    # File Upload Security
    'SecureFileUpload',
    
    # Code Execution Security
    'CodeSecurityValidator',
    'CommandInjectionPrevention',
    
    # API Validators
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

__version__ = '1.0.0'
