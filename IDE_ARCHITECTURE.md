# 🏗️ AI-Powered IDE - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │         Monaco Editor (Code Editor)                 │     │
│  │  - Syntax highlighting                              │     │
│  │  - IntelliSense                                     │     │
│  │  - Multi-language support                           │     │
│  └────────────────────────────────────────────────────┘     │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │         IDE Frontend (ide.js)                       │     │
│  │  - Event handling                                   │     │
│  │  - API communication                                │     │
│  │  - UI updates                                       │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │         IDE Routes (ide_routes.py)                  │     │
│  │  - /ide/execute                                     │     │
│  │  - /ide/analyze                                     │     │
│  │  - /ide/challenges                                  │     │
│  └────────────────────────────────────────────────────┘     │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │      Code Executor (code_executor.py)               │     │
│  │  - Execution engine                                 │     │
│  │  - Docker/Local execution                           │     │
│  │  - AI integration                                   │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Docker     │    │  LLM (AI)    │    │  Language    │
│  Containers  │    │  Analysis    │    │  Configs     │
│              │    │              │    │              │
│ - Python     │    │ - OpenAI     │    │ - Templates  │
│ - Node.js    │    │ - Groq       │    │ - Errors     │
│ - Java       │    │ - Error      │    │ - Challenges │
│ - GCC        │    │   explain    │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Component Details

### 1. Frontend Layer

#### Monaco Editor
- **Purpose**: Rich code editing experience
- **Features**: 
  - Syntax highlighting
  - Auto-completion
  - Error underlining
  - Multi-cursor editing
- **Source**: Microsoft CDN
- **Languages**: Python, JS, Java, C++, C

#### IDE Frontend (ide.js)
- **Purpose**: User interaction and API communication
- **Responsibilities**:
  - Handle user actions (run, analyze, etc.)
  - Send code to backend
  - Display results
  - Manage tabs (Output, AI Help, Analysis)
  - Update statistics

### 2. Backend Layer

#### FastAPI Routes (ide_routes.py)
```python
Router: /ide
├── GET  /languages          # List supported languages
├── POST /execute            # Execute code
├── POST /analyze            # Analyze code quality
├── GET  /challenges         # Get all challenges
├── GET  /challenges/{id}    # Get specific challenge
└── GET  /template/{lang}    # Get language template
```

#### Code Executor (code_executor.py)
**Main Class**: `CodeExecutor`

**Methods**:
- `execute_code()` - Main execution entry point
- `_execute_in_docker()` - Docker-based execution
- `_execute_locally()` - Local fallback execution
- `_get_ai_error_explanation()` - AI error analysis
- `analyze_code_quality()` - Code quality scoring

### 3. Execution Layer

#### Docker Execution Flow
```
1. Create temp file with user code
2. Mount temp directory to container
3. Compile (if needed)
4. Run with timeout and memory limits
5. Capture output/errors
6. Clean up
```

**Security Features**:
- Isolated containers
- No network access (`--network=none`)
- Memory limits (128-256MB)
- Time limits (10-15s)
- Read-only mounts where possible

#### Local Execution Flow
```
1. Create temp file with user code
2. Run subprocess with timeout
3. Capture output/errors
4. Clean up temp files
```

**Security Features**:
- Subprocess isolation
- Timeout enforcement
- No shell injection (parameterized commands)

### 4. AI Analysis Layer

#### Error Explanation Flow
```
User Code → Error
    ↓
Check Common Errors (Quick Hint)
    ↓
Send to LLM:
  - Code
  - Error message
  - Language context
    ↓
LLM Response:
  - What went wrong
  - Problem location
  - How to fix
  - Pro tip
    ↓
Display to User
```

#### Code Quality Analysis Flow
```
User Code
    ↓
Send to LLM:
  - Code
  - Language
    ↓
LLM Response:
  - Quality score (1-10)
  - Strengths (2)
  - Improvements (2)
  - Performance tip
    ↓
Display to User
```

## Data Flow

### Execute Code Request
```
Browser                Backend              Docker/Local         LLM
   |                      |                      |                |
   |--POST /execute------>|                      |                |
   |  {code, lang}        |                      |                |
   |                      |--Create temp file--->|                |
   |                      |                      |                |
   |                      |--Execute------------>|                |
   |                      |                      |                |
   |                      |<--Output/Error-------|                |
   |                      |                      |                |
   |                      |--Analyze error-------|--------------->|
   |                      |                      |                |
   |                      |<--Explanation--------|----------------|
   |                      |                      |                |
   |<--Response-----------|                      |                |
   |  {output, ai_help}   |                      |                |
```

### Analyze Code Request
```
Browser                Backend              LLM
   |                      |                  |
   |--POST /analyze------>|                  |
   |  {code, lang}        |                  |
   |                      |--Analyze-------->|
   |                      |                  |
   |                      |<--Analysis-------|
   |                      |                  |
   |<--Response-----------|                  |
   |  {score, tips}       |                  |
```

## File Structure

