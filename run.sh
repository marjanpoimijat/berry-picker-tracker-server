# Clear the terminal
clear

# Start the database
postgres &

# Activate the virtual environment
source .venv/bin/activate

# Start the server
uvicorn --app-dir=src main:app --reload
