#!/bin/bash

# If the first argument is 'hugo', run Hugo with proper permissions
if [ "$1" = "hugo" ]; then
    # Ensure directories exist with proper permissions
    mkdir -p /src/public
    chown -R vscode:vscode /src/public /src 2>/dev/null || true
    
    # Switch to vscode user and run Hugo
    exec su - vscode -c "cd /src && hugo $*"
else
    # For python commands, switch to vscode user
    if [ "$1" = "python3" ]; then
        exec su - vscode -c "cd /src && python3 $*"
    elif [ "$1" = "image-optimizer" ]; then
        exec su - vscode -c "cd /src && image-optimizer $*"
    else
        # For other commands, just execute them
        exec "$@"
    fi
fi