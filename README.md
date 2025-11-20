# 👔 Recruiter – AI Resume Shortlister

An AI-powered Streamlit app that helps **recruiters and hiring managers** quickly screen multiple candidates against a single job description.

Instead of reading every resume line by line, you upload:

- 📂 Several **candidate resumes** (PDF or TXT)  
- 📄 One **job description** (PDF or TXT)

…and the app returns a **ranked shortlist** with:

- A **verdict** for each candidate (Strong Yes / Yes / Maybe / No)  
- A **fit score** (0–100%)  
- A recruiter-style **evaluation report** you can download in Markdown  

---

## 🧠 The Story – From a Recruiter’s Point of View

You’re hiring for a critical role.

- 1 JD  
- 20+ resumes in your inbox  
- A busy day full of meetings  

You don’t want AI to “replace” you, but you *do* want help answering:

> “Which 3–5 candidates should I look at first, and what should I focus on in their interviews?”

This app acts like a **digital hiring assistant**:

1. You drop in all the resumes and the JD.
2. The app calls an **OpenAI model** that “thinks” like a recruiter.
3. For each candidate, it generates a compact evaluation:
   - ✅ Overall verdict: Strong Yes / Yes / Maybe / No  
   - 🎯 Fit score: 0–100%  
   - 💪 Key hiring strengths  
   - ⚠️ Risks / concerns  
   - ❓ Interview focus areas  
   - 🔎 Optional note you could share with the candidate  

You still make the final decision—but now you start with a **prioritized shortlist** and a clear view of where to probe in the next round.

---

## ✨ Key Features

- **Multi-candidate upload**  
  Upload multiple resumes at once for the *same* role (PDF/TXT).

- **Single JD, many profiles**  
  All candidates are evaluated against one job description, ensuring consistent criteria.

- **Recruiter-style verdicts**  
  For every candidate, the model returns:
  - `Verdict: Strong Yes / Yes / Maybe / No`  
  - `Fit Score: NN%`  

- **Shortlist filter**  
  One checkbox lets you show **only Strong Yes and Yes** candidates when you want to see the shortlist.

- **Ranked summary table**  
  A neat table with:
  - Rank (starting from 1)  
  - Candidate file name  
  - Verdict (with emoji badge)  
  - Fit score (%)  

- **Detailed reports + downloads**  
  Each candidate gets a full Markdown report inside an expander, plus a **“Download report”** button.

- **Polished UI**  
  Custom CSS for a modern “glass card” look, gradient buttons, and an **“🎯 AI-Powered Shortlisting”** badge to emphasize recruiter mode.

---

## 🏗️ Tech Stack

- **Python 3.9+**  
- **Streamlit** – web UI framework  
- **OpenAI Python SDK** – calls GPT models for evaluation logic  
- **PyMuPDF (`fitz`)** – extract text from PDFs  
- **Pandas** – build the ranking table  

---

## 📂 Project Structure

    recruiter-resume-shortlister/
        ├─ app.py            # Main Streamlit app (UI + logic)
        └─ requirements.txt  # Python dependencies

---

## ✅ Prerequisites

1. **OpenAI account + API key**
   - Create an API key from your OpenAI dashboard.
   - Keep it handy; you’ll paste it into the app or set it as an environment variable.

2. **Python 3.9 or later**
   - On Windows: install from the official Python website (check “Add Python to PATH”).
   - On macOS/Linux: use system Python or install via package manager if needed.

3. **Basic tooling**
   - Terminal / Command Prompt (for running commands)
   - Optional: a code editor like VS Code

---

## 🔧 Installation & Setup

### 1. Download / clone the project

Create a folder (for example):

    mkdir recruiter-resume-shortlister
    cd recruiter-resume-shortlister

Save `app.py` and `requirements.txt` into this folder.

---

### 2. Create and activate a virtual environment (recommended)

**Windows (PowerShell or CMD):**

    python -m venv .venv
    .\.venv\Scripts\activate

**macOS / Linux:**

    python3 -m venv .venv
    source .venv/bin/activate

You should see `(.venv)` at the start of your terminal prompt once it’s active.

---

### 3. Install dependencies

With the virtual environment activated:

    pip install -r requirements.txt

This installs:

- `streamlit`  
- `pymupdf`  
- `openai`  

---

### 4. Provide your OpenAI API key

You can do this in **either** of two ways.

#### Option A – Environment variable (recommended)

**Windows (PowerShell):**

    setx OPENAI_API_KEY "sk-xxxxxxxxxxxxxxxx"

Then close and reopen the terminal, re-activate the venv, and run the app.

