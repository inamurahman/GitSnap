from github import Github
from datetime import datetime, timedelta, timezone
from collections import defaultdict
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
# Example usage
if __name__ == "__main__":
    # Configure these parameters
    token = "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"  # Remove before sharing!
    owner = "Hari2k3"
    repo = "Frontend-employeeapp"
    # Optional date filtering
    start = datetime(2025, 6, 12, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    # Get commits
    result = get_commits_by_author(owner, repo, start, end, token)
    if result:
        # print(result)
        print(f"Found {len(result)} authors")
        for author, commits in result.items():
            print(f"\nAuthor: {author} ({len(commits)} commits)")
            for i, commit in enumerate(commits[:3], 1):  # Print first 3 commits per author
                # print(commit,"\n")
                print(f"  {i}. {commit['message'][:50]}... ({commit['date']}) ({commit['patches']})")
    else:
        print("No commits found")from github import Github
from datetime import datetime, timedelta, timezone
from collections import defaultdict
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
# Example usage
if __name__ == "__main__":
    # Configure these parameters
    token = "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"  # Remove before sharing!
    owner = "Hari2k3"
    repo = "Frontend-employeeapp"
    # Optional date filtering
    start = datetime(2025, 6, 12, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    # Get commits
    result = get_commits_by_author(owner, repo, start, end, token)
    if result:
        # print(result)
        print(f"Found {len(result)} authors")
        for author, commits in result.items():
            print(f"\nAuthor: {author} ({len(commits)} commits)")
            for i, commit in enumerate(commits[:3], 1):  # Print first 3 commits per author
                # print(commit,"\n")
                print(f"  {i}. {commit['message'][:50]}... ({commit['date']}) ({commit['patches']})")
    else:
        print("No commits found")