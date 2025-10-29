# Data Directory

This folder contains input PDFs and output JSON files.

## Structure

- **input/**: Place your credit document PDFs here for local testing
- **output/**: Extracted JSON results will be saved here

## Important

PDF and JSON files are in `.gitignore` and won't be committed to GitHub.
This keeps your data private and the repository clean.

## Example Usage
```bash
# Place PDF in input
cp ~/Downloads/credit_agreement.pdf data/input/

# Run extraction
python scripts/main.py data/input/credit_agreement.pdf

# Check output
cat data/output/credit_agreement_extracted.json
```
