
import re
from constants import WEAK_WORDS, ROLE_KEYWORDS, MEASURABLE_REGEX, ACTION_VERBS

def calculate_ats_score(resume_data):
    """
    Calculates a heuristic ATS score based on various factors.
    Returns a score out of 100 and a list of feedback messages.
    """
    score = 100
    feedback = []

    # 1. Content Length Check (Simple word count estimation)
    # Assuming avg 500-1000 words for 1-2 pages
    total_text = " ".join([str(v) for v in resume_data.values() if isinstance(v, str)])
    # Add experience text
    for exp in resume_data.get('experience', []):
        total_text += " " + exp.get('responsibilities', '')
    
    # Add project text
    for proj in resume_data.get('projects', []):
        total_text += " " + proj.get('description', '')
    
    word_count = len(total_text.split())
    if word_count < 200:
        score -= 20
        feedback.append("Resume is too short. Add more detail to Experience and Projects.")
    elif word_count > 1200:
        score -= 10
        feedback.append("Resume might be too long (over 2 pages). condense bullet points.")

    # 2. Measurable Results Check
    measurable_count = 0
    for pattern in MEASURABLE_REGEX:
        if re.search(pattern, total_text, re.IGNORECASE):
            measurable_count += 1
    
    if measurable_count < 3:
        score -= 15
        feedback.append(f"Found only {measurable_count} measurable result(s). Aim for at least 3-5 (e.g., 'Increased sales by 20%', 'Saved $10k').")

    # 3. Action Verb Check
    verb_count = 0
    total_text_lower = total_text.lower()
    for verb in ACTION_VERBS:
        if f" {verb.lower()} " in f" {total_text_lower} ": # weak match
            verb_count += 1
    
    if verb_count < 5:
        score -= 10
        feedback.append(f"Low usage of action verbs (Found {verb_count}). Use words like 'Orchestrated', 'Developed', 'Spearheaded'.")

    # 4. Contact Info Check
    if not resume_data.get('email') or not resume_data.get('phone'):
        score -= 20
        feedback.append("Missing critical contact information (Email or Phone).")
    
    if not resume_data.get('linkedin'):
        score -= 5
        feedback.append("LinkedIn profile is recommended for better visibility.")

    # 5. Weak Words Check
    weak_word_hits = []
    for weak, strong in WEAK_WORDS.items():
        if weak in total_text_lower:
            weak_word_hits.append(f"'{weak}' -> '{strong}'")
            score -= 2
    
    if weak_word_hits:
        feedback.append(f"Found weak words: {', '.join(weak_word_hits[:3])}...")

    return max(0, score), feedback

def get_role_keywords(target_role):
    """
    Returns a list of keywords for a given target role.
    """
    if not target_role:
        return []
    
    target_role_lower = target_role.lower()
    for role, keywords in ROLE_KEYWORDS.items():
        if role in target_role_lower:
            return keywords
            
    # Fallback: simple split if no match found (naive)
    return []

def refine_text_with_ats_rules(text):
    """
    Simple function to clean text:
    - remove emojis (basic range)
    - standardise quotes
    """
    if not text:
        return ""
        
    # Remove basic emojis (ranges can be extensive, using a simple broad range for now)
    # This is a basic regex for some emojis, might not catch everything but good enough for a constraint
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    
    # Capitalize first letter if it's a sentence/bullet
    text = text.strip()
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
        
    return text

def validate_email(email):
    # Basic email regex
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
