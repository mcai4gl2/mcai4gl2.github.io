#!/bin/bash

# Get the command
cmd="$1"

# If no command provided, run shell
if [ -z "$cmd" ]; then
    exec /bin/sh
fi

# Handle different commands
case "$cmd" in
    "hugo")
        # Ensure directories exist with proper permissions
        mkdir -p /src/public
        chown -R vscode:vscode /src/public /src 2>/dev/null || true
        
        # Shift to remove the first argument (hugo)
        shift
        
        # Run Hugo directly as root with explicit paths
        exec hugo --source=/src --destination=/src/public $*
        ;;
    "python3")
        # Shift to remove the first argument (python3)
        shift
        
        # Switch to vscode user and run Python with remaining arguments
        exec su - vscode -c "cd /src && python3 $*"
        ;;
    "image-optimizer")
        # Shift to remove the first argument (image-optimizer)
        shift
        
        # Switch to vscode user and run image-optimizer with remaining arguments
        exec su - vscode -c "cd /src && image-optimizer $*"
        ;;
    *)
        # For other commands, just execute them
        exec "$@"
        ;;
esac