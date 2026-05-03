"""
Advanced Feedback Engine
Comprehensive AI-powered answer evaluation with multi-dimensional analysis
Inspired by: Pramp, Interviewing.io, LeetCode, HackerRank
"""
import logging
import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class AdvancedFeedbackEngine:
    """
    Best-in-class feedback system with:
    - Multi-dimensional scoring
    - Detailed rubric-based evaluation
    - Actionable improvement suggestions
    - Communication analysis
    - Technical depth assessment
    - Comparison with ideal answers
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.openai_url = "https://api.openai.com/v1/chat/completions"
    
    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        category: str = "General",
        difficulty: str = "intermediate",
        context: Dict = None
    ) -> Dict:
        """
        Comprehensive answer evaluation with company-specific and difficulty-aware feedback
        
        Returns:
            Dict with detailed feedback including:
            - Overall score (0-10)
            - Dimension scores (technical, communication, structure, completeness)
            - Strengths (what was done well)
            - Weaknesses (areas to improve)
            - Specific suggestions (actionable items)
            - Ideal answer comparison
            - Company-specific tips
            - Difficulty-appropriate expectations
            - Next steps
        """
        try:
            # Extract company from context if available
            company = context.get("company", "") if context else ""
            
            # Multi-dimensional analysis
            dimensions = await self._analyze_dimensions(question, answer, category, difficulty)
            
            # Communication analysis
            communication = self._analyze_communication(answer)
            
            # Technical depth
            technical = self._analyze_technical_depth(answer, category)
            
            # Structure analysis
            structure = self._analyze_structure(answer, category)
            
            # Completeness check
            completeness = self._analyze_completeness(question, answer)
            
            # Generate AI-powered insights (if API available) with enhanced context
            ai_insights = await self._get_ai_insights(question, answer, category, difficulty, company)
            
            # Calculate overall score with difficulty adjustment
            overall_score = self._calculate_overall_score(dimensions, communication, technical, structure, completeness, difficulty)
            
            # Generate actionable feedback with company-specific and difficulty-aware advice
            feedback = self._generate_feedback(
                overall_score=overall_score,
                dimensions=dimensions,
                communication=communication,
                technical=technical,
                structure=structure,
                completeness=completeness,
                ai_insights=ai_insights,
                category=category,
                difficulty=difficulty,
                company=company,
                question=question
            )
            
            return feedback
            
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return self._fallback_evaluation(question, answer)
    
    async def _analyze_dimensions(
        self,
        question: str,
        answer: str,
        category: str,
        difficulty: str
    ) -> Dict:
        """
        Multi-dimensional scoring rubric
        Dimensions: Technical Accuracy, Communication, Problem-Solving, Completeness
        """
        dimensions = {
            "technical_accuracy": 0,
            "communication_clarity": 0,
            "problem_solving": 0,
            "completeness": 0,
            "depth": 0
        }
        
        # Technical accuracy (0-10)
        if category in ["Python", "JavaScript", "Data Structures", "Algorithms"]:
            dimensions["technical_accuracy"] = self._score_technical_accuracy(answer, category)
        else:
            dimensions["technical_accuracy"] = 7.0  # Default for non-technical
        
        # Communication clarity (0-10)
        dimensions["communication_clarity"] = self._score_communication(answer)
        
        # Problem-solving approach (0-10)
        dimensions["problem_solving"] = self._score_problem_solving(answer, question)
        
        # Completeness (0-10)
        dimensions["completeness"] = self._score_completeness(question, answer)
        
        # Depth of understanding (0-10)
        dimensions["depth"] = self._score_depth(answer, category)
        
        return dimensions
    
    def _score_technical_accuracy(self, answer: str, category: str) -> float:
        """Enhanced technical accuracy scoring with better keyword matching"""
        score = 4.0  # Lower base score to be more discriminating
        
        # Expanded category-specific keywords with weights
        keywords = {
            "Python": {
                "high": ["class", "inheritance", "decorator", "generator", "comprehension", "async", "await"],
                "medium": ["function", "method", "variable", "loop", "list", "dict", "import", "def", "return"],
                "basic": ["print", "if", "else", "for", "while"]
            },
            "JavaScript": {
                "high": ["closure", "prototype", "promise", "async/await", "event loop", "hoisting"],
                "medium": ["function", "const", "let", "arrow", "callback", "event", "DOM"],
                "basic": ["var", "if", "else", "for"]
            },
            "Data Structures": {
                "high": ["time complexity", "space complexity", "amortized", "balanced tree", "hash collision"],
                "medium": ["array", "linked list", "tree", "graph", "hash", "stack", "queue"],
                "basic": ["list", "search", "insert", "delete"]
            },
            "Algorithms": {
                "high": ["dynamic programming", "greedy", "divide and conquer", "backtracking", "memoization"],
                "medium": ["time complexity", "space complexity", "O(n)", "sort", "search", "recursive"],
                "basic": ["loop", "iteration", "comparison"]
            },
            "System Design": {
                "high": ["CAP theorem", "eventual consistency", "sharding", "replication", "consensus"],
                "medium": ["scalability", "load balancer", "database", "cache", "microservice", "API"],
                "basic": ["server", "client", "request", "response"]
            },
            "Database": {
                "high": ["ACID", "normalization", "denormalization", "indexing strategy", "query optimization"],
                "medium": ["SQL", "query", "index", "join", "transaction", "primary key", "foreign key"],
                "basic": ["table", "select", "insert", "update", "delete"]
            },
            "Behavioral": {
                "high": ["quantifiable result", "metrics", "impact", "leadership", "conflict resolution"],
                "medium": ["situation", "task", "action", "result", "team", "project"],
                "basic": ["I did", "we did", "my role"]
            }
        }
        
        answer_lower = answer.lower()
        category_keywords = keywords.get(category, {"medium": [], "basic": []})
        
        # Count weighted keyword matches
        high_matches = sum(1 for kw in category_keywords.get("high", []) if kw.lower() in answer_lower)
        medium_matches = sum(1 for kw in category_keywords.get("medium", []) if kw.lower() in answer_lower)
        basic_matches = sum(1 for kw in category_keywords.get("basic", []) if kw.lower() in answer_lower)
        
        # Weighted scoring
        score += high_matches * 1.5
        score += medium_matches * 0.8
        score += basic_matches * 0.3
        
        # Check for code examples (strong indicator)
        if "```" in answer or ("def " in answer and ":" in answer) or ("function " in answer and "{" in answer):
            score += 1.5
        
        # Check for detailed explanations
        explanation_words = ["because", "therefore", "this means", "for example", "specifically", "in other words"]
        explanation_count = sum(1 for word in explanation_words if word in answer_lower)
        score += min(explanation_count * 0.4, 1.5)
        
        # Check for comparisons (shows deeper understanding)
        if any(word in answer_lower for word in ["compared to", "versus", "vs", "difference between", "unlike"]):
            score += 0.8
        
        # Check for real-world context
        if any(word in answer_lower for word in ["in practice", "real-world", "production", "industry standard"]):
            score += 0.7
        
        # Penalty for very short answers
        word_count = len(answer.split())
        if word_count < 20:
            score -= 2.0
        elif word_count < 40:
            score -= 1.0
        
        return min(10.0, max(0.0, score))
    
    def _score_communication(self, answer: str) -> float:
        """Enhanced communication clarity scoring"""
        score = 3.0  # Lower base to be more discriminating
        
        # Length check with better ranges
        word_count = len(answer.split())
        if 80 <= word_count <= 250:
            score += 3.0  # Ideal length
        elif 50 <= word_count < 80 or 250 < word_count <= 400:
            score += 2.0  # Good length
        elif 30 <= word_count < 50 or 400 < word_count <= 600:
            score += 1.0  # Acceptable
        elif word_count < 20:
            score -= 1.5  # Too short penalty
        elif word_count > 600:
            score -= 0.5  # Too verbose penalty
        
        # Sentence structure and variety
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        sentence_count = len(sentences)
        
        if sentence_count >= 5:
            score += 1.5
        elif sentence_count >= 3:
            score += 1.0
        elif sentence_count < 2:
            score -= 0.5
        
        # Check sentence length variety (good communication has varied sentence lengths)
        if sentence_count > 2:
            sentence_lengths = [len(s.split()) for s in sentences]
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            if 10 <= avg_length <= 25:  # Ideal average sentence length
                score += 0.8
        
        # Use of examples (strong indicator of clarity)
        example_indicators = ["for example", "such as", "like", "instance", "e.g.", "for instance"]
        example_count = sum(1 for indicator in example_indicators if indicator in answer.lower())
        score += min(example_count * 0.8, 1.5)
        
        # Clarity and transition indicators
        transition_words = ["first", "second", "third", "finally", "however", "therefore", 
                          "moreover", "additionally", "consequently", "thus", "hence"]
        transition_count = sum(1 for word in transition_words if word in answer.lower())
        score += min(transition_count * 0.5, 1.5)
        
        # Professional language indicators
        professional_phrases = ["in my experience", "based on", "according to", "research shows", 
                               "best practice", "industry standard", "proven approach"]
        professional_count = sum(1 for phrase in professional_phrases if phrase in answer.lower())
        score += min(professional_count * 0.4, 1.0)
        
        # Penalty for excessive filler words
        filler_count = self._count_filler_words(answer)
        if filler_count > 8:
            score -= 1.5
        elif filler_count > 5:
            score -= 1.0
        elif filler_count > 3:
            score -= 0.5
        
        # Bonus for clear structure
        if any(word in answer.lower() for word in ["in summary", "to conclude", "in conclusion"]):
            score += 0.5
        
        return min(10.0, max(0.0, score))
    
    def _score_problem_solving(self, answer: str, question: str) -> float:
        """Enhanced problem-solving approach scoring"""
        score = 3.0  # Lower base score
        
        answer_lower = answer.lower()
        
        # Mentions systematic approach/strategy
        approach_indicators = ["approach", "strategy", "method", "solution", "way to", "technique", 
                              "algorithm", "process", "steps", "methodology"]
        approach_count = sum(1 for indicator in approach_indicators if indicator in answer_lower)
        score += min(approach_count * 0.7, 2.0)
        
        # Mentions trade-offs and considerations (critical thinking)
        tradeoff_indicators = ["trade-off", "tradeoff", "advantage", "disadvantage", "pros", "cons",
                              "benefit", "drawback", "limitation", "consideration"]
        tradeoff_count = sum(1 for indicator in tradeoff_indicators if indicator in answer_lower)
        score += min(tradeoff_count * 0.9, 2.5)
        
        # Mentions alternatives (shows breadth of knowledge)
        alternative_indicators = ["alternative", "another way", "could also", "instead", "alternatively",
                                 "other option", "different approach", "another method"]
        alternative_count = sum(1 for indicator in alternative_indicators if indicator in answer_lower)
        score += min(alternative_count * 0.8, 2.0)
        
        # Structured thinking (step-by-step approach)
        structure_indicators = ["step 1", "step 2", "first", "second", "third", "then", "next", 
                               "after that", "finally", "lastly"]
        structure_count = sum(1 for indicator in structure_indicators if indicator in answer_lower)
        score += min(structure_count * 0.6, 1.5)
        
        # Problem breakdown (shows analytical thinking)
        breakdown_indicators = ["break down", "analyze", "consider", "evaluate", "assess",
                               "examine", "investigate", "determine"]
        breakdown_count = sum(1 for indicator in breakdown_indicators if indicator in answer_lower)
        score += min(breakdown_count * 0.5, 1.0)
        
        # Edge cases and error handling (thorough thinking)
        edge_case_indicators = ["edge case", "corner case", "exception", "error handling",
                               "boundary", "special case", "what if"]
        edge_count = sum(1 for indicator in edge_case_indicators if indicator in answer_lower)
        score += min(edge_count * 0.8, 1.5)
        
        # Optimization thinking
        optimization_indicators = ["optimize", "improve", "efficient", "performance", "faster",
                                  "better", "reduce complexity"]
        optimization_count = sum(1 for indicator in optimization_indicators if indicator in answer_lower)
        score += min(optimization_count * 0.6, 1.0)
        
        return min(10.0, max(0.0, score))
    
    def _score_completeness(self, question: str, answer: str) -> float:
        """Enhanced answer completeness scoring"""
        score = 3.0  # Lower base score
        
        # Extract key concepts from question (improved)
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Remove common question words
        question_words = set(re.findall(r'\b\w{4,}\b', question_lower))  # Words with 4+ chars
        answer_words = set(re.findall(r'\b\w{4,}\b', answer_lower))
        
        common_words = {"what", "when", "where", "which", "would", "could", "should", 
                       "does", "have", "been", "this", "that", "with", "from", "they"}
        question_words -= common_words
        
        # Check coverage of question concepts
        if question_words:
            coverage = len(question_words & answer_words) / len(question_words)
            score += coverage * 4.0  # Up to 4 points for coverage
        
        # Check for examples (shows completeness)
        example_indicators = ["example", "for instance", "such as", "like", "e.g.", "for example"]
        example_count = sum(1 for indicator in example_indicators if indicator in answer_lower)
        score += min(example_count * 0.8, 1.5)
        
        # Check for reasoning/explanation
        reasoning_indicators = ["because", "therefore", "this is why", "the reason", "due to",
                               "as a result", "consequently", "thus", "hence"]
        reasoning_count = sum(1 for indicator in reasoning_indicators if indicator in answer_lower)
        score += min(reasoning_count * 0.6, 1.5)
        
        # Check for comprehensive coverage indicators
        comprehensive_indicators = ["also", "additionally", "furthermore", "moreover", "in addition",
                                   "another", "besides", "as well"]
        comprehensive_count = sum(1 for indicator in comprehensive_indicators if indicator in answer_lower)
        score += min(comprehensive_count * 0.5, 1.0)
        
        # Check for conclusion/summary
        conclusion_indicators = ["conclusion", "summary", "in summary", "to summarize", "overall",
                                "in conclusion", "to conclude"]
        if any(indicator in answer_lower for indicator in conclusion_indicators):
            score += 0.8
        
        # Check for edge cases/exceptions (shows thoroughness)
        edge_indicators = ["edge case", "exception", "special case", "also consider", "however",
                          "but", "although", "unless"]
        edge_count = sum(1 for indicator in edge_indicators if indicator in answer_lower)
        score += min(edge_count * 0.6, 1.2)
        
        # Penalty for very short answers (likely incomplete)
        word_count = len(answer.split())
        if word_count < 30:
            score -= 2.0
        elif word_count < 50:
            score -= 1.0
        
        return min(10.0, max(0.0, score))
    
    def _score_depth(self, answer: str, category: str) -> float:
        """Enhanced depth of understanding scoring"""
        score = 3.0  # Lower base score
        
        answer_lower = answer.lower()
        
        # Technical depth indicators (weighted by importance)
        high_depth_indicators = [
            "implementation", "underlying", "internal", "mechanism",
            "architecture", "design pattern", "best practice",
            "optimization", "performance", "efficiency", "complexity analysis",
            "scalability", "maintainability", "trade-off analysis"
        ]
        
        medium_depth_indicators = [
            "works by", "how it", "why it", "the way", "process",
            "principle", "concept", "theory", "approach"
        ]
        
        # Count depth indicators with weights
        high_matches = sum(1 for indicator in high_depth_indicators if indicator in answer_lower)
        medium_matches = sum(1 for indicator in medium_depth_indicators if indicator in answer_lower)
        
        score += min(high_matches * 1.2, 3.0)
        score += min(medium_matches * 0.6, 1.5)
        
        # Mentions edge cases (shows thorough understanding)
        edge_case_indicators = ["edge case", "corner case", "exception", "error handling",
                               "boundary condition", "special case"]
        edge_count = sum(1 for indicator in edge_case_indicators if indicator in answer_lower)
        score += min(edge_count * 0.9, 1.5)
        
        # Mentions real-world application (practical depth)
        real_world_indicators = ["real-world", "production", "in practice", "industry",
                                "practical", "actual use", "real scenario"]
        real_world_count = sum(1 for indicator in real_world_indicators if indicator in answer_lower)
        score += min(real_world_count * 0.8, 1.5)
        
        # Mentions comparisons (comparative understanding)
        comparison_indicators = ["compared to", "versus", "vs", "difference between",
                                "unlike", "similar to", "in contrast"]
        comparison_count = sum(1 for indicator in comparison_indicators if indicator in answer_lower)
        score += min(comparison_count * 0.7, 1.5)
        
        # Technical details (shows deep knowledge)
        technical_detail_indicators = ["specifically", "precisely", "exactly", "in detail",
                                      "technically", "under the hood", "internally"]
        detail_count = sum(1 for indicator in technical_detail_indicators if indicator in answer_lower)
        score += min(detail_count * 0.6, 1.0)
        
        # Mentions limitations/constraints (mature understanding)
        limitation_indicators = ["limitation", "constraint", "drawback", "challenge",
                                "consideration", "caveat", "trade-off"]
        limitation_count = sum(1 for indicator in limitation_indicators if indicator in answer_lower)
        score += min(limitation_count * 0.7, 1.5)
        
        # Code examples with explanation (strong depth indicator)
        has_code = "```" in answer or ("def " in answer and ":" in answer) or ("function " in answer and "{" in answer)
        has_explanation = any(word in answer_lower for word in ["this code", "the function", "this implementation"])
        if has_code and has_explanation:
            score += 1.5
        elif has_code:
            score += 0.8
        
        return min(10.0, max(0.0, score))
    
    def _analyze_communication(self, answer: str) -> Dict:
        """Detailed communication analysis"""
        return {
            "word_count": len(answer.split()),
            "sentence_count": len([s for s in answer.split('.') if s.strip()]),
            "avg_sentence_length": len(answer.split()) / max(len([s for s in answer.split('.') if s.strip()]), 1),
            "has_examples": any(word in answer.lower() for word in ["example", "for instance", "such as"]),
            "has_structure": any(word in answer.lower() for word in ["first", "second", "finally", "then"]),
            "clarity_score": self._score_communication(answer),
            "filler_words": self._count_filler_words(answer),
            "technical_terms": self._count_technical_terms(answer)
        }
    
    def _count_filler_words(self, answer: str) -> int:
        """Count filler words"""
        fillers = ["um", "uh", "like", "you know", "basically", "actually", "literally", "just", "really", "very"]
        answer_lower = answer.lower()
        return sum(answer_lower.count(filler) for filler in fillers)
    
    def _count_technical_terms(self, answer: str) -> int:
        """Count technical terms"""
        technical_terms = [
            "algorithm", "complexity", "optimization", "implementation",
            "architecture", "design pattern", "data structure", "API",
            "database", "scalability", "performance", "efficiency"
        ]
        answer_lower = answer.lower()
        return sum(1 for term in technical_terms if term in answer_lower)
    
    def _get_company_specific_tips(self, company: str, category: str) -> str:
        """Get company-specific interview tips"""
        company_tips = {
            "Google": {
                "general": "Google values scalability, efficiency, and innovative thinking. Mention how your solution scales to billions of users.",
                "Python": "Discuss Python's role in Google's infrastructure. Mention tools like Bazel, gRPC, or Protocol Buffers if relevant.",
                "System Design": "Focus on distributed systems, CAP theorem, and Google's technologies (BigTable, Spanner, MapReduce concepts).",
                "Machine Learning": "Reference TensorFlow, Google's ML infrastructure, and production ML systems at scale."
            },
            "Amazon": {
                "general": "Amazon emphasizes Leadership Principles. Show customer obsession, ownership, and bias for action in your answers.",
                "Python": "Mention AWS services, boto3, Lambda, or how Python integrates with AWS ecosystem.",
                "System Design": "Discuss AWS services, microservices, and how to build highly available, fault-tolerant systems.",
                "Behavioral": "Use STAR method and tie answers to Amazon's 16 Leadership Principles."
            },
            "Microsoft": {
                "general": "Microsoft values growth mindset, collaboration, and customer focus. Show how you learn and adapt.",
                "Python": "Discuss Azure integration, .NET interoperability, or Microsoft's Python tools.",
                "System Design": "Reference Azure services, hybrid cloud solutions, and enterprise-scale architectures."
            },
            "TCS": {
                "general": "TCS values practical solutions for enterprise clients. Focus on reliability, maintainability, and business value.",
                "Python": "Mention enterprise applications, automation, and integration with TCS platforms like BaNCS or Ignio.",
                "System Design": "Discuss scalable enterprise solutions, banking systems, and client-specific requirements."
            },
            "Infosys": {
                "general": "Infosys emphasizes innovation and digital transformation. Show how technology solves business problems.",
                "Python": "Reference enterprise automation, Infosys platforms like Nia or Finacle integration.",
                "System Design": "Focus on enterprise architecture, cloud solutions, and digital transformation strategies."
            },
            "Wipro": {
                "general": "Wipro values innovation and client-centric solutions. Emphasize practical problem-solving.",
                "Python": "Discuss HOLMES AI platform, automation, and enterprise Python applications.",
                "System Design": "Reference cloud solutions, AI/ML integration, and scalable enterprise systems."
            },
            "Cognizant": {
                "general": "Cognizant focuses on digital solutions and client success. Show business impact of technical decisions.",
                "Python": "Mention intelligent automation, healthcare/banking solutions, and enterprise applications.",
                "System Design": "Discuss industry-specific solutions, cloud architecture, and digital transformation."
            },
            "Accenture": {
                "general": "Accenture values innovation and strategic thinking. Connect technical solutions to business outcomes.",
                "Python": "Reference myWizard platform, automation, and consulting-focused solutions.",
                "System Design": "Focus on enterprise transformation, cloud strategy, and scalable consulting solutions."
            },
            "Capgemini": {
                "general": "Capgemini emphasizes innovation and engineering excellence. Show technical depth and business acumen.",
                "Python": "Discuss intelligent automation, engineering solutions, and enterprise platforms.",
                "System Design": "Reference cloud infrastructure, digital transformation, and engineering best practices."
            }
        }
        
        company_data = company_tips.get(company, {})
        specific_tip = company_data.get(category, company_data.get("general", ""))
        return specific_tip if specific_tip else f"For {company} interviews, demonstrate both technical expertise and business understanding."
    
    def _get_difficulty_expectations(self, difficulty: str, category: str) -> str:
        """Get difficulty-specific expectations"""
        expectations = {
            "beginner": f"""
