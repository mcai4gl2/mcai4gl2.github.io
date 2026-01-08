#!/bin/sh
# Debug script for Hugo startup
echo "=== Hugo Debug Script Started ===" | tee /tmp/hugo-debug.log
# Ensure we're in the correct directory
cd /src
echo "Current working directory: $(pwd)" | tee -a /tmp/hugo-debug.log
echo "Current user: $(whoami)" | tee -a /tmp/hugo-debug.log
echo "Hugo version: $(hugo version)" | tee -a /tmp/hugo-debug.log
echo "Python version: $(python3 --version)" | tee -a /tmp/hugo-debug.log
echo "=== Checking if config.toml exists ===" | tee -a /tmp/hugo-debug.log
ls -la config.toml 2>&1 | tee -a /tmp/hugo-debug.log
echo "=== Checking if Hugo is already running ===" | tee -a /tmp/hugo-debug.log
ps aux | grep hugo | grep -v grep | tee -a /tmp/hugo-debug.log
echo "=== Starting Hugo server ===" | tee -a /tmp/hugo-debug.log
echo "Command: hugo server --bind 0.0.0.0 --port 1313 --buildDrafts --buildFuture" | tee -a /tmp/hugo-debug.log
# Start Hugo with detailed logging
hugo server --bind 0.0.0.0 --port 1313 --buildDrafts --buildFuture > /tmp/hugo-server.log 2>&1 &
HUGO_PID=$!
echo "Hugo started with PID: $HUGO_PID" | tee -a /tmp/hugo-debug.log
echo "=== Waiting 3 seconds for Hugo to start ===" | tee -a /tmp/hugo-debug.log
sleep 3
echo "=== Checking if Hugo is running ===" | tee -a /tmp/hugo-debug.log
ps aux | grep $HUGO_PID | grep -v grep | tee -a /tmp/hugo-debug.log
echo "=== Checking if port 1313 is listening ===" | tee -a /tmp/hugo-debug.log
netstat -tlnp 2>/dev/null | grep 1313 || ss -tlnp | grep 1313 | tee -a /tmp/hugo-debug.log
echo "=== Hugo Debug Script Completed ===" | tee -a /tmp/hugo-debug.log
