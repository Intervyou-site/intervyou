#!/usr/bin/env python3
"""Quick test of resume analyzer functionality"""

from resume_analyzer import analyze_resume_full
import json

def test_resume_analyzer():
    """Test the resume analyzer with sample resume"""
    
    # Read sample resume
    with open('test_resume_sample.txt', 'rb') as f:
        file_bytes = f.read()
    
    # Analyze
    print("🔍 Analyzing sample resume...")
    result = analyze_resume_full(file_bytes, 'test_resume_sample.txt')
    
    # Print results
    if result.get('success'):
        print("\n✅ Analysis successful!")
        print(f"\n📊 Overall Score: {result['overall_score']}% (Grade: {result['grade']})")
        print(f"\n📈 Detailed Scores:")
        print(f"  - Format: {result['scores']['format']}%")
        print(f"  - Content: {result['scores']['content']}%")
        print(f"  - Structure: {result['scores']['structure']}%")
        
        print(f"\n📝 Statistics:")
        print(f"  - Word Count: {result['word_count']}")
        print(f"  - Action Verbs: {result['action_verbs']['count']}")
        print(f"  - Quantifiable Achievements: {result['achievements']['numbers_found']}")
        
        print(f"\n💡 Feedback ({len(result['feedback'])} items):")
        for item in result['feedback']:
            icon = {'critical': '🔴', 'warning': '⚠️', 'info': 'ℹ️', 'success': '✅'}.get(item['type'], 'ℹ️')
            print(f"  {icon} [{item['category']}] {item['message']}")
        
        print("\n✨ Test completed successfully!")
    else:
        print(f"\n❌ Analysis failed: {result.get('error')}")
        return False
    
    return True

if __name__ == "__main__":
    test_resume_analyzer()
