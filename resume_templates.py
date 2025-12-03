# resume_templates.py
"""
Professional Resume Templates
Inspired by modern resume builders with multiple design options
"""

from typing import Dict, Any, List
from datetime import datetime


def format_phone(phone: str) -> str:
    """Format phone number consistently"""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone


def format_date_range(start: str, end: str) -> str:
    """Format date range consistently"""
    if end.lower() in ['present', 'current', 'now']:
        return f"{start} - Present"
    return f"{start} - {end}"


# Template 1: Professional (Clean and Modern)
def generate_professional_template(data: Dict[str, Any]) -> str:
    """Generate a clean, professional resume template"""
    
    # Contact section
    contact = f"""
{data.get('name', 'YOUR NAME').upper()}
{data.get('title', 'Professional Title')}

{data.get('email', 'email@example.com')} | {format_phone(data.get('phone', '(000) 000-0000'))} | {data.get('location', 'City, State')}
{f"LinkedIn: {data.get('linkedin', '')}" if data.get('linkedin') else ''} {f"| Portfolio: {data.get('portfolio', '')}" if data.get('portfolio') else ''}
{f"| GitHub: {data.get('github', '')}" if data.get('github') else ''}
"""

    # Professional Summary
    summary = f"""
PROFESSIONAL SUMMARY
{'─' * 80}
{data.get('summary', 'Dynamic professional with proven expertise in driving results and leading teams. Passionate about innovation and continuous improvement.')}
"""

    # Core Competencies
    skills = data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',')]
    
    skills_section = f"""
CORE COMPETENCIES
{'─' * 80}
{' • '.join(skills[:8])}
"""

    # Professional Experience
    experiences = data.get('experiences', [])
    exp_section = f"""
PROFESSIONAL EXPERIENCE
{'─' * 80}
"""
    
    for exp in experiences:
        exp_section += f"""
{exp.get('company', 'Company Name')} | {exp.get('location', 'City, State')}
{exp.get('title', 'Job Title')} | {format_date_range(exp.get('start_date', 'MM/YYYY'), exp.get('end_date', 'Present'))}

"""
        achievements = exp.get('achievements', [])
        for achievement in achievements:
            exp_section += f"• {achievement}\n"
        exp_section += "\n"

    # Education
    education = data.get('education', [])
    edu_section = f"""
EDUCATION
{'─' * 80}
"""
    
    for edu in education:
        edu_section += f"""
{edu.get('degree', 'Degree')} in {edu.get('major', 'Major')}
{edu.get('school', 'University Name')}, {edu.get('location', 'City, State')} | {edu.get('graduation', 'Year')}
{f"GPA: {edu.get('gpa', '')}" if edu.get('gpa') else ''}
{f"Honors: {edu.get('honors', '')}" if edu.get('honors') else ''}

"""

    # Certifications
    certifications = data.get('certifications', [])
    cert_section = ""
    if certifications:
        cert_section = f"""
CERTIFICATIONS
{'─' * 80}
"""
        for cert in certifications:
            cert_section += f"• {cert.get('name', 'Certification')} - {cert.get('issuer', 'Issuing Organization')}, {cert.get('year', 'Year')}\n"

    # Projects
    projects = data.get('projects', [])
    proj_section = ""
    if projects:
        proj_section = f"""
KEY PROJECTS
{'─' * 80}
"""
        for proj in projects:
            proj_section += f"""
{proj.get('name', 'Project Name')} | {proj.get('technologies', 'Technologies')}
{proj.get('description', 'Project description and your role')}

"""

    # Technical Skills
    tech_skills = data.get('technical_skills', {})
    tech_section = ""
    if tech_skills:
        tech_section = f"""
TECHNICAL SKILLS
{'─' * 80}
"""
        for category, skills_list in tech_skills.items():
            if isinstance(skills_list, list):
                tech_section += f"{category}: {', '.join(skills_list)}\n"
            else:
                tech_section += f"{category}: {skills_list}\n"

    return (contact + summary + skills_section + exp_section + 
            edu_section + cert_section + proj_section + tech_section).strip()


