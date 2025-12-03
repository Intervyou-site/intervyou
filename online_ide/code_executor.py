"""
Code Executor with Docker sandboxing and AI-powered error analysis
"""
import os
import subprocess
import tempfile
import time
import re
from typing import Dict, Any, Optional
from .language_configs import LANGUAGE_CONFIGS
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from llm_utils import call_llm_chat
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    call_llm_chat = None


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
                result = self._execute_locally(file_path, config, input_data)
            
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
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
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
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
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
            # Check for common errors first
            config = LANGUAGE_CONFIGS.get(language, {})
            common_errors = config.get('common_errors', {})
            
            quick_hint = None
            for error_type, hint in common_errors.items():
                if error_type.lower() in error.lower():
                    quick_hint = hint
                    break
            
            # Get AI-powered detailed explanation
            if not LLM_AVAILABLE or not call_llm_chat:
                return {
                    "quick_hint": quick_hint or "Check the error message for details.",
                    "detailed_analysis": {
                        "explanation": "AI explanation unavailable. LLM not configured.",
                        "problem_location": "Review the error message above",
                        "fix": "Check your syntax and logic",
                        "tip": "Read error messages carefully"
                    }
                }
            
            prompt = f"""You are a helpful coding tutor. A student is learning {language} and encountered an error.

Code:
```{language}
{code}
```

Error Message:
{error}

Output (if any):
{output}

Please provide:
1. A simple explanation of what went wrong (2-3 sentences, beginner-friendly)
2. The specific line or part of code causing the issue
3. A concrete fix or suggestion
4. A tip to avoid this error in the future

Keep it concise, friendly, and educational. Format as JSON with keys: explanation, problem_location, fix, tip"""

            # Call async function synchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ai_response = loop.run_until_complete(
                call_llm_chat("You are a helpful coding tutor.", prompt, model="gpt-4o-mini", max_tokens=500)
            )
            loop.close()
            
            # Try to parse JSON response
            import json
            try:
                ai_data = json.loads(ai_response)
            except:
                # Fallback if not JSON
                ai_data = {
                    "explanation": ai_response[:200] if ai_response else "Unable to parse AI response",
                    "problem_location": "Check the error message above",
                    "fix": "Review your code syntax and logic",
                    "tip": "Read error messages carefully - they often point to the exact issue"
                }
            
            return {
                "quick_hint": quick_hint,
                "detailed_analysis": ai_data
            }
            
        except Exception as e:
            return {
                "quick_hint": "An error occurred in your code. Check the error message for details.",
                "detailed_analysis": {
                    "explanation": "Unable to generate AI explanation at this time.",
                    "problem_location": "Review the error message",
                    "fix": "Check your syntax and logic",
                    "tip": "Test your code with simple inputs first"
                }
            }
    
    def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code quality and provide suggestions
        Another unique feature!
        """
        try:
            if not LLM_AVAILABLE or not call_llm_chat:
                return {
                    "score": 7,
                    "strengths": ["Code structure looks reasonable"],
                    "improvements": ["AI analysis unavailable - LLM not configured"],
                    "performance_tip": "Configure LLM for detailed analysis"
                }
            
            prompt = f"""Analyze this {language} code and provide brief feedback:

```{language}
{code}
```

Provide:
1. Code quality score (1-10)
2. Two strengths
3. Two areas for improvement
4. One performance tip

Keep it concise and actionable. Format as JSON with keys: score, strengths (array), improvements (array), performance_tip"""

            # Call async function synchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ai_response = loop.run_until_complete(
                call_llm_chat("You are a code quality analyzer.", prompt, model="gpt-4o-mini", max_tokens=400)
            )
            loop.close()
            
            import json
            try:
                analysis = json.loads(ai_response)
            except:
                analysis = {
                    "score": 7,
                    "strengths": ["Code is readable", "Basic structure is good"],
                    "improvements": ["Consider edge cases", "Add comments"],
                    "performance_tip": "Look for optimization opportunities"
                }
            
            return analysis
            
        except Exception as e:
            return {
                "score": 0,
                "strengths": [],
                "improvements": [],
                "performance_tip": "Unable to analyze at this time"
            }
