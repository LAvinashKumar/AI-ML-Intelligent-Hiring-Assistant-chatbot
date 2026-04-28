"""
Utility functions for TalentScout: input validation, exit detection, candidate info extraction.
"""

import re

# Keywords that signal the user wants to end the conversation
EXIT_KEYWORDS = {"exit", "quit", "stop", "bye", "goodbye", "done", "end", "leave"}


def is_exit_intent(text: str) -> bool:
    """Return True if the user's message contains an exit keyword."""
    normalized = text.strip().lower()
    # Check exact match or if the message is just the keyword
    words = set(re.findall(r"\b\w+\b", normalized))
    return bool(words & EXIT_KEYWORDS)


def is_valid_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email.strip()))


def is_valid_phone(phone: str) -> bool:
    """Validate phone: digits only (with optional +, spaces, dashes), 7–15 digits total."""
    digits = re.sub(r"[\s\-\(\)\+]", "", phone)
    return digits.isdigit() and 7 <= len(digits) <= 15


def format_candidate_summary(info: dict) -> str:
    """Format collected candidate info into a readable summary string."""
    if not info:
        return "No information collected yet."
    lines = ["**Candidate Summary**", ""]
    field_labels = {
        "full_name": "Full Name",
        "email": "Email",
        "phone": "Phone",
        "experience": "Years of Experience",
        "desired_role": "Desired Role(s)",
        "location": "Current Location",
        "tech_stack": "Tech Stack",
    }
    for key, label in field_labels.items():
        value = info.get(key)
        if value:
            lines.append(f"- **{label}:** {value}")
    return "\n".join(lines)
