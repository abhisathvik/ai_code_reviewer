# 🚀 GitHub Deployment Guide

Deploy your AI PR Reviewer to GitHub in 3 easy steps!

## Step 1: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `ai_code_reviewer`
3. **Description**: `🤖 AI-powered GitHub PR reviewer using Ollama - automatically reviews pull requests with intelligent feedback`
4. **Make it PUBLIC** (required for GitHub Actions to work properly)
5. **Don't initialize** with README, .gitignore, or license (we already have them)
6. **Click "Create repository"**

## Step 2: Run Deployment Script

```bash
# Make the script executable (already done)
chmod +x deploy_to_github.sh

# Run the deployment script
./deploy_to_github.sh
```

The script will:
- ✅ Ask for your GitHub username
- ✅ Set up the remote repository
- ✅ Push all your code to GitHub
- ✅ Show you the next steps

## Step 3: Test the AI Reviewer

1. **Go to your repository**: https://github.com/YOUR_USERNAME/ai_code_reviewer
2. **Create a test PR**:
   - Make a small change to any file
   - Create a pull request
   - Watch the magic happen!
3. **Check GitHub Actions**: Go to the "Actions" tab to see the workflow running
4. **See the AI review**: The bot will post intelligent feedback on your PR

## 🎯 What Happens After Deployment

### Automatic PR Reviews
- Every new PR triggers the AI reviewer
- Ollama downloads and runs locally (free!)
- AI analyzes code changes
- Intelligent feedback is posted as comments

### GitHub Actions Workflow
- Runs on: `pull_request` events
- Installs: Python, Ollama, AI models
- Reviews: Code quality, security, performance
- Posts: Structured feedback comments

### AI Review Features
- 🔍 **Code Quality Analysis**
- 🛡️ **Security Vulnerability Detection**
- ⚡ **Performance Optimization Suggestions**
- 📝 **Best Practice Recommendations**
- 🐛 **Potential Bug Detection**
- 📚 **Documentation Suggestions**

## 🔧 Configuration Options

### Change AI Model
Edit `.github/workflows/pr-reviewer.yml`:
```yaml
ollama pull mistral  # or codellama, deepseek-coder, etc.
```

### Customize Review Focus
Edit `pr_reviewer.py` → `generate_review_prompt()` method

### Adjust Triggers
Edit `.github/workflows/pr-reviewer.yml` → `on:` section

## 🧪 Testing Your Deployment

### Create Test PR
1. Make a small change to any file
2. Commit and push to a new branch
3. Create pull request
4. Watch the AI reviewer analyze your code!

### Monitor GitHub Actions
- Go to repository → Actions tab
- See the "AI PR Reviewer" workflow running
- Check logs if there are any issues

## 🎉 Success!

Once deployed, your AI PR Reviewer will:
- ✅ Automatically review every PR
- ✅ Provide intelligent, constructive feedback
- ✅ Help improve code quality
- ✅ Run completely free (no API costs)
- ✅ Work with any programming language

## 📞 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Verify repository is public
3. Ensure workflow file is in `.github/workflows/`
4. Check that GitHub Actions are enabled

---

**Your AI-powered code review assistant is ready to help! 🤖✨**
