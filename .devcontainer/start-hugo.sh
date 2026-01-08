#!/bin/sh
cd /src
# Start Hugo server in background
hugo server --bind 0.0.0.0 --port 1313 --buildDrafts --buildFuture > /dev/null 2>&1 &
