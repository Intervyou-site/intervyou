"""
Free AI Detection Heuristics
Detects common patterns in AI-generated text (ChatGPT, GPT-4, etc.)
No external API required - uses pattern matching and statistical analysis
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import language_tool_python

# Common AI phrases and patterns
AI_PHRASES = [
    # Formal transitions
    "it's important to note", "it's worth noting", "it should be noted",
    "it's worth mentioning", "it's essential to understand",
    
    # Conclusions
    "in conclusion", "to summarize", "in summary", "overall",
    "to sum up", "in essence",
    
    # Connectors
    "furthermore", "moreover", "additionally", "consequently",
    "therefore", "thus", "hence", "accordingly",
    
    # Qualifiers
    "it's crucial to", "it's vital to", "it's imperative to",
    "one must consider", "one should note",
    
    # Explanatory
    "this means that", "in other words", "that is to say",
    "to put it simply", "to clarify",
    
    # Hedging
    "it can be argued", "one might say", "it could be said",
    "some may argue", "it's possible that",
    
    # Academic style
    "research suggests", "studies show", "evidence indicates",
    "experts believe", "scholars argue"
]

# ChatGPT-specific patterns
CHATGPT_PATTERNS = [
    r"as an ai",
    r"i don't have personal",
    r"i cannot (provide|access|browse)",
    r"my knowledge cutoff",
    r"as of my last update",
    r"i'm (sorry|unable) to",
    r"i don't have the ability to",
    r"i can't (browse|access) the internet"
]

# Overly formal words
FORMAL_WORDS = [
    "utilize", "facilitate", "implement", "demonstrate", "establish",
    "comprehensive", "fundamental", "significant", "substantial",
    "numerous", "various", "particular", "specific", "essential",
    "crucial", "vital", "imperative", "paramount", "optimal"
]

# Perfect structure indicators
STRUCTURE_PATTERNS = [
    r"^(firstly|first|1\.)",  # Numbered/ordered lists
    r"(secondly|second|2\.)",
    r"(thirdly|third|3\.)",
    r"(finally|lastly|in conclusion)",
]


def detect_ai_generated(text: str) -> Dict:
    """
    Main AI detection function
    Returns comprehensive analysis of AI probability
    """
    if not text or len(text.strip()) < 20:
        return {
            "ai_probability": 0.0,
            "confidence": "low",
            "indicators": [],
            "warning": None,
            "details": {}
        }
    
    indicators = []
    scores = []
    details = {}
    
    # Check 1: AI phrases
    phrase_score, phrase_indicators = check_ai_phrases(text)
    if phrase_score > 0:
        scores.append(phrase_score)
        indicators.extend(phrase_indicators)
        details["ai_phrases"] = phrase_indicators
    
    # Check 2: ChatGPT-specific patterns
    chatgpt_score, chatgpt_indicators = check_chatgpt_patterns(text)
    if chatgpt_score > 0:
        scores.append(chatgpt_score)
        indicators.extend(chatgpt_indicators)
        details["chatgpt_patterns"] = chatgpt_indicators
    
    # Check 3: Formal language
    formal_score, formal_indicators = check_formal_language(text)
    if formal_score > 0:
        scores.append(formal_score)
        indicators.extend(formal_indicators)
        details["formal_language"] = formal_indicators
    
    # Check 4: Perfect structure
    structure_score, structure_indicators = check_structure(text)
    if structure_score > 0:
        scores.append(structure_score)
        indicators.extend(structure_indicators)
        details["structure"] = structure_indicators
    
    # Check 5: Grammar perfection
    grammar_score, grammar_indicators = check_grammar_perfection(text)
    if grammar_score > 0:
        scores.append(grammar_score)
        indicators.extend(grammar_indicators)
        details["grammar"] = grammar_indicators
    
    # Check 6: Sentence uniformity
    uniformity_score, uniformity_indicators = check_sentence_uniformity(text)
    if uniformity_score > 0:
        scores.append(uniformity_score)
        indicators.extend(uniformity_indicators)
        details["uniformity"] = uniformity_indicators
    
    # Check 7: Vocabulary sophistication
    vocab_score, vocab_indicators = check_vocabulary(text)
    if vocab_score > 0:
        scores.append(vocab_score)
        indicators.extend(vocab_indicators)
        details["vocabulary"] = vocab_indicators
    
    # Calculate final probability (weighted average)
    if scores:
        ai_probability = min(sum(scores) / len(scores), 1.0)
    else:
        ai_probability = 0.0
    
    # Determine confidence level
    confidence = get_confidence_level(len(indicators), ai_probability)
    
    # Generate warning
    warning = generate_warning(ai_probability, confidence)
    
    return {
        "ai_probability": round(ai_probability, 3),
        "confidence": confidence,
        "indicators": indicators,
        "warning": warning,
        "details": details,
        "verdict": get_verdict(ai_probability)
    }


def check_ai_phrases(text: str) -> Tuple[float, List[str]]:
    """Check for common AI phrases"""
    text_lower = text.lower()
    found_phrases = []
    
    for phrase in AI_PHRASES:
        if phrase in text_lower:
            found_phrases.append(f"Contains AI phrase: '{phrase}'")
    
    if not found_phrases:
        return 0.0, []
    
    # Score based on frequency (more aggressive)
    phrase_count = len(found_phrases)
    if phrase_count >= 5:
        score = 0.7  # Very strong indicator
    elif phrase_count >= 4:
        score = 0.6
    elif phrase_count >= 3:
        score = 0.5
    elif phrase_count >= 2:
        score = 0.4
    else:
        score = 0.2
    
    return score, found_phrases[:3]  # Return top 3


def check_chatgpt_patterns(text: str) -> Tuple[float, List[str]]:
    """Check for ChatGPT-specific patterns"""
    text_lower = text.lower()
    found_patterns = []
    
    for pattern in CHATGPT_PATTERNS:
        if re.search(pattern, text_lower):
            found_patterns.append(f"ChatGPT pattern detected: '{pattern}'")
    
    if not found_patterns:
        return 0.0, []
    
    # ChatGPT patterns are strong indicators
    score = min(0.8, len(found_patterns) * 0.4)
    
    return score, found_patterns


def check_formal_language(text: str) -> Tuple[float, List[str]]:
    """Check for overly formal language"""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0, []
    
    formal_count = sum(1 for word in words if word in FORMAL_WORDS)
    formal_ratio = formal_count / len(words)
    
    if formal_ratio < 0.05:
        return 0.0, []
    
    indicators = [f"High formal word usage: {formal_ratio:.1%} ({formal_count}/{len(words)} words)"]
    
    if formal_ratio >= 0.15:
        score = 0.5  # Strong indicator
    elif formal_ratio >= 0.10:
        score = 0.4
    elif formal_ratio >= 0.07:
        score = 0.3
    else:
        score = 0.2
    
    return score, indicators


def check_structure(text: str) -> Tuple[float, List[str]]:
    """Check for perfect structure (numbered lists, etc.)"""
    indicators = []
    matches = 0
    
    for pattern in STRUCTURE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            matches += 1
    
    if matches >= 3:
        indicators.append("Perfect numbered structure (1, 2, 3...)")
        score = 0.5  # Strong indicator of AI
    elif matches >= 2:
        indicators.append("Structured format detected")
        score = 0.3
    else:
        return 0.0, []
    
    return score, indicators


def check_grammar_perfection(text: str) -> Tuple[float, List[str]]:
    """Check if grammar is suspiciously perfect"""
    # Count basic grammar issues
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) < 2:
        return 0.0, []
    
    # Check for common human errors (lack of them is suspicious)
    human_errors = [
        r'\b(your|you\'re)\b.*\b(your|you\'re)\b',  # your/you're confusion
        r'\b(their|there|they\'re)\b',  # their/there/they're
        r'\bits\b',  # it's vs its
        r'\bthen\b.*\bthan\b',  # then/than
    ]
    
    # Perfect capitalization
    perfect_caps = all(s[0].isupper() for s in sentences if s)
    
    # No contractions (AI often avoids them)
    has_contractions = bool(re.search(r"n't|'ll|'ve|'re|'m|'d", text))
    
    indicators = []
    score = 0.0
    
    if perfect_caps and len(sentences) >= 3:
        indicators.append("Perfect capitalization (unusual for humans)")
        score += 0.2  # Increased weight
    
    if not has_contractions and len(text.split()) > 30:
        indicators.append("No contractions used (AI-like)")
        score += 0.3  # Increased weight
    
    return score, indicators


def check_sentence_uniformity(text: str) -> Tuple[float, List[str]]:
    """Check if sentences are suspiciously uniform in length"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) < 3:
        return 0.0, []
    
    lengths = [len(s.split()) for s in sentences]
    avg_length = sum(lengths) / len(lengths)
    
    # Calculate variance
    variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
    std_dev = variance ** 0.5
    
    # Low variance = uniform = AI-like
    if std_dev < 3 and len(sentences) >= 4:
        indicators = [f"Uniform sentence length (std dev: {std_dev:.1f})"]
        score = 0.2
    else:
        return 0.0, []
    
    return score, indicators


