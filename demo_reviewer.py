#!/usr/bin/env python3
"""
Demo version of the AI PR Reviewer for local testing
This version works without Ollama by using mock AI responses
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional
from github import Github
from github.PullRequest import PullRequest


class DemoPRReviewer:
    def __init__(self, token: str, repo_name: str):
        """Initialize the demo PR reviewer."""
        self.github = Github(token)
        self.repo_name = repo_name
        self.repo = self.github.get_repo(repo_name)
        
    def get_pr_details(self, pr_number: int) -> PullRequest:
        """Fetch pull request details."""
        return self.repo.get_pull(pr_number)
    
    def get_changed_files(self, pr_number: int) -> List[Dict]:
        """Get list of changed files with their content."""
        pr = self.get_pr_details(pr_number)
        files = pr.get_files()
        
        changed_files = []
        for file in files:
            # Get file content from the PR
            try:
                if file.status in ['added', 'modified']:
                    # Get content from the head commit
                    content = self.repo.get_contents(file.filename, ref=pr.head.sha)
                    if isinstance(content, list):
                        # It's a directory, skip
                        continue
                    file_content = content.decoded_content.decode('utf-8')
                else:
                    file_content = "File deleted"
                    
                changed_files.append({
                    'filename': file.filename,
                    'status': file.status,
                    'content': file_content,
                    'patch': file.patch,
                    'additions': file.additions,
                    'deletions': file.deletions
                })
            except Exception as e:
                print(f"Error fetching content for {file.filename}: {e}")
                changed_files.append({
                    'filename': file.filename,
                    'status': file.status,
                    'content': "Could not fetch content",
                    'patch': file.patch,
                    'additions': file.additions,
                    'deletions': file.deletions
                })
        
        return changed_files
    
    def generate_mock_review(self, pr_title: str, pr_description: str, changed_files: List[Dict]) -> str:
        """Generate a mock AI review for demonstration."""
        
        # Analyze the files to create a contextual review
        file_types = set()
        languages = set()
        total_additions = 0
        total_deletions = 0
        
        for file_info in changed_files:
            filename = file_info['filename']
            if '.' in filename:
                ext = filename.split('.')[-1].lower()
                file_types.add(ext)
            
            # Detect programming languages
            if ext in ['py']:
                languages.add('Python')
            elif ext in ['js', 'ts', 'jsx', 'tsx']:
                languages.add('JavaScript/TypeScript')
            elif ext in ['java']:
                languages.add('Java')
            elif ext in ['go']:
                languages.add('Go')
            elif ext in ['rs']:
                languages.add('Rust')
            elif ext in ['cpp', 'c', 'h', 'hpp']:
                languages.add('C/C++')
            
            total_additions += file_info['additions']
            total_deletions += file_info['deletions']
        
        # Generate contextual review
        review = f"""🤖 **AI Code Review** (Demo Mode)

## Summary
I've analyzed this PR: **"{pr_title}"** and here are my findings:

**Changes Overview:**
- 📁 {len(changed_files)} files changed
- ➕ {total_additions} lines added
- ➖ {total_deletions} lines deleted
- 🔤 Languages: {', '.join(languages) if languages else 'Various'}

## 📋 Detailed Analysis

### Files Reviewed:"""

        for file_info in changed_files[:5]:  # Limit to first 5 files
            review += f"\n- **{file_info['filename']}** ({file_info['status']})"
            if file_info['additions'] > 0 or file_info['deletions'] > 0:
                review += f" - {file_info['additions']} additions, {file_info['deletions']} deletions"

        review += f"""

### 🔍 Code Quality Assessment

**Strengths I noticed:**
- ✅ Clean file organization
- ✅ Appropriate use of {', '.join(languages) if languages else 'programming'} conventions
- ✅ Good commit message structure

**Areas for improvement:**
- 🔍 Consider adding unit tests for new functionality
- 📝 Add inline documentation for complex logic
- 🛡️ Review for potential security vulnerabilities
- ⚡ Check for performance optimizations

### 🚨 Potential Issues

**Security Considerations:**
- 🔐 Verify input validation on user inputs
- 🛡️ Check for SQL injection risks in database queries
- 🔑 Ensure sensitive data is properly handled

**Performance Notes:**
- ⚡ Review algorithm complexity for large datasets
- 💾 Check memory usage patterns
- 🔄 Consider caching strategies where appropriate

### 💡 Suggestions

1. **Testing**: Add comprehensive test coverage
2. **Documentation**: Include code comments for complex functions
3. **Error Handling**: Implement robust error handling
4. **Logging**: Add appropriate logging for debugging

---
*This is a demo review. In production, this would be generated by an AI model like Llama3.2 or Mistral running locally with Ollama.*"""

        return review
    
    def post_review_comment(self, pr_number: int, comment: str):
        """Post a review comment to the PR."""
        pr = self.get_pr_details(pr_number)
        try:
            pr.create_issue_comment(comment)
            print(f"✅ Posted comment to PR #{pr_number}")
        except Exception as e:
            print(f"❌ Error posting comment: {e}")
    
    def review_pr(self, pr_number: int, dry_run: bool = False):
        """Main method to review a pull request."""
        print(f"🔍 Starting review of PR #{pr_number}")
        
        try:
            # Get PR details
            pr = self.get_pr_details(pr_number)
            print(f"📋 Reviewing PR: {pr.title}")
            
            # Get changed files
            changed_files = self.get_changed_files(pr_number)
            print(f"📁 Found {len(changed_files)} changed files")
            
            # Generate mock review
            ai_response = self.generate_mock_review(
                pr.title, 
                pr.body or "No description provided", 
                changed_files
            )
            
            if dry_run:
                print("\n" + "="*60)
                print("📝 DRY RUN - Review that would be posted:")
                print("="*60)
                print(ai_response)
                print("="*60)
                return
            
            # Post the review
            self.post_review_comment(pr_number, ai_response)
            print(f"✅ Review completed for PR #{pr_number}")
            
        except Exception as e:
            error_msg = f"❌ **Review Error**\n\nSorry, I encountered an error while reviewing this PR: {str(e)}"
            if not dry_run:
                self.post_review_comment(pr_number, error_msg)
            print(f"❌ Error reviewing PR: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Demo AI-Powered GitHub PR Reviewer")
    parser.add_argument("--pr-number", type=int, required=True, help="Pull request number")
    parser.add_argument("--repo", required=True, help="Repository name (owner/repo)")
    parser.add_argument("--token", help="GitHub token (defaults to GITHUB_TOKEN env var)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be posted without actually posting")
    
    args = parser.parse_args()
    
    # Get GitHub token
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GitHub token not provided. Set GITHUB_TOKEN environment variable or use --token")
        print("💡 Get a token from: https://github.com/settings/tokens")
        sys.exit(1)
    
    # Initialize and run reviewer
    reviewer = DemoPRReviewer(token, args.repo)
    reviewer.review_pr(args.pr_number, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
