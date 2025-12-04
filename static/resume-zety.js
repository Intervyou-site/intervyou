// Resume Builder JavaScript
let resumeData = {
    template: 'professional',
    name: '',
    title: '',
    email: '',
    phone: '',
    location: '',
    linkedin: '',
    summary: '',
    experiences: [],
    education: [],
    skills: []
};

let zoomLevel = 100;
let experienceCount = 0;
let educationCount = 0;
let updateTimeout = null;

// Debounced update to prevent flickering
function debouncedUpdate() {
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(() => {
        updatePreview();
    }, 300);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    addExperience();
    addEducation();
    updatePreview();
});

function setupEventListeners() {
    // Personal info inputs with debouncing
    ['name', 'title', 'email', 'phone', 'location', 'linkedin'].forEach(field => {
        const input = document.getElementById(field);
        if (input) {
            input.addEventListener('input', (e) => {
                resumeData[field] = e.target.value;
                debouncedUpdate();
            });
        }
    });

    // Summary with debouncing
    const summary = document.getElementById('summary');
    if (summary) {
        summary.addEventListener('input', (e) => {
            resumeData.summary = e.target.value;
            const count = document.getElementById('summaryCount');
            if (count) count.textContent = e.target.value.length;
            debouncedUpdate();
        });
    }

    // Skills input
    const skillInput = document.getElementById('skillInput');
    if (skillInput) {
        skillInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.target.value.trim()) {
                e.preventDefault();
                addSkill(e.target.value.trim());
                e.target.value = '';
            }
        });
    }

    // Template selection
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.template-card').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            resumeData.template = this.dataset.template;
            updatePreview();
        });
    });

    // Download button
    document.getElementById('downloadBtn').addEventListener('click', downloadPDF);
}

function addExperience() {
    experienceCount++;
    const experience = {
        id: experienceCount,
        company: '',
        title: '',
        location: '',
        startDate: '',
        endDate: '',
        achievements: ['']
    };
    
    resumeData.experiences.push(experience);
    
    const html = `
        <div class="experience-item" data-id="${experienceCount}">
            <div class="item-header">
                <div class="item-number">${experienceCount}</div>
                <button class="remove-btn" onclick="removeExperience(${experienceCount})">
                    <i class="fas fa-trash"></i> Remove
                </button>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Company *</label>
                    <input type="text" onchange="updateExperience(${experienceCount}, 'company', this.value)" placeholder="Company Name">
                </div>
                <div class="form-group">
                    <label>Job Title *</label>
                    <input type="text" onchange="updateExperience(${experienceCount}, 'title', this.value)" placeholder="Software Engineer">
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" onchange="updateExperience(${experienceCount}, 'location', this.value)" placeholder="City, State">
                </div>
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="month" onchange="updateExperience(${experienceCount}, 'startDate', this.value)">
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="month" onchange="updateExperience(${experienceCount}, 'endDate', this.value)">
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" onchange="toggleCurrent(${experienceCount}, this.checked)"> Currently working here
                    </label>
                </div>
            </div>
            <div class="form-group" style="margin-top: 16px;">
                <label>Key Achievements</label>
                <textarea rows="3" onchange="updateExperience(${experienceCount}, 'achievements', this.value.split('\\n'))" placeholder="• Led team of 5 developers&#10;• Increased performance by 40%&#10;• Implemented CI/CD pipeline"></textarea>
            </div>
        </div>
    `;
    
    document.getElementById('experienceList').insertAdjacentHTML('beforeend', html);
}

function removeExperience(id) {
    resumeData.experiences = resumeData.experiences.filter(exp => exp.id !== id);
    document.querySelector(`.experience-item[data-id="${id}"]`).remove();
    updatePreview();
}

function updateExperience(id, field, value) {
    const exp = resumeData.experiences.find(e => e.id === id);
    if (exp) {
        exp[field] = value;
        updatePreview();
    }
}

function toggleCurrent(id, isCurrent) {
    const exp = resumeData.experiences.find(e => e.id === id);
    if (exp) {
        exp.endDate = isCurrent ? 'Present' : '';
        updatePreview();
    }
}