**macOS / Linux (current terminal session):**

    export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"

#### Option B – Paste inside the app

- If you don’t set the environment variable, that’s fine.  
- When the app loads, paste your key into the sidebar field:
  - “OpenAI API Key (optional)”

---

## 🚀 Running the App

From inside the project folder, with the virtual environment activated:

    streamlit run app.py

Streamlit will start a local web server and show something like:

    Local URL: http://localhost:8501

Open that URL in your browser if it doesn’t open automatically.

---

## 🧭 Using the App (Recruiter Walkthrough)

1. **Open the app** in your browser (usually `http://localhost:8501`).

2. **In the sidebar (left):**
   - Paste your **OpenAI API key** if you didn’t set the environment variable.  
   - Pick a model (for example, `gpt-4.1-mini` is a good balance of speed and quality).

3. **Upload candidate resumes (left side, main area):**
   - Click “Upload Candidate Resumes (PDF or TXT) – multiple allowed”.  
   - Select multiple resume files:
     - Supported formats: PDF and TXT.  
   - The app shows how many resumes are uploaded in the “Resumes uploaded” metric.

4. **Upload job description (right side):**
   - Click “Upload Job Description (PDF or TXT)”.  
   - Upload the JD in PDF or TXT.  
   - The “JD uploaded” metric turns to 1.

5. *(Optional)* **Shortlist filter:**
   - Toggle “Show only Strong Yes and Yes candidates” if you want to view only the shortlist.

6. Click “🔍 Evaluate All Candidates for This Role”.

7. The app will:
   - Extract text from each resume and from the JD.  
   - Build a recruiter-style prompt per candidate.  
   - Call the selected OpenAI model.  
   - Parse `Fit Score` and `Verdict` from the model output.

8. **Review results:**

   - **Shortlist Summary table**
     - Ranked by **Fit Score** (highest first).  
     - Index starts at **Rank 1, 2, 3…** (not 0).  
     - Shows:
       - Candidate file name  
       - Verdict (with emoji badges: 🟢 Strong Yes, ✅ Yes, 🟡 Maybe, 🔴 No)  
       - Fit Score (%)  

   - **Detailed Recruiter Reports**
     - For each candidate, expand the section:
       - Overall Verdict  
       - Fit Score  
       - Key Hiring Strengths  
       - Hiring Risks / Concerns  
       - Interview Focus Areas  
       - Suggested Role Level / Fit Notes  
       - Optional Note to Candidate  
     - Each section has a “Download this candidate's report (Markdown)” button.

9. **Iterate / tweak**
   - Adjust the shortlist filter.  
   - Swap in a different JD.  
   - Re-run with a different OpenAI model.

---

## 🔍 How It Works (Under the Hood)

1. **File ingestion**
   - PDFs are read via PyMuPDF (`fitz`) and converted to text.  
   - TXT files are read directly.

2. **Prompt construction**
   - For each resume, the app builds a structured prompt that includes:
     - The candidate’s resume text.  
     - The JD text.  
     - Clear instructions for the LLM to answer as a recruiter in specific Markdown sections.

3. **Model call**
   - The app calls the OpenAI Chat Completions API with:
     - A system message: “You are a recruiter / hiring manager…”  
     - A user message: the full evaluation prompt.

4. **Post-processing**
   - Uses regex to extract the `Fit Score: NN%` and `Verdict: …` from the LLM’s Markdown output.  
   - Wraps verdicts with emoji badges for quick visual scanning.

5. **Presentation**
   - Builds a summary table via Pandas and displays it using `st.table`.  
   - Shows detailed reports inside `st.expander`, with a Markdown download button per candidate.

---

## 🔐 Security Notes

- Your **OpenAI API key** is used only on your machine to call the OpenAI API.  
- It is not stored in the repository.  
- If you paste it into the app sidebar, avoid sharing your screen with that field visible.  
- For team use, prefer setting `OPENAI_API_KEY` via environment variables or a secrets manager.

---

## ⚠️ Limitations & Tips

- Results depend on the **quality of resumes and JD**:
  - Clean, text-based PDFs work best (not image scans).  
- The model doesn’t know your internal culture or salary bands:
  - Treat it as a **decision-support tool**, not a fully autonomous gatekeeper.  
- Always apply your own judgment and comply with local hiring regulations when using AI in recruitment.

---

## 📌 Future Enhancements (Ideas)

- CSV export of the shortlist table (for ATS upload).  
- Custom scoring weights (for example, skills vs experience vs domain).  
- Support for additional file formats (DOCX).  
- Tagging candidates with custom labels (for example, “pipeline”, “backup”, “next round”).  

---
