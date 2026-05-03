"""
FastAPI routes for Online IDE
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
import os
from .code_executor import CodeExecutor
from .language_configs import LANGUAGE_CONFIGS, CODING_CHALLENGES

# Setup templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter(prefix="/ide", tags=["IDE"])
executor = CodeExecutor()


class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    input_data: Optional[str] = ""


class CodeAnalysisRequest(BaseModel):
    code: str
    language: str


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def ide_page(request: Request):
    """Serve the IDE HTML page"""
    return templates.TemplateResponse(request=request, name="ide.html")


@router.get("/test", response_class=HTMLResponse)
async def ide_test_page(request: Request):
    """Serve a simple test IDE page"""
    return templates.TemplateResponse(request=request, name="ide_test.html")


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {
                "id": lang_id,
                "name": config["name"],
                "version": config["version"],
                "template": config["template"]
            }
            for lang_id, config in LANGUAGE_CONFIGS.items()
        ]
    }


@router.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    """
    Execute code and return results with AI-powered error analysis
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language not in LANGUAGE_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
    
    result = executor.execute_code(
        code=request.code,
        language=request.language,
        input_data=request.input_data
    )
    
    return result


@router.post("/analyze")
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code quality and provide suggestions
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language not in LANGUAGE_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
    
    analysis = executor.analyze_code_quality(
        code=request.code,
        language=request.language
    )
    
    return analysis


