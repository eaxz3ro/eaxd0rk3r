## Features

- Search multiple websites using predefined Google Dork queries.
- Run Google Dork queries with options to select specific queries or ranges of queries.
- Supports both single URL input and bulk URL input from a file.
- Handles API quota limits (status code 429) and gracefully exits when the quota is reached.
- Saves results to a JSON file.

## Prerequisites

- Python 3.x
- `requests` library (for making HTTP requests)
- Google Custom Search API Key and Search Engine ID (CSE ID)

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/eaxz3ro/eaxd0rk3r.git
    cd eaxd0rk3r
    ```

2. **Get Google API Key and Search Engine ID:**

   Follow the instructions in the [Google Custom Search Engine Documentation](https://developers.google.com/custom-search/v1/overview) to obtain an API key and create a Custom Search Engine (CSE).
   Replace the placeholder API key and CSE ID in the script:
      ```python
      api_key = 'YOUR-API-KEY-HERE'
      search_engine_id = 'YOUR-CSE-ID-HERE'
      ```

## Usage

Run the script via the command line with the following options:

```bash
python3 eaxd0rk3r.py [-u URL] [-f FILE] [-o OUTPUT]
