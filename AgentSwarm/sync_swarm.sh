#!/bin/bash
# Sync Swarm script for Git-based collaboration (v2)
echo "Starting synchronization..."
cd /data || { echo "Failed to enter /data directory"; exit 1; }

# Check if it's a git repo
if [ ! -d ".git" ]; then
    echo "Error: .git directory not found in /data"
    exit 1
fi

# Set Identity (if needed)
git config user.name "MemoirSwarm"
git config user.email "swarm@headless.local"

# Add all changes
git add .

# Check for JULES_CONSULT.md and add specifically
if [ -f "JULES_CONSULT.md" ]; then
    echo "Urgent: JULES_CONSULT.md detected. Adding to commit."
    git add JULES_CONSULT.md
fi

# Commit
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
else
    COMMIT_MSG="Auto-update from Swarm $(date +'%Y-%m-%d %H:%M:%S')"
    if [ -f "JULES_CONSULT.md" ]; then
        COMMIT_MSG="URGENT: JULES_CONSULT Report - $COMMIT_MSG"
    fi
    git commit -m "$COMMIT_MSG"
    echo "Changes committed."
fi

# Push to current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push origin "$CURRENT_BRANCH" || { echo "Git push failed"; exit 1; }

# Cleanup JULES_CONSULT after successful push to prevent repeat reports
if [ -f "JULES_CONSULT.md" ]; then
    rm JULES_CONSULT.md
    git add JULES_CONSULT.md
    git commit -m "Cleanup: JULES_CONSULT processed"
    git push origin "$CURRENT_BRANCH"
fi

echo "Synchronization complete."
