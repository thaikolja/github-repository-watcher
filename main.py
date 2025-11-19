#!/usr/bin/env python3

"""
Watch all GitHub repositories (personal + organizations).

This script fetches all repositories accessible to the authenticated user,
including personal repositories and those from organizations where the user
is a member or collaborator. It then subscribes (watches) each repository
to receive notifications for updates.

Requirements:
- A GitHub personal access token with 'repo' scope.
- The 'requests' library installed (`pip install requests`).

Usage:
    Replace "YOUR_TOKEN_HERE" in the code with your GitHub personal access token.
    Run: python main.py

Note:
    Be cautious with the token; do not commit it to version control.
    Generate a token at: https://github.com/settings/tokens
"""

# For system exit and HTTP requests
import sys

# HTTP requests library
import requests

# For type hinting
from typing import Any

# ========== ENTER YOUR GITHUB ACCESS TOKEN HERE ==========

# GitHub personal access token for API authentication
# Replace with your token
TOKEN: str = "YOUR_TOKEN_HERE"

# ========== DO NOT MODIFY BELOW THIS LINE ================

# Check if token is set (failsafe, though token is hardcoded here)
if TOKEN == "YOUR_TOKEN_HERE":
	print("Error: Set GITHUB_TOKEN")
	print("Generate at: https://github.com/settings/tokens")
	sys.exit(1)

# Headers for GitHub API requests, including authorization and API version
HEADERS: dict[str, str] = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}


def watch_repo(owner: str, repo: str) -> None:
	"""
	Subscribe to a repository to receive notifications.

	This function sends a PUT request to the GitHub API to watch the specified
	repository. Watching means subscribing to notifications for issues, pulls,
	releases, etc.

	Args:
			owner (str): The GitHub username or organization name owning the repo.
			repo (str): The name of the repository.

	Raises:
			Exception: If the API request fails (e.g., network issues, invalid token).
	"""
	# Build the subscription URL for the repository
	url: str = f"https://api.github.com/repos/{owner}/{repo}/subscription"

	# Try to watch the repo
	try:
		resp = requests.put(
			url,
			json={"subscribed": True, "ignored": False},
			headers=HEADERS,
			timeout=10
		)

		# Check response status: 200 means success
		status: str = "✅" if resp.status_code == 200 else f"⚠️ {resp.status_code}"

		# Print result with status emoji
		print(f"{status} {owner}/{repo}")

	# Handle exceptions (e.g., network errors)
	except Exception as e:
		print(f"❌ {owner}/{repo}: {e}")


def main() -> None:
	"""
	Fetch and watch all accessible repositories.

	This function paginates through the user's repositories using the GitHub API,
	fetching up to 100 repos per page. For each repo, it calls watch_repo to
	subscribe. It handles pagination, API errors, and user interrupts.

	The affiliation parameter includes owner, collaborator, and organization_member
	to cover personal and org repos. Visibility is set to 'all' for public and private.

	Prints progress and a summary at the end.
	"""
	# Print start message
	print("Fetching repositories...\n")

	# Initialize page counter for pagination
	page: int = 1

	# Initialize total counter for processed repos
	total: int = 0

	# Loop through pages until no more repos
	while True:
		# Try to fetch repos for the current page
		try:
			# Set query parameters: page number, repos per page, affiliation, visibility
			params: dict[str, Any] = {
				"page": page,
				"per_page": 100,
				"affiliation": "owner,collaborator,organization_member",
				"visibility": "all"
			}

			# Make API request to get user repos
			resp = requests.get(
				"https://api.github.com/user/repos",
				headers=HEADERS,
				params=params,
				timeout=10
			)

			# Check for API errors (non-200 status)
			if resp.status_code != 200:
				print(f"API Error: {resp.status_code}")
				break

			# Parse JSON response into list of repo dicts
			repos: list[dict[str, Any]] = resp.json()

			# Check if no more repos (empty list)
			if not repos:
				break

			# Loop through repos on this page
			for repo in repos:
				# Watch each repo using owner login and repo name
				watch_repo(repo["owner"]["login"], repo["name"])

				# Increment total processed count
				total += 1

			# Go to next page
			page += 1

		# Handle keyboard interrupt (Ctrl+C) to stop gracefully
		except KeyboardInterrupt:
			print("\nStopped by user")
			break

		# Handle other exceptions (e.g., network issues)
		except Exception as e:
			print(f"Error: {e}")
			break

	# Print completion message with total processed
	if total > 1:
		print(f"\nDone! You're now watching {total} repositories.")
	elif total == 1:
		print(f"\nDone! You're now watching 1 repository.")


# Run main if script is executed directly
if __name__ == "__main__":
	main()
