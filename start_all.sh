#!/bin/bash
# Start both Space Guild backend and frontend in tmux

SESSION_NAME="spaceguild"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is not installed"
    echo "Install with: sudo apt-get install tmux  # or brew install tmux on Mac"
    exit 1
fi

# Kill existing session if it exists
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? == 0 ]; then
    echo "Killing existing session: $SESSION_NAME"
    tmux kill-session -t $SESSION_NAME
fi

echo "========================================"
echo "Starting Space Guild in tmux"
echo "========================================"
echo ""
echo "Creating tmux session: $SESSION_NAME"
echo ""
echo "Layout:"
echo "  - Left pane:  Backend  (http://0.0.0.0:8000)"
echo "  - Right pane: Frontend (http://localhost:8080)"
echo ""
echo "Controls:"
echo "  - Ctrl+B then arrow keys: Switch panes"
echo "  - Ctrl+B then d: Detach session (keeps running)"
echo "  - tmux attach -t $SESSION_NAME: Reattach"
echo "  - Ctrl+C in each pane: Stop servers"
echo "  - tmux kill-session -t $SESSION_NAME: Kill session"
echo ""
echo "========================================"
echo ""

# Create new session with backend in first window
tmux new-session -d -s $SESSION_NAME -n servers

# Split window vertically (side by side)
tmux split-window -h -t $SESSION_NAME:servers

# Left pane: Backend
tmux send-keys -t $SESSION_NAME:servers.0 "./start_backend.sh" C-m

# Right pane: Frontend
tmux send-keys -t $SESSION_NAME:servers.1 "./start_frontend.sh" C-m

# Attach to session
echo "Attaching to tmux session..."
sleep 1
tmux attach-session -t $SESSION_NAME
