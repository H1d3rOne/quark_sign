---
name: "github"
description: "Manages GitHub repositories via API (pull, push, delete, add, etc.). Invoke when user asks for GitHub operations, repository management, or Git/GitHub commands."
---

# GitHub Manager

This skill provides comprehensive GitHub repository management capabilities using GitHub API and Git commands.

## Default Configuration

This skill uses the following default GitHub credentials:
- **Username**: H1d3rOne
- **Token**: YOUR_GITHUB_TOKEN_HERE

### Setting Up Default Credentials

```bash
# Set default GitHub token
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE

# Configure Git with default user
git config --global user.name "H1d3rOne"

# Configure GitHub CLI with default token
echo "YOUR_GITHUB_TOKEN_HERE" | gh auth login --with-token
```

All operations will automatically use these credentials unless explicitly overridden.

## When to Use This Skill

Invoke this skill when user asks for:
- GitHub repository operations (create, delete, clone, fork)
- Git operations (pull, push, commit, add, branch, merge)
- GitHub API interactions (issues, PRs, releases, webhooks)
- Repository management and configuration
- GitHub authentication and setup

## Prerequisites

**Default credentials are pre-configured** (see Default Configuration section above).

### Optional: Override Default Credentials

If you need to use different credentials:

1. **GitHub Personal Access Token**:
   - Generate at: https://github.com/settings/tokens
   - Required scopes: `repo`, `workflow`, `admin:org`, `user`
   - Set as environment variable: `GITHUB_TOKEN`

2. **Git Configuration**:
   - Git must be installed and configured
   - User name and email should be set

3. **SSH Key (Optional but recommended)**:
   - For SSH-based authentication
   - Add to GitHub account: https://github.com/settings/keys

## Available Operations

### Repository Operations

#### Create Repository
```bash
# Create new repository
gh repo create <repo-name> --public --description "Description"
gh repo create <repo-name> --private --description "Description"

# Create with README and .gitignore
gh repo create <repo-name> --public --readme --gitignore Python
```

#### Clone Repository
```bash
# Clone via HTTPS (using default user H1d3rOne)
git clone https://github.com/H1d3rOne/repo.git

# Clone via SSH (using default user H1d3rOne)
git clone git@github.com:H1d3rOne/repo.git

# Clone specific branch
git clone -b <branch-name> https://github.com/H1d3rOne/repo.git
```

#### Delete Repository
```bash
gh repo delete <repo-name>
```

#### Fork Repository
```bash
gh repo fork <source-repo>
```

### Git Operations

#### Basic Git Workflow
```bash
# Initialize repository
git init

# Add files
git add .
git add <file-name>
git add *.py

# Commit changes
git commit -m "Commit message"
git commit -am "Commit message"  # Add and commit tracked files

# Push to remote
git push origin <branch-name>
git push -u origin <branch-name>  # Set upstream

# Pull from remote
git pull origin <branch-name>
git pull --rebase origin <branch-name>
```

#### Branch Management
```bash
# Create and switch branch
git checkout -b <branch-name>
git switch -c <branch-name>

# List branches
git branch -a

# Delete branch
git branch -d <branch-name>
git push origin --delete <branch-name>  # Delete remote branch

# Merge branch
git merge <branch-name>
```

#### Remote Management
```bash
# Add remote
git remote add origin <url>

# List remotes
git remote -v

# Change remote URL
git remote set-url origin <new-url>
```

### GitHub API Operations

#### Issues Management
```bash
# List issues
gh issue list

# Create issue
gh issue create --title "Issue title" --body "Issue description"

# View issue
gh issue view <issue-number>

# Close issue
gh issue close <issue-number>
```

#### Pull Requests
```bash
# Create PR
gh pr create --title "PR title" --body "PR description" --base main

# List PRs
gh pr list

# View PR
gh pr view <pr-number>

# Merge PR
gh pr merge <pr-number> --merge
```

#### Releases
```bash
# Create release
gh release create <tag-name> --title "Release title" --notes "Release notes"

# List releases
gh release list

# View release
gh release view <tag-name>
```

#### Webhooks
```bash
# List webhooks
gh api repos/:owner/:repo/hooks

# Create webhook
gh api repos/:owner/:repo/hooks -f name="web" -f active=true -f config.url="<webhook-url>"
```

### Advanced Operations

#### Git Configuration
```bash
# Set global config
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set local config
git config user.name "Your Name"
git config user.email "your.email@example.com"

# View config
git config --list
```

#### Git Status and History
```bash
# View status
git status

# View log
git log --oneline
git log --graph --all

# View diff
git diff
git diff <file-name>
git diff <branch1> <branch2>
```

#### Git Stash
```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply stash
git stash apply
git stash pop

# Drop stash
git stash drop
```

#### Git Reset and Revert
```bash
# Reset to commit
git reset --soft <commit-hash>  # Keep changes staged
git reset --mixed <commit-hash>  # Keep changes unstaged
git reset --hard <commit-hash>  # Discard changes

# Revert commit
git revert <commit-hash>
```

### GitHub CLI Configuration

```bash
# Authenticate with GitHub
gh auth login

# Check authentication status
gh auth status

# Logout
gh auth logout

# Set default repository
gh repo set-default <owner/repo>
```

## Common Workflows

### Initial Repository Setup
```bash
# 1. Create repository on GitHub (using default user H1d3rOne)
gh repo create my-project --public --readme

# 2. Clone locally
git clone git@github.com:H1d3rOne/my-project.git
cd my-project

# 3. Add files and commit
git add .
git commit -m "Initial commit"

# 4. Push to GitHub
git push -u origin main
```

### Feature Branch Workflow
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Push to remote
git push -u origin feature/new-feature

# 4. Create pull request
gh pr create --title "Add new feature" --body "Description of changes"
```

### Release Workflow
```bash
# 1. Tag release
git tag -a v1.0.0 -m "Release version 1.0.0"

# 2. Push tags
git push origin v1.0.0

# 3. Create GitHub release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"
```

## Error Handling

### Authentication Issues
```bash
# If you get authentication errors:
gh auth login  # Re-authenticate
export GITHUB_TOKEN=your_token  # Set token
```

### Permission Issues
```bash
# If you get permission denied:
chmod +x /path/to/adb  # Fix permissions
sudo chmod -R 755 /path/to/directory
```

### Merge Conflicts
```bash
# Resolve conflicts:
git status  # Check conflicts
# Edit conflicted files
git add <resolved-files>
git commit  # Complete merge
```

## Best Practices

1. **Always pull before pushing** to avoid conflicts
2. **Use meaningful commit messages** following conventional commits
3. **Create feature branches** for new features
4. **Write descriptive PR descriptions** with context
5. **Use tags for releases** to mark stable versions
6. **Keep sensitive data out of repositories** (use .gitignore)
7. **Review changes before committing** using `git diff`
8. **Use .gitignore** to exclude unnecessary files

## Environment Variables

- `GITHUB_TOKEN`: Personal access token for API authentication (default: YOUR_GITHUB_TOKEN_HERE)
- `GIT_AUTHOR_NAME`: Git author name (default: H1d3rOne)
- `GIT_AUTHOR_EMAIL`: Git author email
- `GIT_COMMITTER_NAME`: Git committer name (default: H1d3rOne)
- `GIT_COMMITTER_EMAIL`: Git committer email

## Notes

- This skill supports both GitHub CLI (`gh`) and Git commands
- For API operations, ensure `gh` is installed and authenticated
- For Git operations, ensure Git is properly configured
- Some operations may require additional permissions or scopes
- Always backup important data before destructive operations (delete, reset, etc.)