@router.get("/challenges")
async def get_challenges(language: str = "python"):
    """Get coding challenges for specific language"""
    
    # Language-specific challenges
    challenges_by_language = {
        "python": [
            {"id": 1, "title": "Two Sum", "difficulty": "easy", "description": "Find two numbers that add up to a target"},
            {"id": 2, "title": "Reverse String", "difficulty": "easy", "description": "Reverse a given string"},
            {"id": 3, "title": "Palindrome Check", "difficulty": "easy", "description": "Check if a string is a palindrome"},
            {"id": 4, "title": "FizzBuzz", "difficulty": "easy", "description": "Print FizzBuzz sequence"},
            {"id": 5, "title": "List Comprehension", "difficulty": "easy", "description": "Use list comprehension to filter data"},
            {"id": 6, "title": "Dictionary Operations", "difficulty": "medium", "description": "Manipulate Python dictionaries"},
            {"id": 7, "title": "Lambda Functions", "difficulty": "medium", "description": "Use lambda functions effectively"},
            {"id": 8, "title": "Decorators", "difficulty": "medium", "description": "Create and use Python decorators"},
            {"id": 9, "title": "Generators", "difficulty": "hard", "description": "Implement Python generators"},
            {"id": 10, "title": "Context Managers", "difficulty": "hard", "description": "Create custom context managers"}
        ],
        "javascript": [
            {"id": 11, "title": "Array Methods", "difficulty": "easy", "description": "Use map, filter, reduce"},
            {"id": 12, "title": "String Manipulation", "difficulty": "easy", "description": "Reverse and manipulate strings"},
            {"id": 13, "title": "Object Destructuring", "difficulty": "easy", "description": "Use ES6 destructuring"},
            {"id": 14, "title": "Arrow Functions", "difficulty": "easy", "description": "Convert to arrow function syntax"},
            {"id": 15, "title": "Promises", "difficulty": "medium", "description": "Work with JavaScript promises"},
            {"id": 16, "title": "Async/Await", "difficulty": "medium", "description": "Use async/await pattern"},
            {"id": 17, "title": "Closures", "difficulty": "medium", "description": "Understand and use closures"},
            {"id": 18, "title": "Prototypes", "difficulty": "medium", "description": "Work with prototypal inheritance"},
            {"id": 19, "title": "Event Loop", "difficulty": "hard", "description": "Understand the event loop"},
            {"id": 20, "title": "Module Patterns", "difficulty": "hard", "description": "Implement module patterns"}
        ],
        "java": [
            {"id": 21, "title": "Sum of Array", "difficulty": "easy", "description": "Calculate sum of array elements"},
            {"id": 22, "title": "ArrayList Operations", "difficulty": "easy", "description": "Work with ArrayList"},
            {"id": 23, "title": "String Methods", "difficulty": "easy", "description": "Use Java String methods"},
            {"id": 24, "title": "Loops and Arrays", "difficulty": "easy", "description": "Iterate through arrays"},
            {"id": 25, "title": "OOP Basics", "difficulty": "medium", "description": "Create classes and objects"},
            {"id": 26, "title": "Inheritance", "difficulty": "medium", "description": "Implement inheritance"},
            {"id": 27, "title": "Interfaces", "difficulty": "medium", "description": "Work with interfaces"},
            {"id": 28, "title": "Exception Handling", "difficulty": "medium", "description": "Handle exceptions properly"},
            {"id": 29, "title": "Generics", "difficulty": "hard", "description": "Use Java generics"},
            {"id": 30, "title": "Streams API", "difficulty": "hard", "description": "Use Java 8 Streams"}
        ],
        "cpp": [
            {"id": 31, "title": "Sum of Numbers", "difficulty": "easy", "description": "Calculate sum using loops"},
            {"id": 32, "title": "Vectors", "difficulty": "easy", "description": "Work with STL vectors"},
            {"id": 33, "title": "Pointers Basics", "difficulty": "easy", "description": "Understand pointers"},
            {"id": 34, "title": "References", "difficulty": "easy", "description": "Use references"},
            {"id": 35, "title": "Classes and Objects", "difficulty": "medium", "description": "OOP in C++"},
            {"id": 36, "title": "Operator Overloading", "difficulty": "medium", "description": "Overload operators"},
            {"id": 37, "title": "Templates", "difficulty": "medium", "description": "Use C++ templates"},
            {"id": 38, "title": "STL Algorithms", "difficulty": "medium", "description": "Use STL algorithms"},
            {"id": 39, "title": "Smart Pointers", "difficulty": "hard", "description": "Use smart pointers"},
            {"id": 40, "title": "Move Semantics", "difficulty": "hard", "description": "Understand move semantics"}
        ],
        "c": [
            {"id": 41, "title": "Sum Calculator", "difficulty": "easy", "description": "Calculate sum of numbers"},
            {"id": 42, "title": "Arrays", "difficulty": "easy", "description": "Work with arrays"},
            {"id": 43, "title": "Pointers", "difficulty": "easy", "description": "Understand pointers"},
            {"id": 44, "title": "Strings", "difficulty": "easy", "description": "String manipulation in C"},
            {"id": 45, "title": "Structures", "difficulty": "medium", "description": "Use struct"},
            {"id": 46, "title": "File I/O", "difficulty": "medium", "description": "Read and write files"},
            {"id": 47, "title": "Dynamic Memory", "difficulty": "medium", "description": "Use malloc and free"},
            {"id": 48, "title": "Linked Lists", "difficulty": "medium", "description": "Implement linked list"},
            {"id": 49, "title": "Function Pointers", "difficulty": "hard", "description": "Use function pointers"},
            {"id": 50, "title": "Bit Manipulation", "difficulty": "hard", "description": "Manipulate bits"}
        ]
    }
    
    # Get challenges for the specified language
    challenges = challenges_by_language.get(language, challenges_by_language["python"])
    
    return {"challenges": challenges, "language": language}


