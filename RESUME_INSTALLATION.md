# 🔧 Resume Analyzer & Generator - Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Existing IntervYou application setup

---

## Installation Steps

### 1. Install Dependencies

The required packages have already been added to `requirements.txt`:

```bash
pip install PyPDF2>=3.0.0 python-docx>=1.1.0
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

Run the test script to ensure everything is working:

```bash
python test_resume_analyzer.py
```

Expected output:
```
🔍 Analyzing sample resume...
✅ Analysis successful!
📊 Overall Score: 93.4% (Grade: A+)
...
✨ Test completed successfully!
```

### 3. Start the Application

```bash
# Development mode
python fastapi_app.py

# Or with uvicorn
uvicorn fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Feature

Open your browser and navigate to:
```
http://localhost:8000/resume
```

Or access through the UI:
```
Login → Explore → Resume Analyzer
```

---

## Files Added/Modified

### New Files Created

```
resume_analyzer.py              # Core analysis module
templates/resume.html           # UI template
test_resume_analyzer.py         # Test script
test_resume_sample.txt          # Sample resume
RESUME_FEATURE.md               # Technical documentation
RESUME_USAGE_GUIDE.md           # User guide
RESUME_FEATURE_SUMMARY.md       # Implementation summary
RESUME_QUICK_REFERENCE.md       # Quick reference card
RESUME_INSTALLATION.md          # This file
```

### Modified Files

```
fastapi_app.py                  # Added resume routes
templates/index.html            # Added navigation link
requirements.txt                # Added dependencies
```

---

## Configuration

No additional configuration required! The feature uses:
- Existing authentication system
- Existing database connection
- Existing template engine
- Existing static file serving

---

## Verification Checklist

After installation, verify:

- [ ] Dependencies installed successfully
- [ ] Test script runs without errors
- [ ] Application starts without errors
- [ ] `/resume` page loads correctly
- [ ] File upload works
- [ ] Analysis returns results
- [ ] Resume generation works
- [ ] Download functionality works
- [ ] Navigation menu shows "Resume Analyzer"
- [ ] Dark mode toggle works

---

## Troubleshooting

### Issue: Import Error for PyPDF2 or python-docx

**Solution:**
```bash
pip install --upgrade PyPDF2 python-docx
```

### Issue: "Module 'resume_analyzer' not found"

**Solution:**
Ensure `resume_analyzer.py` is in the same directory as `fastapi_app.py`

### Issue: Template not found error

**Solution:**
Verify `templates/resume.html` exists and `TEMPLATES_DIR` is correctly configured in `fastapi_app.py`

### Issue: File upload fails

**Solution:**
- Check file size (max 5MB)
- Verify file format (PDF, DOCX, TXT only)
- Ensure proper file permissions

### Issue: Analysis returns empty results

**Solution:**
- Verify PDF is not image-based (scanned)
- Try converting to plain text first
- Check file encoding for TXT files

---

## Testing

### Manual Testing

1. **Test Analysis:**
   - Upload `test_resume_sample.txt`
   - Verify score is displayed
   - Check feedback items appear
   - Confirm statistics are shown

2. **Test Generation:**
   - Fill in all required fields
   - Click "Generate Resume"
   - Verify template appears
   - Test download functionality

### Automated Testing

```bash
python test_resume_analyzer.py
```

### API Testing

Using curl:

```bash
# Test analyze endpoint
curl -X POST http://localhost:8000/api/resume/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_resume_sample.txt"

# Test generate endpoint
curl -X POST http://localhost:8000/api/resume/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "location": "New York, NY",
    "summary": "Experienced professional...",
    "skills": "Python, JavaScript, Leadership"
  }'
```

---

## Production Deployment

### Environment Variables

No additional environment variables required for basic functionality.

Optional (for future AI enhancements):
```bash
OPENAI_API_KEY=your_key_here          # For AI-powered suggestions
HUGGINGFACE_TOKEN=your_token_here     # For advanced analysis
```

### Performance Considerations

- File uploads are limited to 5MB
- Analysis typically completes in <2 seconds
- No external API calls required (runs locally)
- Minimal memory footprint

### Security

- User authentication required
- File type validation
- File size limits enforced
- No file storage (processed in memory)
- XSS protection via template escaping

---

## Database

No database changes required! The feature uses:
- Existing user authentication
- No new tables needed
- All analysis done in-memory

---

## Monitoring

### Logs to Watch

```python
# In fastapi_app.py
print("✅ Resume analyzer imports successful")
```

### Metrics to Track

- Upload success rate
- Average analysis time
- User engagement (page visits)
- Download count
- Error rates

---

## Rollback

If you need to remove the feature:

1. **Remove routes from `fastapi_app.py`:**
   - Delete resume route section (lines with `/resume`, `/api/resume/*`)

2. **Remove navigation link:**
   - Edit `templates/index.html`
   - Remove Resume Analyzer link from Explore dropdown

3. **Remove files:**
   ```bash
   rm resume_analyzer.py
   rm templates/resume.html
   rm test_resume_analyzer.py
   rm test_resume_sample.txt
   rm RESUME_*.md
   ```

4. **Revert requirements.txt:**
   - Remove PyPDF2 and python-docx lines

---

## Upgrade Path

### Future Enhancements

When adding new features:

1. **AI Integration:**
   - Add OpenAI/Hugging Face credentials
   - Update `resume_analyzer.py` with AI functions
   - Test with `analyze_resume_with_ai()`

2. **ATS Optimization:**
   - Add keyword matching algorithms
   - Integrate job description parser
   - Update scoring criteria

3. **PDF Export:**
   - Add reportlab formatting
   - Create PDF templates
   - Update download functionality

---

## Support

### Documentation

- **User Guide:** `RESUME_USAGE_GUIDE.md`
- **Technical Docs:** `RESUME_FEATURE.md`
- **Quick Reference:** `RESUME_QUICK_REFERENCE.md`
- **Summary:** `RESUME_FEATURE_SUMMARY.md`

### Testing

```bash
python test_resume_analyzer.py
```

### Debugging

Enable debug mode in FastAPI:
```python
uvicorn fastapi_app:app --reload --log-level debug
```

---

## Success Criteria

Installation is successful when:

✅ All dependencies installed
✅ Test script passes
✅ Application starts without errors
✅ Feature accessible via navigation
✅ File upload works
✅ Analysis returns accurate results
✅ Resume generation works
✅ Download functionality works
✅ No console errors
✅ Mobile responsive

---

## Next Steps

After successful installation:

1. **Test thoroughly** with various resume formats
2. **Review documentation** to understand features
3. **Train users** on how to use the feature
4. **Monitor usage** and gather feedback
5. **Plan enhancements** based on user needs

---

## Quick Start Commands

```bash
# Install dependencies
pip install PyPDF2 python-docx

# Run tests
python test_resume_analyzer.py

# Start application
python fastapi_app.py

# Access feature
# Open browser: http://localhost:8000/resume
```

---

**Installation Complete! 🎉**

The Resume Analyzer & Generator is now ready to help users create professional, MNC-standard resumes!
