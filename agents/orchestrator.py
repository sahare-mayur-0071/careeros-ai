from agents.resume_agent import ResumeIntelligenceAgent
from agents.ats_agent import ATSOptimizationAgent
from agents.skill_gap_agent import SkillGapAnalysisAgent
from agents.job_match_agent import JobMatchingAgent
from agents.interview_agent import InterviewCoachAgent
from agents.roadmap_agent import LearningRoadmapAgent
from agents.certification_agent import CertificationAdvisorAgent
from agents.portfolio_agent import PortfolioBuilderAgent
from agents.branding_agent import PersonalBrandingAgent
from agents.report_agent import CareerReportAgent

from utils.scoring import calculate_career_readiness
import os

class OrchestratorAgent:
    def __init__(self):
        self.resume_agent = ResumeIntelligenceAgent()
        self.ats_agent = ATSOptimizationAgent()
        self.skill_gap_agent = SkillGapAnalysisAgent()
        self.job_match_agent = JobMatchingAgent()
        self.interview_agent = InterviewCoachAgent()
        self.roadmap_agent = LearningRoadmapAgent()
        self.cert_agent = CertificationAdvisorAgent()
        self.portfolio_agent = PortfolioBuilderAgent()
        self.branding_agent = PersonalBrandingAgent()
        self.report_agent = CareerReportAgent()

    def run_pipeline(self, resume_text: str, target_role: str, status_callback=None) -> dict:
        """Executes the full CareerOS agent pipeline."""
        session_data = {}
        import time
        
        def update_status(msg, progress):
            time.sleep(3) # Pace requests to avoid Gemini Free Tier 429 errors
            if status_callback:
                status_callback(msg, progress)

        update_status("Resume Intelligence Agent parsing resume...", 10)
        parsed_resume = self.resume_agent.process(resume_text)
        session_data['parsed_resume'] = parsed_resume

        update_status("ATS Optimization Agent analyzing...", 20)
        ats_analysis = self.ats_agent.optimize(parsed_resume, target_role)
        session_data['ats_analysis'] = ats_analysis

        update_status("Skill Gap Analysis Agent comparing skills...", 30)
        skill_gaps = self.skill_gap_agent.analyze(parsed_resume, target_role)
        session_data['skill_gaps'] = skill_gaps

        update_status("Job Matching Agent finding roles...", 40)
        job_matches = self.job_match_agent.match(parsed_resume)
        session_data['job_matches'] = job_matches

        update_status("Learning Roadmap Agent building plan...", 50)
        missing_skills = skill_gaps.get('missing_skills', []) if isinstance(skill_gaps, dict) else []
        roadmap = self.roadmap_agent.generate(missing_skills, target_role)
        session_data['roadmap'] = roadmap

        update_status("Interview Coach Agent preparing questions...", 60)
        interview_prep = self.interview_agent.generate(parsed_resume, target_role)
        session_data['interview_prep'] = interview_prep

        update_status("Certification Advisor checking credentials...", 70)
        acquired_skills = skill_gaps.get('acquired_skills', []) if isinstance(skill_gaps, dict) else []
        certs = self.cert_agent.recommend(target_role, acquired_skills, missing_skills)
        session_data['certifications'] = certs

        update_status("Portfolio Builder Agent suggesting projects...", 80)
        portfolio = self.portfolio_agent.build(target_role, missing_skills)
        session_data['portfolio'] = portfolio

        update_status("Personal Branding Agent updating profiles...", 90)
        branding = self.branding_agent.brand(parsed_resume, target_role)
        session_data['branding'] = branding

        update_status("Calculating Career Readiness Score...", 95)
        ats_score = ats_analysis.get('ats_score', 0) if isinstance(ats_analysis, dict) else 0
        top_match = 0
        if isinstance(job_matches, dict) and isinstance(job_matches.get('top_matches'), list) and len(job_matches['top_matches']) > 0:
            first_match = job_matches['top_matches'][0]
            if isinstance(first_match, dict):
                top_match = first_match.get('match_percentage', 0)
        gap_count = len(missing_skills) if isinstance(missing_skills, list) else 0
        
        proj_list = parsed_resume.get('projects') if isinstance(parsed_resume, dict) else []
        project_count = len(proj_list) if isinstance(proj_list, list) else 0
        
        readiness_score = calculate_career_readiness(ats_score, top_match, gap_count, project_count)
        
        session_data['scores'] = {
            'readiness': readiness_score,
            'ats': ats_score,
            'job_match': top_match
        }

        update_status("Generating Career Report...", 98)
        os.makedirs("reports", exist_ok=True)
        report_path = "reports/CareerOS_Report.pdf"
        self.report_agent.generate_pdf(session_data, report_path)
        session_data['report_path'] = report_path

        update_status("Pipeline Complete!", 100)
        
        return session_data