function addEducation() {
    educationCount++;
    const education = {
        id: educationCount,
        degree: '',
        major: '',
        school: '',
        location: '',
        graduation: '',
        gpa: ''
    };
    
    resumeData.education.push(education);
    
    const html = `
        <div class="education-item" data-id="${educationCount}">
            <div class="item-header">
                <div class="item-number">${educationCount}</div>
                <button class="remove-btn" onclick="removeEducation(${educationCount})">
                    <i class="fas fa-trash"></i> Remove
                </button>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Degree *</label>
                    <input type="text" onchange="updateEducation(${educationCount}, 'degree', this.value)" placeholder="Bachelor of Science">
                </div>
                <div class="form-group">
                    <label>Major/Field</label>
                    <input type="text" onchange="updateEducation(${educationCount}, 'major', this.value)" placeholder="Computer Science">
                </div>
                <div class="form-group">
                    <label>School *</label>
                    <input type="text" onchange="updateEducation(${educationCount}, 'school', this.value)" placeholder="University Name">
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" onchange="updateEducation(${educationCount}, 'location', this.value)" placeholder="City, State">
                </div>
                <div class="form-group">
                    <label>Graduation Date</label>
                    <input type="month" onchange="updateEducation(${educationCount}, 'graduation', this.value)">
                </div>
                <div class="form-group">
                    <label>GPA (Optional)</label>
                    <input type="text" onchange="updateEducation(${educationCount}, 'gpa', this.value)" placeholder="3.8/4.0">
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('educationList').insertAdjacentHTML('beforeend', html);
}

function removeEducation(id) {
    resumeData.education = resumeData.education.filter(edu => edu.id !== id);
    document.querySelector(`.education-item[data-id="${id}"]`).remove();
    updatePreview();
}

function updateEducation(id, field, value) {
    const edu = resumeData.education.find(e => e.id === id);
    if (edu) {
        edu[field] = value;
        updatePreview();
    }
}

function addSkill(skill) {
    if (!resumeData.skills.includes(skill)) {
        resumeData.skills.push(skill);
        renderSkills();
        updatePreview();
    }
}

function removeSkill(skill) {
    resumeData.skills = resumeData.skills.filter(s => s !== skill);
    renderSkills();
    updatePreview();
}

function renderSkills() {
    const container = document.getElementById('skillsList');
    container.innerHTML = resumeData.skills.map(skill => `
        <span class="skill-tag">
            ${escapeHtml(skill)}
            <i class="fas fa-times" onclick="removeSkill('${escapeHtml(skill)}')"></i>
        </span>
    `).join('');
}

function updatePreview() {
    const preview = document.getElementById('resumePreview');
    if (!preview) return;
    
    // Check if RESUME_TEMPLATES is defined
    const template = (typeof RESUME_TEMPLATES !== 'undefined' && RESUME_TEMPLATES[resumeData.template]) 
        ? RESUME_TEMPLATES[resumeData.template] 
        : { fonts: { body: "'Inter', sans-serif", heading: "'Inter', sans-serif" }, colors: { primary: '#2563eb' } };
    
    // Apply template-specific fonts
    if (template.fonts && template.fonts.body) {
        preview.style.fontFamily = template.fonts.body;
    }
    
    preview.innerHTML = generateResumeHTML();
}

function generateResumeHTML() {
    const preview = document.getElementById('resumePreview');
    if (preview) {
        preview.className = `resume-preview ${resumeData.template}`;
    }
    
    const template = (typeof RESUME_TEMPLATES !== 'undefined' && RESUME_TEMPLATES[resumeData.template]) 
        ? RESUME_TEMPLATES[resumeData.template]
        : { fonts: { body: "'Inter', sans-serif", heading: "'Inter', sans-serif" }, colors: { primary: '#2563eb' } };
    
    // Template-specific generation
    if (resumeData.template === 'modern' || resumeData.template === 'tech') {
        return generateTwoColumnTemplate(template);
    }
    
    // Default single-column template structure
    const headingFont = template.fonts && template.fonts.heading ? template.fonts.heading : "'Inter', sans-serif";
    let html = `
        <div class="resume-header">
            <div class="resume-name" style="font-family: ${headingFont};">${escapeHtml(resumeData.name) || 'Your Name'}</div>
            <div class="resume-title">${escapeHtml(resumeData.title) || 'Professional Title'}</div>
            <div class="resume-contact">
                ${resumeData.email ? `<span><i class="fas fa-envelope"></i> ${escapeHtml(resumeData.email)}</span>` : ''}
                ${resumeData.phone ? `<span><i class="fas fa-phone"></i> ${escapeHtml(resumeData.phone)}</span>` : ''}
                ${resumeData.location ? `<span><i class="fas fa-map-marker-alt"></i> ${escapeHtml(resumeData.location)}</span>` : ''}
                ${resumeData.linkedin ? `<span><i class="fab fa-linkedin"></i> ${escapeHtml(resumeData.linkedin)}</span>` : ''}
            </div>
        </div>
    `;

    if (resumeData.summary) {
        html += `
            <div class="resume-section">
                <div class="resume-section-title">Professional Summary</div>
                <div class="resume-summary">${escapeHtml(resumeData.summary)}</div>
            </div>
        `;
    }

    if (resumeData.experiences.length > 0 && resumeData.experiences.some(e => e.company)) {
        html += `<div class="resume-section">
            <div class="resume-section-title">Work Experience</div>`;
        
        resumeData.experiences.forEach(exp => {
            if (exp.company) {
                html += `
                    <div class="resume-experience-item">
                        <div class="resume-item-header">
                            <div class="resume-item-title">${escapeHtml(exp.title) || 'Job Title'}</div>
                            <div class="resume-item-date">${formatDate(exp.startDate)} - ${exp.endDate === 'Present' ? 'Present' : formatDate(exp.endDate)}</div>
                        </div>
                        <div class="resume-item-subtitle">${escapeHtml(exp.company)}${exp.location ? ` • ${escapeHtml(exp.location)}` : ''}</div>
                        ${exp.achievements && exp.achievements.length > 0 && exp.achievements[0] ? `
                            <ul class="resume-item-achievements">
                                ${exp.achievements.filter(a => a.trim()).map(achievement => `<li>${escapeHtml(achievement)}</li>`).join('')}
                            </ul>
                        ` : ''}
                    </div>
                `;
            }
        });
        
        html += `</div>`;
    }

    if (resumeData.education.length > 0 && resumeData.education.some(e => e.school)) {
        html += `<div class="resume-section">
            <div class="resume-section-title">Education</div>`;
        
        resumeData.education.forEach(edu => {
            if (edu.school) {
                html += `
                    <div class="resume-education-item">
                        <div class="resume-item-header">
                            <div class="resume-item-title">${escapeHtml(edu.degree)}${edu.major ? ` in ${escapeHtml(edu.major)}` : ''}</div>
                            <div class="resume-item-date">${formatDate(edu.graduation)}</div>
                        </div>
                        <div class="resume-item-subtitle">${escapeHtml(edu.school)}${edu.location ? ` • ${escapeHtml(edu.location)}` : ''}</div>
                        ${edu.gpa ? `<div style="font-size: 13px; color: #64748b; margin-top: 4px;">GPA: ${escapeHtml(edu.gpa)}</div>` : ''}
                    </div>
                `;
            }
        });
        
        html += `</div>`;
    }

    if (resumeData.skills.length > 0) {
        html += `
            <div class="resume-section">
                <div class="resume-section-title">Skills</div>
                <div class="resume-skills">
                    ${resumeData.skills.map(skill => `<span class="resume-skill">${escapeHtml(skill)}</span>`).join('')}
                </div>
            </div>
        `;
    }

    return html;
}

function formatDate(dateStr) {
    if (!dateStr || dateStr === 'Present') return dateStr || '';
    const date = new Date(dateStr + '-01');
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function zoomIn() {
    if (zoomLevel < 150) {
        zoomLevel += 10;
        applyZoom();
    }
}

function zoomOut() {
    if (zoomLevel > 50) {
        zoomLevel -= 10;
        applyZoom();
    }
}

function applyZoom() {
    document.getElementById('resumePreview').style.transform = `scale(${zoomLevel / 100})`;
    document.getElementById('zoomLevel').textContent = `${zoomLevel}%`;
}

function generateTwoColumnTemplate(template) {
    const sidebarColor = (template.colors && template.colors.sidebar) ? template.colors.sidebar : '#2563eb';
    const headingFont = (template.fonts && template.fonts.heading) ? template.fonts.heading : "'Inter', sans-serif";
    return `
        <div class="resume-sidebar" style="background: ${sidebarColor};">
            <div class="resume-name" style="font-family: ${headingFont};">${escapeHtml(resumeData.name) || 'Your Name'}</div>
            <div class="resume-title">${escapeHtml(resumeData.title) || 'Professional Title'}</div>
            
            ${resumeData.email || resumeData.phone || resumeData.location ? `
                <div class="resume-section" style="margin-top: 30px;">
                    <div class="resume-section-title">Contact</div>
                    ${resumeData.email ? `<div style="margin-bottom: 8px; font-size: 13px;"><i class="fas fa-envelope"></i> ${escapeHtml(resumeData.email)}</div>` : ''}
                    ${resumeData.phone ? `<div style="margin-bottom: 8px; font-size: 13px;"><i class="fas fa-phone"></i> ${escapeHtml(resumeData.phone)}</div>` : ''}
                    ${resumeData.location ? `<div style="margin-bottom: 8px; font-size: 13px;"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(resumeData.location)}</div>` : ''}
                </div>
            ` : ''}
            
            ${resumeData.skills.length > 0 ? `
                <div class="resume-section">
                    <div class="resume-section-title">Skills</div>
                    ${resumeData.skills.map(skill => `<div style="margin-bottom: 6px; font-size: 13px;">• ${escapeHtml(skill)}</div>`).join('')}
                </div>
            ` : ''}
        </div>
        <div class="resume-main">
            ${resumeData.summary ? `
                <div class="resume-section">
                    <div class="resume-section-title" style="color: #1e293b; border-bottom-color: #e2e8f0;">Profile</div>
                    <div class="resume-summary">${escapeHtml(resumeData.summary)}</div>
                </div>
            ` : ''}
            
            ${generateExperienceSection()}
            ${generateEducationSection()}
        </div>
    `;
}

function generateExperienceSection() {
    if (resumeData.experiences.length === 0 || !resumeData.experiences.some(e => e.company)) {
        return '';
    }
    
    let html = `<div class="resume-section">
        <div class="resume-section-title" style="color: #1e293b; border-bottom-color: #e2e8f0;">Experience</div>`;
    
    resumeData.experiences.forEach(exp => {
        if (exp.company) {
            html += `
                <div class="resume-experience-item">
                    <div class="resume-item-header">
                        <div class="resume-item-title">${escapeHtml(exp.title) || 'Job Title'}</div>
                        <div class="resume-item-date">${formatDate(exp.startDate)} - ${exp.endDate === 'Present' ? 'Present' : formatDate(exp.endDate)}</div>
                    </div>
                    <div class="resume-item-subtitle">${escapeHtml(exp.company)}${exp.location ? ` • ${escapeHtml(exp.location)}` : ''}</div>
                    ${exp.achievements && exp.achievements.length > 0 && exp.achievements[0] ? `
                        <ul class="resume-item-achievements">
                            ${exp.achievements.filter(a => a.trim()).map(achievement => `<li>${escapeHtml(achievement)}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        }
    });
    
    return html + `</div>`;
}

