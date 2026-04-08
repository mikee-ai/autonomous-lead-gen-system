#!/bin/bash

# SSH Key Setup for Autonomous Lead Generation System
# Run this on your LOCAL machine (not the VPS) to configure passwordless SSH access.

set -e

echo "=========================================="
echo "Autonomous Lead Generation System"
echo "SSH Key Setup (run on local machine)"
echo "=========================================="
echo ""

# Step 1: Check prerequisites
echo "[1/5] Checking prerequisites..."
for cmd in ssh ssh-keygen ssh-copy-id; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "  Error: '$cmd' is not installed. Please install OpenSSH client tools."
        exit 1
    fi
done
echo "  ✓ All required tools found."

# Step 2: Set up ~/.ssh directory
echo ""
echo "[2/5] Setting up ~/.ssh directory..."
if [ ! -d "$HOME/.ssh" ]; then
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    echo "  ✓ Created ~/.ssh directory."
else
    chmod 700 "$HOME/.ssh"
    echo "  ✓ ~/.ssh directory already exists."
fi

# Step 3: Generate SSH key
echo ""
echo "[3/5] Setting up SSH key..."

KEY_PATH="$HOME/.ssh/lead_gen_vps_ed25519"

if [ -f "$KEY_PATH" ]; then
    echo "  SSH key already exists at $KEY_PATH"
    echo "  Skipping key generation (remove it manually if you want a new one)."
else
    echo "  Generating new Ed25519 SSH key pair..."
    read -p "  Enter an email label for the key (or press Enter to skip): " KEY_COMMENT
    if [ -z "$KEY_COMMENT" ]; then
        KEY_COMMENT="lead-gen-vps"
    fi
    ssh-keygen -t ed25519 -f "$KEY_PATH" -C "$KEY_COMMENT" -N ""
    echo "  ✓ Key pair generated:"
    echo "    Private: $KEY_PATH"
    echo "    Public:  ${KEY_PATH}.pub"
fi

# Ensure correct permissions regardless
chmod 600 "$KEY_PATH"
chmod 644 "${KEY_PATH}.pub"

# Step 4: Copy key to VPS
echo ""
echo "[4/5] Copying public key to your VPS..."

read -p "  Enter your VPS IP address: " VPS_IP

if [ -z "$VPS_IP" ]; then
    echo "  Error: VPS IP address cannot be empty."
    exit 1
fi

read -p "  Enter SSH user (default: root): " SSH_USER
SSH_USER="${SSH_USER:-root}"

read -p "  Enter SSH port (default: 22): " SSH_PORT
SSH_PORT="${SSH_PORT:-22}"

echo ""
echo "  Copying public key to $SSH_USER@$VPS_IP (port $SSH_PORT)..."
echo "  You may be prompted for the VPS password one last time."
echo ""

ssh-copy-id -i "${KEY_PATH}.pub" -p "$SSH_PORT" "$SSH_USER@$VPS_IP"

echo ""
echo "  ✓ Public key copied to VPS."

# Step 5: Configure SSH shortcut
echo ""
echo "[5/5] Configuring SSH shortcut..."

SSH_CONFIG="$HOME/.ssh/config"

# Create config file if it doesn't exist
if [ ! -f "$SSH_CONFIG" ]; then
    touch "$SSH_CONFIG"
    chmod 600 "$SSH_CONFIG"
fi

# Check if entry already exists
if grep -q "^Host lead-gen-vps" "$SSH_CONFIG" 2>/dev/null; then
    echo "  SSH config entry 'lead-gen-vps' already exists."
    echo "  To update it, edit ~/.ssh/config manually."
else
    cat >> "$SSH_CONFIG" << EOF

# Autonomous Lead Generation System - VPS
Host lead-gen-vps
    HostName $VPS_IP
    User $SSH_USER
    Port $SSH_PORT
    IdentityFile $KEY_PATH
    IdentitiesOnly yes
EOF
    chmod 600 "$SSH_CONFIG"
    echo "  ✓ Added 'lead-gen-vps' entry to ~/.ssh/config"
fi

# Test connection
echo ""
echo "Testing SSH connection..."
echo ""

if ssh -o ConnectTimeout=10 -o BatchMode=yes lead-gen-vps "echo '  ✓ Connection successful! Logged in as \$(whoami) on \$(hostname)'"; then
    echo ""
    echo "=========================================="
    echo "✓ SSH Setup Complete!"
    echo "=========================================="
    echo ""
    echo "You can now connect to your VPS with:"
    echo "  ssh lead-gen-vps"
    echo ""
    echo "Next steps:"
    echo "  1. Connect to your VPS:  ssh lead-gen-vps"
    echo "  2. Follow the Deployment Guide:  docs/DEPLOYMENT.md"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "⚠ SSH key was copied but connection test failed."
    echo "=========================================="
    echo ""
    echo "Try connecting manually:"
    echo "  ssh -i $KEY_PATH -p $SSH_PORT $SSH_USER@$VPS_IP"
    echo ""
    echo "Common issues:"
    echo "  - Firewall blocking port $SSH_PORT"
    echo "  - SSH service not running on the VPS"
    echo "  - Incorrect IP address"
    echo ""
    exit 1
fi
