# Clear the terminal
clear

# Terminate previous instances
sudo docker compose down

# Start the server locally
sudo docker compose up -d --build

# Show the logs
sudo docker logs -f berry-picker-tracker-server-web-1
