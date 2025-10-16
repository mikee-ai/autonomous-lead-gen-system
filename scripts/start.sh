#!/bin/bash

# Start the Autonomous Lead Generation System

set -e

echo "Starting Autonomous Lead Generation System..."

# Check if config exists
if [ ! -f /opt/lead_agent/config/config.py ]; then
    echo "Error: Configuration file not found!"
    echo "Please copy config.template.py to config.py and fill in your API keys."
    exit 1
fi

# Activate virtual environment
cd /opt/lead_agent
source venv/bin/activate

# Start the agent in the background
echo "Starting lead generation agent..."
nohup python3 src/agent.py > logs/agent.log 2>&1 &
AGENT_PID=$!
echo $AGENT_PID > /opt/lead_agent/agent.pid
echo "✓ Agent started (PID: $AGENT_PID)"

# Start the dashboard
echo "Starting dashboard..."
nohup python3 src/dashboard.py > logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!
echo $DASHBOARD_PID > /opt/lead_agent/dashboard.pid
echo "✓ Dashboard started (PID: $DASHBOARD_PID)"

echo ""
echo "=========================================="
echo "✓ System is running!"
echo "=========================================="
echo ""
echo "Agent PID: $AGENT_PID"
echo "Dashboard PID: $DASHBOARD_PID"
echo ""
echo "View logs:"
echo "  Agent: tail -f /opt/lead_agent/logs/agent.log"
echo "  Dashboard: tail -f /opt/lead_agent/logs/dashboard.log"
echo ""
echo "Access dashboard: http://YOUR_SERVER_IP:5000"
echo ""

