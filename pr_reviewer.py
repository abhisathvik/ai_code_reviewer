#!/usr/bin/env python3
"""
AI-Powered GitHub PR Reviewer
Automatically reviews pull requests using Ollama and posts AI-generated feedback.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional
import requests
from github import Github
from github.PullRequest import PullRequest
from github.Commit import Commit


class GitHubPRReviewer:
    def __init__(self, token: str, repo_name: str):
        """Initialize the GitHub PR reviewer."""
        self.github = Github(token)
        self.repo_name = repo_name
        self.repo = self.github.get_repo(repo_name)
        self.ollama_base_url = "http://localhost:11434"
        
    def get_pr_details(self, pr_number: int) -> PullRequest:
        """Fetch pull request details."""
        return self.repo.get_pull(pr_number)
    
    def get_pr_diff(self, pr_number: int) -> str:
        """Get the diff/patch for the pull request."""
        pr = self.get_pr_details(pr_number)
        return pr.diff_url
    
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
    
    def call_ollama(self, prompt: str, model: str = "llama3.2") -> str:
        """Call Ollama API to get AI review."""
        url = f"{self.ollama_base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Error calling Ollama: {e}"
    
    def generate_review_prompt(self, pr_title: str, pr_description: str, changed_files: List[Dict]) -> str:
        """Generate a comprehensive prompt for AI review."""
        prompt = f"""You are an expert code reviewer. Please review this GitHub Pull Request and provide constructive feedback.

Pull Request Title: {pr_title}
Pull Request Description: {pr_description}

Changed Files:
"""
        
        for file_info in changed_files:
            prompt += f"\n--- File: {file_info['filename']} ({file_info['status']}) ---\n"
            prompt += f"Additions: {file_info['additions']}, Deletions: {file_info['deletions']}\n"
            
            if file_info['patch']:
                prompt += f"Patch/Diff:\n{file_info['patch']}\n"
            else:
                prompt += f"Content:\n{file_info['content'][:2000]}...\n" if len(file_info['content']) > 2000 else f"Content:\n{file_info['content']}\n"
        
        prompt += """
Please provide a thorough code review focusing on:

1. **Code Quality**: Is the code clean, readable, and well-structured?
2. **Best Practices**: Does it follow language-specific best practices?
3. **Security**: Are there any potential security vulnerabilities?
4. **Performance**: Are there any performance concerns?
5. **Bugs**: Do you see any potential bugs or issues?
6. **Documentation**: Is the code well-documented?
7. **Testing**: Are there adequate tests or test coverage concerns?

Format your response as follows:
- Start with a brief summary
- Use bullet points for specific issues
- Include line numbers when referencing specific code
- Suggest specific improvements
- Highlight good practices you notice
- Be constructive and helpful

Keep your response concise but comprehensive (aim for 300-500 words).
"""
        
        return prompt
    
    def parse_review_response(self, response: str) -> List[str]:
        """Parse the AI response into individual comments."""
        # Split response into logical sections for separate comments
        lines = response.split('\n')
        comments = []
        current_comment = []
        
        for line in lines:
            if line.strip().startswith(('**', '-', '•', '*')) and current_comment:
                # Start of a new section, save previous comment
                if current_comment:
                    comments.append('\n'.join(current_comment))
                    current_comment = []
            current_comment.append(line)
        
        # Add the last comment
        if current_comment:
            comments.append('\n'.join(current_comment))
        
        # If we only have one comment, split it further if it's too long
        if len(comments) == 1 and len(comments[0]) > 1000:
            # Split by double newlines or major sections
            parts = comments[0].split('\n\n')
            comments = []
            current = []
            for part in parts:
                if len('\n'.join(current + [part])) > 800:
                    if current:
                        comments.append('\n'.join(current))
                        current = [part]
                    else:
                        comments.append(part)
                else:
                    current.append(part)
            if current:
                comments.append('\n'.join(current))
        
        return comments
    
    def post_review_comment(self, pr_number: int, comment: str):
        """Post a review comment to the PR."""
        pr = self.get_pr_details(pr_number)
        try:
            pr.create_issue_comment(comment)
            print(f"Posted comment to PR #{pr_number}")
        except Exception as e:
            print(f"Error posting comment: {e}")
    
    def review_pr(self, pr_number: int):
        """Main method to review a pull request."""
        print(f"Starting review of PR #{pr_number}")
        
        try:
            # Get PR details
            pr = self.get_pr_details(pr_number)
            print(f"Reviewing PR: {pr.title}")
            
            # Get changed files
            changed_files = self.get_changed_files(pr_number)
            print(f"Found {len(changed_files)} changed files")
            
            # Generate AI prompt
            prompt = self.generate_review_prompt(
                pr.title, 
                pr.body or "No description provided", 
                changed_files
            )
            
            print("Calling Ollama for AI review...")
            # Get AI review
            ai_response = self.call_ollama(prompt)
            
            if ai_response.startswith("Error"):
                print(f"Error getting AI review: {ai_response}")
                return
            
            print("Parsing AI response...")
            # Parse and post comments
            comments = self.parse_review_response(ai_response)
            
            # Post a summary comment first
            summary = f"🤖 **AI Code Review**\n\nI've analyzed this PR and here are my findings:\n\n{ai_response[:2000]}..."
            if len(ai_response) > 2000:
                summary += "\n\n*[Review truncated - see additional comments below]*"
            
            self.post_review_comment(pr_number, summary)
            
            # Post additional detailed comments if needed
            if len(comments) > 1:
                for i, comment in enumerate(comments[1:], 1):
                    detailed_comment = f"📝 **Detailed Review Part {i}**\n\n{comment}"
                    self.post_review_comment(pr_number, detailed_comment)
            
            print(f"Review completed for PR #{pr_number}")
            
        except Exception as e:
            error_msg = f"❌ **Review Error**\n\nSorry, I encountered an error while reviewing this PR: {str(e)}"
            self.post_review_comment(pr_number, error_msg)
            print(f"Error reviewing PR: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI-Powered GitHub PR Reviewer")
    parser.add_argument("--pr-number", type=int, required=True, help="Pull request number")
    parser.add_argument("--repo", required=True, help="Repository name (owner/repo)")
    parser.add_argument("--token", help="GitHub token (defaults to GITHUB_TOKEN env var)")
    
    args = parser.parse_args()
    
    # Get GitHub token
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GitHub token not provided. Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)
    
    # Initialize and run reviewer
    reviewer = GitHubPRReviewer(token, args.repo)
    reviewer.review_pr(args.pr_number)


if __name__ == "__main__":
    main()