# Template 2: Modern (Bold and Eye-catching)
def generate_modern_template(data: Dict[str, Any]) -> str:
    """Generate a modern, bold resume template"""
    
    template = f"""
{'═' * 80}
                    {data.get('name', 'YOUR NAME').upper()}
                    {data.get('title', 'Professional Title')}
{'═' * 80}

📧 {data.get('email', 'email@example.com')}  |  📱 {format_phone(data.get('phone', '000-000-0000'))}  |  📍 {data.get('location', 'City, State')}
{f"🔗 {data.get('linkedin', '')}" if data.get('linkedin') else ''}  {f"| 🌐 {data.get('portfolio', '')}" if data.get('portfolio') else ''}

{'═' * 80}
💼 PROFESSIONAL SUMMARY
{'═' * 80}

{data.get('summary', 'Results-driven professional with expertise in delivering high-impact solutions.')}

{'═' * 80}
🎯 CORE STRENGTHS
{'═' * 80}

"""
    
    skills = data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',')]
    
    for i, skill in enumerate(skills, 1):
        template += f"  {i}. {skill}\n"
    
    template += f"""
{'═' * 80}
💼 PROFESSIONAL JOURNEY
{'═' * 80}

"""
    
    experiences = data.get('experiences', [])
    for exp in experiences:
        template += f"""
▸ {exp.get('title', 'Job Title')}
  {exp.get('company', 'Company Name')} | {exp.get('location', 'Location')}
  {format_date_range(exp.get('start_date', 'Start'), exp.get('end_date', 'End'))}
  
"""
        achievements = exp.get('achievements', [])
        for achievement in achievements:
            template += f"  ✓ {achievement}\n"
        template += "\n"
    
    template += f"""
{'═' * 80}
🎓 EDUCATION
{'═' * 80}

"""
    
    education = data.get('education', [])
    for edu in education:
        template += f"""
▸ {edu.get('degree', 'Degree')} in {edu.get('major', 'Major')}
  {edu.get('school', 'University')} | {edu.get('graduation', 'Year')}
  {f"GPA: {edu.get('gpa', '')}" if edu.get('gpa') else ''}

"""
    
    return template.strip()


# Template 3: Executive (Sophisticated)
def generate_executive_template(data: Dict[str, Any]) -> str:
    """Generate an executive-level resume template"""
    
    template = f"""
{data.get('name', 'YOUR NAME').upper()}
{data.get('title', 'Executive Title')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTACT INFORMATION
{data.get('email', 'email@example.com')} • {format_phone(data.get('phone', '000-000-0000'))} • {data.get('location', 'City, State')}
{data.get('linkedin', 'LinkedIn Profile')} • {data.get('portfolio', 'Portfolio/Website')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY

{data.get('summary', 'Senior executive with 15+ years of experience driving organizational growth and leading high-performing teams. Proven track record of strategic planning, operational excellence, and delivering measurable business results.')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AREAS OF EXPERTISE

"""
    
    skills = data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',')]
    
    # Format skills in columns
    for i in range(0, len(skills), 3):
        row = skills[i:i+3]
        template += "    " + " | ".join(f"{skill:<25}" for skill in row) + "\n"
    
    template += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL EXPERIENCE

"""
    
    experiences = data.get('experiences', [])
    for exp in experiences:
        template += f"""
{exp.get('company', 'Company Name').upper()} — {exp.get('location', 'Location')}
{exp.get('title', 'Title')} | {format_date_range(exp.get('start_date', 'Start'), exp.get('end_date', 'End'))}

"""
        achievements = exp.get('achievements', [])
        for achievement in achievements:
            template += f"    ▪ {achievement}\n"
        template += "\n"
    
    template += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EDUCATION & CREDENTIALS

"""
    
    education = data.get('education', [])
    for edu in education:
        template += f"""
{edu.get('degree', 'Degree')} in {edu.get('major', 'Major')}
{edu.get('school', 'University')}, {edu.get('location', 'Location')} | {edu.get('graduation', 'Year')}

"""
    
    return template.strip()


# Template 4: Creative (For Design/Creative Roles)
def generate_creative_template(data: Dict[str, Any]) -> str:
    """Generate a creative resume template"""
    
    template = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                     {data.get('name', 'YOUR NAME').upper().center(75)}       ║
║                     {data.get('title', 'Creative Professional').center(75)}  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ CONTACT                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

  ✉  {data.get('email', 'email@example.com')}
  ☎  {format_phone(data.get('phone', '000-000-0000'))}
  ⌂  {data.get('location', 'City, State')}
  ⚡ {data.get('portfolio', 'portfolio.com')}
  ⚡ {data.get('linkedin', 'linkedin.com/in/profile')}

┌─────────────────────────────────────────────────────────────────────────────┐
│ ABOUT ME                                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

{data.get('summary', 'Creative professional passionate about design and innovation. Bringing ideas to life through compelling visual storytelling and user-centered design.')}

┌─────────────────────────────────────────────────────────────────────────────┐
│ SKILLS & EXPERTISE                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

"""
    
    skills = data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',')]
    
    for skill in skills:
        template += f"  ★ {skill}\n"
    
    template += """
┌─────────────────────────────────────────────────────────────────────────────┐
│ EXPERIENCE                                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

"""
    
    experiences = data.get('experiences', [])
    for exp in experiences:
        template += f"""
  ► {exp.get('title', 'Title')}
    {exp.get('company', 'Company')} | {format_date_range(exp.get('start_date', 'Start'), exp.get('end_date', 'End'))}
    
