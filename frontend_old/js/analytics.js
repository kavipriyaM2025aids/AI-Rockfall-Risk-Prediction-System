document.addEventListener('DOMContentLoaded', async () => {
    const loading = document.getElementById('analytics-loading');
    const error = document.getElementById('analytics-error');
    const content = document.getElementById('analytics-content');

    const data = await window.api.getAnalyticsData();

    loading.style.display = 'none';

    if (!data) {
        error.style.display = 'flex';
        return;
    }

    content.style.display = 'block';

    // Chart Options Defaults
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter, sans-serif';

    // 1. Risk Distribution (Doughnut)
    if (data.riskDistribution) {
        const ctxRisk = document.getElementById('chart-risk').getContext('2d');
        new Chart(ctxRisk, {
            type: 'doughnut',
            data: {
                labels: ['Safe', 'Moderate', 'Early Warning', 'High Risk'],
                datasets: [{
                    data: [
                        data.riskDistribution.safe || 0,
                        data.riskDistribution.moderate || 0,
                        data.riskDistribution.earlyWarning || 0,
                        data.riskDistribution.highRisk || 0
                    ],
                    backgroundColor: ['#22c55e', '#eab308', '#f97316', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // 2. Prediction Trend (Bar)
    if (data.predictionTrend) {
        const ctxTrend = document.getElementById('chart-trend').getContext('2d');
        new Chart(ctxTrend, {
            type: 'bar',
            data: {
                labels: data.predictionTrend.labels,
                datasets: [{
                    label: 'Predictions Made',
                    data: data.predictionTrend.data,
                    backgroundColor: '#3b82f6',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // 3. Confidence Trend (Line)
    if (data.confidenceTrend) {
        const ctxConf = document.getElementById('chart-confidence').getContext('2d');
        new Chart(ctxConf, {
            type: 'line',
            data: {
                labels: data.confidenceTrend.labels,
                datasets: [{
                    label: 'Average Confidence (%)',
                    data: data.confidenceTrend.data,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { 
                        beginAtZero: false, 
                        min: 50, max: 100,
                        grid: { color: 'rgba(255,255,255,0.05)' } 
                    },
                    x: { grid: { display: false } }
                }
            }
        });
    }
});
