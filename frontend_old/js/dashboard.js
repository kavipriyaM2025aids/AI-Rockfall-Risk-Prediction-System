document.addEventListener('DOMContentLoaded', async () => {
    // DOM Elements
    const elements = {
        grid: document.getElementById('dashboard-grid'),
        loading: document.getElementById('dashboard-loading'),
        error: document.getElementById('dashboard-error'),
        totalPredictions: document.getElementById('stat-total-predictions'),
        highRisk: document.getElementById('stat-high-risk'),
        earlyWarning: document.getElementById('stat-early-warning'),
        trackedWorkers: document.getElementById('stat-tracked-workers'),
        confidence: document.getElementById('stat-confidence'),
        riskStatus: document.getElementById('stat-risk-status'),
        latestTime: document.getElementById('stat-latest-time'),
        alertsList: document.getElementById('recent-alerts-list'),
        weatherWidget: document.getElementById('weather-widget')
    };

    // Helper: Map risk string to CSS class
    const getRiskClass = (riskLevel) => {
        const map = {
            'safe': 'bg-safe',
            'moderate': 'bg-moderate',
            'early warning': 'bg-early-warning',
            'high risk': 'bg-high-risk'
        };
        return map[riskLevel?.toLowerCase()] || 'bg-moderate';
    };

    // Load Dashboard Data
    async function loadDashboard() {
        const [statsData, weatherData, alertsData] = await Promise.all([
            window.api.getDashboardStatistics(),
            window.api.getCurrentWeather(),
            window.api.getAlerts()
        ]);

        // Weather Update
        if (weatherData) {
            elements.weatherWidget.innerHTML = `
                <i class="fa-solid fa-cloud-sun" style="color: var(--early-warning);"></i>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: 600;">${weatherData.temperature}°C, ${weatherData.condition}</span>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">${weatherData.location || 'Mine Site'}</span>
                </div>
            `;
        } else {
            elements.weatherWidget.innerHTML = `<span style="color: var(--text-muted); font-size: 0.85rem;">Weather data unavailable</span>`;
        }

        if (statsData) {
            // Update Stats
            elements.totalPredictions.textContent = statsData.totalPredictions ?? 'Data unavailable';
            elements.highRisk.textContent = statsData.highRiskZones ?? 'Data unavailable';
            elements.earlyWarning.textContent = statsData.earlyWarnings ?? 'Data unavailable';
            elements.trackedWorkers.textContent = statsData.trackedWorkers ?? 'Data unavailable';
            elements.confidence.textContent = statsData.averageConfidence ? `${statsData.averageConfidence}%` : 'Data unavailable';
            elements.latestTime.textContent = statsData.latestAnalysisTime || 'Data unavailable';
            
            if (statsData.currentRiskStatus) {
                elements.riskStatus.textContent = statsData.currentRiskStatus;
                elements.riskStatus.className = `badge ${getRiskClass(statsData.currentRiskStatus)}`;
                elements.riskStatus.style.color = '#fff';
            } else {
                elements.riskStatus.textContent = 'Data unavailable';
            }

            // Populate Alerts
            if (alertsData && alertsData.length > 0) {
                elements.alertsList.innerHTML = alertsData.slice(0, 4).map(alert => `
                    <div style="padding: 12px; border-radius: 8px; background: rgba(255,255,255,0.03); margin-bottom: 8px; border-left: 3px solid var(--${alert.riskLevel.replace(' ', '-')});">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-weight: 600; font-size: 0.9rem;">${alert.type}</span>
                            <span style="font-size: 0.75rem; color: var(--text-muted);">${alert.time}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">
                            Zone: ${alert.zone}
                        </div>
                    </div>
                `).join('');
            } else {
                elements.alertsList.innerHTML = `<div class="state-container" style="min-height: auto; padding: 20px;"><p>No recent alerts.</p></div>`;
            }

            // Toggle UI states
            elements.loading.style.display = 'none';
            elements.grid.style.display = 'block';
        } else {
            // Error State
            elements.loading.style.display = 'none';
            elements.error.style.display = 'flex';
        }
    }

    // Initialize
    loadDashboard();
});
