# ⚡ Quick Start Guide - Get Running in 15 Minutes

## 🎯 Goal
Get your AI job referral agent running on GitHub Actions in 15 minutes.

---

## ✅ Checklist (Complete in Order)

### [ ] Step 1: Telegram Bot (3 minutes)
1. Open Telegram → Search `@BotFather`
2. Send `/newbot` //8573462686:AAHXnXxfRJ5kCbPGQM8tRlVt9ke_17CEdnM
3. Name: "Job Search Bot" 
4. Username: "your_unique_job_bot"
5. **Copy the token** → Save in Notes app
6. Search `@userinfobot` → Send any message 
'''
//@rapchiko
Id: 951885353
First: sam
Lang: en
Registered: Check Date (https://t.me/m/ECxXXcW-YWM0)

🧠 Explanations and answers
Free AI → DeepSeek (https://t.me/deepseek_gidbot) & ChatGPT (https://t.me/chatgpt_gidbot)

🖼 Visualize your ideas
Make Image → NanoBanana (https://t.me/nanobanana_gidbot)

'''
7. **Copy your chat ID** → Save in Notes app

### [ ] Step 2: Google Sheets (5 minutes)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project: "Job Agent"
3. Enable APIs:
   - Google Sheets API
   - Google Drive API
4. Create Service Account:
   - Credentials → Create → Service Account
   - Name: "job-agent"
   - Download JSON key
5. Open your Google Sheet
6. Click Share → Add service account email (from JSON)
7. Give "Editor" access
8. **Copy Sheet ID** from URL → Save in Notes //(job-hunt@jobhunt-491019.iam.gserviceaccount.com)

### [ ] Step 3: Anthropic API (2 minutes)
1. Go to [console.anthropic.com](https://console.anthropic.com/) 
2. Sign up / Log in
3. API Keys → Create Key
4. **Copy the key** → Save in Notes

### [ ] Step 4: GitHub Setup (5 minutes)
1. Create repository: `job-referral-agent`
2. Upload files:
   - `job_referral_agent.py`
   - `requirements.txt`
   - `.github/workflows/job_search.yml`
3. Go to Settings → Secrets → Actions
4. Add secrets (from your Notes):
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID
   - `ANTHROPIC_API_KEY`: Your Claude key
   - `GOOGLE_SHEET_ID`: Your sheet ID
   - `GOOGLE_CREDENTIALS`: Entire JSON content (copy all)

### [ ] Step 5: Test Run (2 minutes)
1. Go to Actions tab
2. Click "AI Job Referral Agent"
3. Run workflow → Run workflow
4. Wait 2 minutes
5. **Check Telegram** for notification! 🎉

---

## 🚨 Common Issuesz

### "Google Sheets permission denied"
→ Did you share the sheet with the service account email?

### "Telegram error"
→ Did you start a chat with your bot first?

### "No jobs found"
→ Normal! Try adjusting search parameters in code

### "Claude API error"
→ Check API key is correct and has credit

---

## 🎊 Success!

If you got a Telegram message with job results, you're done! 

The agent will now run automatically every 6 hours.

---

## 📞 Next Actions

1. **Customize search**: Edit `job_referral_agent.py` (line 45)
2. **Change schedule**: Edit `.github/workflows/job_search.yml` (line 5)
3. **Add more features**: See README.md

---

**Total time**: ~15 minutes  
**Monthly cost**: $0 (free tier)  
**Jobs tracked**: Unlimited

🚀 Happy job hunting!
