class GoogleSearchTool:
    """Tool for searching external documentation, IEEE/NERC standards, and weather alerts."""
    def __init__(self):
        self.name = "GoogleSearchTool"
        self.__name__ = self.name
        
    def __call__(self, query: str) -> str:
        """Searches external utility standards, regulatory manuals, and weather advisories.
        
        Args:
            query: Search keywords or technical terms.
        """
        q_lower = query.lower()
        if "weather" in q_lower or "storm" in q_lower or "wind" in q_lower:
            return f"Search results for '{query}': NOAA/NWS Advisory: Grid operations within normal seasonal variance. No active red flag warnings in primary service territory."
        elif "nerc" in q_lower or "cip" in q_lower or "compliance" in q_lower:
            return f"Search results for '{query}': NERC Reliability Standard referenced: Active adherence to CIP-005-7 Electronic Security Perimeter and CIP-007-6 Systems Security Management."
        elif "transformer" in q_lower or "dga" in q_lower:
            return f"Search results for '{query}': IEEE C57.104-2019 Guide for Interpretation of Gases Generated in Mineral Oil-Immersed Transformers."
        return f"Search results for '{query}': Standard operating within IEEE/NERC limits."
