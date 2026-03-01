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
        Comprehensive answer evaluation
        
        Returns:
            Dict with detailed feedback including:
            - Overall score (0-10)
            - Dimension scores (technical, communication, structure, completeness)
            - Strengths (what was done well)
            - Weaknesses (areas to improve)
            - Specific suggestions (actionable items)
            - Ideal answer comparison
            - Next steps
        """
        try:
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
            
            # Generate AI-powered insights (if API available)
            ai_insights = await self._get_ai_insights(question, answer, category, difficulty)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(dimensions, communication, technical, structure, completeness)
            
            # Generate actionable feedback
            feedback = self._generate_feedback(
                overall_score=overall_score,
                dimensions=dimensions,
                communication=communication,
                technical=technical,
                structure=structure,
                completeness=completeness,
                ai_insights=ai_insights,
                category=category
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
        difficulty: str
    ) -> Optional[Dict]:
        """Get AI-powered insights using OpenAI with enhanced prompts"""
        if not self.openai_api_key:
            return None
        
        try:
            prompt = f"""You are an expert technical interviewer and career coach with 15+ years of experience at top tech companies (Google, Amazon, Microsoft). Analyze this interview answer with the rigor of a senior interviewer.

**Question:** {question}
**Category:** {category}
**Difficulty:** {difficulty}
**Candidate's Answer:** {answer}

Provide detailed, actionable feedback in JSON format:

{{
  "strengths": [
    "List 3-5 SPECIFIC things done well (be precise, not generic)",
    "Focus on technical accuracy, communication clarity, problem-solving approach",
    "Mention specific phrases or concepts the candidate used well"
  ],
  "weaknesses": [
    "List 3-5 SPECIFIC areas to improve (be constructive but honest)",
    "Point out missing concepts, unclear explanations, or gaps in logic",
    "Identify what a senior engineer would expect that's missing"
  ],
  "suggestions": [
    "Provide 4-6 ACTIONABLE improvement suggestions",
    "Be specific: 'Add X', 'Explain Y in more detail', 'Consider Z'",
    "Include both immediate fixes and long-term learning recommendations"
  ],
  "ideal_answer_outline": "Brief 3-4 sentence outline of what an excellent answer would cover",
  "missing_elements": [
    "List 2-4 key concepts or points that should have been mentioned",
    "Focus on what would make this answer go from good to excellent"
  ],
  "score_justification": "2-3 sentences explaining why this answer deserves its score, referencing specific strengths and weaknesses"
}}

**Evaluation Criteria:**
- Technical Accuracy: Correct terminology, concepts, and explanations
- Completeness: Addresses all parts of the question
- Depth: Goes beyond surface-level, shows deep understanding
- Communication: Clear, structured, easy to follow
- Problem-Solving: Shows analytical thinking, considers trade-offs

