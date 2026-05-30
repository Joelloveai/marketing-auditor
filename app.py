import streamlit as st
import requests
import json
from groq import Groq
import os

# ------------------------------------------------------------
# SAFE API KEY HANDLING (works locally AND on Streamlit Cloud)
# ------------------------------------------------------------
try:
    # On Streamlit Cloud, the secret is stored in st.secrets
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    # Local development: load API key from .env file
    from dotenv import load_dotenv

    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        st.error(
            "GROQ_API_KEY not found. Create a .env file or add the secret in Streamlit Cloud."
        )
        st.stop()


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text[:8000]  # first 8000 characters only
    except Exception:
        return ""


def call_groq(prompt):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        st.error(f"Groq API error: {e}")
        return None


def audit_seo(html):
    return call_groq(
        f"SEO expert. Return JSON: seo_score (0-100), missing_tags (array), recommendation.\n{html[:3000]}"
    )


def audit_copy(html):
    return call_groq(
        f"Copy expert. Return JSON: copy_score (0-100), headline_quality, tone_suggestion, recommendation.\n{html[:3000]}"
    )


def audit_conversion(html):
    return call_groq(
        f"Conversion expert. Return JSON: conversion_score (0-100), cta_visibility, friction_points (array), recommendation.\n{html[:3000]}"
    )


def audit_brand(html):
    return call_groq(
        f"Brand strategist. Return JSON: brand_score (0-100), trust_signals (array), recommendation.\n{html[:3000]}"
    )


def audit_mobile(html):
    return call_groq(
        f"Mobile expert. Return JSON: mobile_score (0-100), issues (array), recommendation.\n{html[:3000]}"
    )


# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="AI Marketing Auditor", layout="wide")
st.title("📊 AI Marketing Audit")
st.markdown(
    "Enter any website URL to get a professional marketing audit (SEO, copy, conversion, brand, mobile)."
)
url = st.text_input("🌐 Website URL", placeholder="https://example.com")

if st.button("Run Audit", type="primary"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("🔍 Auditing website... this may take 30 seconds."):
            html = fetch_html(url)
            if html:
                seo = audit_seo(html)
                copy = audit_copy(html)
                conversion = audit_conversion(html)
                brand = audit_brand(html)
                mobile = audit_mobile(html)

                scores = []
                if seo and "seo_score" in seo:
                    scores.append(seo["seo_score"])
                if copy and "copy_score" in copy:
                    scores.append(copy["copy_score"])
                if conversion and "conversion_score" in conversion:
                    scores.append(conversion["conversion_score"])
                if brand and "brand_score" in brand:
                    scores.append(brand["brand_score"])
                if mobile and "mobile_score" in mobile:
                    scores.append(mobile["mobile_score"])
                overall = sum(scores) / len(scores) if scores else 0

                st.success(
                    f"Audit complete! Overall Marketing Health: **{overall:.0f}/100**"
                )
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    if seo:
                        st.metric("SEO Score", f"{seo['seo_score']}/100")
                        st.caption(f"📌 {seo['recommendation']}")
                    if copy:
                        st.metric("Copy Score", f"{copy['copy_score']}/100")
                        st.caption(f"📌 {copy['recommendation']}")
                    if conversion:
                        st.metric(
                            "Conversion Score", f"{conversion['conversion_score']}/100"
                        )
                        st.caption(f"📌 {conversion['recommendation']}")
                with col2:
                    if brand:
                        st.metric("Brand Score", f"{brand['brand_score']}/100")
                        st.caption(f"📌 {brand['recommendation']}")
                    if mobile:
                        st.metric("Mobile Score", f"{mobile['mobile_score']}/100")
                        st.caption(f"📌 {mobile['recommendation']}")

                # Save report as text file and offer download
                with open("MARKETING_AUDIT_REPORT.txt", "w") as f:
                    f.write(f"Website: {url}\n")
                    f.write(f"Overall Score: {overall:.0f}/100\n\n")
                    for name, data in [
                        ("SEO", seo),
                        ("Copy", copy),
                        ("Conversion", conversion),
                        ("Brand", brand),
                        ("Mobile", mobile),
                    ]:
                        if data:
                            f.write(
                                f"{name} Score: {data.get(f'{name.lower()}_score', 'N/A')}\n"
                            )
                            f.write(
                                f"Recommendation: {data.get('recommendation', 'N/A')}\n\n"
                            )
                st.download_button(
                    "📥 Download Full Report",
                    data=open("MARKETING_AUDIT_REPORT.txt").read(),
                    file_name="marketing_audit_report.txt",
                )
