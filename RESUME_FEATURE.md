# 📄 Resume Analyzer & Generator Feature

## Overview
The Resume Analyzer & Generator is a comprehensive tool that helps users improve their resumes and create MNC-standard CVs using AI-powered analysis.

## Features

### 1. Resume Analysis 🔍
Upload your existing resume and get instant feedback on:

- **Overall Score & Grade**: Get a comprehensive score (0-100%) with letter grade (A+ to D)
- **Detailed Scoring**:
  - Format Score (15%): Layout, length, consistency
  - Content Score (35%): Action verbs, quantifiable achievements, impact
  - Structure Score (20%): Essential sections presence
  - Language Score (15%): Grammar, tone, clarity
  - Relevance Score (15%): Industry alignment, recent experience

- **Actionable Feedback**: Prioritized recommendations for improvement
- **Statistics Dashboard**:
  - Word count analysis
  - Action verbs usage
  - Quantifiable achievements count
  - Section completeness

### 2. Resume Generation ✨
Create a professional MNC-standard resume template by filling in:

- Personal Information (name, email, phone, location)
- Professional Summary
- Core Skills & Competencies
- Work Experience
- Education
- Certifications (optional)
- Technical Skills
- Projects (optional)
- Awards & Recognition (optional)

The generator creates a well-formatted resume following industry best practices used by top companies like Google, Amazon, Microsoft, Meta, and Apple.

## Supported File Formats

### Analysis
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Plain Text (.txt)
- Maximum file size: 5MB

### Generation
- Output: Plain text format (.txt)
- Easily copy-paste into Word/Google Docs for formatting

## MNC Resume Standards

The analyzer evaluates resumes based on standards used by top multinational corporations:

### Essential Sections
1. Contact Information
2. Professional Summary (3-4 lines)
3. Core Competencies/Skills
4. Professional Experience (with quantifiable achievements)
5. Education
6. Certifications
7. Technical Skills

### Best Practices
- Use strong action verbs (Achieved, Developed, Led, Optimized, etc.)
- Include quantifiable achievements (numbers, percentages, metrics)
- Keep it concise (300-800 words for 1-2 pages)
- Use professional tone and active voice
- Tailor content to target role/industry
- Highlight recent and relevant experience

## How to Use

### Analyzing a Resume

1. Navigate to **Explore → Resume Analyzer** from the main menu
2. Click the **Analyze Resume** tab
3. Upload your resume (drag & drop or click to browse)
4. Click **Analyze Resume** button
5. Review your score, feedback, and recommendations
6. Make improvements based on the suggestions

### Generating a Resume

1. Navigate to **Explore → Resume Analyzer** from the main menu
2. Click the **Generate Resume** tab
3. Fill in all required fields:
   - Personal information
   - Professional summary
   - Skills
   - Work experience
   - Education
4. Click **Generate Resume** button
5. Review the generated template
6. Click **Download** to save as a text file
7. Copy into your preferred word processor for final formatting

## Technical Implementation

### Backend (`resume_analyzer.py`)
- Text extraction from PDF/DOCX/TXT files
- Multi-criteria analysis engine
- Scoring algorithms based on MNC standards
- Feedback generation system
- Template generation with placeholders

### Frontend (`templates/resume.html`)
- Drag-and-drop file upload
- Real-time analysis display
- Interactive form for resume generation
- Responsive design with dark mode support
- Download functionality

### API Endpoints
- `GET /resume` - Resume analyzer page
- `POST /api/resume/analyze` - Analyze uploaded resume
- `POST /api/resume/generate` - Generate resume template

## Dependencies

```
PyPDF2>=3.0.0          # PDF text extraction
python-docx>=1.1.0     # DOCX text extraction
```

## Future Enhancements

- [ ] AI-powered content suggestions using LLM
- [ ] ATS (Applicant Tracking System) optimization score
- [ ] Industry-specific templates (Tech, Finance, Healthcare, etc.)
- [ ] Multi-language support
- [ ] Resume comparison feature
- [ ] Export to PDF with professional formatting
- [ ] LinkedIn profile import
- [ ] Cover letter generator
- [ ] Interview preparation based on resume content

## Testing

Run the test script to verify functionality:

```bash
python test_resume_analyzer.py
```

This will analyze the sample resume and display detailed results.

## Integration

The Resume Analyzer is fully integrated into the IntervYou platform:

- Accessible from the **Explore** dropdown menu
- Requires user authentication
- Consistent UI/UX with the rest of the platform
- Dark mode support
- Mobile-responsive design

## Support

For issues or feature requests related to the Resume Analyzer, please contact the development team or create an issue in the project repository.

---

**Built with ❤️ for IntervYou - AI Interview Coach**
