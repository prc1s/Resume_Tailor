"""
Utilities for formatting user input.
"""
import re

class Formatter:
    """Cleans and standardizes user-provided data."""
    
    def format_location(self, location: str) -> str:
        """
        Standardizes the location string.
        - Fixes capitalization.
        - Corrects common abbreviations (e.g., KSA).
        - Ensures consistent formatting.
        """
        if not location:
            return ""
            
        # Title case all words
        location = location.strip().title()
        
        # Specific corrections using regex for robustness
        # Correct "Riyad" to "Riyadh"
        location = re.sub(r'\bRiyad\b', 'Riyadh', location)
        
        # Correct "Ksa" or "Saudi Arabi" to "Saudi Arabia"
        location = re.sub(r'\bKsa\b', 'Saudi Arabia', location, flags=re.IGNORECASE)
        location = re.sub(r'Saudi Arabi\b', 'Saudi Arabia', location, flags=re.IGNORECASE)
        
        # Standardize comma separation
        parts = [part.strip() for part in location.split(',')]
        if len(parts) > 1 and "Saudi Arabia" in parts[1]:
             parts[1] = "Saudi Arabia"
        
        return ", ".join(filter(None, parts))

# Global formatter instance
formatter = Formatter() 