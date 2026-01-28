import re
import os
import logging
from guardrails.hub import ToxicLanguage

# Disable Guardrails telemetry
os.environ["GUARDRAILS_DISABLE_TELEMETRY"] = "true"

# Suppress OpenTelemetry noise
logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)
logging.getLogger(
    "opentelemetry.exporter.otlp.proto.http.trace_exporter"
).setLevel(logging.CRITICAL)

# Hub validator
toxic_validator = ToxicLanguage(
    threshold=0.50,
    validation_method="sentence",
    on_fail="exception"
)

JOKE_PATTERNS = [
    r"\btell\s+me\s+a\s+joke\b",
    r"\bjoke\b",
    r"\bfunny\b"
]

GREETING_PATTERNS = [
    r"^(hi|hello|hey|greetings)\b",
    r"\bhow\s+are\s+you\b",
    r"\bwhat'?s\s+up\b"
]

RESTRICTED_TOPICS = [
    r"\bmovies?\b",
    r"\bmusic\b",
    r"\bsports?\b",
    r"\bweather\b",
    r"\bgames?\b",
    r"\bentertainment\b"
]


def _match_any(patterns, text: str) -> bool:
    text = text.lower()
    return any(re.search(p, text) for p in patterns)


def validate_input(text: str):

    result = toxic_validator.validate(text, metadata={})
    if result.outcome == 'fail':
        return False, "Ask in a proper way, I can help you with simple works"
    
    if _match_any(GREETING_PATTERNS, text):
        return False, "Hello! How can I help you with your task?"

    if _match_any(JOKE_PATTERNS, text):
        return False, "I can only help with simple work! Not joke."

    if _match_any(RESTRICTED_TOPICS, text):
        return False, "I'm designed to help only with work-related or technical tasks."

    return True, None


def validate_output(text: str):
    result = toxic_validator.validate(text, metadata={})
    if result.outcome == 'fail':
        return "I'm unable to provide a response to that request."
    return text
    