- Clear explanation of fundamental concepts
- At least one simple example
- Basic understanding of {category} principles
- 50-100 words with organized thoughts
- No need for advanced optimizations or edge cases
            """,
            "intermediate": f"""
- Solid understanding with detailed explanations
- Multiple examples or use cases
- Discussion of trade-offs and alternatives
- 100-200 words with clear structure
- Mention of common pitfalls or best practices
- Some consideration of performance/scalability
            """,
            "advanced": f"""
- Deep technical knowledge with nuanced understanding
- Real-world production examples
- Comprehensive trade-off analysis
- 150-300 words with excellent structure
- Discussion of edge cases, optimizations, and scalability
- Industry best practices and advanced concepts
- Comparison of multiple approaches with justification
            """
        }
        return expectations.get(difficulty, expectations["intermediate"])
    
    def _get_score_description(self, difficulty: str, score_range: str) -> str:
        """Get score description based on difficulty level"""
        descriptions = {
            "beginner": {
                "9-10": "Excellent grasp of fundamentals with clear examples",
                "7-8": "Good understanding of basics, minor gaps acceptable",
                "5-6": "Basic knowledge but needs more clarity or examples",
                "3-4": "Significant gaps in fundamental understanding",
                "1-2": "Minimal understanding of basic concepts"
            },
            "intermediate": {
                "9-10": "Comprehensive answer with trade-offs and best practices",
                "7-8": "Solid understanding with good examples, minor improvements needed",
                "5-6": "Decent knowledge but missing key concepts or depth",
                "3-4": "Surface-level understanding with significant gaps",
                "1-2": "Insufficient knowledge for intermediate level"
            },
            "advanced": {
                "9-10": "Expert-level answer with production insights and deep analysis",
                "7-8": "Strong technical depth with good trade-off discussion",
                "5-6": "Good knowledge but lacks advanced concepts or depth",
                "3-4": "Intermediate-level answer, not meeting advanced expectations",
                "1-2": "Insufficient depth for advanced level"
            }
        }
        return descriptions.get(difficulty, descriptions["intermediate"]).get(score_range, "")
    
    def _analyze_technical_depth(self, answer: str, category: str) -> Dict:
        """Analyze technical depth"""
        return {
            "has_code_example": "```" in answer or "def " in answer or "function " in answer,
            "mentions_complexity": any(word in answer.lower() for word in ["o(n)", "time complexity", "space complexity"]),
            "mentions_trade_offs": any(word in answer.lower() for word in ["trade-off", "advantage", "disadvantage"]),
            "mentions_alternatives": any(word in answer.lower() for word in ["alternative", "another approach", "could also"]),
            "depth_score": self._score_depth(answer, category),
            "technical_accuracy": self._score_technical_accuracy(answer, category)
        }
    
    def _analyze_structure(self, answer: str, category: str) -> Dict:
        """Analyze answer structure"""
        is_behavioral = category in ["Behavioral", "Leadership", "HR Interview"]
        
        structure = {
            "has_introduction": len(answer) > 50 and answer[:100].lower().count("i") > 0,
            "has_body": len(answer.split()) > 30,
            "has_conclusion": any(word in answer.lower() for word in ["conclusion", "summary", "overall"]),
            "is_organized": any(word in answer.lower() for word in ["first", "second", "then", "finally"]),
            "paragraph_count": answer.count('\n\n') + 1
        }
        
        if is_behavioral:
            # Check for STAR structure
            structure["has_situation"] = any(word in answer.lower() for word in ["situation", "when", "at", "during"])
            structure["has_task"] = any(word in answer.lower() for word in ["task", "responsible", "needed to", "had to"])
            structure["has_action"] = any(word in answer.lower() for word in ["i did", "i implemented", "i created", "i worked"])
            structure["has_result"] = any(word in answer.lower() for word in ["result", "outcome", "achieved", "improved"])
        
        return structure
    
    def _analyze_completeness(self, question: str, answer: str) -> Dict:
        """Analyze answer completeness"""
        return {
            "addresses_question": self._addresses_question(question, answer),
            "provides_examples": any(word in answer.lower() for word in ["example", "for instance", "such as"]),
            "explains_reasoning": any(word in answer.lower() for word in ["because", "therefore", "this is why"]),
            "covers_edge_cases": any(word in answer.lower() for word in ["edge case", "exception", "also"]),
            "completeness_score": self._score_completeness(question, answer)
        }
    
    def _addresses_question(self, question: str, answer: str) -> bool:
        """Check if answer addresses the question"""
        # Extract key words from question
        question_words = set(re.findall(r'\b\w+\b', question.lower()))
        answer_words = set(re.findall(r'\b\w+\b', answer.lower()))
        
        # Remove common words
        common_words = {"the", "a", "an", "is", "are", "was", "were", "what", "how", "why", "when", "where"}
        question_words -= common_words
        
        # Check overlap
        overlap = len(question_words & answer_words) / max(len(question_words), 1)
        return overlap > 0.3
    
    async def _get_ai_insights(
        self,
        question: str,
        answer: str,
        category: str,
        difficulty: str,
        company: str = ""
    ) -> Optional[Dict]:
        """Get AI-powered insights using OpenAI with enhanced prompts including company and difficulty context"""
        if not self.openai_api_key:
            return None
        
        try:
            # Build company-specific context
            company_context = ""
            if company:
                company_tips = self._get_company_specific_tips(company, category)
                company_context = f"\n**Company Context:** This is for a {company} interview. {company_tips}"
            
            # Build difficulty-specific expectations
            difficulty_expectations = self._get_difficulty_expectations(difficulty, category)
            
            prompt = f"""You are an expert technical interviewer analyzing a real interview answer. Be SPECIFIC and reference the ACTUAL content of the answer.

