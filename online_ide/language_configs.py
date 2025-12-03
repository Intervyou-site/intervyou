"""
Language configurations for the online IDE
"""

LANGUAGE_CONFIGS = {
    "python": {
        "name": "Python",
        "version": "3.11",
        "extension": ".py",
        "docker_image": "python:3.11-slim",
        "compile_cmd": None,
        "run_cmd": "python {file}",
        "timeout": 10,
        "memory_limit": "128m",
        "template": '''# Write your Python code here
def solution():
    # Your code here
    pass

if __name__ == "__main__":
    solution()
''',
        "common_errors": {
            "IndentationError": "Python uses indentation to define code blocks. Make sure your code is properly indented.",
            "NameError": "You're trying to use a variable that hasn't been defined yet.",
            "SyntaxError": "There's a syntax mistake in your code. Check for missing colons, parentheses, or quotes.",
            "TypeError": "You're using an operation on incompatible data types.",
            "IndexError": "You're trying to access an index that doesn't exist in your list.",
        }
    },
    "javascript": {
        "name": "JavaScript",
        "version": "Node 20",
        "extension": ".js",
        "docker_image": "node:20-slim",
        "compile_cmd": None,
        "run_cmd": "node {file}",
        "timeout": 10,
        "memory_limit": "128m",
        "template": '''// Write your JavaScript code here
function solution() {
    // Your code here
}

solution();
''',
        "common_errors": {
            "ReferenceError": "You're trying to use a variable that hasn't been declared.",
            "TypeError": "You're performing an invalid operation on a value.",
            "SyntaxError": "There's a syntax error in your code. Check for missing brackets or semicolons.",
        }
    },
    "java": {
        "name": "Java",
        "version": "17",
        "extension": ".java",
        "docker_image": "eclipse-temurin:17-jdk-alpine",
        "compile_cmd": "javac {file}",
        "run_cmd": "java Main",
        "timeout": 15,
        "memory_limit": "256m",
        "template": '''public class Main {
    public static void main(String[] args) {
        // Write your Java code here
        solution();
    }
    
    public static void solution() {
        // Your code here
    }
}
''',
        "common_errors": {
            "cannot find symbol": "You're using a variable or method that hasn't been declared.",
            "class, interface, or enum expected": "Check your class structure and curly braces.",
            "';' expected": "You're missing a semicolon at the end of a statement.",
        }
    },
    "cpp": {
        "name": "C++",
        "version": "g++ 11",
        "extension": ".cpp",
        "docker_image": "gcc:11",
        "compile_cmd": "g++ -o program {file}",
        "run_cmd": "./program",
        "timeout": 15,
        "memory_limit": "256m",
        "template": '''#include <iostream>
using namespace std;

int main() {
    // Write your C++ code here
    
    return 0;
}
''',
        "common_errors": {
            "expected ';'": "You're missing a semicolon at the end of a statement.",
            "was not declared": "You're using a variable that hasn't been declared.",
            "undefined reference": "You're calling a function that doesn't exist or isn't linked.",
        }
    },
    "c": {
        "name": "C",
        "version": "gcc 11",
        "extension": ".c",
        "docker_image": "gcc:11",
        "compile_cmd": "gcc -o program {file}",
        "run_cmd": "./program",
        "timeout": 15,
        "memory_limit": "256m",
        "template": '''#include <stdio.h>

int main() {
    // Write your C code here
    
    return 0;
}
''',
        "common_errors": {
            "expected ';'": "You're missing a semicolon at the end of a statement.",
            "undeclared": "You're using a variable that hasn't been declared.",
            "implicit declaration": "You're using a function without including its header file.",
        }
    }
}

# Coding challenges for practice
CODING_CHALLENGES = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "Given an array of integers and a target, return indices of two numbers that add up to target.",
        "examples": [
            {"input": "[2,7,11,15], target=9", "output": "[0,1]"},
            {"input": "[3,2,4], target=6", "output": "[1,2]"}
        ],
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "expected_output": "[0, 1]"},
            {"input": "[3,2,4]\n6", "expected_output": "[1, 2]"},
            {"input": "[3,3]\n6", "expected_output": "[0, 1]"}
        ]
    },
    {
        "id": 2,
        "title": "Reverse String",
        "difficulty": "Easy",
        "description": "Write a function that reverses a string.",
        "examples": [
            {"input": "hello", "output": "olleh"},
            {"input": "world", "output": "dlrow"}
        ],
        "test_cases": [
            {"input": "hello", "expected_output": "olleh"},
            {"input": "world", "expected_output": "dlrow"},
            {"input": "python", "expected_output": "nohtyp"}
        ]
    },
    {
        "id": 3,
        "title": "Palindrome Check",
        "difficulty": "Easy",
        "description": "Check if a given string is a palindrome (reads same forwards and backwards).",
        "examples": [
            {"input": "racecar", "output": "true"},
            {"input": "hello", "output": "false"}
        ],
        "test_cases": [
            {"input": "racecar", "expected_output": "true"},
            {"input": "hello", "expected_output": "false"},
            {"input": "madam", "expected_output": "true"}
        ]
    },
    {
        "id": 4,
        "title": "FizzBuzz",
        "difficulty": "Easy",
        "description": "Print numbers 1 to n. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', for both print 'FizzBuzz'.",
        "examples": [
            {"input": "15", "output": "1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz"}
        ],
        "test_cases": [
            {"input": "15", "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"}
        ]
    },
    {
        "id": 5,
        "title": "Find Maximum",
        "difficulty": "Easy",
        "description": "Find the maximum number in an array.",
        "examples": [
            {"input": "[1, 5, 3, 9, 2]", "output": "9"},
            {"input": "[-1, -5, -3]", "output": "-1"}
        ],
        "test_cases": [
            {"input": "[1, 5, 3, 9, 2]", "expected_output": "9"},
            {"input": "[-1, -5, -3]", "expected_output": "-1"}
        ]
    }
]
