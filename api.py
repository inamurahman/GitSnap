from github import Github
from datetime import datetime, timedelta, timezone, date
from collections import defaultdict
import os
def get_commits_by_author(repo_owner, repo_name, start_date=None, end_date=None, github_token=None):
    """
    Returns a dictionary of {author: [list of commits]} or None if no commits found
    Args:
        repo_owner (str): Repository owner username
        repo_name (str): Repository name
        start_date (datetime): Optional start date filter (UTC)
        end_date (datetime): Optional end date filter (UTC)
        github_token (str): GitHub personal access token
    Returns:
        dict: {author: [list of commits]} or None if no commits
    """
    # Initialize GitHub connection
    g = Github(github_token) if github_token else Github()
    try:
        # Get repository
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        # Get commits with optional date filtering
        if start_date and end_date:
            commits = repo.get_commits(since=start_date, until=end_date)
        else:
            commits = repo.get_commits()
        # Dictionary to store results
        author_commits = defaultdict(list)
        # Process commits
        for commit in commits:
            changes=[]
            patch=[]
            author = commit.author.login if commit.author else commit.commit.author.name
            full_commit = repo.get_commit(commit.sha)
            for file in full_commit.files:
                changes.append([file.filename,file.additions,file.deletions])
                print(f" - {file.filename}: +{file.additions}/-{file.deletions}")
                if file.patch:
                    patch.append(file.patch)
            commit_data = {
                "sha": commit.sha,
                "message": commit.commit.message,
                "date": commit.commit.author.date.isoformat(),
                "url": commit.html_url,
                "changes":changes,
                "patches":patch
            }
            author_commits[author].append(commit_data)
        return dict(author_commits) if author_commits else None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def get_commits():
    """
    Example function to demonstrate usage of get_commits_by_author.
    This is not necessary for the main functionality but shows how to call it.
    """
    owner = "Hari2k3"
    repo = "Frontend-employeeapp"
    start = datetime.combine(date.today(), datetime.min.time(), tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    token = os.getenv("GITHUB_TOKEN")  # Ensure you set this environment variable
    return get_commits_by_author(owner, repo, start, end, token)
