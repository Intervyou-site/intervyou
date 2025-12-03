# 🔌 AI-Powered IDE - API Examples

## Complete API Reference with Examples

### 1. Get Supported Languages

**Endpoint**: `GET /ide/languages`

**Request**:
```bash
curl http://localhost:8000/ide/languages
```

**Response**:
```json
{
  "languages": [
    {
      "id": "python",
      "name": "Python",
      "version": "3.11",
      "template": "# Write your Python code here\ndef solution():\n    # Your code here\n    pass\n\nif __name__ == \"__main__\":\n    solution()\n"
    },
    {
      "id": "javascript",
      "name": "JavaScript",
      "version": "Node 20",
      "template": "// Write your JavaScript code here\nfunction solution() {\n    // Your code here\n}\n\nsolution();\n"
    }
  ]
}
```

---

### 2. Execute Code (Success)

**Endpoint**: `POST /ide/execute`

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello, World!\")\nfor i in range(5):\n    print(f\"Count: {i}\")",
    "language": "python",
    "input_data": ""
  }'
```

**Response**:
```json
{
  "success": true,
  "output": "Hello, World!\nCount: 0\nCount: 1\nCount: 2\nCount: 3\nCount: 4\n",
  "error": "",
  "execution_time": 0.234
}
```

---

### 3. Execute Code (Error with AI Explanation)

**Endpoint**: `POST /ide/execute`

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def greet()\n    print(\"Hello\")",
    "language": "python",
    "input_data": ""
  }'
```

**Response**:
```json
{
  "success": false,
  "output": "",
  "error": "  File \"/tmp/code_1234567890.py\", line 1\n    def greet()\n               ^\nSyntaxError: invalid syntax\n",
  "execution_time": 0.045,
  "ai_explanation": {
    "quick_hint": "There's a syntax mistake in your code. Check for missing colons, parentheses, or quotes.",
    "detailed_analysis": {
      "explanation": "You're missing a colon (:) at the end of your function definition. In Python, function definitions must end with a colon before the indented code block that follows.",
      "problem_location": "Line 1: 'def greet()' is missing a colon at the end",
      "fix": "Change 'def greet()' to 'def greet():' - add a colon after the closing parenthesis",
      "tip": "In Python, all function definitions, class definitions, if statements, loops, and other compound statements require a colon at the end of the header line."
    }
  }
}
```

---

### 4. Execute Code with Input

**Endpoint**: `POST /ide/execute`

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "name = input(\"Enter your name: \")\nprint(f\"Hello, {name}!\")",
    "language": "python",
    "input_data": "Alice"
  }'
```

**Response**:
```json
{
  "success": true,
  "output": "Enter your name: Hello, Alice!\n",
  "error": "",
  "execution_time": 0.156
}
```

---

### 5. Execute JavaScript Code

**Endpoint**: `POST /ide/execute`

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n-1) + fibonacci(n-2);\n}\n\nconsole.log(fibonacci(10));",
    "language": "javascript",
    "input_data": ""
  }'
```

**Response**:
```json
{
  "success": true,
  "output": "55\n",
  "error": "",
  "execution_time": 0.312
}
```

---

### 6. Execute Java Code

**Endpoint**: `POST /ide/execute`

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello from Java!\");\n    }\n}",
    "language": "java",
    "input_data": ""
  }'
```

**Response**:
```json
{
  "success": true,
  "output": "Hello from Java!\n",
  "error": "",
  "execution_time": 1.234
}
```

---

### 7. Analyze Code Quality

**Endpoint**: `POST /ide/analyze`

**Request**:
```bash
curl -X POST http://localhost:8000/ide/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def calculate_sum(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total\n\nresult = calculate_sum([1, 2, 3, 4, 5])\nprint(result)",
    "language": "python"
  }'
