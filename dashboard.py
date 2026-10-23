"""
ThreatScope AI Dashboard
Streamlit-based visualization and exploration of threat intelligence findings
"""

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from config import DB_PATH, THREAT_CATEGORIES
from database import get_statistics
import json

st.set_page_config(
    page_title="ThreatScope AI Dashboard",
    page_icon="🔍",
    layout="wide"
)

@st.cache_resource
def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_classifications(limit=100):
    """Load classifications from database."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        SELECT c.*, p.content, p.author, p.platform, p.url
        FROM classifications c
        JOIN posts p ON c.post_id = p.id
        WHERE c.threat_category IS NOT NULL
        ORDER BY c.created_at DESC
        LIMIT ?
    ''', (limit,))

    results = c.fetchall()
    conn.close()
    return results

def main():
    st.title("🔍 ThreatScope AI")
    st.subheader("Autonomous Threat Intelligence Dashboard")

    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Select View", [
            "Overview",
            "Threat Findings",
            "Detailed Analysis",
            "Research Brief"
        ])

    # Overview page
    if page == "Overview":
        st.markdown("---")

        # Key metrics
        stats = get_statistics()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Signals Reviewed",
                stats.get('total_posts', 0)
            )

        with col2:
            threat_count = sum(stats.get('by_category', {}).values())
            st.metric(
                "Threat Clusters",
                len(stats.get('by_category', {}))
            )

        with col3:
            high_count = stats.get('by_severity', {}).get('high', 0)
            st.metric(
                "High Priority",
                high_count,
                delta=None
            )

        with col4:
            medium_count = stats.get('by_severity', {}).get('medium', 0)
            st.metric(
                "Medium Priority",
                medium_count
            )

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Threats by Category")
            if stats.get('by_category'):
                category_data = pd.DataFrame(
                    list(stats['by_category'].items()),
                    columns=['Category', 'Count']
                )
                st.bar_chart(category_data.set_index('Category'))
            else:
                st.info("No classifications yet")

        with col2:
            st.subheader("Severity Distribution")
            if stats.get('by_severity'):
                severity_data = pd.DataFrame(
                    list(stats['by_severity'].items()),
                    columns=['Severity', 'Count']
                )
                st.pie_chart(severity_data.set_index('Severity')['Count'])
            else:
                st.info("No classifications yet")

        st.markdown("---")
        st.subheader("Confidence Distribution")
        if stats.get('by_confidence'):
            conf_data = pd.DataFrame(
                list(stats['by_confidence'].items()),
                columns=['Confidence', 'Count']
            )
            st.bar_chart(conf_data.set_index('Confidence'))
        else:
            st.info("No classifications yet")

    # Threat Findings page
    elif page == "Threat Findings":
        st.markdown("---")
        st.subheader("All Detected Threats")

        classifications = load_classifications(limit=100)

        if not classifications:
            st.info("No threats detected yet. Run the analysis agent to populate findings.")
        else:
            # Filter options
            col1, col2, col3 = st.columns(3)

            with col1:
                severity_filter = st.multiselect(
                    "Filter by Severity",
                    ["high", "medium", "low"],
                    default=["high", "medium"]
                )

            with col2:
                confidence_filter = st.multiselect(
                    "Filter by Confidence",
                    ["high", "medium", "low"],
                    default=["high", "medium"]
                )

            with col3:
                category_filter = st.multiselect(
                    "Filter by Category",
                    list(THREAT_CATEGORIES.keys()),
                    default=list(THREAT_CATEGORIES.keys())
                )

            # Display findings
            for classification in classifications:
                if (classification['severity'] not in severity_filter or
                    classification['confidence'] not in confidence_filter or
                    classification['threat_category'] not in category_filter):
                    continue

                threat_name = THREAT_CATEGORIES.get(
                    classification['threat_category'], {}
                ).get('name', classification['threat_category'])

                with st.expander(
                    f"🚨 {threat_name} | {classification['confidence'].upper()} | {classification['platform'].upper()}",
                    expanded=False
                ):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(f"**Severity**: {classification['severity'].upper()}")
                    with col2:
                        st.write(f"**Confidence**: {classification['confidence'].upper()}")
                    with col3:
                        st.write(f"**Verified**: {'Yes' if classification['human_verified'] else 'No'}")

                    st.write(f"**Author**: {classification['author']}")
                    st.write(f"**URL**: {classification['url']}")

                    st.markdown("**Post Content**:")
                    st.code(classification['content'][:500] + "..." if len(classification['content']) > 500 else classification['content'])

                    st.markdown("**Reasoning**:")
                    st.write(classification['reasoning'])

                    if classification['signals']:
                        try:
                            signals = json.loads(classification['signals']) if isinstance(classification['signals'], str) else classification['signals']
                            st.markdown("**Detected Signals**:")
                            for signal in signals:
                                st.write(f"- **{signal.get('signal_type', 'Unknown')}** ({signal.get('confidence', 'unknown')} confidence)")
                                st.write(f"  {signal.get('signal_text', '')}")
                        except:
                            pass

    # Detailed Analysis page
    elif page == "Detailed Analysis":
        st.markdown("---")
        st.subheader("Methodology & Framework")

        st.markdown("""
