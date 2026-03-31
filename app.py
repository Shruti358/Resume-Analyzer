import json
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

from job_listings import load_jobs_df, rank_jobs_by_resume_skills
from ml_model import analyze_resume
from utils import extract_skills

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    PdfReader = None


def _read_uploaded_text(upload) -> str:
    if upload is None:
        return ""

    name = (upload.name or "").lower()
    data = upload.getvalue()

    if name.endswith(".txt"):
        for enc in ("utf-8", "utf-16", "cp1252"):
            try:
                return data.decode(enc)
            except Exception:
                continue
        return data.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        if PdfReader is None:
            raise RuntimeError("PDF support requires 'pypdf'. Please install it from requirements.txt.")
        reader = PdfReader(BytesIO(data))
        parts: list[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return "\n".join(parts).strip()

    raise RuntimeError("Unsupported file type. Please upload a .txt or .pdf file.")


def _skills_df(resume_skills: list[str], job_skills: list[str]) -> pd.DataFrame:
    resume_set = set(resume_skills)
    job_set = set(job_skills)
    all_skills = sorted(job_set | resume_set)
    rows = []
    for s in all_skills:
        rows.append(
            {
                "skill": s,
                "in_resume": s in resume_set,
                "in_job": s in job_set,
                "status": (
                    "Matched" if (s in resume_set and s in job_set) else
                    "Missing" if (s in job_set and s not in resume_set) else
                    "Extra"
                ),
            }
        )
    return pd.DataFrame(rows)


# Page configuration
st.set_page_config(page_title="Resume Analyzer Dashboard", page_icon="📄", layout="wide")

st.markdown(
    """
<style>
  .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
  .stMetric { border: 1px solid rgba(49, 51, 63, 0.2); padding: 14px; border-radius: 12px; }
  .small-muted { color: rgba(49, 51, 63, 0.7); font-size: 0.9rem; }
</style>
""",
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("📊 Dashboard")
    page = st.radio(
        "Navigate",
        ["Job Recommendations", "Analyzer", "History", "Form demo", "About"],
        index=1,
    )
    st.markdown("---")
    st.caption("Tip: Use `python -m streamlit run app.py` to launch.")


if page == "Job Recommendations":
    st.title("Job Recommendation App")
    st.write("Upload your resume in PDF format")
    st.markdown("---")

    uploaded = st.file_uploader("Choose a file", type=["pdf", "txt"], help="PDF or TXT — PDF preferred.")

    if uploaded is not None:
        try:
            text = _read_uploaded_text(uploaded)
            if not text.strip():
                st.warning("No text could be read from the file. Try another PDF or use TXT.")
            else:
                skills = extract_skills(text)
                jobs_df = load_jobs_df()
                ranked = rank_jobs_by_resume_skills(skills, jobs_df)
                st.subheader("Recommended Jobs:")
                st.dataframe(ranked, use_container_width=True, hide_index=True)
                if not skills:
                    st.caption(
                        "No skills from the predefined list were found in your resume. "
                        "Recommendations are shown in default order; add tech keywords to improve matching."
                    )
        except Exception as e:
            st.error(f"Could not process file: {e}")
    else:
        st.info("Upload a resume PDF (or TXT) to see ranked job recommendations.")

elif page == "Analyzer":
    st.title("AI Resume Analyzer")
    st.markdown(
        '<div class="small-muted">Compare a resume against a job description and get a clear skills-gap report.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    left, right = st.columns(2, gap="large")

    with left:
        st.subheader("📄 Resume")
        resume_upload = st.file_uploader("Upload Resume (TXT/PDF)", type=["txt", "pdf"], key="resume_upload")
        resume_text = st.text_area("Or paste resume text", height=260, placeholder="Paste your resume here...")

    with right:
        st.subheader("💼 Job Description")
        job_upload = st.file_uploader("Upload Job Description (TXT/PDF)", type=["txt", "pdf"], key="job_upload")
        job_text = st.text_area("Or paste job description", height=260, placeholder="Paste the job description here...")

    with st.expander("⚙️ Options", expanded=False):
        show_extras = st.checkbox("Show extra skills (in resume but not required)", value=True)
        table_filter = st.multiselect("Filter table", ["Matched", "Missing", "Extra"], default=["Matched", "Missing", "Extra"])

    analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)

    if analyze:
        try:
            resume_src = _read_uploaded_text(resume_upload) if resume_upload else ""
            job_src = _read_uploaded_text(job_upload) if job_upload else ""

            final_resume_text = (resume_src.strip() or resume_text.strip())
            final_job_text = (job_src.strip() or job_text.strip())

            if not final_resume_text or not final_job_text:
                st.warning("⚠️ Please provide both Resume and Job Description (upload or paste).")
                st.stop()

            resume_skills = extract_skills(final_resume_text)
            job_skills = extract_skills(final_job_text)

            if not job_skills:
                st.warning("⚠️ No recognized skills found in the job description.")
                st.stop()

            result = analyze_resume(resume_skills, job_skills)
            match_percentage = int(result["match_score"] * 100)

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Match Score", f"{match_percentage}%")
            m2.metric("Matched Skills", len(set(resume_skills) & set(job_skills)))
            m3.metric("Missing Skills", len(result["missing_skills"]))
            m4.metric("Resume Skills Found", len(set(resume_skills)))

            st.markdown("### Confidence")
            st.progress(result["probability"])

            df = _skills_df(resume_skills, job_skills)
            if not show_extras:
                df = df[df["status"] != "Extra"]
            if table_filter:
                df = df[df["status"].isin(table_filter)]

            c1, c2 = st.columns([1, 1], gap="large")
            with c1:
                st.markdown("### Skills Breakdown")
                counts = df["status"].value_counts().reindex(["Matched", "Missing", "Extra"]).fillna(0).astype(int)
                st.bar_chart(counts)

            with c2:
                st.markdown("### Skills Table")
                st.dataframe(df.sort_values(["status", "skill"]), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("📚 Skills to Learn (Priority)")
            if result["learning_path"]:
                for i, skill in enumerate(result["learning_path"], 1):
                    st.write(f"{i}. **{skill.title()}**")
            else:
                st.success("✅ You have all the required skills!")

            report = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "match_percentage": match_percentage,
                "result": result,
                "resume_skills": sorted(set(resume_skills)),
                "job_skills": sorted(set(job_skills)),
            }
            st.session_state.history.insert(0, report)

            st.markdown("---")
            st.subheader("⬇️ Download Report")
            r1, r2 = st.columns(2)
            with r1:
                st.download_button(
                    "Download JSON",
                    data=json.dumps(report, indent=2).encode("utf-8"),
                    file_name="resume_analysis_report.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with r2:
                st.download_button(
                    "Download Skills CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="skills_breakdown.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")

elif page == "History":
    st.title("History")
    st.markdown('<div class="small-muted">Your recent analyses in this session.</div>', unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.history:
        st.info("No history yet. Run an analysis from the Analyzer page.")
    else:
        for item in st.session_state.history[:10]:
            with st.expander(f"{item['timestamp']} — Match {item['match_percentage']}%"):
                st.json(item)

        if st.button("Clear history", use_container_width=True):
            st.session_state.history = []
            st.rerun()

elif page == "Form demo":
    st.title("Outside vs inside `st.form`")
    st.markdown(
        '<div class="small-muted">Widgets outside a form rerun the script on every change. '
        "Inside a form, widget values are applied when you click the form submit button.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    fc1, fc2 = st.columns(2, gap="large")
    with fc1:
        st.subheader("Outside a form")
        out_txt = st.text_input("Outside text input", key="demo_out_txt")
        out_area = st.text_area("Outside text area", key="demo_out_area")
        st.markdown("---")
        st.subheader("Values from outside")
        st.write("**Text input:**", out_txt)
        st.write("**Text area:**", out_area)
    with fc2:
        st.subheader("Inside a form")
        with st.form("streamlit_form_demo"):
            in_txt = st.text_input("Inside text input")
            in_area = st.text_area("Inside text area")
            form_submitted = st.form_submit_button("Submit form")
        st.markdown("---")
        st.subheader("Values from inside")
        if form_submitted:
            st.write("**Text input:**", in_txt)
            st.write("**Text area:**", in_area)
        else:
            st.caption("Submit the form to update the values below.")
            st.write("**Text input:**", "—")
            st.write("**Text area:**", "—")

elif page == "About":
    st.title("About")
    st.markdown(
        """
This dashboard extracts skills from a resume and a job description, then:
- calculates a match score
- lists missing skills as a learning path
- generates a downloadable report

**Input formats**: Paste text, or upload `TXT/PDF`.

**Job Recommendations** ranks sample listings using skills extracted from your resume.
""".strip()
    )