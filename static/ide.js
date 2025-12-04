// AI-Powered IDE JavaScript
console.log('IDE JavaScript loaded');
let editor;
let currentLanguage = 'python';
let runCount = 0;
let successCount = 0;

// Initialize Monaco Editor
function initializeEditor() {
    console.log('Initializing Monaco editor...');
    
    if (typeof monaco === 'undefined') {
        console.error('Monaco editor not loaded');
        document.getElementById('editor').innerHTML = '<div style="color: #f48771; padding: 20px; text-align: center;"><i class="fas fa-exclamation-triangle" style="font-size: 48px; margin-bottom: 15px;"></i><br>Failed to load code editor. Please refresh the page.</div>';
        return;
    }
    
    try {
        const editorElement = document.getElementById('editor');
        if (!editorElement) {
            console.error('Editor element not found');
            return;
        }
        
        editor = monaco.editor.create(editorElement, {
            value: '# Write your Python code here\ndef solution():\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    solution()\n',
            language: 'python',
            theme: 'vs-dark',
            fontSize: 14,
            minimap: { enabled: true },
            automaticLayout: true,
            scrollBeyondLastLine: false,
            lineNumbers: 'on',
            renderWhitespace: 'selection',
            tabSize: 4,
            wordWrap: 'on'
        });

        console.log('Monaco editor initialized successfully');
        
        // Load initial template after a short delay
        setTimeout(() => {
            loadTemplate();
        }, 100);
        
    } catch (error) {
        console.error('Failed to initialize Monaco editor:', error);
        document.getElementById('editor').innerHTML = '<div style="color: #f48771; padding: 20px; text-align: center;"><i class="fas fa-exclamation-triangle" style="font-size: 48px; margin-bottom: 15px;"></i><br>Error initializing editor: ' + error.message + '</div>';
    }
}

// Wait for Monaco to be ready - using unpkg loader
require.config({ 
    paths: { 
        vs: 'https://unpkg.com/monaco-editor@0.44.0/min/vs' 
    } 
});

// Load Monaco with error handling
window.monacoLoadError = false;
window.monacoLoadTimeout = setTimeout(function() {
    if (!editor) {
        console.error('Monaco failed to load within timeout');
        window.monacoLoadError = true;
        createFallbackEditor();
    }
}, 10000); // 10 second timeout

try {
    require(['vs/editor/editor.main'], function () {
        clearTimeout(window.monacoLoadTimeout);
        console.log('Monaco loaded, initializing editor...');
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeEditor);
        } else {
            initializeEditor();
        }
    });
} catch (error) {
    console.error('Error loading Monaco:', error);
    clearTimeout(window.monacoLoadTimeout);
    createFallbackEditor();
}

// Fallback editor using textarea
function createFallbackEditor() {
    console.log('Creating fallback textarea editor');
    const editorElement = document.getElementById('editor');
    if (!editorElement) return;
    
    editorElement.innerHTML = `
        <textarea id="fallbackEditor" style="
            width: 100%;
            height: 100%;
            background: #1e1e1e;
            color: #d4d4d4;
            border: none;
            padding: 15px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            resize: none;
            outline: none;
        "># Write your Python code here
def solution():
    # Your code here
    pass

if __name__ == "__main__":
    solution()
</textarea>
    `;
    
    // Create a simple editor object that mimics Monaco's API
    editor = {
        getValue: function() {
            return document.getElementById('fallbackEditor').value;
        },
        setValue: function(value) {
            document.getElementById('fallbackEditor').value = value;
        },
        getModel: function() {
            return {
                setLanguage: function() {}
            };
        }
    };
    
    console.log('Fallback editor created');
}

// Language mapping for Monaco
const languageMap = {
    'python': 'python',
    'javascript': 'javascript',
    'java': 'java',
    'cpp': 'cpp',
    'c': 'c'
};

// Event Listeners - wrapped in DOMContentLoaded to ensure elements exist
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up event listeners');
    
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.addEventListener('change', (e) => {
            currentLanguage = e.target.value;
            if (editor && editor.getModel && typeof monaco !== 'undefined') {
                monaco.editor.setModelLanguage(editor.getModel(), languageMap[currentLanguage]);
            }
            loadTemplate();
        });
    }

    const runBtn = document.getElementById('runBtn');
    if (runBtn) runBtn.addEventListener('click', runCode);
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeCode);
    
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) clearBtn.addEventListener('click', clearEditor);
    
    const templateBtn = document.getElementById('templateBtn');
    if (templateBtn) templateBtn.addEventListener('click', loadTemplate);
    
    console.log('Event listeners attached');
});

// Tab switching and challenges - moved to DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName);
        });
    });

    // Load challenges
    loadChallenges();
});

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