function generateEducationSection() {
    if (resumeData.education.length === 0 || !resumeData.education.some(e => e.school)) {
        return '';
    }
    
    let html = `<div class="resume-section">
        <div class="resume-section-title" style="color: #1e293b; border-bottom-color: #e2e8f0;">Education</div>`;
    
    resumeData.education.forEach(edu => {
        if (edu.school) {
            html += `
                <div class="resume-education-item">
                    <div class="resume-item-header">
                        <div class="resume-item-title">${escapeHtml(edu.degree)}${edu.major ? ` in ${escapeHtml(edu.major)}` : ''}</div>
                        <div class="resume-item-date">${formatDate(edu.graduation)}</div>
                    </div>
                    <div class="resume-item-subtitle">${escapeHtml(edu.school)}${edu.location ? ` • ${escapeHtml(edu.location)}` : ''}</div>
                    ${edu.gpa ? `<div style="font-size: 13px; color: #64748b; margin-top: 4px;">GPA: ${escapeHtml(edu.gpa)}</div>` : ''}
                </div>
            `;
        }
    });
    
    return html + `</div>`;
}

// Resume Analyzer
document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('resumeFile');
    
    if (uploadZone && fileInput) {
        uploadZone.addEventListener('click', () => fileInput.click());
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('drag-over');
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('drag-over');
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('drag-over');
            if (e.dataTransfer.files.length) {
                handleFileUpload(e.dataTransfer.files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }
});

