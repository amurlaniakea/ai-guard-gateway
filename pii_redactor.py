
import re

class PIIRedactor:
    def __init__(self):
        self.patterns = {
            "email": r"[\w\.-]+@[\w\.-]+\.\w+",
            "card": r"\b(?:\d[ -]*?){13,16}\b"
        }

    def redact(self, text):
        redacted_text = text
        for label, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, f"[{label.upper()}_REDACTED]", redacted_text)
        return redacted_text
