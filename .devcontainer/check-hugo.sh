#!/bin/sh
# Script to check Hugo status
echo "=== Hugo Status Check ==="
echo "Time: $(date)"
echo "=== Hugo processes ==="
ps aux | grep hugo | grep -v grep || echo "No Hugo processes found"
echo "=== Port 1313 status ==="
netstat -tlnp 2>/dev/null | grep 1313 || ss -tlnp 2>/dev/null | grep 1313 || echo "Port 1313 not listening"
echo "=== Recent Hugo logs ==="
if [ -f /tmp/hugo-server.log ]; then
    echo "Last 10 lines of Hugo server log:"
    tail -10 /tmp/hugo-server.log
else
    echo "No Hugo server log found"
fi
echo "=== End of Status Check ==="
