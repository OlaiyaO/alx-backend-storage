# Web Cache and Tracker

This project caches the HTML content of web pages and tracks how many times each URL is accessed using Redis.

## Features

- **Caching**: Saves the HTML content of a URL for 10 seconds to avoid repeated requests.
- **Tracking**: Counts how many times each URL is accessed.

## Requirements

- Python 3.x
- Redis
- Python packages: `requests`, `redis`

## Setup

1. Install dependencies:
    ```bash
    pip install requests redis
    ```

2. Make sure Redis is installed and running:
    - On macOS (with Homebrew):
      ```bash
      brew install redis
      brew services start redis
      ```
    - On Linux:
      ```bash
      sudo apt-get install redis-server
      sudo systemctl start redis
      ```

## Usage

Use the `get_page(url: str)` function to get the HTML content of a webpage.

Example:

```python
from your_script_name import get_page

html_content = get_page("http://example.com")
print(html_content)