"""
        achievements = exp.get('achievements', [])
        for achievement in achievements:
            template += f"    • {achievement}\n"
        template += "\n"
    
    template += """
┌─────────────────────────────────────────────────────────────────────────────┐
│ EDUCATION                                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

"""
    
    education = data.get('education', [])
    for edu in education:
        template += f"""
  ► {edu.get('degree', 'Degree')} in {edu.get('major', 'Major')}
    {edu.get('school', 'University')} | {edu.get('graduation', 'Year')}

"""
    
    return template.strip()


# Template 5: Technical (For IT/Engineering)
def generate_technical_template(data: Dict[str, Any]) -> str:
    """Generate a technical resume template"""
    
    template = f"""
{'=' * 80}
{data.get('name', 'YOUR NAME').upper()}
{data.get('title', 'Software Engineer / Technical Professional')}
{'=' * 80}

[CONTACT]
Email: {data.get('email', 'email@example.com')}
Phone: {format_phone(data.get('phone', '000-000-0000'))}
Location: {data.get('location', 'City, State')}
GitHub: {data.get('github', 'github.com/username')}
LinkedIn: {data.get('linkedin', 'linkedin.com/in/profile')}
Portfolio: {data.get('portfolio', 'portfolio.com')}

{'=' * 80}
[SUMMARY]
{'=' * 80}

{data.get('summary', 'Experienced software engineer with expertise in full-stack development, cloud architecture, and agile methodologies. Passionate about building scalable solutions and mentoring teams.')}

{'=' * 80}
[TECHNICAL SKILLS]
{'=' * 80}

"""
    
    tech_skills = data.get('technical_skills', {})
    if tech_skills:
        for category, skills_list in tech_skills.items():
            if isinstance(skills_list, list):
                template += f"{category}:\n  {', '.join(skills_list)}\n\n"
            else:
                template += f"{category}:\n  {skills_list}\n\n"
    else:
        skills = data.get('skills', [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',')]
        template += f"Core Skills:\n  {', '.join(skills)}\n\n"
    
    template += f"""
{'=' * 80}
[PROFESSIONAL EXPERIENCE]
{'=' * 80}

"""
    
    experiences = data.get('experiences', [])
    for exp in experiences:
        template += f"""
{exp.get('company', 'Company Name')} | {exp.get('location', 'Location')}
{exp.get('title', 'Title')} | {format_date_range(exp.get('start_date', 'Start'), exp.get('end_date', 'End'))}

"""
        achievements = exp.get('achievements', [])
        for achievement in achievements:
            template += f"  - {achievement}\n"
        template += "\n"
    
    # Projects section (important for technical roles)
    projects = data.get('projects', [])
    if projects:
        template += f"""
{'=' * 80}
[KEY PROJECTS]
{'=' * 80}

"""
        for proj in projects:
            template += f"""
{proj.get('name', 'Project Name')}
Technologies: {proj.get('technologies', 'Tech Stack')}
{proj.get('description', 'Project description')}
{f"Link: {proj.get('link', '')}" if proj.get('link') else ''}

"""
    
    template += f"""
{'=' * 80}
[EDUCATION]
{'=' * 80}

"""
    
    education = data.get('education', [])
    for edu in education:
        template += f"""
{edu.get('degree', 'Degree')} in {edu.get('major', 'Major')}
{edu.get('school', 'University')} | {edu.get('graduation', 'Year')}
{f"GPA: {edu.get('gpa', '')}" if edu.get('gpa') else ''}

"""
    
    return template.strip()


# Template selector
TEMPLATES = {
    'professional': {
        'name': 'Professional',
        'description': 'Clean and modern design suitable for most industries',
        'generator': generate_professional_template
    },
    'modern': {
        'name': 'Modern',
        'description': 'Bold and eye-catching with icons and visual elements',
        'generator': generate_modern_template
    },
    'executive': {
        'name': 'Executive',
        'description': 'Sophisticated design for senior-level positions',
        'generator': generate_executive_template
    },
    'creative': {
        'name': 'Creative',
        'description': 'Unique design for creative and design roles',
        'generator': generate_creative_template
    },
    'technical': {
        'name': 'Technical',
        'description': 'Optimized for IT, engineering, and technical roles',
        'generator': generate_technical_template
    }
}


def generate_resume(data: Dict[str, Any], template_name: str = 'professional') -> str:
    """Generate resume using specified template"""
    template = TEMPLATES.get(template_name, TEMPLATES['professional'])
    return template['generator'](data)


def get_available_templates() -> List[Dict[str, str]]:
    """Get list of available templates"""
    return [
        {
            'id': key,
            'name': value['name'],
            'description': value['description']
        }
        for key, value in TEMPLATES.items()
    ]
