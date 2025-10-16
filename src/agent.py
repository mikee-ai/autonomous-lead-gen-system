"""
Autonomous AI Lead Generation Agent - FINAL VERSION
Uses realistic people names for better deliverability

Author: Mikee Shattuck
"""

import requests
import json
import time
import logging
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Keys
APOLLO_API_KEY = "zkZ9TI5jBY2ZkqxiZwof1g"
INSTANTLY_API_KEY = "YjUzNzFjY2EtZGNiNC00OTIzLTgxZGYtZDg1Nzc3YzY5OTg3OlRvZHBXZm9Fb2xqUA=="

# Inframail API Configuration
INFRAMAIL_API_KEY = "inf_5721608913cf5d15e4fddb7b8e3257f03d3b7c47ce3b0f5418335f5b13059e1a"
INFRAMAIL_CUSTOMER_ID = "31761933"
INFRAMAIL_PROFILE_ID = "2b25dd6a-7c8a-42ba-aabf-23780350b865"
INFRAMAIL_HOST_ORDER_ID = "1755058187025"

# Campaign Settings
INSTANTLY_CAMPAIGN_ID = "1dfdc50b-465a-4cea-8a33-d80ef0a3e010"
TARGET_LOCATION = "United States"

# Safe Ramp Schedule
EMAILS_PER_ACCOUNT_PER_DAY = 20
ACCOUNTS_TO_CREATE_PER_DAY = 20
TARGET_TOTAL_ACCOUNTS = 100

# Your existing domains
EXISTING_DOMAINS = [
    "mikeeaipro.com",
    "elitemikeeai.com",
    "alphamikeeai.com",
    "primemikeeai.com",
    "mikeeaiproconnect.com"
]

# Realistic name lists for email accounts
FIRST_NAMES = [
    "sarah", "michael", "jennifer", "david", "jessica", "james", "emily", "robert",
    "amanda", "william", "ashley", "john", "melissa", "daniel", "nicole", "matthew",
    "lauren", "christopher", "rachel", "andrew", "stephanie", "joseph", "lisa", "ryan",
    "karen", "brian", "michelle", "kevin", "amy", "mark", "angela", "steven",
    "rebecca", "thomas", "laura", "jason", "heather", "joshua", "kimberly", "eric",
    "elizabeth", "richard", "maria", "charles", "nancy", "paul", "linda", "donald"
]

LAST_NAMES = [
    "smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis",
    "rodriguez", "martinez", "hernandez", "lopez", "gonzalez", "wilson", "anderson", "thomas",
    "taylor", "moore", "jackson", "martin", "lee", "thompson", "white", "harris",
    "clark", "lewis", "robinson", "walker", "hall", "allen", "young", "king",
    "wright", "scott", "torres", "nguyen", "hill", "flores", "green", "adams",
    "nelson", "baker", "hall", "rivera", "campbell", "mitchell", "carter", "roberts"
]

# API Endpoints
APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"
APOLLO_ENRICH_URL = "https://api.apollo.io/api/v1/people/match"
INSTANTLY_LEADS_URL = "https://api.instantly.ai/api/v1/lead/add"
INSTANTLY_ACCOUNTS_URL = "https://api.instantly.ai/api/v2/accounts"
INSTANTLY_CAMPAIGN_URL = f"https://api.instantly.ai/api/v2/campaigns/{INSTANTLY_CAMPAIGN_ID}"
INFRAMAIL_EMAIL_URL = "https://app.inframail.io/api/v1/host/operations/email"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'/root/lead_agent/logs/agent_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# INFRAMAIL MANAGER
# ============================================================================

