// AI-Powered IDE JavaScript
let editor;
let currentLanguage = 'python';
let runCount = 0;
let successCount = 0;

// Initialize Monaco Editor
require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' } });

require(['vs/editor/editor.main'], function () {
    editor = monaco.editor.create(document.getElementById('editor'), {
        value: '',
        language: 'python',
        theme: 'vs-dark',
        fontSize: 14,
        minimap: { enabled: true },
        automaticLayout: true,
        scrollBeyondLastLine: false,
        lineNumbers: 'on',
        renderWhitespace: 'selection',
        tabSize: 4
    });

    // Load initial template
    loadTemplate();
});

// Language mapping for Monaco
const languageMap = {
    'python': 'python',
    'javascript': 'javascript',
    'java': 'java',
    'cpp': 'cpp',
    'c': 'c'
};

// Event Listeners
document.getElementById('languageSelect').addEventListener('change', (e) => {
    currentLanguage = e.target.value;
    monaco.editor.setModelLanguage(editor.getModel(), languageMap[currentLanguage]);
    loadTemplate();
});

document.getElementById('runBtn').addEventListener('click', runCode);
document.getElementById('analyzeBtn').addEventListener('click', analyzeCode);
document.getElementById('clearBtn').addEventListener('click', clearEditor);
document.getElementById('templateBtn').addEventListener('click', loadTemplate);

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        switchTab(tabName);
    });
});

// Load challenges
loadChallenges();

// Functions
async function runCode() {
    const code = editor.getValue();
    const inputData = document.getElementById('inputData').value;

    if (!code.trim()) {
        showNotification('Please write some code first!', 'error');
        return;
    }

    showLoading(true);
    runCount++;
    updateStats();

    try {
        const response = await fetch('/ide/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: currentLanguage,
                input_data: inputData
            })
        });

        const result = await response.json();
        
        showLoading(false);
        displayOutput(result);

        if (result.success) {
            successCount++;
            updateStats();
        }

        // Show execution time
        if (result.execution_time) {
            document.getElementById('executionTime').textContent = 
                `⚡ ${result.execution_time}s`;
        }

    } catch (error) {
        showLoading(false);
        showNotification('Failed to execute code: ' + error.message, 'error');
    }
}

function displayOutput(result) {
    const outputContent = document.getElementById('outputContent');
    
    if (result.success) {
        outputContent.innerHTML = `
            <div class="ai-section output-success">
                <h4><i class="fas fa-check-circle"></i> Success!</h4>
                <pre>${escapeHtml(result.output || 'Program executed successfully (no output)')}</pre>
            </div>
        `;
        switchTab('output');
    } else {
        outputContent.innerHTML = `
            <div class="ai-section output-error">
                <h4><i class="fas fa-times-circle"></i> Error</h4>
                <pre>${escapeHtml(result.error)}</pre>
            </div>
        `;
        
        // Display AI explanation if available
        if (result.ai_explanation) {
            displayAIHelp(result.ai_explanation);
            switchTab('ai-help');
        } else {
            switchTab('output');
        }
    }
}

function displayAIHelp(aiExplanation) {
    const aiHelpContent = document.getElementById('aiHelpContent');
    
    let html = '';
    
    // Quick hint
    if (aiExplanation.quick_hint) {
        html += `
            <div class="quick-hint">
                <strong><i class="fas fa-lightbulb"></i> Quick Hint:</strong><br>
                ${escapeHtml(aiExplanation.quick_hint)}
            </div>
        `;
    }
    
    // Detailed analysis
    if (aiExplanation.detailed_analysis) {
        const analysis = aiExplanation.detailed_analysis;
        
        html += `
            <div class="ai-section">
                <h4><i class="fas fa-info-circle"></i> What Went Wrong</h4>
                <p>${escapeHtml(analysis.explanation || 'Error analysis unavailable')}</p>
            </div>
            
            <div class="ai-section">
                <h4><i class="fas fa-map-marker-alt"></i> Problem Location</h4>
                <p>${escapeHtml(analysis.problem_location || 'Check error message')}</p>
            </div>
            
            <div class="ai-section">
                <h4><i class="fas fa-wrench"></i> How to Fix</h4>
                <p>${escapeHtml(analysis.fix || 'Review your code')}</p>
            </div>
            
            <div class="ai-section">
                <h4><i class="fas fa-graduation-cap"></i> Pro Tip</h4>
                <p>${escapeHtml(analysis.tip || 'Keep practicing!')}</p>
            </div>
        `;
    }
    
    aiHelpContent.innerHTML = html;
}

