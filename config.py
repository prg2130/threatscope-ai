import os
from dotenv import load_dotenv

load_dotenv()

# API Keys and Credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ThreatScope AI 1.0")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Bluesky / ATProtocol
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

# Database
DB_PATH = os.getenv("DB_PATH", "threatscope.db")

# Collection settings
REDDIT_SUBREDDITS = [
    "scams",
    "Scams",
    "cscareers",
    "jobs",
    "cscareerquestions",
    "recruiting",
    "techscams",
    "PersonalFinance",
]
REDDIT_POSTS_PER_SUBREDDIT = 100  # Recent posts to scan
REDDIT_SEARCH_KEYWORDS = [
    "AI recruiter",
    "fake recruiter",
    "deepfake interview",
    "synthetic recruiter",
    "voice clone job",
    "impersonation scam",
    "recruiter scam",
    "fake job offer",
]

# Classification thresholds
CONFIDENCE_THRESHOLD = "medium"  # Only report medium+ confidence
SEVERITY_MIN = "low"  # Report all severity levels

# Output settings
DASHBOARD_PORT = 8501
REPORT_OUTPUT_DIR = "./reports"

# Threat categories (aligned with framework)
THREAT_CATEGORIES = {
    "fake_recruiter_impersonation": {
        "name": "Fake Recruiter Impersonation",
        "description": "AI-generated or stolen personas posing as legitimate recruiters",
        "fist_phase": "Preparation + Promotion",
        "mitre_technique": "T1684.001",
    },
    "credential_harvesting": {
        "name": "Credential Harvesting via Fake Verification",
        "description": "Requests for sensitive data under pretense of verification",
        "fist_phase": "Engagement",
        "mitre_technique": "T1598.002",
    },
    "synthetic_endorsement": {
        "name": "AI-Powered Synthetic Endorsement",
        "description": "Deepfakes, voice clones, or LLM-generated testimonials posing as real employees",
        "fist_phase": "Promotion",
        "mitre_technique": "T1589.002",
    },
    "coordinated_behavior": {
        "name": "Coordinated Inauthentic Behavior",
        "description": "Multiple accounts discussing same fake job in coordinated pattern",
        "fist_phase": "Preparation + Promotion",
        "mitre_technique": "T1659",
    },
}

# Severity and Confidence levels
SEVERITY_LEVELS = ["low", "medium", "high"]
CONFIDENCE_LEVELS = ["low", "medium", "high"]
