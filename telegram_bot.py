#!/usr/bin/env python3
"""
Enhanced Telegram Bot Interface for Job Referral Agent
Supports interactive commands: /search, /status, /help, /stats
"""

import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

from job_referral_agent import JobReferralAgent

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramJobBot:
    def __init__(self):
        self.agent = JobReferralAgent()
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 *Welcome to Your AI Job Referral Agent!*

I help you find relevant software engineering jobs and connect with recruiters.

*Available Commands:*
/search - Start a new job search
/status - Check current search status
/stats - View your job search statistics
/help - Show this help message

*Automatic Features:*
✅ Searches job boards every 6 hours
✅ AI-powered resume matching
✅ Finds company contacts
✅ Updates your Google Sheet
✅ Sends you instant notifications

Ready to find your dream job? Try `/search` now!
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 *Help - Command Guide*

*🔍 /search*
Manually trigger a job search across:
- Naukri.com
- LinkedIn Jobs  
- Instahyre
- (More sources coming soon!)

*📊 /status*
Check:
- Last search time
- Jobs found in last run
- System status

*📈 /stats*
View statistics:
- Total jobs tracked
- High-match jobs (80%+)
- Applications pending
- Success rate

*💡 /help*
Show this help message

*Settings:*
To customize your job search parameters, edit the config in GitHub repository.

Need more help? Check the README.md in your repo!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command - trigger manual job search"""
        await update.message.reply_text("🔍 Starting job search... This may take 2-3 minutes.")
        
        try:
            # Run job search
            await self.agent.run_job_search()
            await update.message.reply_text("✅ Job search complete! Check your Google Sheet for results.")
        except Exception as e:
            logger.error(f"Search error: {e}")
            await update.message.reply_text(f"❌ Search failed: {str(e)}\n\nPlease check logs or try again later.")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        try:
            # Get stats from Google Sheet
            if self.agent.sheet:
                all_values = self.agent.sheet.get_all_values()
                total_jobs = len(all_values) - 1  # Exclude header
                
                # Count by status
                status_counts = {}
                for row in all_values[1:]:  # Skip header
                    if len(row) > 6:
                        status = row[6]  # Status column
                        status_counts[status] = status_counts.get(status, 0) + 1
                
                status_message = f"""
📊 *Current Status*

*Total Jobs Tracked:* {total_jobs}

*By Status:*
- New: {status_counts.get('New', 0)}
- Applied: {status_counts.get('Applied', 0)}  
- Interview: {status_counts.get('Interview', 0)}
- Offer: {status_counts.get('Offer', 0)}
- Rejected: {status_counts.get('Rejected', 0)}

*Last Updated:* {datetime.now().strftime('%Y-%m-%d %H:%M')}

Use /search to find more jobs!
                """
                await update.message.reply_text(status_message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Could not connect to Google Sheet. Check your setup.")
        except Exception as e:
            logger.error(f"Status error: {e}")
            await update.message.reply_text(f"❌ Error retrieving status: {str(e)}")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - detailed statistics"""
        try:
            if self.agent.sheet:
                all_values = self.agent.sheet.get_all_values()
                
                if len(all_values) <= 1:
                    await update.message.reply_text("📊 No jobs tracked yet. Run `/search` to get started!", parse_mode='Markdown')
                    return
                
                total_jobs = len(all_values) - 1
                
                # Calculate average match score
                match_scores = []
                high_match = 0
                medium_match = 0
                low_match = 0
                
                sources = {}
                companies = {}
                
                for row in all_values[1:]:
                    if len(row) > 5:
                        # Match score (column F)
                        try:
                            score = int(row[5])
                            match_scores.append(score)
                            if score >= 80:
                                high_match += 1
                            elif score >= 60:
                                medium_match += 1
                            else:
                                low_match += 1
                        except:
                            pass
                        
                        # Source tracking (column E)
                        if len(row) > 4:
                            source = row[4]
                            sources[source] = sources.get(source, 0) + 1
                        
                        # Company tracking (column B)
                        if len(row) > 1:
                            company = row[1]
                            companies[company] = companies.get(company, 0) + 1
                
                avg_match = sum(match_scores) / len(match_scores) if match_scores else 0
                
                # Top companies
                top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]
                
                stats_message = f"""
📈 *Detailed Statistics*

*Overview:*
- Total Jobs: {total_jobs}
- Average Match: {avg_match:.1f}%

*Match Distribution:*
- High (80%+): {high_match} jobs 🎯
- Medium (60-79%): {medium_match} jobs ⭐
- Low (<60%): {low_match} jobs

*Jobs by Source:*
"""
                for source, count in sources.items():
                    stats_message += f"- {source}: {count}\n"
                
                stats_message += "\n*Top Companies:*\n"
                for company, count in top_companies:
                    stats_message += f"- {company}: {count}\n"
                
                stats_message += f"\n*Last Updated:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                await update.message.reply_text(stats_message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Could not connect to Google Sheet.")
        except Exception as e:
            logger.error(f"Stats error: {e}")
            await update.message.reply_text(f"❌ Error calculating stats: {str(e)}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        
        # Create application
        application = Application.builder().token(self.telegram_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("search", self.search_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Start bot
        logger.info("Bot is running! Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramJobBot()
    bot.run()
