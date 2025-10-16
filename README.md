# Autonomous Lead Generation System

This package contains a fully autonomous AI agent that generates leads for your business. It integrates with Apollo.io, Inframail, and Instantly.ai to create a complete, end-to-end lead generation pipeline.

This system is designed to be deployed on any VPS and run 24/7, continuously finding new leads, creating email accounts, and managing your cold outreach campaigns.

## Features

*   **Fully Autonomous:** Set it up once, and it runs forever.
*   **Automatic Lead Generation:** Discovers and enriches targeted leads from Apollo.io.
*   **Automatic Email Account Creation:** Creates and warms up email accounts with Inframail.
*   **Automatic Campaign Management:** Adds leads and accounts to Instantly.ai campaigns.
*   **Real-Time Dashboard:** A beautiful web interface to monitor the agent's activity.
*   **Easy Deployment:** Simple setup scripts for any Debian-based VPS.
*   **Scalable:** Designed to scale to thousands of emails per day.

## How It Works

The system is composed of two main components:

1.  **The Autonomous Agent (`agent.py`):** A Python script that runs continuously, orchestrating the entire lead generation process.
2.  **The Dashboard (`dashboard.py`):** A Flask web application that provides a real-time view of the agent's activities.

## Getting Started

To deploy this system, you will need:

*   A VPS (like Hostinger, DigitalOcean, etc.) running a Debian-based OS (e.g., Ubuntu 22.04).
*   API keys for:
    *   Apollo.io
    *   Instantly.ai
    *   Inframail
*   At least one domain name for sending emails.

Follow the instructions in the `docs/DEPLOYMENT.md` file to get started.

## Documentation

*   **[Deployment Guide](docs/DEPLOYMENT.md):** Step-by-step instructions for deploying the system on a fresh VPS.
*   **[Configuration Guide](docs/CONFIGURATION.md):** Detailed explanation of all configuration options.
*   **[Usage Guide](docs/USAGE.md):** How to manage and monitor the system after deployment.

## For Manus AI Users

If you are a Manus AI user, you can deploy this system with a single prompt. See `MANUS_PROMPT.md` for instructions.

## License

This project is open-source and available for free. See the [LICENSE](LICENSE) file for more details.

