# 📖 Usage Examples

## Example 1: Extract from Local PDF
```python
from scripts.pdf_extractor import PDFExtractor
from scripts.claude_api import ClaudeAPI
import json

# Extract text
extractor = PDFExtractor()
extraction = extractor.extract_all("data/input/credit_agreement.pdf")

# Analyze with Claude
api = ClaudeAPI()
terms = api.extract_credit_terms(extraction['text'])

# Display results
print(json.dumps(terms, indent=2))
```

## Example 2: Batch Processing
```python
import os
from scripts.pdf_extractor import PDFExtractor
from scripts.claude_api import ClaudeAPI

extractor = PDFExtractor()
api = ClaudeAPI()

# Process all PDFs in input folder
input_dir = "data/input"
output_dir = "data/output"

for filename in os.listdir(input_dir):
    if filename.endswith('.pdf'):
        print(f"Processing: {filename}")
        
        # Extract
        pdf_path = os.path.join(input_dir, filename)
        extraction = extractor.extract_all(pdf_path)
        
        # Analyze
        terms = api.extract_credit_terms(extraction['text'])
        
        # Save
        output_path = os.path.join(output_dir, filename.replace('.pdf', '.json'))
        with open(output_path, 'w') as f:
            json.dump(terms, f, indent=2)
        
        print(f"✅ Saved: {output_path}\n")
```

## Example 3: Kaggle Notebook

See `notebooks/credit_extractor_kaggle.ipynb` for complete Kaggle example.

Key cells:
```python
# Cell 1: Install packages
!pip install -q anthropic pdfplumber

# Cell 2: Download PDF
import urllib.request
url = "https://home.treasury.gov/system/files/136/Chrysler_docs.pdf"
urllib.request.urlretrieve(url, "/kaggle/working/doc.pdf")

# Cell 3: Extract and analyze
# [See notebook for full code]
```

## Example 4: Cost Tracking
```python
class CostTracker:
    def __init__(self):
        self.total_cost = 0
        self.documents_processed = 0
    
    def track_extraction(self, input_tokens, output_tokens):
        cost = (input_tokens * 3 + output_tokens * 15) / 1_000_000
        self.total_cost += cost
        self.documents_processed += 1
        return cost
    
    def report(self):
        avg = self.total_cost / self.documents_processed if self.documents_processed > 0 else 0
        print(f"Documents: {self.documents_processed}")
        print(f"Total cost: ${self.total_cost:.4f}")
        print(f"Average: ${avg:.4f}/doc")

tracker = CostTracker()
# Use after each extraction
```

## Example Results

### Chrysler Credit Agreement (2009)

**Input:**
- 30 pages processed
- ~25K tokens

**Output:**
```json
{
  "borrower": "Chrysler LLC",
  "lender": "U.S. Department of Treasury",
  "loan_details": {
    "total_amount": "$4.0 billion",
    "facility_type": "Term Loan"
  },
  "interest_terms": {
    "base_rate": "LIBOR or 2%",
    "margin": "3.5%"
  }
}
```

**Cost:** $0.087

## Tips

1. **Process first 30-40 pages** for most credit agreements (main terms usually there)
2. **Use temperature=0** for extraction (deterministic results)
3. **Batch process at night** to save time
4. **Cache extracted text** to avoid re-processing PDFs

## More Examples

See the [notebooks/](../notebooks/) folder for more examples.
