"""
Intelligent Category-Specific Question Generator
Generates relevant interview questions for each category using AI
"""

import os
import json
import asyncio
from typing import List, Dict, Optional
from functools import lru_cache

# Category-specific prompts and keywords
CATEGORY_CONTEXTS = {
    "Python": {
        "description": "Python programming language",
        "topics": [
            "decorators", "generators", "list comprehensions", "OOP", "inheritance",
            "lambda functions", "context managers", "metaclasses", "async/await",
            "data structures", "file handling", "exception handling", "modules",
            "pip", "virtual environments", "testing", "debugging"
        ],
        "difficulty_levels": {
            "easy": "basic syntax, data types, control flow",
            "medium": "functions, classes, modules, file I/O",
            "hard": "decorators, generators, metaclasses, async programming"
        }
    },
    "Web Development": {
        "description": "Web development technologies and concepts",
        "topics": [
            "HTML", "CSS", "JavaScript", "React", "Vue", "Angular",
            "REST API", "GraphQL", "HTTP methods", "authentication",
            "frontend", "backend", "databases", "deployment", "security",
            "responsive design", "accessibility", "performance optimization"
        ],
        "difficulty_levels": {
            "easy": "HTML basics, CSS styling, JavaScript fundamentals",
            "medium": "frameworks, APIs, databases, authentication",
            "hard": "architecture, scalability, security, performance"
        }
    },
    "Data Structures": {
        "description": "Data structures and algorithms",
        "topics": [
            "arrays", "linked lists", "stacks", "queues", "trees", "graphs",
            "hash tables", "heaps", "sorting", "searching", "Big O notation",
            "recursion", "dynamic programming", "greedy algorithms",
            "binary search", "DFS", "BFS", "time complexity", "space complexity"
        ],
        "difficulty_levels": {
            "easy": "arrays, linked lists, basic sorting",
            "medium": "trees, graphs, hash tables, recursion",
            "hard": "dynamic programming, advanced algorithms, optimization"
        }
    },
    "HR / Behavioral": {
        "description": "Behavioral and HR interview questions",
        "topics": [
            "tell me about yourself", "strengths", "weaknesses", "teamwork",
            "conflict resolution", "leadership", "failure", "success",
            "motivation", "career goals", "work style", "communication",
            "problem solving", "time management", "adaptability"
        ],
        "difficulty_levels": {
            "easy": "basic background, interests, goals",
            "medium": "specific experiences, challenges, achievements",
            "hard": "complex situations, ethical dilemmas, leadership"
        }
    },
    "System Design": {
        "description": "System design and architecture",
        "topics": [
            "scalability", "load balancing", "caching", "databases",
            "microservices", "API design", "distributed systems",
            "message queues", "CDN", "sharding", "replication",
            "consistency", "availability", "partition tolerance",
            "monitoring", "logging", "security", "performance"
        ],
        "difficulty_levels": {
            "easy": "basic concepts, simple systems",
            "medium": "scalable systems, databases, caching",
            "hard": "distributed systems, trade-offs, complex architectures"
        }
    },
    "AI / ML": {
        "description": "Artificial Intelligence and Machine Learning",
        "topics": [
            "supervised learning", "unsupervised learning", "reinforcement learning",
            "neural networks", "deep learning", "CNN", "RNN", "transformers",
            "overfitting", "underfitting", "regularization", "cross-validation",
            "feature engineering", "model evaluation", "classification", "regression",
            "clustering", "dimensionality reduction", "NLP", "computer vision"
        ],
        "difficulty_levels": {
            "easy": "basic concepts, supervised vs unsupervised",
            "medium": "algorithms, model evaluation, feature engineering",
            "hard": "deep learning, advanced techniques, optimization"
        }
    },
    "JavaScript": {
        "description": "JavaScript programming",
        "topics": [
            "closures", "promises", "async/await", "callbacks", "event loop",
            "prototypes", "ES6+", "arrow functions", "destructuring",
            "spread operator", "modules", "DOM manipulation", "AJAX",
            "fetch API", "error handling", "testing", "frameworks"
        ],
        "difficulty_levels": {
            "easy": "variables, functions, arrays, objects",
            "medium": "closures, promises, async, DOM",
            "hard": "event loop, prototypes, advanced patterns"
        }
    },
    "Database": {
        "description": "Database systems and SQL",
        "topics": [
            "SQL", "NoSQL", "joins", "indexes", "normalization",
            "transactions", "ACID", "queries", "optimization",
            "MongoDB", "PostgreSQL", "MySQL", "Redis",
            "data modeling", "relationships", "constraints"
        ],
        "difficulty_levels": {
            "easy": "basic queries, SELECT, WHERE, ORDER BY",
            "medium": "joins, indexes, transactions, normalization",
            "hard": "optimization, complex queries, distributed databases"
        }
    },
    "DevOps": {
        "description": "DevOps and deployment",
        "topics": [
            "CI/CD", "Docker", "Kubernetes", "Git", "Jenkins",
            "deployment", "monitoring", "logging", "automation",
            "infrastructure as code", "cloud platforms", "AWS", "Azure",
            "testing", "security", "scalability"
        ],
        "difficulty_levels": {
            "easy": "Git basics, deployment concepts",
            "medium": "Docker, CI/CD, cloud platforms",
            "hard": "Kubernetes, infrastructure automation, scaling"
        }
    },
    "React": {
        "description": "React framework",
        "topics": [
            "components", "props", "state", "hooks", "useEffect",
            "useState", "context", "Redux", "routing", "lifecycle",
            "virtual DOM", "JSX", "forms", "events", "performance",
            "testing", "best practices"
        ],
        "difficulty_levels": {
            "easy": "components, props, state basics",
            "medium": "hooks, context, routing, forms",
            "hard": "performance optimization, advanced patterns, testing"
        }
    }
}


