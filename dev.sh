#!/bin/bash

# Configuration
SESSION_NAME="movie_ticketing_app"
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
VENV_CMD="pipenv run"
REDIS_PORT=6379

# Function to display help
show_help() {
    echo "Usage: ./dev.sh [start|stop]"
    echo "  start : Starts all services in a tiled layout (default)."
    echo "  stop  : Kills the tmux session and all running services."
}

# Function to stop the session
stop_services() {
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Successfully stopped all services in session: $SESSION_NAME"
    else
        echo "No active session found for: $SESSION_NAME"
    fi
}

# Function to start the session
start_services() {
    # Check if tmux is installed
    if ! command -v tmux &> /dev/null; then
        echo "Error: tmux is not installed."
        exit 1
    fi

    # Check if session already exists
    tmux has-session -t "$SESSION_NAME" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Session $SESSION_NAME already exists. Attaching..."
        tmux attach-session -t "$SESSION_NAME"
        return
    fi

    echo "Starting full-stack services in tiled layout: $SESSION_NAME"

    # 1. Create the session and start Django in the first pane
    tmux new-session -d -s "$SESSION_NAME" -n "services"
    tmux send-keys -t "$SESSION_NAME:services" "cd $BACKEND_DIR && $VENV_CMD python manage.py runserver" C-m

    # 2. Split vertically for Frontend
    tmux split-window -v -t "$SESSION_NAME:services"
    tmux send-keys -t "$SESSION_NAME:services" "cd $FRONTEND_DIR && npm run dev" C-m

    # 3. Split horizontally (top right) for Celery
    tmux split-window -h -t "$SESSION_NAME:services.0"
    tmux send-keys -t "$SESSION_NAME:services" "cd $BACKEND_DIR && $VENV_CMD celery -A MovieTicketingProject worker -l info" C-m

    # 4. Split horizontally (bottom right) for Redis/Valkey
    tmux split-window -h -t "$SESSION_NAME:services.2"
    
    # Check if port 6379 is already in use (by Valkey or another Redis)
    if ss -tulpn | grep -q ":$REDIS_PORT"; then
        tmux send-keys -t "$SESSION_NAME:services" "echo 'Port $REDIS_PORT is already in use by another service (e.g. Valkey). Using existing instance.' && redis-cli ping || echo 'Connected to existing service.'" C-m
    else
        tmux send-keys -t "$SESSION_NAME:services" "redis-server" C-m
    fi

    # Optional: Balance the panes
    tmux select-layout -t "$SESSION_NAME:services" tiled

    # Attach to the session
    tmux attach-session -t "$SESSION_NAME"
}

# Main logic
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -z "$1" ]; then
            start_services
        else
            echo "Unknown command: $1"
            show_help
            exit 1
        fi
        ;;
esac
