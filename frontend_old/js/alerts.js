document.addEventListener('DOMContentLoaded', async () => {
    const loading = document.getElementById('alerts-loading');
    const empty = document.getElementById('alerts-empty');
    const error = document.getElementById('alerts-error');
    const container = document.getElementById('alerts-container');

    const getRiskClass = (risk) => {
        const map = {
            'safe': 'bg-safe',
            'moderate': 'bg-moderate',
            'early warning': 'bg-early-warning',
            'high risk': 'bg-high-risk'
        };
        return map[risk?.toLowerCase()] || 'bg-moderate';
    };

    const getIcon = (risk) => {
        const map = {
            'early warning': '<i class="fa-solid fa-bolt" style="color: var(--early-warning);"></i>',
            'high risk': '<i class="fa-solid fa-triangle-exclamation" style="color: var(--high-risk);"></i>'
        };
        return map[risk?.toLowerCase()] || '<i class="fa-solid fa-circle-info" style="color: var(--primary);"></i>';
    };

    const alertsData = await window.api.getAlerts();

    loading.style.display = 'none';

    if (!alertsData) {
        error.style.display = 'flex';
        return;
    }

    if (alertsData.length === 0) {
        empty.style.display = 'flex';
        return;
    }

    container.style.display = 'flex';
    container.innerHTML = alertsData.map(alert => `
        <div class="glass" style="padding: 20px; display: flex; gap: 20px; border-left: 4px solid var(--${alert.riskLevel.replace(' ', '-')}); align-items: flex-start;">
            <div style="font-size: 1.5rem; margin-top: 4px;">
                ${getIcon(alert.riskLevel)}
            </div>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <h3 style="font-size: 1.1rem; font-weight: 600;">${alert.type}</h3>
                    <span style="font-size: 0.85rem; color: var(--text-muted);">${alert.time}</span>
                </div>
                <div style="margin-bottom: 12px; font-size: 0.95rem;">
                    <span style="color: var(--text-muted);">Zone:</span> ${alert.zone} &nbsp;|&nbsp; 
                    <span style="color: var(--text-muted);">Risk Level:</span> <span class="badge ${getRiskClass(alert.riskLevel)}" style="color: white; padding: 2px 8px; font-size: 0.7rem;">${alert.riskLevel}</span>
                </div>
                <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 8px; font-size: 0.9rem;">
                    <div style="margin-bottom: 8px;"><strong>Reason:</strong> ${alert.reason}</div>
                    <div style="color: var(--text-muted);"><strong>Action:</strong> ${alert.action}</div>
                </div>
            </div>
        </div>
    `).join('');
});
