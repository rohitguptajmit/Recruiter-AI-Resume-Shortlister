import re
from typing import Optional, List, Dict

import fitz  # PyMuPDF for PDF parsing
import pandas as pd
import streamlit as st
from openai import OpenAI


# -------------------- PAGE CONFIG -------------------- #

st.set_page_config(
    page_title="👔 Recruiter – AI Resume Shortlister",
    page_icon="👔",
    layout="wide",
)

# -------------------- GLOBAL CUSTOM STYLE -------------------- #

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #f7fbff, #eef2f7);
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: #4a5568;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 18px;
        padding: 1.3rem 1.4rem;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }

    .pill {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: #edf2ff;
        color: #3730a3;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    .stButton>button {
        border-radius: 999px;
        padding: 0.6rem 1.7rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.45);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4338ca, #6d28d9);
    }

    .stFileUploader>div>div {
        border-radius: 14px !important;
        border: 1px dashed #cbd5e1 !important;
        background-color: rgba(255, 255, 255, 0.96);
    }

    .stCheckbox>label {
        font-size: 0.9rem;
        font-weight: 500;
    }

    .dataframe tbody tr th {
        font-size: 0.85rem;
    }
    .dataframe td, .dataframe th {
        font-size: 0.85rem;
        padding: 0.35rem 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HERO SECTION -------------------- #

left_hero, right_hero = st.columns([2.8, 1.2])

with left_hero:
    st.markdown(
        """
        <div class="glass-card">
            <div class="hero-title">👔 Recruiter – AI Resume Shortlister</div>
            <p class="hero-subtitle">
                Upload multiple <b>candidate resumes</b> and a single <b>job description</b>.  
                Let an OpenAI-powered recruiter score, rank, and summarize each profile for quick shortlisting.
            </p>
            <div style="margin-top:0.6rem;">
                <span class="pill">AI screening</span>
                <span class="pill">Fit score & verdict</span>
                <span class="pill">Shortlist view</span>
                <span class="pill">Interview focus areas</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_hero:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:0.8rem; font-weight:600; text-transform:uppercase; color:#6b7280; letter-spacing:0.08em;">
                Quick glance
            </div>
            <div style="font-size:2.1rem; font-weight:800; margin-top:0.4rem;">
                ⚡
            </div>
            <div style="font-size:0.88rem; color:#4b5563; margin-top:0.4rem;">
                Drop in resumes<br/>Get a ranked shortlist<br/>In one click.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")


# -------------------- FILE UTILITIES -------------------- #

def extract_pdf_text(uploaded_file) -> str:
    """Extract plain text from a PDF UploadedFile."""
    file_bytes = uploaded_file.read()
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def get_text_from_file(uploaded_file) -> str:
    """Handle PDF and TXT uploads."""
    if uploaded_file.type == "application/pdf":
        return extract_pdf_text(uploaded_file)
    return uploaded_file.read().decode("utf-8", errors="ignore")


# -------------------- PROMPT + OPENAI CALL -------------------- #

def build_prompt(resume_text: str, job_text: str) -> str:
    return f"""
You are an experienced **recruiter and hiring manager**.

Your task is to evaluate a **candidate's resume** against a **specific job description** and provide a concise, structured report from a recruiter’s point of view.

Use **professional hiring language** and respond in **Markdown** using the exact sections below:

1. **Overall Verdict**  
   - Start with a single line in the format:  
     `Verdict: Strong Yes` or `Verdict: Yes` or `Verdict: Maybe` or `Verdict: No`  
   - Treat this as your recommendation for **shortlisting** for interview.

2. **Fit Score**  
   - A single line starting with: `Fit Score: NN%` (0–100 based on overall match to the role).

3. **Key Hiring Strengths**  

4. **Hiring Risks / Concerns**  

5. **Interview Focus Areas**  

6. **Suggested Role Level / Fit Notes (Optional)**  

7. **Optional Note to Candidate**  

Base all judgments **strictly** on the resume vs the job description. Avoid inventing facts.

Candidate Resume:
\"\"\"{resume_text}\"\"\"

Job Description:
\"\"\"{job_text}\"\"\"
    """.strip()


def call_openai(model_name: str, prompt: str, api_key: Optional[str] = None) -> str:
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = OpenAI()

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise, structured AI recruiter and hiring manager "
                    "who evaluates candidates against specific roles."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


# -------------------- PARSING HELPERS -------------------- #

def extract_fit_score(markdown_output: str) -> Optional[int]:
    match = re.search(r"Fit Score:\s*(\d{1,3})\s*%", markdown_output, re.IGNORECASE)
    if not match:
        match = re.search(r"(\d{1,3})\s*%", markdown_output)
        if not match:
            return None
    value = int(match.group(1))
    if 0 <= value <= 100:
        return value
    return None


def extract_verdict(markdown_output: str) -> str:
    match = re.search(r"Verdict:\s*(.+)", markdown_output, re.IGNORECASE)
    if match:
        verdict = match.group(1).strip()
        verdict = verdict.split("\n")[0].strip()
        return verdict
    return "N/A"


def is_shortlist_verdict(verdict: str) -> bool:
    v = verdict.lower()
    return v.startswith("strong yes") or v.startswith("yes")


def display_verdict_badge(verdict: str) -> str:
    v = verdict.lower()
    if v.startswith("strong yes"):
        return f"🟢 {verdict}"
    if v.startswith("yes"):
        return f"✅ {verdict}"
    if v.startswith("maybe"):
        return f"🟡 {verdict}"
    if v.startswith("no"):
        return f"🔴 {verdict}"
    return verdict


# -------------------- SIDEBAR CONFIG -------------------- #

with st.sidebar:
    st.header("⚙️ Settings")

    st.markdown(
        "This app uses the **OpenAI API** as a recruiter assistant.\n\n"
        "1. Create an API key from your OpenAI account.\n"
        "2. Either paste it below or set the `OPENAI_API_KEY` environment variable."
    )

    api_key_input = st.text_input(
        "OpenAI API Key (optional)",
        type="password",
        help="Leave blank if you already set OPENAI_API_KEY in your environment.",
    )

    model_name = st.selectbox(
        "Model",
        options=["gpt-4.1-mini", "gpt-4.1", "o4-mini"],
        index=0,
        help="Smaller models are faster/cheaper; larger ones can be more accurate.",
    )

    st.markdown("---")
    st.caption("Upload multiple candidate resumes and one JD on the main page.")


# -------------------- MAIN INPUT AREA -------------------- #

st.markdown("")

col1, col2 = st.columns(2)

with col1:
    resumes_files: List = st.file_uploader(
        "📁 Upload Candidate Resumes (PDF or TXT) – multiple allowed",
        type=["pdf", "txt"],
        help="Upload multiple CVs/resumes to evaluate them for the same role.",
        accept_multiple_files=True,
    )

with col2:
    job_file = st.file_uploader(
        "📁 Upload Job Description (PDF or TXT)",
        type=["pdf", "txt"],
        help="Role description / JD in PDF or TXT.",
    )

status_cols = st.columns(3)
with status_cols[0]:
    st.metric("Resumes uploaded", len(resumes_files) if resumes_files else 0)
with status_cols[1]:
    st.metric("JD uploaded", 1 if job_file else 0)
with status_cols[2]:
    st.markdown(
        """
        <div style="
            display:inline-block;
            padding:6px 16px;
            background:linear-gradient(135deg,#6366f1,#7c3aed);
            color:white;
            border-radius:999px;
            font-size:0.9rem;
            font-weight:600;
            margin-top:14px;
        ">
            🎯 AI-Powered Shortlisting
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("---")

show_shortlist_only = st.checkbox(
    "Show only **Strong Yes** and **Yes** candidates",
    value=False,
    help="When enabled, only shortlisted candidates are shown in the table and reports.",
)

analyze_button = st.button("🔍 Evaluate All Candidates for This Role")


# -------------------- RESULT RENDERING -------------------- #

def render_results(results_sorted: List[Dict], shortlist_only: bool, *, updated: bool):
    if shortlist_only:
        display_results = [r for r in results_sorted if is_shortlist_verdict(r["verdict"])]
    else:
        display_results = results_sorted

    if updated:
        st.success("✅ Evaluation complete! Scroll down for the shortlist and detailed reports.")

    st.subheader("📊 Shortlist Summary")

    if not display_results:
        st.info("No candidates match the current filter.")
        return

    summary_rows = []
    for r in display_results:
        summary_rows.append(
            {
                "Candidate": r["candidate_name"],
                "Verdict": display_verdict_badge(r["verdict"]),
                "Fit Score (%)": r["fit_score"] if r["fit_score"] is not None else "N/A",
            }
        )

    df = pd.DataFrame(summary_rows)
    df.index = df.index + 1
    df.index.name = "Rank"
    st.table(df)

    st.subheader("📌 Detailed Recruiter Reports")

    for r in display_results:
        with st.expander(f"📄 {r['candidate_name']} – {r['verdict']}"):
            st.markdown(r["report"])
            st.download_button(
                "💾 Download this candidate's report (Markdown)",
                r["report"],
                file_name=f"{r['candidate_name']}_recruiter_report.md",
                mime="text/markdown",
                key=f"download_{r['candidate_name']}",
            )


# -------------------- EVALUATION LOGIC -------------------- #

if analyze_button:
    if not job_file:
        st.warning("⚠️ Please upload a **job description**.")
    elif not resumes_files:
        st.warning("⚠️ Please upload at least **one candidate resume**.")
    else:
        try:
            with st.spinner("⏳ Reading files and evaluating all candidates like a recruiter..."):
                job_text = get_text_from_file(job_file)

                results: List[Dict] = []
                for upload in resumes_files:
                    candidate_name = upload.name
                    resume_text = get_text_from_file(upload)
                    prompt = build_prompt(resume_text, job_text)
                    output = call_openai(
                        model_name=model_name,
                        prompt=prompt,
                        api_key=api_key_input.strip() or None,
                    )
                    score = extract_fit_score(output)
                    verdict = extract_verdict(output)

                    results.append(
                        {
                            "candidate_name": candidate_name,
                            "fit_score": score if score is not None else None,
                            "verdict": verdict,
                            "report": output,
                        }
                    )

            results_sorted = sorted(
                results,
                key=lambda r: (r["fit_score"] is None, -(r["fit_score"] or 0)),
            )

            st.session_state["recruiter_results"] = results_sorted
            render_results(results_sorted, show_shortlist_only, updated=True)

        except Exception as e:
            st.error(
                "❌ Something went wrong while evaluating the candidates.\n\n"
                f"**Details:** {e}"
            )

# If user hasn’t clicked again but results exist, show them (no “previous run” wording)
elif "recruiter_results" in st.session_state:
    results_sorted = st.session_state["recruiter_results"]
    render_results(results_sorted, show_shortlist_only, updated=False)
