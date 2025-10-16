# Configuration Guide

This guide explains all the settings available in the `config.py` file. You must copy `config.template.py` to `config.py` and fill in your details before running the system.

## API Keys

These are the essential API keys required for the system to function.

*   `APOLLO_API_KEY`: Your API key for Apollo.io. You can find this in your Apollo settings under **Integrations > API**.
*   `INSTANTLY_API_KEY`: Your API key for Instantly.ai. You can find this in your Instantly settings under **Integrations**.
*   `INFRAMAIL_API_KEY`: Your API key for Inframail. You can find this in your Inframail account.
*   `INFRAMAIL_CUSTOMER_ID`: Your Inframail customer ID.
*   `INFRAMAIL_PROFILE_ID`: The ID of the Inframail profile you want to use.
*   `INFRAMAIL_HOST_ORDER_ID`: The ID of the hosting order in Inframail where you want to create email accounts.

## Campaign Settings

*   `INSTANTLY_CAMPAIGN_ID`: The ID of the campaign in Instantly.ai where you want to add leads and email accounts. You can find this in the URL of your campaign page.
*   `TARGET_LOCATION`: The geographical location to target for lead generation in Apollo.io (e.g., "United States", "Germany").

## Scaling Settings

These settings control the volume of your outreach.

*   `EMAILS_PER_ACCOUNT_PER_DAY`: The maximum number of emails each email account will send per day. It is recommended to keep this number low (20-30) to maintain a good sender reputation.
*   `ACCOUNTS_TO_CREATE_PER_DAY`: The number of new email accounts the system will create each day until the `TARGET_TOTAL_ACCOUNTS` is reached.
*   `TARGET_TOTAL_ACCOUNTS`: The total number of email accounts you want the system to create and maintain.

## Domain Settings

*   `EXISTING_DOMAINS`: A list of domain names that you have configured in Inframail. The system will use these domains to create new email accounts.

## Advanced Settings

These settings allow for more fine-grained control over the lead generation process.

*   `PERSON_TITLES`: A list of job titles to target in Apollo.io.
*   `ORGANIZATION_EMPLOYEE_RANGES`: A list of company sizes to target in Apollo.io.
*   `WARMUP_DAYS`: The number of days to warm up a new email account before it starts sending campaign emails. This is a crucial step to ensure good deliverability.
*   `LOG_LEVEL`: The logging level for the application. Can be `DEBUG`, `INFO`, `WARNING`, or `ERROR`.

