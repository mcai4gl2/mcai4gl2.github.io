FROM klakegg/hugo:ext-alpine AS hugo

# Install git for submodule management
RUN apk add --no-cache git

# Set the working directory
WORKDIR /src

# Create a non-root user
RUN addgroup -g 1000 vscode && \
    adduser -D -s /bin/sh -u 1000 -G vscode vscode

# Change ownership of the workspace
RUN chown -R vscode:vscode /src

# Switch to the non-root user
USER vscode

# Expose the default Hugo server port
EXPOSE 1313

# Set the command to start the Hugo server
CMD ["hugo", "server", "--bind", "0.0.0.0", "--port", "1313"]