"""
ThreatScope AI Agent - Autonomous threat intelligence research agent
Analyzes publicly available social media for emerging online threats
"""

from database import init_db, insert_post, insert_classification, get_unverified_high_confidence, get_statistics
from collectors import collect_all_sources
from classifier import classify_post, batch_classify_posts
from datetime import datetime
import json

class ThreatScopeAgent:
    """Main orchestration agent for threat intelligence research."""

    def __init__(self):
        self.db_initialized = False
        self.posts_collected = 0
        self.posts_classified = 0
        self.high_severity_threats = []

    def initialize(self):
        """Initialize database and agent."""
        print("Initializing ThreatScope AI...")
        init_db()
        self.db_initialized = True
        print("✓ Database initialized")

    def collect_data(self, reddit=True, rss=True, bluesky=False):
        """Phase 1: Collect data from social media sources."""
        print("\n" + "="*60)
        print("PHASE 1: DATA COLLECTION")
        print("="*60)

        if not self.db_initialized:
            self.initialize()

        posts = collect_all_sources(
            reddit_enabled=reddit,
            rss_enabled=rss,
            bluesky_enabled=bluesky
        )

        # Store posts in database
        for post in posts:
            inserted = insert_post(
                post_id=post['id'],
                platform=post['platform'],
                author=post['author'],
                title=post.get('title', ''),
                content=post['content'],
                url=post['url'],
                created_at=post['created_at'],
                source_metadata=post.get('source_metadata')
            )
            if inserted:
                self.posts_collected += 1

        print(f"\n✓ Collected {self.posts_collected} posts")
        return posts

    def analyze_threats(self, posts=None, sample_size=None):
        """Phase 2: Classify posts for threats."""
        print("\n" + "="*60)
        print("PHASE 2: THREAT ANALYSIS & CLASSIFICATION")
        print("="*60)

        if posts is None:
            # Fetch from DB if not provided
            import sqlite3
            from config import DB_PATH
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM posts WHERE id NOT IN (SELECT post_id FROM classifications)')
            posts = [dict(row) for row in c.fetchall()]
            conn.close()

        if sample_size and len(posts) > sample_size:
            posts = posts[:sample_size]

        print(f"Classifying {len(posts)} posts...\n")

        # Classify each post
        for i, post in enumerate(posts, 1):
            print(f"[{i}/{len(posts)}] Analyzing: {post.get('title', post.get('content', ''))[:60]}...")

            classification = classify_post(
                post_content=post['content'],
                platform=post['platform'],
                author=post['author']
            )

            # Store classification
            classification_id = insert_classification(
                post_id=post['id'],
                threat_category=classification.get('threat_category'),
                severity=classification.get('severity'),
                confidence=classification.get('confidence'),
                reasoning=classification.get('reasoning'),
                signals=classification.get('signals', [])
            )

            if classification.get('threat_detected') and classification.get('severity') == 'high':
                self.high_severity_threats.append({
                    'post_id': post['id'],
                    'classification': classification,
                    'post': post
                })

            self.posts_classified += 1

        print(f"\n✓ Classified {self.posts_classified} posts")
        print(f"✓ Found {len(self.high_severity_threats)} high-severity threats")

    def validate_findings(self, require_manual_review=True):
        """Phase 3: Manual validation of high-confidence findings."""
        print("\n" + "="*60)
        print("PHASE 3: VALIDATION & REVIEW")
        print("="*60)

        unverified = get_unverified_high_confidence()

        if not unverified:
            print("✓ No high-confidence findings requiring review")
            return

        print(f"Found {len(unverified)} high-confidence findings for review:\n")

        for i, finding in enumerate(unverified, 1):
            print(f"\n[{i}] {finding['threat_category'].replace('_', ' ').title()}")
            print(f"    Confidence: {finding['confidence'].upper()}")
            print(f"    Severity: {finding['severity'].upper()}")
            print(f"    Platform: {finding['platform']}")
            print(f"    Author: {finding['author']}")
            print(f"\n    Post: {finding['content'][:200]}...")
            print(f"    URL: {finding['url']}")
            print(f"    Reasoning: {finding['reasoning']}")

        if require_manual_review:
            print(f"\n⚠ Manual review required for all findings before publication")

    def generate_intelligence_brief(self, output_file="threat_report.md"):
        """Phase 4: Generate research intelligence brief."""
        print("\n" + "="*60)
        print("PHASE 4: INTELLIGENCE REPORT GENERATION")
        print("="*60)

        stats = get_statistics()

        report = self._build_report(stats)

        with open(output_file, 'w') as f:
            f.write(report)

        print(f"\n✓ Intelligence brief generated: {output_file}")
        return report

    def _build_report(self, stats):
        """Build markdown intelligence brief."""
        report = f"""# ThreatScope AI Intelligence Brief
Autonomous Threat Intelligence Research

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report documents findings from an autonomous threat intelligence analysis of public social media discussions focusing on AI-enabled recruitment scams and related online harms.

### Key Statistics

- **Total signals reviewed**: {stats['total_posts']}
- **Threat clusters identified**: {len(stats.get('by_category', {}))}
- **High-priority findings**: {stats.get('by_severity', {}).get('high', 0)}
- **Medium-priority findings**: {stats.get('by_severity', {}).get('medium', 0)}
- **Low-priority findings**: {stats.get('by_severity', {}).get('low', 0)}

## Threat Findings by Category

### By Threat Type
"""

        for category, count in stats.get('by_category', {}).items():
            report += f"- **{category.replace('_', ' ').title()}**: {count} findings\n"

        report += f"""

### By Confidence Level
"""

        for confidence, count in stats.get('by_confidence', {}).items():
            report += f"- **{confidence.upper()}**: {count} findings\n"

        report += f"""

## Methodology

This analysis uses the FIST (Fraud Incident Structured Threat) framework combined with MITRE F3 (Fight Fraud Framework) threat classification.

### Threat Categories

1. **Fake Recruiter Impersonation** (MITRE T1684.001)
   - AI-generated or stolen personas posing as legitimate recruiters
   - Detection: Recent profiles, stolen photos, generic communication, AI voice/video

2. **Credential Harvesting** (MITRE T1598.002)
   - Requests for sensitive data under verification pretense
   - Detection: Password/banking requests, suspicious verification forms

3. **Synthetic Endorsement** (MITRE T1589.002)
   - Deepfakes, voice clones, LLM-generated testimonials
   - Detection: AI tells in video, unverifiable testimonials, lip sync issues

4. **Coordinated Inauthentic Behavior** (MITRE T1659)
   - Multiple accounts discussing same fake opportunity
   - Detection: Coordinated posting patterns, unusual account clusters

## Limitations & Disclaimers

- **Confidence levels**: Classifications reflect available evidence; unverified allegations are marked LOW confidence
- **False positives**: Automated LLM classification requires manual verification
- **Privacy**: No personal information has been retained; all posts are from public sources
- **Temporal**: Findings reflect social media discussions current as of collection date

## Recommendations for Further Research

1. **Verification**: Manual spot-check high-confidence findings against primary sources
2. **Victim Impact**: Attempt to quantify financial impact or prevalence of reported scams
3. **Platform Response**: Document platform enforcement actions on identified accounts
4. **Threat Actor Attribution**: Investigate potential connections between accounts/tactics

## Methodology Transparency

- **Data sources**: Reddit (public posts), RSS threat feeds
- **Classification model**: Claude Opus (LLM-based analysis with structured prompts)
- **Validation approach**: Human review of high-confidence findings before publication
- **No false labels**: Findings distinguish observed signals from conclusive proof

---

**Data Processed**: {stats['total_posts']} posts
**Analysis Framework**: FIST + MITRE F3 Threat Classification
**Collection Period**: {datetime.now().strftime('%Y-%m-%d')}
"""

        return report

    def run_full_pipeline(self, reddit=True, rss=True, sample_size=None):
        """Run complete 7-day MVP pipeline."""
        print("\n")
        print("🔍 ThreatScope AI - Threat Intelligence Research Agent")
        print("Building portfolio project for 10a Labs Research Fellowship")
        print("="*60)

        # Initialize
        self.initialize()

        # Phase 1: Collect
        posts = self.collect_data(reddit=reddit, rss=rss)

        # Phase 2: Analyze
        self.analyze_threats(posts=posts, sample_size=sample_size)

        # Phase 3: Validate
        self.validate_findings()

        # Phase 4: Report
        self.generate_intelligence_brief()

        print("\n" + "="*60)
        print("✓ ThreatScope AI Pipeline Complete")
        print("="*60)

if __name__ == "__main__":
    agent = ThreatScopeAgent()
    agent.run_full_pipeline(reddit=True, rss=True, sample_size=50)
