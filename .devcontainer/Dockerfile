FROM klakegg/hugo:ext-alpine AS hugo

# Install git and Python for image optimizer
RUN apk add --no-cache \
    git \
    python3 \
    py3-pip \
    python3-dev \
    gcc \
    musl-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    net-tools

# Set the working directory
WORKDIR /src

# Install Python dependencies for image optimizer
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the image optimizer package files
COPY image_optimizer/ ./image_optimizer/
COPY setup.py .
COPY image_optimizer_minimal.py .

# Copy the Hugo scripts
COPY .devcontainer/debug-hugo.sh /usr/local/bin/debug-hugo.sh
COPY .devcontainer/check-hugo.sh /usr/local/bin/check-hugo.sh
RUN chmod +x /usr/local/bin/debug-hugo.sh /usr/local/bin/check-hugo.sh

# Install the image optimizer package
RUN pip3 install -e .

# Create a non-root user
RUN addgroup -g 1000 vscode && \
    adduser -D -s /bin/sh -u 1000 -G vscode vscode

# Change ownership of the workspace
RUN chown -R vscode:vscode /src

# Copy the entrypoint script
COPY .devcontainer/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use the entrypoint script (runs as root)
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command is to run as vscode user
CMD ["/bin/sh"]

# Expose the default Hugo server port
EXPOSE 1313