async function handleFileUpload(file) {
    const resultsDiv = document.getElementById('analysisResults');
    resultsDiv.innerHTML = '<div style="text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i> Analyzing resume...</div>';
    resultsDiv.style.display = 'block';
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/resume/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            displayAnalysisResults(data);
        } else {
            resultsDiv.innerHTML = '<div style="color: #dc2626;">Failed to analyze resume. Please try again.</div>';
        }
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = '<div style="color: #dc2626;">An error occurred. Please try again.</div>';
    }
}

function displayAnalysisResults(data) {
    const resultsDiv = document.getElementById('analysisResults');
    const score = data.score || 75;
    
    let html = `
        <div class="analysis-score">
            <div class="score-circle">${score}</div>
            <div style="font-size: 14px; color: #64748b;">Overall Score</div>
        </div>
    `;
    
    if (data.strengths && data.strengths.length > 0) {
        html += `
            <div class="analysis-section">
                <h4><i class="fas fa-check-circle" style="color: #10b981;"></i> Strengths</h4>
                ${data.strengths.map(s => `<div class="analysis-item">${escapeHtml(s)}</div>`).join('')}
            </div>
        `;
    }
    
    if (data.improvements && data.improvements.length > 0) {
        html += `
            <div class="analysis-section">
                <h4><i class="fas fa-exclamation-circle" style="color: #f59e0b;"></i> Areas for Improvement</h4>
                ${data.improvements.map(i => `<div class="analysis-item">${escapeHtml(i)}</div>`).join('')}
            </div>
        `;
    }
    
    resultsDiv.innerHTML = html;
}

async function downloadPDF() {
    const btn = document.getElementById('downloadBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    btn.disabled = true;

    try {
        const response = await fetch('/resume/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resumeData)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${resumeData.name || 'resume'}_resume.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            alert('Failed to generate PDF. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while generating the PDF.');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}
