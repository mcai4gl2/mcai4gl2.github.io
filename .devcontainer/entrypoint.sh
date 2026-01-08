#!/bin/bash

# If the first argument is 'hugo', run Hugo with proper permissions
if [ "$1" = "hugo" ]; then
    # Ensure the public directory exists with proper permissions
    mkdir -p /src/public
    chown -R vscode:vscode /src/public 2>/dev/null || true
    
    # Run Hugo as the vscode user
    exec sudo -u vscode hugo "$@"
else
    # For other commands, just execute them
    exec "$@"
fi