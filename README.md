# ThreatScope AI - Autonomous Threat Intelligence Research Agent

**An independent threat intelligence research tool that analyzes public social media discussions to identify AI-enabled recruitment scams and coordinated inauthentic behavior.**

This project demonstrates research methodology, threat analysis, and operational intelligence production for the 10a Labs Research Fellow position.

## Overview

ThreatScope AI monitors publicly available social media posts (Reddit, RSS feeds, Bluesky) to identify emerging threats related to:

1. **Fake Recruiter Impersonation** - AI-generated personas posing as legitimate recruiters
2. **Credential Harvesting** - Requests for sensitive data under pretense of verification
3. **Synthetic Endorsement** - Deepfakes, voice clones, or LLM-generated testimonials
4. **Coordinated Inauthentic Behavior** - Multiple accounts promoting the same fraudulent opportunity

## Research Framework

ThreatScope uses the **FIST + MITRE F3 Framework** for threat classification:

- **FIST**: Four-phase operational model (Preparation → Promotion → Engagement → Concealment)
- **MITRE F3**: Fight Fraud Framework with specific tactics and techniques for financial fraud
- **Custom AI Extensions**: Deepfake detection, LLM pattern recognition, synthetic content identification

## Architecture

```
ThreatScope AI
├── Collectors (data extraction)
│   ├── Reddit API
│   ├── RSS Feeds
│   └── Bluesky (AT Protocol)
│
├── Classifier (AI-powered analysis)
│   └── Claude Opus (LLM-based threat classification)
│
├── Database (SQLite)
│   ├── Posts
│   ├── Classifications
│   ├── Signals (extracted evidence)
│   └── Research Briefs
│
├── Dashboard (Streamlit)
│   ├── Overview
│   ├── Threat findings
│   ├── Analysis methodology
│   └── Intelligence brief
│
└── Agent (orchestration)
    ├── Phase 1: Data Collection
    ├── Phase 2: Threat Analysis
    ├── Phase 3: Human Validation
    └── Phase 4: Intelligence Reporting
```

## Quick Start

### 1. Setup

```bash
cd threatscope-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with:
- **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com
- **REDDIT_CLIENT_ID** & **REDDIT_CLIENT_SECRET**: Get from https://www.reddit.com/prefs/apps

### 3. Run the Agent

```bash
python agent.py
```

This runs the full pipeline:
1. Collects posts from Reddit and RSS feeds
2. Classifies each post for threats
3. Validates high-confidence findings
4. Generates intelligence brief

### 4. View the Dashboard

```bash
streamlit run dashboard.py
```

Opens at `http://localhost:8501`

## 7-Day MVP Plan

| Day | Task | Deliverable |
|-----|------|------------|
| 1 | Define threat taxonomy and research questions | Threat framework document |
| 2 | Implement API collectors (Reddit, RSS) | 500+ public posts in database |
| 3 | Build LLM classifier with confidence scoring | Classification schema, test results |
| 4 | Create Streamlit dashboard | Interactive visualization |
| 5 | Human validation workflow | Review process, ground truth |
| 6 | Generate intelligence brief | 2-page research report |
| 7 | Publish GitHub repo + demo | Documented, runnable project |

## Key Features

### Data Collection
- **Reddit API**: Subreddit monitoring + keyword search
- **RSS Feeds**: Security news aggregation (BleepingComputer, SecurityOnline)
- **Extensible**: Easy to add Bluesky, Twitter, other sources

### Threat Classification
- **LLM-Powered**: Claude Opus analyzes posts using structured threat framework
- **Confidence Scoring**: HIGH/MEDIUM/LOW confidence levels with evidence
- **Signal Extraction**: Automatically identifies and documents threat indicators

### Human-In-The-Loop Validation
- High-confidence findings flagged for manual review
- Evidence-linked reasoning for every classification
- Manual verification before publication

### Operational Intelligence
- **Threat Dashboard**: Real-time visualization of findings
- **Research Brief**: Markdown intelligence report with methodology
- **Evidence Preservation**: All posts, classifications, and signals stored for audit

## Threat Taxonomy

### 1. Fake Recruiter Impersonation (MITRE T1684.001)

**Definition**: AI-generated or stolen personas posing as legitimate recruiters

**Detection Signals**:
- Recently created LinkedIn profile with stolen/generated photos
- Inconsistent communication patterns (too generic or unnaturally polished)
- Job descriptions with unusual phrasing patterns
- AI-generated voice or video in interviews
- Company website/LinkedIn does not match recruiter claims

**Confidence Scoring**:
- **HIGH**: Multiple independent signals
- **MEDIUM**: 1-2 signals or pattern matches known scams
- **LOW**: Single signal or innocent explanation possible

### 2. Credential Harvesting (MITRE T1598.002)

**Definition**: Requests for sensitive data (SSN, banking info, passwords) under pretense of verification

**Detection Signals**:
- Password or banking information requested before employment starts
- "Verify identity" forms requesting PII beyond standard hiring
- Links to suspicious verification websites
- Urgency language ("verify within 24 hours")

**Severity**:
- **HIGH**: Direct credential theft confirmed
- **MEDIUM**: Social engineering attempt observed
- **LOW**: Suspicious but unverified

### 3. Synthetic Endorsement (MITRE T1589.002)

**Definition**: Deepfakes, voice clones, or LLM-generated testimonials posing as real employees

**Detection Signals**:
- Video interview with subtle AI tells (blinking patterns, lip sync issues)
- Voice cloning detected in call recordings
- Employee testimonials that cannot be verified on company LinkedIn
- Generic positive language matching LLM output patterns

