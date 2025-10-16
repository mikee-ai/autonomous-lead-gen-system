#!/bin/bash

# Stop the Autonomous Lead Generation System

echo "Stopping Autonomous Lead Generation System..."

# Stop agent
if [ -f /opt/lead_agent/agent.pid ]; then
    AGENT_PID=$(cat /opt/lead_agent/agent.pid)
    if ps -p $AGENT_PID > /dev/null 2>&1; then
        kill $AGENT_PID
        echo "✓ Agent stopped (PID: $AGENT_PID)"
    else
        echo "⚠ Agent not running"
    fi
    rm /opt/lead_agent/agent.pid
else
    echo "⚠ Agent PID file not found"
fi

# Stop dashboard
if [ -f /opt/lead_agent/dashboard.pid ]; then
    DASHBOARD_PID=$(cat /opt/lead_agent/dashboard.pid)
    if ps -p $DASHBOARD_PID > /dev/null 2>&1; then
        kill $DASHBOARD_PID
        echo "✓ Dashboard stopped (PID: $DASHBOARD_PID)"
    else
        echo "⚠ Dashboard not running"
    fi
    rm /opt/lead_agent/dashboard.pid
else
    echo "⚠ Dashboard PID file not found"
fi

echo ""
echo "System stopped."

