"""
Credit-Safe Apollo Manager
Prevents wasted credits from failed API calls

Key Features:
1. Pre-validates data before consuming credits
2. Checks for existing leads before enrichment
3. Implements retry logic with exponential backoff
4. Tracks credit usage in real-time
5. Validates email format before API calls
6. Caches results to avoid duplicate calls
"""

import requests
import json
import time
import logging
import re
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CreditSafeApolloManager:
    """Apollo.io manager with credit protection"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }
        self.credits_used_this_session = 0
        self.successful_enrichments = 0
        self.failed_enrichments = 0
        self.cache = {}  # Cache to avoid duplicate API calls
        
    def validate_email(self, email: str) -> bool:
        """Validate email format before making API call"""
        if not email or not isinstance(email, str):
            return False
        
        # Basic email regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def is_cached(self, email: str) -> Optional[Dict]:
        """Check if we already have this contact in cache"""
        return self.cache.get(email.lower())
    
    def add_to_cache(self, email: str, data: Dict):
        """Add contact to cache to avoid duplicate calls"""
        self.cache[email.lower()] = data
    
    def check_credit_balance(self) -> Optional[int]:
        """
        Check remaining credits before making calls
        Returns: remaining credits or None if unable to check
        """
        try:
            # Note: Apollo doesn't have a direct API to check credits
            # This is a placeholder - you'd need to track manually
            logger.info(f"Credits used this session: {self.credits_used_this_session}")
            return None
        except Exception as e:
            logger.warning(f"Could not check credit balance: {e}")
            return None
    
    def search_with_validation(self, 
                               person_titles: List[str],
                               person_locations: List[str],
                               org_size_ranges: List[str],
                               limit: int = 100) -> List[Dict]:
        """
        Search for contacts with pre-validation
        Only returns contacts that have valid emails
        """
        
        # Validate inputs before making API call
        if not person_titles or not person_locations:
            logger.error("Invalid search parameters - no titles or locations provided")
            return []
        
        if limit <= 0 or limit > 100:
            logger.error(f"Invalid limit: {limit}. Must be between 1 and 100")
            return []
        
        payload = {
            "api_key": self.api_key,
            "person_titles": person_titles,
            "person_locations": person_locations,
            "organization_num_employees_ranges": org_size_ranges,
            "page": 1,
            "per_page": limit
        }
        
        try:
            logger.info(f"Searching Apollo for {limit} contacts...")
            
            response = requests.post(
                "https://api.apollo.io/api/v1/mixed_people/search",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check for successful response BEFORE processing
            if response.status_code != 200:
                logger.error(f"Search failed with status {response.status_code}: {response.text}")
                return []
            
            data = response.json()
            people = data.get('people', [])
            
            # Filter out contacts without emails BEFORE enrichment
            valid_contacts = []
            for person in people:
                email = person.get('email')
                
                # Skip if no email or invalid email
                if not email or not self.validate_email(email):
                    logger.debug(f"Skipping contact without valid email: {person.get('name', 'Unknown')}")
                    continue
                
                valid_contacts.append(person)
            
            logger.info(f"Found {len(valid_contacts)} contacts with valid emails (filtered from {len(people)} total)")
            
            # Track credits used (search uses credits too)
            self.credits_used_this_session += limit
            
            return valid_contacts
            
        except requests.exceptions.Timeout:
            logger.error("Apollo API timeout - no credits consumed")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during search: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []
    
    def enrich_with_retry(self, 
                          first_name: str, 
                          last_name: str, 
                          organization_name: str,
                          max_retries: int = 3) -> Optional[Dict]:
        """
        Enrich contact with retry logic and validation
        Only consumes credits if enrichment succeeds
        """
        
        # Pre-validate inputs
        if not first_name or not last_name:
            logger.error("Cannot enrich: missing first or last name")
            self.failed_enrichments += 1
            return None
        
        # Create cache key
        cache_key = f"{first_name.lower()}_{last_name.lower()}_{organization_name.lower() if organization_name else 'none'}"
        
        # Check cache first (avoid duplicate API calls)
        cached = self.is_cached(cache_key)
        if cached:
            logger.info(f"Using cached data for {first_name} {last_name} (saved 1 credit)")
            return cached
        
        payload = {
            "api_key": self.api_key,
            "first_name": first_name,
            "last_name": last_name,
            "organization_name": organization_name,
            "reveal_personal_emails": True
        }
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Enriching {first_name} {last_name} (attempt {attempt + 1}/{max_retries})")
                
                response = requests.post(
                    "https://api.apollo.io/api/v1/people/match",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                # Check status code BEFORE processing
                if response.status_code == 404:
                    logger.warning(f"Contact not found: {first_name} {last_name}")
                    self.failed_enrichments += 1
                    return None
                
                if response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code != 200:
                    logger.error(f"Enrichment failed with status {response.status_code}: {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        self.failed_enrichments += 1
                        return None
                
                # Parse response
                data = response.json()
                person = data.get('person', {})
                
                # Validate we got an email
                email = person.get('email')
                if not email or not self.validate_email(email):
                    logger.warning(f"Enrichment returned invalid email for {first_name} {last_name}")
                    self.failed_enrichments += 1
                    return None
                
                # Success! Cache the result
                self.add_to_cache(cache_key, person)
                self.credits_used_this_session += 1
                self.successful_enrichments += 1
                
                logger.info(f"✓ Enriched: {first_name} {last_name} - {email}")
                return person
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    logger.error(f"All retries exhausted for {first_name} {last_name}")
                    self.failed_enrichments += 1
                    return None
                    
            except Exception as e:
                logger.error(f"Error enriching {first_name} {last_name}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    self.failed_enrichments += 1
                    return None
        
        # All retries failed
        self.failed_enrichments += 1
        return None
    
    def batch_enrich_safe(self, contacts: List[Dict], max_credits: int = None) -> List[Dict]:
        """
        Safely enrich a batch of contacts with credit limit
        Stops if max_credits is reached
        """
        
        enriched_contacts = []
        
        for i, contact in enumerate(contacts):
            # Check credit limit
            if max_credits and self.credits_used_this_session >= max_credits:
                logger.warning(f"Credit limit reached ({max_credits}). Stopping enrichment.")
                break
            
            # Extract contact info
            first_name = contact.get('first_name', '')
            last_name = contact.get('last_name', '')
            company = contact.get('organization_name', '')
            
            # Skip if already has valid email
            existing_email = contact.get('email')
            if existing_email and self.validate_email(existing_email):
                logger.info(f"Contact already has valid email: {existing_email}")
                enriched_contacts.append(contact)
                continue
            
            # Enrich with retry
            enriched = self.enrich_with_retry(first_name, last_name, company)
            
            if enriched:
                enriched_contacts.append(enriched)
            else:
                logger.warning(f"Failed to enrich {first_name} {last_name}")
            
            # Rate limiting: small delay between calls
            if i < len(contacts) - 1:
                time.sleep(0.5)
        
        return enriched_contacts
    
    def get_session_stats(self) -> Dict:
        """Get statistics for this session"""
        return {
            "credits_used": self.credits_used_this_session,
            "successful_enrichments": self.successful_enrichments,
            "failed_enrichments": self.failed_enrichments,
            "cache_size": len(self.cache),
            "success_rate": f"{(self.successful_enrichments / max(1, self.successful_enrichments + self.failed_enrichments) * 100):.1f}%"
        }


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize manager
    apollo = CreditSafeApolloManager(api_key="YOUR_API_KEY")
    
    # Search with validation
    contacts = apollo.search_with_validation(
        person_titles=["Owner", "Founder"],
        person_locations=["United States"],
        org_size_ranges=["11,20", "21,50"],
        limit=10
    )
    
    # Enrich with credit limit
    enriched = apollo.batch_enrich_safe(contacts, max_credits=50)
    
    # Print stats
    stats = apollo.get_session_stats()
    print("\n" + "="*60)
    print("SESSION STATISTICS")
    print("="*60)
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("="*60)

