# 🤖 AI Job Referral Agent - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Telegram Bot Setup](#telegram-bot-setup)
3. [Google Sheets Setup](#google-sheets-setup)
4. [Anthropic API Setup](#anthropic-api-setup)
5. [GitHub Repository Setup](#github-repository-setup)
6. [Testing Locally](#testing-locally)
7. [Deploying to GitHub Actions](#deploying-to-github-actions)
8. [Troubleshooting](#troubleshooting)

---

## 🛠️ Prerequisites

- Gmail account (for Google Sheets)
- Telegram account
- GitHub account
- Anthropic API access (free tier available)

---

## 📱 Telegram Bot Setup

### Step 1: Create Your Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts:
   - Choose a name (e.g., "My Job Search Assistant")
   - Choose a username (e.g., "my_job_search_bot")
4. **IMPORTANT**: Copy the API token (looks like: `8573462686:AAGCngmEjpo0uA2HjQDxagCG4c9gpqJFRnQ`)
5. **CRITICAL SECURITY**: 
   - ✅ Store this token securely
   - ❌ Never share it publicly
   - ❌ Never commit it to GitHub directly

### Step 2: Get Your Chat ID

1. Start a conversation with your new bot
2. Send any message (e.g., "Hello")
3. Open this URL in browser (replace YOUR_BOT_TOKEN):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":123456789}` - that's your chat ID
5. Copy the numeric chat ID

**Alternative Method:**
1. Search for `@userinfobot` on Telegram
2. Send it any message
3. It will reply with your user ID (this is your chat ID)

---

## 📊 Google Sheets Setup

### Step 1: Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "Job Search Agent")
3. Enable Google Sheets API:
   - Navigation Menu → APIs & Services → Library
   - Search "Google Sheets API" → Enable
4. Enable Google Drive API:
   - Search "Google Drive API" → Enable

### Step 2: Create Service Account Credentials

1. Navigation Menu → APIs & Services → Credentials
2. Click "Create Credentials" → "Service Account"
3. Fill details:
   - Name: "job-agent-service"
   - Role: Editor
   - Click "Done"
4. Click on the created service account
5. Go to "Keys" tab
6. Click "Add Key" → "Create New Key" → JSON
7. **Download the JSON file** - you'll need this entire content

### Step 3: Set Up Your Google Sheet

1. Open your existing sheet: [Your Sheet Link](https://docs.google.com/spreadsheets/d/1WV8O_gC4RU9O4Yrg05NKwtViQ-vua4qcbX7y7BXGTs0/edit)
2. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS_IS_THE_SHEET_ID]/edit
   ```
   Your ID: `1WV8O_gC4RU9O4Yrg05NKwtViQ-vua4qcbX7y7BXGTs0`

3. **Share the sheet with service account:**
   - Click "Share" button in your sheet
   - Paste the service account email (from JSON file, looks like: `job-agent-service@project-id.iam.gserviceaccount.com`)
   - Give "Editor" permissions
   - Uncheck "Notify people"
   - Click "Share"

### Step 4: Prepare Sheet Headers

The agent will auto-create headers, but you can manually add these columns:

| Date Added | Company Name | Job Title | Job URL | Source | Match Score | Status | CEO Name | CEO LinkedIn | Recruiter Name | Recruiter Email | Recruiter LinkedIn | Key Highlights | Notes |

---

## 🔑 Anthropic API Setup

### Option 1: Free Tier (Recommended for testing)

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up with your email
3. Go to "API Keys" section
4. Create new API key
5. **Copy the key** (starts with `sk-ant-...`)
6. Free tier includes $5 credit (sufficient for ~200 job analyses)

### Option 2: Paid Plan

- If you need more usage, add payment method
- Pay-as-you-go pricing: ~$0.03 per job analysis

---

## 🐙 GitHub Repository Setup

### Step 1: Create Repository

1. Go to [GitHub](https://github.com)
2. Click "New Repository"
3. Name it: `job-referral-agent`
4. Make it **Private** (recommended)
5. Click "Create Repository"

### Step 2: Upload Code

**Option A: Using Git Command Line**

```bash
# Clone this repository or download the files
git clone <this-repo-url>
cd job-referral-agent

# Initialize git (if not already)
git init

# Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USERNAME/job-referral-agent.git

# Commit and push
git add .
git commit -m "Initial commit: AI Job Referral Agent"
git push -u origin main
```

**Option B: Using GitHub Web Interface**

1. Click "uploading an existing file"
2. Drag and drop all files:
   - `job_referral_agent.py`
   - `requirements.txt`
   - `.github/workflows/job_search.yml`
   - `.env.example`
   - `README.md` (this file)
3. Commit changes

### Step 3: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Navigate to "Secrets and variables" → "Actions"
4. Click "New repository secret" for each:

| Secret Name | Value | Where to Get It |
|------------|-------|-----------------|
| `TELEGRAM_BOT_TOKEN` | Your bot token | From BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID | From getUpdates or userinfobot |
| `ANTHROPIC_API_KEY` | Your Claude API key | From Anthropic Console |
| `GOOGLE_SHEET_ID` | Your sheet ID | From sheet URL |
| `GOOGLE_CREDENTIALS` | Entire JSON content | From downloaded JSON file |

**For GOOGLE_CREDENTIALS:**
- Open the downloaded JSON file in a text editor
- Copy the **ENTIRE** content (including `{` and `}`)
- Paste it as the secret value
- It should look like:
  ```json
  {
    "type": "service_account",
    "project_id": "your-project",
    "private_key_id": "...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...",
    ...
  }
  ```

---

## 🧪 Testing Locally (Optional)

Before deploying to GitHub Actions, test locally:

### Step 1: Set Up Local Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create .env File

```bash
# Copy example
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use any text editor
```

### Step 3: Run the Agent

```bash
python job_referral_agent.py
```

Expected output:
```
INFO - Starting job search...
INFO - Scraped 5 jobs from Naukri
INFO - Scraped 3 jobs from LinkedIn
INFO - Found 8 unique jobs
INFO - Added 3 jobs to Google Sheet
INFO - Telegram message sent successfully
INFO - Job search complete
```

---

## 🚀 Deploying to GitHub Actions

### Step 1: Enable GitHub Actions

1. Go to your repository
2. Click "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"

### Step 2: Verify Workflow File

- Check that `.github/workflows/job_search.yml` exists
- The workflow is set to run every 6 hours automatically
- You can also trigger it manually

### Step 3: Manual Test Run

1. Go to "Actions" tab
2. Click "AI Job Referral Agent" workflow
3. Click "Run workflow" dropdown
4. Click "Run workflow" button
5. Wait 2-3 minutes
6. Check Telegram for notification

### Step 4: Monitor Runs

- View run history in "Actions" tab
- Check logs by clicking on specific run
- Get Telegram notifications after each run

---

## 🎯 Customization

### Adjust Search Parameters

Edit `job_referral_agent.py`:

```python
self.search_params = {
    'titles': [
        'Software Engineer',      # Add/remove job titles
        'Robotics Engineer',
        'ML Engineer'
    ],
    'locations': [
        'Remote',                  # Add/remove locations
        'Bengaluru',
        'Mumbai'
    ],
    'keywords': [
        'Python',                  # Add/remove keywords
        'ROS',
        'AI'
    ]
}
```

### Adjust Schedule

Edit `.github/workflows/job_search.yml`:

```yaml
schedule:
  # Every 6 hours
  - cron: '0 */6 * * *'
  
  # Daily at 9 AM IST (3:30 AM UTC)
  # - cron: '30 3 * * *'
  
  # Twice daily (9 AM and 6 PM IST)
  # - cron: '30 3,12 * * *'
```

### Adjust Match Threshold

Edit `job_referral_agent.py`:

```python
# Current: Jobs with 60%+ match
if match_result['match_score'] > 60:

# More selective (70%+):
if match_result['match_score'] > 70:

# Less selective (50%+):
if match_result['match_score'] > 50:
```

---

## 🐛 Troubleshooting

### Issue: No Telegram notifications

**Solution:**
1. Verify bot token is correct
2. Ensure you've sent at least one message to the bot
3. Check chat ID is numeric (not string)
4. Look at GitHub Actions logs for error messages

### Issue: Google Sheets not updating

**Solution:**
1. Verify sheet is shared with service account email
2. Check GOOGLE_CREDENTIALS is valid JSON
3. Ensure Google Sheets API is enabled
4. Verify sheet ID is correct

### Issue: No jobs found

**Solution:**
1. Check internet connectivity
2. Job boards might be blocking requests - add delays
3. Adjust search parameters (broader terms)
4. Check website structure hasn't changed

### Issue: Claude API errors

**Solution:**
1. Verify API key is valid
2. Check usage limits (free tier: $5 credit)
3. Add error handling for rate limits
4. Monitor API usage in console

### Issue: GitHub Actions failing

**Solution:**
1. Check all secrets are set correctly
2. View detailed logs in Actions tab
3. Ensure requirements.txt has all dependencies
4. Check workflow file syntax

---

## 📊 Expected Costs

### Free Tier (Recommended for MVP)

- **GitHub Actions**: 2000 minutes/month (sufficient for 24 runs/day)
- **Anthropic Claude**: $5 free credit (~200 job analyses)
- **Google Sheets API**: Free up to 500 requests/minute
- **Telegram Bot API**: Free unlimited

**Total**: $0/month (until free credits exhausted)

### After Free Tier

- **Claude API**: ~$0.03 per job analysis
- **GitHub Actions**: Free for public repos, $0.008/minute for private
- If analyzing 50 jobs/day: ~$45/month

### Cost Reduction Tips

1. Increase match score threshold (fewer API calls)
2. Run less frequently (2-3 times/day)
3. Use cheaper Claude Haiku model for initial screening
4. Cache results to avoid re-analyzing same jobs

---

## 🔒 Security Best Practices

1. **Never commit secrets to Git**
   - Use `.gitignore` to exclude `.env`
   - Always use GitHub Secrets

2. **Revoke compromised tokens immediately**
   - Telegram: `/revoke` in BotFather
   - Anthropic: Delete key in console
   - Google: Revoke service account

3. **Use private GitHub repository**
   - Your job search data is personal
   - API keys stored as secrets

4. **Regularly rotate API keys**
   - Every 3-6 months
   - After any suspected exposure

---

## 📈 Next Steps / Future Enhancements

- [ ] Add email automation for direct outreach
- [ ] LinkedIn profile scraping for mutual connections
- [ ] Application tracking (applied, interview, rejected)
- [ ] Custom email templates based on job match
- [ ] Resume tailoring suggestions per job
- [ ] Interview preparation tips
- [ ] Salary data aggregation
- [ ] Company culture research
- [ ] Referral request automation

---

## 🆘 Support

If you encounter issues:

1. Check this README thoroughly
2. Review GitHub Actions logs
3. Test locally first
4. Check API rate limits
5. Verify all credentials are correct

---

## 📄 License

MIT License - Feel free to modify and use for your job search!

---

**Good luck with your job search! 🚀**
