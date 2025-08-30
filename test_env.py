#!/usr/bin/env python3
"""
Test script để kiểm tra môi trường phát triển
"""
import sys
import subprocess

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def test_pip_packages():
    """Test các thư viện cần thiết"""
    print("\n📦 Testing required packages...")
    required_packages = [
        'streamlit',
        'openai',
        'anthropic',
        'google.generativeai',
        'langchain',
        'python-dotenv'
    ]

    success_count = 0
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai as genai
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package} - OK")
            success_count += 1
        except ImportError:
            print(f"❌ {package} - MISSING")

    return success_count == len(required_packages)

def test_env_file():
    """Test file .env"""
    print("\n🔑 Testing .env file...")
    try:
        from dotenv import load_dotenv
        import os

        load_dotenv()

        # Check for API keys (optional)
        api_keys = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
        }

        found_keys = [k for k, v in api_keys.items() if v]
        if found_keys:
            print(f"✅ Found {len(found_keys)} API key(s): {', '.join(found_keys)}")
        else:
            print("⚠️  No API keys found in .env (optional for basic testing)")

        return True
    except ImportError:
        print("❌ python-dotenv not found")
        return False
    except Exception as e:
        print(f"⚠️  Error reading .env: {e}")
        return True  # Not critical

def main():
    """Main test function"""
    print("🚀 Testing Development Environment")
    print("=" * 50)

    tests = [
        test_python_version,
        test_pip_packages,
        test_env_file
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 50)
    print("📊 Test Results:")

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("\n🎉 Your environment is ready for LLM development!")
        print("\nNext steps:")
        print("1. Add your API keys to .env file (see ENV_SETUP_GUIDE.md)")
        print("2. Run: cd starter_ai_agents/ai_travel_agent")
        print("3. Run: streamlit run travel_agent.py")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\nPlease fix the failed tests before proceeding.")

if __name__ == "__main__":
    main()

