#!/usr/bin/env python3
"""
Test script for the AI PR Reviewer
Run this to test the reviewer locally before deploying
"""

import os
import sys
import json
from pr_reviewer import GitHubPRReviewer


def test_github_connection():
    """Test GitHub API connection."""
    print("🔗 Testing GitHub connection...")
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        return False
    
    try:
        from github import Github
        github = Github(token)
        user = github.get_user()
        print(f"✅ Connected as: {user.login}")
        return True
    except Exception as e:
        print(f"❌ GitHub connection failed: {e}")
        return False


def test_ollama_connection():
    """Test Ollama connection."""
    print("\n🤖 Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models")
            if models:
                print("Available models:")
                for model in models:
                    print(f"  - {model['name']}")
            return True
        else:
            print("❌ Ollama responded with error")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False


def test_model_availability(model_name="llama3.2"):
    """Test if the specified model is available."""
    print(f"\n🧠 Testing model availability: {model_name}")
    
    try:
        import requests
        payload = {
            "model": model_name,
            "prompt": "Hello, are you working?",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Model {model_name} is working")
            print(f"Response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Model {model_name} failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False


def test_pr_fetch():
    """Test fetching PR details."""
    print("\n📋 Testing PR fetch functionality...")
    
    # You'll need to replace these with actual values for testing
    repo_name = input("Enter repository name (owner/repo): ").strip()
    if not repo_name:
        print("❌ Repository name is required")
        return False
    
    try:
        pr_number = int(input("Enter PR number to test: ").strip())
    except ValueError:
        print("❌ Invalid PR number")
        return False
    
    try:
        token = os.getenv("GITHUB_TOKEN")
        reviewer = GitHubPRReviewer(token, repo_name)
        
        # Test fetching PR details
        pr = reviewer.get_pr_details(pr_number)
        print(f"✅ Successfully fetched PR: {pr.title}")
        
        # Test fetching changed files
        files = reviewer.get_changed_files(pr_number)
        print(f"✅ Found {len(files)} changed files")
        
        for file_info in files[:3]:  # Show first 3 files
            print(f"  - {file_info['filename']} ({file_info['status']})")
        
        return True
    except Exception as e:
        print(f"❌ PR fetch test failed: {e}")
        return False


def test_ai_review():
    """Test AI review generation."""
    print("\n🤖 Testing AI review generation...")
    
    # Create a sample prompt
    sample_prompt = """You are an expert code reviewer. Please review this GitHub Pull Request:

Pull Request Title: Fix authentication bug
Pull Request Description: This PR fixes a critical authentication issue

Changed Files:
--- File: auth.py (modified) ---
Additions: 5, Deletions: 2
Patch/Diff:
@@ -10,7 +10,7 @@ def authenticate_user(username, password):
-    if username == "admin" and password == "password":
+    if username == "admin" and password == get_env_password():
         return True
     return False

Please provide a thorough code review focusing on code quality, security, and best practices."""

    try:
        token = os.getenv("GITHUB_TOKEN")
        reviewer = GitHubPRReviewer(token, "test/repo")  # Dummy repo for testing
        
        response = reviewer.call_ollama(sample_prompt)
        
        if response and not response.startswith("Error"):
            print("✅ AI review generation successful")
            print(f"Response length: {len(response)} characters")
            print(f"Sample response: {response[:200]}...")
            return True
        else:
            print(f"❌ AI review generation failed: {response}")
            return False
    except Exception as e:
        print(f"❌ AI review test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 AI PR Reviewer Test Suite")
    print("=" * 40)
    
    tests = [
        test_github_connection,
        test_ollama_connection,
        test_model_availability,
        test_ai_review
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except KeyboardInterrupt:
            print("\n\n⏹️  Tests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} tests passed!")
        print("\n🚀 Your AI PR Reviewer is ready to use!")
    else:
        print(f"❌ {total - passed} out of {total} tests failed")
        print("\n🔧 Please fix the issues above before deploying")
        
        if not results[0]:  # GitHub connection
            print("💡 Set GITHUB_TOKEN environment variable")
        if not results[1]:  # Ollama connection
            print("💡 Start Ollama: ollama serve")
        if not results[2]:  # Model availability
            print("💡 Pull a model: ollama pull llama3.2")


if __name__ == "__main__":
    main()
