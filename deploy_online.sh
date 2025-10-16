#!/bin/bash

# Online Deployment Script for AI PR Reviewer
# Supports multiple platforms: Vercel, Railway, Render

echo "🚀 AI PR Reviewer - Online Deployment"
echo "======================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Run 'git init' first."
    exit 1
fi

echo ""
echo "🌐 Choose your deployment platform:"
echo "1. Vercel (Recommended - Free, Fast, Easy)"
echo "2. Railway (Good for full-stack apps)"
echo "3. Render (Reliable, good free tier)"
echo "4. Deploy all platforms"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        deploy_vercel
        ;;
    2)
        deploy_railway
        ;;
    3)
        deploy_render
        ;;
    4)
        deploy_all
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

deploy_vercel() {
    echo ""
    echo "🎯 Deploying to Vercel..."
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo "📦 Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    echo "🚀 Deploying to Vercel..."
    vercel --prod
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully deployed to Vercel!"
        echo "🌐 Your app will be available at the URL shown above"
        echo ""
        echo "📋 Next steps:"
        echo "1. Visit your deployed URL"
        echo "2. Test the demo review functionality"
        echo "3. Set up GitHub token for real PR reviews"
        echo "4. Share your AI PR Reviewer with others!"
    else
        echo "❌ Vercel deployment failed"
        exit 1
    fi
}

deploy_railway() {
    echo ""
    echo "🎯 Deploying to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        echo "📦 Installing Railway CLI..."
        curl -fsSL https://railway.app/install.sh | sh
    fi
    
    echo "🚀 Deploying to Railway..."
    railway login
    railway link
    railway up
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully deployed to Railway!"
        echo "🌐 Check your Railway dashboard for the URL"
    else
        echo "❌ Railway deployment failed"
        exit 1
    fi
}

deploy_render() {
    echo ""
    echo "🎯 Deploying to Render..."
    
    echo "📋 Manual deployment steps for Render:"
    echo ""
    echo "1. Go to: https://render.com/dashboard"
    echo "2. Click 'New +' → 'Web Service'"
    echo "3. Connect your GitHub repository"
    echo "4. Configure:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python3 web_app.py"
    echo "   - Python Version: 3.11"
    echo "5. Click 'Create Web Service'"
    echo ""
    echo "📁 Render will automatically deploy from your GitHub repository"
    echo "⏱️  Deployment typically takes 3-5 minutes"
    
    read -p "Press Enter when you've completed the Render setup..."
    echo "✅ Render deployment initiated!"
}

deploy_all() {
    echo ""
    echo "🎯 Deploying to all platforms..."
    
    deploy_vercel
    echo ""
    deploy_railway
    echo ""
    deploy_render
}

# Show deployment options
echo ""
echo "🎉 Deployment Options Summary:"
echo "==============================="
echo ""
echo "📍 Vercel (Recommended):"
echo "   • Free tier: 100GB bandwidth/month"
echo "   • Global CDN, automatic HTTPS"
echo "   • Perfect for API endpoints"
echo "   • Easy GitHub integration"
echo ""
echo "🚂 Railway:"
echo "   • Free tier: $5 credit/month"
echo "   • Full-stack app support"
echo "   • Database integration"
echo "   • Real-time deployment"
echo ""
echo "🎨 Render:"
echo "   • Free tier: 750 hours/month"
echo "   • Reliable hosting"
echo "   • Good for production apps"
echo "   • Automatic deployments"
echo ""
echo "💡 Recommendation: Start with Vercel for quick deployment!"
