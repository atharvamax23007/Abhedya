// RBAC Tab Switching Logic
const tabs = document.querySelectorAll('.tab-btn');
const views = document.querySelectorAll('.role-view');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        views.forEach(v => v.classList.add('hidden'));

        tab.classList.add('active');
        const target = tab.getAttribute('data-role');
        document.getElementById(target).classList.remove('hidden');
    });
});

// Officer Portal: Token Generation Logic
document.getElementById('authForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('generateBtn');
    submitBtn.textContent = 'Generating Token...';
    submitBtn.disabled = true;
    
    const payload = {
        officer_id: document.getElementById('officerId').value,
        soldier_id: document.getElementById('soldierId').value,
        item_id: parseInt(document.getElementById('itemId').value)
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/generate_qr', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        
        if (data.qr_image) {
            document.getElementById('qrImage').src = `data:image/png;base64,${data.qr_image}`;
            document.getElementById('qrDisplay').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error generating token:', error);
        alert('Failed to connect to the tactical intranet. Ensure backend is running.');
    } finally {
        submitBtn.textContent = 'Generate QR Token';
        submitBtn.disabled = false;
    }
});

// Soldier Portal: Request Submission Logic (Frontend Mock)
document.getElementById('requestForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Gear request successfully submitted to the command ledger.');
    e.target.reset();
});