def check_vocabulary(text: str) -> Tuple[float, List[str]]:
    """Check vocabulary sophistication"""
    words = re.findall(r'\b\w+\b', text.lower())
    if len(words) < 20:
        return 0.0, []
    
    # Check for varied vocabulary (AI uses more diverse words)
    unique_ratio = len(set(words)) / len(words)
    
    # Check average word length (AI tends to use longer words)
    avg_word_length = sum(len(w) for w in words) / len(words)
    
    indicators = []
    score = 0.0
    
    if unique_ratio > 0.7 and len(words) > 30:
        indicators.append(f"High vocabulary diversity: {unique_ratio:.1%}")
        score += 0.15
    
    if avg_word_length > 5.5:
        indicators.append(f"Long average word length: {avg_word_length:.1f} chars")
        score += 0.1
    
    return score, indicators


def get_confidence_level(indicator_count: int, probability: float) -> str:
    """Determine confidence level"""
    if indicator_count >= 5 and probability >= 0.6:
        return "high"
    elif indicator_count >= 3 and probability >= 0.4:
        return "medium"
    elif indicator_count >= 1:
        return "low"
    else:
        return "very_low"


def generate_warning(probability: float, confidence: str) -> str:
    """Generate human-readable warning"""
    if probability >= 0.7:
        return "🚨 HIGH RISK: This answer shows strong signs of AI generation (ChatGPT, GPT-4, etc.)"
    elif probability >= 0.5:
        return "⚠️ MEDIUM RISK: This answer may be AI-generated. Multiple AI patterns detected."
    elif probability >= 0.3:
        return "⚠️ LOW RISK: Some AI-like patterns detected. Could be human with formal writing style."
    else:
        return None


