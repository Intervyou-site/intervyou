// Enhanced Resume Builder with Live Preview
document.addEventListener('DOMContentLoaded', function() {
    // Initialize resume data
    const resumeData = {
        personal: {
            name: '',
            title: '',
            email: '',
            phone: '',
            linkedin: '',
            location: ''
        },
        summary: '',
        experience: [],
        education: [],
        skills: [],
        template: 'modern_blue'
    };
    
    // Get all form inputs
    const inputs = document.querySelectorAll('input, textarea, select');
    
    // Add event listeners to all inputs for live preview
    inputs.forEach(input => {
        input.addEventListener('input', updatePreview);
        input.addEventListener('change', updatePreview);
    });
    
    // Update preview function
    function updatePreview() {
        // Get personal information
        resumeData.personal.name = document.querySelector('input[name="name"]')?.value || 'INTERVYOU';
        resumeData.personal.title = document.querySelector('input[name="title"]')?.value || 'PROFESSIONAL TITLE';
        resumeData.personal.email = document.querySelector('input[name="email"]')?.value || '';
        resumeData.personal.phone = document.querySelector('input[name="phone"]')?.value || '';
        resumeData.personal.linkedin = document.querySelector('input[name="linkedin"]')?.value || '';
        
        // Get summary
        resumeData.summary = document.querySelector('textarea[name="summary"]')?.value || '';
        
        // Get skills
        const skillsInput = document.querySelector('textarea[name="skills"]')?.value || '';
        resumeData.skills = skillsInput.split(',').map(s => s.trim()).filter(s => s);
        
        // Generate HTML preview
        generatePreviewHTML();
    }
    
    // Generate preview HTML
    function generatePreviewHTML() {
        const previewContainer = document.getElementById('resumePreview');
        if (!previewContainer) return;
        
        const template = resumeData.template;
        
        if (template === 'modern_blue' || template === 'modern') {
            previewContainer.innerHTML = generateModernTemplate();
        } else if (template === 'classic') {
            previewContainer.innerHTML = generateClassicTemplate();
        } else if (template === 'creative_dark') {
            previewContainer.innerHTML = generateCreativeTemplate();
        } else if (template === 'clean_minimal') {
            previewContainer.innerHTML = generateMinimalTemplate();
        } else if (template === 'purple_accent') {
            previewContainer.innerHTML = generatePurpleTemplate();
        } else {
            previewContainer.innerHTML = generateModernTemplate();
        }
    }
    
    // Modern template with sidebar
    function generateModernTemplate() {
        return `
            <div style="display: grid; grid-template-columns: 40% 60%; min-height: 100%; background: white;">
                <!-- Left Sidebar -->
                <div style="background: #2563eb; color: white; padding: 40px 35px;">
                    <div style="margin-bottom: 40px;">
                        <h1 style="font-size: 28px; font-weight: 700; margin: 0 0 8px 0; color: white;">${resumeData.personal.name || 'YOUR NAME'}</h1>
                        <p style="font-size: 16px; margin: 0; opacity: 0.9; color: white;">${resumeData.personal.title || 'Professional Title'}</p>
                    </div>
                    
                    ${resumeData.personal.email || resumeData.personal.phone || resumeData.personal.linkedin ? `
                    <div style="margin-bottom: 40px;">
                        <h3 style="font-size: 16px; font-weight: 600; margin: 0 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(255,255,255,0.3); color: white;">CONTACT</h3>
                        ${resumeData.personal.phone ? `<p style="font-size: 13px; margin: 0 0 8px 0; color: white;">${resumeData.personal.phone}</p>` : ''}
                        ${resumeData.personal.email ? `<p style="font-size: 13px; margin: 0 0 8px 0; word-break: break-all; color: white;">${resumeData.personal.email}</p>` : ''}
                        ${resumeData.personal.linkedin ? `<p style="font-size: 13px; margin: 0; color: white;">${resumeData.personal.linkedin}</p>` : ''}
                    </div>
                    ` : ''}
                    
                    ${resumeData.skills.length > 0 ? `
                    <div>
                        <h3 style="font-size: 16px; font-weight: 600; margin: 0 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid rgba(255,255,255,0.3); color: white;">SKILLS</h3>
                        ${resumeData.skills.map(skill => `<p style="font-size: 13px; margin: 0 0 8px 0; color: white;">• ${skill}</p>`).join('')}
                    </div>
                    ` : ''}
                </div>
                
                <!-- Right Main Content -->
                <div style="padding: 40px;">
                    ${resumeData.summary ? `
                    <div style="margin-bottom: 32px;">
                        <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; color: #1e293b;">SUMMARY</h3>
                        <p style="font-size: 14px; line-height: 1.6; margin: 0; color: #475569;">${resumeData.summary}</p>
                    </div>
                    ` : ''}
                    
                    <div style="margin-bottom: 32px;">
                        <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; color: #1e293b;">EXPERIENCE</h3>
                        <p style="font-size: 13px; color: #94a3b8; font-style: italic;">Add your experience details in the form</p>
                    </div>
                    
                    <div>
                        <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; color: #1e293b;">EDUCATION</h3>
                        <p style="font-size: 13px; color: #94a3b8; font-style: italic;">Add your education details in the form</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Classic template
    function generateClassicTemplate() {
        return `
            <div style="padding: 40px; background: white;">
                <div style="text-align: center; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 2px solid #1e293b;">
                    <h1 style="font-size: 32px; font-weight: 700; margin: 0 0 8px 0; color: #1e293b;">${resumeData.personal.name || 'YOUR NAME'}</h1>
                    <p style="font-size: 18px; margin: 0 0 16px 0; color: #2563eb;">${resumeData.personal.title || 'Professional Title'}</p>
                    <div style="font-size: 13px; color: #64748b;">
                        ${resumeData.personal.email ? `${resumeData.personal.email}` : ''}
                        ${resumeData.personal.phone ? ` | ${resumeData.personal.phone}` : ''}
                        ${resumeData.personal.linkedin ? ` | ${resumeData.personal.linkedin}` : ''}
                    </div>
                </div>
                
                ${resumeData.summary ? `
                <div style="margin-bottom: 32px;">
                    <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; color: #1e293b;">PROFESSIONAL SUMMARY</h3>
                    <p style="font-size: 14px; line-height: 1.6; margin: 0; color: #475569;">${resumeData.summary}</p>
                </div>
                ` : ''}
                
                ${resumeData.skills.length > 0 ? `
                <div style="margin-bottom: 32px;">
                    <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; color: #1e293b;">SKILLS</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                        ${resumeData.skills.map(skill => `<span style="background: #eff6ff; color: #2563eb; padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: 500;">${skill}</span>`).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;
    }
    
    // Creative template
    function generateCreativeTemplate() {
        return `
            <div style="background: linear-gradient(to bottom, #f093fb 0%, #f093fb 200px, white 200px); padding: 40px;">
                <div style="text-align: center; margin-bottom: 32px; color: white;">
                    <h1 style="font-size: 32px; font-weight: 700; margin: 0 0 8px 0; color: white;">${resumeData.personal.name || 'YOUR NAME'}</h1>
                    <p style="font-size: 18px; margin: 0 0 16px 0; color: white;">${resumeData.personal.title || 'Professional Title'}</p>
                    <div style="font-size: 13px; color: white;">
                        ${resumeData.personal.email ? `${resumeData.personal.email}` : ''}
                        ${resumeData.personal.phone ? ` | ${resumeData.personal.phone}` : ''}
                    </div>
                </div>
                
                ${resumeData.summary ? `
                <div style="margin-bottom: 32px; background: white; padding: 24px; border-radius: 8px;">
                    <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 12px 0; color: #1e293b;">SUMMARY</h3>
                    <p style="font-size: 14px; line-height: 1.6; margin: 0; color: #475569;">${resumeData.summary}</p>
                </div>
                ` : ''}
            </div>
        `;
    }
    
    // Minimal template
    function generateMinimalTemplate() {
        return `
            <div style="padding: 40px; background: white; border: 2px solid #e2e8f0;">
                <div style="margin-bottom: 32px;">
                    <h1 style="font-size: 28px; font-weight: 700; margin: 0 0 4px 0; color: #1e293b;">${resumeData.personal.name || 'YOUR NAME'}</h1>
                    <p style="font-size: 14px; margin: 0 0 12px 0; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">${resumeData.personal.title || 'Professional Title'}</p>
                    <div style="font-size: 12px; color: #94a3b8;">
                        ${resumeData.personal.email ? `${resumeData.personal.email}` : ''}
                        ${resumeData.personal.phone ? ` • ${resumeData.personal.phone}` : ''}
                    </div>
                </div>
                
                ${resumeData.summary ? `
                <div style="margin-bottom: 24px;">
                    <h3 style="font-size: 14px; font-weight: 600; margin: 0 0 8px 0; color: #1e293b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;">Summary</h3>
                    <p style="font-size: 13px; line-height: 1.6; margin: 0; color: #475569;">${resumeData.summary}</p>
                </div>
                ` : ''}
            </div>
        `;
    }
    
    // Purple template
    function generatePurpleTemplate() {
        return generateModernTemplate().replace(/#2563eb/g, '#8b5cf6');
    }
    
    // Template selection
    window.selectTemplate = function(templateId) {
        resumeData.template = templateId;
        
        // Update active state
        document.querySelectorAll('.template-card').forEach(card => {
            card.classList.remove('active');
        });
        document.querySelector(`[data-template="${templateId}"]`)?.classList.add('active');
        
        // Update preview
        updatePreview();
    };
    
    // Initial preview
    updatePreview();
    
    // Download PDF function
    window.downloadPDF = function() {
        alert('PDF download functionality will be implemented. For now, you can print this page (Ctrl+P) and save as PDF.');
        window.print();
    };
    
    // Analyze resume function
    window.analyzeResume = function() {
        alert('ATS analysis functionality will be implemented soon!');
    };
    
    // Import/Export functions
    window.importJSON = function() {
        alert('Import functionality will be implemented soon!');
    };
    
    window.exportJSON = function() {
        const dataStr = JSON.stringify(resumeData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'resume-data.json';
        link.click();
        URL.revokeObjectURL(url);
    };
    
    window.undoAction = function() {
        alert('Undo functionality will be implemented soon!');
    };
    
    window.redoAction = function() {
        alert('Redo functionality will be implemented soon!');
    };
    
    window.clearAll = function() {
        if (confirm('Are you sure you want to clear all data?')) {
            document.querySelectorAll('input, textarea').forEach(input => {
                input.value = '';
            });
            updatePreview();
        }
    };
    
    window.closeModal = function() {
        document.getElementById('jsonModal').classList.remove('show');
    };
    
    window.handlePDFUpload = function(event) {
        const file = event.target.files[0];
        if (file) {
            alert('PDF import functionality will be implemented soon!');
        }
    };
});
