# 🎓 AI-Powered Online IDE - Complete Guide

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [What Makes It Unique](#what-makes-it-unique)
3. [Features Overview](#features-overview)
4. [Installation & Setup](#installation--setup)
5. [User Guide](#user-guide)
6. [API Reference](#api-reference)
7. [Architecture](#architecture)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Quick Start

### 1. Test Installation
```bash
python test_ide.py
```

### 2. Start Server
```bash
python start.py
```

### 3. Access IDE
```
http://localhost:8000/ide
```

### 4. Try It Out
```python
# Write this in the editor
print("Hello from AI IDE!")

# Click "Run Code" or press Ctrl+Enter
```

---

## What Makes It Unique

### The Problem with Traditional IDEs
```
❌ Cryptic error messages
❌ No guidance on how to fix
❌ Intimidating for beginners
❌ No learning support
```

### Our AI-Powered Solution
```
✅ Beginner-friendly explanations
✅ Specific fix suggestions
✅ Educational tips
✅ Encourages learning
```

### Example Comparison

**Traditional IDE:**
```
SyntaxError: invalid syntax
```

**Our AI IDE:**
```
🤖 AI Help

💡 Quick Hint:
There's a syntax mistake in your code. Check for missing 
colons, parentheses, or quotes.

📍 What Went Wrong:
You're missing a colon (:) at the end of your function 
definition. In Python, function definitions must end with 
a colon before the indented code block.

🔍 Problem Location:
Line 1: def hello() <- missing colon here

🔧 How to Fix:
Change "def hello()" to "def hello():"

🎓 Pro Tip:
Function definitions, if statements, loops, and class 
definitions all require a colon at the end in Python.
```

---

## Features Overview

### 1. Multi-Language Support
- **Python 3.11**: Full support with pip packages
- **JavaScript (Node 20)**: Modern ES6+ features
- **Java 17**: Latest LTS version
- **C++ (g++ 11)**: Modern C++ standards
- **C (gcc 11)**: ANSI C and GNU extensions

### 2. AI-Powered Features

#### Error Explanations
- Automatic error detection
- Beginner-friendly language
- Specific problem identification
- Concrete fix suggestions
- Educational tips

#### Code Quality Analysis
- Quality scoring (1-10)
- Strength identification
- Improvement suggestions
- Performance tips
- Best practices guidance

### 3. Built-in Challenges
- **Two Sum**: Array manipulation
- **Reverse String**: String operations
- **Palindrome Check**: Logic and conditions
- **FizzBuzz**: Loops and conditionals
- **Find Maximum**: Array traversal

### 4. Safety & Security
- Docker containerization
- Network isolation
- Memory limits (128-256MB)
- Time limits (10-15 seconds)
- Input validation

### 5. User Experience
- Monaco Editor (VS Code engine)
- Syntax highlighting
- Auto-completion
- Dark theme
- Keyboard shortcuts
- Responsive design

---

## Installation & Setup

### Prerequisites

#### Required:
```bash
# Python 3.11+
python --version

# FastAPI (already installed)
pip list | grep fastapi
```

#### Recommended:
```bash
# Docker Desktop
docker --version

# Should see: Docker version 20.x or higher
```

#### Optional:
```bash
# Node.js (for JavaScript)
node --version

# Java (for Java)
java --version

# GCC (for C/C++)
gcc --version
```

### Environment Setup

1. **API Keys** (in `.env`):
```env
# Option 1: OpenAI
OPENAI_API_KEY=sk-...

# Option 2: Groq (faster, free tier)
GROQ_API_KEY=gsk_...
```

2. **Docker Images** (optional):
```bash
docker pull python:3.11-slim
docker pull node:20-slim
docker pull openjdk:17-slim
docker pull gcc:11
```

### Verification

Run the test suite:
```bash
python test_ide.py
```

Expected output:
```
✅ Configuration tests complete!
✅ Docker check complete!
✅ LLM check complete!
✅ Basic execution tests complete!
✅ Code analysis test complete!
```

---

## User Guide

### Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  Header: AI Code Editor                    [Home] [👤]  │
├──────────┬──────────────────────────┬───────────────────┤
│          │                          │                   │
│ Sidebar  │    Code Editor           │  Output Panel     │
│          │    (Monaco)              │                   │
│ - Lang   │                          │  Tabs:            │
│ - Chall  │                          │  - Output         │
│ - Stats  │                          │  - AI Help        │
│          │                          │  - Analysis       │
│          ├──────────────────────────┤                   │
│          │  Input (stdin)           │                   │
└──────────┴──────────────────────────┴───────────────────┘
```

### Basic Workflow

1. **Select Language**
   - Choose from dropdown in sidebar
   - Editor updates syntax highlighting

2. **Write Code**
   - Type in Monaco Editor
   - Use auto-completion (Ctrl+Space)
   - Syntax highlighting helps

3. **Add Input** (optional)
   - Enter stdin data in input box
   - One value per line

4. **Run Code**
   - Click "Run Code" button
   - Or press `Ctrl+Enter`
   - View output in Output tab

5. **Handle Errors**
   - If error occurs, check AI Help tab
   - Read explanation
   - Apply suggested fix
   - Run again

6. **Analyze Quality**
   - Click "Analyze Quality"
   - Or press `Ctrl+Shift+A`
   - View score and tips in Analysis tab

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Run code |
| `Ctrl+Shift+A` | Analyze code |
| `Ctrl+S` | Save (browser default) |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `Ctrl+/` | Toggle comment |

### Using Challenges

1. **Browse Challenges**
   - View list in sidebar
   - Color-coded by difficulty:
     - 🟢 Green = Easy
     - 🟡 Yellow = Medium
     - 🔴 Red = Hard

2. **Load Challenge**
   - Click challenge name
   - Description loads in editor
   - Template code provided

3. **Solve Challenge**
   - Write solution below template
   - Test with provided examples
   - Run to verify

4. **Submit** (future feature)
   - Automatic test case validation
   - Score tracking
   - Leaderboard integration

---

## API Reference

### Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ide` | Render IDE page |
| GET | `/ide/languages` | List languages |
| POST | `/ide/execute` | Execute code |
| POST | `/ide/analyze` | Analyze code |
| GET | `/ide/challenges` | List challenges |
| GET | `/ide/challenges/{id}` | Get challenge |
| GET | `/ide/template/{lang}` | Get template |

### Execute Code

**Request:**
```json
POST /ide/execute
{
  "code": "print('Hello')",
  "language": "python",
  "input_data": ""
}
```

**Success Response:**
```json
{
  "success": true,
  "output": "Hello\n",
  "error": "",
  "execution_time": 0.123
}
```

**Error Response:**
```json
{
  "success": false,
  "output": "",
  "error": "SyntaxError: ...",
  "execution_time": 0.045,
  "ai_explanation": {
    "quick_hint": "...",
    "detailed_analysis": {
      "explanation": "...",
      "problem_location": "...",
      "fix": "...",
      "tip": "..."
    }
  }
}
```

### Analyze Code

**Request:**
```json
POST /ide/analyze
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python"
}
```

**Response:**
```json
{
  "score": 8,
  "strengths": ["Clear function name", "Simple logic"],
  "improvements": ["Add docstring", "Add type hints"],
  "performance_tip": "Function is efficient"
}
```

---

## Architecture

### System Components

```
User Browser
    ↓
Monaco Editor (Frontend)
    ↓
FastAPI Backend
    ↓
Code Executor
    ↓
Docker/Local Execution
    ↓
LLM (AI Analysis)
```

### Execution Flow

```
1. User writes code
2. Frontend sends to backend
3. Backend creates temp file
4. Executes in Docker/locally
5. Captures output/errors
6. If error: AI analyzes
7. Returns results
8. Frontend displays
```

### Security Layers

```
Layer 1: Input Validation
Layer 2: Docker Isolation
Layer 3: Resource Limits
Layer 4: Output Sanitization
```

---

## Customization

### Adding New Languages

Edit `online_ide/language_configs.py`:

```python
LANGUAGE_CONFIGS["go"] = {
    "name": "Go",
    "version": "1.21",
    "extension": ".go",
    "docker_image": "golang:1.21-alpine",
    "compile_cmd": "go build -o program {file}",
    "run_cmd": "./program",
    "timeout": 10,
    "memory_limit": "128m",
    "template": '''package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
''',
    "common_errors": {
        "undefined": "Variable or function not declared",
        "syntax error": "Check your Go syntax"
    }
}
```

### Adding Challenges

Edit `online_ide/language_configs.py`:

```python
CODING_CHALLENGES.append({
    "id": 6,
    "title": "Binary Search",
    "difficulty": "Medium",
    "description": "Implement binary search algorithm",
    "examples": [
        {"input": "[1,2,3,4,5], target=3", "output": "2"}
    ],
    "test_cases": [
        {"input": "[1,2,3,4,5]\n3", "expected_output": "2"}
    ]
})
```

### Customizing Timeouts

Edit `online_ide/language_configs.py`:

```python
# Increase timeout for complex operations
LANGUAGE_CONFIGS["python"]["timeout"] = 30  # 30 seconds
```

### Customizing Memory Limits

```python
# Increase memory for data-intensive tasks
LANGUAGE_CONFIGS["python"]["memory_limit"] = "512m"  # 512 MB
```

---

## Troubleshooting

### Common Issues

#### 1. Docker Not Found
**Symptom**: "Docker not available" message

**Solution**:
- Install Docker Desktop
- Or: IDE will use local execution (automatic)

#### 2. LLM Not Responding
**Symptom**: No AI explanations

**Solution**:
```bash
# Check API key in .env
cat .env | grep API_KEY

# Verify llm_utils.py works
python -c "from llm_utils import call_llm_chat; print('OK')"
```

#### 3. Execution Timeout
**Symptom**: "Execution timed out" error

**Solution**:
- Check for infinite loops
- Optimize algorithm
- Increase timeout (see Customization)

#### 4. Monaco Editor Not Loading
**Symptom**: Blank editor area

**Solution**:
- Check internet connection (Monaco loads from CDN)
- Check browser console for errors
- Try different browser

#### 5. Language Not Working
**Symptom**: "Execution failed" for specific language

**Solution**:
```bash
# Check if compiler installed
python --version  # Python
node --version    # JavaScript
java --version    # Java
gcc --version     # C/C++

# Or pull Docker image
docker pull python:3.11-slim
```

### Debug Mode

Enable detailed logging:

```python
# In code_executor.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

If execution is slow:

1. **Use Docker**: Faster than local for most cases
2. **Pre-pull images**: `docker pull` all images
3. **Use Groq**: Faster than OpenAI for AI analysis
4. **Cache results**: Implement caching for common errors

---

## Best Practices

### For Users

1. **Start Simple**: Test with "Hello World" first
2. **Read Errors**: AI explanations are educational
3. **Use Challenges**: Great for learning
4. **Analyze Code**: Learn best practices
5. **Save Work**: Copy code before closing

### For Developers

1. **Security First**: Always use Docker in production
2. **Rate Limiting**: Implement to prevent abuse
3. **Caching**: Cache common error explanations
4. **Monitoring**: Track execution times and errors
5. **Backups**: Regular database backups

### For Administrators

1. **Resource Limits**: Monitor CPU/memory usage
2. **API Costs**: Track LLM API usage
3. **User Limits**: Set per-user execution limits
4. **Logging**: Keep execution logs for debugging
5. **Updates**: Keep Docker images updated

---

## Advanced Topics

### Integrating with Mock Interviews

```python
# In fastapi_app.py
@app.get("/mock_interview_with_coding")
def mock_interview_coding(request: Request):
    # Load coding challenge
    # User solves in IDE
    # Track time and quality
    # Include in interview score
    pass
```

### Saving Code Submissions

```python
# Add to database models
class CodeSubmission(Base):
    __tablename__ = "code_submission"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    code = Column(Text)
    language = Column(String(50))
    score = Column(Float)
    timestamp = Column(DateTime)
```

### Collaborative Coding

```python
# Use WebSockets for real-time collaboration
@app.websocket("/ide/collaborate/{room_id}")
async def collaborate(websocket: WebSocket, room_id: str):
    # Share code edits in real-time
    # Multiple users in same room
    pass
```

---

## Performance Metrics

### Typical Response Times

| Operation | Time | Notes |
|-----------|------|-------|
| Load IDE | <1s | Monaco from CDN |
| Execute Python | 0.1-2s | Depends on code |
| Execute Java | 1-3s | Compilation overhead |
| AI Explanation | 1-3s | LLM response time |
| Code Analysis | 1-3s | LLM response time |

### Resource Usage

| Resource | Usage | Limit |
|----------|-------|-------|
| Memory per execution | 50-200MB | 256MB max |
| CPU per execution | 10-50% | 1 core |
| Disk per execution | <1MB | Temp files |
| Network | 0 (Docker) | Isolated |

---

## Future Enhancements

### Planned Features

- [ ] Code saving to user profile
- [ ] Execution history
- [ ] Code sharing (public links)
- [ ] Collaborative editing
- [ ] More languages (Go, Rust, PHP)
- [ ] Custom test cases
- [ ] Syntax error highlighting
- [ ] Auto-save functionality
- [ ] Code templates library
- [ ] Integration with mock interviews
- [ ] Performance profiling
- [ ] Memory usage visualization
- [ ] Step-by-step debugging
- [ ] Code comparison tool
- [ ] Plagiarism detection

### Community Contributions

Want to contribute?

1. Add new languages
2. Create more challenges
3. Improve AI prompts
4. Enhance UI/UX
5. Write documentation
6. Report bugs
7. Suggest features

---

## Conclusion

You now have a **complete, production-ready AI-powered online IDE** that:

✅ Helps users learn from mistakes
✅ Provides intelligent code analysis
✅ Supports multiple languages
✅ Executes code safely
✅ Integrates with your platform

**This feature sets your interview platform apart!**

The AI-powered error explanations make coding less frustrating and more educational, perfect for interview preparation and learning.

---

## Quick Reference

### Essential Commands
```bash
# Test
python test_ide.py

# Start
python start.py

# Access
http://localhost:8000/ide
```

### Essential Shortcuts
- `Ctrl+Enter`: Run code
- `Ctrl+Shift+A`: Analyze code

### Essential Files
- `online_ide/code_executor.py`: Core logic
- `online_ide/language_configs.py`: Languages & challenges
- `templates/ide.html`: UI
- `static/ide.js`: Frontend logic

### Essential Docs
- `IDE_QUICK_START.md`: Quick setup
- `IDE_FEATURE.md`: Complete features
- `IDE_API_EXAMPLES.md`: API reference
- `IDE_ARCHITECTURE.md`: System design

---

**Built with ❤️ for InterVyou - Happy Coding! 🚀**
