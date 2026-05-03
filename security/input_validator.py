"""
Comprehensive Input Validation and Sanitization Module
Protects against SQL injection, command injection, XSS, path traversal, and other attacks
"""

import re
import html
import bleach
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import unicodedata
from urllib.parse import urlparse, parse_qs


class InputValidator:
    """Centralized input validation and sanitization"""
    
    # Dangerous patterns for command injection
    COMMAND_INJECTION_PATTERNS = [
        r'[;&|`$(){}[\]<>]',  # Shell metacharacters
        r'\.\./',  # Path traversal
        r'\\x[0-9a-fA-F]{2}',  # Hex encoding
        r'%[0-9a-fA-F]{2}',  # URL encoding of dangerous chars
    ]
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|DECLARE)\b)",
        r"(--|#|/\*|\*/)",  # SQL comments
        r"(\bOR\b.*=.*|1=1|'=')",  # Common SQL injection
        r"(;.*--)",  # Statement termination with comment
        r"(\bxp_|\bsp_)",  # SQL Server stored procedures
    ]
    
    # Script injection patterns (XSS)
    SCRIPT_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',  # Event handlers
        r'<iframe',
        r'<object',
        r'<embed',
    ]
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'image': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'},
        'video': {'.mp4', '.webm', '.avi', '.mov'},
        'audio': {'.mp3', '.wav', '.m4a', '.ogg', '.webm'},
        'document': {'.pdf', '.doc', '.docx', '.txt'},
        'code': {'.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts'}
    }
    
    # Maximum sizes (in bytes)
    MAX_SIZES = {
        'image': 10 * 1024 * 1024,  # 10MB
        'video': 100 * 1024 * 1024,  # 100MB
        'audio': 50 * 1024 * 1024,  # 50MB
        'document': 10 * 1024 * 1024,  # 10MB
        'code': 1 * 1024 * 1024,  # 1MB
    }
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 10000, allow_html: bool = False) -> str:
        """
        Sanitize string input to prevent XSS and injection attacks
        
        Args:
            value: Input string to sanitize
            max_length: Maximum allowed length
            allow_html: Whether to allow safe HTML tags
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            raise ValueError("Input must be a string")
        
        # Normalize unicode
        value = unicodedata.normalize('NFKC', value)
        
        # Truncate to max length
        value = value[:max_length]
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        if allow_html:
            # Allow only safe HTML tags
            allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'code', 'pre']
            allowed_attrs = {'a': ['href', 'title']}
            value = bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs, strip=True)
        else:
            # Escape all HTML
            value = html.escape(value)
        
        return value.strip()
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """
        Validate email format
        
        Returns:
            (is_valid, error_message)
        """
        if not email or not isinstance(email, str):
            return False, "Email is required"
        
        email = email.strip().lower()
        
        # Length check
        if len(email) > 254:
            return False, "Email is too long"
        
        # Basic format validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Invalid email format"
        
        # Check for dangerous patterns
        if any(char in email for char in ['<', '>', '"', "'", '\\', '/', ';']):
            return False, "Email contains invalid characters"
        
        return True, ""
    
    @staticmethod
    def validate_integer(value: Any, min_val: int = None, max_val: int = None) -> tuple[bool, Optional[int], str]:
        """
        Validate and convert integer input
        
        Returns:
            (is_valid, converted_value, error_message)
        """
        try:
            int_val = int(value)
            
            if min_val is not None and int_val < min_val:
                return False, None, f"Value must be at least {min_val}"
            
            if max_val is not None and int_val > max_val:
                return False, None, f"Value must be at most {max_val}"
            
            return True, int_val, ""
        except (ValueError, TypeError):
            return False, None, "Invalid integer value"
    
    @staticmethod
    def validate_float(value: Any, min_val: float = None, max_val: float = None) -> tuple[bool, Optional[float], str]:
        """
        Validate and convert float input
        
        Returns:
            (is_valid, converted_value, error_message)
        """
        try:
            float_val = float(value)
            
            if min_val is not None and float_val < min_val:
                return False, None, f"Value must be at least {min_val}"
            
            if max_val is not None and float_val > max_val:
                return False, None, f"Value must be at most {max_val}"
            
            return True, float_val, ""
        except (ValueError, TypeError):
            return False, None, "Invalid float value"
    
    @staticmethod
    def validate_enum(value: str, allowed_values: List[str], case_sensitive: bool = False) -> tuple[bool, str]:
        """
        Validate that value is in allowed list
        
        Returns:
            (is_valid, error_message)
        """
        if not case_sensitive:
            value = value.lower()
            allowed_values = [v.lower() for v in allowed_values]
        
        if value not in allowed_values:
            return False, f"Value must be one of: {', '.join(allowed_values)}"
        
        return True, ""
    
    @staticmethod
    def check_sql_injection(value: str) -> tuple[bool, str]:
        """
        Check for SQL injection patterns
        
        Returns:
            (is_safe, warning_message)
        """
        if not isinstance(value, str):
            return True, ""
        
        value_upper = value.upper()
        
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value_upper, re.IGNORECASE):
                return False, "Input contains potentially dangerous SQL patterns"
        
        return True, ""
    
    @staticmethod
    def check_command_injection(value: str) -> tuple[bool, str]:
        """
        Check for command injection patterns
        
        Returns:
            (is_safe, warning_message)
        """
        if not isinstance(value, str):
            return True, ""
        
        for pattern in InputValidator.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, value):
                return False, "Input contains potentially dangerous command characters"
        
        return True, ""
    
    @staticmethod
    def check_script_injection(value: str) -> tuple[bool, str]:
        """
        Check for script injection (XSS) patterns
        
        Returns:
            (is_safe, warning_message)
        """
        if not isinstance(value, str):
            return True, ""
        
        for pattern in InputValidator.SCRIPT_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return False, "Input contains potentially dangerous script patterns"
        
        return True, ""
    
    @staticmethod
    def validate_filename(filename: str, file_type: str = None) -> tuple[bool, str]:
        """
        Validate filename for security
        
        Args:
            filename: The filename to validate
            file_type: Type of file (image, video, audio, document, code)
            
        Returns:
            (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is required"
        
        # Remove path components
        filename = Path(filename).name
        
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Filename contains invalid path characters"
        
        # Check for null bytes
        if '\x00' in filename:
            return False, "Filename contains null bytes"
        
        # Check length
        if len(filename) > 255:
            return False, "Filename is too long"
        
        # Check extension if file_type specified
        if file_type:
            ext = Path(filename).suffix.lower()
            allowed = InputValidator.ALLOWED_EXTENSIONS.get(file_type, set())
            if ext not in allowed:
                return False, f"File type not allowed. Allowed: {', '.join(allowed)}"
        
        return True, ""
    
    @staticmethod
    def validate_file_size(size: int, file_type: str = None) -> tuple[bool, str]:
        """
        Validate file size
        
        Returns:
            (is_valid, error_message)
        """
        if size <= 0:
            return False, "File is empty"
        
        if file_type:
            max_size = InputValidator.MAX_SIZES.get(file_type, 10 * 1024 * 1024)
            if size > max_size:
                max_mb = max_size / (1024 * 1024)
                return False, f"File too large. Maximum size: {max_mb}MB"
        
        return True, ""
    
    @staticmethod
    def sanitize_code(code: str, language: str) -> tuple[bool, str, str]:
        """
        Sanitize code input for execution
        
        Returns:
            (is_safe, sanitized_code, error_message)
        """
        if not code or not isinstance(code, str):
            return False, "", "Code is required"
        
        # Length check
        if len(code) > 100000:  # 100KB
            return False, "", "Code is too long"
        
        # Check for dangerous imports/commands
        dangerous_patterns = {
            'python': [
                r'\bos\.system\b',
                r'\bsubprocess\.',
                r'\beval\(',
                r'\bexec\(',
                r'\b__import__\(',
                r'\bopen\(',  # File operations
                r'\bcompile\(',
            ],
            'javascript': [
                r'\beval\(',
                r'\bFunction\(',
                r'\brequire\(',
                r'\bprocess\.',
                r'\bchild_process',
            ],
            'java': [
                r'\bRuntime\.getRuntime\(',
                r'\bProcessBuilder',
                r'\bSystem\.exit\(',
            ]
        }
        
        patterns = dangerous_patterns.get(language.lower(), [])
        for pattern in patterns:
            if re.search(pattern, code):
                return False, "", f"Code contains potentially dangerous operation: {pattern}"
        
        return True, code, ""
    
    @staticmethod
    def validate_url(url: str, allow_relative: bool = False) -> tuple[bool, str]:
        """
        Validate URL for safety
        
        Returns:
            (is_valid, error_message)
        """
        if not url:
            return False, "URL is required"
        
        # Check for javascript: and data: URLs
        if url.lower().startswith(('javascript:', 'data:', 'vbscript:')):
            return False, "URL scheme not allowed"
        
        if allow_relative and url.startswith('/'):
            return True, ""
        
        try:
            parsed = urlparse(url)
            if not parsed.scheme in ['http', 'https']:
                return False, "Only HTTP and HTTPS URLs are allowed"
            return True, ""
        except Exception:
            return False, "Invalid URL format"
    
    @staticmethod
    def validate_json_structure(data: Dict, required_fields: List[str] = None, 
                               optional_fields: List[str] = None) -> tuple[bool, str]:
        """
        Validate JSON structure
        
        Returns:
            (is_valid, error_message)
        """
        if not isinstance(data, dict):
            return False, "Data must be a JSON object"
        
        # Check required fields
        if required_fields:
            missing = [f for f in required_fields if f not in data]
            if missing:
                return False, f"Missing required fields: {', '.join(missing)}"
        
        # Check for unexpected fields
        if optional_fields is not None:
            allowed = set(required_fields or []) | set(optional_fields)
            unexpected = set(data.keys()) - allowed
            if unexpected:
                return False, f"Unexpected fields: {', '.join(unexpected)}"
        
        return True, ""


class QueryParameterValidator:
    """Validator for URL query parameters"""
    
    @staticmethod
    def validate_pagination(page: Any = 1, limit: Any = 10, max_limit: int = 100) -> tuple[bool, Dict, str]:
        """
        Validate pagination parameters
        
        Returns:
            (is_valid, {page, limit}, error_message)
        """
        is_valid_page, page_val, page_err = InputValidator.validate_integer(page, min_val=1, max_val=10000)
        if not is_valid_page:
            return False, {}, f"Invalid page: {page_err}"
        
        is_valid_limit, limit_val, limit_err = InputValidator.validate_integer(limit, min_val=1, max_val=max_limit)
        if not is_valid_limit:
            return False, {}, f"Invalid limit: {limit_err}"
        
        return True, {"page": page_val, "limit": limit_val}, ""
    
    @staticmethod
    def validate_sort_params(sort_by: str, order: str, allowed_fields: List[str]) -> tuple[bool, Dict, str]:
        """
        Validate sorting parameters
        
        Returns:
            (is_valid, {sort_by, order}, error_message)
        """
        # Validate sort field
        is_valid_field, field_err = InputValidator.validate_enum(sort_by, allowed_fields)
        if not is_valid_field:
            return False, {}, field_err
        
        # Validate order
        is_valid_order, order_err = InputValidator.validate_enum(order, ['asc', 'desc'])
        if not is_valid_order:
            return False, {}, order_err
        
        return True, {"sort_by": sort_by, "order": order}, ""
    
    @staticmethod
    def validate_search_query(query: str, min_length: int = 1, max_length: int = 200) -> tuple[bool, str, str]:
        """
        Validate search query
        
        Returns:
            (is_valid, sanitized_query, error_message)
        """
        if not query:
            return False, "", "Search query is required"
        
        query = query.strip()
        
        if len(query) < min_length:
            return False, "", f"Search query must be at least {min_length} characters"
        
        if len(query) > max_length:
            return False, "", f"Search query must be at most {max_length} characters"
        
        # Check for SQL injection
        is_safe_sql, sql_err = InputValidator.check_sql_injection(query)
        if not is_safe_sql:
            return False, "", sql_err
        
        # Sanitize
        sanitized = InputValidator.sanitize_string(query, max_length=max_length)
        
        return True, sanitized, ""


class FormValidator:
    """Validator for form submissions"""
    
    @staticmethod
    def validate_registration(name: str, email: str, password: str, confirm_password: str = None) -> tuple[bool, Dict, str]:
        """
        Validate user registration form
        
        Returns:
            (is_valid, sanitized_data, error_message)
        """
        # Validate name
        if not name or len(name.strip()) < 2:
            return False, {}, "Name must be at least 2 characters"
        
        if len(name) > 100:
            return False, {}, "Name is too long"
        
        name = InputValidator.sanitize_string(name, max_length=100)
        
        # Validate email
        is_valid_email, email_err = InputValidator.validate_email(email)
        if not is_valid_email:
            return False, {}, email_err
        
        email = email.strip().lower()
        
        # Validate password
        if not password or len(password) < 8:
            return False, {}, "Password must be at least 8 characters"
        
        if len(password) > 128:
            return False, {}, "Password is too long"
        
        # Check password confirmation
        if confirm_password is not None and password != confirm_password:
            return False, {}, "Passwords do not match"
        
        return True, {"name": name, "email": email, "password": password}, ""
    
    @staticmethod
    def validate_question_submission(question: str, answer: str, category: str = None) -> tuple[bool, Dict, str]:
        """
        Validate question/answer submission
        
        Returns:
            (is_valid, sanitized_data, error_message)
        """
        # Validate question
        if not question or len(question.strip()) < 5:
            return False, {}, "Question must be at least 5 characters"
        
        if len(question) > 5000:
            return False, {}, "Question is too long"
        
        question = InputValidator.sanitize_string(question, max_length=5000)
        
        # Validate answer
        if not answer or len(answer.strip()) < 10:
            return False, {}, "Answer must be at least 10 characters"
        
        if len(answer) > 50000:
            return False, {}, "Answer is too long"
        
        answer = InputValidator.sanitize_string(answer, max_length=50000)
        
        # Validate category if provided
        if category:
            allowed_categories = [
                'Behavioral', 'Technical', 'System Design', 'Coding', 
                'Leadership', 'HR Interview', 'Case Study'
            ]
            is_valid_cat, cat_err = InputValidator.validate_enum(category, allowed_categories)
            if not is_valid_cat:
                return False, {}, cat_err
        
        return True, {"question": question, "answer": answer, "category": category}, ""


# Export main classes
__all__ = ['InputValidator', 'QueryParameterValidator', 'FormValidator']
