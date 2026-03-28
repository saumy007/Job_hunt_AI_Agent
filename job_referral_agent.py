#!/usr/bin/env python3
"""
AI Job Referral Agent
Scrapes job boards, matches with resume, finds contacts, sends Telegram updates
"""

import os
import time
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
import anthropic
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from telegram.error import TelegramError
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobReferralAgent:
    def __init__(self):
        # Load environment variables
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_sheet_id = os.getenv('GOOGLE_SHEET_ID')
        
        # Initialize services
        self.claude_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        self.telegram_bot = Bot(token=self.telegram_token)
        self.sheet = self._init_google_sheets()
        
        # Job search parameters
        self.search_params = {
            'titles': ['Software Engineer', 'Backend Engineer', 'Full Stack Engineer', 
                      'Python Developer', 'AI Engineer'],
            'locations': ['Remote', 'Bengaluru', 'Bangalore', 'India'],
            'keywords': ['Python', 'ROS', 'Unity', 'Robotics', 'Simulation', 'AI']
        }
        
        # Resume data (from PDF)
        self.resume_data = self._load_resume_data()
        
    def _init_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            # Set up credentials from environment variable (JSON string)
            creds_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(credentials)
            sheet = client.open_by_key(self.google_sheet_id)
            return sheet.sheet1
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets: {e}")
            return None
    
    def _load_resume_data(self):
        """Load resume data for matching"""
        return {
            'name': 'Saumy Sharma',
            'skills': [
                'Python', 'C++', 'Unity', 'ROS2', 'Isaac Sim', 'Nvidia Omniverse',
                'Machine Learning', 'Robotics', 'Simulation', 'Digital Twin',
                'AR/VR', 'React.js', 'Node.js', 'MongoDB', 'Firebase'
            ],
            'experience': [
                'Robotics Software Developer at Jio Reality Labs',
                'CERN Openlab Summer Intern 2024',
                'Unity Developer at Smollan India',
                'XROS Fellowship 2023'
            ],
            'education': 'B.Tech in Information Technology, CGPA: 7.6/10',
            'achievements': [
                'CERN Webfest 2024 - Most Influential Award',
                'XROS Fellowship 2023 - Top 100 from 10,000 applicants',
                'EY Hackathon Semifinalist'
            ]
        }
    
    async def send_telegram_message(self, message: str, parse_mode='Markdown'):
        """Send notification via Telegram"""
        try:
            await self.telegram_bot.send_message(
                chat_id=self.telegram_chat_id,
                text=message,
                parse_mode=parse_mode
            )
            logger.info("Telegram message sent successfully")
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
    
    def match_job_with_resume(self, job_description: str, job_title: str) -> Dict:
        """Use Claude to analyze job match"""
        try:
            prompt = f"""Analyze this job posting for a candidate with the following profile:

CANDIDATE PROFILE:
Name: {self.resume_data['name']}
Skills: {', '.join(self.resume_data['skills'])}
Experience: {', '.join(self.resume_data['experience'])}
Education: {self.resume_data['education']}

JOB POSTING:
Title: {job_title}
Description: {job_description}

Provide a JSON response with:
1. match_score (0-100): How well the candidate matches this role
2. matching_skills: List of candidate's skills that match the job
3. missing_skills: Skills mentioned in job that candidate lacks
4. recommendation: Should apply (yes/no) with brief reasoning
5. key_highlights: Top 3 resume points to emphasize in application

Return ONLY valid JSON, no other text."""

            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            # Parse JSON response
            return json.loads(response_text)
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return {
                'match_score': 0,
                'matching_skills': [],
                'missing_skills': [],
                'recommendation': 'error',
                'key_highlights': []
            }
    
    def scrape_naukri_jobs(self, query: str, location: str, max_results: int = 10) -> List[Dict]:
        """Scrape jobs from Naukri.com"""
        jobs = []
        try:
            base_url = "https://www.naukri.com"
            search_url = f"{base_url}/{query.replace(' ', '-')}-jobs-in-{location}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('article', class_='jobTuple', limit=max_results)
            
            for card in job_cards:
                try:
                    title_elem = card.find('a', class_='title')
                    company_elem = card.find('a', class_='subTitle')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'url': base_url + title_elem['href'] if title_elem.get('href') else '',
                            'source': 'Naukri',
                            'posted_date': datetime.now().strftime('%Y-%m-%d')
                        }
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"Error parsing job card: {e}")
                    continue
            
            logger.info(f"Scraped {len(jobs)} jobs from Naukri")
            
        except Exception as e:
            logger.error(f"Naukri scraping error: {e}")
        
        return jobs
    
    def scrape_linkedin_jobs(self, keywords: str, location: str, max_results: int = 10) -> List[Dict]:
        """Scrape jobs from LinkedIn (requires no login for public listings)"""
        jobs = []
        try:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='base-card', limit=max_results)
            
            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if title_elem and company_elem and link_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'url': link_elem['href'],
                            'source': 'LinkedIn',
                            'posted_date': datetime.now().strftime('%Y-%m-%d')
                        }
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"Error parsing LinkedIn job: {e}")
                    continue
            
            logger.info(f"Scraped {len(jobs)} jobs from LinkedIn")
            
        except Exception as e:
            logger.error(f"LinkedIn scraping error: {e}")
        
        return jobs
    
    def scrape_instahyre_jobs(self, role: str, max_results: int = 10) -> List[Dict]:
        """Scrape jobs from Instahyre"""
        jobs = []
        try:
            search_url = f"https://www.instahyre.com/search-jobs/{role.replace(' ', '%20')}/"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='opportunity-card', limit=max_results)
            
            for card in job_cards:
                try:
                    title_elem = card.find('div', class_='job-title')
                    company_elem = card.find('div', class_='company-name')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip(),
                            'url': 'https://www.instahyre.com' + card.find('a')['href'] if card.find('a') else '',
                            'source': 'Instahyre',
                            'posted_date': datetime.now().strftime('%Y-%m-%d')
                        }
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"Error parsing Instahyre job: {e}")
                    continue
            
            logger.info(f"Scraped {len(jobs)} jobs from Instahyre")
            
        except Exception as e:
            logger.error(f"Instahyre scraping error: {e}")
        
        return jobs
    
    def find_company_contacts(self, company_name: str) -> Dict:
        """Find company CEO and recruiter contacts using web search and Claude"""
        try:
            # Use Claude to search for contacts
            prompt = f"""Find contact information for {company_name}:
1. CEO name and LinkedIn profile
2. HR/Recruiter contacts
3. Company careers page

Search the web and provide the information in JSON format:
{{
    "company_name": "{company_name}",
    "ceo_name": "Name or null",
    "ceo_linkedin": "LinkedIn URL or null",
    "recruiter_name": "Name or null", 
    "recruiter_email": "Email or null",
    "recruiter_linkedin": "LinkedIn URL or null",
    "careers_page": "URL or null"
}}
"""
            
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            return json.loads(response_text)
            
        except Exception as e:
            logger.error(f"Contact finder error: {e}")
            return {
                'company_name': company_name,
                'ceo_name': None,
                'ceo_linkedin': None,
                'recruiter_name': None,
                'recruiter_email': None,
                'recruiter_linkedin': None,
                'careers_page': None
            }
    
    def update_google_sheet(self, jobs_data: List[Dict]):
        """Update Google Sheet with job data"""
        if not self.sheet:
            logger.error("Google Sheet not initialized")
            return
        
        try:
            # Create header if sheet is empty
            if len(self.sheet.get_all_values()) == 0:
                headers = [
                    'Date Added', 'Company Name', 'Job Title', 'Job URL', 'Source',
                    'Match Score', 'Status', 'CEO Name', 'CEO LinkedIn',
                    'Recruiter Name', 'Recruiter Email', 'Recruiter LinkedIn',
                    'Key Highlights', 'Notes'
                ]
                self.sheet.append_row(headers)
            
            # Add jobs
            for job in jobs_data:
                row = [
                    datetime.now().strftime('%Y-%m-%d %H:%M'),
                    job.get('company', ''),
                    job.get('title', ''),
                    job.get('url', ''),
                    job.get('source', ''),
                    job.get('match_score', 0),
                    'New',
                    job.get('ceo_name', ''),
                    job.get('ceo_linkedin', ''),
                    job.get('recruiter_name', ''),
                    job.get('recruiter_email', ''),
                    job.get('recruiter_linkedin', ''),
                    ', '.join(job.get('key_highlights', [])),
                    ''
                ]
                self.sheet.append_row(row)
            
            logger.info(f"Added {len(jobs_data)} jobs to Google Sheet")
            
        except Exception as e:
            logger.error(f"Google Sheet update error: {e}")
    
    async def run_job_search(self):
        """Main job search workflow"""
        logger.info("Starting job search...")
        
        # Send start notification
        await self.send_telegram_message("🤖 *Job Search Agent Started*\nSearching for relevant opportunities...")
        
        all_jobs = []
        
        # Scrape multiple sources
        for title in self.search_params['titles']:
            for location in self.search_params['locations']:
                # Naukri
                naukri_jobs = self.scrape_naukri_jobs(title, location, max_results=5)
                all_jobs.extend(naukri_jobs)
                
                # LinkedIn
                linkedin_jobs = self.scrape_linkedin_jobs(title, location, max_results=5)
                all_jobs.extend(linkedin_jobs)
                
                # Instahyre
                if location in ['Bengaluru', 'Bangalore']:
                    instahyre_jobs = self.scrape_instahyre_jobs(title, max_results=5)
                    all_jobs.extend(instahyre_jobs)
                
                # Rate limiting
                time.sleep(2)
        
        # Remove duplicates
        unique_jobs = {job['url']: job for job in all_jobs if job.get('url')}.values()
        logger.info(f"Found {len(unique_jobs)} unique jobs")
        
        # Analyze jobs with Claude
        high_match_jobs = []
        for job in unique_jobs:
            # Get job description (simplified - in production, scrape full description)
            job_desc = f"{job['title']} at {job['company']}"
            
            match_result = self.match_job_with_resume(job_desc, job['title'])
            job.update(match_result)
            
            # Find contacts for high-match jobs
            if match_result['match_score'] > 60:
                contacts = self.find_company_contacts(job['company'])
                job.update(contacts)
                high_match_jobs.append(job)
            
            # Rate limiting for API
            time.sleep(1)
        
        # Update Google Sheet
        if high_match_jobs:
            self.update_google_sheet(high_match_jobs)
            
            # Send Telegram summary
            summary = f"✅ *Job Search Complete*\n\n"
            summary += f"📊 Total jobs found: {len(unique_jobs)}\n"
            summary += f"🎯 High-match jobs: {len(high_match_jobs)}\n\n"
            
            # Top 3 matches
            top_jobs = sorted(high_match_jobs, key=lambda x: x['match_score'], reverse=True)[:3]
            
            summary += "*Top Matches:*\n"
            for i, job in enumerate(top_jobs, 1):
                summary += f"\n{i}. *{job['title']}* at {job['company']}\n"
                summary += f"   Match: {job['match_score']}/100\n"
                summary += f"   [Apply here]({job['url']})\n"
            
            await self.send_telegram_message(summary)
        else:
            await self.send_telegram_message("⚠️ No high-match jobs found in this run. Will try again next time.")
        
        logger.info("Job search complete")

async def main():
    """Entry point"""
    agent = JobReferralAgent()
    await agent.run_job_search()

if __name__ == "__main__":
    asyncio.run(main())
