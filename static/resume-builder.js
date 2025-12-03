// Resume Builder Enhanced JavaScript
function resumeBuilderApp() {
  return {
    activeTab: 'build',
    selectedTemplate: 'professional',
    templates: [],
    
    // Form data with comprehensive fields
    formData: {
      // Personal Information
      name: '',
      title: '',
      email: '',
      phone: '',
      location: '',
      linkedin: '',
      portfolio: '',
      github: '',
      
      // Professional Summary
      summary: '',
      
      // Skills
      skills: [],
      skillInput: '',
      
      // Experiences (array of objects)
      experiences: [
        {
          company: '',
          title: '',
          location: '',
          start_date: '',
          end_date: '',
          achievements: ['']
        }
      ],
      
      // Education (array of objects)
      education: [
        {
          degree: '',
          major: '',
          school: '',
          location: '',
          graduation: '',
          gpa: '',
          honors: ''
        }
      ],
      
      // Certifications
      certifications: [],
      certInput: { name: '', issuer: '', year: '' },
      
      // Projects
      projects: [],
      projectInput: { name: '', technologies: '', description: '', link: '' },
      
      // Technical Skills (for technical template)
      technical_skills: {
        'Languages': '',
        'Frameworks': '',
        'Tools': '',
        'Databases': ''
      },
      
      // Template selection
      template: 'professional'
    },
    
    // Analysis data
    selectedFile: null,
    dragOver: false,
    analyzing: false,
    results: null,
    
    // Generation
    generating: false,
    generatedResume: null,
    
    init() {
      this.loadTemplates();
    },
    
    async loadTemplates() {
      try {
        const response = await fetch('/api/resume/templates');
        const data = await response.json();
        if (data.success) {
          this.templates = data.templates;
        }
      } catch (error) {
        console.error('Failed to load templates:', error);
      }
    },
    
    // Skills management
    addSkill() {
      if (this.formData.skillInput.trim()) {
        this.formData.skills.push(this.formData.skillInput.trim());
        this.formData.skillInput = '';
      }
    },
    
    removeSkill(index) {
      this.formData.skills.splice(index, 1);
    },
    
    // Experience management
    addExperience() {
      this.formData.experiences.push({
        company: '',
        title: '',
        location: '',
        start_date: '',
        end_date: '',
        achievements: ['']
      });
    },
    
    removeExperience(index) {
      if (this.formData.experiences.length > 1) {
        this.formData.experiences.splice(index, 1);
      }
    },
    
    addAchievement(expIndex) {
      this.formData.experiences[expIndex].achievements.push('');
    },
    
    removeAchievement(expIndex, achIndex) {
      if (this.formData.experiences[expIndex].achievements.length > 1) {
        this.formData.experiences[expIndex].achievements.splice(achIndex, 1);
      }
    },
    
    // Education management
    addEducation() {
      this.formData.education.push({
        degree: '',
        major: '',
        school: '',
        location: '',
        graduation: '',
        gpa: '',
        honors: ''
      });
    },
    
    removeEducation(index) {
      if (this.formData.education.length > 1) {
        this.formData.education.splice(index, 1);
      }
    },
    
    // Certification management
    addCertification() {
      if (this.formData.certInput.name && this.formData.certInput.issuer) {
        this.formData.certifications.push({...this.formData.certInput});
        this.formData.certInput = { name: '', issuer: '', year: '' };
      }
    },
    
    removeCertification(index) {
      this.formData.certifications.splice(index, 1);
    },
    
    // Project management
    addProject() {
      if (this.formData.projectInput.name) {
        this.formData.projects.push({...this.formData.projectInput});
        this.formData.projectInput = { name: '', technologies: '', description: '', link: '' };
      }
    },
    
    removeProject(index) {
      this.formData.projects.splice(index, 1);
    },
    
    // File upload for analysis
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file && file.size <= 5 * 1024 * 1024) {
        this.selectedFile = file;
      } else {
        alert('File too large. Max 5MB.');
      }
    },
    
    handleDrop(event) {
      this.dragOver = false;
      const file = event.dataTransfer.files[0];
      if (file && file.size <= 5 * 1024 * 1024) {
        this.selectedFile = file;
      }
    },
    
    formatFileSize(bytes) {
      if (!bytes) return '';
      return (bytes / 1024).toFixed(1) + ' KB';
    },
    
    // Analyze resume
    async analyzeResume() {
      if (!this.selectedFile) return;
      
      this.analyzing = true;
      this.results = null;
      
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      
      try {
        const response = await fetch('/api/resume/analyze', {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.results = data;
        } else {
          alert('Error: ' + (data.error || 'Analysis failed'));
        }
      } catch (error) {
        alert('Error analyzing resume: ' + error.message);
      } finally {
        this.analyzing = false;
      }
    },
    
    // Generate resume
    async generateResume() {
      this.generating = true;
      this.generatedResume = null;
      
      // Prepare data
      const data = {
        ...this.formData,
        template: this.selectedTemplate
      };
      
      try {
        const response = await fetch('/api/resume/generate', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
          this.generatedResume = result.resume;
          this.activeTab = 'preview';
        } else {
          alert('Error: ' + (result.error || 'Generation failed'));
        }
      } catch (error) {
        alert('Error generating resume: ' + error.message);
      } finally {
        this.generating = false;
      }
    },
    
    // Download resume
    downloadResume() {
      const blob = new Blob([this.generatedResume], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resume_' + this.formData.name.replace(/\s+/g, '_') + '.txt';
      a.click();
      URL.revokeObjectURL(url);
    },
    
    // Select template
    selectTemplate(templateId) {
      this.selectedTemplate = templateId;
      this.formData.template = templateId;
    },
    
    // Feedback icon helper
    getFeedbackIcon(type) {
      const icons = {
        'critical': '🔴',
        'warning': '⚠️',
        'info': 'ℹ️',
        'success': '✅'
      };
      return icons[type] || 'ℹ️';
    },
    
    // Auto-save to localStorage
    saveProgress() {
      localStorage.setItem('resumeBuilderData', JSON.stringify(this.formData));
    },
    
    loadProgress() {
      const saved = localStorage.getItem('resumeBuilderData');
      if (saved) {
        try {
          this.formData = JSON.parse(saved);
        } catch (e) {
          console.error('Failed to load saved data');
        }
      }
    },
    
    clearForm() {
      if (confirm('Are you sure you want to clear all data?')) {
        localStorage.removeItem('resumeBuilderData');
        location.reload();
      }
    }
  };
}
