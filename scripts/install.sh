#!/bin/bash

# Autonomous Lead Generation System - Installation Script
# This script sets up the system on a fresh VPS

set -e  # Exit on error

echo "=========================================="
echo "Autonomous Lead Generation System"
echo "Installation Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "[1/8] Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

# Install Python 3 and pip
echo "[2/8] Installing Python 3 and pip..."
apt-get install -y python3 python3-pip python3-venv -qq

# Install system dependencies
echo "[3/8] Installing system dependencies..."
apt-get install -y git curl wget nginx certbot python3-certbot-nginx -qq

# Create application directory
echo "[4/8] Creating application directory..."
mkdir -p /opt/lead_agent
mkdir -p /opt/lead_agent/logs
mkdir -p /opt/lead_agent/data

# Copy application files
echo "[5/8] Copying application files..."
cp -r /root/lead_gen_package/* /opt/lead_agent/

# Create Python virtual environment
echo "[6/8] Setting up Python virtual environment..."
cd /opt/lead_agent
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "[7/8] Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Set up configuration
echo "[8/8] Setting up configuration..."
if [ ! -f /opt/lead_agent/config/config.py ]; then
    cp /opt/lead_agent/config/config.template.py /opt/lead_agent/config/config.py
    echo ""
    echo "⚠️  IMPORTANT: Edit /opt/lead_agent/config/config.py with your API keys!"
    echo ""
fi

# Set permissions
chown -R root:root /opt/lead_agent
chmod +x /opt/lead_agent/scripts/*.sh

echo ""
echo "=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit your configuration: nano /opt/lead_agent/config/config.py"
echo "2. Run the setup wizard: /opt/lead_agent/scripts/setup.sh"
echo "3. Start the agent: /opt/lead_agent/scripts/start.sh"
echo ""

