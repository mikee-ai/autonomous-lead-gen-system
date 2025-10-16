"""
Configuration Template for Autonomous Lead Generation System
Copy this file to config.py and fill in your API keys
"""

# ============================================================================
# API KEYS - REQUIRED
# ============================================================================

# Apollo.io API Key
# Get yours at: https://app.apollo.io/#/settings/integrations/api
APOLLO_API_KEY = "YOUR_APOLLO_API_KEY_HERE"

# Instantly.ai API Key
# Get yours at: https://app.instantly.ai/app/settings/integrations
INSTANTLY_API_KEY = "YOUR_INSTANTLY_API_KEY_HERE"

# Inframail API Configuration
# Get yours at: https://app.inframail.io/
INFRAMAIL_API_KEY = "YOUR_INFRAMAIL_API_KEY_HERE"
INFRAMAIL_CUSTOMER_ID = "YOUR_CUSTOMER_ID_HERE"
INFRAMAIL_PROFILE_ID = "YOUR_PROFILE_ID_HERE"
INFRAMAIL_HOST_ORDER_ID = "YOUR_HOST_ORDER_ID_HERE"

# ============================================================================
# CAMPAIGN SETTINGS
# ============================================================================

# Instantly.ai Campaign ID
# Create a campaign in Instantly.ai and paste the ID here
INSTANTLY_CAMPAIGN_ID = "YOUR_CAMPAIGN_ID_HERE"

# Target location for lead generation
TARGET_LOCATION = "United States"

# ============================================================================
# SCALING SETTINGS
# ============================================================================

# How many emails each account should send per day
EMAILS_PER_ACCOUNT_PER_DAY = 20

# How many new email accounts to create per day
ACCOUNTS_TO_CREATE_PER_DAY = 20

# Total number of email accounts to maintain
TARGET_TOTAL_ACCOUNTS = 100

# ============================================================================
# DOMAIN SETTINGS
# ============================================================================

# Your domains configured in Inframail
# Add all domains you want to use for email accounts
EXISTING_DOMAINS = [
    "yourdomain1.com",
    "yourdomain2.com",
    "yourdomain3.com",
]

# ============================================================================
# ADVANCED SETTINGS (Optional)
# ============================================================================

# Lead search criteria (Apollo.io)
PERSON_TITLES = ["Owner", "Founder", "Co-Founder", "Managing Partner", "CEO"]
ORGANIZATION_EMPLOYEE_RANGES = ["11,20", "21,50", "51,100", "101,200"]

# Warmup settings
WARMUP_DAYS = 14  # Days to warm up new email accounts before full sending

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

