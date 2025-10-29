"""
Claude API Integration Module
Handles communication with Anthropic's Claude API
"""

import anthropic
import os
from typing import Optional

class ClaudeAPI:
    """Wrapper for Anthropic Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude API client
        
        Args:
            api_key: Anthropic API key (or uses ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY or pass api_key parameter.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"
    
    def call_api(self, prompt: str, max_tokens: int = 4096) -> str:
        """
        Call Claude API with prompt
        
        Args:
            prompt: Text prompt to send
            max_tokens: Maximum tokens in response
            
        Returns:
            Claude's response as string
        """
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return message.content[0].text

# For testing
if __name__ == "__main__":
    print("✅ Claude API module loaded")