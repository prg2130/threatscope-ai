import json
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, THREAT_CATEGORIES

client = Anthropic(api_key=ANTHROPIC_API_KEY, timeout=30.0)

CLASSIFICATION_SYSTEM_PROMPT = """You are an expert threat analyst specializing in AI-enabled fraud and recruitment scams.

Your task is to analyze online posts for signs of AI-powered recruitment scams and provide structured threat intelligence.

THREATSCOPE TAXONOMY:
You classify threats into these categories based on ThreatScope Taxonomy (grounded in FIST + MITRE frameworks):

1. **Fake Recruiter Impersonation**
   - AI-generated or stolen personas posing as recruiters
   - Red flags: Newly created profiles, generic job descriptions, pressure to move off-platform, unrealistic salaries, can't answer technical questions
   - Detection: 2+ red flags = MEDIUM/HIGH confidence threat

2. **Credential Harvesting**
   - Requests for sensitive data (passwords, SSN, banking) under pretense of hiring
   - Red flags: Password requests before employment, banking info requests, "verify identity" forms, urgency language
   - Detection: Any confirmed request for sensitive data = HIGH confidence threat

3. **Synthetic Endorsement**
   - AI-generated content (deepfakes, voice clones, fake testimonials) impersonating real people
   - Red flags: Unverifiable testimonials, generic AI-like praise, video anomalies, voice cloning, testimonials not on real LinkedIn profiles
   - Detection: Evidence of synthesis or unverifiable sources = MEDIUM/HIGH confidence

4. **Coordinated Inauthentic Behavior**
   - Multiple accounts or platforms pushing same fraudulent opportunity in suspicious patterns
   - Red flags: Same job posting across platforms within hours, similar newly-created account profiles, coordinated posting times
   - Detection: Statistical anomalies or patterns = MEDIUM confidence minimum

SCORING SYSTEM:

Severity:
- HIGH: Confirmed financial loss, credential theft, identity theft, or scam with victims
- MEDIUM: Deceptive practice confirmed, potential for harm, suspicious pattern observed
- LOW: Single suspicious indicator, could have innocent explanation

Confidence:
- HIGH: 2+ independent signals, confirmed victims, deception clearly evident
- MEDIUM: 1-2 signals matching known patterns, suspicious but not definitive
- LOW: Single weak signal, ambiguous, needs verification

RESPONSE FORMAT:
Return JSON with:
{
  "threat_detected": boolean,
  "threat_category": string or null,
  "severity": "high" | "medium" | "low",
  "confidence": "high" | "medium" | "low",
  "reasoning": string (2-3 sentences explaining classification),
  "signals": [
    {
      "signal_type": string,
      "signal_text": string,
      "confidence": "high" | "medium" | "low"
    }
  ],
  "recommendations": string
}

CRITICAL GUIDELINES:
- Flag suspicious patterns: If multiple red flags match a threat type, flag as MEDIUM or HIGH
- Be specific: Extract quotes and concrete evidence for each signal
- Trust patterns: Multiple small signals = MEDIUM confidence minimum
- Balance: A post describing suspicious job + credential request = MEDIUM threat minimum
- If threat_detected is false, explain why (insufficient evidence, legitimate context, etc.)"""

def classify_post(post_content, platform="reddit", author="unknown"):
    """Classify a single post using Claude."""

    user_message = f"""Analyze this post for AI-enabled recruitment scams:

Platform: {platform}
Author: {author}

Post content:
{post_content}

Provide threat classification in JSON format."""

    try:
        response = client.messages.create(
            model="claude-opus-4-1",
            max_tokens=1024,
            system=CLASSIFICATION_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Parse response
        response_text = response.content[0].text

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                classification = json.loads(json_str)
            else:
                classification = parse_natural_language_response(response_text)
        except json.JSONDecodeError:
            classification = parse_natural_language_response(response_text)

        return classification

    except Exception as e:
        print(f"Error classifying post: {e}")
        return {
            "threat_detected": False,
            "threat_category": None,
            "severity": "low",
            "confidence": "low",
            "reasoning": f"Classification error: {str(e)}",
            "signals": [],
            "recommendations": "Manual review required"
        }

def parse_natural_language_response(response_text):
    """Fallback parser for natural language responses."""
    return {
        "threat_detected": False,
        "threat_category": None,
        "severity": "low",
        "confidence": "low",
        "reasoning": "Unable to parse response. " + response_text[:200],
        "signals": [],
        "recommendations": "Manual review required"
    }

def batch_classify_posts(posts, verbose=False):
    """Classify multiple posts with progress tracking."""
    results = []

    for i, post in enumerate(posts):
        if verbose:
            print(f"[{i+1}/{len(posts)}] Classifying {post.get('id', 'unknown')[:20]}...")

        classification = classify_post(
            post_content=post.get('content', ''),
            platform=post.get('platform', 'unknown'),
            author=post.get('author', 'unknown')
        )

        classification['post_id'] = post.get('id')
        results.append(classification)

    return results

def get_threat_category_description(category):
    """Get description for threat category."""
    if category in THREAT_CATEGORIES:
        return THREAT_CATEGORIES[category]
    return None
