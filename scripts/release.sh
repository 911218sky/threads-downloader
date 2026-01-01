#!/bin/bash

echo "========================================"
echo "  Threads Downloader - Release Script"
echo "========================================"
echo

# Get latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [ -z "$LATEST_TAG" ]; then
    LATEST_TAG="v0.0.0"
    echo "No existing tags found. Starting from v0.0.0"
else
    echo "Current version: $LATEST_TAG"
fi

# Parse version numbers
VERSION=${LATEST_TAG#v}
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Calculate new versions
NEW_MAJOR=$((MAJOR + 1))
NEW_MINOR=$((MINOR + 1))
NEW_PATCH=$((PATCH + 1))

echo
echo "Select version bump type:"
echo "  [1] Patch  $MAJOR.$MINOR.$NEW_PATCH  (bug fixes)"
echo "  [2] Minor  $MAJOR.$NEW_MINOR.0  (new features)"
echo "  [3] Major  $NEW_MAJOR.0.0  (breaking changes)"
echo "  [4] Custom version"
echo "  [5] Cancel"
echo

read -p "Enter choice (1-5): " CHOICE

case $CHOICE in
    1) NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH" ;;
    2) NEW_VERSION="$MAJOR.$NEW_MINOR.0" ;;
    3) NEW_VERSION="$NEW_MAJOR.0.0" ;;
    4) read -p "Enter custom version (e.g., 1.2.3): " NEW_VERSION ;;
    *) echo "Cancelled."; exit 0 ;;
esac

echo
echo "New version: v$NEW_VERSION"
echo

read -p "Confirm release v$NEW_VERSION? (y/n): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Update version in pyproject.toml
echo "Updating pyproject.toml..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
else
    sed -i "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
fi

# Git operations
echo
echo "Committing changes..."
git add -A
git commit -m "chore: bump version to v$NEW_VERSION"

echo "Creating tag v$NEW_VERSION..."
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo "Pushing to remote..."
git push origin main
git push origin "v$NEW_VERSION"

echo
echo "========================================"
echo "  Release v$NEW_VERSION pushed!"
echo "  GitHub Actions will build binaries."
echo "========================================"
