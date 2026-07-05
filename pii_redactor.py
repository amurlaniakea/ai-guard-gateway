import re

class PIIRedactor:
    """
    Identifica y enmascara datos personales sensibles (PII) en el texto.
    """
    def __init__(self):
        # Definición de patrones comunes de PII
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "PHONE": r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "IPV4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b", # US Social Security Number
        }

    def redact(self, text: str) -> tuple[str, int]:
        """
        Busca y reemplaza PII en el texto.
        Retorna el texto redactado y la cantidad de hallazgos.
        """
        if not text:
            return "", 0
            
        redacted_text = text
        total_findings = 0
        
        for label, pattern in self.patterns.items():
            matches = re.findall(pattern, redacted_text)
            total_findings += len(matches)
            redacted_text = re.sub(pattern, f"[{label}_REDACTED]", redacted_text)
            
        return redacted_text, total_findings
