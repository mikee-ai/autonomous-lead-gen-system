# Usage Guide

This guide explains how to manage and monitor the Autonomous Lead Generation System after it has been deployed.

## Managing the System

The system is managed through `systemd` services and a set of convenience scripts.

### Starting and Stopping the System

*   **To start the system:**

    ```bash
    sudo systemctl start lead-agent lead-dashboard
    ```

*   **To stop the system:**

    ```bash
    sudo systemctl stop lead-agent lead-dashboard
    ```

### Checking the Status

*   **To check the status of the services:**

    ```bash
    sudo systemctl status lead-agent lead-dashboard
    ```

*   **For a quick summary, use the status script:**

    ```bash
    sudo /opt/lead_agent/scripts/status.sh
    ```

### Viewing Logs

*   **To view the agent logs in real-time:**

    ```bash
    journalctl -u lead-agent -f
    ```

*   **To view the dashboard logs in real-time:**

    ```bash
    journalctl -u lead-dashboard -f
    ```

## The Dashboard

The dashboard provides a real-time overview of the agent's activities. You can access it at the IP address or domain you configured during setup.

The dashboard displays:

*   **System Status:** Whether the agent is running.
*   **Account Status:** The number of email accounts created and their status.
*   **Campaign Stats:** The number of leads added to your campaign.
*   **Recent Activity:** A log of the agent's most recent actions.

## Updating the System

To update the system to the latest version, you will need to download the new package, stop the services, replace the files in `/opt/lead_agent`, and restart the services.

1.  **Stop the services:**

    ```bash
    sudo systemctl stop lead-agent lead-dashboard
    ```

2.  **Replace the files:**

    Copy the new application files to `/opt/lead_agent`.

3.  **Update dependencies (if necessary):**

    ```bash
    cd /opt/lead_agent
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Start the services:**

    ```bash
    sudo systemctl start lead-agent lead-dashboard
    ```