def get_category_context(category: str) -> Dict:
    """Get context for a category, with fallback to generic"""
    return CATEGORY_CONTEXTS.get(category, {
        "description": f"{category} interview questions",
        "topics": ["concepts", "best practices", "common patterns"],
        "difficulty_levels": {
            "easy": "basic concepts",
            "medium": "intermediate topics",
            "hard": "advanced topics"
        }
    })


async def generate_category_questions_with_openai(
    category: str,
    count: int = 10,
    difficulty: str = "medium",
    company: str = None
) -> List[str]:
    """
    Generate category-specific questions using OpenAI
    Supports company-specific question generation
    """
    try:
        from llm_utils import call_llm_chat
    except ImportError:
        return []
    
    context = get_category_context(category)
    topics = ", ".join(context["topics"][:10])  # Top 10 topics
    difficulty_desc = context["difficulty_levels"].get(difficulty, "medium level")
    
    # Build company-specific prompt
    if company:
        system_prompt = f"""You are a senior interviewer at {company} specializing in {context['description']}.
You know {company}'s interview style, culture, and technical focus areas intimately.
Generate questions that reflect {company}'s actual interview process and values."""
        
        # Company-specific examples and focus areas
        company_examples = {
            "Google": "Focus on scalability, distributed systems, and algorithmic thinking. Example: 'How would you design YouTube's recommendation system?'",
            "Amazon": "Focus on AWS services, scalability, and e-commerce systems. For behavioral: Leadership Principles. Example: 'How would you design Amazon's recommendation engine using AWS?'",
            "Microsoft": "Focus on Azure, enterprise solutions, and collaborative development. Example: 'How would you architect a cloud-based collaboration tool?'",
            "Meta": "Emphasize social impact, scale, and user engagement. Example: 'Design a news feed ranking algorithm for billions of users.'",
            "Apple": "Focus on user experience, design thinking, and performance. Example: 'How would you optimize iOS app performance?'",
            "Netflix": "Emphasize streaming technology, personalization, and scale. Example: 'Design a video streaming service for millions of concurrent users.'",
            "Tesla": "Focus on automation, real-time systems, and innovation. Example: 'How would you design an autonomous driving decision system?'",
            "Uber": "Emphasize real-time systems, geolocation, and marketplace dynamics. Example: 'Design a surge pricing algorithm.'",
            "Airbnb": "Focus on trust, community, and marketplace design. Example: 'How would you build a review and rating system?'",
            "Goldman Sachs": "Emphasize financial systems, risk management, and trading. Example: 'Design a high-frequency trading system.'",
            "JP Morgan": "Focus on banking systems, security, and compliance. Example: 'How would you secure a payment processing system?'",
            "McKinsey": "Emphasize case studies, business strategy, and problem-solving. Example: 'How would you help a retail client increase profitability?'",
        }
        
        company_focus = company_examples.get(company, f"Focus on {company}'s core business and technical challenges.")
        
        user_prompt = f"""Generate {count} {difficulty} difficulty {category} interview questions specifically for {company}.

CRITICAL REQUIREMENTS:
1. Questions MUST be about {category} topics (NOT behavioral unless category is HR/Behavioral)
2. Questions MUST mention {company} or its products/services
3. Questions MUST cover these topics: {topics}

{company_focus}

Category: {category}
Topics to cover: {topics}
Difficulty: {difficulty_desc}

Question Requirements:
1. Focus on {category} technical content
2. EXPLICITLY mention {company} or its products/services
3. Reflect {company}'s interview style
4. Use real {company} scenarios related to {category}
5. Questions should be 80-150 characters
6. Test {category} knowledge in {company} context

Examples of good {company} + {category} questions:
- "How would you use {category} to solve [problem] at {company}?"
- "Explain how {company} uses {category} in [product/service]"
- "Write {category} code to implement [feature] for {company}"

Return ONLY a JSON array of question strings.
Format: ["Question 1?", "Question 2?", ...]"""
    else:
        # Generic questions (no company specified)
        system_prompt = f"""You are an expert technical interviewer specializing in {context['description']}.
Generate diverse, relevant interview questions that test real understanding."""
        
        user_prompt = f"""Generate {count} distinct {difficulty} difficulty interview questions for {category}.

Topics to cover: {topics}
Difficulty level: {difficulty_desc}

Requirements:
1. Each question should be clear and concise (under 120 characters)
2. Questions should test understanding, not just memorization
3. Cover different aspects of {category}
4. Make questions practical and relevant to real interviews
5. Vary the question types (explain, compare, implement, debug, etc.)

Return ONLY a JSON array of question strings, nothing else.
Example format: ["Question 1?", "Question 2?", ...]"""
    
    try:
        response = await call_llm_chat(system_prompt, user_prompt, max_tokens=800)
        
        # Parse JSON response
        questions = json.loads(response)
        
        if isinstance(questions, list):
            # Clean and validate questions
            valid_questions = []
            for q in questions:
                q_str = str(q).strip()
                if len(q_str) > 10 and len(q_str) < 200:
                    # Ensure it ends with a question mark
                    if not q_str.endswith('?'):
                        q_str += '?'
                    valid_questions.append(q_str)
            
            return valid_questions[:count]
        
    except json.JSONDecodeError:
        # Try to extract questions from text
        lines = response.split('\n')
        questions = []
        for line in lines:
            line = line.strip().strip('-•*"\'[]')
            if line and len(line) > 10 and ('?' in line or 'what' in line.lower() or 'how' in line.lower() or 'explain' in line.lower()):
                if not line.endswith('?'):
                    line += '?'
                questions.append(line)
        
        return questions[:count]
    
    except Exception as e:
        print(f"OpenAI question generation failed: {e}")
        return []


