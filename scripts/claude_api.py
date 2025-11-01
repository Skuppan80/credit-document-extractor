import anthropic
import json
import re
import os

class ClaudeAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key required")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"
    
    def extract_credit_terms(self, document_text, max_chars=100000):
        if len(document_text) > max_chars:
            document_text = document_text[:max_chars]
        
        prompt = f"""Extract credit terms from this document as JSON:

{document_text}

Return JSON with: borrower, lender, loan_details, interest_terms, maturity."""
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            return json.loads(json_match.group())
        return {"error": "No JSON found"}
