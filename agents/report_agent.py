from agents.base_agent import BaseAgent
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

class CareerReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("Career Report Agent", "Generates comprehensive downloadable PDF reports.")

    def generate_pdf(self, session_data: dict, filepath: str) -> str:
        """Generates a PDF using reportlab."""
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                                rightMargin=40, leftMargin=40,
                                topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1E3A8A'),
            spaceAfter=20
        )
        h2_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#3B82F6'),
            spaceAfter=10,
            spaceBefore=15
        )
        normal_style = styles['Normal']
        
        flowables = []
        
        # Title
        flowables.append(Paragraph("CareerOS AI - Executive Report", title_style))
        flowables.append(Spacer(1, 10))
        
        # Scores
        flowables.append(Paragraph("Career Readiness Overview", h2_style))
        scores = session_data.get('scores', {})
        flowables.append(Paragraph(f"<b>Career Readiness Score:</b> {scores.get('readiness', 'N/A')}/100", normal_style))
        flowables.append(Paragraph(f"<b>ATS Score:</b> {scores.get('ats', 'N/A')}/100", normal_style))
        flowables.append(Paragraph(f"<b>Top Job Match Score:</b> {scores.get('job_match', 'N/A')}/100", normal_style))
        flowables.append(Spacer(1, 15))
        
        # Helper to add section safely
        def add_section(title, content_list):
            if not content_list: return
            story = [Paragraph(title, h2_style)]
            for item in content_list:
                story.append(Paragraph(f"• {item}", normal_style))
            story.append(Spacer(1, 15))
            flowables.append(KeepTogether(story))
            
        # ATS feedback
        ats = session_data.get('ats_analysis', {})
        add_section("ATS Improvement Suggestions", ats.get('recommended_improvements', []))
        
        # Job matches
        jobs = session_data.get('job_matches', {}).get('top_matches', [])
        job_lines = [f"{j.get('role')} ({j.get('match_percentage')}%) - {j.get('explanation')}" for j in jobs]
        add_section("Top Career Matches", job_lines)
        
        # Skill Gaps
        gaps = session_data.get('skill_gaps', {})
        add_section("Missing Skills to Learn", gaps.get('missing_skills', []))
        add_section("Learning Recommendations", gaps.get('learning_recommendations', []))
        
        # Portfolio
        portfolio = session_data.get('portfolio', {})
        projects = portfolio.get('project_ideas', [])
        proj_lines = [f"{p.get('title')}: {p.get('description')}" for p in projects]
        add_section("Recommended Portfolio Projects", proj_lines)
        
        # Certifications
        certs = session_data.get('certifications', {}).get('recommendations', [])
        cert_lines = [f"{c.get('name')} by {c.get('provider')} - {c.get('reason')}" for c in certs]
        add_section("Recommended Certifications", cert_lines)
        
        # Branding
        branding = session_data.get('branding', {})
        brand_lines = [
            f"<b>LinkedIn Headline:</b> {branding.get('linkedin_headline', '')}",
            f"<b>LinkedIn About:</b> {branding.get('linkedin_about', '')}"
        ]
        add_section("Personal Branding Ideas", brand_lines)
        
        # Build PDF
        try:
            doc.build(flowables)
        except Exception as e:
            self.logger.error(f"Error building PDF: {e}")
            
        return filepath
