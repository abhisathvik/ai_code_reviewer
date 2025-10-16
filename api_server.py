#!/usr/bin/env python3
"""
FastAPI server for manual testing of the AI PR Reviewer
This is optional - the main functionality runs in GitHub Actions
"""

import os
import sys
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn

# Import our main reviewer
from pr_reviewer import GitHubPRReviewer


app = FastAPI(
    title="AI PR Reviewer API",
    description="API for testing AI-powered GitHub PR reviews",
    version="1.0.0"
)


class ReviewRequest(BaseModel):
    pr_number: int
    repo_name: str
    github_token: str


class ReviewResponse(BaseModel):
    success: bool
    message: str
    review_id: str = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "AI PR Reviewer API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    try:
        # Check if Ollama is available
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        ollama_status = "unavailable"
    
    return {
        "api": "healthy",
        "ollama": ollama_status,
        "github_token": "configured" if os.getenv("GITHUB_TOKEN") else "missing"
    }


@app.post("/review", response_model=ReviewResponse)
async def review_pr(request: ReviewRequest, background_tasks: BackgroundTasks):
    """
    Trigger a PR review manually.
    
    This endpoint accepts a PR review request and processes it in the background.
    """
    try:
        # Validate inputs
        if not request.github_token and not os.getenv("GITHUB_TOKEN"):
            raise HTTPException(status_code=400, detail="GitHub token is required")
        
        token = request.github_token or os.getenv("GITHUB_TOKEN")
        
        # Start review in background
        review_id = f"review_{request.repo_name.replace('/', '_')}_{request.pr_number}"
        background_tasks.add_task(
            run_review_task,
            token,
            request.repo_name,
            request.pr_number
        )
        
        return ReviewResponse(
            success=True,
            message=f"Review started for PR #{request.pr_number} in {request.repo_name}",
            review_id=review_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def run_review_task(token: str, repo_name: str, pr_number: int):
    """Background task to run the actual PR review."""
    try:
        reviewer = GitHubPRReviewer(token, repo_name)
        reviewer.review_pr(pr_number)
        print(f"Background review completed for PR #{pr_number}")
    except Exception as e:
        print(f"Background review failed for PR #{pr_number}: {e}")


@app.get("/models")
async def list_ollama_models():
    """List available Ollama models."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "models": [model["name"] for model in data.get("models", [])]
            }
        else:
            return {"success": False, "error": "Failed to fetch models"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/models/{model_name}")
async def pull_ollama_model(model_name: str):
    """Pull a new Ollama model."""
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": f"Successfully pulled model: {model_name}"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to pull model: {result.stderr}"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Model pull timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
