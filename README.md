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
pre-commit autoupdate && \            # Update the pre-commit hooks
touch .env                            # For environmental variables
```


Instructions to connect to database locally [HERE](https://github.com/hy-ohtu-syksy-22-bpt/berry-picker-tracker-docs/blob/main/db_locally_instructions.md)


### Updating dependencies

```bash
pip3 freeze > requirements.txt
```

### Running

Either start the "Run the app" task in VSCode or run

```bash
uvicorn --app-dir=src main:app --reload
```

### Testing

Run tests

```bash
pytest
```

If you stumble upon `ModuleNotFoundError`, run

```bash
python3 -m pytest
```

## Licenses

[Licenses](https://github.com/hy-ohtu-syksy-22-bpt/berry-picker-tracker-server/tree/main/licenses)
