"""
Answer Templates Library
Provides pre-written answer structures for common interview questions
"""
import logging
from typing import Dict, List, Optional
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class AnswerTemplatesLibrary:
    """Library of answer templates for common interview questions"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Load all answer templates"""
        return {
            # BEHAVIORAL QUESTIONS
            "tell_me_about_yourself": {
                "question": "Tell me about yourself",
                "category": "Behavioral",
                "structure": [
                    "Current Role (30 seconds)",
                    "Background & Experience (30 seconds)",
                    "Why This Opportunity (30 seconds)"
                ],
                "example": """I'm currently a Software Engineer at TechCorp, where I lead the development of customer-facing web applications using React and Node.js. I work with a team of 5 engineers and we've successfully launched 3 major features this year that increased user engagement by 40%.

I have 3 years of experience in full-stack development, with a strong focus on building scalable, user-friendly applications. I graduated with a Computer Science degree from State University and have worked on projects ranging from e-commerce platforms to data visualization tools. I'm particularly passionate about creating intuitive user experiences and writing clean, maintainable code.

I'm excited about this opportunity at your company because I'm passionate about [specific aspect of the role], and I believe my experience in [relevant skill] would allow me to make an immediate impact on your team. I've been following your company's work on [specific project/product] and I'm impressed by your commitment to [company value].""",
                "tips": [
                    "Keep it under 90 seconds total",
                    "Focus on relevant experience for THIS role",
                    "End with why you're interested in THIS company",
                    "Practice out loud to get timing right",
                    "Avoid personal life details unless relevant"
                ],
                "keywords": ["tell me about yourself", "introduce yourself", "walk me through your background"]
            },
            
            "challenging_project": {
                "question": "Describe a challenging project you worked on",
                "category": "Behavioral",
                "structure": [
                    "Situation: What was the project and context?",
                    "Task: What was your specific role/challenge?",
                    "Action: What steps did you take?",
                    "Result: What was the outcome?"
                ],
                "example": """[Situation] At my previous company, we needed to migrate our monolithic application to a microservices architecture to handle 10x traffic growth. The system was serving 100,000+ active users and the old architecture was causing frequent outages during peak hours.

[Task] I was tasked with leading the backend migration while ensuring zero downtime for our users. The challenge was that the codebase was 5 years old with minimal documentation, and we had a hard deadline of 3 months before our major product launch.

[Action] I started by mapping out all the dependencies and breaking down the monolith into 5 core services. I implemented API gateways for routing, set up comprehensive monitoring with Datadog, and created a phased rollout plan. I coordinated with 3 different teams (frontend, DevOps, and QA) and held weekly sync meetings. We used feature flags to gradually shift traffic to the new services, starting with 5% of users and scaling up over 6 weeks.

[Result] We successfully migrated with zero downtime. Response times improved by 40%, and the new architecture handled Black Friday traffic (5x normal load) without any issues. The CEO personally thanked our team, and this migration approach became the template for future system redesigns. I also documented the entire process, which reduced onboarding time for new engineers by 50%.""",
                "tips": [
                    "Use specific numbers and metrics",
                    "Highlight your leadership and initiative",
                    "Explain the business impact, not just technical details",
                    "Show problem-solving skills",
                    "Mention collaboration with other teams"
                ],
                "keywords": ["challenging project", "difficult project", "complex project", "hardest project"]
            },
            
            "time_you_failed": {
                "question": "Tell me about a time you failed",
                "category": "Behavioral",
                "structure": [
                    "Situation: What happened?",
                    "Task: What were you trying to achieve?",
                    "Action: What went wrong and what did you do?",
                    "Result: What did you learn?"
                ],
                "example": """[Situation] In my second year as a developer, I was leading the development of a new feature that would allow users to export their data in multiple formats. I was confident in my abilities and didn't think I needed much input from the team.

[Task] I was responsible for designing the architecture and implementing the feature within a 2-week sprint. The goal was to support CSV, JSON, and PDF exports for datasets up to 1 million rows.

[Action] I dove straight into coding without properly discussing the approach with senior engineers. I built a solution that worked well for small datasets but completely failed when users tried to export large files - the server would timeout and crash. We had to roll back the feature on launch day, which was embarrassing and delayed our release by 3 weeks.

[Result] This taught me several valuable lessons. First, I learned the importance of seeking input from experienced team members, especially for complex features. Second, I now always test edge cases and performance at scale before deployment. Third, I implemented a practice of doing design reviews before major features. Since then, I've successfully launched 10+ features without any major issues, and I now mentor junior developers on the importance of collaboration and thorough testing. This failure made me a much better engineer.""",
                "tips": [
                    "Choose a real failure, but not a catastrophic one",
                    "Focus heavily on what you learned",
                    "Show how you've improved since then",
                    "Demonstrate self-awareness and growth",
                    "End on a positive note about current practices"
                ],
                "keywords": ["time you failed", "biggest failure", "mistake you made", "when things went wrong"]
            },
            
            "conflict_with_teammate": {
                "question": "Describe a time you had a conflict with a teammate",
                "category": "Behavioral",
                "structure": [
                    "Situation: What was the conflict?",
                    "Task: What needed to be resolved?",
                    "Action: How did you handle it?",
                    "Result: What was the outcome?"
                ],
                "example": """[Situation] During a critical project, I had a disagreement with a senior developer about the technology stack we should use. They wanted to use a familiar but outdated framework, while I advocated for a modern solution that would be more maintainable long-term.

[Task] We needed to make a decision quickly as the project deadline was approaching, and the tension was affecting team morale. As a mid-level developer, I needed to respectfully challenge a senior colleague while finding a solution that worked for everyone.

[Action] I requested a one-on-one meeting to understand their perspective better. I learned they were concerned about the learning curve and project timeline. I proposed a compromise: we'd use the modern framework but I would create comprehensive documentation and pair-program with team members to reduce the learning curve. I also prepared a technical comparison showing long-term benefits. We presented both options to the team lead together.

[Result] The team lead appreciated our collaborative approach and we went with the modern framework with my support plan. I created video tutorials and held daily office hours for the first two weeks. The project launched on time, and the senior developer later thanked me for pushing for the better solution. We became close collaborators and I learned the importance of understanding others' concerns before advocating for my position.""",
                "tips": [
                    "Show emotional intelligence and empathy",
                    "Demonstrate active listening",
                    "Focus on finding win-win solutions",
                    "Avoid blaming the other person",
                    "Highlight positive relationship outcome"
                ],
                "keywords": ["conflict with teammate", "disagreement", "difficult coworker", "team conflict"]
            },
            
            "why_this_company": {
                "question": "Why do you want to work for this company?",
                "category": "Behavioral",
                "structure": [
                    "Company Mission/Values alignment",
                    "Specific products/projects you admire",
                    "Growth opportunities",
                    "How you can contribute"
                ],
                "example": """I'm excited about this opportunity for three main reasons.

First, your company's mission to [specific mission] deeply resonates with me. I've always been passionate about [related passion], and I love that you're using technology to [specific impact]. Your commitment to [specific value] aligns perfectly with my own values.

Second, I'm particularly impressed by [specific product/project]. I've been following your work on [specific feature] and I think the approach you took to [technical challenge] was brilliant. As someone who has worked on similar problems at my current company, I can appreciate the engineering excellence behind it. I'm especially excited about your recent announcement regarding [recent news/product].

Third, I see tremendous growth opportunities here. Your engineering blog posts about [specific topic] show that you invest in your team's development. I'm looking to deepen my expertise in [specific skill], and I know your team is at the forefront of this technology. I'm also excited about the chance to work with [specific team/person] whose work I've admired.

Most importantly, I believe I can make an immediate impact. My experience with [relevant skill] and my track record of [specific achievement] would allow me to contribute to [specific team goal] from day one.""",
                "tips": [
                    "Research the company thoroughly beforehand",
                    "Mention specific products, projects, or blog posts",
                    "Connect your skills to their needs",
                    "Show genuine enthusiasm",
                    "Avoid generic answers like 'great culture'"
                ],
                "keywords": ["why this company", "why do you want to work here", "why us", "what interests you"]
            },
            
            # TECHNICAL QUESTIONS
            "explain_technical_concept": {
                "question": "Explain [technical concept] to a non-technical person",
                "category": "Technical",
                "structure": [
                    "Simple analogy or metaphor",
                    "Basic explanation without jargon",
                    "Real-world example",
                    "Why it matters"
                ],
                "example": """Let me explain APIs using a restaurant analogy.

Imagine you're at a restaurant. You (the customer) want food, and the kitchen (the server) can make that food. But you don't go directly into the kitchen - instead, you tell the waiter what you want. The waiter takes your order to the kitchen, and brings back your food. The waiter is like an API - it's the messenger that takes requests and delivers responses.

In technical terms, an API (Application Programming Interface) is a way for different software applications to talk to each other. When you use a weather app on your phone, it's using an API to request weather data from a weather service, which then sends back the information to display.

For example, when you click "Login with Google" on a website, that website is using Google's API to verify your identity without you having to create a new account. The website asks Google "Is this person who they say they are?" and Google responds with yes or no.

APIs matter because they allow different systems to work together seamlessly. Without APIs, every app would need to build everything from scratch, which would be incredibly inefficient. They're the foundation of how modern software works.""",
                "tips": [
                    "Start with a relatable analogy",
                    "Avoid technical jargon",
                    "Use concrete examples from daily life",
                    "Check for understanding",
                    "Explain the 'why' not just the 'what'"
                ],
                "keywords": ["explain to non-technical", "explain like i'm five", "simple explanation"]
            },
            
            "technical_decision": {
                "question": "Describe a technical decision you made and why",
                "category": "Technical",
                "structure": [
                    "Context: What was the problem?",
                    "Options: What alternatives did you consider?",
                    "Decision: What did you choose and why?",
                    "Outcome: How did it work out?"
                ],
                "example": """[Context] At my previous company, we were building a real-time chat feature for our application. We needed to decide between using WebSockets, Server-Sent Events (SSE), or polling for real-time communication. The feature needed to support 10,000+ concurrent users with minimal latency.

[Options] I evaluated three approaches:
1. WebSockets - Full duplex communication, but more complex to implement and scale
2. Server-Sent Events - Simpler, but only server-to-client communication
3. Long polling - Easiest to implement, but inefficient for real-time updates

I created a comparison matrix considering: scalability, latency, browser support, implementation complexity, and infrastructure costs.

[Decision] I chose WebSockets because:
- We needed bidirectional communication (users sending and receiving messages)
- The latency requirements (<100ms) ruled out polling
- We had the engineering resources to handle the complexity
- Our infrastructure (AWS with ELB) supported WebSocket connections
- The long-term scalability benefits outweighed the initial complexity

[Outcome] The implementation took 3 weeks instead of the estimated 2, but it was worth it. We achieved average latency of 50ms, successfully handled 15,000 concurrent users during peak times, and the architecture scaled smoothly as we grew. Six months later, we added video calling using the same WebSocket infrastructure, which validated our decision. The initial investment in the more complex solution paid off.""",
                "tips": [
                    "Show your decision-making process",
                    "Explain trade-offs you considered",
                    "Use data to support your decision",
                    "Acknowledge any downsides",
                    "Discuss long-term implications"
                ],
                "keywords": ["technical decision", "architecture decision", "technology choice", "design decision"]
            },
            
            # LEADERSHIP QUESTIONS
            "leadership_example": {
                "question": "Give an example of when you showed leadership",
                "category": "Leadership",
                "structure": [
                    "Situation: What was the context?",
                    "Challenge: What needed leadership?",
                    "Action: How did you lead?",
                    "Result: What was the impact?"
                ],
                "example": """[Situation] During a critical product launch, our team lead unexpectedly went on medical leave for 6 weeks. We were 3 weeks away from launch with several major features incomplete and the team was feeling anxious about the timeline.

[Challenge] Although I was a mid-level engineer, I needed to step up and keep the team on track. The challenge was maintaining morale, making technical decisions, and coordinating with stakeholders - all while continuing my own development work.

[Action] I took several leadership actions:
- Organized a team meeting to assess our status and reprioritize features
- Created a daily standup structure to improve communication
- Volunteered to be the point of contact for product and design teams
- Paired junior developers with senior ones to unblock technical challenges
- Set up a shared dashboard to track progress transparently
- Made the tough call to cut two non-critical features to meet the deadline

I also made sure to check in with each team member individually to address concerns and provide support.

[Result] We successfully launched on time with all critical features complete. The product exceeded initial adoption goals by 30%. More importantly, team morale remained high throughout the process. When our team lead returned, they commended the team's performance and I was promoted to senior engineer. Three team members specifically mentioned my leadership in their feedback, and I learned that leadership isn't about title - it's about stepping up when needed.""",
                "tips": [
                    "Show initiative and ownership",
                    "Highlight people management skills",
                    "Demonstrate decision-making under pressure",
                    "Mention team outcomes, not just personal",
                    "Show humility and give credit to team"
                ],
                "keywords": ["leadership", "led a team", "took charge", "stepped up"]
            },
            
            # STRENGTHS & WEAKNESSES
            "greatest_strength": {
                "question": "What is your greatest strength?",
                "category": "Self-Assessment",
                "structure": [
                    "State the strength clearly",
                    "Provide specific example",
                    "Show impact/results",
                    "Connect to the role"
                ],
                "example": """My greatest strength is my ability to break down complex problems into manageable pieces and communicate solutions clearly to both technical and non-technical stakeholders.

For example, at my current company, we were facing a critical performance issue that was affecting our largest client. The problem involved multiple systems and no one could pinpoint the root cause. I spent two days analyzing logs, profiling the application, and mapping out all the dependencies. I discovered that the issue was caused by an interaction between three different services that only occurred under specific conditions.

Instead of just fixing it, I created a visual diagram showing how the systems interacted and where the bottleneck occurred. I presented this to both the engineering team and the client's technical team. This clear communication helped everyone understand the problem and the proposed solution. We implemented the fix, which improved performance by 70%, and the client was so impressed with the transparency that they expanded their contract.

This strength would be particularly valuable in this role because you mentioned the need to work across multiple teams and explain technical decisions to product managers. I thrive in that kind of environment where clear communication is essential.""",
                "tips": [
                    "Choose a strength relevant to the job",
                    "Back it up with a concrete example",
                    "Show measurable impact",
                    "Connect it to the role you're applying for",
                    "Be genuine, not boastful"
                ],
                "keywords": ["greatest strength", "what are you good at", "your strengths", "best quality"]
            },
            
            "greatest_weakness": {
                "question": "What is your greatest weakness?",
                "category": "Self-Assessment",
                "structure": [
                    "State a real weakness (not a humble brag)",
                    "Explain the impact it had",
                    "Describe what you're doing to improve",
                    "Show progress you've made"
                ],
                "example": """My greatest weakness is that I sometimes struggle with delegating tasks because I want to ensure everything is done to a high standard. Early in my career, this led to me taking on too much work and becoming a bottleneck for my team.

For example, during a major project last year, I was reviewing every pull request in detail and rewriting code that didn't meet my standards. While the code quality was high, I was working 60-hour weeks and my team members felt micromanaged. One of them gave me honest feedback that I wasn't giving them opportunities to grow.

This was a wake-up call. I've been actively working on this by:
- Setting clear coding standards upfront so expectations are aligned
- Focusing my reviews on critical issues rather than style preferences
- Pairing with junior developers to teach rather than just fixing
- Consciously stepping back and letting others own features end-to-end
- Tracking my work hours to ensure I'm not overloading myself

The progress has been significant. In our last project, I successfully delegated three major features to team members, provided guidance without micromanaging, and the features were delivered on time with great quality. My team's satisfaction scores improved by 40%, and I'm working more sustainable hours. I'm still working on finding the right balance, but I'm much better than I was a year ago.""",
                "tips": [
                    "Choose a real weakness, not 'I work too hard'",
                    "Show self-awareness and honesty",
                    "Focus on what you're doing to improve",
                    "Demonstrate actual progress",
                    "Don't choose a weakness critical to the role"
                ],
                "keywords": ["greatest weakness", "areas for improvement", "what do you struggle with", "weaknesses"]
            }
        }
    
    def get_template(self, question: str) -> Optional[Dict]:
        """
        Get template for a question using fuzzy matching
        
        Args:
            question: The interview question
            
        Returns:
            Template dict or None if no match found
        """
        question_lower = question.lower().strip()
        
        # Try exact keyword matching first
        for template_id, template in self.templates.items():
            for keyword in template.get("keywords", []):
                if keyword in question_lower:
                    logger.info(f"✅ Template match: {template_id} (keyword: {keyword})")
                    return template
        
        # Try fuzzy matching on question text
        best_match = None
        best_score = 0.0
        
        for template_id, template in self.templates.items():
            template_question = template["question"].lower()
            score = self._similarity(question_lower, template_question)
            
            if score > best_score and score > 0.6:  # 60% similarity threshold
                best_score = score
                best_match = template
        
        if best_match:
            logger.info(f"✅ Template match: fuzzy match (score: {best_score:.2f})")
            return best_match
        
        logger.info(f"❌ No template match for: {question}")
        return None
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def get_all_templates(self) -> List[Dict]:
        """Get all templates"""
        return list(self.templates.values())
    
    def get_templates_by_category(self, category: str) -> List[Dict]:
        """Get templates for a specific category"""
        return [
            template for template in self.templates.values()
            if template.get("category") == category
        ]
    
    def search_templates(self, query: str) -> List[Dict]:
        """Search templates by query"""
        query_lower = query.lower()
        results = []
        
        for template in self.templates.values():
            # Search in question, category, and keywords
            if (query_lower in template["question"].lower() or
                query_lower in template.get("category", "").lower() or
                any(query_lower in kw for kw in template.get("keywords", []))):
                results.append(template)
        
        return results


# Global instance
_templates_library = None

def get_templates_library() -> AnswerTemplatesLibrary:
    """Get or create global templates library"""
    global _templates_library
    if _templates_library is None:
        _templates_library = AnswerTemplatesLibrary()
    return _templates_library
