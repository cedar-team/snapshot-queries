#!/usr/bin/env bash

# check if dependencies are installed
# - gh
# - jq
# - python

# Get the last release info:
PREV_VERSION="$(cat release.json | jq '.version')"
PREV_RELEASE_DATE="$(cat release.json | jq '.when')"
export PREV_RELEASE_DATE="2022-04-25T04:00:00+00:00"

PRs=$(gh pr list --state merged --json=number,title,url,labels,mergeCommit --base main --search "closed:>$PREV_RELEASE_DATE")

# Features
FEATURES=$(echo $PRs | jq -c '[.[] | select(.labels[].name == "enhancement")]')
FIXES=$(echo $PRs | jq -c '[.[] | select(.labels[].name == "fix")]')

MAJOR=false
MINOR=false
PATCH=false

CHANGELOG=""
if [ -n "$FEATURES" ]; then
    MINOR=true

    CHANGES=$(echo $FEATURES | python -c "import json; print('\n'.join(f'- {pr[\"title\"]} [#{pr[\"number\"]}]({pr[\"url\"]})' for pr in json.loads(input())))")
    CHANGELOG="${CHANGELOG}\n### 🚀 Features\n"
    CHANGELOG="${CHANGELOG}\n${CHANGES}\n"
fi

if [ -n "$FIXES" ]; then
    PATCH=true

    CHANGES=$(echo $FIXES | python -c "import json; print('\n'.join(f'- {pr[\"title\"]} [#{pr[\"number\"]}]({pr[\"url\"]})' for pr in json.loads(input())))")
    CHANGELOG="${CHANGELOG}\n### 🐛 Bug Fixes\n"
    CHANGELOG="${CHANGELOG}\n${CHANGES}\n"
fi

if [ "$MINOR" == "true" ]; then
    VERSION=$(python -c "a, b, c=$PREV_VERSION.split('.'); b = int(b) + 1; print(f'{a}.{b}.{c}')")
elif [ "$PATCH" == "true" ]; then
    VERSION=$(python -c "a, b, c=$PREV_VERSION.split('.'); c = int(c) + 1; print(f'{a}.{b}.{c}')")
fi

CHANGELOG="## v$VERSION ($(TZ=America/New_York date +'%Y-%m-%d'))\n${CHANGELOG}"

printf "\n$CHANGELOG\n"

RELEASE_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
RELEASE_COMMIT=$(jq -r '.[0].mergeCommit.oid')

# Create tag
git fetch origin main
git checkout -b release-$VERSION-$RELEASE_COMMIT origin/main
gh pr create --title "Release v$VERSION $RELEASE_COMMIT" --body "Created by $(git config user.name)"
gh pr merge --admin release-$VERSION-$RELEASE_COMMIT
git tag v$VERSION
git push origin --tags

RELEASE_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
RELEASE_COMMIT=$(jq -r '.[0].mergeCommit.oid')
