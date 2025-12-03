# 🚀 Quick Setup Guide - AI-Powered IDE

## Installation Steps

### 1. Files Already Created ✅
```
online_ide/
├── __init__.py
├── code_executor.py
├── language_configs.py
└── ide_routes.py

templates/ide.html
static/ide.js
static/ide.css
```

### 2. Integration Complete ✅
- Routes added to `fastapi_app.py`
- Navigation link added to `templates/index.html`
- Uses existing LLM setup (no new API keys needed!)

### 3. Optional: Install Docker (Recommended)

**Windows:**
```powershell
# Download Docker Desktop from docker.com
# Or use winget:
winget install Docker.DockerDesktop
```

**After Docker is installed:**
```powershell
# Pull language images
docker pull python:3.11-slim
docker pull node:20-slim
docker pull openjdk:17-slim
docker pull gcc:11
```

### 4. Test the IDE

1. **Start your server:**
```powershell
python start.py
```

2. **Navigate to:**
```
http://localhost:8000/ide
```

3. **Try a simple Python program:**
```python
print("Hello from AI IDE!")
```

4. **Try an error to see AI explanation:**
```python
def hello()
print("missing colon!")
```

## 🎯 What Makes This IDE Unique?

### Traditional IDE Error:
```
SyntaxError: invalid syntax
```

### Our AI-Powered IDE:
```
🤖 AI Help:

💡 Quick Hint:
There's a syntax mistake in your code. Check for missing colons, 
parentheses, or quotes.

📍 What Went Wrong:
You're missing a colon (:) at the end of your function definition. 
In Python, function definitions must end with a colon before the 
indented code block.

🔍 Problem Location:
Line 1: def hello() <- missing colon here

🔧 How to Fix:
Change "def hello()" to "def hello():"

🎓 Pro Tip:
Function definitions, if statements, loops, and class definitions 
all require a colon at the end in Python.
```

## 🔑 API Keys

**Good news!** The IDE uses your existing LLM configuration from `llm_utils.py`.

Make sure you have ONE of these in your `.env`:
```env
# Option 1: OpenAI
OPENAI_API_KEY=sk-...

# Option 2: Groq (faster, free tier)
GROQ_API_KEY=gsk_...

# Option 3: Other LLM provider you've configured
```

## 🐳 Docker vs Local Execution

### With Docker (Recommended):
✅ Better security (isolated containers)
✅ Consistent environment
✅ No network access for user code
✅ Easy cleanup

### Without Docker (Fallback):
✅ Still works!
✅ Uses system Python/Node/Java/GCC
⚠️ Less isolated
⚠️ Requires compilers installed locally

**The IDE automatically detects Docker and falls back if unavailable.**

## 🧪 Testing

### Test 1: Basic Execution
```python
# Python
for i in range(5):
    print(f"Count: {i}")
```

### Test 2: Error Handling
```python
# Python with error
x = 10
y = 0
result = x / y  # Division by zero
```

### Test 3: Code Analysis
```python
# Python - click "Analyze Quality"
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(calculate_sum([1, 2, 3, 4, 5]))
```

### Test 4: JavaScript
```javascript
// JavaScript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

console.log(fibonacci(10));
```

### Test 5: Challenges
1. Click on a challenge in the sidebar
2. Write your solution
3. Run and test

## 🎨 Features to Try

1. **Language Switching**: Change language in dropdown
2. **Input Data**: Add stdin input in the input box
3. **Keyboard Shortcuts**: 
   - `Ctrl+Enter` to run
   - `Ctrl+Shift+A` to analyze
4. **Challenges**: Click challenges in sidebar
5. **Templates**: Click "Load Template" for starter code

## 📊 Monitoring

Check your terminal for:
```
✅ Hugging Face utilities loaded successfully
✅ Application startup complete - caches initialized
```

When users run code:
```
Executing Python code...
Using Docker: True/False
Execution time: 0.123s
```

## 🔧 Troubleshooting

### Issue: "Docker not found"
**Solution:** IDE will use local execution automatically. Install Docker for better security.

### Issue: "LLM not responding"
**Solution:** Check your API keys in `.env` and verify `llm_utils.py` works.

### Issue: "Execution timeout"
**Solution:** Code took too long. Check for infinite loops or optimize algorithm.

### Issue: "Monaco Editor not loading"
**Solution:** Check internet connection (Monaco loads from CDN).

## 🚀 Next Steps

1. **Test all languages** to ensure compilers are available
2. **Add more challenges** in `language_configs.py`
3. **Customize error hints** for common mistakes
4. **Monitor usage** and adjust timeouts/limits
5. **Consider adding**:
   - Code saving to user profile
   - Sharing functionality
   - More languages
   - Custom test cases

## 📈 Performance Tips

### For Better Speed:
1. Keep Docker images pulled locally
2. Use Groq API (faster than OpenAI)
3. Cache common error explanations
4. Adjust timeout limits based on usage

### For Better Security:
1. Always use Docker in production
2. Set strict memory limits
3. Disable network in containers
4. Validate all user input

## 🎓 Educational Use

Perfect for:
- Interview preparation
- Learning to code
- Debugging practice
- Algorithm challenges
- Code review training

## 📞 Support

If you encounter issues:
1. Check Docker status: `docker --version`
2. Check Python: `python --version`
3. Check API keys in `.env`
4. Review logs in terminal
5. Test with simple "Hello World" first

---

**Your AI-powered coding assistant is ready!** 🎉

Start coding at: `http://localhost:8000/ide`
