#!/bin/bash
# Sync Swarm script for Git-based collaboration
echo "Starting synchronization..."
cd /data || { echo "Failed to enter /data directory"; exit 1; }

# Check if it's a git repo
if [ ! -d ".git" ]; then
    echo "Error: .git directory not found in /data"
    exit 1
fi

# Add all changes
git add .

# Commit (only if there are changes)
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
else
    git commit -m "Auto-update from Swarm $(date +'%Y-%m-%d %H:%M:%S')"
    echo "Changes committed."
fi

# Push
git push origin jules/git-sync-swarm || { echo "Git push failed"; exit 1; }
echo "Synchronization complete."
