"""
Coding Challenge Service

Handles coding challenge questions with test cases and code execution
"""

import json
import random
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

class CodingChallengeService:
    """Service for managing coding challenges"""
    
    # Coding challenge bank
    CODING_CHALLENGES = [
        {
            "id": "two-sum",
            "title": "Two Sum",
            "difficulty": "beginner",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
            "examples": [
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}
            ],
            "starter_code": {
                "python": "def two_sum(nums, target):\n    # Write your code here\n    pass",
                "javascript": "function twoSum(nums, target) {\n    // Write your code here\n}",
                "java": "public int[] twoSum(int[] nums, int target) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
                {"input": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
                {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]}
            ],
            "hints": [
                "Try using a hash map to store numbers you've seen",
                "For each number, check if target - number exists in the map"
            ]
        },
        {
            "id": "reverse-string",
            "title": "Reverse String",
            "difficulty": "beginner",
            "description": "Write a function that reverses a string. The input string is given as an array of characters.",
            "examples": [
                {"input": "s = ['h','e','l','l','o']", "output": "['o','l','l','e','h']"},
                {"input": "s = ['H','a','n','n','a','h']", "output": "['h','a','n','n','a','H']"}
            ],
            "starter_code": {
                "python": "def reverse_string(s):\n    # Write your code here\n    pass",
                "javascript": "function reverseString(s) {\n    // Write your code here\n}",
                "java": "public void reverseString(char[] s) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"s": ["h", "e", "l", "l", "o"]}, "expected": ["o", "l", "l", "e", "h"]},
                {"input": {"s": ["H", "a", "n", "n", "a", "h"]}, "expected": ["h", "a", "n", "n", "a", "H"]}
            ],
            "hints": [
                "Use two pointers approach",
                "Swap characters from both ends moving towards center"
            ]
        },
        {
            "id": "palindrome-number",
            "title": "Palindrome Number",
            "difficulty": "beginner",
            "description": "Given an integer x, return true if x is a palindrome, and false otherwise.",
            "examples": [
                {"input": "x = 121", "output": "true", "explanation": "121 reads as 121 from left to right and right to left"},
                {"input": "x = -121", "output": "false", "explanation": "From left to right, it reads -121. From right to left, it becomes 121-"},
                {"input": "x = 10", "output": "false"}
            ],
            "starter_code": {
                "python": "def is_palindrome(x):\n    # Write your code here\n    pass",
                "javascript": "function isPalindrome(x) {\n    // Write your code here\n}",
                "java": "public boolean isPalindrome(int x) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"x": 121}, "expected": True},
                {"input": {"x": -121}, "expected": False},
                {"input": {"x": 10}, "expected": False},
                {"input": {"x": 0}, "expected": True}
            ],
            "hints": [
                "Negative numbers are not palindromes",
                "Convert to string or reverse the number mathematically"
            ]
        },
        {
            "id": "fizzbuzz",
            "title": "FizzBuzz",
            "difficulty": "beginner",
            "description": "Given an integer n, return a string array where: answer[i] == 'FizzBuzz' if i is divisible by 3 and 5, 'Fizz' if divisible by 3, 'Buzz' if divisible by 5, or str(i) otherwise.",
            "examples": [
                {"input": "n = 3", "output": "['1','2','Fizz']"},
                {"input": "n = 5", "output": "['1','2','Fizz','4','Buzz']"},
                {"input": "n = 15", "output": "['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz','11','Fizz','13','14','FizzBuzz']"}
            ],
            "starter_code": {
                "python": "def fizzbuzz(n):\n    # Write your code here\n    pass",
                "javascript": "function fizzBuzz(n) {\n    // Write your code here\n}",
                "java": "public List<String> fizzBuzz(int n) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"n": 3}, "expected": ["1", "2", "Fizz"]},
                {"input": {"n": 5}, "expected": ["1", "2", "Fizz", "4", "Buzz"]},
                {"input": {"n": 15}, "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]}
            ],
            "hints": [
                "Check divisibility by 15 first (both 3 and 5)",
                "Use modulo operator to check divisibility"
            ]
        },
        {
            "id": "valid-parentheses",
            "title": "Valid Parentheses",
            "difficulty": "intermediate",
            "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets and in the correct order.",
            "examples": [
                {"input": "s = '()'", "output": "true"},
                {"input": "s = '()[]{}'", "output": "true"},
                {"input": "s = '(]'", "output": "false"}
            ],
            "starter_code": {
                "python": "def is_valid(s):\n    # Write your code here\n    pass",
                "javascript": "function isValid(s) {\n    // Write your code here\n}",
                "java": "public boolean isValid(String s) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"s": "()"}, "expected": True},
                {"input": {"s": "()[]{}"}, "expected": True},
                {"input": {"s": "(]"}, "expected": False},
                {"input": {"s": "([)]"}, "expected": False},
                {"input": {"s": "{[]}"}, "expected": True}
            ],
            "hints": [
                "Use a stack data structure",
                "Push opening brackets, pop and match closing brackets"
            ]
        },
        {
            "id": "merge-sorted-arrays",
            "title": "Merge Two Sorted Arrays",
            "difficulty": "intermediate",
            "description": "You are given two integer arrays nums1 and nums2, sorted in non-decreasing order. Merge nums1 and nums2 into a single array sorted in non-decreasing order.",
            "examples": [
                {"input": "nums1 = [1,2,3], nums2 = [2,5,6]", "output": "[1,2,2,3,5,6]"},
                {"input": "nums1 = [1], nums2 = []", "output": "[1]"}
            ],
            "starter_code": {
                "python": "def merge(nums1, nums2):\n    # Write your code here\n    pass",
                "javascript": "function merge(nums1, nums2) {\n    // Write your code here\n}",
                "java": "public int[] merge(int[] nums1, int[] nums2) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"nums1": [1, 2, 3], "nums2": [2, 5, 6]}, "expected": [1, 2, 2, 3, 5, 6]},
                {"input": {"nums1": [1], "nums2": []}, "expected": [1]},
                {"input": {"nums1": [], "nums2": [1]}, "expected": [1]}
            ],
            "hints": [
                "Use two pointers, one for each array",
                "Compare elements and add smaller one to result"
            ]
        },
        {
            "id": "binary-search",
            "title": "Binary Search",
            "difficulty": "intermediate",
            "description": "Given a sorted array of integers nums and an integer target, write a function to search target in nums. If target exists, return its index. Otherwise, return -1.",
            "examples": [
                {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
                {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"}
            ],
            "starter_code": {
                "python": "def binary_search(nums, target):\n    # Write your code here\n    pass",
                "javascript": "function binarySearch(nums, target) {\n    // Write your code here\n}",
                "java": "public int binarySearch(int[] nums, int target) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "expected": 4},
                {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "expected": -1},
                {"input": {"nums": [5], "target": 5}, "expected": 0}
            ],
            "hints": [
                "Use left and right pointers",
                "Compare middle element with target and adjust search range"
            ]
        },
        {
            "id": "longest-substring",
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "advanced",
            "description": "Given a string s, find the length of the longest substring without repeating characters.",
            "examples": [
                {"input": "s = 'abcabcbb'", "output": "3", "explanation": "The answer is 'abc', with length 3"},
                {"input": "s = 'bbbbb'", "output": "1", "explanation": "The answer is 'b', with length 1"},
                {"input": "s = 'pwwkew'", "output": "3", "explanation": "The answer is 'wke', with length 3"}
            ],
            "starter_code": {
                "python": "def length_of_longest_substring(s):\n    # Write your code here\n    pass",
                "javascript": "function lengthOfLongestSubstring(s) {\n    // Write your code here\n}",
                "java": "public int lengthOfLongestSubstring(String s) {\n    // Write your code here\n}"
            },
            "test_cases": [
                {"input": {"s": "abcabcbb"}, "expected": 3},
                {"input": {"s": "bbbbb"}, "expected": 1},
                {"input": {"s": "pwwkew"}, "expected": 3},
                {"input": {"s": ""}, "expected": 0}
            ],
            "hints": [
                "Use sliding window technique",
                "Keep track of characters in current window using a set or map"
            ]
        }
    ]
    
    def __init__(self):
        self.cache = {}
    
    def get_all_challenges(self, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all coding challenges, optionally filtered by difficulty"""
        challenges = self.CODING_CHALLENGES.copy()
        
        if difficulty:
            challenges = [c for c in challenges if c.get("difficulty") == difficulty]
        
        return challenges
    
    def get_challenge_by_id(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific challenge by ID"""
        for challenge in self.CODING_CHALLENGES:
            if challenge.get("id") == challenge_id:
                return challenge.copy()
        return None
    
    def get_random_challenge(self, difficulty: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a random coding challenge"""
        challenges = self.get_all_challenges(difficulty)
        return random.choice(challenges) if challenges else None
    
    def get_starter_code(self, challenge_id: str, language: str = "python") -> str:
        """Get starter code for a challenge in specified language"""
        challenge = self.get_challenge_by_id(challenge_id)
        if not challenge:
            return ""
        
        starter_code = challenge.get("starter_code", {})
        return starter_code.get(language, starter_code.get("python", ""))
    
    def get_test_cases(self, challenge_id: str) -> List[Dict[str, Any]]:
        """Get test cases for a challenge"""
        challenge = self.get_challenge_by_id(challenge_id)
        if not challenge:
            return []
        
        return challenge.get("test_cases", [])
    
    def validate_solution(self, challenge_id: str, user_code: str, language: str = "python") -> Dict[str, Any]:
        """
        Validate user's solution against test cases
        
        Note: This is a placeholder. Actual code execution should be done
        through the online_ide/code_executor.py service
        """
        challenge = self.get_challenge_by_id(challenge_id)
        if not challenge:
            return {"error": "Challenge not found"}
        
        test_cases = challenge.get("test_cases", [])
        
        return {
            "challenge_id": challenge_id,
            "test_cases": test_cases,
            "user_code": user_code,
            "language": language,
            "message": "Use /api/code/execute endpoint to run code"
        }
    
    def get_hints(self, challenge_id: str) -> List[str]:
        """Get hints for a challenge"""
        challenge = self.get_challenge_by_id(challenge_id)
        if not challenge:
            return []
        
        return challenge.get("hints", [])
    
    def get_challenge_stats(self) -> Dict[str, Any]:
        """Get statistics about available challenges"""
        total = len(self.CODING_CHALLENGES)
        by_difficulty = {}
        
        for challenge in self.CODING_CHALLENGES:
            diff = challenge.get("difficulty", "unknown")
            by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
        
        return {
            "total_challenges": total,
            "by_difficulty": by_difficulty,
            "languages_supported": ["python", "javascript", "java"]
        }
