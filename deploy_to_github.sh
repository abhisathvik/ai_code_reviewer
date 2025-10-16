#!/bin/bash

# Deploy AI PR Reviewer to GitHub
# Run this script after creating the GitHub repository

echo "🚀 AI PR Reviewer - GitHub Deployment"
echo "======================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Run 'git init' first."
    exit 1
fi

# Get repository URL from user
echo ""
echo "📋 Please create a GitHub repository first:"
echo "1. Go to: https://github.com/new"
echo "2. Name: ai_code_reviewer"
echo "3. Description: 🤖 AI-powered GitHub PR reviewer using Ollama"
echo "4. Make it PUBLIC (required for GitHub Actions)"
echo "5. Don't initialize with README"
echo "6. Click 'Create repository'"
echo ""

read -p "📝 Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "❌ Username is required"
    exit 1
fi

# Set up remote and push
echo ""
echo "🔗 Setting up GitHub remote..."

# Remove existing origin if it exists
git remote remove origin 2>/dev/null

# Add new origin
git remote add origin "https://github.com/$username/ai_code_reviewer.git"

echo "✅ Remote added: https://github.com/$username/ai_code_reviewer.git"

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Successfully deployed to GitHub!"
    echo ""
    echo "📍 Your repository: https://github.com/$username/ai_code_reviewer"
    echo "⚡ GitHub Actions: https://github.com/$username/ai_code_reviewer/actions"
    echo ""
    echo "🧪 Next steps:"
    echo "1. Go to your repository on GitHub"
    echo "2. Create a test PR to see the AI reviewer in action"
    echo "3. Check the Actions tab to see the workflow running"
    echo ""
    echo "🔧 The AI reviewer will automatically:"
    echo "   • Install Ollama and AI models"
    echo "   • Analyze your PR code changes"
    echo "   • Post intelligent feedback comments"
    echo "   • Help improve code quality"
    echo ""
    echo "✨ Your AI PR Reviewer is now live!"
else
    echo "❌ Failed to push to GitHub"
    echo "💡 Make sure the repository exists and you have access"
    exit 1
fi
