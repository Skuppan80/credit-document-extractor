"""
Data Processing Module
Handles parsing and structuring extracted data
"""

import json
import re
from typing import Dict, Any

class DataProcessor:
    """Process and structure extracted credit document data"""
    
    def __init__(self):
        pass
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Extract JSON from Claude's response
        
        Args:
            response: Claude API response text
            
        Returns:
            Parsed JSON as dictionary
        """
        # Try to find JSON in response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Invalid JSON in response"}
        else:
            return {"error": "No JSON found in response"}
    
    def save_to_json(self, data: Dict[str, Any], output_path: str):
        """
        Save data to JSON file
        
        Args:
            data: Dictionary to save
            output_path: Path to output file
        """
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

# For testing
if __name__ == "__main__":
    print("✅ Data Processor module loaded")