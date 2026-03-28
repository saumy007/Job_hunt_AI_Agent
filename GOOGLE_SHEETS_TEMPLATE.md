# 📊 Google Sheets Template Structure

## Sheet Structure

Your Google Sheet will automatically be populated with the following columns:

### Column Headers (Row 1)

| Column | Description | Example |
|--------|-------------|---------|
| A - Date Added | When the job was found | 2024-03-23 10:30 |
| B - Company Name | Employer name | Jio Reality Labs |
| C - Job Title | Position title | Robotics Software Engineer |
| D - Job URL | Direct link to apply | https://... |
| E - Source | Where job was found | Naukri, LinkedIn, Instahyre |
| F - Match Score | AI-calculated fit (0-100) | 85 |
| G - Status | Application tracking | New, Applied, Interview, Rejected, Offer |
| H - CEO Name | Company CEO | Akash Ambani |
| I - CEO LinkedIn | CEO LinkedIn profile | linkedin.com/in/... |
| J - Recruiter Name | HR contact name | Priya Sharma |
| K - Recruiter Email | Recruiter email | recruiter@company.com |
| L - Recruiter LinkedIn | Recruiter LinkedIn | linkedin.com/in/... |
| M - Key Highlights | Resume points to emphasize | ROS2, Isaac Sim experience |
| N - Notes | Your personal notes | Sent connection request on 3/23 |

---

## Sample Data (What It Looks Like)

### Example Row 1
```
2024-03-23 09:15 | Nvidia | Senior Robotics Engineer | https://nvidia.com/careers/123 | LinkedIn | 92 | New | Jensen Huang | linkedin.com/in/jensenh | Sarah Johnson | sarah.j@nvidia.com | linkedin.com/in/sarahj | Isaac Sim expertise, CERN internship, ROS2 integration | Great match - apply today!
```

### Example Row 2
```
2024-03-23 09:18 | Boston Dynamics | Software Engineer - Simulation | https://bostondynamics.com/jobs/456 | Instahyre | 88 | Applied | Robert Playter | linkedin.com/in/rplayter | Mike Chen | careers@bd.com | linkedin.com/in/mikec | Unity development, Humanoid robotics, Sim-to-real | Applied on 3/23, follow up in 1 week
```

---

## Color Coding (Manual - You Can Add)

Suggested conditional formatting:

- **Match Score**:
  - 80-100: Dark Green
  - 60-79: Light Green
  - 40-59: Yellow
  - 0-39: Red

- **Status**:
  - New: White
  - Applied: Light Blue
  - Interview: Orange
  - Offer: Green
  - Rejected: Gray

---

## How to Set Up Conditional Formatting

1. Select column F (Match Score)
2. Format → Conditional Formatting
3. Add rules:
   - Greater than or equal to 80 → Dark Green background
   - Between 60 and 79 → Light Green background
   - Between 40 and 59 → Yellow background
   - Less than 40 → Red background

---

## Usage Tips

### 1. Track Your Applications

Update the "Status" column as you progress:
```
New → Applied → Interview → Offer
                      ↓
                   Rejected
```

### 2. Use Notes Column

Track all interactions:
```
"3/23: Sent LinkedIn connection request to recruiter"
"3/24: Applied via company portal"
"3/25: Recruiter accepted connection"
"3/26: Sent follow-up message"
"3/30: Interview scheduled for 4/5"
```

### 3. Filter and Sort

- Sort by Match Score (highest first)
- Filter by Status (show only "New" jobs)
- Filter by Company (track specific companies)

### 4. Create Pivot Tables

Analyze your job search:
- Jobs by Source (which platform has best matches?)
- Average Match Score by Company
- Application conversion rate

---

## Advanced: Additional Sheets

Consider adding these tabs to your workbook:

### Sheet 2: "Application Tracker"
Track detailed application progress:
- Date Applied
- Interview Rounds
- Assessments
- References
- Offer Details

### Sheet 3: "Contact Log"
Log all communications:
- Date
- Person Contacted
- Method (LinkedIn, Email, Phone)
- Response
- Next Action

### Sheet 4: "Company Research"
Deep dive on target companies:
- Company Name
- Industry
- Size
- Funding
- Culture Notes
- Employee Reviews

### Sheet 5: "Referral Network"
Track potential referrers:
- Name
- Company
- Connection Strength
- Last Contact
- Willing to Refer?

---

## API Integration Details

The agent updates the sheet using Google Sheets API v4:

```python
# Header creation (first run only)
headers = [
    'Date Added', 'Company Name', 'Job Title', 'Job URL', 'Source',
    'Match Score', 'Status', 'CEO Name', 'CEO LinkedIn',
    'Recruiter Name', 'Recruiter Email', 'Recruiter LinkedIn',
    'Key Highlights', 'Notes'
]

# Data appending (each job)
row = [
    datetime.now().strftime('%Y-%m-%d %H:%M'),
    job['company'],
    job['title'],
    job['url'],
    job['source'],
    job['match_score'],
    'New',
    job['ceo_name'],
    job['ceo_linkedin'],
    job['recruiter_name'],
    job['recruiter_email'],
    job['recruiter_linkedin'],
    ', '.join(job['key_highlights']),
    ''
]
```

---

## Data Privacy

**Important**: This sheet contains sensitive data:
- Personal job search strategy
- Contact information
- Application history

**Security recommendations**:
1. Don't share the sheet publicly
2. Only share with service account (for the agent)
3. Regularly review access permissions
4. Consider enabling 2FA on your Google account

---

## Backup Strategy

1. **Automatic Backups**:
   - Google Sheets auto-saves
   - View version history: File → Version History

2. **Manual Backups**:
   - File → Download → Excel (.xlsx)
   - Save locally weekly
   - Keep in Google Drive backup folder

3. **Export Options**:
   - CSV (for data analysis in Python/R)
   - PDF (for printing/sharing)
   - Excel (for offline work)

---

## Troubleshooting

### Issue: Duplicate entries

**Solution**: The agent checks URLs to avoid duplicates, but if you see duplicates:
```python
# Manual deduplication in Google Sheets
Data → Remove duplicates → Select "Job URL" column
```

### Issue: Formatting breaks

**Solution**: 
- The agent appends rows without formatting
- Reapply conditional formatting rules after large updates
- Consider creating a "template row" and copying formatting down

### Issue: Too many rows

**Solution**:
- Archive old data to separate sheet monthly
- Keep only active applications in main sheet
- Use filters to hide irrelevant jobs

---

## Integration with Other Tools

### Export to Notion
1. Download as CSV
2. Import to Notion database
3. Use Notion's Kanban view for application tracking

### Export to Airtable
1. Airtable can import Google Sheets directly
2. Link: Airtable → Add Base → Import → From Google Sheets

### Export to Excel
1. Download as .xlsx
2. Use Excel's Power Query for advanced analysis
3. Create charts and dashboards

---

## Pro Tips

1. **Daily Review**: Check new entries every morning
2. **Quick Apply**: Apply to 80+ match scores immediately
3. **Follow Up**: Set reminders for recruiter follow-ups (use Notes)
4. **Network**: Reach out to employees before applying
5. **Customize**: Add custom columns for your needs

---

**Your job search data is now organized and actionable! 🎯**