def generate_category_questions_with_hf(
    category: str,
    count: int = 10,
    difficulty: str = "medium"
) -> List[str]:
    """
    Generate category-specific questions using HuggingFace
    """
    try:
        from huggingface_utils import generate_question_local
    except ImportError:
        return []
    
    context = get_category_context(category)
    questions = []
    
    # Generate questions with category context
    for i in range(count):
        try:
            # Pick a random topic from the category
            import random
            topic = random.choice(context["topics"]) if context["topics"] else category
            
            # Generate question
            question = generate_question_local(f"{category} - {topic}", difficulty)
            
            if question and len(question) > 10:
                questions.append(question)
        except Exception as e:
            print(f"HF question generation failed for {category}: {e}")
            continue
    
    return questions


def generate_template_questions(category: str, count: int = 10) -> List[str]:
    """
    Generate questions using templates (fallback method)
    """
    context = get_category_context(category)
    topics = context["topics"]
    
    templates = [
        "What is {topic} in {category}?",
        "Explain {topic} and how it works.",
        "What are the key features of {topic}?",
        "How would you implement {topic}?",
        "What are the advantages of {topic}?",
        "Compare {topic} with alternatives.",
        "When would you use {topic}?",
        "What are common pitfalls with {topic}?",
        "How does {topic} improve performance?",
        "Explain the concept of {topic} with an example."
    ]
    
    questions = []
    import random
    
    for i in range(count):
        template = random.choice(templates)
        topic = random.choice(topics) if topics else category
        
        question = template.format(topic=topic, category=category)
        questions.append(question)
    
    return questions


async def generate_smart_questions(
    category: str,
    count: int = 10,
    difficulty: str = "medium",
    use_openai: bool = True,
    company: str = None
) -> List[Dict[str, str]]:
    """
    Smart question generation with multiple fallbacks
    Supports company-specific question generation
    Returns list of dicts with id and prompt
    """
    questions = []
    
    # Method 1: Try OpenAI (best quality)
    if use_openai and os.getenv("OPENAI_API_KEY"):
        try:
            openai_questions = await generate_category_questions_with_openai(
                category, count, difficulty, company
            )
            if openai_questions:
                questions = [
                    {"id": f"ai-{i+1}", "prompt": q, "source": "openai"}
                    for i, q in enumerate(openai_questions)
                ]
                print(f"✅ Generated {len(questions)} questions for {category} using OpenAI")
                return questions
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
    
    # Method 2: Try HuggingFace (good quality, free)
    try:
        hf_questions = generate_category_questions_with_hf(category, count, difficulty)
        if hf_questions:
            questions = [
                {"id": f"hf-{i+1}", "prompt": q, "source": "huggingface"}
                for i, q in enumerate(hf_questions)
            ]
            print(f"✅ Generated {len(questions)} questions for {category} using HuggingFace")
            return questions
    except Exception as e:
        print(f"HuggingFace generation failed: {e}")
    
    # Method 3: Template-based (always works)
    template_questions = generate_template_questions(category, count)
    questions = [
        {"id": f"template-{i+1}", "prompt": q, "source": "template"}
        for i, q in enumerate(template_questions)
    ]
    print(f"✅ Generated {len(questions)} questions for {category} using templates")
    
    return questions


# Test function
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("Testing Category-Specific Question Generation\n")
        
        categories = ["Python", "Web Development", "Data Structures", "AI / ML"]
        
        for category in categories:
            print(f"\n{'='*60}")
            print(f"Category: {category}")
            print(f"{'='*60}")
            
            questions = await generate_smart_questions(category, count=5, use_openai=True)
            
            for i, q in enumerate(questions, 1):
                print(f"{i}. {q['prompt']}")
                print(f"   Source: {q['source']}")
    
    asyncio.run(test())