```

**Response**:
```json
{
  "score": 8,
  "strengths": [
    "Code is clear and readable with good variable names",
    "Function follows single responsibility principle"
  ],
  "improvements": [
    "Consider adding a docstring to explain the function's purpose",
    "Could use Python's built-in sum() function for better performance"
  ],
  "performance_tip": "For large lists, consider using sum(numbers) which is implemented in C and runs faster than a Python loop"
}
```

---

### 8. Get All Challenges

**Endpoint**: `GET /ide/challenges`

**Request**:
```bash
curl http://localhost:8000/ide/challenges
```

**Response**:
```json
{
  "challenges": [
    {
      "id": 1,
      "title": "Two Sum",
      "difficulty": "Easy",
      "description": "Given an array of integers and a target, return indices of two numbers that add up to target.",
      "examples": [
        {
          "input": "[2,7,11,15], target=9",
          "output": "[0,1]"
        },
        {
          "input": "[3,2,4], target=6",
          "output": "[1,2]"
        }
      ],
      "test_cases": [
        {
          "input": "[2,7,11,15]\n9",
          "expected_output": "[0, 1]"
        }
      ]
    },
    {
      "id": 2,
      "title": "Reverse String",
      "difficulty": "Easy",
      "description": "Write a function that reverses a string.",
      "examples": [
        {
          "input": "hello",
          "output": "olleh"
        }
      ],
      "test_cases": [
        {
          "input": "hello",
          "expected_output": "olleh"
        }
      ]
    }
  ]
}
```

---

### 9. Get Specific Challenge

**Endpoint**: `GET /ide/challenges/{challenge_id}`

**Request**:
```bash
curl http://localhost:8000/ide/challenges/1
```

**Response**:
```json
{
  "id": 1,
  "title": "Two Sum",
  "difficulty": "Easy",
  "description": "Given an array of integers and a target, return indices of two numbers that add up to target.",
  "examples": [
    {
      "input": "[2,7,11,15], target=9",
      "output": "[0,1]"
    },
    {
      "input": "[3,2,4], target=6",
      "output": "[1,2]"
    }
  ],
  "test_cases": [
    {
      "input": "[2,7,11,15]\n9",
      "expected_output": "[0, 1]"
    },
    {
      "input": "[3,2,4]\n6",
      "expected_output": "[1, 2]"
    },
    {
      "input": "[3,3]\n6",
      "expected_output": "[0, 1]"
    }
  ]
}
```

---

### 10. Get Language Template

**Endpoint**: `GET /ide/template/{language}`

**Request**:
```bash
curl http://localhost:8000/ide/template/python
```

**Response**:
```json
{
  "language": "python",
  "template": "# Write your Python code here\ndef solution():\n    # Your code here\n    pass\n\nif __name__ == \"__main__\":\n    solution()\n"
}
```

---

## Error Responses

### 400 Bad Request - Empty Code

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "",
    "language": "python"
  }'
```

**Response**:
```json
{
  "detail": "Code cannot be empty"
}
```

---

### 400 Bad Request - Unsupported Language

**Request**:
```bash
curl -X POST http://localhost:8000/ide/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"test\")",
    "language": "ruby"
  }'
```

**Response**:
```json
{
  "detail": "Unsupported language: ruby"
}
```

---

### 404 Not Found - Challenge Not Found

**Request**:
```bash
curl http://localhost:8000/ide/challenges/999
```

**Response**:
```json
{
  "detail": "Challenge not found"
}
```

---

## Advanced Examples

### Example 1: Runtime Error with AI Help

**Request**:
```json
{
  "code": "x = 10\ny = 0\nresult = x / y",
  "language": "python",
  "input_data": ""
}
```

**Response**:
```json
{
  "success": false,
  "output": "",
  "error": "Traceback (most recent call last):\n  File \"/tmp/code.py\", line 3, in <module>\n    result = x / y\nZeroDivisionError: division by zero\n",
  "execution_time": 0.089,
  "ai_explanation": {
    "quick_hint": "You're performing an invalid operation on a value.",
    "detailed_analysis": {
      "explanation": "You're trying to divide by zero, which is mathematically undefined. Python raises a ZeroDivisionError when this happens.",
      "problem_location": "Line 3: 'result = x / y' where y is 0",
      "fix": "Check if y is not zero before dividing: 'if y != 0: result = x / y else: print(\"Cannot divide by zero\")'",
      "tip": "Always validate your inputs before performing operations that could fail. Division by zero is a common edge case to check for."
    }
  }
}
```

---

### Example 2: Timeout Error

**Request**:
```json
{
  "code": "while True:\n    pass",
  "language": "python",
  "input_data": ""
}
```

**Response**:
```json
{
  "success": false,
  "output": "",
  "error": "Execution timed out (limit: 10s)",
  "execution_time": 10.0,
  "ai_explanation": {
    "quick_hint": "Your code took too long to execute.",
    "detailed_analysis": {
      "explanation": "Your code has an infinite loop that never terminates. The execution was stopped after 10 seconds to prevent resource exhaustion.",
      "problem_location": "Line 1-2: 'while True: pass' creates an infinite loop",
      "fix": "Add a condition to break out of the loop, or use a for loop with a specific number of iterations",
      "tip": "Always ensure your loops have a termination condition. Use break statements or counter variables to exit loops."
    }
  }
}
```

