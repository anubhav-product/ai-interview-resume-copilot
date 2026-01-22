// ==================== DOM ELEMENTS ====================
const resumeInput = document.getElementById('resumeInput');
const resumeDropZone = document.getElementById('resumeDropZone');
const jobDescription = document.getElementById('jobDescription');
const analyzeBtn = document.getElementById('analyzeBtn');
const resetBtn = document.getElementById('resetBtn');
const modelSelect = document.getElementById('modelSelect');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const analysisContent = document.getElementById('analysisContent');
const downloadTxt = document.getElementById('downloadTxt');
const downloadMd = document.getElementById('downloadMd');
const wordCount = document.getElementById('wordCount');

let currentAnalysis = null;

// ==================== EVENT LISTENERS ====================

// Resume file input
resumeInput.addEventListener('change', handleResumeSelect);

// Resume drag and drop
resumeDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    resumeDropZone.classList.add('drag-over');
});

resumeDropZone.addEventListener('dragleave', () => {
    resumeDropZone.classList.remove('drag-over');
});

resumeDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    resumeDropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        resumeInput.files = files;
        handleResumeSelect();
    }
});

// Click on drop zone to browse
resumeDropZone.addEventListener('click', () => {
    resumeInput.click();
});

// Job description word count
jobDescription.addEventListener('input', () => {
    const count = jobDescription.value.trim().split(/\s+/).filter(w => w.length > 0).length;
    wordCount.textContent = count;
});

// Analyze button
analyzeBtn.addEventListener('click', handleAnalyze);

// Reset button
resetBtn.addEventListener('click', handleReset);

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const tabName = e.target.dataset.tab;
        switchTab(tabName);
    });
});

// Download buttons
downloadTxt.addEventListener('click', () => downloadAnalysis('txt'));
downloadMd.addEventListener('click', () => downloadAnalysis('md'));

// ==================== FILE HANDLING ====================

function handleResumeSelect() {
    const file = resumeInput.files[0];
    if (file) {
        const resumeInfo = document.getElementById('resumeInfo');
        const resumeFileName = document.getElementById('resumeFileName');
        const uploadArea = resumeDropZone;

        // Check file type
        if (file.type !== 'application/pdf') {
            showError('Please upload a PDF file');
            resumeInput.value = '';
            return;
        }

        // Check file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showError('File size must be less than 5MB');
            resumeInput.value = '';
            return;
        }

        // Display file info
        uploadArea.style.display = 'none';
        resumeInfo.style.display = 'block';
        resumeFileName.textContent = `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    }
}

// ==================== ANALYZE ====================

async function handleAnalyze() {
    // Validate inputs
    if (!resumeInput.files[0]) {
        showError('Please upload a resume');
        return;
    }

    if (!jobDescription.value.trim()) {
        showError('Please enter a job description');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('resume', resumeInput.files[0]);
    formData.append('job_description', jobDescription.value);
    formData.append('model', modelSelect.value);

    // Show loading state
    analyzeBtn.disabled = true;
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    btnText.textContent = 'Analyzing...';
    btnLoader.classList.remove('hidden');
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';

    try {
        // Call API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Store analysis for export
        currentAnalysis = data.analysis;

        // Display results
        displayResults(data);
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Resume';
        btnLoader.classList.add('hidden');
    }
}

function displayResults(data) {
    const { analysis, model, timestamp } = data;

    // Parse markdown to HTML
    const htmlContent = parseMarkdown(analysis);
    analysisContent.innerHTML = htmlContent;

    // Update metadata
    document.getElementById('resultModel').textContent = model;
    document.getElementById('resultTime').textContent = new Date(timestamp).toLocaleString();
    document.getElementById('summaryModel').textContent = model;

    // Reset tabs
    switchTab('report');
}

function parseMarkdown(markdown) {
    let html = markdown;

    // Headers
    html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.*?)_/g, '<em>$1</em>');

    // Lists
    html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^- (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^\d+\. (.*?)$/gm, '<li>$1</li>');

    // Wrap list items
    html = html.replace(/(<li>.*?<\/li>)/s, (match) => {
        return '<ul>' + match + '</ul>';
    });

    // Cleanup multiple ul tags
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Code blocks
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';

    return html;
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabContent = document.getElementById(`${tabName}-tab`);
    if (tabContent) {
        tabContent.classList.add('active');
    }

    // Mark button as active
    const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// ==================== DOWNLOAD ====================

function downloadAnalysis(format) {
    if (!currentAnalysis) {
        alert('No analysis to download');
        return;
    }

    const element = document.createElement('a');
    const timestamp = new Date().toISOString().split('T')[0];
    const content = currentAnalysis;
    const mimeType = format === 'txt' ? 'text/plain' : 'text/markdown';
    const filename = `resume_analysis_${timestamp}.${format}`;

    element.setAttribute('href', 'data:' + mimeType + ';charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ==================== RESET ====================

function handleReset() {
    // Clear inputs
    resumeInput.value = '';
    jobDescription.value = '';
    wordCount.textContent = '0';

    // Clear file info
    const resumeInfo = document.getElementById('resumeInfo');
    const uploadArea = resumeDropZone;
    resumeInfo.style.display = 'none';
    uploadArea.style.display = 'block';

    // Hide results
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Reset to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Focus on resume input
    resumeInput.focus();
}

// ==================== ERROR HANDLING ====================

function showError(message) {
    const errorMsg = document.getElementById('errorMessage');
    errorMsg.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

// ==================== UTILITY FUNCTIONS ====================

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Add smooth scroll behavior
document.addEventListener('DOMContentLoaded', () => {
    // Add animation to elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('[class*="section"]').forEach(el => {
        observer.observe(el);
    });
});

// Prevent multiple submissions
let isSubmitting = false;

async function submitAnalysis() {
    if (isSubmitting) return;
    isSubmitting = true;

    try {
        await handleAnalyze();
    } finally {
        isSubmitting = false;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!analyzeBtn.disabled) {
            handleAnalyze();
        }
    }

    // Escape to close error
    if (e.key === 'Escape') {
        errorSection.style.display = 'none';
    }
});

// ==================== RESPONSIVE BEHAVIOR ====================

// Adjust for mobile
if (window.innerWidth < 768) {
    document.querySelector('.section-grid').style.gridTemplateColumns = '1fr';
}

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        document.querySelector('.section-grid').style.gridTemplateColumns = '1fr';
    } else {
        document.querySelector('.section-grid').style.gridTemplateColumns = '1fr 1fr';
    }
});

// ==================== INITIALIZATION ====================

console.log('✅ AI Resume Copilot loaded');