Be honest but encouraging. Focus on growth, not criticism."""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a senior technical interviewer providing detailed, actionable feedback. Be specific, honest, and constructive. Focus on helping candidates improve."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
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
        completeness: Dict
    ) -> float:
        """Calculate weighted overall score"""
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
        category: str
    ) -> Dict:
        """Generate comprehensive feedback"""
        
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
        
        # Generate suggestions
        suggestions = self._generate_suggestions(dimensions, communication, technical, structure, weaknesses, ai_insights)
        
        # Generate next steps
        next_steps = self._generate_next_steps(overall_score, weaknesses, category)
        
        return {
            "overall_score": round(overall_score, 1),
            "level": level,
            "level_emoji": level_emoji,
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
        
        # Use AI insights if available
        if ai_insights and "strengths" in ai_insights:
            return ai_insights["strengths"][:5]
        
        # Dimension-based strengths
        if dimensions["technical_accuracy"] >= 8.0:
            strengths.append("Strong technical accuracy and correct use of terminology")
        
        if dimensions["communication_clarity"] >= 8.0:
            strengths.append("Clear and well-structured communication")
        
        if dimensions["problem_solving"] >= 8.0:
            strengths.append("Excellent problem-solving approach with consideration of alternatives")
        
        if dimensions["depth"] >= 8.0:
            strengths.append("Deep understanding demonstrated with detailed explanations")
        
        # Communication-based strengths
        if communication.get("has_examples"):
            strengths.append("Good use of examples to illustrate points")
        
        if communication.get("has_structure"):
            strengths.append("Well-organized answer with logical flow")
        
        # Technical-based strengths
        if technical.get("has_code_example"):
            strengths.append("Provided concrete code examples")
        
        if technical.get("mentions_trade_offs"):
            strengths.append("Considered trade-offs and different approaches")
        
        # Structure-based strengths
        if structure.get("is_organized"):
            strengths.append("Structured answer with clear progression")
        
        return strengths[:5] if strengths else ["Attempted to answer the question"]
    
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
        
        # Use AI insights if available
        if ai_insights and "weaknesses" in ai_insights:
            return ai_insights["weaknesses"][:5]
        
        # Dimension-based weaknesses
        if dimensions["technical_accuracy"] < 6.0:
            weaknesses.append("Technical accuracy could be improved - review key concepts")
        
        if dimensions["communication_clarity"] < 6.0:
            weaknesses.append("Communication clarity needs work - practice explaining concepts simply")
        
        if dimensions["completeness"] < 6.0:
            weaknesses.append("Answer incomplete - address all parts of the question")
        
        if dimensions["depth"] < 6.0:
            weaknesses.append("Lacks depth - provide more detailed explanations")
        
        # Communication-based weaknesses
        if communication.get("word_count", 0) < 30:
            weaknesses.append("Answer too brief - elaborate more on your points")
        
        if communication.get("filler_words", 0) > 5:
            weaknesses.append("Reduce filler words (um, like, basically) for more professional delivery")
        
        if not communication.get("has_examples"):
            weaknesses.append("Add concrete examples to support your explanations")
        
        # Technical-based weaknesses
        if not technical.get("has_code_example") and dimensions["technical_accuracy"] < 7.0:
            weaknesses.append("Include code examples to demonstrate understanding")
        
        if not technical.get("mentions_trade_offs"):
            weaknesses.append("Discuss trade-offs and alternative approaches")
        
        # Structure-based weaknesses
        if not structure.get("is_organized"):
            weaknesses.append("Improve organization - use structured approach (e.g., First, Then, Finally)")
        
        return weaknesses[:5] if weaknesses else []
    
    def _generate_suggestions(
        self,
        dimensions: Dict,
        communication: Dict,
        technical: Dict,
        structure: Dict,
        weaknesses: List[str],
        ai_insights: Optional[Dict]
    ) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []
        
        # Use AI insights if available
        if ai_insights and "suggestions" in ai_insights:
            return ai_insights["suggestions"][:5]
        
        # Based on weaknesses
        if dimensions["technical_accuracy"] < 7.0:
            suggestions.append("Review fundamental concepts and practice explaining them in your own words")
        
        if dimensions["communication_clarity"] < 7.0:
            suggestions.append("Practice the 'Explain Like I'm 5' technique - simplify complex ideas")
        
        if not communication.get("has_examples"):
            suggestions.append("Always include at least one concrete example when explaining concepts")
        
        if not structure.get("is_organized"):
            suggestions.append("Use frameworks like 'Situation-Action-Result' or 'Problem-Solution-Benefit'")
        
        if dimensions["depth"] < 7.0:
            suggestions.append("Go deeper - explain the 'why' behind concepts, not just the 'what'")
        
        if not technical.get("mentions_trade_offs"):
            suggestions.append("Discuss pros/cons and when to use different approaches")
        
        # General suggestions
        suggestions.append("Practice with a timer to improve pacing and completeness")
        suggestions.append("Record yourself and review to identify areas for improvement")
        
        return suggestions[:6]
    
    def _generate_next_steps(
        self,
        overall_score: float,
        weaknesses: List[str],
        category: str
    ) -> List[str]:
        """Generate personalized next steps"""
        next_steps = []
        
        if overall_score < 6.0:
            next_steps.append(f"📚 Review {category} fundamentals - focus on core concepts")
            next_steps.append("🎯 Practice 5 similar questions this week")
            next_steps.append("📝 Write out answers before speaking to organize thoughts")
        elif overall_score < 8.0:
            next_steps.append("🔄 Practice this question again with improvements")
            next_steps.append("📊 Focus on weak areas identified above")
            next_steps.append("🎤 Record and review your answers")
        else:
            next_steps.append("🌟 Great job! Try more advanced questions")
            next_steps.append("🎯 Practice explaining to others to solidify understanding")
            next_steps.append("📈 Move to next difficulty level")
        
        return next_steps
    
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
