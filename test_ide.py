"""
Quick test script for the AI-Powered IDE
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from online_ide.code_executor import CodeExecutor
from online_ide.language_configs import LANGUAGE_CONFIGS, CODING_CHALLENGES

def test_basic_execution():
    """Test basic code execution"""
    print("🧪 Testing Code Executor...")
    executor = CodeExecutor()
    
    # Test Python
    print("\n1️⃣ Testing Python execution:")
    result = executor.execute_code(
        code='print("Hello from Python!")',
        language='python'
    )
    print(f"   Success: {result['success']}")
    print(f"   Output: {result['output'].strip()}")
    print(f"   Time: {result['execution_time']}s")
    
    # Test Python with error
    print("\n2️⃣ Testing Python with error (AI explanation):")
    result = executor.execute_code(
        code='def hello()\n    print("missing colon")',
        language='python'
    )
    print(f"   Success: {result['success']}")
    print(f"   Error detected: {bool(result.get('error'))}")
    print(f"   AI explanation available: {bool(result.get('ai_explanation'))}")
    if result.get('ai_explanation'):
        ai = result['ai_explanation']
        if ai.get('quick_hint'):
            print(f"   Quick hint: {ai['quick_hint'][:50]}...")
    
    # Test JavaScript
    print("\n3️⃣ Testing JavaScript execution:")
    result = executor.execute_code(
        code='console.log("Hello from JavaScript!");',
        language='javascript'
    )
    print(f"   Success: {result['success']}")
    if result['success']:
        print(f"   Output: {result['output'].strip()}")
    else:
        print(f"   Note: Node.js may not be installed (this is OK)")
    
    print("\n✅ Basic execution tests complete!")

def test_code_analysis():
    """Test code quality analysis"""
    print("\n🧪 Testing Code Analysis...")
    executor = CodeExecutor()
    
    code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
    
    result = executor.analyze_code_quality(code, 'python')
    print(f"   Score: {result.get('score', 'N/A')}/10")
    print(f"   Strengths: {len(result.get('strengths', []))} found")
    print(f"   Improvements: {len(result.get('improvements', []))} suggested")
    print(f"   Performance tip available: {bool(result.get('performance_tip'))}")
    
    print("\n✅ Code analysis test complete!")

def test_configurations():
    """Test language configurations"""
    print("\n🧪 Testing Configurations...")
    
    print(f"   Languages available: {len(LANGUAGE_CONFIGS)}")
    for lang_id, config in LANGUAGE_CONFIGS.items():
        print(f"   - {config['name']} ({config['version']})")
    
    print(f"\n   Coding challenges: {len(CODING_CHALLENGES)}")
    for challenge in CODING_CHALLENGES[:3]:
        print(f"   - {challenge['title']} ({challenge['difficulty']})")
    
    print("\n✅ Configuration tests complete!")

def test_docker_availability():
    """Check if Docker is available"""
    print("\n🧪 Testing Docker Availability...")
    import subprocess
    
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            print(f"   ✅ Docker available: {version}")
            print("   → Code will run in isolated containers (recommended)")
        else:
            print("   ⚠️  Docker not available")
            print("   → Code will run locally (fallback mode)")
    except Exception as e:
        print("   ⚠️  Docker not available")
        print("   → Code will run locally (fallback mode)")
    
    print("\n✅ Docker check complete!")

def test_llm_availability():
    """Check if LLM is configured"""
    print("\n🧪 Testing LLM Configuration...")
    
    try:
        from llm_utils import call_llm_chat
        print("   ✅ LLM utilities imported successfully")
        
        # Check for API keys
        import os
        has_openai = bool(os.environ.get("OPENAI_API_KEY"))
        has_groq = bool(os.environ.get("GROQ_API_KEY"))
        
        if has_openai:
            print("   ✅ OpenAI API key found")
        if has_groq:
            print("   ✅ Groq API key found")
        
        if not (has_openai or has_groq):
            print("   ⚠️  No LLM API keys found in environment")
            print("   → AI explanations may not work")
        else:
            print("   → AI-powered error explanations ready!")
            
    except Exception as e:
        print(f"   ⚠️  LLM utilities not available: {e}")
        print("   → AI explanations will not work")
    
    print("\n✅ LLM check complete!")

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 AI-Powered IDE - Test Suite")
    print("=" * 60)
    
    try:
        test_configurations()
        test_docker_availability()
        test_llm_availability()
        test_basic_execution()
        test_code_analysis()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("   1. Start your server: python start.py")
        print("   2. Navigate to: http://localhost:8000/ide")
        print("   3. Try writing and running code!")
        print("\n💡 Tip: Install Docker for better security and isolation")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
