document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const elements = {
        btnUploadMode: document.getElementById('btn-mode-upload'),
        btnSimulateMode: document.getElementById('btn-mode-simulate'),
        simulationBanner: document.getElementById('simulation-banner'),
        
        uploadSection: document.getElementById('upload-section'),
        previewSection: document.getElementById('preview-section'),
        fileInput: document.getElementById('file-input'),
        dropZone: document.getElementById('drop-zone'),
        imagePreview: document.getElementById('image-preview'),
        sourceBadge: document.getElementById('source-badge'),
        btnAnalyze: document.getElementById('btn-analyze'),
        btnClear: document.getElementById('btn-clear'),
        
        resultEmpty: document.getElementById('result-empty'),
        resultLoading: document.getElementById('result-loading'),
        resultContent: document.getElementById('result-content'),
        
        resRiskLevel: document.getElementById('res-risk-level'),
        resConfidence: document.getElementById('res-confidence'),
        resExplanation: document.getElementById('res-explanation'),
        resCracksContainer: document.getElementById('res-cracks-container'),
        resCracksText: document.getElementById('res-cracks-text')
    };

    let currentFile = null;
    let isSimulationMode = false;

    // Helper: Map risk string to CSS color
    const getRiskColor = (riskLevel) => {
        const map = {
            'safe': 'var(--safe)',
            'moderate': 'var(--moderate)',
            'early warning': 'var(--early-warning)',
            'high risk': 'var(--high-risk)'
        };
        return map[riskLevel?.toLowerCase()] || 'var(--moderate)';
    };

    // Mode Switching
    elements.btnUploadMode.addEventListener('click', () => {
        isSimulationMode = false;
        elements.btnUploadMode.className = 'btn btn-primary';
        elements.btnSimulateMode.className = 'btn';
        elements.btnSimulateMode.style.background = 'rgba(255,255,255,0.1)';
        elements.simulationBanner.style.display = 'none';
        elements.sourceBadge.textContent = 'Source: User Uploaded Sample';
        clearInput();
    });

    elements.btnSimulateMode.addEventListener('click', () => {
        isSimulationMode = true;
        elements.btnSimulateMode.className = 'btn btn-primary';
        elements.btnUploadMode.className = 'btn';
        elements.btnUploadMode.style.background = 'rgba(255,255,255,0.1)';
        elements.simulationBanner.style.display = 'flex';
        elements.sourceBadge.textContent = 'Source: Mine Slope Image Dataset';
        
        // Load a mock image for simulation visually (since it's a frontend prototype)
        // In a real scenario, this would fetch from backend dataset
        showPreview('https://images.unsplash.com/photo-1574768391782-bdf4b373efae?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80');
        
        // Auto-analyze in simulation mode
        setTimeout(() => elements.btnAnalyze.click(), 1000);
    });

    // File Upload Handling
    elements.btnAnalyze.addEventListener('click', async () => {
        if (!currentFile && !isSimulationMode) return;
        
        // UI Loading State
        elements.resultEmpty.style.display = 'none';
        elements.resultContent.style.display = 'none';
        elements.resultLoading.style.display = 'flex';

        // Call API
        let data = null;
        if (isSimulationMode) {
            // For simulation, we might fetch a random prediction from the backend test endpoint
            // Since we must use ACTUAL backend data, we call the predict API with simulation flag
            // However, since there is no actual file in simulation mode (we used a placeholder), 
            // we will create a dummy blob just to satisfy the form data, but backend should know it's simulation
            const dummyBlob = new Blob([''], { type: 'image/jpeg' });
            data = await window.api.uploadImage(dummyBlob, true);
        } else {
            data = await window.api.uploadImage(currentFile, false);
        }

        // Handle Response
        elements.resultLoading.style.display = 'none';
        
        if (data) {
            elements.resultContent.style.display = 'flex';
            elements.resRiskLevel.textContent = data.riskLevel || 'Data unavailable';
            elements.resRiskLevel.style.color = getRiskColor(data.riskLevel);
            elements.resConfidence.textContent = data.confidence ? `${data.confidence}%` : '--%';
            elements.resExplanation.textContent = data.explanation || 'No explanation provided.';
            
            if (data.detectedCracks || data.unstableRegions) {
                elements.resCracksContainer.style.display = 'block';
                const crackText = [];
                if (data.detectedCracks) crackText.push(`${data.detectedCracks} cracks detected`);
                if (data.unstableRegions) crackText.push(`${data.unstableRegions} unstable regions identified`);
                elements.resCracksText.textContent = crackText.join(', ');
            } else {
                elements.resCracksContainer.style.display = 'none';
            }
        } else {
            elements.resultEmpty.style.display = 'flex';
            elements.resultEmpty.innerHTML = `
                <i class="fa-solid fa-circle-exclamation" style="font-size: 2.5rem; margin-bottom: 16px; color: var(--high-risk);"></i>
                <p>Failed to retrieve prediction.<br>Data unavailable.</p>
            `;
        }
    });

    elements.btnClear.addEventListener('click', clearInput);

    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and Drop
    elements.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.dropZone.style.borderColor = 'var(--primary)';
    });

    elements.dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        elements.dropZone.style.borderColor = 'var(--card-border)';
    });

    elements.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.dropZone.style.borderColor = 'var(--card-border)';
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }
        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            showPreview(e.target.result);
        };
        reader.readAsDataURL(file);
    }

    function showPreview(src) {
        elements.imagePreview.src = src;
        elements.uploadSection.style.display = 'none';
        elements.previewSection.style.display = 'flex';
    }

    function clearInput() {
        currentFile = null;
        elements.fileInput.value = '';
        elements.imagePreview.src = '';
        elements.uploadSection.style.display = 'block';
        elements.previewSection.style.display = 'none';
        
        elements.resultContent.style.display = 'none';
        elements.resultLoading.style.display = 'none';
        elements.resultEmpty.style.display = 'flex';
        elements.resultEmpty.innerHTML = `
            <i class="fa-solid fa-magnifying-glass" style="font-size: 2.5rem; margin-bottom: 16px;"></i>
            <p>Upload an image or start simulation<br>to view prediction results.</p>
        `;
    }
});
