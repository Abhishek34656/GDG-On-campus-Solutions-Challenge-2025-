document.getElementById('videoForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const topic = document.getElementById('topic').value.trim();
    if (!topic) {
        alert('Please enter a topic!');
        return;
    }

    const preview = document.getElementById('preview');
    preview.innerHTML = '<p>Generating video... Please wait.</p>';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate video. Please try again.');
        }

        const data = await response.json();
        const videoUrl = data.video_url;

        const videoPreview = document.getElementById('videoPreview');
        videoPreview.src = videoUrl;
        videoPreview.style.display = 'block';

        preview.innerHTML = '<h2>Video Preview</h2>';
    } catch (error) {
        console.error('Error:', error);
        preview.innerHTML = `<p style="color: red;">${error.message}</p>`;
    }
});