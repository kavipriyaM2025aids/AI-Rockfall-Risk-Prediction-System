import sys
import os

new_func = """async function renderAnalyticsUI() {
    showLoading(true);
    const container = document.getElementById('view-analytics');
    
    try {
        const historyRes = await fetch(`${API_URL}/history`).then(r => r.json()).catch(() => []);
        
        let riskCounts = { HIGH: 0, MEDIUM: 0, LOW: 0, UNKNOWN: 0 };
        let dates = {};
        
        historyRes.forEach(h => {
            let status = h.risk_status || 'UNKNOWN';
            if (riskCounts[status] !== undefined) {
                riskCounts[status]++;
            } else {
                riskCounts['UNKNOWN']++;
            }
            
            let dateStr = new Date(h.timestamp).toLocaleDateString();
            if(!dates[dateStr]) dates[dateStr] = 0;
            dates[dateStr]++;
        });

        // Prepare chart data
        const trendLabels = Object.keys(dates).reverse();
        const trendData = Object.values(dates).reverse();
        
        container.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
                <div>
                    <h2 style="font-size:1.8rem; font-weight:700; margin-bottom:4px;">Analytics Dashboard</h2>
                    <p style="color:var(--text-muted); font-size:0.9rem;">Metrics, trends and distributions.</p>
                </div>
            </div>
            
            <div class="grid-2 mb-8">
                <div class="glass-panel" style="padding:24px; display:flex; flex-direction:column; height:350px;">
                    <h3 style="font-size:1rem; font-weight:600; margin-bottom:16px;">Prediction Trends</h3>
                    <div style="flex:1; width:100%; position:relative;">
                        <canvas id="chart-trends"></canvas>
                    </div>
                </div>
                <div class="glass-panel" style="padding:24px; display:flex; flex-direction:column; height:350px;">
                    <h3 style="font-size:1rem; font-weight:600; margin-bottom:16px;">Risk Distribution</h3>
                    <div style="flex:1; width:100%; position:relative;">
                        <canvas id="chart-risk"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="grid-3">
                <div class="glass-panel" style="padding:24px;">
                    <h4 style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:12px;">Total Predictions Analyzed</h4>
                    <div style="font-size:1.8rem; font-weight:bold; color:var(--text-main);">${historyRes.length}</div>
                </div>
                <div class="glass-panel" style="padding:24px;">
                    <h4 style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:12px;">High Risk Incidents</h4>
                    <div style="font-size:1.8rem; font-weight:bold; color:var(--danger);">${riskCounts.HIGH}</div>
                </div>
                <div class="glass-panel" style="padding:24px;">
                    <h4 style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:12px;">XGBoost Risk Assessment</h4>
                    <div style="font-size:0.85rem; color:var(--text-main);">Experimental rule-based fallback active pending model retraining on new dataset.</div>
                </div>
            </div>
        `;
        
        if (window.lucide) lucide.createIcons();
        
        // Render Charts after DOM updates
        setTimeout(() => {
            const ctxTrends = document.getElementById('chart-trends');
            const ctxRisk = document.getElementById('chart-risk');
            
            if (ctxTrends && window.Chart) {
                new Chart(ctxTrends, {
                    type: 'line',
                    data: {
                        labels: trendLabels.length > 0 ? trendLabels : ['No Data'],
                        datasets: [{
                            label: 'Predictions',
                            data: trendData.length > 0 ? trendData : [0],
                            borderColor: '#06B6D4',
                            backgroundColor: 'rgba(6, 182, 212, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { stepSize: 1, color: '#94A3B8' } },
                            x: { grid: { display: false }, ticks: { color: '#94A3B8' } }
                        }
                    }
                });
            }
            
            if (ctxRisk && window.Chart) {
                new Chart(ctxRisk, {
                    type: 'doughnut',
                    data: {
                        labels: ['High Risk', 'Medium Risk', 'Low Risk', 'Unknown'],
                        datasets: [{
                            data: [riskCounts.HIGH, riskCounts.MEDIUM, riskCounts.LOW, riskCounts.UNKNOWN],
                            backgroundColor: ['#EF4444', '#F59E0B', '#10B981', '#94A3B8'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom', labels: { color: '#F8FAFC' } }
                        }
                    }
                });
            }
        }, 100);

    } catch (e) {
        console.error(e);
        container.innerHTML = `<div class="badge danger">Error loading analytics data</div>`;
    } finally {
        showLoading(false);
    }
}"""

with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('function renderAnalyticsUI()'):
        start_idx = i
    if start_idx != -1 and line.startswith('// ============================================================================'):
        if 'REPORTS' in lines[i+1]:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [new_func + '\n\n'] + lines[end_idx:]
    with open('frontend/js/app.js', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Updated renderAnalyticsUI successfully.')
else:
    print('Could not find boundaries.')