```
online_ide/
├── __init__.py
│   └── Module exports
│
├── code_executor.py
│   ├── CodeExecutor class
│   ├── execute_code()
│   ├── _execute_in_docker()
│   ├── _execute_locally()
│   ├── _get_ai_error_explanation()
│   └── analyze_code_quality()
│
├── language_configs.py
│   ├── LANGUAGE_CONFIGS dict
│   │   ├── Python config
│   │   ├── JavaScript config
│   │   ├── Java config
│   │   ├── C++ config
│   │   └── C config
│   └── CODING_CHALLENGES list
│
└── ide_routes.py
    ├── GET /languages
    ├── POST /execute
    ├── POST /analyze
    ├── GET /challenges
    ├── GET /challenges/{id}
    └── GET /template/{lang}

templates/
└── ide.html
    ├── Header
    ├── Sidebar (languages, challenges, stats)
    ├── Editor area (Monaco)
    ├── Input section
    └── Output panel (tabs)

static/
├── ide.js
│   ├── Monaco initialization
│   ├── Event handlers
│   ├── API calls
│   └── UI updates
│
└── ide.css
    ├── Layout styles
    ├── Dark theme
    ├── Component styles
    └── Responsive design
```

## Security Architecture

### Defense Layers

```
Layer 1: Input Validation
├── Code length limits
├── Language verification
└── Input sanitization

Layer 2: Execution Isolation
├── Docker containers (preferred)
│   ├── No network access
│   ├── Memory limits
│   ├── Time limits
│   └── Isolated filesystem
└── Local subprocess (fallback)
    ├── Timeout enforcement
    └── No shell injection

Layer 3: Output Sanitization
├── HTML escaping
├── Error message filtering
└── Output length limits

Layer 4: Rate Limiting (future)
├── Per-user limits
├── API rate limits
└── Resource quotas
```

## Performance Optimization

### Caching Strategy
```
1. Language Templates
   └── Cached in memory (LANGUAGE_CONFIGS)

2. Docker Images
   └── Pre-pulled and cached locally

3. Common Error Explanations (future)
   └── Cache frequent error patterns

4. LLM Responses (future)
   └── Cache similar code analysis
```

### Async Operations
```
Frontend:
├── Non-blocking UI updates
├── Loading indicators
└── Debounced requests

Backend:
├── Async LLM calls
├── Background cleanup
└── Parallel Docker operations
```

## Scalability Considerations

### Current Design
- Single-server deployment
- Synchronous code execution
- In-memory state

### Future Scaling Options
```
1. Horizontal Scaling
   ├── Load balancer
   ├── Multiple backend instances
   └── Shared state (Redis)

2. Execution Queue
   ├── Message queue (RabbitMQ/Redis)
   ├── Worker processes
   └── Job prioritization

3. Distributed Execution
   ├── Kubernetes pods
   ├── Auto-scaling
   └── Resource management

4. CDN Integration
   ├── Static assets
   ├── Monaco Editor
   └── Templates
```

## Error Handling

### Error Flow
```
Code Execution Error
    ↓
Capture Error Details
    ↓
Check Common Patterns
    ↓
Generate AI Explanation
    ↓
Format for Display
    ↓
Return to User
```

### Error Types Handled
1. **Syntax Errors**: Missing colons, brackets, etc.
2. **Runtime Errors**: Division by zero, null references
3. **Compilation Errors**: Type mismatches, undefined symbols
4. **Timeout Errors**: Infinite loops, slow algorithms
5. **Memory Errors**: Out of memory, stack overflow

## Monitoring Points

### Metrics to Track
```
1. Execution Metrics
   ├── Execution time
   ├── Success rate
   ├── Error rate
   └── Language usage

2. AI Metrics
   ├── LLM response time
   ├── Explanation quality
   ├── API usage
   └── Cost tracking

3. User Metrics
   ├── Active users
   ├── Code runs per user
   ├── Challenge completion
   └── Feature usage

4. System Metrics
   ├── Docker availability
   ├── Resource usage
   ├── API latency
   └── Error rates
```

## Integration Points

### With InterVyou Platform
```
1. Authentication
   └── Uses existing user session

2. Database
   └── Can store code submissions (future)

3. LLM Service
   └── Shares llm_utils.py

4. Navigation
   └── Integrated in main menu

5. Styling
   └── Consistent with platform theme
```

## Technology Stack

```
Frontend:
├── Monaco Editor (Microsoft)
├── Vanilla JavaScript
├── CSS3 (Dark theme)
└── Font Awesome icons

Backend:
├── FastAPI (Python)
├── Pydantic (Validation)
├── asyncio (Async operations)
└── subprocess (Execution)

Execution:
├── Docker (Containerization)
├── Python 3.11
├── Node.js 20
├── OpenJDK 17
└── GCC 11

AI:
├── OpenAI GPT-4o-mini
├── Groq (Alternative)
└── Custom prompts

Infrastructure:
├── Windows/Linux/Mac support
├── SQLite/PostgreSQL
└── Environment variables
```

## Deployment Architecture

```
Development:
├── Local Python server
├── SQLite database
├── Local Docker
└── Development API keys

Production:
├── Gunicorn/Uvicorn
├── PostgreSQL/Supabase
├── Docker Swarm/K8s
├── Production API keys
├── Load balancer
└── CDN for static assets
```

---

**This architecture provides a solid foundation for a scalable, secure, and user-friendly online IDE!**
