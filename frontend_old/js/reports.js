document.addEventListener('DOMContentLoaded', async () => {
    const loading = document.getElementById('reports-loading');
    const error = document.getElementById('reports-error');
    const content = document.getElementById('reports-content');

    const data = await window.api.getReportSummary();

    loading.style.display = 'none';

    if (!data) {
        error.style.display = 'flex';
        return;
    }

    content.style.display = 'block';

    // Set Date
    document.getElementById('report-date').textContent = `Generated on: ${new Date().toLocaleString()}`;

    // Summary Stats
    if (data.summary) {
        document.getElementById('rep-total').textContent = data.summary.total || '--';
        document.getElementById('rep-safe').textContent = data.summary.safe || '--';
        document.getElementById('rep-moderate').textContent = data.summary.moderate || '--';
        document.getElementById('rep-high').textContent = data.summary.highRisk || '--';
    }

    // Events Table
    const tbody = document.getElementById('rep-events-body');
    if (data.events && data.events.length > 0) {
        tbody.innerHTML = data.events.map(ev => `
            <tr>
                <td>${ev.time}</td>
                <td><span class="badge ${ev.type === 'Early Warning' ? 'bg-early-warning' : 'bg-high-risk'}" style="color: white; padding: 2px 6px; font-size: 0.7rem;">${ev.type}</span></td>
                <td>${ev.zone}</td>
                <td style="color: var(--text-muted);">${ev.action}</td>
            </tr>
        `).join('');
    } else {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 24px;">No critical events recorded.</td></tr>`;
    }

    // Worker Stats
    if (data.workerSafety) {
        document.getElementById('rep-workers-active').textContent = data.workerSafety.activeTracked || '--';
        document.getElementById('rep-workers-breaches').textContent = data.workerSafety.zoneBreaches || '--';
    }
});
