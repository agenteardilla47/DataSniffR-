from we_we_we import SecuritySigil

shield = SecuritySigil()

def invoke(payload: dict | None = None):
    """Evaluate text via SecuritySigil.

    Payload: {"text": "..."}
    """
    payload = payload or {}
    return shield.evaluate(payload.get("text", ""))