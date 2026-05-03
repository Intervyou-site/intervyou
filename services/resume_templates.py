"""
Professional Resume PDF Templates
Supports multiple template styles with modern designs
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas as pdf_canvas
from io import BytesIO
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ResumeTemplateGenerator:
    """Generate professional resume PDFs with multiple template styles"""
    
    def __init__(self):
        self.page_width, self.page_height = letter
        self.margin = 0.75 * inch
    
    def generate_pdf(self, resume_data: Dict, template_style: str = "modern_blue") -> BytesIO:
        """Generate resume PDF with specified template style"""
        try:
            if template_style == "modern_blue":
                return self._generate_modern_blue_template(resume_data)
            elif template_style == "classic":
                return self._generate_classic_template(resume_data)
            elif template_style == "creative_dark":
                return self._generate_creative_dark_template(resume_data)
            elif template_style == "clean_minimal":
                return self._generate_clean_minimal_template(resume_data)
            elif template_style == "purple_accent":
                return self._generate_purple_accent_template(resume_data)
            else:
                return self._generate_modern_blue_template(resume_data)
        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            raise
    
    def _generate_modern_blue_template(self, resume_data: Dict) -> BytesIO:
        """Modern template with blue accent - centered header, ATS-optimized"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            rightMargin=0.75*inch, 
            leftMargin=0.75*inch, 
            topMargin=0.5*inch, 
            bottomMargin=0.5*inch
        )
        
        story = []
        styles = self._get_modern_blue_styles()
        
        # Header - Name (centered, bold, large)
        name = resume_data.get("name", "YOUR NAME").upper()
        story.append(Paragraph(name, styles["Name"]))
        story.append(Spacer(1, 0.08 * inch))
        
        # Contact Info (centered, single line with separators)
        contact_parts = []
        if resume_data.get("email"):
            contact_parts.append(resume_data["email"])
        if resume_data.get("phone"):
            contact_parts.append(resume_data["phone"])
        if resume_data.get("linkedin"):
            linkedin = resume_data["linkedin"].replace("https://", "").replace("http://", "")
            contact_parts.append(linkedin)
        
        if contact_parts:
            contact_text = " • ".join(contact_parts)
            story.append(Paragraph(contact_text, styles["Contact"]))
            story.append(Spacer(1, 0.12 * inch))
        
        # Horizontal line separator
        story.append(HRFlowable(
            width="100%", 
            thickness=1.5, 
            color=colors.HexColor("#2563EB"), 
            spaceBefore=0, 
            spaceAfter=0.18*inch
        ))
        
        # Professional Summary
        if resume_data.get("summary"):
            story.append(Paragraph("PROFESSIONAL SUMMARY", styles["SectionHeader"]))
            story.append(Spacer(1, 0.08 * inch))
            story.append(Paragraph(resume_data["summary"], styles["Body"]))
            story.append(Spacer(1, 0.2 * inch))
        
        # Experience Section
        self._add_experience_section(story, resume_data, styles)
        
        # Education Section
        self._add_education_section(story, resume_data, styles)
        
        # Skills Section (at the end for ATS optimization)
        skills = resume_data.get("skills", [])
        if skills:
            story.append(Paragraph("SKILLS", styles["SectionHeader"]))
            story.append(Spacer(1, 0.08 * inch))
            skills_text = " • ".join(skills) if isinstance(skills, list) else skills
            story.append(Paragraph(skills_text, styles["Body"]))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _generate_classic_template(self, resume_data: Dict) -> BytesIO:
        """Classic professional template"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.4*inch, bottomMargin=0.4*inch)
        
        story = []
        styles = self._get_classic_styles()
        
        # Header - left aligned
        name = resume_data.get("name", "YOUR NAME").upper()
        story.append(Paragraph(name, styles["Name"]))
        story.append(Spacer(1, 0.03 * inch))
        
        # Contact - stacked
        if resume_data.get("email"):
            story.append(Paragraph(resume_data["email"], styles["Contact"]))
        if resume_data.get("phone"):
            story.append(Paragraph(resume_data["phone"], styles["Contact"]))
        if resume_data.get("linkedin"):
            story.append(Paragraph(resume_data["linkedin"], styles["Contact"]))
        
        story.append(Spacer(1, 0.15 * inch))
        
        # Summary
        if resume_data.get("summary"):
            story.append(Paragraph("PROFESSIONAL SUMMARY", styles["SectionHeader"]))
            story.append(Spacer(1, 0.05 * inch))
            story.append(Paragraph(resume_data["summary"], styles["Body"]))
            story.append(Spacer(1, 0.15 * inch))
        
        # Skills
        skills = resume_data.get("skills", [])
        if skills:
            story.append(Paragraph("SKILLS", styles["SectionHeader"]))
            story.append(Spacer(1, 0.05 * inch))
            skills_text = " • ".join(skills) if isinstance(skills, list) else skills
            story.append(Paragraph(skills_text, styles["Body"]))
            story.append(Spacer(1, 0.15 * inch))
        
        # Experience
        self._add_experience_section(story, resume_data, styles)
        
        # Education
        self._add_education_section(story, resume_data, styles)
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _generate_creative_dark_template(self, resume_data: Dict) -> BytesIO:
        """Creative template with dark sidebar"""
        buffer = BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        
        # Dark sidebar
        c.setFillColor(colors.HexColor("#1a1f2e"))
        c.rect(0, 0, 2.5 * inch, self.page_height, fill=1, stroke=0)
        
        # Sidebar content
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        y_pos = self.page_height - 3 * inch
        
        # Contact
        c.drawString(0.3 * inch, y_pos, "CONTACT")
        y_pos -= 0.3 * inch
        c.setFont("Helvetica", 9)
        
        if resume_data.get("phone"):
            c.drawString(0.3 * inch, y_pos, resume_data["phone"])
            y_pos -= 0.2 * inch
        if resume_data.get("email"):
            c.drawString(0.3 * inch, y_pos, resume_data["email"][:25])
            y_pos -= 0.2 * inch
        if resume_data.get("linkedin"):
            c.drawString(0.3 * inch, y_pos, resume_data["linkedin"][:25])
            y_pos -= 0.4 * inch
        
        # Skills
        skills = resume_data.get("skills", [])
        if skills:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(0.3 * inch, y_pos, "SKILLS")
            y_pos -= 0.3 * inch
            c.setFont("Helvetica", 9)
            
            if isinstance(skills, list):
                for skill in skills[:10]:
                    c.drawString(0.3 * inch, y_pos, f"• {skill[:20]}")
                    y_pos -= 0.18 * inch
        
        # Main content
        c.setFillColor(colors.black)
        x_start = 3 * inch
        y_pos = self.page_height - 1 * inch
        
        # Name
        c.setFont("Helvetica-Bold", 24)
        name = resume_data.get("name", "YOUR NAME").upper()
        c.drawString(x_start, y_pos, name)
        y_pos -= 0.3 * inch
        
        # Title
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.HexColor("#666666"))
        title = resume_data.get("title", "PROFESSIONAL TITLE")
        c.drawString(x_start, y_pos, title)
        y_pos -= 0.5 * inch
        
        # Summary
        if resume_data.get("summary"):
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_start, y_pos, "SUMMARY")
            y_pos -= 0.25 * inch
            
            c.setFont("Helvetica", 10)
            summary_lines = self._wrap_text(resume_data["summary"], 50)
            for line in summary_lines[:4]:
                c.drawString(x_start, y_pos, line)
                y_pos -= 0.15 * inch
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _generate_clean_minimal_template(self, resume_data: Dict) -> BytesIO:
        """Clean minimal template"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.4*inch, bottomMargin=0.4*inch)
        
        story = []
        styles = self._get_clean_minimal_styles()
        
        # Name
        name = resume_data.get("name", "YOUR NAME").upper()
        story.append(Paragraph(name, styles["Name"]))
        story.append(Spacer(1, 0.03 * inch))
        
        # Contact
        contact_parts = []
        if resume_data.get("email"):
            contact_parts.append(resume_data["email"])
        if resume_data.get("phone"):
            contact_parts.append(resume_data["phone"])
        if resume_data.get("linkedin"):
            contact_parts.append(resume_data["linkedin"])
        
        if contact_parts:
            story.append(Paragraph(" | ".join(contact_parts), styles["Contact"]))
            story.append(Spacer(1, 0.15 * inch))
        
        # Summary
        if resume_data.get("summary"):
            story.append(Paragraph("SUMMARY", styles["SectionHeader"]))
            story.append(Spacer(1, 0.05 * inch))
            story.append(Paragraph(resume_data["summary"], styles["Body"]))
            story.append(Spacer(1, 0.15 * inch))
        
        # Experience
        self._add_experience_section(story, resume_data, styles, header="WORK EXPERIENCE")
        
        # Education
        self._add_education_section(story, resume_data, styles)
        
        # Skills
        skills = resume_data.get("skills", [])
        if skills:
            story.append(Paragraph("KEY SKILLS", styles["SectionHeader"]))
            story.append(Spacer(1, 0.05 * inch))
            skills_text = " • ".join(skills) if isinstance(skills, list) else skills
            story.append(Paragraph(skills_text, styles["Body"]))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _generate_purple_accent_template(self, resume_data: Dict) -> BytesIO:
        """Template with purple accent"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.4*inch, bottomMargin=0.4*inch)
        
        story = []
        styles = self._get_purple_accent_styles()
        
        # Name
        name = resume_data.get("name", "YOUR NAME").upper()
        story.append(Paragraph(name, styles["Name"]))
        story.append(Spacer(1, 0.03 * inch))
        
        # Contact
        contact_parts = []
        if resume_data.get("email"):
            contact_parts.append(resume_data["email"])
        if resume_data.get("phone"):
            contact_parts.append(resume_data["phone"])
        if resume_data.get("linkedin"):
            contact_parts.append(resume_data["linkedin"])
        
        if contact_parts:
            story.append(Paragraph(" | ".join(contact_parts), styles["Contact"]))
            story.append(Spacer(1, 0.1 * inch))
            story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#7C3AED"), spaceBefore=0, spaceAfter=0.12*inch))
        
        # Summary
        if resume_data.get("summary"):
            story.append(Paragraph("SUMMARY", styles["SectionHeader"]))
            story.append(Spacer(1, 0.05 * inch))
            story.append(Paragraph(resume_data["summary"], styles["Body"]))
            story.append(Spacer(1, 0.15 * inch))
        
        # Experience
        self._add_experience_section(story, resume_data, styles, header="WORK EXPERIENCE")
        
        # Education
        self._add_education_section(story, resume_data, styles)
        
        # Skills
        skills = resume_data.get("skills", [])
        if skills:
            story.append(Paragraph("SKILLS", styles["SectionHeader"]))
            story.append(Spacer(1, 0.05 * inch))
            skills_text = ", ".join(skills) if isinstance(skills, list) else skills
            story.append(Paragraph(skills_text, styles["Body"]))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _add_experience_section(self, story, resume_data, styles, header="EXPERIENCE"):
        """Add experience section with proper alignment and formatting"""
        experiences = resume_data.get("experience", [])
        if not experiences:
            return
        
        story.append(Paragraph(header, styles["SectionHeader"]))
        story.append(Spacer(1, 0.08 * inch))
        
        for i, exp in enumerate(experiences):
            title = exp.get("title", "")
            company = exp.get("company", "")
            start = exp.get("start", "")
            end = exp.get("end", "Present")
            
            # Job Title (bold, larger)
            if title:
                story.append(Paragraph(f"<b>{title}</b>", styles["JobTitle"]))
                story.append(Spacer(1, 0.02 * inch))
            
            # Company and Date (same line, company on left, date on right)
            if company and start:
                # Format dates properly
                if start and "-" in start:  # Format: 2020-01
                    start_parts = start.split("-")
                    start_formatted = f"{start_parts[0]}-{start_parts[1]}" if len(start_parts) == 2 else start
                else:
                    start_formatted = start
                
                if end and end != "Present" and "-" in end:
                    end_parts = end.split("-")
                    end_formatted = f"{end_parts[0]}-{end_parts[1]}" if len(end_parts) == 2 else end
                else:
                    end_formatted = end
                
                company_date = f'<font color="#666666"><i>{company}</i></font> | <font color="#888888">{start_formatted} – {end_formatted}</font>'
                story.append(Paragraph(company_date, styles.get("Company", styles["Body"])))
                story.append(Spacer(1, 0.06 * inch))
            elif company:
                story.append(Paragraph(f'<font color="#666666"><i>{company}</i></font>', styles.get("Company", styles["Body"])))
                story.append(Spacer(1, 0.06 * inch))
            
            # Description (bullet points)
            if exp.get("description"):
                desc_lines = exp["description"].split("\n")
                for line in desc_lines[:6]:  # Limit to 6 bullet points
                    line = line.strip()
                    if line:
                        # Remove existing bullet if present
                        if line.startswith("•") or line.startswith("-") or line.startswith("*"):
                            line = line[1:].strip()
                        story.append(Paragraph(f"• {line}", styles["Body"]))
                        story.append(Spacer(1, 0.02 * inch))
            
            # Space between experiences
            if i < len(experiences) - 1:
                story.append(Spacer(1, 0.12 * inch))
            else:
                story.append(Spacer(1, 0.2 * inch))
    
    def _add_education_section(self, story, resume_data, styles):
        """Add education section with proper alignment"""
        education = resume_data.get("education", [])
        if not education:
            return
        
        story.append(Paragraph("EDUCATION", styles["SectionHeader"]))
        story.append(Spacer(1, 0.08 * inch))
        
        for i, edu in enumerate(education):
            degree = edu.get("degree", "")
            school = edu.get("school", "")
            year = edu.get("year", "")
            gpa = edu.get("gpa", "")
            
            # Degree (bold)
            if degree:
                story.append(Paragraph(f"<b>{degree}</b>", styles["JobTitle"]))
                story.append(Spacer(1, 0.02 * inch))
            
            # School, Year, and GPA on same line
            school_parts = []
            if school:
                school_parts.append(f'<font color="#666666"><i>{school}</i></font>')
            if year:
                school_parts.append(f'<font color="#888888">{year}</font>')
            if gpa:
                school_parts.append(f'<font color="#888888">GPA: {gpa}</font>')
            
            if school_parts:
                story.append(Paragraph(" | ".join(school_parts), styles.get("Company", styles["Body"])))
            
            # Space between education entries
            if i < len(education) - 1:
                story.append(Spacer(1, 0.12 * inch))
            else:
                story.append(Spacer(1, 0.2 * inch))
    
    def _wrap_text(self, text, width):
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def _get_modern_blue_styles(self) -> Dict:
        """Styles for modern blue template - ATS-optimized with professional spacing"""
        return {
            "Name": ParagraphStyle(
                "Name", 
                fontSize=28, 
                textColor=colors.black, 
                fontName="Helvetica-Bold", 
                alignment=TA_CENTER, 
                spaceAfter=0, 
                leading=32,
                spaceBefore=0
            ),
            "Contact": ParagraphStyle(
                "Contact", 
                fontSize=10, 
                textColor=colors.HexColor("#555555"), 
                fontName="Helvetica", 
                alignment=TA_CENTER, 
                leading=14,
                spaceAfter=0
            ),
            "SectionHeader": ParagraphStyle(
                "SectionHeader", 
                fontSize=12, 
                textColor=colors.HexColor("#2563EB"), 
                fontName="Helvetica-Bold", 
                spaceBefore=0, 
                spaceAfter=0, 
                leading=16,
                borderWidth=0,
                borderPadding=0,
                leftIndent=0
            ),
            "JobTitle": ParagraphStyle(
                "JobTitle", 
                fontSize=11, 
                textColor=colors.black, 
                fontName="Helvetica-Bold", 
                spaceAfter=0, 
                leading=14,
                leftIndent=0
            ),
            "Company": ParagraphStyle(
                "Company", 
                fontSize=10, 
                textColor=colors.HexColor("#666666"), 
                fontName="Helvetica", 
                spaceAfter=0, 
                leading=13,
                leftIndent=0
            ),
            "Body": ParagraphStyle(
                "Body", 
                fontSize=10, 
                textColor=colors.HexColor("#333333"), 
                fontName="Helvetica", 
                leading=14, 
                spaceAfter=0, 
                leftIndent=12,
                bulletIndent=0
            )
        }
    
    def _get_classic_styles(self) -> Dict:
        """Styles for classic template"""
        return {
            "Name": ParagraphStyle("Name", fontSize=20, textColor=colors.black, fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=6),
            "Contact": ParagraphStyle("Contact", fontSize=10, textColor=colors.HexColor("#333333"), fontName="Helvetica", alignment=TA_LEFT),
            "SectionHeader": ParagraphStyle("SectionHeader", fontSize=12, textColor=colors.black, fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=6),
            "JobTitle": ParagraphStyle("JobTitle", fontSize=11, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=2),
            "Company": ParagraphStyle("Company", fontSize=10, textColor=colors.HexColor("#333333"), fontName="Helvetica", spaceAfter=4),
            "Body": ParagraphStyle("Body", fontSize=10, textColor=colors.HexColor("#333333"), fontName="Helvetica", leading=14, spaceAfter=2)
        }
    
    def _get_clean_minimal_styles(self) -> Dict:
        """Styles for clean minimal template"""
        return {
            "Name": ParagraphStyle("Name", fontSize=22, textColor=colors.black, fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=6),
            "Contact": ParagraphStyle("Contact", fontSize=10, textColor=colors.HexColor("#666666"), fontName="Helvetica", alignment=TA_LEFT),
            "SectionHeader": ParagraphStyle("SectionHeader", fontSize=11, textColor=colors.black, fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=6),
            "JobTitle": ParagraphStyle("JobTitle", fontSize=11, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=2),
            "Company": ParagraphStyle("Company", fontSize=10, textColor=colors.HexColor("#666666"), fontName="Helvetica", spaceAfter=4),
            "Body": ParagraphStyle("Body", fontSize=10, textColor=colors.HexColor("#333333"), fontName="Helvetica", leading=14, spaceAfter=2)
        }
    
    def _get_purple_accent_styles(self) -> Dict:
        """Styles for purple accent template"""
        return {
            "Name": ParagraphStyle("Name", fontSize=28, textColor=colors.HexColor("#7C3AED"), fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=4, leading=32),
            "Contact": ParagraphStyle("Contact", fontSize=10, textColor=colors.HexColor("#666666"), fontName="Helvetica", alignment=TA_LEFT, leading=12),
            "SectionHeader": ParagraphStyle("SectionHeader", fontSize=13, textColor=colors.HexColor("#7C3AED"), fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=4, leading=16),
            "JobTitle": ParagraphStyle("JobTitle", fontSize=11, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=2, leading=14),
            "Company": ParagraphStyle("Company", fontSize=10, textColor=colors.HexColor("#666666"), fontName="Helvetica-Oblique", spaceAfter=3, leading=12),
            "Body": ParagraphStyle("Body", fontSize=10, textColor=colors.HexColor("#333333"), fontName="Helvetica", leading=13, spaceAfter=1)
        }


# Global instance
_template_generator = None

def get_template_generator() -> ResumeTemplateGenerator:
    """Get or create global template generator"""
    global _template_generator
    if _template_generator is None:
        _template_generator = ResumeTemplateGenerator()
    return _template_generator
