const socket = io({
    transports: ['websocket'],
    upgrade: false
});
const form = document.getElementById('objectiveForm');
const submitBtn = document.getElementById('submitBtn');
const objective = document.getElementById('objective');
const logger = document.getElementById('logger');
const logContent = document.getElementById('logContent');
const result = document.getElementById('result');
const markdownContent = document.getElementById('markdown-content');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    const logEntry = document.createElement('p');
    logEntry.textContent = `Connection error: ${error.message}`;
    logEntry.classList.add('error');
    logContent.appendChild(logEntry);
});

socket.on('log', function(data) {
    logger.classList.remove('hidden');
    const logEntry = document.createElement('p');
    logEntry.textContent = data.message;
    logContent.appendChild(logEntry);
    logContent.scrollTop = logContent.scrollHeight;
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    objective.disabled = true;
    logger.classList.remove('hidden');
    result.classList.add('hidden');

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ objective: objective.value }),
        });
        const data = await response.json();
        markdownContent.innerHTML = marked.parse(data.result);
        result.classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        const logEntry = document.createElement('p');
        logEntry.textContent = `Error: ${error.message}`;
        logEntry.classList.add('error');
        logContent.appendChild(logEntry);
    } finally {
        submitBtn.disabled = false;
        objective.disabled = false;
    }
});

copyBtn.addEventListener('click', () => {
    const content = markdownContent.innerText;
    navigator.clipboard.writeText(content).then(() => {
        alert('Content copied to clipboard!');
    });
});

downloadBtn.addEventListener('click', () => {
    const content = markdownContent.innerText;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'result.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});
