# 🏦 Credit Document Extractor
AI-powered credit arrangement document analyzer using Claude API and Kaggle.

## 🎯 Overview
This project extracts structured financial data from credit arrangement PDFs using:
- **LLM**: Claude Sonnet 4.5 (Anthropic)
- **Compute**: Kaggle (free notebooks)
- **Processing**: Direct extraction (no RAG needed)

## 📊 What It Extracts

- Borrower & Lender information
- Principal amounts & interest rates
- Loan terms & maturity dates
- Financial covenants
- Collateral details
- Fees & prepayment terms
- Events of default

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API key
- Kaggle account

### Setup

1. Clone repository:
```bash
git clone https://github.com/YOUR_USERNAME/credit-document-extractor.git
cd credit-document-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Usage

See `notebooks/` for Kaggle notebooks with examples.

## 📁 Project Structure
```
credit-document-extractor/
├── notebooks/          # Kaggle notebooks
├── scripts/            # Python modules
│   ├── pdf_extractor.py
│   ├── claude_api.py
│   └── data_processor.py
├── data/
│   ├── input/         # Input PDFs
│   └── output/        # Extracted JSON
└── docs/              # Documentation
```

## 💰 Cost

- **Per document**: ~$0.09
- **Free tier**: $5 credit = ~55 documents

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📝 License

MIT License - see LICENSE file for details.

## 🔗 Links

- [Anthropic API Docs](https://docs.anthropic.com)
- [Kaggle](https://www.kaggle.com)
- [Project Documentation](./docs/)

---

**Status**: 🚧 In Development

**Last Updated**: [Today's Date]