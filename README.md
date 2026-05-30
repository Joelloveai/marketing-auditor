# AI Marketing Auditor

A web app that audits any website’s SEO, copy, conversion, brand, and mobile performance in under 60 seconds using AI.

🔗 **Live Demo:** [joel-marketing-audit.streamlit.app]

## What It Does
- Enter any website URL
- 5 AI agents analyse the page (SEO, copy, conversion, brand, mobile)
- Get scores (0‑100) + actionable recommendations
- Download a full report

## Tech Stack
- Streamlit (frontend)
- Groq API (Llama 3.3)
- Python + requests

## Run Locally
```bash
git clone https://github.com/Joelloveai/ai-marketing-auditor.git
cd ai-marketing-auditor
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Add GROQ_API_KEY to .env file
streamlit run app.py
