
import re

class PIIRedactor:
    def __init__(self):
        self.patterns = {
            "email": r"[\w\.-]+@[\w\.-]+\.\w+",
            "card": r"\b(?:\d[ -]*?){13,16}\b",
            "phone": r"\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b",
            "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
        }

    def redact(self, text):
        redacted_text = text
        for label, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, f"[{label.upper()}_REDACTED]", redacted_text)
        return redacted_text
