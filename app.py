import streamlit as st
import os
import tempfile
import plotly.graph_objects as go
from dotenv import load_dotenv

from agents.orchestrator import OrchestratorAgent
from utils.file_parser import parse_pdf, parse_image
from utils.storage import load_memory, save_memory

load_dotenv()

st.set_page_config(
    page_title="CareerOS AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2563eb;
    }
    .metric-title {
        font-size: 1rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .section-header {
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 10px;
        margin-bottom: 20px;
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'session_data' not in st.session_state:
    st.session_state.session_data = load_memory()

def render_metric(title, value, color="#2563eb"):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value" style="color: {color}">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("💼 CareerOS AI")
    st.markdown("Your Autonomous Career Operating System.")
    
    api_key = st.text_input("Gemini API Key", type="password", help="Required if not in .env")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        import google.generativeai as genai
        genai.configure(api_key=api_key)

    target_role = st.selectbox(
        "Target Career Path",
        ["Software Engineer", "Full Stack Developer", "Data Analyst", 
         "Data Scientist", "AI Engineer", "Machine Learning Engineer",
         "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "Product Manager"]
    )

    uploaded_file = st.file_uploader("Upload Resume (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
    
    if st.button("Launch CareerOS Pipeline", type="primary", use_container_width=True):
        if not os.getenv("GEMINI_API_KEY"):
            st.error("API Key is missing!")
        elif not uploaded_file:
            st.error("Please upload a resume.")
        else:
            with st.spinner("Booting CareerOS AI..."):
                file_ext = uploaded_file.name.split('.')[-1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    if file_ext == "pdf":
                        resume_text = parse_pdf(tmp_path)
                    elif file_ext in ["png", "jpg", "jpeg"]:
                        resume_text = parse_image(tmp_path)
                    else:
                        resume_text = ""
                    
                    status_placeholder = st.empty()
                    progress_bar = st.progress(0)
                    
                    def ui_callback(msg, prog):
                        status_placeholder.text(msg)
                        progress_bar.progress(prog)
                        
                    orchestrator = OrchestratorAgent()
                    data = orchestrator.run_pipeline(resume_text, target_role, ui_callback)
                    
                    st.session_state.session_data = data
                    save_memory(data)
                    
                    status_placeholder.empty()
                    progress_bar.empty()
                    st.success("Analysis Complete!")
                    
                except Exception as e:
                    st.error(f"Pipeline Error: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                        
    if st.session_state.session_data:
        if st.button("Clear Memory & Restart", use_container_width=True):
            st.session_state.session_data = {}
            save_memory({})
            st.rerun()

# --- Main Dashboard ---
if st.session_state.session_data:
    data = st.session_state.session_data
    scores = data.get('scores') if isinstance(data.get('scores'), dict) else {}
    
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>CareerOS Executive Dashboard</h1>", unsafe_allow_html=True)
    
    # 1. Top Level Metrics
    c1, c2, c3 = st.columns(3)
    with c1: render_metric("Career Readiness", f"{scores.get('readiness', 0)}/100", "#10b981")
    with c2: render_metric("ATS Score", f"{scores.get('ats', 0)}/100", "#3b82f6")
    with c3: render_metric("Top Job Match", f"{scores.get('job_match', 0)}%", "#8b5cf6")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for granular data
    tabs = st.tabs([
        "📄 Resume & ATS", 
        "🎯 Skills & Jobs", 
        "📚 Learning Plan", 
        "🛠️ Portfolio & Brand", 
        "🎙️ Interview Prep"
    ])
    
    with tabs[0]: # Resume & ATS
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 class='section-header'>Resume Intelligence</h3>", unsafe_allow_html=True)
            res = data.get('parsed_resume') if isinstance(data.get('parsed_resume'), dict) else {}
            st.write("**Summary:**", res.get('summary', ''))
            st.write("**Extracted Skills:**", ", ".join(res.get('skills', [])))
        with col2:
            st.markdown("<h3 class='section-header'>ATS Optimization</h3>", unsafe_allow_html=True)
            ats = data.get('ats_analysis') if isinstance(data.get('ats_analysis'), dict) else {}
            st.error("**Missing Keywords:** " + ", ".join(ats.get('missing_keywords', []) if isinstance(ats.get('missing_keywords'), list) else []))
            for imp in (ats.get('recommended_improvements', []) if isinstance(ats.get('recommended_improvements'), list) else []):
                st.info(imp)
                
    with tabs[1]: # Skills & Jobs
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 class='section-header'>Skill Gap Analysis</h3>", unsafe_allow_html=True)
            gaps = data.get('skill_gaps') if isinstance(data.get('skill_gaps'), dict) else {}
            st.warning("**Critical Gaps:**")
            for g in (gaps.get('critical_gaps', []) if isinstance(gaps.get('critical_gaps'), list) else []): st.write(f"- {g}")
        with col2:
            st.markdown("<h3 class='section-header'>Top Job Matches</h3>", unsafe_allow_html=True)
            job_matches_dict = data.get('job_matches') if isinstance(data.get('job_matches'), dict) else {}
            jobs = job_matches_dict.get('top_matches') if isinstance(job_matches_dict.get('top_matches'), list) else []
            for j in jobs:
                if isinstance(j, dict):
                    st.success(f"**{j.get('role')} ({j.get('match_percentage')}%)**\\n{j.get('explanation')}")
                
    with tabs[2]: # Learning Plan
        st.markdown("<h3 class='section-header'>90-Day Learning Roadmap</h3>", unsafe_allow_html=True)
        rm = data.get('roadmap') if isinstance(data.get('roadmap'), dict) else {}
        c1, c2, c3 = st.columns(3)
        for i, period in enumerate(['30_days', '60_days', '90_days']):
            with [c1, c2, c3][i]:
                plan = rm.get(f'roadmap_{period}') if isinstance(rm.get(f'roadmap_{period}'), dict) else {}
                st.write(f"### Day {period.split('_')[0]}")
                st.write(f"**Focus:** {plan.get('focus', '')}")
                st.write("**Goals:**")
                for g in (plan.get('weekly_goals', []) if isinstance(plan.get('weekly_goals'), list) else []): st.write(f"- {g}")
        
        st.markdown("### Recommended Certifications")
        certs_dict = data.get('certifications') if isinstance(data.get('certifications'), dict) else {}
        certs = certs_dict.get('recommendations') if isinstance(certs_dict.get('recommendations'), list) else []
        for c in certs:
            if isinstance(c, dict):
                st.write(f"🏆 **{c.get('name')}** ({c.get('provider')}) - {c.get('reason')}")

    with tabs[3]: # Portfolio & Brand
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 class='section-header'>Portfolio Builder</h3>", unsafe_allow_html=True)
            port = data.get('portfolio') if isinstance(data.get('portfolio'), dict) else {}
            for p in (port.get('project_ideas', []) if isinstance(port.get('project_ideas'), list) else []):
                if isinstance(p, dict):
                    with st.expander(f"💡 {p.get('title')}"):
                        st.write(p.get('description'))
                        stack = p.get('tech_stack', [])
                        st.write("**Stack:**", ", ".join(stack if isinstance(stack, list) else []))
        with col2:
            st.markdown("<h3 class='section-header'>Personal Branding</h3>", unsafe_allow_html=True)
            brand = data.get('branding') if isinstance(data.get('branding'), dict) else {}
            st.text_area("LinkedIn Headline", brand.get('linkedin_headline', ''), height=70)
            st.text_area("LinkedIn About", brand.get('linkedin_about', ''), height=150)

    with tabs[4]: # Interview Prep
        st.markdown("<h3 class='section-header'>Interview Coach</h3>", unsafe_allow_html=True)
        prep = data.get('interview_prep') if isinstance(data.get('interview_prep'), dict) else {}
        
        qt1, qt2, qt3 = st.tabs(["Technical", "Behavioral", "Project Discussion"])
        with qt1:
            for q in (prep.get('technical_questions', []) if isinstance(prep.get('technical_questions'), list) else []):
                if isinstance(q, dict):
                    with st.expander(q.get('question', '')):
                        for pt in (q.get('expected_answer_points', []) if isinstance(q.get('expected_answer_points'), list) else []): st.write(f"- {pt}")
        with qt2:
            for q in (prep.get('behavioral_questions', []) if isinstance(prep.get('behavioral_questions'), list) else []):
                if isinstance(q, dict):
                    with st.expander(q.get('question', '')):
                        for pt in (q.get('expected_answer_points', []) if isinstance(q.get('expected_answer_points'), list) else []): st.write(f"- {pt}")
        with qt3:
            for q in (prep.get('project_discussion_questions', []) if isinstance(prep.get('project_discussion_questions'), list) else []):
                if isinstance(q, dict):
                    with st.expander(q.get('question', '')):
                        for pt in (q.get('expected_answer_points', []) if isinstance(q.get('expected_answer_points'), list) else []): st.write(f"- {pt}")

    # Sidebar Download
    report_path = data.get('report_path')
    if report_path and os.path.exists(report_path):
        with st.sidebar:
            st.markdown("---")
            with open(report_path, "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name="CareerOS_Report.pdf", mime="application/pdf", use_container_width=True, type="primary")
else:
    st.info("👈 Upload your resume and click 'Launch CareerOS Pipeline' to begin.")
