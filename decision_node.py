def decide_route(query: str) -> str:
    q = query.lower()

    
    if "whether" in q:
        q = q.replace("whether", "weather")

    weather_kw = [
        "weather", "temperature", "forecast", "rain",
        "sunny", "wind", "climate", "humidity",
        "weather in", "temp in", "temperature in"
    ]

    doc_kw = ["pdf", "document", "file", "paper", "read"]

    if any(k in q for k in weather_kw):
        return "weather"

    if any(k in q for k in doc_kw):
        return "pdf"

    return "weather"   