---

### Example 3: Complex Code Analysis

**Request**:
```json
{
  "code": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)\n\nprint(quicksort([3,6,8,10,1,2,1]))",
  "language": "python"
}
```

**Response**:
```json
{
  "score": 9,
  "strengths": [
    "Excellent implementation of quicksort algorithm with clear logic",
    "Good use of list comprehensions for readability",
    "Proper base case handling for recursion"
  ],
  "improvements": [
    "Consider adding type hints for better code documentation",
    "Could add docstring explaining the algorithm and parameters"
  ],
  "performance_tip": "This implementation creates new lists which uses O(n) extra space. For better memory efficiency, consider an in-place quicksort implementation, though this version is more readable for learning purposes."
}
```

---

## JavaScript Examples

### Example 1: Async/Await Code

**Request**:
```json
{
  "code": "async function fetchData() {\n    return new Promise(resolve => {\n        setTimeout(() => resolve('Data loaded'), 1000);\n    });\n}\n\nfetchData().then(data => console.log(data));",
  "language": "javascript",
  "input_data": ""
}
```

**Response**:
```json
{
  "success": true,
  "output": "Data loaded\n",
  "error": "",
  "execution_time": 1.234
}
```

---

### Example 2: JavaScript Error

**Request**:
```json
{
  "code": "const arr = [1, 2, 3];\nconsole.log(arr[10].toString());",
  "language": "javascript",
  "input_data": ""
}
```

**Response**:
```json
{
  "success": false,
  "output": "",
  "error": "TypeError: Cannot read property 'toString' of undefined\n",
  "execution_time": 0.123,
  "ai_explanation": {
    "quick_hint": "You're performing an invalid operation on a value.",
    "detailed_analysis": {
      "explanation": "You're trying to access an array element at index 10, but the array only has 3 elements (indices 0-2). This returns undefined, and you can't call toString() on undefined.",
      "problem_location": "Line 2: 'arr[10]' returns undefined because the index is out of bounds",
      "fix": "Check if the index exists before accessing: 'if (arr[10]) console.log(arr[10].toString())' or use optional chaining: 'arr[10]?.toString()'",
      "tip": "Always validate array indices before accessing them. JavaScript returns undefined for out-of-bounds access instead of throwing an error like some other languages."
    }
  }
}
```

---

## Python Testing Examples

### Example: Unit Test Code

**Request**:
```json
{
  "code": "def add(a, b):\n    return a + b\n\n# Test cases\nassert add(2, 3) == 5\nassert add(-1, 1) == 0\nassert add(0, 0) == 0\nprint('All tests passed!')",
  "language": "python",
  "input_data": ""
}
```

**Response**:
```json
{
  "success": true,
  "output": "All tests passed!\n",
  "error": "",
  "execution_time": 0.098
}
```

---

## Usage in Frontend

### JavaScript Fetch Example

```javascript
// Execute code
async function runCode(code, language, inputData = '') {
  const response = await fetch('/ide/execute', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: code,
      language: language,
      input_data: inputData
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log('Output:', result.output);
  } else {
    console.error('Error:', result.error);
    if (result.ai_explanation) {
      console.log('AI Help:', result.ai_explanation);
    }
  }
  
  return result;
}

// Analyze code
async function analyzeCode(code, language) {
  const response = await fetch('/ide/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: code,
      language: language
    })
  });
  
  const analysis = await response.json();
  console.log('Score:', analysis.score);
  console.log('Strengths:', analysis.strengths);
  console.log('Improvements:', analysis.improvements);
  
  return analysis;
}
```

---

## Rate Limiting (Future)

When rate limiting is implemented:

**Response** (429 Too Many Requests):
```json
{
  "detail": "Rate limit exceeded. Please wait 60 seconds before trying again.",
  "retry_after": 60
}
```

---

## Summary

The IDE API provides:
- ✅ Multi-language code execution
- ✅ AI-powered error explanations
- ✅ Code quality analysis
- ✅ Built-in coding challenges
- ✅ Language templates
- ✅ Comprehensive error handling

All responses are JSON-formatted and include detailed information to help users learn and improve their coding skills.