### Threat Classification Framework

**ThreatScope uses the FIST + MITRE F3 framework:**

#### 1. Fake Recruiter Impersonation (MITRE T1684.001)
- AI-generated or stolen personas
- Signals: Recent profiles, stolen photos, generic communication
- Confidence: HIGH = multiple signals; MEDIUM = 1-2 signals; LOW = single signal

#### 2. Credential Harvesting (MITRE T1598.002)
- Requests for sensitive data under verification pretense
- Signals: Password/banking requests, suspicious forms
- Typical severity: HIGH for confirmed requests, MEDIUM for suspicious patterns

#### 3. Synthetic Endorsement (MITRE T1589.002)
- Deepfakes, voice clones, LLM-generated testimonials
- Signals: AI tells in video, unverifiable testimonials
- Detection: Technical analysis + manual review

#### 4. Coordinated Inauthentic Behavior (MITRE T1659)
- Multiple accounts discussing same fake opportunity
- Signals: Coordinated posting patterns, unusual clusters
- Requires statistical analysis of temporal/spatial patterns

### Scoring System

**Severity Levels:**
- HIGH: Direct financial loss, credential theft, identity theft confirmed
- MEDIUM: Potential harm, deceptive practice confirmed
- LOW: Suspicious indicators, requires investigation

**Confidence Levels:**
- HIGH: Multiple independent signals OR technical detection
- MEDIUM: 1-2 strong signals OR pattern matches known scams
- LOW: Single signal OR innocent explanation possible

### Validation Process

All high-confidence findings are flagged for manual human review before publication to ensure:
- No false labeling of individuals
- Proper sourcing and evidence linking
- Privacy preservation
        """)

    # Research Brief page
    elif page == "Research Brief":
        st.markdown("---")
        st.subheader("Intelligence Brief")

        stats = get_statistics()

        brief = f"""
# ThreatScope AI Intelligence Brief

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Framework**: FIST + MITRE F3 Threat Classification

## Key Findings

- **Total Signals Reviewed**: {stats['total_posts']}
- **Threat Clusters Identified**: {len(stats.get('by_category', {}))}
- **High-Priority Findings**: {stats.get('by_severity', {}).get('high', 0)}

## Threats by Category
"""

        for category, count in stats.get('by_category', {}).items():
            brief += f"- {category.replace('_', ' ').title()}: {count}\n"

        brief += f"""

## Severity Distribution
"""

        for severity, count in stats.get('by_severity', {}).items():
            brief += f"- {severity.upper()}: {count}\n"

        st.markdown(brief)

        # Download button
        st.download_button(
            label="📥 Download as Markdown",
            data=brief,
            file_name=f"threatscope_brief_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
