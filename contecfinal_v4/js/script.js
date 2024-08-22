document.getElementById('upload-button').addEventListener('click', function() {
    const fileInput = document.getElementById('image-upload');
    const fileError = document.getElementById('file-error');
    const resultsPanel = document.getElementById('results');
    const loadingSpinner = document.getElementById('loading-spinner');
    const progressBar = document.getElementById('progress-bar');
    
    // Clear previous error
    fileError.textContent = '';
    resultsPanel.innerHTML = '';
    
    // File validation
    const file = fileInput.files[0];
    if (!file || !['image/jpeg', 'image/png'].includes(file.type)) {
        fileError.textContent = 'Please upload a valid image file (JPEG or PNG).';
        return;
    }
    
    // Show loading spinner
    loadingSpinner.style.display = 'block';
    
    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.value = progress;
        if (progress >= 100) {
            clearInterval(interval);
            progressBar.value = 0;
            loadingSpinner.style.display = 'none';
            resultsPanel.innerHTML = `
                <h3>Visual Effects Analysis:</h3>
                <ul>
                    <li><strong>Color Grading:</strong> Detected cool tones with high contrast.</li>
                    <li><strong>Motion Blur:</strong> Medium intensity, directional blur.</li>
                    <li><strong>Compositing Techniques:</strong> Layered foreground elements with background defocus.</li>
                </ul>`;
        }
    }, 200);
});

// Theme toggle
const toggleThemeBtn = document.getElementById('toggle-theme');
toggleThemeBtn.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        toggleThemeBtn.textContent = 'Switch to Light Mode';
    } else {
        toggleThemeBtn.textContent = 'Switch to Dark Mode';
    }
});