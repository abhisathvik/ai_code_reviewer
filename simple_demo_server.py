#!/usr/bin/env python3
"""
Simple demo server for testing the AI PR Reviewer locally
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(
    title="AI PR Reviewer Demo",
    description="Local demo of AI-powered GitHub PR reviews",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Home page with demo interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI PR Reviewer Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
            .card { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea; }
            .success { border-left-color: #28a745; }
            .warning { border-left-color: #ffc107; }
            .info { border-left-color: #17a2b8; }
            .code { background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; }
            .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #5a6fd8; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 AI PR Reviewer Demo</h1>
            <p>Test the AI-powered GitHub PR reviewer locally</p>
        </div>

        <div class="card info">
            <h3>🚀 Quick Start</h3>
            <p>This demo shows how the AI PR Reviewer works. Follow these steps:</p>
            <ol>
                <li>Get a GitHub token from <a href="https://github.com/settings/tokens" target="_blank">GitHub Settings</a></li>
                <li>Set the token: <code class="code">export GITHUB_TOKEN=your_token_here</code></li>
                <li>Test with a real repository and PR</li>
            </ol>
        </div>

        <div class="card warning">
            <h3>⚠️ GitHub Token Required</h3>
            <p>To test with real GitHub data, you need a GitHub personal access token:</p>
            <ul>
                <li>Go to <a href="https://github.com/settings/tokens" target="_blank">GitHub Settings → Developer Settings → Personal Access Tokens</a></li>
                <li>Generate a new token with <code>repo</code> scope (or <code>public_repo</code> for public repositories)</li>
                <li>Set it as an environment variable: <code class="code">export GITHUB_TOKEN=your_token</code></li>
            </ul>
        </div>

        <div class="card success">
            <h3>✅ Available Endpoints</h3>
            <ul>
                <li><strong>GET /health</strong> - Check system health</li>
                <li><strong>GET /models</strong> - List available AI models (requires Ollama)</li>
                <li><strong>POST /demo-review</strong> - Generate a demo review</li>
                <li><strong>GET /docs</strong> - API documentation</li>
            </ul>
        </div>

        <div class="card info">
            <h3>🧪 Test Commands</h3>
            <p>Once you have your GitHub token set up:</p>
            <div class="code">
                # Test GitHub connection<br>
                python3 setup_and_test.py<br><br>
                
                # Test demo reviewer (dry run)<br>
                python3 demo_reviewer.py --pr-number 1 --repo owner/repo --dry-run<br><br>
                
                # Start full API server<br>
                python3 api_server.py
            </div>
        </div>

        <div class="card">
            <h3>🎯 What This Does</h3>
            <p>The AI PR Reviewer automatically:</p>
            <ul>
                <li>🔍 Analyzes code changes in pull requests</li>
                <li>🤖 Uses AI to generate intelligent feedback</li>
                <li>📝 Posts structured comments with suggestions</li>
                <li>🛡️ Identifies security and performance issues</li>
                <li>✨ Provides constructive code improvement advice</li>
            </ul>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/health" class="btn">Check Health</a>
            <a href="/demo-review" class="btn">Generate Demo Review</a>
            <a href="/docs" class="btn">API Docs</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Check system health."""
    import os
    
    health_status = {
        "api": "healthy",
        "github_token": "configured" if os.getenv("GITHUB_TOKEN") else "missing",
        "ollama": "checking...",
        "python_version": "3.x",
        "status": "demo_mode"
    }
    
    # Check Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        health_status["ollama"] = "running" if response.status_code == 200 else "not_responding"
    except:
        health_status["ollama"] = "not_installed"
    
    return health_status


@app.get("/demo-review")
async def generate_demo_review():
    """Generate a demo review to show what the AI reviewer produces."""
    
    demo_review = """🤖 **AI Code Review** (Demo Mode)

## Summary
This is a demonstration of what the AI PR Reviewer would generate for a real pull request.

**Changes Overview:**
- 📁 3 files changed
- ➕ 45 lines added
- ➖ 12 lines deleted
- 🔤 Languages: Python, JavaScript

## 📋 Detailed Analysis

### Files Reviewed:
- **src/auth.py** (modified) - 23 additions, 5 deletions
- **tests/test_auth.py** (added) - 15 additions, 0 deletions
- **README.md** (modified) - 7 additions, 7 deletions

### 🔍 Code Quality Assessment

**Strengths I noticed:**
- ✅ Clean file organization
- ✅ Good use of Python conventions
- ✅ Comprehensive test coverage
- ✅ Clear commit message structure

**Areas for improvement:**
- 🔍 Consider adding type hints for better code documentation
- 📝 Add inline documentation for complex authentication logic
- 🛡️ Review for potential security vulnerabilities in password handling
- ⚡ Check for performance optimizations in database queries

### 🚨 Potential Issues

**Security Considerations:**
- 🔐 Verify password hashing uses secure algorithms (bcrypt, scrypt)
- 🛡️ Check for SQL injection risks in user queries
- 🔑 Ensure JWT tokens are properly signed and have reasonable expiration

**Performance Notes:**
- ⚡ Consider implementing rate limiting for authentication attempts
- 💾 Review database connection pooling
- 🔄 Add caching for frequently accessed user data

### 💡 Suggestions

1. **Testing**: Excellent test coverage! Consider adding integration tests
2. **Documentation**: Add docstrings for the authentication functions
3. **Error Handling**: Implement more specific error messages for debugging
4. **Logging**: Add structured logging for authentication events

### 🎯 Code Examples

**Good practices observed:**
```python
def authenticate_user(username: str, password: str) -> bool:
    # Good: Type hints and clear function signature
    hashed_password = get_user_password(username)
    return bcrypt.verify(password, hashed_password)
```

**Suggestions for improvement:**
```python
def authenticate_user(username: str, password: str) -> AuthenticationResult:
    # Better: Return structured result instead of just boolean
    try:
        user = get_user_by_username(username)
        if not user:
            return AuthenticationResult(success=False, reason="user_not_found")
        
        if bcrypt.verify(password, user.hashed_password):
            return AuthenticationResult(success=True, user=user)
        else:
            return AuthenticationResult(success=False, reason="invalid_password")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return AuthenticationResult(success=False, reason="system_error")
```

---
*This is a demo review. In production, this would be generated by an AI model like Llama3.2 or Mistral running locally with Ollama.*"""

    return {
        "success": True,
        "review": demo_review,
        "metadata": {
            "demo_mode": True,
            "generated_by": "demo_reviewer",
            "timestamp": "2024-01-16T07:00:00Z"
        }
    }


if __name__ == "__main__":
    print("🚀 Starting AI PR Reviewer Demo Server")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API docs at: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "simple_demo_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