**Question:** {question}
**Category:** {category}
**Difficulty:** {difficulty}
**Candidate's Answer:** {answer}
{company_context}

**Difficulty Expectations ({difficulty}):**
{difficulty_expectations}

Analyze THIS SPECIFIC ANSWER (not a generic answer). Reference actual phrases, concepts, and details from the candidate's response.

Provide feedback in JSON format:

{{
  "strengths": [
    "Quote or reference SPECIFIC parts of their answer that were good",
    "Example: 'You correctly explained that [specific concept they mentioned]'",
    "Example: 'Your example about [their actual example] was relevant'",
    "Be precise - mention what THEY said, not what anyone could say"
  ],
  "weaknesses": [
    "Point out SPECIFIC gaps in THIS answer",
    "Example: 'You mentioned X but didn't explain how it relates to Y'",
    "Example: 'Your answer focused on A but missed B which is crucial for this question'",
    "Reference what's actually missing from THEIR response"
  ],
  "suggestions": [
    "Give ACTIONABLE advice specific to improving THIS answer",
    "Example: 'Add an explanation of [specific missing concept]'",
    "Example: 'Expand on your point about [what they mentioned] by discussing [specific addition]'",
    "Make it clear what to add/change in THIS specific answer"
  ],
  "ideal_answer_outline": "What THIS answer should have covered (2-3 sentences) - be specific to the question",
  "missing_elements": [
    "List SPECIFIC concepts/points missing from THIS answer",
    "Be concrete: 'Did not mention error handling', not 'Could be more complete'"
  ],
  "score_justification": "Explain the score based on what THIS answer contains and lacks, considering the {difficulty} difficulty level",
  "company_specific_advice": "{f'Specific advice for {company} interviews' if company else 'General interview advice'}",
  "ideal_answer_example": "Provide a brief example of how a strong candidate would answer this specific question (2-3 sentences)"
}}

