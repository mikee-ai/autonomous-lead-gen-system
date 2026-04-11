"""
Real-Time AI Agent Dashboard
Beautiful web interface to watch your autonomous agent work
"""

from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime
import os
import sys

# Add project root to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    APOLLO_API_KEY,
    INSTANTLY_API_KEY,
    INFRAMAIL_API_KEY,
    INFRAMAIL_CUSTOMER_ID,
    INFRAMAIL_PROFILE_ID,
    INFRAMAIL_HOST_ORDER_ID,
    INSTANTLY_CAMPAIGN_ID,
)

# Set Flask template directory to the same directory as this file (src/)
_src_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=_src_dir)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get real-time stats from all systems"""
    
    # Get Inframail accounts
    inframail_count = 0
    try:
        response = requests.get(
            f"https://app.inframail.io/api/v1/host/operations/email?hostOrderId={INFRAMAIL_HOST_ORDER_ID}&customerId={INFRAMAIL_CUSTOMER_ID}&profileId={INFRAMAIL_PROFILE_ID}",
            headers={"x-api-key": INFRAMAIL_API_KEY}
        )
        if response.status_code == 200:
            inframail_count = len(response.json().get('emails', []))
    except:
        pass
    
    # Get Instantly accounts
    instantly_count = 0
    try:
        response = requests.get(
            "https://api.instantly.ai/api/v2/accounts",
            headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}"}
        )
        if response.status_code == 200:
            instantly_count = len(response.json())
    except:
        pass
    
    # Get campaign accounts
    campaign_accounts = 0
    try:
        response = requests.get(
            f"https://api.instantly.ai/api/v2/campaigns/{INSTANTLY_CAMPAIGN_ID}",
            headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}"}
        )
        if response.status_code == 200:
            campaign_accounts = len(response.json().get('email_list', []))
    except:
        pass
    
    # Get campaign analytics
    campaign_stats = {}
    try:
        response = requests.get(
            f"https://api.instantly.ai/api/v2/campaigns/analytics?campaign_id={INSTANTLY_CAMPAIGN_ID}",
            headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}"}
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                campaign_stats = data[0] if isinstance(data, list) else data
    except:
        pass
    
    # Read latest log
    log_lines = []
    log_file = '/root/lead_agent/logs/with_campaign_assignment.log'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                log_lines = f.readlines()[-50:]  # Last 50 lines
        except:
            pass
    
    # Calculate stats
    daily_capacity = campaign_accounts * 20
    accounts_to_create = max(0, 100 - inframail_count)
    days_to_2k = max(1, (accounts_to_create + 19) // 20)  # Round up
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'infrastructure': {
            'inframail_accounts': inframail_count,
            'instantly_accounts': instantly_count,
            'campaign_accounts': campaign_accounts,
            'daily_capacity': daily_capacity,
            'target_accounts': 100,
            'accounts_remaining': accounts_to_create,
            'days_to_2k': days_to_2k
        },
        'campaign': {
            'sent': campaign_stats.get('sent', 0),
            'delivered': campaign_stats.get('delivered', 0),
            'opened': campaign_stats.get('opened', 0),
            'clicked': campaign_stats.get('clicked', 0),
            'replied': campaign_stats.get('replied', 0),
            'bounced': campaign_stats.get('bounced', 0),
            'open_rate': round(campaign_stats.get('open_rate', 0) * 100, 1) if campaign_stats.get('open_rate') else 0,
            'reply_rate': round(campaign_stats.get('reply_rate', 0) * 100, 1) if campaign_stats.get('reply_rate') else 0
        },
        'recent_activity': [line.strip() for line in log_lines if line.strip()]
    })

@app.route('/api/accounts')
def get_accounts():
    """Get list of all email accounts"""
    accounts = []
    
    try:
        response = requests.get(
            f"https://app.inframail.io/api/v1/host/operations/email?hostOrderId={INFRAMAIL_HOST_ORDER_ID}&customerId={INFRAMAIL_CUSTOMER_ID}&profileId={INFRAMAIL_PROFILE_ID}",
            headers={"x-api-key": INFRAMAIL_API_KEY}
        )
        if response.status_code == 200:
            emails = response.json().get('emails', [])
            accounts = [{'email': e['email'], 'domain': e['email'].split('@')[1]} for e in emails]
    except:
        pass
    
    return jsonify({'accounts': accounts})

if __name__ == '__main__':
    # Run on all interfaces so it's accessible from outside
    app.run(host='0.0.0.0', port=8080, debug=False)

