#!/bin/bash

# Check status of the Autonomous Lead Generation System

echo "=========================================="
echo "System Status"
echo "=========================================="
echo ""

# Check agent
if [ -f /opt/lead_agent/agent.pid ]; then
    AGENT_PID=$(cat /opt/lead_agent/agent.pid)
    if ps -p $AGENT_PID > /dev/null 2>&1; then
        echo "✓ Agent: Running (PID: $AGENT_PID)"
    else
        echo "✗ Agent: Not running (stale PID file)"
    fi
else
    echo "✗ Agent: Not running"
fi

# Check dashboard
if [ -f /opt/lead_agent/dashboard.pid ]; then
    DASHBOARD_PID=$(cat /opt/lead_agent/dashboard.pid)
    if ps -p $DASHBOARD_PID > /dev/null 2>&1; then
        echo "✓ Dashboard: Running (PID: $DASHBOARD_PID)"
    else
        echo "✗ Dashboard: Not running (stale PID file)"
    fi
else
    echo "✗ Dashboard: Not running"
fi

echo ""
echo "Recent agent activity:"
if [ -f /opt/lead_agent/logs/agent.log ]; then
    tail -n 5 /opt/lead_agent/logs/agent.log
else
    echo "No log file found"
fi

echo ""

