# Berry Picker Tracker back-end server

## Installation

### Requirements

- `python3`
- `pip3`

### Set-up

```bash
python3 -m venv .venv && \            # Create a virtual environment in `./.venv`
source ./.venv/bin/activate && \      # Activate the virtual environment
pip3 install -r requirements.txt && \ # Install dependencies — see `./requirements.txt` for more info
pre-commit install && \               # Install the pre-commit hook
pre-commit autoupdate                 # Update the pre-commit hooks
```

### Updating dependencies

```bash
pip freeze > requirements.txt
```

### Running

Either run `uvicorn --app-dir=src main:app --reload` manually or start the "Run the app" task in VSCode

### Testing

Run tests

```
pytest
```
If you stumble upon "ModuleNotFoundError", run

```
python3 -m pytest
```