**CRITICAL RULES:**
1. Reference the ACTUAL answer content - quote phrases they used
2. Identify SPECIFIC gaps - what concepts/details are missing
3. NO generic advice like "be more clear" - say WHAT to clarify
4. NO generic praise like "good effort" - say WHAT was good
5. Make it obvious you read THEIR answer, not a template
6. Consider the {difficulty} level - adjust expectations accordingly
{f'7. For {company}: Mention company-specific expectations and technologies' if company else ''}

**Scoring Guide for {difficulty} level:**
- 9-10: {self._get_score_description(difficulty, '9-10')}
- 7-8: {self._get_score_description(difficulty, '7-8')}
- 5-6: {self._get_score_description(difficulty, '5-6')}
- 3-4: {self._get_score_description(difficulty, '3-4')}
- 1-2: {self._get_score_description(difficulty, '1-2')}

Be honest and specific. This helps them improve."""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": f"You are a senior technical interviewer specializing in {category} interviews{f' at {company}' if company else ''}. Analyze the SPECIFIC answer provided. Reference actual content from the answer. Be precise, not generic. Quote their phrases. Identify specific gaps. Give actionable advice tailored to {difficulty} level."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500,
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(self.openai_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"AI insights error: {e}")
            return None
    
    def _calculate_overall_score(
        self,
        dimensions: Dict,
        communication: Dict,
        technical: Dict,
        structure: Dict,
        completeness: Dict,
        difficulty: str = "intermediate"
    ) -> float:
        """Calculate weighted overall score with difficulty adjustment"""
        # Weighted average of dimensions
        weights = {
            "technical_accuracy": 0.25,
            "communication_clarity": 0.20,
            "problem_solving": 0.20,
            "completeness": 0.20,
            "depth": 0.15
        }
        
        score = sum(dimensions[dim] * weight for dim, weight in weights.items())
        
        # Bonus for good structure
        if structure.get("is_organized"):
            score += 0.3
        
        # Penalty for too many fillers
        if communication.get("filler_words", 0) > 5:
            score -= 0.5
        
        # Difficulty-based adjustment (be more lenient for beginners, stricter for advanced)
        if difficulty == "beginner":
            # Boost beginner scores slightly if they show basic understanding
            if score >= 5.0:
                score += 0.5
        elif difficulty == "advanced":
            # Be stricter for advanced - require more depth
            if dimensions["depth"] < 7.0:
                score -= 0.5
        
        return min(10.0, max(0.0, score))
    
    def _generate_feedback(
        self,
        overall_score: float,
        dimensions: Dict,
        communication: Dict,
        technical: Dict,
        structure: Dict,
        completeness: Dict,
        ai_insights: Optional[Dict],
        category: str,
        difficulty: str = "intermediate",
        company: str = "",
        question: str = ""
    ) -> Dict:
        """Generate comprehensive feedback with company-specific and difficulty-aware advice"""
        
        # Determine performance level
        if overall_score >= 8.5:
            level = "Excellent"
            level_emoji = "🌟"
        elif overall_score >= 7.0:
            level = "Good"
            level_emoji = "✅"
        elif overall_score >= 5.5:
            level = "Fair"
            level_emoji = "📊"
        else:
            level = "Needs Improvement"
            level_emoji = "📈"
        
        # Generate strengths
        strengths = self._identify_strengths(dimensions, communication, technical, structure, ai_insights)
        
        # Generate weaknesses
        weaknesses = self._identify_weaknesses(dimensions, communication, technical, structure, ai_insights)
        
        # Generate suggestions with company and difficulty context
        suggestions = self._generate_suggestions(dimensions, communication, technical, structure, weaknesses, ai_insights, difficulty, company, category)
        
        # Generate next steps
        next_steps = self._generate_next_steps(overall_score, weaknesses, category, difficulty)
        
        # Add company-specific tips if company is provided
        company_tips = []
        if company:
            company_tips = self._generate_company_tips(company, category, dimensions, question)
        
        # Add ideal answer example if available from AI
        ideal_answer = None
        if ai_insights and "ideal_answer_example" in ai_insights:
            ideal_answer = ai_insights["ideal_answer_example"]
        
        feedback = {
            "overall_score": round(overall_score, 1),
            "level": level,
            "level_emoji": level_emoji,
            "difficulty": difficulty,
            "dimensions": {
                "technical_accuracy": round(dimensions["technical_accuracy"], 1),
                "communication": round(dimensions["communication_clarity"], 1),
                "problem_solving": round(dimensions["problem_solving"], 1),
                "completeness": round(dimensions["completeness"], 1),
                "depth": round(dimensions["depth"], 1)
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "next_steps": next_steps,
            "communication_analysis": communication,
            "technical_analysis": technical,
            "structure_analysis": structure,
            "completeness_analysis": completeness,
            "ai_insights": ai_insights,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add optional fields if available
        if company_tips:
            feedback["company_specific_tips"] = company_tips
        if ideal_answer:
            feedback["ideal_answer_example"] = ideal_answer
        if company:
            feedback["company"] = company
        
        return feedback
    
    def _identify_strengths(
        self,
        dimensions: Dict,
        communication: Dict,
        technical: Dict,
        structure: Dict,
        ai_insights: Optional[Dict]
    ) -> List[str]:
        """Identify specific strengths"""
        strengths = []
        
        # Use AI insights if available (they should be specific)
        if ai_insights and "strengths" in ai_insights and ai_insights["strengths"]:
            return ai_insights["strengths"][:5]
        
        # Dimension-based strengths (make them more specific)
        if dimensions["technical_accuracy"] >= 8.0:
            strengths.append("Demonstrated strong technical knowledge with accurate terminology")
        elif dimensions["technical_accuracy"] >= 6.5:
            strengths.append("Showed understanding of core technical concepts")
        
        if dimensions["communication_clarity"] >= 8.0:
            strengths.append("Communicated ideas clearly with good structure and flow")
        elif dimensions["communication_clarity"] >= 6.5:
            strengths.append("Explained concepts in an understandable way")
        
        if dimensions["problem_solving"] >= 8.0:
            strengths.append("Demonstrated strong analytical thinking and considered multiple approaches")
        elif dimensions["problem_solving"] >= 6.5:
            strengths.append("Showed problem-solving approach")
        
        if dimensions["depth"] >= 8.0:
            strengths.append("Provided in-depth explanations showing deep understanding")
        elif dimensions["depth"] >= 6.5:
            strengths.append("Went beyond surface-level explanation")
        
        # Communication-based strengths (more specific)
        if communication.get("has_examples"):
            strengths.append("Supported explanation with concrete examples")
        
        if communication.get("has_structure"):
            strengths.append("Organized answer with logical progression (first, then, finally)")
        
        # Technical-based strengths (more specific)
        if technical.get("has_code_example"):
            strengths.append("Included code examples to demonstrate implementation")
        
        if technical.get("mentions_trade_offs"):
            strengths.append("Discussed trade-offs between different approaches")
        
        if technical.get("mentions_alternatives"):
            strengths.append("Considered alternative solutions")
        
        # Structure-based strengths
        if structure.get("has_conclusion"):
            strengths.append("Concluded answer with summary of key points")
        
        return strengths[:5] if strengths else ["Provided a response to the question"]
    
    def _identify_weaknesses(
        self,
        dimensions: Dict,
        communication: Dict,
        technical: Dict,
        structure: Dict,
        ai_insights: Optional[Dict]
    ) -> List[str]:
        """Identify specific weaknesses"""
        weaknesses = []
        
        # Use AI insights if available (they should be specific)
        if ai_insights and "weaknesses" in ai_insights and ai_insights["weaknesses"]:
            return ai_insights["weaknesses"][:5]
        
        # Dimension-based weaknesses (make them more actionable)
        if dimensions["technical_accuracy"] < 5.0:
            weaknesses.append("Technical explanation needs improvement - review core concepts and terminology")
        elif dimensions["technical_accuracy"] < 6.5:
            weaknesses.append("Some technical details are missing or could be more accurate")
        
        if dimensions["communication_clarity"] < 5.0:
            weaknesses.append("Explanation is unclear - break down complex ideas into simpler parts")
        elif dimensions["communication_clarity"] < 6.5:
            weaknesses.append("Could communicate more clearly - use simpler language and better structure")
        
        if dimensions["completeness"] < 5.0:
            weaknesses.append("Answer is incomplete - address all parts of the question")
        elif dimensions["completeness"] < 6.5:
            weaknesses.append("Missing some key points that should be covered")
        
        if dimensions["depth"] < 5.0:
            weaknesses.append("Explanation is too surface-level - explain the 'why' and 'how', not just 'what'")
        elif dimensions["depth"] < 6.5:
            weaknesses.append("Could go deeper - add more details and reasoning")
        
        # Communication-based weaknesses (specific)
        word_count = communication.get("word_count", 0)
        if word_count < 20:
            weaknesses.append("Answer is too brief (under 20 words) - aim for 80-150 words with details and examples")
        elif word_count < 40:
            weaknesses.append("Answer needs more elaboration - add examples and explain your reasoning")
        
        if communication.get("filler_words", 0) > 8:
            weaknesses.append("Too many filler words (um, like, basically) - practice speaking more confidently")
        elif communication.get("filler_words", 0) > 5:
            weaknesses.append("Reduce filler words for more professional delivery")
        
        if not communication.get("has_examples") and word_count > 30:
            weaknesses.append("Missing concrete examples - add at least one specific example to illustrate your point")
        
        # Technical-based weaknesses (specific)
        if not technical.get("has_code_example") and dimensions["technical_accuracy"] < 7.0:
            weaknesses.append("Add code examples to demonstrate your understanding")
        
        if not technical.get("mentions_trade_offs") and dimensions["problem_solving"] < 7.0:
            weaknesses.append("Discuss pros/cons and when to use different approaches")
        
        if not technical.get("mentions_alternatives"):
            weaknesses.append("Consider mentioning alternative solutions or approaches")
        
        # Structure-based weaknesses (specific)
        if not structure.get("is_organized") and word_count > 40:
            weaknesses.append("Improve organization - use clear structure like 'First...Then...Finally' or 'Problem-Solution-Benefit'")
        
        if not structure.get("has_conclusion") and word_count > 60:
            weaknesses.append("Add a brief conclusion to summarize your key points")
        
        return weaknesses[:5] if weaknesses else []
    
    def _generate_suggestions(
        self,
        dimensions: Dict,
        communication: Dict,
        technical: Dict,
        structure: Dict,
        weaknesses: List[str],
        ai_insights: Optional[Dict],
        difficulty: str = "intermediate",
        company: str = "",
        category: str = ""
    ) -> List[str]:
        """Generate actionable suggestions with difficulty and company context"""
        suggestions = []
        
        # Use AI insights if available (they should be specific)
        if ai_insights and "suggestions" in ai_insights and ai_insights["suggestions"]:
            return ai_insights["suggestions"][:6]
        
        # Difficulty-specific suggestions
        if difficulty == "beginner":
            if dimensions["technical_accuracy"] < 6.0:
                suggestions.append("Start with the basics - make sure you understand core concepts before moving to advanced topics")
            if not communication.get("has_examples"):
                suggestions.append("Add simple, relatable examples - like comparing a stack to a pile of plates")
        elif difficulty == "advanced":
            if dimensions["depth"] < 7.0:
                suggestions.append("Go deeper - discuss implementation details, performance implications, and production considerations")
            if not technical.get("mentions_trade_offs"):
                suggestions.append("Analyze trade-offs comprehensively - discuss when to use each approach and why")
        
        # Generate specific suggestions based on weaknesses
        if dimensions["technical_accuracy"] < 6.0:
            suggestions.append("Study the fundamental concepts for this topic - create flashcards for key terms")
        elif dimensions["technical_accuracy"] < 7.5:
            suggestions.append("Review technical details - ensure you can explain concepts without looking them up")
        
        if dimensions["communication_clarity"] < 6.0:
            suggestions.append("Practice the 'Explain Like I'm 5' technique - simplify complex ideas into everyday language")
        elif dimensions["communication_clarity"] < 7.5:
            suggestions.append("Work on clarity - explain one concept at a time before moving to the next")
        
        if not communication.get("has_examples"):
            suggestions.append("Always include at least one concrete, specific example when explaining concepts")
        
        if not structure.get("is_organized"):
            suggestions.append("Use frameworks: STAR (Situation-Task-Action-Result) for behavioral, or Problem-Solution-Benefit for technical")
        
        if dimensions["depth"] < 6.5:
            suggestions.append("Go deeper - explain WHY things work this way, not just WHAT they are")
        
        if not technical.get("mentions_trade_offs"):
            suggestions.append("Discuss trade-offs: 'Approach A is better for X because..., but Approach B works better for Y because...'")
        
        if communication.get("word_count", 0) < 50:
            target_words = "50-100" if difficulty == "beginner" else "100-200" if difficulty == "intermediate" else "150-300"
            suggestions.append(f"Aim for {target_words} words - provide enough detail without rambling")
        
        if dimensions["problem_solving"] < 7.0:
            suggestions.append("Show your thinking process - explain how you'd approach solving this problem step-by-step")
        
        # Company-specific suggestions
        if company:
            company_suggestion = self._get_company_suggestion(company, category, dimensions)
            if company_suggestion:
                suggestions.append(company_suggestion)
        
        # General improvement suggestions
        suggestions.append("Practice with a timer - aim to answer in 2-3 minutes with complete thoughts")
        
        if dimensions["overall_score"] < 7.0:
            suggestions.append("Record yourself answering and review - identify filler words and unclear explanations")
        
        return suggestions[:7]
    
    def _generate_next_steps(
        self,
        overall_score: float,
        weaknesses: List[str],
        category: str,
        difficulty: str = "intermediate"
    ) -> List[str]:
        """Generate personalized next steps with difficulty awareness"""
        next_steps = []
        
        if overall_score < 6.0:
            next_steps.append(f"📚 Review {category} fundamentals - focus on core concepts")
            if difficulty == "beginner":
                next_steps.append("🎯 Practice 3-5 similar beginner questions this week")
                next_steps.append("📝 Write out answers before speaking to organize thoughts")
            else:
                next_steps.append("🎯 Practice 5-7 similar questions this week")
                next_steps.append("📝 Study example answers from top performers")
        elif overall_score < 8.0:
            next_steps.append("🔄 Practice this question again with improvements")
            next_steps.append("📊 Focus on weak areas identified above")
            next_steps.append("🎤 Record and review your answers")
            if difficulty == "advanced":
                next_steps.append("💡 Research production use cases and real-world examples")
        else:
            if difficulty == "beginner":
                next_steps.append("🌟 Great job! Try intermediate-level questions")
            elif difficulty == "intermediate":
                next_steps.append("🌟 Excellent! Move to advanced questions")
            else:
                next_steps.append("🌟 Outstanding! Help others or tackle system design challenges")
            next_steps.append("🎯 Practice explaining to others to solidify understanding")
            next_steps.append("📈 Challenge yourself with harder variations")
        
        return next_steps
    
    def _get_company_suggestion(self, company: str, category: str, dimensions: Dict) -> str:
        """Get company-specific suggestion"""
        suggestions = {
            "Google": "For Google interviews, emphasize scalability - explain how your solution handles billions of users",
            "Amazon": "For Amazon interviews, tie your answer to Leadership Principles like 'Customer Obsession' or 'Ownership'",
            "Microsoft": "For Microsoft interviews, show growth mindset - mention how you'd learn and adapt",
            "TCS": "For TCS interviews, focus on practical enterprise solutions and business value",
            "Infosys": "For Infosys interviews, connect technical solutions to digital transformation outcomes",
            "Wipro": "For Wipro interviews, emphasize innovation and client-centric problem-solving",
            "Cognizant": "For Cognizant interviews, discuss business impact and industry-specific applications",
            "Accenture": "For Accenture interviews, link technical decisions to strategic business outcomes",
            "Capgemini": "For Capgemini interviews, demonstrate both technical depth and engineering excellence"
        }
        return suggestions.get(company, "")
    
    def _generate_company_tips(self, company: str, category: str, dimensions: Dict, question: str) -> List[str]:
        """Generate company-specific tips"""
        tips = []
        
        # Add company-specific context
        company_tip = self._get_company_specific_tips(company, category)
        if company_tip:
            tips.append(f"💼 {company} Focus: {company_tip}")
        
        # Add category-specific company tips
        if "System Design" in category or "system" in question.lower():
            if company in ["Google", "Amazon", "Microsoft"]:
                tips.append(f"🏗️ For {company}: Discuss their cloud platform and services in your answer")
            elif company in ["TCS", "Infosys", "Wipro", "Cognizant", "Accenture", "Capgemini"]:
                tips.append(f"🏗️ For {company}: Focus on enterprise-scale solutions and client requirements")
        
        if "Behavioral" in category:
            if company == "Amazon":
                tips.append("📋 Amazon Tip: Structure answers using STAR and reference specific Leadership Principles")
            elif company == "Google":
                tips.append("📋 Google Tip: Show 'Googleyness' - collaboration, innovation, and user focus")
            elif company in ["TCS", "Infosys", "Wipro"]:
                tips.append(f"📋 {company} Tip: Emphasize teamwork, adaptability, and client satisfaction")
        
        return tips[:3]
    
    def _fallback_evaluation(self, question: str, answer: str) -> Dict:
        """Enhanced fallback evaluation with better scoring"""
        word_count = len(answer.split())
        answer_lower = answer.lower()
        
        # More sophisticated scoring based on multiple factors
        base_score = 3.0
        
        # Length scoring
        if word_count < 15:
            length_score = 1.0
            length_feedback = "Answer is too brief"
        elif word_count < 30:
            length_score = 3.0
            length_feedback = "Answer needs more detail"
        elif word_count < 60:
            length_score = 5.0
            length_feedback = "Decent length but could elaborate more"
        elif word_count < 150:
            length_score = 7.0
            length_feedback = "Good length and detail"
        elif word_count < 300:
            length_score = 8.0
            length_feedback = "Comprehensive answer"
        else:
            length_score = 7.0
            length_feedback = "Very detailed (ensure it's focused)"
        
        # Content quality indicators
        quality_score = 0
        strengths = []
        weaknesses = []
        
        # Check for examples
        if any(word in answer_lower for word in ["example", "for instance", "such as"]):
            quality_score += 1.0
            strengths.append("Provided examples to illustrate points")
        else:
            weaknesses.append("Add concrete examples to support your explanation")
        
        # Check for structure
        if any(word in answer_lower for word in ["first", "second", "then", "finally"]):
            quality_score += 0.8
            strengths.append("Used structured approach")
        else:
            weaknesses.append("Organize answer with clear structure (First, Then, Finally)")
        
        # Check for technical depth
        if any(word in answer_lower for word in ["because", "therefore", "this means"]):
            quality_score += 0.7
            strengths.append("Explained reasoning")
        else:
            weaknesses.append("Explain the 'why' behind your answer")
        
        # Check for code/technical content
        if "```" in answer or "def " in answer or "function " in answer:
            quality_score += 1.5
            strengths.append("Included code examples")
        
        # Calculate final score
        final_score = min(10.0, base_score + length_score * 0.5 + quality_score)
        
        # Determine level
        if final_score >= 8.5:
            level = "Excellent"
            level_emoji = "🌟"
        elif final_score >= 7.0:
            level = "Good"
            level_emoji = "✅"
        elif final_score >= 5.5:
            level = "Fair"
            level_emoji = "📊"
        else:
            level = "Needs Improvement"
            level_emoji = "📈"
        
        # Default strengths/weaknesses if none found
        if not strengths:
            strengths = ["Attempted to answer the question", "Provided a response"]
        
        if not weaknesses:
            weaknesses = ["Add more detail and examples", "Explain concepts more thoroughly"]
        
        # Generate suggestions
        suggestions = [
            "Practice explaining concepts in your own words",
            "Use the STAR method for behavioral questions (Situation, Task, Action, Result)",
            "Include specific examples from your experience",
            "Structure your answer with clear beginning, middle, and end"
        ]
        
        if word_count < 50:
            suggestions.insert(0, "Elaborate more - aim for 80-150 words for most answers")
        
        # Generate next steps
        if final_score < 6.0:
            next_steps = [
                "📚 Review fundamental concepts for this topic",
                "🎯 Practice 5 similar questions this week",
                "📝 Write out answers before speaking to organize thoughts"
            ]
        elif final_score < 8.0:
            next_steps = [
                "🔄 Practice this question again with improvements",
                "📊 Focus on adding more examples and details",
                "🎤 Record yourself to improve delivery"
            ]
        else:
            next_steps = [
                "🌟 Great job! Try more challenging questions",
                "🎯 Help others to solidify your understanding",
                "📈 Move to next difficulty level"
            ]
        
        return {
            "overall_score": round(final_score, 1),
            "level": level,
            "level_emoji": level_emoji,
            "dimensions": {
                "technical_accuracy": round(final_score, 1),
                "communication": round(length_score, 1),
                "problem_solving": round(final_score * 0.9, 1),
                "completeness": round(length_score * 0.8, 1),
                "depth": round(quality_score + 4.0, 1)
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "next_steps": next_steps,
            "note": "💡 Enable OpenAI API for detailed AI-powered feedback",
            "timestamp": datetime.utcnow().isoformat()
        }


# Global instance
_feedback_engine = None

def get_feedback_engine(openai_api_key: str = None) -> AdvancedFeedbackEngine:
    """Get or create global feedback engine"""
    global _feedback_engine
    if _feedback_engine is None:
        _feedback_engine = AdvancedFeedbackEngine(openai_api_key)
    return _feedback_engine
