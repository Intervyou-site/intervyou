// Professional Resume Templates Data
const RESUME_TEMPLATES = {
    professional: {
        name: 'Professional',
        description: 'Clean and traditional layout perfect for corporate roles',
        colors: {
            primary: '#2563eb',
            secondary: '#1e293b',
            accent: '#64748b',
            background: '#ffffff'
        },
        fonts: {
            heading: "'Georgia', serif",
            body: "'Inter', sans-serif"
        },
        layout: 'single-column',
        sections: ['header', 'summary', 'experience', 'education', 'skills']
    },
    
    modern: {
        name: 'Modern',
        description: 'Two-column design with colored sidebar for tech professionals',
        colors: {
            primary: '#2563eb',
            secondary: '#ffffff',
            accent: '#f8fafc',
            sidebar: '#2563eb'
        },
        fonts: {
            heading: "'Inter', sans-serif",
            body: "'Inter', sans-serif"
        },
        layout: 'two-column',
        sections: ['sidebar', 'main']
    },
    
    executive: {
        name: 'Executive',
        description: 'Sophisticated design for senior-level positions',
        colors: {
            primary: '#1e293b',
            secondary: '#475569',
            accent: '#cbd5e1',
            background: '#ffffff'
        },
        fonts: {
            heading: "'Playfair Display', serif",
            body: "'Inter', sans-serif"
        },
        layout: 'single-column',
        sections: ['header', 'summary', 'experience', 'education', 'skills']
    },
    
    creative: {
        name: 'Creative',
        description: 'Eye-catching gradient design for creative industries',
        colors: {
            primary: '#f093fb',
            secondary: '#f5576c',
            accent: '#ffffff',
            gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
        },
        fonts: {
            heading: "'Poppins', sans-serif",
            body: "'Inter', sans-serif"
        },
        layout: 'single-column',
        sections: ['header', 'summary', 'experience', 'education', 'skills']
    },
    
    minimal: {
        name: 'Minimal',
        description: 'Simple and elegant with focus on content',
        colors: {
            primary: '#1e293b',
            secondary: '#64748b',
            accent: '#e2e8f0',
            background: '#ffffff'
        },
        fonts: {
            heading: "'Inter', sans-serif",
            body: "'Inter', sans-serif"
        },
        layout: 'single-column',
        sections: ['header', 'summary', 'experience', 'education', 'skills']
    },
    
    bold: {
        name: 'Bold',
        description: 'Strong visual impact with dark header sections',
        colors: {
            primary: '#1e293b',
            secondary: '#ffffff',
            accent: '#475569',
            background: '#ffffff'
        },
        fonts: {
            heading: "'Montserrat', sans-serif",
            body: "'Inter', sans-serif"
        },
        layout: 'single-column',
        sections: ['header', 'summary', 'experience', 'education', 'skills']
    },
    
    elegant: {
        name: 'Elegant',
        description: 'Refined serif typography for traditional industries',
        colors: {
            primary: '#6b7280',
            secondary: '#1f2937',
            accent: '#d1d5db',
            background: '#ffffff'
        },
        fonts: {
            heading: "'Merriweather', serif",
            body: "'Lato', sans-serif"
        },
        layout: 'single-column',
        sections: ['header', 'summary', 'experience', 'education', 'skills']
    },
    
    tech: {
        name: 'Tech',
        description: 'Modern tech-focused design with code-like aesthetics',
        colors: {
            primary: '#10b981',
            secondary: '#1e293b',
            accent: '#6ee7b7',
            background: '#ffffff'
        },
        fonts: {
            heading: "'Roboto Mono', monospace",
            body: "'Inter', sans-serif"
        },
        layout: 'two-column',
        sections: ['sidebar', 'main']
    }
};
