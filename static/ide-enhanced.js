// Enhanced LeetCode-Style Code Editor
let monacoEditor = null;

function codeEditor() {
    return {
        // State
        language: 'python',
        problemTab: 'description',
        consoleTab: 'testcases',
        notes: '',
        shownHints: [],
        
        currentProblem: {
            id: 1,
            title: 'Two Sum',
            difficulty: 'easy',
            description: 'Given an array of integers <code>nums</code> and an integer <code>target</code>, return indices of the two numbers such that they add up to <code>target</code>.<br><br>You may assume that each input would have exactly one solution, and you may not use the same element twice.<br><br>You can return the answer in any order.',
            examples: [
                '<strong>Input:</strong> nums = [2,7,11,15], target = 9<br><strong>Output:</strong> [0,1]<br><strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].',
                '<strong>Input:</strong> nums = [3,2,4], target = 6<br><strong>Output:</strong> [1,2]',
                '<strong>Input:</strong> nums = [3,3], target = 6<br><strong>Output:</strong> [0,1]'
            ],
            constraints: [
                '2 <= nums.length <= 10⁴',
                '-10⁹ <= nums[i] <= 10⁹',
                '-10⁹ <= target <= 10⁹',
                'Only one valid answer exists'
            ],
            hints: [
                'A really brute force way would be to search for all possible pairs of numbers but that would be too slow. Again, it\'s best to try out brute force solutions for just for completeness. It is from these brute force solutions that you can come up with optimizations.',
                'So, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y which is value - x where value is the input parameter. Can we change our array somehow so that this search becomes faster?',
                'The second train of thought is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?'
            ],
            starterCode: {
                python: `def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    # Write your code here
    pass`,
                javascript: `/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function(nums, target) {
    // Write your code here
};`,
                java: `class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Write your code here
        return new int[0];
    }
}`,
                cpp: `class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Write your code here
    }
};`,
                c: `/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // Write your code here
}`
            }
        },
        
        testCases: [
            { input: 'nums = [2,7,11,15], target = 9', expected: '[0,1]', actual: '', status: '' },
            { input: 'nums = [3,2,4], target = 6', expected: '[1,2]', actual: '', status: '' },
            { input: 'nums = [3,3], target = 6', expected: '[0,1]', actual: '', status: '' }
        ],
        
        output: {
            content: '',
            type: ''
        },
        
        submissions: [],
        
        // Methods
        init() {
            this.initMonaco();
            this.loadNotes();
            this.loadSubmissions();
        },
        
        initMonaco() {
            require.config({ paths: { vs: 'https://unpkg.com/monaco-editor@0.44.0/min/vs' } });
            
            require(['vs/editor/editor.main'], () => {
                monacoEditor = monaco.editor.create(document.getElementById('monaco-editor'), {
                    value: this.currentProblem.starterCode[this.language],
                    language: this.language,
                    theme: 'vs-dark',
                    fontSize: 14,
                    minimap: { enabled: true },
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    lineNumbers: 'on',
                    renderWhitespace: 'selection',
                    tabSize: 4,
                    wordWrap: 'on',
                    suggestOnTriggerCharacters: true,
                    quickSuggestions: true,
                    formatOnPaste: true,
                    formatOnType: true
                });
                
                // Add keyboard shortcuts
                monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
                    this.runCode();
                });
                
                monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => {
                    this.submitCode();
                });
            });
        },
        
        changeLanguage() {
            if (monacoEditor) {
                const currentCode = monacoEditor.getValue();
                const starterCode = this.currentProblem.starterCode[this.language];
                
                // Only reset if user hasn't written much code
                if (currentCode.trim().length < 50 || confirm('Switch language? Your current code will be replaced.')) {
                    monaco.editor.setModelLanguage(monacoEditor.getModel(), this.language);
                    monacoEditor.setValue(starterCode);
                }
            }
        },
        
        resetCode() {
            if (confirm('Reset to starter code? Your changes will be lost.')) {
                monacoEditor.setValue(this.currentProblem.starterCode[this.language]);
            }
        },
        
        async runCode() {
            const code = monacoEditor.getValue();
            
            if (!code.trim()) {
                this.showNotification('Please write some code first!', 'error');
                return;
            }
            
            this.consoleTab = 'testcases';
            this.output.content = 'Running test cases...';
            this.output.type = '';
            
            try {
                const response = await fetch('/ide/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        code: code,
                        language: this.language,
                        test_cases: this.testCases.map(tc => tc.input)
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Update test cases with results
                    result.test_results.forEach((testResult, index) => {
                        this.testCases[index].actual = testResult.output;
                        this.testCases[index].status = testResult.passed ? 'passed' : 'failed';
                    });
                    
                    const allPassed = result.test_results.every(tr => tr.passed);
                    this.output.content = allPassed ? 
                        '✓ All test cases passed!' : 
                        '✗ Some test cases failed. Check the Test Cases tab.';
                    this.output.type = allPassed ? 'success' : 'error';
                } else {
                    this.output.content = result.error;
                    this.output.type = 'error';
                    this.consoleTab = 'output';
                }
            } catch (error) {
                this.output.content = 'Error: ' + error.message;
                this.output.type = 'error';
                this.consoleTab = 'output';
            }
        },
        
        async submitCode() {
            const code = monacoEditor.getValue();
            
            if (!code.trim()) {
                this.showNotification('Please write some code first!', 'error');
                return;
            }
            
            this.output.content = 'Submitting your solution...';
            this.output.type = '';
            this.consoleTab = 'output';
            
            try {
                const response = await fetch('/ide/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        code: code,
                        language: this.language,
                        problem_id: this.currentProblem.id
                    })
                });
                
                const result = await response.json();
                
                if (result.accepted) {
                    this.output.content = `✓ Accepted!\n\nRuntime: ${result.runtime}\nMemory: ${result.memory}\n\nYour solution beats ${result.beats}% of submissions!`;
                    this.output.type = 'success';
                    
                    // Add to submissions
                    this.submissions.unshift({
                        status: 'accepted',
                        time: new Date().toLocaleString(),
                        language: this.language,
                        runtime: result.runtime,
                        memory: result.memory,
                        code: code
                    });
                    
                    this.saveSubmissions();
                    this.showNotification('Solution accepted! 🎉', 'success');
                } else {
                    this.output.content = `✗ Wrong Answer\n\nTest Case: ${result.failed_test}\nExpected: ${result.expected}\nActual: ${result.actual}`;
                    this.output.type = 'error';
                    
                    this.submissions.unshift({
                        status: 'wrong',
                        time: new Date().toLocaleString(),
                        language: this.language,
                        runtime: result.runtime || 'N/A',
                        memory: result.memory || 'N/A',
                        code: code
                    });
                    
                    this.saveSubmissions();
                }
            } catch (error) {
                this.output.content = 'Submission error: ' + error.message;
                this.output.type = 'error';
            }
        },
        
        toggleHint(index) {
            const hintIndex = this.shownHints.indexOf(index);
            if (hintIndex > -1) {
                this.shownHints.splice(hintIndex, 1);
            } else {
                this.shownHints.push(index);
            }
        },
        
        saveNotes() {
            localStorage.setItem(`notes_${this.currentProblem.id}`, this.notes);
        },
        
        loadNotes() {
            this.notes = localStorage.getItem(`notes_${this.currentProblem.id}`) || '';
        },
        
        saveSubmissions() {
            localStorage.setItem(`submissions_${this.currentProblem.id}`, JSON.stringify(this.submissions));
        },
        
        loadSubmissions() {
            const saved = localStorage.getItem(`submissions_${this.currentProblem.id}`);
            if (saved) {
                this.submissions = JSON.parse(saved);
            }
        },
        
        loadSubmission(submission) {
            if (confirm('Load this submission? Your current code will be replaced.')) {
                monacoEditor.setValue(submission.code);
                this.language = submission.language;
                monaco.editor.setModelLanguage(monacoEditor.getModel(), this.language);
            }
        },
        
        toggleTheme() {
            const currentTheme = monacoEditor.getModel()._options.theme;
            const newTheme = currentTheme === 'vs-dark' ? 'vs-light' : 'vs-dark';
            monaco.editor.setTheme(newTheme);
        },
        
        toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        },
        
        showSettings() {
            alert('Settings panel coming soon!');
        },
        
        showNotification(message, type) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 70px;
                right: 20px;
                background: ${type === 'success' ? 'var(--accent-green)' : 'var(--accent-red)'};
                color: #000;
                padding: 16px 24px;
                border-radius: 8px;
                z-index: 10000;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
    };
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