def get_verdict(probability: float) -> str:
    """Get simple verdict"""
    if probability >= 0.7:
        return "Likely AI-generated"
    elif probability >= 0.5:
        return "Possibly AI-generated"
    elif probability >= 0.3:
        return "Uncertain (some AI patterns)"
    else:
        return "Likely human-written"


def get_detailed_report(result: Dict) -> str:
    """Generate detailed text report"""
    lines = []
    
    lines.append(f"AI Detection Analysis")
    lines.append(f"=" * 50)
    lines.append(f"AI Probability: {result['ai_probability']:.1%}")
    lines.append(f"Confidence: {result['confidence'].upper()}")
    lines.append(f"Verdict: {result['verdict']}")
    lines.append("")
    
    if result['warning']:
        lines.append(f"⚠️  {result['warning']}")
        lines.append("")
    
    if result['indicators']:
        lines.append("Detected Indicators:")
        for indicator in result['indicators']:
            lines.append(f"  • {indicator}")
        lines.append("")
    
    if result['details']:
        lines.append("Detailed Analysis:")
        for category, items in result['details'].items():
            if items:
                lines.append(f"  {category.replace('_', ' ').title()}:")
                for item in items[:2]:  # Show top 2 per category
                    lines.append(f"    - {item}")
    
    return "\n".join(lines)


# Test function
if __name__ == "__main__":
    # Test with AI-generated text
    ai_text = """
    Feature engineering is a crucial aspect of machine learning that involves 
    selecting, transforming, and creating new features from raw data. It's 
    important to note that this process significantly impacts model performance. 
    Furthermore, it requires domain knowledge to extract meaningful patterns. 
    In conclusion, effective feature engineering can substantially improve 
    prediction accuracy.
    """
    
    result = detect_ai_generated(ai_text)
    print(get_detailed_report(result))
    print("\n" + "=" * 50 + "\n")
    
    # Test with human text
    human_text = """
    I think feature engineering is when you make new features from your data. 
    Like if you have dates, you can extract the month or day. It helps the 
    model learn better patterns. I've used it in my projects and it really 
    improved my results.
    """
    
    result2 = detect_ai_generated(human_text)
    print(get_detailed_report(result2))
