# ThreatScope AI Intelligence Brief
Research Fellow Application | 10a Labs

**Generated**: 2026-10-22 22:32:06

## Executive Summary

This report documents findings from an autonomous threat intelligence analysis of public social media discussions focusing on AI-enabled recruitment scams and related online harms.

### Key Statistics

- **Total signals reviewed**: 15
- **Threat clusters identified**: 0
- **High-priority findings**: 0
- **Medium-priority findings**: 0
- **Low-priority findings**: 15

## Threat Findings by Category

### By Threat Type


### By Confidence Level
- **LOW**: 15 findings


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

**Data Processed**: 15 posts
**Analysis Framework**: FIST + MITRE F3 Threat Classification
**Collection Period**: 2026-10-22
