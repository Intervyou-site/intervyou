"""
Code Executor with Docker sandboxing and AI-powered error analysis
"""
import os
import subprocess
import tempfile
import time
import re
import hashlib
from typing import Dict, Any, Optional
from .language_configs import LANGUAGE_CONFIGS
import sys
import asyncio

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import LLM utilities
try:
    from src.llm_utils import call_llm_chat
    LLM_AVAILABLE = True
    # Check if API key is actually configured
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        LLM_AVAILABLE = False
except ImportError:
    LLM_AVAILABLE = False
    call_llm_chat = None

# Simple in-memory cache for AI responses (to reduce API calls)
_ai_response_cache = {}
_cache_max_size = 100  # Limit cache size


class CodeExecutor:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def execute_code(self, code: str, language: str, input_data: str = "") -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment
        """
        if language not in LANGUAGE_CONFIGS:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "output": "",
                "execution_time": 0
            }
        
        config = LANGUAGE_CONFIGS[language]
        
        try:
            # Create temporary file
            file_name = f"code_{int(time.time())}{config['extension']}"
            file_path = os.path.join(self.temp_dir, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            start_time = time.time()
            
            # Check if Docker is available
            docker_available = self._check_docker()
            
            if docker_available:
                result = self._execute_in_docker(file_path, config, input_data)
            else:
                # Execute locally with a note
                result = self._execute_locally(file_path, config, input_data)
                if result['success']:
                    result['note'] = "⚠️ Running locally (Docker not available). For enhanced security, install Docker Desktop."
            
            execution_time = time.time() - start_time
            
            # Clean up
            try:
                os.remove(file_path)
                if config['compile_cmd']:
                    # Remove compiled files
                    if language == "java":
                        class_file = os.path.join(self.temp_dir, "Main.class")
                        if os.path.exists(class_file):
                            os.remove(class_file)
                    elif language in ["cpp", "c"]:
                        program_file = os.path.join(self.temp_dir, "program")
                        if os.path.exists(program_file):
                            os.remove(program_file)
            except:
                pass
            
            result['execution_time'] = round(execution_time, 3)
            
            # If there's an error, add AI-powered explanation
            if not result['success'] and result.get('error'):
                result['ai_explanation'] = self._get_ai_error_explanation(
                    code, language, result['error'], result.get('output', '')
                )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "execution_time": 0,
                "ai_explanation": "An unexpected error occurred during code execution."
            }
    
    def _check_docker(self) -> bool:
        """Check if Docker is available and running"""
        try:
            # Check if docker command exists
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5,
                text=True
            )
            # Docker is available if command succeeds
            return result.returncode == 0
        except FileNotFoundError:
            # Docker command not found
            return False
        except subprocess.TimeoutExpired:
            # Docker command timed out (daemon might not be running)
            return False
        except Exception:
            return False
    
    def _execute_in_docker(self, file_path: str, config: Dict, input_data: str) -> Dict[str, Any]:
        """Execute code in Docker container"""
        try:
            file_name = os.path.basename(file_path)
            
            # Compile if needed
            if config['compile_cmd']:
                compile_cmd = config['compile_cmd'].format(file=file_name)
                docker_compile = [
                    "docker", "run", "--rm",
                    "-v", f"{self.temp_dir}:/code",
                    "-w", "/code",
                    f"--memory={config['memory_limit']}",
                    config['docker_image'],
                    "sh", "-c", compile_cmd
                ]
                
                compile_result = subprocess.run(
                    docker_compile,
                    capture_output=True,
                    text=True,
                    timeout=config['timeout']
                )
                
                if compile_result.returncode != 0:
                    return {
                        "success": False,
                        "error": compile_result.stderr,
                        "output": compile_result.stdout
                    }
            
            # Run code
            run_cmd = config['run_cmd'].format(file=file_name)
            docker_run = [
                "docker", "run", "--rm",
                "-i",  # Interactive mode to enable stdin
                "-v", f"{self.temp_dir}:/code",
                "-w", "/code",
                f"--memory={config['memory_limit']}",
                "--network=none",  # No network access
                config['docker_image'],
                "sh", "-c", run_cmd
            ]
            
            run_result = subprocess.run(
                docker_run,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=config['timeout']
            )
            
            return {
                "success": run_result.returncode == 0,
                "output": run_result.stdout,
                "error": run_result.stderr if run_result.returncode != 0 else ""
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out (limit: {config['timeout']}s)",
                "output": ""
            }
        except FileNotFoundError:
            # Docker command not found - fall back to local execution
            return self._execute_locally(file_path, config, input_data)
        except Exception as e:
            error_msg = str(e)
            # If Docker error, try local execution as fallback
            if "docker" in error_msg.lower() or "daemon" in error_msg.lower():
                return self._execute_locally(file_path, config, input_data)
            return {
                "success": False,
                "error": error_msg,
                "output": ""
            }
    
    def _execute_locally(self, file_path: str, config: Dict, input_data: str) -> Dict[str, Any]:
        """Execute code locally (fallback when Docker is not available)"""
        try:
            file_name = os.path.basename(file_path)
            work_dir = os.path.dirname(file_path)
            
            # Compile if needed
            if config['compile_cmd']:
                compile_cmd = config['compile_cmd'].format(file=file_name)
                compile_result = subprocess.run(
                    compile_cmd,
                    shell=True,
                    cwd=work_dir,
                    capture_output=True,
                    text=True,
                    timeout=config['timeout']
                )
                
                if compile_result.returncode != 0:
                    return {
                        "success": False,
                        "error": compile_result.stderr,
                        "output": compile_result.stdout
                    }
            
            # Run code
            run_cmd = config['run_cmd'].format(file=file_name)
            run_result = subprocess.run(
                run_cmd,
                shell=True,
                cwd=work_dir,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=config['timeout']
            )
            
            return {
                "success": run_result.returncode == 0,
                "output": run_result.stdout,
                "error": run_result.stderr if run_result.returncode != 0 else ""
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out (limit: {config['timeout']}s)",
                "output": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": ""
            }
    
    def _get_ai_error_explanation(self, code: str, language: str, error: str, output: str) -> Dict[str, Any]:
        """
        Use AI to explain the error and suggest fixes
        This is the UNIQUE feature that sets this IDE apart!
        """
        try:
            # First, try to parse the error intelligently
            parsed_error = self._parse_error(error, language)
            
            # Check for common errors first
            config = LANGUAGE_CONFIGS.get(language, {})
            common_errors = config.get('common_errors', {})
            
            quick_hint = None
            for error_type, hint in common_errors.items():
                if error_type.lower() in error.lower():
                    quick_hint = hint
                    break
            
            # If no quick hint, generate one from parsed error
            if not quick_hint:
                quick_hint = parsed_error.get('quick_hint', 'Check the error message for details.')
            
            # Try to get AI-powered detailed explanation
            if LLM_AVAILABLE and call_llm_chat:
                try:
                    detailed_analysis = self._get_ai_detailed_analysis(code, language, error, output, parsed_error)
                except Exception as e:
                    print(f"AI analysis failed: {e}")
                    detailed_analysis = self._get_fallback_analysis(parsed_error, language)
            else:
                # Use intelligent fallback
                detailed_analysis = self._get_fallback_analysis(parsed_error, language)
            
            return {
                "quick_hint": quick_hint,
                "detailed_analysis": detailed_analysis
            }
            
        except Exception as e:
            print(f"Error in _get_ai_error_explanation: {e}")
            return {
                "quick_hint": "An error occurred in your code. Check the error message for details.",
                "detailed_analysis": {
                    "explanation": "Review the error message above for clues about what went wrong.",
                    "problem_location": "Check the line number in the error message",
                    "fix": "Read the error message carefully and check your syntax",
                    "tip": "Test your code with simple inputs first"
                }
            }
    
    def _has_obvious_syntax_error(self, code: str, language: str) -> bool:
        """Check for OBVIOUS syntax errors only - avoid false positives"""
        try:
            if language == "python":
                # Python: Use AST parser (very accurate)
                import ast
                try:
                    ast.parse(code)
                    return False  # No syntax errors
                except SyntaxError:
                    return True  # Has syntax errors
            
            # For other languages, be VERY conservative
            # Only flag if there's an obvious structural problem
            
            # Check if code is completely empty
            if not code.strip():
                return True
            
            # For JavaScript and other languages, don't try to parse
            # Just assume it's valid unless it's obviously broken
            # The actual execution will catch real errors
            return False
            
        except Exception as e:
            # If we can't check, assume no syntax errors
            print(f"Syntax check error: {e}")
            return False
    
    def _parse_error(self, error: str, language: str) -> Dict[str, Any]:
        """Parse error message to extract useful information"""
        result = {
            "error_type": "Unknown",
            "line_number": None,
            "message": error,
            "quick_hint": None
        }
        
        if language == "python":
            # Parse Python errors
            if "SyntaxError" in error:
                result["error_type"] = "SyntaxError"
                result["quick_hint"] = "There's a syntax mistake in your code. Check for missing colons, parentheses, or quotes."
                # Extract line number
                import re
                line_match = re.search(r'line (\d+)', error)
                if line_match:
                    result["line_number"] = int(line_match.group(1))
                # Check for specific syntax issues
                if "invalid character" in error.lower():
                    result["quick_hint"] = "You have an invalid character in your code. This might be a special Unicode character that Python doesn't recognize."
                elif "expected" in error.lower():
                    result["quick_hint"] = "Python expected something different. Check if you're missing a closing bracket, parenthesis, or quote."
            
            elif "IndentationError" in error:
                result["error_type"] = "IndentationError"
                result["quick_hint"] = "Python uses indentation to define code blocks. Make sure your code is properly indented with consistent spaces or tabs."
            
            elif "NameError" in error:
                result["error_type"] = "NameError"
                result["quick_hint"] = "You're trying to use a variable or function that hasn't been defined yet. Check your spelling and make sure you've defined it before using it."
            
            elif "TypeError" in error:
                result["error_type"] = "TypeError"
                result["quick_hint"] = "You're trying to perform an operation on incompatible data types. For example, you can't add a string to a number."
            
            elif "IndexError" in error:
                result["error_type"] = "IndexError"
                result["quick_hint"] = "You're trying to access an index that doesn't exist in your list. Remember, Python lists start at index 0."
            
            elif "KeyError" in error:
                result["error_type"] = "KeyError"
                result["quick_hint"] = "You're trying to access a dictionary key that doesn't exist. Use .get() method or check if the key exists first."
            
            elif "ValueError" in error:
                result["error_type"] = "ValueError"
                result["quick_hint"] = "The value you're using is not appropriate for the operation. For example, trying to convert a non-numeric string to an integer."
            
            elif "AttributeError" in error:
                result["error_type"] = "AttributeError"
                result["quick_hint"] = "You're trying to access an attribute or method that doesn't exist on this object."
            
            elif "ZeroDivisionError" in error:
                result["error_type"] = "ZeroDivisionError"
                result["quick_hint"] = "You're trying to divide by zero. Add a check to make sure the divisor is not zero."
        
        elif language == "javascript":
            if "ReferenceError" in error:
                result["error_type"] = "ReferenceError"
                result["quick_hint"] = "You're trying to use a variable that hasn't been declared. Use 'let', 'const', or 'var' to declare it first."
            elif "TypeError" in error:
                result["error_type"] = "TypeError"
                result["quick_hint"] = "You're performing an invalid operation. Check if you're calling a function on the right type of value."
            elif "SyntaxError" in error:
                result["error_type"] = "SyntaxError"
                result["quick_hint"] = "There's a syntax error in your code. Check for missing brackets, semicolons, or quotes."
        
        return result
    
    def _get_fallback_analysis(self, parsed_error: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Provide intelligent fallback analysis when AI is not available"""
        error_type = parsed_error.get("error_type", "Unknown")
        line_number = parsed_error.get("line_number")
        
        # Build explanation based on error type
        explanations = {
            "SyntaxError": {
                "explanation": f"Your code has a syntax error. This means Python can't understand the structure of your code. Common causes include missing colons, unmatched brackets, or incorrect indentation.",
                "problem_location": f"Line {line_number}" if line_number else "Check the error message for the line number",
                "fix": "Review the line mentioned in the error. Look for missing colons at the end of if/for/while/def statements, unmatched parentheses or brackets, or missing quotes around strings.",
                "tip": "Use a code editor with syntax highlighting to catch these errors early. Python is very particular about syntax!"
            },
            "IndentationError": {
                "explanation": "Python uses indentation (spaces or tabs) to define code blocks. Your code has inconsistent or incorrect indentation.",
                "problem_location": f"Line {line_number}" if line_number else "Check where your indentation changes",
                "fix": "Make sure all lines in the same block have the same indentation. Use either 4 spaces or 1 tab consistently throughout your code. Don't mix spaces and tabs!",
                "tip": "Most Python developers use 4 spaces for indentation. Configure your editor to insert spaces when you press Tab."
            },
            "NameError": {
                "explanation": "You're trying to use a variable or function name that Python doesn't recognize. This usually means you haven't defined it yet, or there's a typo in the name.",
                "problem_location": f"Line {line_number}" if line_number else "Look for undefined variables",
                "fix": "Check the spelling of the variable name. Make sure you've defined the variable before using it. Remember that Python is case-sensitive (myVar and myvar are different).",
                "tip": "Define variables before you use them, and watch out for typos. Use descriptive names to avoid confusion."
            },
            "TypeError": {
                "explanation": "You're trying to perform an operation on incompatible data types. For example, you can't add a string to a number, or call a method that doesn't exist on that type.",
                "problem_location": f"Line {line_number}" if line_number else "Check your operations",
                "fix": "Convert data types when needed (e.g., str(5) to convert number to string, int('5') to convert string to number). Make sure you're calling methods that exist on that object type.",
                "tip": "Use type() function to check what type a variable is. Print intermediate values to debug type issues."
            },
            "IndexError": {
                "explanation": "You're trying to access a list index that doesn't exist. Remember, Python lists are zero-indexed (first element is at index 0).",
                "problem_location": f"Line {line_number}" if line_number else "Check your list access",
                "fix": "Make sure the index is within the valid range. For a list of length n, valid indices are 0 to n-1. Use len(list) to check the list length before accessing.",
                "tip": "Use list slicing or check the length before accessing: if index < len(my_list): ..."
            },
            "ValueError": {
                "explanation": "The value you're using is not appropriate for the operation you're trying to perform. Common example: trying to convert a non-numeric string to an integer.",
                "problem_location": f"Line {line_number}" if line_number else "Check your value conversions",
                "fix": "Validate input before converting. Use try-except blocks to handle conversion errors gracefully. Check if the value is in the expected format.",
                "tip": "Use try-except blocks when converting user input: try: num = int(input()) except ValueError: print('Invalid number')"
            },
            "ZeroDivisionError": {
                "explanation": "You're attempting to divide by zero, which is mathematically undefined and causes an error in Python.",
                "problem_location": f"Line {line_number}" if line_number else "Check your division operations",
                "fix": "Add a check before dividing: if divisor != 0: result = numerator / divisor. Or use try-except to handle the error.",
                "tip": "Always validate that your divisor is not zero before performing division operations."
            }
        }
        
        # Get explanation for this error type, or use generic
        analysis = explanations.get(error_type, {
            "explanation": "An error occurred in your code. Review the error message carefully for clues about what went wrong.",
            "problem_location": f"Line {line_number}" if line_number else "Check the error message for the line number",
            "fix": "Read the error message carefully. It usually tells you exactly what's wrong. Check your syntax, variable names, and logic.",
            "tip": "Break down your code into smaller parts and test each part separately to isolate the problem."
        })
        
        return analysis
    
    def _get_ai_detailed_analysis(self, code: str, language: str, error: str, output: str, parsed_error: Dict) -> Dict[str, Any]:
        """Get AI-powered detailed analysis with caching and better error handling"""
        
        # Create cache key from error type and message (not full code to avoid cache misses)
        cache_key = hashlib.md5(
            f"{language}:{parsed_error.get('error_type')}:{error[:200]}".encode()
        ).hexdigest()
        
        # Check cache first
        if cache_key in _ai_response_cache:
            print("Using cached AI response")
            return _ai_response_cache[cache_key]
        
        prompt = f"""You are a helpful coding tutor. A student is learning {language} and encountered an error.

Code:
```{language}
{code[:500]}  # Limit code length
```

Error Message:
{error[:300]}  # Limit error length

Error Type: {parsed_error.get('error_type', 'Unknown')}
Line Number: {parsed_error.get('line_number', 'Unknown')}

Please provide a brief, beginner-friendly explanation in JSON format with these keys:
- explanation: What went wrong (2-3 sentences)
- problem_location: Specific line or part causing the issue
- fix: Concrete steps to fix it
- tip: One helpful tip to avoid this in future

Keep it concise and encouraging. Focus on learning."""

        try:
            # Call async function synchronously
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(call_llm_chat("You are a helpful coding tutor.", prompt, model="gpt-4o-mini", max_tokens=400))
                    )
                    ai_response = future.result(timeout=15)  # Increased timeout for retries
            else:
                ai_response = loop.run_until_complete(
                    call_llm_chat("You are a helpful coding tutor.", prompt, model="gpt-4o-mini", max_tokens=400)
                )
            
            # Try to parse JSON response
            import json
            try:
                ai_data = json.loads(ai_response)
                
                # Cache the successful response
                if len(_ai_response_cache) >= _cache_max_size:
                    # Remove oldest entry (simple FIFO)
                    _ai_response_cache.pop(next(iter(_ai_response_cache)))
                _ai_response_cache[cache_key] = ai_data
                
                return ai_data
            except:
                # If not JSON, use fallback
                return self._get_fallback_analysis(parsed_error, language)
                
        except Exception as e:
            error_msg = str(e)
            print(f"AI call failed: {e}")
            
            # Check if it's a rate limit error
            if "429" in error_msg or "rate limit" in error_msg.lower():
                # Return fallback with rate limit message
                fallback = self._get_fallback_analysis(parsed_error, language)
                fallback["rate_limit_note"] = "⚠️ AI analysis temporarily unavailable due to rate limits. The explanation below is based on common error patterns."
                return fallback
            
            return self._get_fallback_analysis(parsed_error, language)
    
    def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code quality and provide suggestions
        Another unique feature!
        """
        try:
            # First, do basic static analysis
            basic_analysis = self._basic_code_analysis(code, language)
            
            # Try AI-powered analysis if available
            if LLM_AVAILABLE and call_llm_chat:
                try:
                    ai_analysis = self._get_ai_code_analysis(code, language, basic_analysis)
                    return ai_analysis
                except Exception as e:
                    print(f"AI analysis failed: {e}")
                    return basic_analysis
            else:
                return basic_analysis
            
        except Exception as e:
            print(f"Error in analyze_code_quality: {e}")
            return {
                "score": 5,
                "strengths": ["Code structure looks reasonable"],
                "improvements": ["Consider adding comments to explain complex logic"],
                "performance_tip": "Test your code with various inputs to ensure it handles edge cases"
            }
    
    def _basic_code_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Perform basic static code analysis without AI"""
        score = 5  # Start with middle score
        strengths = []
        improvements = []
        
        # Only check for OBVIOUS syntax errors (very strict check)
        # We don't want false positives
        has_obvious_error = self._has_obvious_syntax_error(code, language)
        if has_obvious_error:
            return {
                "score": 2,
                "strengths": ["You're practicing and learning from errors"],
                "improvements": [
                    "Fix the syntax errors in your code first",
                    "Check for missing colons, brackets, or quotes",
                    "Review the error message in the Output tab"
                ],
                "performance_tip": "Fix syntax errors before analyzing code quality. Use the AI Help tab for guidance on fixing errors."
            }
        
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        
        if language == "python":
            # Check for docstrings
            if '"""' in code or "'''" in code:
                strengths.append("Good use of docstrings for documentation")
                score += 1
            else:
                improvements.append("Add docstrings to document your functions and classes")
            
            # Check for functions
            if 'def ' in code:
                strengths.append("Code is organized into functions")
                score += 1
            else:
                if len(non_empty_lines) > 10:
                    improvements.append("Consider breaking code into smaller functions for better organization")
            
            # Check for comments
            comment_lines = [line for line in lines if line.strip().startswith('#')]
            if len(comment_lines) > 0:
                strengths.append("Code includes helpful comments")
                score += 0.5
            else:
                if len(non_empty_lines) > 5:
                    improvements.append("Add comments to explain complex logic")
            
            # Check for type hints
            if '->' in code or ': int' in code or ': str' in code:
                strengths.append("Uses type hints for better code clarity")
                score += 1
            else:
                improvements.append("Consider adding type hints to function parameters and return values")
            
            # Check for error handling
            if 'try:' in code and 'except' in code:
                strengths.append("Includes error handling with try-except blocks")
                score += 1
            else:
                improvements.append("Add error handling for robust code")
            
            # Check for meaningful variable names
            if any(len(word) > 2 for line in non_empty_lines for word in line.split() if word.isidentifier()):
                strengths.append("Uses descriptive variable names")
                score += 0.5
            
            # Check code length
            if len(non_empty_lines) > 50:
                improvements.append("Consider breaking this into smaller, more manageable functions")
                score -= 0.5
            
            # Check for main guard
            if 'if __name__ == "__main__":' in code:
                strengths.append("Properly uses if __name__ == '__main__' guard")
                score += 0.5
        
        elif language == "javascript":
            # Check for const/let vs var
            if 'const ' in code or 'let ' in code:
                strengths.append("Uses modern const/let instead of var")
                score += 1
            else:
                improvements.append("Use const or let instead of var for better scoping")
            
            # Check for arrow functions
            if '=>' in code:
                strengths.append("Uses modern arrow function syntax")
                score += 0.5
            
            # Check for functions
            if 'function ' in code or '=>' in code:
                strengths.append("Code is organized into functions")
                score += 1
            
            # Check for comments
            if '//' in code or '/*' in code:
                strengths.append("Includes helpful comments")
                score += 0.5
            else:
                improvements.append("Add comments to explain your logic")
            
            # Check for error handling
            if 'try' in code and 'catch' in code:
                strengths.append("Includes error handling")
                score += 1
            else:
                improvements.append("Add try-catch blocks for error handling")
        
        elif language in ["c", "cpp"]:
            # Check for comments
            comment_lines = [line for line in lines if line.strip().startswith('//') or '/*' in line]
            if len(comment_lines) > 0:
                strengths.append("Code includes helpful comments")
                score += 1
            else:
                if len(non_empty_lines) > 5:
                    improvements.append("Add comments to explain your logic")
            
            # Check for proper includes
            if '#include' in code:
                strengths.append("Properly includes necessary headers")
                score += 0.5
            
            # Check for functions (besides main)
            function_count = code.count('(') - code.count('main(')
            if function_count > 2:  # More than just main and one other
                strengths.append("Code is organized into functions")
                score += 1
            else:
                if len(non_empty_lines) > 15:
                    improvements.append("Consider breaking code into smaller functions")
            
            # Check for proper variable initialization
            if '= ' in code:  # Basic check for initialization
                strengths.append("Variables are properly initialized")
                score += 0.5
            
            # Check for return statement
            if 'return 0;' in code or 'return ' in code:
                strengths.append("Proper use of return statements")
                score += 0.5
            
            # C++ specific checks
            if language == "cpp":
                if 'using namespace std;' in code:
                    strengths.append("Uses C++ standard namespace")
                    score += 0.5
                
                if 'cout' in code or 'cin' in code:
                    strengths.append("Uses C++ I/O streams")
                    score += 0.5
                else:
                    improvements.append("Consider using cout/cin instead of printf/scanf")
                
                if 'vector' in code or 'string' in code:
                    strengths.append("Uses C++ STL containers")
                    score += 1
                else:
                    improvements.append("Consider using STL containers like vector or string")
            
            # C specific checks
            if language == "c":
                if 'printf' in code or 'scanf' in code:
                    strengths.append("Uses standard I/O functions")
                    score += 0.5
                
                if 'malloc' in code and 'free' in code:
                    strengths.append("Properly manages dynamic memory")
                    score += 1
                elif 'malloc' in code and 'free' not in code:
                    improvements.append("Remember to free() allocated memory to prevent leaks")
                    score -= 0.5
            
            # Check for magic numbers
            if any(char.isdigit() for line in non_empty_lines for char in line if not line.strip().startswith('//')):
                improvements.append("Consider using named constants instead of magic numbers")
        
        elif language == "java":
            # Check for comments
            if '//' in code or '/*' in code:
                strengths.append("Code includes helpful comments")
                score += 1
            else:
                if len(non_empty_lines) > 5:
                    improvements.append("Add comments to explain your logic")
            
            # Check for proper class structure
            if 'public class' in code or 'class ' in code:
                strengths.append("Proper class structure")
                score += 1
            
            # Check for methods (besides main)
            method_count = code.count('public ') + code.count('private ') + code.count('protected ')
            if method_count > 1:
                strengths.append("Code is organized into methods")
                score += 1
            else:
                if len(non_empty_lines) > 15:
                    improvements.append("Consider breaking code into smaller methods")
            
            # Check for proper naming conventions
            if any(word[0].isupper() for line in lines for word in line.split() if word and word[0].isalpha()):
                strengths.append("Follows Java naming conventions")
                score += 0.5
            
            # Check for error handling
            if 'try' in code and 'catch' in code:
                strengths.append("Includes proper error handling")
                score += 1
            else:
                improvements.append("Add try-catch blocks for error handling")
            
            # Check for access modifiers
            if 'private' in code or 'protected' in code:
                strengths.append("Uses proper encapsulation with access modifiers")
                score += 1
            else:
                improvements.append("Use private/protected modifiers for better encapsulation")
            
            # Check for modern Java features
            if 'List<' in code or 'ArrayList<' in code:
                strengths.append("Uses Java Collections Framework")
                score += 1
            
            if 'stream()' in code or 'lambda' in code or '->' in code:
                strengths.append("Uses modern Java 8+ features")
                score += 1
        
        # Cap score at 10
        score = min(10, max(1, round(score, 1)))
        
        # Ensure we have at least some feedback
        if not strengths:
            strengths = ["Your code runs successfully", "Basic structure is present"]
        if not improvements:
            improvements = ["Keep practicing and learning new concepts"]
        
        # Generate performance tip based on code
        performance_tips = [
            "Consider the time complexity of your algorithms - can you make it faster?",
            "Think about edge cases - what happens with empty inputs or very large numbers?",
            "Look for opportunities to reduce redundant calculations",
            "Consider using built-in functions and libraries for common operations",
            "Test your code with various inputs to ensure it's robust"
        ]
        
        import random
        performance_tip = random.choice(performance_tips)
        
        return {
            "score": score,
            "strengths": strengths[:3],  # Limit to top 3
            "improvements": improvements[:3],  # Limit to top 3
            "performance_tip": performance_tip
        }
    
    def _get_ai_code_analysis(self, code: str, language: str, basic_analysis: Dict) -> Dict[str, Any]:
        """Get AI-powered code analysis with caching and better error handling"""
        
        # Create cache key
        cache_key = hashlib.md5(
            f"quality:{language}:{code[:300]}".encode()
        ).hexdigest()
        
        # Check cache first
        if cache_key in _ai_response_cache:
            print("Using cached AI code analysis")
            return _ai_response_cache[cache_key]
        
        prompt = f"""Analyze this {language} code and provide brief feedback:

```{language}
{code[:500]}  # Limit code length
```

Basic Analysis Score: {basic_analysis['score']}/10

Provide concise feedback in JSON format with:
- score: number 1-10 (adjust the basic score if needed)
- strengths: array of 2-3 positive points
- improvements: array of 2-3 actionable suggestions
- performance_tip: one specific performance or best practice tip

Keep it encouraging and actionable."""

        try:
            # Call async function
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(call_llm_chat("You are a code quality analyzer.", prompt, model="gpt-4o-mini", max_tokens=400))
                    )
                    ai_response = future.result(timeout=15)  # Increased timeout for retries
            else:
                ai_response = loop.run_until_complete(
                    call_llm_chat("You are a code quality analyzer.", prompt, model="gpt-4o-mini", max_tokens=400)
                )
            
            import json
            try:
                analysis = json.loads(ai_response)
                # Ensure score is valid
                if 'score' in analysis:
                    analysis['score'] = min(10, max(1, analysis['score']))
                
                # Cache the successful response
                if len(_ai_response_cache) >= _cache_max_size:
                    _ai_response_cache.pop(next(iter(_ai_response_cache)))
                _ai_response_cache[cache_key] = analysis
                
                return analysis
            except:
                return basic_analysis
                
        except Exception as e:
            error_msg = str(e)
            print(f"AI analysis failed: {e}")
            
            # Check if it's a rate limit error
            if "429" in error_msg or "rate limit" in error_msg.lower():
                # Add note to basic analysis
                basic_analysis["rate_limit_note"] = "⚠️ AI-enhanced analysis temporarily unavailable due to rate limits. Showing basic analysis."
            
            return basic_analysis
