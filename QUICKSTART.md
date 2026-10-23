# ThreatScope AI - Quick Start Guide

Get ThreatScope running in 5 minutes.

## Prerequisites

- Python 3.9+
- Internet connection
- Anthropic API key (free or paid)
- (Optional) Reddit API credentials

## Step 1: Clone and Setup

```bash
# Navigate to project
cd threatscope-ai

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure

```bash
# Copy template
cp .env.example .env

# Edit .env with your keys
# Required:
#   ANTHROPIC_API_KEY=your_key_from_anthropic.com
# Optional (recommended):
#   REDDIT_CLIENT_ID=your_reddit_id
#   REDDIT_CLIENT_SECRET=your_reddit_secret
#   REDDIT_USER_AGENT=ThreatScope/1.0 (by YourName)
```

## Step 3: Run the Agent

```bash
# Run full analysis pipeline
python agent.py

# This will:
# 1. Initialize database
# 2. Collect posts from Reddit and RSS feeds
# 3. Classify each post for threats
# 4. Generate intelligence brief (threat_report.md)
```

**First run note**: If you don't have Reddit credentials, the agent will skip Reddit collection but still run RSS feed analysis. That's fine for testing.

## Step 4: View Results

```bash
# Dashboard visualization
streamlit run dashboard.py

# Opens at http://localhost:8501
```

Then:
1. Go to **Overview** for key metrics
2. Click **Threat Findings** to see detected threats
3. Check **Detailed Analysis** for methodology
4. Review **Research Brief** for final report

## Step 5: Check Output

```bash
# Intelligence brief (markdown report)
cat threat_report.md

# Database (all collected data)
sqlite3 threatscope.db

# Browse posts and classifications
.tables
SELECT * FROM classifications LIMIT 5;
```

## Troubleshooting

### "No module named 'anthropic'"
```bash
pip install -r requirements.txt
```

### "Reddit credentials not found"
Reddit is optional. If you skip it, RSS feeds still work.
To enable Reddit:
1. Create app at reddit.com/prefs/apps
2. Add credentials to .env

### "anthropic.AuthenticationError"
Your ANTHROPIC_API_KEY is invalid or missing. Get it at https://console.anthropic.com/account/keys

### Streamlit won't load dashboard
```bash
# Kill any existing process
pkill -f streamlit

# Try again
streamlit run dashboard.py --logger.level=debug
```

## What to Expect

### First Run

- **Collecting data**: 2-5 minutes (depends on Reddit/RSS)
- **Classifying posts**: 5-15 minutes (Claude API calls)
- **Generating report**: 30 seconds
- **Total**: 10-30 minutes for ~100 posts

### Output

✓ **threatscope.db** - SQLite database with posts and classifications
✓ **threat_report.md** - Markdown intelligence brief
✓ **Dashboard** - Interactive visualization at localhost:8501

### Sample Finding

```
🚨 Fake Recruiter Impersonation | HIGH | REDDIT
├─ Confidence: HIGH
├─ Severity: MEDIUM
├─ Author: [reddit_user]
└─ Reasoning: Multiple signals indicate synthetic recruiter involvement
   ├─ Recent LinkedIn profile creation
   ├─ Generic job description language
   └─ Request for banking before employment
```

## Next Steps

1. **Review findings**: Check dashboard for detected threats
2. **Validate**: Manually verify high-confidence findings
3. **Customize**: Edit config.py to adjust subreddits, keywords
4. **Extend**: Add more data sources in collectors.py

## For 10a Labs Application

Package for submission:
```bash
# Create submission directory
mkdir threatscope-submission
cp -r threatscope-ai/* threatscope-submission/
cp threat_report.md threatscope-submission/
cd threatscope-submission
git init
git add .
git commit -m "ThreatScope AI: Autonomous threat intelligence research agent"
git remote add origin [your-github-repo]
git push -u origin main
```

Then reference in your application:
> "I developed an independent threat-intelligence research prototype that analyzes public reporting on AI-enabled scams, categorizes emerging tactics, and produces evidence-linked intelligence briefs. The full source code and methodology are documented in the GitHub repository above."

## Documentation

- **README.md** - Full project documentation
- **config.py** - Configuration options
- **agent.py** - Main orchestration logic
- **classifier.py** - Threat classification system
- **dashboard.py** - Streamlit visualization

## Support

For issues:
1. Check README.md
2. Review .env configuration
3. Check API key validity
4. Run with verbose logging: `python agent.py 2>&1 | tee agent.log`

---

**Ready to analyze threats?** Run `python agent.py` and check the dashboard!
