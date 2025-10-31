# 🔧 Setup Guide

Complete setup instructions for the Credit Document Extractor.

## Prerequisites

- Python 3.8 or higher
- Git
- Anthropic API key
- (Optional) Kaggle account

## Step-by-Step Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/credit-document-extractor.git
cd credit-document-extractor
```

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 3. Get Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up (get $5 free credits)
3. Navigate to API Keys
4. Create new key: "Credit Extractor"
5. Copy the key (starts with `sk-ant-api03-...`)

### 4. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env file
nano .env

# Add your API key:
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### 5. Test Installation
```bash
# Run test script
python test_api_key.py

# Expected output:
# ✅ API key works perfectly!
```

## Kaggle Setup

### 1. Create Kaggle Account

1. Go to https://www.kaggle.com
2. Sign up with Google/email
3. Verify phone number (required for secrets)

### 2. Upload Notebook

1. Go to Kaggle → Code → New Notebook
2. Upload `notebooks/credit_extractor_kaggle.ipynb`
3. Or copy-paste cells manually

### 3. Add API Key Secret

1. In notebook, right sidebar → Add-ons → Secrets
2. Add secret:
   - Label: `ANTHROPIC_API_KEY`
   - Key: `ANTHROPIC_API_KEY`
   - Value: [your API key]
3. Toggle ON: "Make available in this notebook"

### 4. Configure Notebook Settings

- Internet: ✅ ON (required)
- Accelerator: None (GPU not needed)
- Persistence: Files only

## Troubleshooting

### "No module named anthropic"
```bash
pip install anthropic pdfplumber
```

### "API key not found"

Check that `.env` file exists and contains:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### "Could not connect to API"

- Check internet connection
- Verify API key is valid
- Check you have remaining credits

## Next Steps

See [EXAMPLES.md](EXAMPLES.md) for usage examples.