async function analyzeCode() {
    const code = editor.getValue();

    if (!code.trim()) {
        showNotification('Please write some code first!', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/ide/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: currentLanguage
            })
        });

        const analysis = await response.json();
        
        showLoading(false);
        displayAnalysis(analysis);
        switchTab('analysis');

    } catch (error) {
        showLoading(false);
        showNotification('Failed to analyze code: ' + error.message, 'error');
    }
}

function displayAnalysis(analysis) {
    const analysisContent = document.getElementById('analysisContent');
    
    let html = `
        <div class="score-display">
            <div class="score-number">${analysis.score || 0}/10</div>
            <div class="score-label">Code Quality Score</div>
        </div>
    `;
    
    if (analysis.strengths && analysis.strengths.length > 0) {
        html += `
            <div class="analysis-section">
                <h4><i class="fas fa-thumbs-up"></i> Strengths</h4>
                <ul>
                    ${analysis.strengths.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (analysis.improvements && analysis.improvements.length > 0) {
        html += `
            <div class="analysis-section">
                <h4><i class="fas fa-arrow-up"></i> Areas for Improvement</h4>
                <ul>
                    ${analysis.improvements.map(i => `<li>${escapeHtml(i)}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (analysis.performance_tip) {
        html += `
            <div class="analysis-section">
                <h4><i class="fas fa-rocket"></i> Performance Tip</h4>
                <p>${escapeHtml(analysis.performance_tip)}</p>
            </div>
        `;
    }
    
    analysisContent.innerHTML = html;
}

async function loadTemplate() {
    try {
        const response = await fetch(`/ide/template/${currentLanguage}`);
        const data = await response.json();
        editor.setValue(data.template);
    } catch (error) {
        console.error('Failed to load template:', error);
    }
}

function clearEditor() {
    editor.setValue('');
    document.getElementById('inputData').value = '';
    document.getElementById('executionTime').textContent = '';
}

async function loadChallenges() {
    try {
        const response = await fetch('/ide/challenges');
        const data = await response.json();
        
        const challengesList = document.getElementById('challengesList');
        challengesList.innerHTML = data.challenges.map(challenge => `
            <div class="challenge-item ${challenge.difficulty.toLowerCase()}" 
                 onclick="loadChallenge(${challenge.id})">
                <div class="challenge-title">${challenge.title}</div>
                <div class="challenge-difficulty">${challenge.difficulty}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load challenges:', error);
    }
}

async function loadChallenge(challengeId) {
    try {
        const response = await fetch(`/ide/challenges/${challengeId}`);
        const challenge = await response.json();
        
        // Show challenge description
        const description = `
/*
Challenge: ${challenge.title}
Difficulty: ${challenge.difficulty}

Description:
${challenge.description}

Examples:
${challenge.examples.map(ex => `Input: ${ex.input} → Output: ${ex.output}`).join('\n')}

Write your solution below:
*/

`;
        
        editor.setValue(description + LANGUAGE_CONFIGS[currentLanguage].template);
        showNotification(`Loaded: ${challenge.title}`, 'success');
        
    } catch (error) {
        showNotification('Failed to load challenge', 'error');
    }
}

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    const tabMap = {
        'output': 'outputTab',
        'ai-help': 'aiHelpTab',
        'analysis': 'analysisTab'
    };
    
    document.getElementById(tabMap[tabName]).classList.add('active');
}

function updateStats() {
    document.getElementById('runCount').textContent = runCount;
    document.getElementById('successCount').textContent = successCount;
}

function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

function showNotification(message, type) {
    // Simple notification (you can enhance this)
    const color = type === 'success' ? '#4ec9b0' : '#f48771';
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${color};
        color: white;
        padding: 15px 20px;
        border-radius: 4px;
        z-index: 2000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to run
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runCode();
    }
    
    // Ctrl/Cmd + Shift + A to analyze
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'A') {
        e.preventDefault();
        analyzeCode();
    }
});

// Language configs for frontend
const LANGUAGE_CONFIGS = {
    python: { template: '# Python code' },
    javascript: { template: '// JavaScript code' },
    java: { template: '// Java code' },
    cpp: { template: '// C++ code' },
    c: { template: '// C code' }
};
