"""
Secure Code Execution Validator
Validates and sanitizes code before execution to prevent command injection
"""

import re
from typing import Tuple, List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CodeSecurityValidator:
    """Validate code for security issues before execution"""
    
    # Dangerous patterns by language
    DANGEROUS_PATTERNS = {
        'python': {
            'imports': [
                r'\bimport\s+os\b',
                r'\bfrom\s+os\s+import\b',
                r'\bimport\s+subprocess\b',
                r'\bfrom\s+subprocess\s+import\b',
                r'\bimport\s+sys\b',
                r'\bimport\s+socket\b',
                r'\bimport\s+requests\b',
                r'\bimport\s+urllib\b',
                r'\bimport\s+shutil\b',
                r'\bimport\s+pickle\b',
                r'\bimport\s+marshal\b',
                r'\bimport\s+ctypes\b',
            ],
            'functions': [
                r'\beval\s*\(',
                r'\bexec\s*\(',
                r'\bcompile\s*\(',
                r'\b__import__\s*\(',
                r'\bopen\s*\(',
                r'\bfile\s*\(',
                r'\binput\s*\(',
                r'\braw_input\s*\(',
                r'\bglobals\s*\(',
                r'\blocals\s*\(',
                r'\bvars\s*\(',
                r'\bdir\s*\(',
                r'\bgetattr\s*\(',
                r'\bsetattr\s*\(',
                r'\bdelattr\s*\(',
                r'\b__builtins__',
            ],
            'system': [
                r'os\.system',
                r'os\.popen',
                r'os\.spawn',
                r'os\.exec',
                r'subprocess\.',
                r'commands\.',
            ]
        },
        'javascript': {
            'functions': [
                r'\beval\s*\(',
                r'\bFunction\s*\(',
                r'\bsetTimeout\s*\(',
                r'\bsetInterval\s*\(',
                r'\brequire\s*\(',
                r'\bimport\s*\(',
            ],
            'system': [
                r'process\.exit',
                r'process\.kill',
                r'child_process',
                r'fs\.',
                r'require\s*\(\s*[\'"]fs[\'"]\s*\)',
                r'require\s*\(\s*[\'"]child_process[\'"]\s*\)',
            ],
            'network': [
                r'\bfetch\s*\(',
                r'\bXMLHttpRequest',
                r'require\s*\(\s*[\'"]http[\'"]\s*\)',
                r'require\s*\(\s*[\'"]https[\'"]\s*\)',
            ]
        },
        'java': {
            'system': [
                r'Runtime\.getRuntime\s*\(',
                r'ProcessBuilder',
                r'System\.exit',
                r'System\.load',
                r'System\.loadLibrary',
            ],
            'reflection': [
                r'Class\.forName',
                r'\.getClass\s*\(',
                r'\.getDeclaredMethod',
                r'\.invoke\s*\(',
            ],
            'io': [
                r'FileInputStream',
                r'FileOutputStream',
                r'FileReader',
                r'FileWriter',
                r'RandomAccessFile',
            ]
        },
        'cpp': {
            'system': [
                r'\bsystem\s*\(',
                r'\bexec\s*\(',
                r'\bpopen\s*\(',
            ],
            'io': [
                r'\bfopen\s*\(',
                r'\bfreopen\s*\(',
                r'\bremove\s*\(',
                r'\brename\s*\(',
            ]
        },
        'c': {
            'system': [
                r'\bsystem\s*\(',
                r'\bexec\s*\(',
                r'\bpopen\s*\(',
            ],
            'io': [
                r'\bfopen\s*\(',
                r'\bfreopen\s*\(',
                r'\bremove\s*\(',
                r'\brename\s*\(',
            ]
        }
    }
    
    # Maximum code length by language
    MAX_CODE_LENGTH = {
        'python': 50000,
        'javascript': 50000,
        'java': 100000,
        'cpp': 100000,
        'c': 100000,
        'go': 50000,
        'rust': 50000,
    }
    
    @staticmethod
    def validate_code_length(code: str, language: str) -> Tuple[bool, str]:
        """
        Validate code length
        
        Returns:
            (is_valid, error_message)
        """
        max_length = CodeSecurityValidator.MAX_CODE_LENGTH.get(language.lower(), 50000)
        
        if len(code) > max_length:
            return False, f"Code too long. Maximum: {max_length} characters"
        
        if len(code) == 0:
            return False, "Code is empty"
        
        return True, ""
    
    @staticmethod
    def check_dangerous_patterns(code: str, language: str) -> Tuple[bool, List[str]]:
        """
        Check code for dangerous patterns
        
        Returns:
            (is_safe, list_of_violations)
        """
        violations = []
        language = language.lower()
        
        if language not in CodeSecurityValidator.DANGEROUS_PATTERNS:
            # Unknown language - allow but log
            logger.warning(f"Unknown language for security check: {language}")
            return True, []
        
        patterns = CodeSecurityValidator.DANGEROUS_PATTERNS[language]
        
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, code, re.IGNORECASE):
                    violations.append(f"{category}: {pattern}")
        
        is_safe = len(violations) == 0
        return is_safe, violations
    
    @staticmethod
    def sanitize_input_data(input_data: str, max_length: int = 10000) -> Tuple[bool, str, str]:
        """
        Sanitize input data for code execution
        
        Returns:
            (is_valid, sanitized_data, error_message)
        """
        if not isinstance(input_data, str):
            return False, "", "Input data must be a string"
        
        # Check length
        if len(input_data) > max_length:
            return False, "", f"Input data too long. Maximum: {max_length} characters"
        
        # Remove null bytes
        input_data = input_data.replace('\x00', '')
        
        # Check for shell metacharacters
        dangerous_chars = ['`', '$', '|', ';', '&', '>', '<', '(', ')', '{', '}']
        for char in dangerous_chars:
            if char in input_data:
                logger.warning(f"Input data contains dangerous character: {char}")
                # Don't reject, but log - input data might legitimately contain these
        
        return True, input_data, ""
    
    @staticmethod
    def validate_language(language: str) -> Tuple[bool, str]:
        """
        Validate that language is supported
        
        Returns:
            (is_valid, error_message)
        """
        supported_languages = {
            'python', 'javascript', 'java', 'cpp', 'c',
            'go', 'rust', 'typescript', 'ruby', 'php'
        }
        
        language = language.lower()
        
        if language not in supported_languages:
            return False, f"Unsupported language: {language}"
        
        return True, ""
    
    @staticmethod
    def validate_execution_request(
        code: str,
        language: str,
        input_data: str = "",
        strict_mode: bool = True
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Comprehensive validation of code execution request
        
        Args:
            code: Code to execute
            language: Programming language
            input_data: Input data for the code
            strict_mode: If True, reject code with any dangerous patterns
            
        Returns:
            (is_valid, result_dict)
            result_dict contains either 'error' or 'warnings'
        """
        # Validate language
        is_valid_lang, lang_error = CodeSecurityValidator.validate_language(language)
        if not is_valid_lang:
            return False, {"error": lang_error}
        
        # Validate code length
        is_valid_length, length_error = CodeSecurityValidator.validate_code_length(code, language)
        if not is_valid_length:
            return False, {"error": length_error}
        
        # Check for dangerous patterns
        is_safe, violations = CodeSecurityValidator.check_dangerous_patterns(code, language)
        
        if not is_safe:
            if strict_mode:
                return False, {
                    "error": "Code contains dangerous operations",
                    "violations": violations
                }
            else:
                # Allow but warn
                logger.warning(f"Code contains dangerous patterns: {violations}")
        
        # Validate input data
        is_valid_input, sanitized_input, input_error = CodeSecurityValidator.sanitize_input_data(input_data)
        if not is_valid_input:
            return False, {"error": input_error}
        
        # Return success with any warnings
        result = {
            "sanitized_input": sanitized_input,
            "warnings": violations if violations else []
        }
        
        return True, result


class CommandInjectionPrevention:
    """Prevent command injection in system calls"""
    
    # Shell metacharacters that could be used for injection
    SHELL_METACHARACTERS = {
        ';', '&', '|', '`', '$', '(', ')', '{', '}',
        '<', '>', '\n', '\r', '\\', '"', "'", ' '
    }
    
    @staticmethod
    def is_safe_argument(arg: str) -> bool:
        """
        Check if argument is safe for shell execution
        
        Returns:
            True if safe, False otherwise
        """
        # Check for shell metacharacters
        for char in CommandInjectionPrevention.SHELL_METACHARACTERS:
            if char in arg:
                return False
        
        # Check for path traversal
        if '..' in arg:
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename_for_execution(filename: str) -> Optional[str]:
        """
        Sanitize filename for safe execution
        
        Returns:
            Sanitized filename or None if unsafe
        """
        # Only allow alphanumeric, underscore, hyphen, and dot
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
            return None
        
        # No path traversal
        if '..' in filename:
            return None
        
        # No hidden files
        if filename.startswith('.'):
            return None
        
        return filename
    
    @staticmethod
    def build_safe_command(base_command: str, args: List[str]) -> Optional[List[str]]:
        """
        Build safe command array for subprocess execution
        
        Args:
            base_command: Base command (e.g., 'python', 'node')
            args: List of arguments
            
        Returns:
            Safe command list or None if unsafe
        """
        # Validate base command
        allowed_commands = {
            'python', 'python3', 'node', 'java', 'javac',
            'gcc', 'g++', 'go', 'rustc', 'ruby', 'php'
        }
        
        if base_command not in allowed_commands:
            logger.error(f"Disallowed base command: {base_command}")
            return None
        
        # Validate all arguments
        safe_args = []
        for arg in args:
            if not CommandInjectionPrevention.is_safe_argument(arg):
                logger.error(f"Unsafe argument detected: {arg}")
                return None
            safe_args.append(arg)
        
        return [base_command] + safe_args


# Export main classes
__all__ = ['CodeSecurityValidator', 'CommandInjectionPrevention']
