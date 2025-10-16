#!/bin/bash

# Setup wizard for Autonomous Lead Generation System

echo "=========================================="
echo "Autonomous Lead Generation System"
echo "Setup Wizard"
echo "=========================================="
echo ""

# Check if config exists
if [ ! -f /opt/lead_agent/config/config.py ]; then
    echo "Error: Configuration file not found!"
    echo "Please run install.sh first."
    exit 1
fi

# Setup systemd services
echo "[1/3] Setting up systemd services..."
cp /opt/lead_agent/scripts/lead-agent.service /etc/systemd/system/
cp /opt/lead_agent/scripts/lead-dashboard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable lead-agent.service
systemctl enable lead-dashboard.service
echo "✓ Services configured to start on boot"

# Setup nginx (optional)
echo ""
read -p "[2/3] Do you want to setup nginx reverse proxy for the dashboard? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your domain name (e.g., dashboard.yourdomain.com): " DOMAIN
    
    cat > /etc/nginx/sites-available/lead-dashboard << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    ln -sf /etc/nginx/sites-available/lead-dashboard /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
    echo "✓ Nginx configured for $DOMAIN"
    
    read -p "Do you want to setup SSL with Let's Encrypt? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        certbot --nginx -d $DOMAIN
        echo "✓ SSL certificate installed"
    fi
fi

# Final instructions
echo ""
echo "[3/3] Setup complete!"
echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Your system is ready to use!"
echo ""
echo "Commands:"
echo "  Start:  systemctl start lead-agent lead-dashboard"
echo "  Stop:   systemctl stop lead-agent lead-dashboard"
echo "  Status: systemctl status lead-agent lead-dashboard"
echo "  Logs:   journalctl -u lead-agent -f"
echo ""
echo "Or use the convenience scripts:"
echo "  /opt/lead_agent/scripts/start.sh"
echo "  /opt/lead_agent/scripts/stop.sh"
echo "  /opt/lead_agent/scripts/status.sh"
echo ""

