# GitHub Repository Watcher

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/) ![GitHub Release](https://img.shields.io/github/v/release/thaikolja/github-repository-watcher?style=flat) ![GitHub License](https://img.shields.io/github/license/thaikolja/github-repository-watcher?style=flat)

**Never miss an issue** in one of your many repositories on GitHub. Run this Python script once, and you've **subscribed to all of your repositories**, including those in your organization.

## Features

- Bulk subscribe to all accessible repositories
- Supports personal, organization, and collaborator repositories
- Handles large accounts with pagination
- Simple status output for each repository
- Minimal dependencies, fast setup

## Example Output

<img src="https://github.com/user-attachments/assets/da40c043-fbbc-4737-a200-5a88a18e65f1" alt="Output example" width="300" height="auto" title="Output example" />

## Requirements

- Python `3.6` or newer
- `requests` library (`pip install requests`)
- [GitHub personal access token](https://github.com/settings/tokens) with `repo` scope

## Install & Usage
1. Clone this repository and change into the directory:

   ```bash
   git clone https://github.com/thaikolja/github-repository-watcher.git
   cd github-repository-watcher
   ```

2. Create a virtual Python environment (recommended) and switch into it:

   ```bash
   python3 -m venv venv && source venv/bin/activate
   ```

3. Install the `requests` library:

   ```bash
   pip install requests
   ```

4. Edit the top section of the file `main.py` and set your [GitHub token](https://github.com/settings/tokens):

   ```python
   # ========== ENTER YOUR GITHUB ACCESS TOKEN HERE ==========
   
   # GitHub personal access token for API authentication
   # Replace with your token
   TOKEN: str = "YOUR_TOKEN_HERE"
   
   # ========== DO NOT MODIFY BELOW THIS LINE ================
   ```
1. Run:
   ```bash
   python3 main.py
   ```

## License
MIT

## Authors

* Kolja Nolte (kolja.nolte@gmail.com)
