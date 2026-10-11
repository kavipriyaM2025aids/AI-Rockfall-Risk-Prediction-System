document.addEventListener('DOMContentLoaded', async () => {
    const loading = document.getElementById('history-loading');
    const empty = document.getElementById('history-empty');
    const error = document.getElementById('history-error');
    const table = document.getElementById('history-table');
    const tbody = document.getElementById('history-body');

    const getRiskBadge = (risk) => {
        const map = {
            'safe': 'bg-safe',
            'moderate': 'bg-moderate',
            'early warning': 'bg-early-warning',
            'high risk': 'bg-high-risk'
        };
        const cls = map[risk?.toLowerCase()] || 'bg-moderate';
        return `<span class="badge ${cls}" style="color: white; padding: 4px 8px; font-size: 0.75rem;">${risk}</span>`;
    };

    const getEwBadge = (status) => {
        if (status) return `<span class="badge bg-early-warning" style="color: white;"><i class="fa-solid fa-bolt"></i> YES</span>`;
        return `<span class="badge" style="background: rgba(255,255,255,0.1); color: var(--text-muted);">NO</span>`;
    };

    const historyData = await window.api.getPredictionHistory();

    loading.style.display = 'none';

    if (!historyData) {
        error.style.display = 'flex';
        return;
    }

    if (historyData.length === 0) {
        empty.style.display = 'flex';
        return;
    }

    table.style.display = 'table';
    tbody.innerHTML = historyData.map(item => `
        <tr>
            <td style="white-space: nowrap;">${item.dateTime}</td>
            <td>${item.source}</td>
            <td>${item.zone}</td>
            <td>${getRiskBadge(item.riskLevel)}</td>
            <td style="font-weight: 600;">${item.confidence}%</td>
            <td>${getEwBadge(item.earlyWarningStatus)}</td>
            <td style="font-size: 0.85rem; color: var(--text-muted); max-width: 300px;">${item.reason}</td>
        </tr>
    `).join('');
});
