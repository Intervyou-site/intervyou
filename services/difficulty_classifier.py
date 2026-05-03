"""
Difficulty Classifier for Interview Questions
Intelligently classifies questions into beginner, intermediate, and advanced levels
"""
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class DifficultyClassifier:
    """Classifies interview questions by difficulty level"""
    
    def __init__(self):
        # Keywords that indicate difficulty levels
        self.beginner_indicators = {
            # Basic concepts
            "what is", "define", "explain the difference between", "list", 
            "name", "basic", "simple", "introduction", "beginner",
            "fundamental", "overview", "describe",
            
            # Basic operations
            "how do you", "how to", "what are the types of",
            "give an example", "syntax", "declaration",
            
            # Common beginner topics
            "variable", "data type", "loop", "if statement", "function definition",
            "array", "string", "integer", "boolean"
        }
        
        self.intermediate_indicators = {
            # Practical application
            "implement", "create", "build", "design a simple",
            "how would you", "compare and contrast", "advantages and disadvantages",
            "when would you use", "best practices", "common use cases",
            
            # Intermediate concepts
            "class", "object", "inheritance", "polymorphism", "encapsulation",
            "exception handling", "file handling", "database connection",
            "api", "rest", "json", "xml", "testing",
            
            # Problem-solving
            "solve", "find", "calculate", "determine", "optimize",
            "debug", "fix", "improve", "refactor"
        }
        
        self.advanced_indicators = {
            # Complex concepts
            "architecture", "design pattern", "scalability", "performance",
            "distributed", "concurrent", "parallel", "asynchronous",
            "microservices", "system design", "trade-offs", "complexity analysis",
            
            # Advanced operations
            "optimize for", "scale to", "handle millions", "design for",
            "architect", "implement a production", "enterprise-level",
            
            # Deep technical
            "memory management", "garbage collection", "thread-safe",
            "race condition", "deadlock", "caching strategy",
            "load balancing", "sharding", "replication",
            
            # Advanced problem-solving
            "big o", "time complexity", "space complexity",
            "algorithm", "data structure design", "optimize performance"
        }
        
        # Category-specific difficulty mappings
        self.category_difficulty_map = {
            "Python": {
                "beginner": [
                    "What is Python?",
                    "What are Python data types?",
                    "How do you create a list in Python?",
                    "What is a variable in Python?",
                    "How do you write a for loop?",
                    "What is the difference between list and tuple?",
                    "How do you define a function?",
                    "What are Python comments?",
                    "How do you take user input?",
                    "What is string concatenation?"
                ],
                "intermediate": [
                    "What are Python decorators?",
                    "Explain list comprehensions.",
                    "How does exception handling work?",
                    "What are lambda functions?",
                    "Explain OOP concepts in Python.",
                    "What is the difference between @staticmethod and @classmethod?",
                    "How do you work with files in Python?",
                    "What are Python generators?",
                    "Explain the map, filter, and reduce functions.",
                    "How do you handle JSON data?"
                ],
                "advanced": [
                    "What is the Global Interpreter Lock (GIL)?",
                    "Explain Python's memory management and garbage collection.",
                    "What are metaclasses in Python?",
                    "How do you optimize Python code for performance?",
                    "Explain the difference between deep and shallow copy.",
                    "What are context managers and how do you create custom ones?",
                    "How does Python's asyncio work?",
                    "Explain Python's descriptor protocol.",
                    "What are Python's magic methods and dunder methods?",
                    "How do you implement a custom iterator?"
                ]
            },
            "Web Development": {
                "beginner": [
                    "What is HTML?",
                    "What is CSS?",
                    "What is JavaScript?",
                    "What is a web server?",
                    "What is HTTP?",
                    "What are HTML tags?",
                    "How do you create a link in HTML?",
                    "What is a CSS selector?",
                    "What is the DOM?",
                    "What is a variable in JavaScript?"
                ],
                "intermediate": [
                    "What is the difference between REST and GraphQL?",
                    "Explain how JWT authentication works.",
                    "What are the main differences between HTTP and HTTPS?",
                    "How does CORS work?",
                    "What is responsive web design?",
                    "Explain the MVC architecture pattern.",
                    "What are Progressive Web Apps?",
                    "How do you handle state management?",
                    "What is the difference between cookies and local storage?",
                    "How do you optimize website performance?"
                ],
                "advanced": [
                    "How would you design a scalable web application?",
                    "Explain microservices architecture.",
                    "How do you implement server-side rendering?",
                    "What are Web Workers and Service Workers?",
                    "How do you optimize for Core Web Vitals?",
                    "Explain the critical rendering path.",
                    "How do you implement real-time features with WebSockets?",
                    "What are the security best practices for web applications?",
                    "How do you handle millions of concurrent users?",
                    "Explain CDN and edge computing strategies."
                ]
            },
            "Data Structures": {
                "beginner": [
                    "What is an array?",
                    "What is a linked list?",
                    "What is a stack?",
                    "What is a queue?",
                    "What is the difference between array and linked list?",
                    "How do you implement a stack?",
                    "What is LIFO and FIFO?",
                    "What is a node in a linked list?",
                    "How do you access array elements?",
                    "What is array indexing?"
                ],
                "intermediate": [
                    "What is a hash table and how does it work?",
                    "Explain binary search tree.",
                    "What is the time complexity of common operations?",
                    "How do you detect a cycle in a linked list?",
                    "What is a heap data structure?",
                    "Explain BFS and DFS.",
                    "What is a trie?",
                    "How do you implement a queue using stacks?",
                    "What is a priority queue?",
                    "Explain the difference between tree and graph."
                ],
                "advanced": [
                    "How do you implement a LRU cache?",
                    "Explain self-balancing trees (AVL, Red-Black).",
                    "What is a B-tree and when would you use it?",
                    "How do you find the shortest path in a weighted graph?",
                    "Explain dynamic programming with examples.",
                    "What is amortized time complexity?",
                    "How do you implement a skip list?",
                    "Explain segment trees and their applications.",
                    "What is a Bloom filter?",
                    "How do you design a data structure for a specific problem?"
                ]
            },
            "System Design": {
                "beginner": [
                    "What is system design?",
                    "What is a client-server architecture?",
                    "What is a database?",
                    "What is an API?",
                    "What is a web server?",
                    "What is cloud computing?",
                    "What is scalability?",
                    "What is a load balancer?",
                    "What is caching?",
                    "What is a CDN?"
                ],
                "intermediate": [
                    "How would you design a URL shortener?",
                    "Explain load balancing strategies.",
                    "What is database sharding?",
                    "How would you design a rate limiter?",
                    "What is caching and what are common strategies?",
                    "How would you design a notification system?",
                    "Explain the CAP theorem.",
                    "What is database replication?",
                    "How do you handle session management?",
                    "What is horizontal vs vertical scaling?"
                ],
                "advanced": [
                    "How would you design Twitter/X?",
                    "How would you design Netflix?",
                    "How would you design Uber?",
                    "Explain distributed consensus algorithms.",
                    "How do you handle millions of concurrent users?",
                    "Design a global-scale messaging system.",
                    "How would you design a search engine?",
                    "Explain eventual consistency and strong consistency.",
                    "How do you design for fault tolerance?",
                    "Design a distributed file system like HDFS."
                ]
            },
            "Machine Learning": {
                "beginner": [
                    "What is machine learning?",
                    "What is supervised learning?",
                    "What is unsupervised learning?",
                    "What is a training set?",
                    "What is a test set?",
                    "What is a feature?",
                    "What is a label?",
                    "What is classification?",
                    "What is regression?",
                    "What is overfitting?"
                ],
                "intermediate": [
                    "Explain the bias-variance tradeoff.",
                    "What are ensemble methods?",
                    "How do you handle imbalanced datasets?",
                    "What is cross-validation?",
                    "Explain regularization techniques.",
                    "What is feature engineering?",
                    "How do you evaluate a classification model?",
                    "What is the difference between bagging and boosting?",
                    "Explain gradient descent.",
                    "What are hyperparameters?"
                ],
                "advanced": [
                    "Explain the mathematics behind neural networks.",
                    "How do you optimize deep learning models?",
                    "What is transfer learning and when would you use it?",
                    "Explain attention mechanisms in transformers.",
                    "How do you handle concept drift in production?",
                    "Design an ML system for real-time predictions.",
                    "Explain reinforcement learning algorithms.",
                    "How do you deploy ML models at scale?",
                    "What are the ethical considerations in ML?",
                    "How do you debug and interpret ML models?"
                ]
            },
            "Behavioral": {
                "beginner": [
                    "Tell me about yourself.",
                    "Why do you want this job?",
                    "What are your strengths?",
                    "What are your weaknesses?",
                    "Where do you see yourself in 5 years?",
                    "Why should we hire you?",
                    "What motivates you?",
                    "What is your greatest achievement?",
                    "How do you handle stress?",
                    "What are your hobbies?"
                ],
                "intermediate": [
                    "Describe a challenging project you worked on.",
                    "Tell me about a time you failed.",
                    "How do you handle conflicts in a team?",
                    "Describe a time you had to learn something quickly.",
                    "How do you prioritize tasks?",
                    "Tell me about a time you disagreed with your manager.",
                    "How do you handle feedback?",
                    "Describe a time you went above and beyond.",
                    "How do you stay updated with technology?",
                    "Tell me about a time you had to make a difficult decision."
                ],
                "advanced": [
                    "Describe a time you led a team through a crisis.",
                    "How would you handle a situation where your team is underperforming?",
                    "Tell me about a time you had to influence without authority.",
                    "Describe a complex technical decision you made and its impact.",
                    "How do you balance technical debt with feature development?",
                    "Tell me about a time you had to pivot a project mid-way.",
                    "How do you mentor junior developers?",
                    "Describe your approach to building team culture.",
                    "How do you handle stakeholder management?",
                    "Tell me about a time you had to make a trade-off decision."
                ]
            },
            "Aptitude": {
                "beginner": [
                    # Quantitative Aptitude - Beginner (20 questions)
                    "If a train travels 120 km in 2 hours, what is its average speed?",
                    "What is 15% of 200?",
                    "A product costs $80 after a 20% discount. What was the original price?",
                    "If 5 workers can complete a task in 12 days, how many days will 3 workers take?",
                    "What is the sum of first 10 natural numbers?",
                    "If a = 5 and b = 3, what is 2a + 3b?",
                    "What is the area of a rectangle with length 10 cm and width 5 cm?",
                    "If x + 5 = 12, what is x?",
                    "What is 25% of 80?",
                    "A car travels 60 km in 1 hour. How far will it travel in 3 hours?",
                    "What is the perimeter of a square with side 8 cm?",
                    "If 3x = 15, what is x?",
                    "What is the average of 10, 20, and 30?",
                    "A book costs $25. If you buy 4 books, how much do you pay?",
                    "What is 10% of 500?",
                    "If a dozen eggs cost $12, what is the cost of one egg?",
                    "What is the next number in the series: 2, 4, 6, 8, __?",
                    "If y - 7 = 10, what is y?",
                    "What is the product of 6 and 9?",
                    "A rectangle has length 12 m and width 8 m. What is its area?",
                    
                    # Logical Reasoning - Beginner (20 questions)
                    "If all roses are flowers and some flowers fade quickly, which statement is definitely true?",
                    "Complete the series: 2, 6, 12, 20, 30, __?",
                    "If CODING is written as DPEJOH, how is PYTHON written?",
                    "In a certain code, if FRIEND is 6 and FAMILY is 6, what is LOVE?",
                    "A is taller than B. C is shorter than B. D is taller than A. Who is the shortest?",
                    "If all cats are animals and some animals are pets, which is true?",
                    "What comes next: A, C, E, G, __?",
                    "If Monday is 2 days after Saturday, what day is tomorrow?",
                    "Which number doesn't belong: 2, 4, 6, 9, 10?",
                    "If North is up, what direction is opposite to East?",
                    "Complete: 1, 1, 2, 3, 5, 8, __?",
                    "If all birds can fly and penguins are birds, can penguins fly?",
                    "What is the next letter: B, D, F, H, __?",
                    "If today is Wednesday, what day was it 3 days ago?",
                    "Which shape is different: Circle, Square, Triangle, Rectangle?",
                    "If A = 1, B = 2, C = 3, what is CAB?",
                    "Complete the pattern: 5, 10, 15, 20, __?",
                    "If all students study and John is a student, does John study?",
                    "What comes after: Red, Orange, Yellow, Green, __?",
                    "If 2 + 2 = 4, what is 3 + 3?",
                    
                    # Data Interpretation - Beginner (10 questions)
                    "A pie chart shows: Sales A=40%, B=30%, C=20%, D=10%. If total sales = $10,000, what is B's sales?",
                    "A bar graph shows monthly sales: Jan=50, Feb=60, Mar=55, Apr=70. What is the average?",
                    "If revenue increased from $500 to $650, what is the percentage increase?",
                    "A table shows: Product A sold 100 units, Product B sold 150 units. What is the total?",
                    "If 60% of students passed and there are 200 students, how many passed?",
                    "A graph shows temperature: Mon=20°C, Tue=22°C, Wed=21°C. What is the average?",
                    "If a company's profit is $50,000 and expenses are $30,000, what is the revenue?",
                    "A chart shows: Q1=100, Q2=120, Q3=110, Q4=130. What is the total for the year?",
                    "If 25% of employees work remotely and there are 400 employees, how many work remotely?",
                    "A pie chart shows market share: Company A=50%, Company B=30%, Company C=20%. If total market is $1M, what is Company A's share?"
                ],
                "intermediate": [
                    # Quantitative Aptitude - Intermediate (25 questions)
                    "The ratio of ages of A and B is 3:5. If B is 10 years older than A, what is A's age?",
                    "A train 100m long crosses a platform 200m long in 15 seconds. What is the speed of the train?",
                    "If the compound interest on $1000 for 2 years at 10% per annum is $210, what is the principal?",
                    "A mixture contains milk and water in ratio 4:1. If 5 liters of water is added, the ratio becomes 4:3. Find the original quantity.",
                    "Two pipes can fill a tank in 10 and 15 hours respectively. If both pipes are opened together, how long will it take?",
                    "A shopkeeper marks his goods 40% above cost price and gives a 20% discount. What is his profit percentage?",
                    "If the average of 5 numbers is 20 and one number is 30, what is the sum of the other 4?",
                    "A person invests $5000 at 8% simple interest. How much will he have after 3 years?",
                    "The sum of three consecutive integers is 72. What is the largest integer?",
                    "A car travels from A to B at 60 km/h and returns at 40 km/h. What is the average speed?",
                    "If 12 men can complete a work in 15 days, how many men are needed to complete it in 10 days?",
                    "A number is increased by 20% and then decreased by 20%. What is the net change?",
                    "The diagonal of a square is 10√2 cm. What is the area of the square?",
                    "If x:y = 2:3 and y:z = 4:5, what is x:z?",
                    "A sum of money doubles itself in 8 years at simple interest. What is the rate of interest?",
                    "The average age of 30 students is 15 years. If the teacher's age is included, the average becomes 16 years. What is the teacher's age?",
                    "A boat travels 30 km upstream in 6 hours and 30 km downstream in 3 hours. What is the speed of the stream?",
                    "If the cost price of 12 articles equals the selling price of 10 articles, what is the profit percentage?",
                    "A number when divided by 5 leaves remainder 3. What is the remainder when the square of the number is divided by 5?",
                    "The ratio of boys to girls in a class is 3:2. If there are 15 boys, how many girls are there?",
                    "A person covers a distance of 240 km in 4 hours partly by car at 70 km/h and partly by train at 50 km/h. Find the distance covered by car.",
                    "If a:b = 2:3 and b:c = 4:5, find a:b:c.",
                    "The price of a commodity increases by 25%. By what percentage should consumption be reduced so that expenditure remains the same?",
                    "A sum of $8000 is divided among A, B, and C in the ratio 2:3:5. What is C's share?",
                    "If 15% of x is equal to 20% of y, what is the ratio x:y?",
                    
                    # Logical Reasoning - Intermediate (15 questions)
                    "In a certain code, COMPUTER is written as RFUVQNPC. How is MEDICINE written?",
                    "If in a code language, RAIN is written as 8$%6 and MORE is written as 7#8@, how is REMAIN written?",
                    "A clock shows 3:15. What is the angle between the hour and minute hands?",
                    "If the day before yesterday was Thursday, what day will it be the day after tomorrow?",
                    "In a row of students, A is 7th from the left and B is 9th from the right. If they interchange positions, A becomes 11th from the left. How many students are there?",
                    "If PALE is coded as 2134 and EARTH is coded as 41590, how is PEARL coded?",
                    "A is the father of B. C is the daughter of B. D is the brother of B. What is the relationship between A and D?",
                    "If '+' means '×', '×' means '-', '-' means '÷', and '÷' means '+', what is 8 + 2 - 4 × 3 ÷ 6?",
                    "In a certain code, if ROSE is 6821 and CHAIR is 73456, what is SEARCH?",
                    "A man pointing to a photograph says, 'The lady in the photograph is my nephew's maternal grandmother.' How is the lady related to the man's sister?",
                    "If South-East becomes North and North-East becomes West, what does South become?",
                    "In a class, Ravi is 10th from the top and 25th from the bottom. How many students are in the class?",
                    "If MISTAKE is coded as 9765412 and NAKED is coded as 84123, how is DISTANT coded?",
                    "A, B, C, D, and E are sitting in a row. A is to the left of B. C is to the right of B but left of D. E is to the right of D. Who is in the middle?",
                    "If the positions of the first and sixth letters of the word CONTAGIOUS are interchanged, similarly the positions of the second and seventh are interchanged, and so on, which letter will be the fourth from the right end?",
                    
                    # Data Interpretation - Intermediate (10 questions)
                    "A company's revenue for 4 quarters: Q1=$200k, Q2=$250k, Q3=$300k, Q4=$350k. What is the percentage growth from Q1 to Q4?",
                    "A bar chart shows sales: Product A=40%, Product B=30%, Product C=20%, Product D=10%. If Product A sales are $80,000, what is the total sales?",
                    "A line graph shows monthly expenses: Jan=$5k, Feb=$6k, Mar=$5.5k, Apr=$7k. What is the average monthly expense?",
                    "A table shows: Revenue=$500k, Cost of Goods=$300k, Operating Expenses=$100k. What is the profit margin percentage?",
                    "A pie chart shows budget allocation: Marketing=30%, R&D=25%, Operations=35%, Admin=10%. If total budget is $2M, how much is allocated to R&D?",
                    "A graph shows user growth: Month 1=1000, Month 2=1500, Month 3=2250. If this pattern continues, what will be Month 4?",
                    "A table shows: Product A sold 500 units at $20 each, Product B sold 300 units at $30 each. What is the total revenue?",
                    "A chart shows employee distribution: Engineering=40%, Sales=25%, Marketing=20%, HR=15%. If there are 80 engineers, how many total employees?",
                    "A graph shows quarterly profit: Q1=$50k, Q2=$60k, Q3=$55k, Q4=$70k. What is the average quarterly profit?",
                    "A table shows conversion rates: Week 1=5%, Week 2=6%, Week 3=5.5%, Week 4=7%. What is the average conversion rate?"
                ],
                "advanced": [
                    # Quantitative Aptitude - Advanced (25 questions)
                    "A train 150m long passes a platform 250m long in 20 seconds. Another train 200m long traveling in opposite direction passes the first train in 10 seconds. Find the speed of the second train.",
                    "The compound interest on a sum for 2 years at 10% per annum is $420. What is the simple interest on the same sum for the same period at the same rate?",
                    "A mixture of 40 liters contains milk and water in ratio 3:1. How much water should be added to make the ratio 2:1?",
                    "Three pipes A, B, and C can fill a tank in 6, 8, and 12 hours respectively. If all three are opened together, in how many hours will the tank be filled?",
                    "A shopkeeper marks his goods 50% above cost price. He gives a discount of 20% on marked price and still makes a profit of $120. What is the cost price?",
                    "The average of 10 numbers is 40. If two numbers 45 and 55 are removed, what is the new average?",
                    "A person invests $10,000 partly at 8% and partly at 10% simple interest. If the total interest after 1 year is $920, how much was invested at 10%?",
                    "The sum of three numbers in AP is 27 and their product is 504. Find the numbers.",
                    "A car travels from A to B at 60 km/h, B to C at 80 km/h, and C to A at 40 km/h. If AB = BC = CA, what is the average speed for the entire journey?",
                    "If 15 men can complete a work in 20 days working 8 hours a day, how many days will 20 men take working 6 hours a day?",
                    "A number is increased by 20%, then decreased by 20%, then increased by 20%. What is the net percentage change?",
                    "The diagonal of a rectangle is 13 cm and its perimeter is 34 cm. Find the area.",
                    "If a:b = 2:3, b:c = 4:5, and c:d = 6:7, find a:d.",
                    "A sum of money at compound interest amounts to $6,050 in 1 year and $6,655 in 2 years. What is the rate of interest?",
                    "The average age of a family of 5 members is 24 years. If the age of the youngest member is 8 years, what was the average age of the family at the birth of the youngest member?",
                    "A boat travels 48 km upstream in 8 hours and 72 km downstream in 6 hours. Find the speed of the boat in still water and the speed of the stream.",
                    "If the cost price of 15 articles equals the selling price of 12 articles, and the shopkeeper gives a 10% discount on marked price, what is the markup percentage?",
                    "A number when divided by 7 leaves remainder 4. What is the remainder when the cube of the number is divided by 7?",
                    "The ratio of boys to girls in a class is 5:3. If 8 boys leave and 4 girls join, the ratio becomes 1:1. Find the original number of students.",
                    "A person covers a distance of 360 km in 6 hours partly by car at 70 km/h, partly by train at 50 km/h, and partly by bus at 40 km/h. If the distance covered by car is twice the distance covered by bus, find the distance covered by train.",
                    "If a:b:c = 2:3:5 and a² + b² + c² = 380, find the value of a + b + c.",
                    "The price of a commodity increases by 30%. By what percentage should consumption be reduced so that expenditure increases by only 10%?",
                    "A sum of $15,000 is divided among A, B, and C such that A gets 2/3 of what B gets and B gets 3/4 of what C gets. Find A's share.",
                    "If 20% of a = 30% of b and 40% of b = 50% of c, what is the ratio a:b:c?",
                    "A cistern has two pipes. One can fill it in 10 hours and the other can empty it in 15 hours. If both pipes are opened when the cistern is half full, how long will it take to fill it completely?",
                    
                    # Logical Reasoning - Advanced (15 questions)
                    "In a certain code language, if ALGORITHM is written as ZOTLIRGSN, how is PROGRAMMING written?",
                    "A clock loses 10 minutes every hour. If it is set correctly at 12 noon, what time will it show when the actual time is 6 PM?",
                    "In a row of 40 students, A is 16th from the left and B is 18th from the right. How many students are there between A and B?",
                    "If PALE is coded as 2134, EARTH is coded as 41590, and PEARL is coded as 24153, how is LEATHER coded?",
                    "A is the son of B. C, B's sister, has a son D and a daughter E. F is the maternal uncle of D. How is F related to A?",
                    "If '+' means '÷', '×' means '+', '-' means '×', and '÷' means '-', what is the value of 16 + 4 × 5 - 2 ÷ 3?",
                    "In a certain code, if ROSE is 6821, CHAIR is 73456, and SEARCH is 214573, what is ORCHESTRA?",
                    "A man pointing to a photograph says, 'The lady in the photograph is the daughter of my grandmother's only son.' How is the lady related to the man?",
                    "If North-East becomes West, North-West becomes South-West, and South-East becomes North, what does South-West become?",
                    "In a class of 60 students, Ravi is 15th from the top in Math and 20th from the bottom in Science. If 5 students are between Ravi's positions in Math and Science, how many students are there who scored better than Ravi in both subjects?",
                    "If MISTAKE is coded as 9765412, NAKED is coded as 84123, and DISTANT is coded as 3765485, how is STAIN coded?",
                    "Six people A, B, C, D, E, and F are sitting in a circle facing the center. A is to the immediate left of D. B is opposite to F. C is between A and B. Who is to the immediate right of F?",
                    "If the positions of the first and last letters of the word CONTAGIOUS are interchanged, similarly the positions of the second and second-last are interchanged, and so on, which letter will be the fifth from the left end?",
                    "In a certain code, if COMPUTER is written as PMOCTUER, how is KEYBOARD written?",
                    "A, B, C, D, E, F, G, and H are sitting around a circular table facing the center. A is third to the right of H, who is second to the right of D. C is second to the left of A and is not a neighbor of D. F is not a neighbor of D. B is second to the left of E. Who is to the immediate right of A?",
                    
                    # Data Interpretation - Advanced (10 questions)
                    "A company's quarterly revenues are: Q1=$500k, Q2=$625k, Q3=$781k, Q4=$976k. What is the compound quarterly growth rate?",
                    "A multi-line graph shows sales of 3 products over 4 quarters. Product A: Q1=100, Q2=120, Q3=110, Q4=140. Product B: Q1=80, Q2=90, Q3=100, Q4=110. Product C: Q1=60, Q2=70, Q3=80, Q4=90. Which product has the highest growth rate?",
                    "A table shows: Revenue=$2M, COGS=$1.2M, Operating Expenses=$500k, Interest=$100k, Taxes=$80k. What is the net profit margin?",
                    "A stacked bar chart shows monthly expenses: Rent=$5k, Salaries=$20k, Marketing=$8k, Utilities=$2k. If rent increases by 20%, salaries by 10%, and marketing by 15%, what is the new total monthly expense?",
                    "A pie chart shows investment portfolio: Stocks=40%, Bonds=30%, Real Estate=20%, Cash=10%. If stocks appreciate by 25%, bonds by 5%, real estate by 10%, and cash remains same, what is the new portfolio composition?",
                    "A graph shows exponential user growth: Month 1=1000, Month 2=1500, Month 3=2250, Month 4=3375. What is the monthly growth rate?",
                    "A table shows: Product A sold 1000 units at $50 with 20% margin, Product B sold 500 units at $100 with 30% margin. What is the weighted average margin?",
                    "A chart shows employee attrition: Q1=5%, Q2=6%, Q3=7%, Q4=8%. If the company has 1000 employees at the start of Q1, how many employees remain at the end of Q4?",
                    "A graph shows quarterly profit margins: Q1=15%, Q2=18%, Q3=16%, Q4=20%. If Q4 revenue is $1M, what is the average quarterly profit assuming revenue grows 10% each quarter?",
                    "A complex table shows conversion funnel: Visitors=10,000, Sign-ups=2,000, Trials=1,000, Paid=300. If marketing spend is $50,000, what is the customer acquisition cost?"
                ]
            }
        }
    
    def classify_question(self, question: str, category: str = None) -> str:
        """
        Classify a question into beginner, intermediate, or advanced
        
        Args:
            question: The question text
            category: Optional category for context
        
        Returns:
            "beginner", "intermediate", or "advanced"
        """
        question_lower = question.lower()
        
        # Check category-specific mappings first
        if category and category in self.category_difficulty_map:
            for level, questions in self.category_difficulty_map[category].items():
                for q in questions:
                    if self._similarity(question_lower, q.lower()) > 0.7:
                        return level
        
        # Count indicators for each level
        beginner_score = sum(1 for indicator in self.beginner_indicators if indicator in question_lower)
        intermediate_score = sum(1 for indicator in self.intermediate_indicators if indicator in question_lower)
        advanced_score = sum(1 for indicator in self.advanced_indicators if indicator in question_lower)
        
        # Additional heuristics
        word_count = len(question.split())
        has_technical_terms = any(term in question_lower for term in [
            "algorithm", "complexity", "optimize", "scale", "architecture",
            "distributed", "concurrent", "performance"
        ])
        
        # Adjust scores based on heuristics
        if word_count > 20:
            advanced_score += 1
        if has_technical_terms:
            advanced_score += 2
        
        # Determine difficulty
        scores = {
            "beginner": beginner_score,
            "intermediate": intermediate_score,
            "advanced": advanced_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            # Default to intermediate if no clear indicators
            return "intermediate"
        
        # Return the level with highest score
        for level, score in scores.items():
            if score == max_score:
                return level
        
        return "intermediate"
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Calculate simple similarity between two strings"""
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def get_questions_by_difficulty(
        self, 
        category: str, 
        difficulty: str,
        count: int = 10
    ) -> List[str]:
        """Get questions for a specific difficulty level"""
        logger.info(f"🔎 get_questions_by_difficulty called: category='{category}', difficulty='{difficulty}', count={count}")
        logger.info(f"📚 Available categories: {list(self.category_difficulty_map.keys())}")
        
        if category in self.category_difficulty_map:
            questions = self.category_difficulty_map[category].get(difficulty, [])
            logger.info(f"✅ Found {len(questions)} questions for {category}/{difficulty}")
            if questions:
                logger.info(f"📋 First question: {questions[0][:80]}...")
            return questions[:count]
        else:
            logger.warning(f"⚠️ Category '{category}' not found in difficulty map!")
        return []
    
    def classify_batch(
        self, 
        questions: List[str], 
        category: str = None
    ) -> Dict[str, List[str]]:
        """Classify a batch of questions"""
        classified = {
            "beginner": [],
            "intermediate": [],
            "advanced": []
        }
        
        for question in questions:
            difficulty = self.classify_question(question, category)
            classified[difficulty].append(question)
        
        return classified


# Global instance
_classifier = None

def get_difficulty_classifier() -> DifficultyClassifier:
    """Get or create the global difficulty classifier"""
    global _classifier
    if _classifier is None:
        _classifier = DifficultyClassifier()
    return _classifier
