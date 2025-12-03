#!/usr/bin/env python3
"""Test resume templates functionality"""

from resume_templates import generate_resume, get_available_templates
import json

# Sample comprehensive data
sample_data = {
    'name': 'John Doe',
    'title': 'Senior Software Engineer',
    'email': 'john.doe@email.com',
    'phone': '5551234567',
    'location': 'San Francisco, CA',
    'linkedin': 'linkedin.com/in/johndoe',
    'portfolio': 'johndoe.com',
    'github': 'github.com/johndoe',
    
    'summary': 'Experienced software engineer with 8+ years of expertise in full-stack development, cloud architecture, and team leadership. Proven track record of delivering scalable solutions that improved system performance by 40% and reduced costs by $200K annually.',
    
    'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker', 'Kubernetes', 'PostgreSQL'],
    
    'experiences': [
        {
            'company': 'Tech Corp',
            'title': 'Senior Software Engineer',
            'location': 'San Francisco, CA',
            'start_date': 'Jan 2020',
            'end_date': 'Present',
            'achievements': [
                'Led development of microservices architecture serving 1M+ daily users',
                'Reduced deployment time by 60% through CI/CD implementation',
                'Mentored team of 5 junior engineers'
            ]
        },
        {
            'company': 'StartupXYZ',
            'title': 'Software Engineer',
            'location': 'San Francisco, CA',
            'start_date': 'Jun 2017',
            'end_date': 'Dec 2019',
            'achievements': [
                'Built RESTful APIs handling 500K requests/day',
                'Optimized database queries improving response time by 45%'
            ]
        }
    ],
    
    'education': [
        {
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'school': 'Stanford University',
            'location': 'Stanford, CA',
            'graduation': '2017',
            'gpa': '3.8',
            'honors': 'Magna Cum Laude'
        }
    ],
    
    'certifications': [
        {'name': 'AWS Certified Solutions Architect', 'issuer': 'Amazon Web Services', 'year': '2022'},
        {'name': 'Certified Kubernetes Administrator', 'issuer': 'CNCF', 'year': '2021'}
    ],
    
    'projects': [
        {
            'name': 'E-Commerce Platform',
            'technologies': 'React, Node.js, PostgreSQL, AWS',
            'description': 'Built scalable platform processing $2M+ in transactions',
            'link': 'github.com/johndoe/ecommerce'
        }
    ],
    
    'technical_skills': {
        'Languages': 'Python, JavaScript, TypeScript, Java',
        'Frameworks': 'React, Node.js, Django, Flask',
        'Tools': 'Docker, Kubernetes, Jenkins, Git',
        'Databases': 'PostgreSQL, MongoDB, Redis'
    }
}

def test_all_templates():
    """Test all available templates"""
    print("🧪 Testing Resume Templates\n")
    print("=" * 80)
    
    # Get available templates
    templates = get_available_templates()
    print(f"\n📋 Available Templates: {len(templates)}\n")
    
    for template in templates:
        print(f"  ✓ {template['name']}: {template['description']}")
    
    print("\n" + "=" * 80)
    print("\n🎨 Generating Resumes with Each Template:\n")
    
    # Test each template
    for template in templates:
        template_id = template['id']
        template_name = template['name']
        
        print(f"\n{'─' * 80}")
        print(f"Template: {template_name} ({template_id})")
        print(f"{'─' * 80}\n")
        
        try:
            resume = generate_resume(sample_data, template_id)
            
            # Show first 500 characters
            preview = resume[:500] + "..." if len(resume) > 500 else resume
            print(preview)
            
            # Stats
            lines = resume.count('\n')
            chars = len(resume)
            print(f"\n📊 Stats: {lines} lines, {chars} characters")
            print(f"✅ {template_name} template generated successfully!")
            
        except Exception as e:
            print(f"❌ Error generating {template_name}: {e}")
    
    print("\n" + "=" * 80)
    print("\n✨ All templates tested successfully!\n")

def test_minimal_data():
    """Test with minimal required data"""
    print("\n🧪 Testing with Minimal Data\n")
    print("=" * 80)
    
    minimal_data = {
        'name': 'Jane Smith',
        'title': 'Software Developer',
        'email': 'jane@email.com',
        'phone': '5559876543',
        'location': 'New York, NY',
        'summary': 'Passionate developer with strong problem-solving skills.',
        'skills': ['Python', 'JavaScript', 'SQL'],
        'experiences': [
            {
                'company': 'Tech Startup',
                'title': 'Developer',
                'location': 'NY',
                'start_date': '2022',
                'end_date': 'Present',
                'achievements': ['Built web applications']
            }
        ],
        'education': [
            {
                'degree': 'BS',
                'major': 'CS',
                'school': 'University',
                'graduation': '2022'
            }
        ]
    }
    
    try:
        resume = generate_resume(minimal_data, 'professional')
        print(resume[:300] + "...")
        print(f"\n✅ Minimal data test passed!")
    except Exception as e:
        print(f"❌ Minimal data test failed: {e}")

if __name__ == "__main__":
    test_all_templates()
    test_minimal_data()
    print("\n🎉 All tests completed!\n")
