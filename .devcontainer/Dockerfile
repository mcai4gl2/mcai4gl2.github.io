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
    zlib-dev

# Set the working directory
WORKDIR /src

# Install Python dependencies for image optimizer
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the image optimizer package files
COPY image_optimizer/ ./image_optimizer/
COPY setup.py .
COPY image_optimizer_minimal.py .

# Install the image optimizer package
RUN pip3 install -e .

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