@router.get("/challenges/{challenge_id}")
async def get_challenge(challenge_id: int):
    """Get specific coding challenge"""
    
    # Comprehensive challenge database with detailed information
    all_challenges = {
        # Python challenges (1-10)
        1: {
            "id": 1, "title": "Two Sum", "difficulty": "easy",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
            "examples": [
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}
            ]
        },
        2: {
            "id": 2, "title": "Reverse String", "difficulty": "easy",
            "description": "Write a function that reverses a string.",
            "examples": [
                {"input": "'hello'", "output": "'olleh'"},
                {"input": "'world'", "output": "'dlrow'"}
            ]
        },
        3: {
            "id": 3, "title": "Palindrome Check", "difficulty": "easy",
            "description": "Check if a given string is a palindrome (reads same forwards and backwards).",
            "examples": [
                {"input": "'racecar'", "output": "True"},
                {"input": "'hello'", "output": "False"}
            ]
        },
        4: {
            "id": 4, "title": "FizzBuzz", "difficulty": "easy",
            "description": "Print numbers 1 to n. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', for both print 'FizzBuzz'.",
            "examples": [
                {"input": "n = 15", "output": "1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz"}
            ]
        },
        5: {
            "id": 5, "title": "List Comprehension", "difficulty": "easy",
            "description": "Use Python list comprehension to filter and transform data efficiently.",
            "examples": [
                {"input": "Filter even numbers from [1,2,3,4,5,6]", "output": "[2, 4, 6]"}
            ]
        },
        6: {
            "id": 6, "title": "Dictionary Operations", "difficulty": "medium",
            "description": "Perform common dictionary operations like merging, filtering, and transforming.",
            "examples": [
                {"input": "Merge two dicts", "output": "Combined dictionary"}
            ]
        },
        7: {
            "id": 7, "title": "Lambda Functions", "difficulty": "medium",
            "description": "Use lambda functions with map, filter, and reduce.",
            "examples": [
                {"input": "Square all numbers in list", "output": "List of squared numbers"}
            ]
        },
        8: {
            "id": 8, "title": "Decorators", "difficulty": "medium",
            "description": "Create and use Python decorators to modify function behavior.",
            "examples": [
                {"input": "Add timing decorator", "output": "Function with execution time"}
            ]
        },
        9: {
            "id": 9, "title": "Generators", "difficulty": "hard",
            "description": "Implement Python generators for memory-efficient iteration.",
            "examples": [
                {"input": "Generate fibonacci sequence", "output": "Lazy fibonacci generator"}
            ]
        },
        10: {
            "id": 10, "title": "Context Managers", "difficulty": "hard",
            "description": "Create custom context managers using __enter__ and __exit__ methods.",
            "examples": [
                {"input": "File handler context manager", "output": "Automatic resource cleanup"}
            ]
        },
        
        # JavaScript challenges (11-20)
        11: {
            "id": 11, "title": "Array Methods", "difficulty": "easy",
            "description": "Master JavaScript array methods: map, filter, reduce, forEach.",
            "examples": [
                {"input": "[1,2,3,4,5]", "output": "Use map to double each number"}
            ]
        },
        12: {
            "id": 12, "title": "String Manipulation", "difficulty": "easy",
            "description": "Reverse and manipulate strings using JavaScript methods.",
            "examples": [
                {"input": "'hello'", "output": "'olleh'"}
            ]
        },
        13: {
            "id": 13, "title": "Object Destructuring", "difficulty": "easy",
            "description": "Use ES6 destructuring to extract values from objects and arrays.",
            "examples": [
                {"input": "const {name, age} = person", "output": "Extracted values"}
            ]
        },
        14: {
            "id": 14, "title": "Arrow Functions", "difficulty": "easy",
            "description": "Convert traditional functions to arrow function syntax.",
            "examples": [
                {"input": "function(x) { return x * 2 }", "output": "x => x * 2"}
            ]
        },
        15: {
            "id": 15, "title": "Promises", "difficulty": "medium",
            "description": "Work with JavaScript promises for asynchronous operations.",
            "examples": [
                {"input": "Fetch data from API", "output": "Promise chain"}
            ]
        },
        16: {
            "id": 16, "title": "Async/Await", "difficulty": "medium",
            "description": "Use async/await pattern for cleaner asynchronous code.",
            "examples": [
                {"input": "async function fetchData()", "output": "Awaited result"}
            ]
        },
        17: {
            "id": 17, "title": "Closures", "difficulty": "medium",
            "description": "Understand and use JavaScript closures for data privacy.",
            "examples": [
                {"input": "Counter function", "output": "Private state"}
            ]
        },
        18: {
            "id": 18, "title": "Prototypes", "difficulty": "medium",
            "description": "Work with prototypal inheritance in JavaScript.",
            "examples": [
                {"input": "Create prototype chain", "output": "Inherited methods"}
            ]
        },
        19: {
            "id": 19, "title": "Event Loop", "difficulty": "hard",
            "description": "Understand the JavaScript event loop and call stack.",
            "examples": [
                {"input": "setTimeout vs Promise", "output": "Execution order"}
            ]
        },
        20: {
            "id": 20, "title": "Module Patterns", "difficulty": "hard",
            "description": "Implement module patterns for code organization.",
            "examples": [
                {"input": "IIFE module", "output": "Encapsulated code"}
            ]
        },
        
        # Java challenges (21-30)
        21: {
            "id": 21, "title": "Sum of Array", "difficulty": "easy",
            "description": "Calculate the sum of all elements in an integer array.",
            "examples": [
                {"input": "int[] arr = {1, 2, 3, 4, 5}", "output": "15"},
                {"input": "int[] arr = {10, 20, 30}", "output": "60"}
            ]
        },
        22: {
            "id": 22, "title": "ArrayList Operations", "difficulty": "easy",
            "description": "Work with Java ArrayList: add, remove, iterate, and search.",
            "examples": [
                {"input": "ArrayList<Integer> list", "output": "Modified list"}
            ]
        },
        23: {
            "id": 23, "title": "String Methods", "difficulty": "easy",
            "description": "Use Java String methods: substring, indexOf, replace, split.",
            "examples": [
                {"input": "String text = \"Hello\"", "output": "Manipulated string"}
            ]
        },
        24: {
            "id": 24, "title": "Loops and Arrays", "difficulty": "easy",
            "description": "Iterate through arrays using for, while, and enhanced for loops.",
            "examples": [
                {"input": "int[] numbers = {1,2,3,4,5}", "output": "Sum of elements"}
            ]
        },
        25: {
            "id": 25, "title": "OOP Basics", "difficulty": "medium",
            "description": "Create classes and objects with fields, constructors, and methods.",
            "examples": [
                {"input": "class Person", "output": "Person object"}
            ]
        },
        26: {
            "id": 26, "title": "Inheritance", "difficulty": "medium",
            "description": "Implement inheritance with extends keyword and method overriding.",
            "examples": [
                {"input": "class Dog extends Animal", "output": "Inherited behavior"}
            ]
        },
        27: {
            "id": 27, "title": "Interfaces", "difficulty": "medium",
            "description": "Work with interfaces to define contracts for classes.",
            "examples": [
                {"input": "interface Drawable", "output": "Implemented interface"}
            ]
        },
        28: {
            "id": 28, "title": "Exception Handling", "difficulty": "medium",
            "description": "Handle exceptions properly using try-catch-finally blocks.",
            "examples": [
                {"input": "try { risky code }", "output": "Handled exception"}
            ]
        },
        29: {
            "id": 29, "title": "Generics", "difficulty": "hard",
            "description": "Use Java generics for type-safe collections and methods.",
            "examples": [
                {"input": "List<T> genericList", "output": "Type-safe operations"}
            ]
        },
        30: {
            "id": 30, "title": "Streams API", "difficulty": "hard",
            "description": "Use Java 8 Streams for functional-style operations on collections.",
            "examples": [
                {"input": "list.stream().filter().map()", "output": "Transformed data"}
            ]
        },
        
        # C++ challenges (31-40)
        31: {
            "id": 31, "title": "Sum of Numbers", "difficulty": "easy",
            "description": "Calculate the sum of N numbers using a loop.",
            "examples": [
                {"input": "n=5, numbers: 1 2 3 4 5", "output": "15"},
                {"input": "n=3, numbers: 10 20 30", "output": "60"}
            ]
        },
        32: {
            "id": 32, "title": "Vectors", "difficulty": "easy",
            "description": "Work with STL vectors: push_back, pop_back, iteration.",
            "examples": [
                {"input": "vector<int> v", "output": "Modified vector"}
            ]
        },
        33: {
            "id": 33, "title": "Pointers Basics", "difficulty": "easy",
            "description": "Understand pointers, dereferencing, and memory addresses.",
            "examples": [
                {"input": "int* ptr = &x", "output": "Pointer operations"}
            ]
        },
        34: {
            "id": 34, "title": "References", "difficulty": "easy",
            "description": "Use references for efficient parameter passing.",
            "examples": [
                {"input": "void swap(int& a, int& b)", "output": "Swapped values"}
            ]
        },
        35: {
            "id": 35, "title": "Classes and Objects", "difficulty": "medium",
            "description": "Create classes with constructors, destructors, and member functions.",
            "examples": [
                {"input": "class Rectangle", "output": "Rectangle object"}
            ]
        },
        36: {
            "id": 36, "title": "Operator Overloading", "difficulty": "medium",
            "description": "Overload operators for custom classes.",
            "examples": [
                {"input": "Complex operator+(Complex)", "output": "Custom addition"}
            ]
        },
        37: {
            "id": 37, "title": "Templates", "difficulty": "medium",
            "description": "Use C++ templates for generic programming.",
            "examples": [
                {"input": "template<typename T>", "output": "Generic function"}
            ]
        },
        38: {
            "id": 38, "title": "STL Algorithms", "difficulty": "medium",
            "description": "Use STL algorithms: sort, find, count, transform.",
            "examples": [
                {"input": "sort(v.begin(), v.end())", "output": "Sorted vector"}
            ]
        },
        39: {
            "id": 39, "title": "Smart Pointers", "difficulty": "hard",
            "description": "Use unique_ptr, shared_ptr for automatic memory management.",
            "examples": [
                {"input": "unique_ptr<int> p", "output": "Safe memory handling"}
            ]
        },
        40: {
            "id": 40, "title": "Move Semantics", "difficulty": "hard",
            "description": "Understand move constructors and rvalue references.",
            "examples": [
                {"input": "std::move(obj)", "output": "Efficient transfer"}
            ]
        },
        
        # C challenges (41-50)
        41: {
            "id": 41, "title": "Sum Calculator", "difficulty": "easy",
            "description": "Calculate the sum of N numbers using scanf and printf.",
            "examples": [
                {"input": "n=5, numbers: 1 2 3 4 5", "output": "Sum = 15"},
                {"input": "n=3, numbers: 10 20 30", "output": "Sum = 60"}
            ]
        },
        42: {
            "id": 42, "title": "Arrays", "difficulty": "easy",
            "description": "Work with C arrays: declaration, initialization, iteration.",
            "examples": [
                {"input": "int arr[5]", "output": "Array operations"}
            ]
        },
        43: {
            "id": 43, "title": "Pointers", "difficulty": "easy",
            "description": "Master C pointers and pointer arithmetic.",
            "examples": [
                {"input": "int *ptr", "output": "Pointer manipulation"}
            ]
        },
        44: {
            "id": 44, "title": "Strings", "difficulty": "easy",
            "description": "String manipulation in C using char arrays and string.h.",
            "examples": [
                {"input": "char str[100]", "output": "String operations"}
            ]
        },
        45: {
            "id": 45, "title": "Structures", "difficulty": "medium",
            "description": "Use struct to create custom data types.",
            "examples": [
                {"input": "struct Person", "output": "Structured data"}
            ]
        },
        46: {
            "id": 46, "title": "File I/O", "difficulty": "medium",
            "description": "Read and write files using fopen, fread, fwrite.",
            "examples": [
                {"input": "FILE *fp", "output": "File operations"}
            ]
        },
        47: {
            "id": 47, "title": "Dynamic Memory", "difficulty": "medium",
            "description": "Use malloc, calloc, realloc, and free for dynamic memory.",
            "examples": [
                {"input": "int *ptr = malloc(size)", "output": "Dynamic allocation"}
            ]
        },
        48: {
            "id": 48, "title": "Linked Lists", "difficulty": "medium",
            "description": "Implement singly linked list with insert, delete, search.",
            "examples": [
                {"input": "struct Node", "output": "Linked list operations"}
            ]
        },
        49: {
            "id": 49, "title": "Function Pointers", "difficulty": "hard",
            "description": "Use function pointers for callbacks and dynamic dispatch.",
            "examples": [
                {"input": "int (*func_ptr)(int)", "output": "Function pointer call"}
            ]
        },
        50: {
            "id": 50, "title": "Bit Manipulation", "difficulty": "hard",
            "description": "Manipulate bits using bitwise operators.",
            "examples": [
                {"input": "x & (1 << n)", "output": "Bit operations"}
            ]
        }
    }
    
    challenge = all_challenges.get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge


@router.get("/template/{language}")
async def get_template(language: str):
    """Get code template for a language"""
    if language not in LANGUAGE_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    
    return {
        "language": language,
        "template": LANGUAGE_CONFIGS[language]["template"]
    }