**Confidence**:
- **HIGH**: Technical detection of deepfake or voice cloning
- **MEDIUM**: Human review suspects synthesis
- **LOW**: Unverifiable but plausible

### 4. Coordinated Inauthentic Behavior (MITRE T1659)

**Definition**: Multiple accounts discussing the same fake job opportunity in coordinated pattern

**Detection Signals**:
- Same job posting across multiple platforms within hours
- Similar user profiles promoting same opportunity
- Posting timestamps suggest coordination rather than organic discovery
- Unusual account creation patterns (newly created accounts)

**Confidence**:
- **HIGH**: Statistical anomalies detected
- **MEDIUM**: Suspicious clustering observed
- **LOW**: Could be coincidental

## Limitations & Disclaimers

### Important

1. **Unverified**: This is a research tool analyzing publicly available discussions. Classifications represent observed patterns, not conclusive proof.

2. **No Personal Identification**: The tool does not attempt to identify individuals. Findings are about patterns, tactics, and indicators.

3. **False Positives**: Automated classification requires manual validation. Some findings flagged as suspicious may be legitimate.

4. **Privacy**: No personal data is retained. All analysis is based on public posts.

5. **Temporal**: Findings reflect the state of social media at collection time. Threat actors evolve tactics.

## Publication Standards

Before publishing findings:

1. **Human Review**: All high-confidence findings are manually verified
2. **Evidence Linking**: Every classification includes source citations
3. **Confidence Transparency**: Explicitly state confidence levels and limitations
4. **Privacy Protection**: No personal information published
5. **Methodology Disclosure**: Full documentation of analysis approach

## Project Structure

```
threatscope-ai/
├── agent.py              # Main orchestration agent
├── classifier.py         # LLM-based threat classification
├── collectors.py         # Data collection (Reddit, RSS, etc.)
├── database.py           # SQLite schema and operations
├── dashboard.py          # Streamlit visualization
├── config.py             # Configuration and constants
├── requirements.txt      # Python dependencies
├── .env.example          # Configuration template
├── README.md             # This file
├── threatscope.db        # SQLite database (created on first run)
└── reports/              # Generated intelligence briefs
```

## API Keys & Setup

### Anthropic API (Required)

1. Sign up: https://console.anthropic.com
2. Create API key: https://console.anthropic.com/account/keys
3. Add to `.env`: `ANTHROPIC_API_KEY=your_key`

### Reddit API (Recommended)

1. Create app: https://www.reddit.com/prefs/apps
2. Get credentials:
   - Client ID (under app name)
   - Client Secret
3. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USER_AGENT=ThreatScope/1.0 (by YourUsername)
   ```

### Optional: Bluesky

Create account at https://bsky.app and add credentials to `.env`

## Output & Reporting

### Database
- **posts**: Collected social media posts
- **classifications**: AI-generated threat classifications
- **signals**: Extracted evidence for each classification
- **research_briefs**: Generated intelligence reports

### Intelligence Brief

Generated as markdown with:
- Executive summary
- Threat findings by category
- Methodology and framework
- Limitations and disclaimers
- Recommendations for further research

## Example: AI-Enabled Recruitment Scam

**Scenario**: A Reddit post describes a suspicious job interview process

**ThreatScope Analysis**:

```
Threat Category: Fake Recruiter Impersonation
Severity: MEDIUM
Confidence: HIGH

Reasoning: Multiple signals indicate synthetic recruiter involvement

Signals Detected:
1. LinkedIn profile created 2 weeks ago (HIGH confidence)
2. "Interview" via AI video call platform (MEDIUM confidence)
3. Generic job description language patterns (MEDIUM confidence)
4. Request for banking information before employment (HIGH confidence)

Recommendation: Manual review and potential platform reporting
```

## For 10a Labs Application

This project demonstrates:

1. **Research Methodology**: FIST + MITRE F3 framework applied systematically
2. **Technical Implementation**: Operational system collecting, analyzing, and reporting threats
3. **Transparency**: Evidence-linked reasoning, confidence scoring, methodology disclosure
4. **Safety**: Human-in-the-loop validation, no false labeling
5. **Relevance**: Focus on emerging AI misuse and online harms

## Contributing & Future Work

### Potential Extensions

- [ ] Deepfake detection with technical analysis (computer vision)
- [ ] Voice cloning detection (audio analysis)
- [ ] Cross-platform graph analysis (LinkedIn → WhatsApp → payment sites)
- [ ] Threat actor attribution (organizational pattern matching)
- [ ] Real-time monitoring with webhook notifications
- [ ] Integration with abuse reporting systems

### Design Principles

- **Conservatively**: Err on the side of LOW confidence when uncertain
- **Transparently**: Document all assumptions and limitations
- **Ethically**: Protect privacy, avoid false labeling
- **Operationally**: Produce actionable intelligence, not speculation

## References

1. **FIST Framework**: Fraud Incident Structured Threat Modeling (arxiv 2025)
2. **MITRE F3**: Fight Fraud Framework (attack.mitre.org)
3. **NIST**: Cybersecurity & AI Framework (NIST IR 8596)
4. **Stanford Internet Observatory**: Coordinated inauthentic behavior research
5. **DHS**: AI-enabled threat assessments

## License

MIT License - See LICENSE file

## Author

Built for 10a Labs Research Fellow Application
Research focus: AI safety, online threat intelligence, information integrity

---

**Questions?** This project aims to demonstrate research rigor, operational security, and ethical AI deployment. The methodology is documented for reproducibility and external validation.