class InframailManager:
    """Manages email account creation via Inframail API"""
    
    def __init__(self, api_key: str, customer_id: str, profile_id: str, host_order_id: str):
        self.api_key = api_key
        self.customer_id = customer_id
        self.profile_id = profile_id
        self.host_order_id = host_order_id
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    
    def get_email_accounts(self) -> List[str]:
        """Get all existing email accounts"""
        try:
            response = requests.get(
                f"{INFRAMAIL_EMAIL_URL}?hostOrderId={self.host_order_id}&customerId={self.customer_id}&profileId={self.profile_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return [email['email'] for email in data.get('emails', [])]
            return []
        except Exception as e:
            logger.error(f"Failed to get Inframail accounts: {e}")
            return []
    
    def create_email_account(self, email: str, password: str) -> bool:
        """Create a new email account in Inframail"""
        payload = {
            "profileId": self.profile_id,
            "email": email,
            "password": password,
            "mode": "add"
        }
        
        try:
            response = requests.post(
                INFRAMAIL_EMAIL_URL,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                logger.info(f"   ✓ Created: {email}")
                return True
            else:
                logger.error(f"   ✗ Failed to create {email}: {response.status_code}")
                logger.error(f"      Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Inframail API error: {e}")
            return False

# ============================================================================
# INSTANTLY MANAGER
# ============================================================================

class InstantlyManager:
    """Manages Instantly.ai operations"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    def get_accounts(self) -> List[str]:
        """Get all email accounts in Instantly"""
        try:
            response = requests.get(INSTANTLY_ACCOUNTS_URL, headers=self.headers)
            if response.status_code == 200:
                accounts = response.json()
                return [acc['email'] for acc in accounts]
            return []
        except Exception as e:
            logger.error(f"Instantly API error: {e}")
            return []
    
    def get_campaign_accounts(self) -> List[str]:
        """Get email accounts assigned to campaign"""
        try:
            response = requests.get(INSTANTLY_CAMPAIGN_URL, headers=self.headers)
            if response.status_code == 200:
                campaign = response.json()
                return campaign.get('email_list', [])
            return []
        except Exception as e:
            logger.error(f"Failed to get campaign accounts: {e}")
            return []
    
    def assign_accounts_to_campaign(self, email_list: List[str]) -> bool:
        """Assign email accounts to campaign"""
        payload = {"email_list": email_list}
        
        try:
            response = requests.patch(
                INSTANTLY_CAMPAIGN_URL,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                logger.info(f"   ✓ Assigned {len(email_list)} accounts to campaign")
                return True
            else:
                logger.error(f"   ✗ Failed to assign accounts: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Campaign assignment error: {e}")
            return False
    
    def add_email_account(self, email: str, password: str, domain: str, first_name: str, last_name: str) -> bool:
        """Add email account to Instantly"""
        
        # Inframail uses standard SMTP/IMAP settings
        smtp_host = f"mail.{domain}"
        imap_host = f"mail.{domain}"
        
        payload = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "provider_code": 1,  # 1 = Custom IMAP/SMTP (Inframail)
            "imap_username": email,
            "imap_password": password,
            "imap_host": imap_host,
            "imap_port": 993,
            "smtp_username": email,
            "smtp_password": password,
            "smtp_host": smtp_host,
            "smtp_port": 587
        }
        
        try:
            response = requests.post(
                INSTANTLY_ACCOUNTS_URL,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"      ✓ Added to Instantly")
                return True
            else:
                logger.error(f"      ✗ Failed to add to Instantly: {response.status_code}")
                logger.error(f"         Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Instantly API error: {e}")
            return False
    
    def add_lead(self, email: str, first_name: str, company: str) -> bool:
        """Add a lead to Instantly campaign"""
        payload = {
            "api_key": self.api_key,
            "campaign_id": INSTANTLY_CAMPAIGN_ID,
            "email": email,
            "first_name": first_name,
            "company_name": company
        }
        
        try:
            response = requests.post(INSTANTLY_LEADS_URL, json=payload)
            return response.status_code == 200
        except:
            return False

# ============================================================================
# APOLLO MANAGER
# ============================================================================

class ApolloManager:
    """Manages Apollo.io lead generation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}
    
    def search_business_owners(self, limit: int = 100) -> List[Dict]:
        """Search for business owners"""
        payload = {
            "api_key": self.api_key,
            "person_titles": ["Owner", "Founder", "Co-Founder", "Managing Partner"],
            "person_locations": [TARGET_LOCATION],
            "organization_num_employees_ranges": ["11,20", "21,50", "51,100"],
            "page": 1,
            "per_page": min(limit, 100)
        }
        
        try:
            response = requests.post(APOLLO_SEARCH_URL, headers=self.headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data.get('people', [])
            return []
        except Exception as e:
            logger.error(f"Apollo search error: {e}")
            return []
    
    def enrich_person(self, first_name: str, last_name: str, company: str) -> Optional[str]:
        """Enrich person data to get email"""
        payload = {
            "api_key": self.api_key,
            "first_name": first_name,
            "last_name": last_name,
            "organization_name": company,
            "reveal_personal_emails": True
        }
        
        try:
            response = requests.post(APOLLO_ENRICH_URL, headers=self.headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                person = data.get('person', {})
                return person.get('email')
            return None
        except:
            return None

# ============================================================================
# AUTONOMOUS AGENT
# ============================================================================

class AutonomousLeadAgent:
    """Main autonomous agent that orchestrates everything"""
    
    def __init__(self):
        self.inframail = InframailManager(
            INFRAMAIL_API_KEY,
            INFRAMAIL_CUSTOMER_ID,
            INFRAMAIL_PROFILE_ID,
            INFRAMAIL_HOST_ORDER_ID
        )
        self.instantly = InstantlyManager(INSTANTLY_API_KEY)
        self.apollo = ApolloManager(APOLLO_API_KEY)
        
        self.stats = {
            'accounts_created': 0,
            'accounts_connected': 0,
            'leads_imported': 0,
            'leads_to_import_today': 0
        }
    
    def generate_password(self) -> str:
        """Generate secure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choices(chars, k=16))
    
    def create_email_accounts(self, num_accounts: int) -> int:
        """Create email accounts with realistic people names"""
        logger.info(f"\n{'='*60}")
        logger.info(f"CREATING {num_accounts} EMAIL ACCOUNTS")
        logger.info(f"{'='*60}\n")
        
        accounts_per_domain = num_accounts // len(EXISTING_DOMAINS)
        remaining = num_accounts % len(EXISTING_DOMAINS)
        
        used_names = set()
        created_count = 0
        
        for i, domain in enumerate(EXISTING_DOMAINS):
            count = accounts_per_domain + (1 if i < remaining else 0)
            if count == 0:
                continue
            
            logger.info(f"\n[{domain}] Creating {count} accounts")
            
            for j in range(count):
                # Generate realistic name-based email
                while True:
                    first = random.choice(FIRST_NAMES)
                    last = random.choice(LAST_NAMES)
                    email = f"{first}.{last}@{domain}"
                    if email not in used_names:
                        used_names.add(email)
                        break
                
                password = self.generate_password()
                first_name = first.capitalize()
                last_name = last.capitalize()
                
                logger.info(f"[{created_count+1}/{num_accounts}] {email}")
                
                # Create in Inframail
                if self.inframail.create_email_account(email, password):
                    self.stats['accounts_created'] += 1
                    
                    # Add to Instantly
                    if self.instantly.add_email_account(email, password, domain, first_name, last_name):
                        self.stats['accounts_connected'] += 1
                        created_count += 1
                        
                        # Add to campaign
                        campaign_accounts = self.instantly.get_campaign_accounts()
                        if email not in campaign_accounts:
                            campaign_accounts.append(email)
                            self.instantly.assign_accounts_to_campaign(campaign_accounts)
                    
                    time.sleep(2)  # Rate limiting
        
        return created_count
    
    def import_leads(self, num_leads: int) -> int:
        """Import leads from Apollo to Instantly"""
        logger.info(f"\n{'='*60}")
        logger.info(f"IMPORTING {num_leads} LEADS")
        logger.info(f"{'='*60}\n")
        
        imported = 0
        batch_size = 100
        batches = (num_leads + batch_size - 1) // batch_size
        
        for batch in range(batches):
            batch_limit = min(batch_size, num_leads - imported)
            
            logger.info(f"\nBatch {batch+1}/{batches} - Searching for {batch_limit} business owners...")
            people = self.apollo.search_business_owners(batch_limit)
            
            for person in people:
                if imported >= num_leads:
                    break
                
                first_name = person.get('first_name', '')
                last_name = person.get('last_name', '')
                company = person.get('organization_name', '')
                email = person.get('email')
                
                if not email or '@' not in email:
                    # Try to enrich
                    email = self.apollo.enrich_person(first_name, last_name, company)
                
                if email and '@' in email:
                    if self.instantly.add_lead(email, first_name, company):
                        imported += 1
                        self.stats['leads_imported'] += 1
                        if imported % 10 == 0:
                            logger.info(f"   Imported {imported}/{num_leads} leads...")
                
                time.sleep(0.5)  # Rate limiting
        
        return imported
    
    def run(self):
        """Main execution"""
        logger.info(f"\n{'='*60}")
        logger.info(f"AUTONOMOUS LEAD AGENT - STARTING")
        logger.info(f"{'='*60}\n")
        
        # Check current infrastructure
        inframail_accounts = self.inframail.get_email_accounts()
        instantly_accounts = self.instantly.get_accounts()
        
        total_accounts = len(inframail_accounts)
        connected_accounts = len(instantly_accounts)
        
        logger.info(f"Current Infrastructure:")
        logger.info(f"  - Inframail accounts: {total_accounts}")
        logger.info(f"  - Instantly accounts: {connected_accounts}")
        logger.info(f"  - Current capacity: {connected_accounts * EMAILS_PER_ACCOUNT_PER_DAY} emails/day")
        
        # Calculate what to do today
        accounts_needed = max(0, TARGET_TOTAL_ACCOUNTS - total_accounts)
        accounts_to_create = min(ACCOUNTS_TO_CREATE_PER_DAY, accounts_needed)
        
        logger.info(f"\nToday's Plan:")
        logger.info(f"  - Accounts to create: {accounts_to_create}")
        
        # Create accounts if needed
        if accounts_to_create > 0:
            created = self.create_email_accounts(accounts_to_create)
            connected_accounts += created
        
        # Calculate leads to import based on capacity
        self.stats['leads_to_import_today'] = connected_accounts * EMAILS_PER_ACCOUNT_PER_DAY
        
        logger.info(f"  - Leads to import: {self.stats['leads_to_import_today']}")
        
        # Import leads
        if self.stats['leads_to_import_today'] > 0:
            self.import_leads(self.stats['leads_to_import_today'])
        
        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"DAILY RUN COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Accounts created: {self.stats['accounts_created']}")
        logger.info(f"Accounts connected: {self.stats['accounts_connected']}")
        logger.info(f"Leads imported: {self.stats['leads_imported']}")
        logger.info(f"New daily capacity: {connected_accounts * EMAILS_PER_ACCOUNT_PER_DAY} emails/day")
        logger.info(f"{'='*60}\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    agent = AutonomousLeadAgent()
    agent.run()

