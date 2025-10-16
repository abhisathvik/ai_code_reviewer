# 🚀 Quick Start Guide

Get your AI PR Reviewer up and running in 5 minutes!

## 1. Deploy to Your Repository

### Option A: Fork This Repository (Recommended)
1. Click "Fork" on this repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai_code_reviewer.git
   cd ai_code_reviewer
   ```
3. Push to your repository:
   ```bash
   git push origin main
   ```

### Option B: Copy Files to Existing Repository
1. Copy these files to your repository:
   - `.github/workflows/pr-reviewer.yml`
   - `pr_reviewer.py`
   - `requirements.txt`
2. Commit and push:
   ```bash
   git add .
   git commit -m "Add AI PR reviewer"
   git push
   ```

## 2. Test It Out

1. Create a test PR in your repository
2. Watch the Actions tab - you should see "AI PR Reviewer" running
3. Once complete, check your PR for AI-generated comments!

## 3. Customize (Optional)

### Change the AI Model
Edit `.github/workflows/pr-reviewer.yml`:
```yaml
ollama pull mistral  # or codellama, deepseek-coder, etc.
```

### Adjust Review Focus
Edit the `generate_review_prompt()` method in `pr_reviewer.py` to customize what the AI looks for.

## 4. Troubleshooting

### If the Action Fails:
1. Check the Actions tab for error logs
2. Ensure GitHub Actions are enabled in your repo settings
3. Verify the workflow file is in `.github/workflows/`

### If No Comments Appear:
1. Check if the PR is from a fork (GitHub Actions have limited permissions on forks)
2. Verify the `GITHUB_TOKEN` has write permissions
3. Look for errors in the Action logs

## 5. Advanced Setup

### Local Testing
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull llama3.2

# Set your GitHub token
export GITHUB_TOKEN=your_token_here

# Test the reviewer
python test_reviewer.py
```

### API Server (Optional)
```bash
# Run the FastAPI server
python api_server.py

# Visit http://localhost:8000/docs for API documentation
```

## 🎉 You're Done!

Your AI PR Reviewer is now active! Every new PR will automatically get intelligent code reviews.

### What Happens Next:
1. **PR Created** → GitHub Action triggers
2. **Code Analysis** → AI reviews your changes
3. **Smart Comments** → Detailed feedback posted to PR
4. **Continuous Learning** → Improve your code with each review

### Pro Tips:
- The bot works best with focused PRs (not too large)
- Include good PR descriptions for better AI context
- The AI will learn your codebase patterns over time

Happy coding! 🤖✨
