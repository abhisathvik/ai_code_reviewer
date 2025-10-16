#!/usr/bin/env python3
"""
Setup and test script for the AI PR Reviewer
"""

import os
import sys
from github import Github


def check_github_token():
    """Check if GitHub token is available and valid."""
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("\n🔧 To get a GitHub token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Give it a name like 'AI PR Reviewer'")
        print("4. Select scopes: 'repo' (for private repos) or 'public_repo' (for public repos)")
        print("5. Copy the token")
        print("6. Run: export GITHUB_TOKEN=your_token_here")
        print("\n💡 For this demo, you can also use: --token YOUR_TOKEN when running scripts")
        return False
    
    try:
        github = Github(token)
        user = github.get_user()
        print(f"✅ GitHub connection successful!")
        print(f"👤 Connected as: {user.login}")
        print(f"📧 Email: {user.email or 'Not public'}")
        return True
    except Exception as e:
        print(f"❌ GitHub connection failed: {e}")
        print("💡 Check your token permissions and try again")
        return False


def test_repository_access(repo_name):
    """Test access to a specific repository."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return False
    
    try:
        github = Github(token)
        repo = github.get_repo(repo_name)
        print(f"✅ Repository access successful!")
        print(f"📁 Repository: {repo.full_name}")
        print(f"🔓 Private: {repo.private}")
        print(f"⭐ Stars: {repo.stargazers_count}")
        return True
    except Exception as e:
        print(f"❌ Repository access failed: {e}")
        return False


def list_recent_prs(repo_name, limit=5):
    """List recent pull requests."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return
    
    try:
        github = Github(token)
        repo = github.get_repo(repo_name)
        prs = repo.get_pulls(state='all', sort='created', direction='desc')[:limit]
        
        print(f"\n📋 Recent Pull Requests in {repo_name}:")
        print("-" * 50)
        
        for i, pr in enumerate(prs, 1):
            print(f"{i}. #{pr.number}: {pr.title}")
            print(f"   👤 Author: {pr.user.login}")
            print(f"   📅 Created: {pr.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   🔄 State: {pr.state}")
            print()
        
        return prs
    except Exception as e:
        print(f"❌ Error fetching PRs: {e}")
        return []


def main():
    """Main setup and test function."""
    print("🚀 AI PR Reviewer Setup & Test")
    print("=" * 40)
    
    # Check GitHub connection
    if not check_github_token():
        print("\n⚠️  Please set up your GitHub token first")
        return
    
    # Get repository name
    print("\n📁 Enter repository details for testing:")
    repo_name = input("Repository name (owner/repo, e.g., 'microsoft/vscode'): ").strip()
    
    if not repo_name:
        print("❌ Repository name is required")
        return
    
    # Test repository access
    if not test_repository_access(repo_name):
        print(f"\n⚠️  Cannot access {repo_name}")
        print("💡 Make sure the repository exists and your token has access")
        return
    
    # List recent PRs
    prs = list_recent_prs(repo_name)
    
    if prs:
        print("🧪 Ready to test! You can now:")
        print("1. Run the demo reviewer on an existing PR:")
        print(f"   python demo_reviewer.py --pr-number {prs[0].number} --repo {repo_name} --dry-run")
        print("\n2. Start the API server:")
        print("   python api_server.py")
        print("\n3. Create a test PR in your repository")
        
        # Ask if user wants to test
        test_now = input("\n🤔 Would you like to test the demo reviewer now? (y/n): ").strip().lower()
        if test_now in ['y', 'yes']:
            try:
                pr_number = int(input(f"Enter PR number (or press Enter for #{prs[0].number}): ").strip() or prs[0].number)
                
                print(f"\n🧪 Testing demo reviewer on PR #{pr_number}...")
                os.system(f"python demo_reviewer.py --pr-number {pr_number} --repo {repo_name} --dry-run")
                
            except ValueError:
                print("❌ Invalid PR number")
            except KeyboardInterrupt:
                print("\n⏹️  Test cancelled")
    else:
        print("❌ No PRs found or error accessing repository")


if __name__ == "__main__":
    main()
