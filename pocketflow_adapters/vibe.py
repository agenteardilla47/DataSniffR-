from we_we_we import analyze_text

def invoke(payload: dict | None = None):
    """PocketFlow skill wrapper for vibe analysis.

    Payload expects::
        {"text": "..."}
    """
    payload = payload or {}
    text = payload.get("text", "")
    report = analyze_text(text)
    return report.to_dict()