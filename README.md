# 🤖 AI-Powered GitHub PR Reviewer

An intelligent GitHub Pull Request reviewer that uses AI to automatically analyze code changes and provide constructive feedback. Built with Ollama (local LLM) and runs entirely within GitHub Actions - completely free!

## ✨ Features

- **Automatic PR Reviews**: Triggers on PR creation and updates
- **AI-Powered Analysis**: Uses Ollama with Llama3/Mistral models
- **Comprehensive Feedback**: Reviews code quality, security, performance, and best practices
- **Free & Open Source**: No external API costs, runs locally in GitHub Actions
- **Smart Commenting**: Posts organized, actionable feedback directly to PRs

## 🏗️ Architecture

```
GitHub PR Created/Updated
        ↓
GitHub Action Triggered
        ↓
Fetch PR Details & Diff
        ↓
Send to Ollama (Local LLM)
        ↓
AI Generates Review
        ↓
Post Comments to PR
```

## 🛠️ Components

- **Backend**: Python with FastAPI (for optional API mode)
- **AI Model**: Ollama with Llama3.2 or Mistral (local, free)
- **GitHub Integration**: GitHub REST API via PyGithub
- **CI/CD**: GitHub Actions workflow
- **Hosting**: Runs entirely within GitHub Actions (no external hosting needed)

## 🚀 Setup

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/yourusername/ai_code_reviewer.git
cd ai_code_reviewer
```

### 2. Enable GitHub Actions

The workflow will automatically trigger on PR events. Make sure GitHub Actions are enabled for your repository.

### 3. Configure GitHub Token (if needed)

The workflow uses the built-in `GITHUB_TOKEN` which should work automatically. For additional permissions, you can:

1. Go to your repository settings
2. Navigate to "Actions" → "General"
3. Ensure "Read and write permissions" is enabled for the token

### 4. Test the Setup

Create a test PR in your repository to see the AI reviewer in action!

## 📁 Project Structure

```
ai_code_reviewer/
├── .github/
│   └── workflows/
│       └── pr-reviewer.yml    # GitHub Actions workflow
├── pr_reviewer.py             # Main reviewer script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Configuration

### Customizing the AI Model

Edit `.github/workflows/pr-reviewer.yml` to change the Ollama model:

```yaml
- name: Install Ollama
  run: |
    curl -fsSL https://ollama.ai/install.sh | sh
    ollama serve &
    sleep 10
    ollama pull llama3.2  # Change this to mistral, codellama, etc.
```

Available models:
- `llama3.2` (default) - Good balance of speed and quality
- `mistral` - Fast and efficient
- `codellama` - Specialized for code
- `deepseek-coder` - Excellent for code analysis

### Adjusting Review Prompts

Edit the `generate_review_prompt()` method in `pr_reviewer.py` to customize what the AI focuses on during reviews.

## 🎯 How It Works

### 1. Trigger
When a PR is created or updated, GitHub Actions automatically triggers the workflow.

### 2. Setup
The workflow:
- Installs Python and dependencies
- Downloads and starts Ollama
- Pulls the specified AI model (e.g., Llama3.2)

### 3. Analysis
The script:
- Fetches PR details and changed files
- Generates a comprehensive prompt for the AI
- Sends the prompt to Ollama for analysis

### 4. Review Generation
Ollama analyzes the code focusing on:
- Code quality and readability
- Security vulnerabilities
- Performance concerns
- Best practices adherence
- Potential bugs
- Documentation quality
- Test coverage

### 5. Comment Posting
The AI-generated review is:
- Parsed into organized sections
- Posted as comments on the PR
- Formatted with emojis and clear structure

## 📝 Example Review Output

```
🤖 AI Code Review

I've analyzed this PR and here are my findings:

**Summary**: This PR adds user authentication functionality with good overall structure.

**Strengths**:
- Clean separation of concerns
- Proper error handling
- Good use of type hints

**Issues Found**:
- Line 45: Potential SQL injection vulnerability in user query
- Line 78: Missing input validation for email field
- Consider adding unit tests for the new authentication methods

**Suggestions**:
- Add rate limiting for login attempts
- Consider using environment variables for JWT secrets
- Add logging for authentication events
```

## 🔒 Security Considerations

- The bot runs with the repository's `GITHUB_TOKEN`
- No external API keys or secrets required
- All AI processing happens locally in GitHub Actions
- Code is never sent to external services

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not responding**
   - Check if the model was downloaded successfully
   - Ensure sufficient time for Ollama to start (sleep 10 in workflow)

2. **GitHub API rate limits**
   - The built-in token should have sufficient rate limits
   - Consider adding delays between API calls if needed

3. **Large PR timeouts**
   - GitHub Actions has a 6-hour limit
   - Consider splitting very large PRs

### Debug Mode

Add debug logging by modifying the workflow:

```yaml
- name: Run AI PR Review
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    PR_NUMBER: ${{ github.event.number }}
    REPO_NAME: ${{ github.repository }}
    DEBUG: "true"
  run: |
    python pr_reviewer.py --pr-number $PR_NUMBER --repo $REPO_NAME
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with a PR (the bot will review it!)
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing local LLM capabilities
- [GitHub Actions](https://github.com/features/actions) for the CI/CD platform
- [PyGithub](https://pygithub.readthedocs.io/) for GitHub API integration
- The open-source community for the amazing AI models

---

**Happy Coding! 🚀**
