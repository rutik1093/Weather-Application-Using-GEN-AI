# app/decision_node.py

def decide_route(query: str) -> str:
    """
    Decide whether the query should go to:
    - Weather API
    - PDF/document retrieval

    Returns:
        "weather" or "pdf"
    """
    q = query.lower().strip()

    # Weather-related keywords
    weather_kw = [
        "weather", "temperature", "forecast", "rain", "sunny", "wind",
        "humidity", "climate", "storm", "snow", 
        "weather in", "temperature in"
    ]

    # PDF / document-related keywords
    doc_kw = [
        "pdf", "document", "file", "paper", "read",
        "from pdf", "in pdf", "according to pdf",
        "check pdf", "extract pdf", "open pdf"
    ]

    # 1️⃣ Weather intent check
    for kw in weather_kw:
        if kw in q:
            return "weather"

    # 2️⃣ PDF/document intent check
    for kw in doc_kw:
        if kw in q:
            return "pdf"

    # 3️⃣ Default → PDF RAG
    return "pdf"
