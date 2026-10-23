import json
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, THREAT_CATEGORIES

client = Anthropic(api_key=ANTHROPIC_API_KEY, timeout=30.0)

CLASSIFICATION_SYSTEM_PROMPT = """You are an expert threat analyst specializing in AI-enabled fraud and recruitment scams.

Your task is to analyze online posts for signs of AI-powered recruitment scams and provide structured threat intelligence.

THREAT FRAMEWORK:
You classify threats into these categories based on the FIST + MITRE framework:

1. **Fake Recruiter Impersonation** (MITRE T1684.001)
   - AI-generated or stolen recruiter personas
   - Signals: Recent LinkedIn profile, stolen photos, generic communication, AI video/voice

2. **Credential Harvesting** (MITRE T1598.002)
   - Requests for sensitive data under verification pretense
   - Signals: Password/banking requests before employment, suspicious verification forms

3. **Synthetic Endorsement** (MITRE T1589.002)
   - Deepfakes, voice clones, LLM-generated testimonials
   - Signals: AI tells in video, unverifiable employee testimonials, lip sync issues

4. **Coordinated Inauthentic Behavior** (MITRE T1659)
   - Multiple accounts discussing same fake opportunity
   - Signals: Coordinated posting patterns, unusual account clusters

SCORING SYSTEM:

Severity:
- HIGH: Direct financial loss, credential theft, identity theft
- MEDIUM: Potential harm confirmed, deceptive practice confirmed
- LOW: Suspicious indicators, warrants investigation

Confidence:
- HIGH: Multiple independent signals OR technical detection confirms
- MEDIUM: 1-2 strong signals OR pattern matches known scams
- LOW: Single signal OR could have innocent explanation

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

Guidelines:
- Be conservative: flag uncertainty as LOW confidence
- Extract specific quotes/evidence in signals
- Explain what evidence supports each confidence level
- If threat_detected is false, signals may be empty"""

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
