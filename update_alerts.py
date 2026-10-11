import sys

with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '// ---------------- ALERTS ----------------'
end_marker = '// ---------------- SETTINGS ----------------'

if start_marker not in content or end_marker not in content:
    print('Failed to find markers')
    sys.exit(1)

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

new_function = r'''// ---------------- ALERTS ----------------
async function renderAlerts() {
    showLoading(true);
    const container = document.getElementById('view-alerts');
    try {
        const [historyRes, statusRes] = await Promise.all([
            fetch(`${API_URL}/history`).then(r => r.json()).catch(() => []),
            fetch(`${API_URL}/status`).then(r => r.json()).catch(() => ({}))
        ]);
        
        let highRiskCount = 0;
        if (Array.isArray(historyRes)) {
            historyRes.forEach(h => {
                if (h.risk_status === 'HIGH') highRiskCount++;
            });
        }

        let html = `
            <header style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                <div>
                    <h2>ALERT CENTER</h2>
                    <p>Real-time safety notifications and system risk monitoring</p>
                </div>
                <div style="background:var(--bg-main); padding:8px 16px; border-radius:20px; border:1px solid var(--glass-border); display:flex; align-items:center; gap:8px; font-size:0.75rem; font-weight:bold; color:var(--brand-primary); letter-spacing:1px; box-shadow:0 2px 10px rgba(139, 92, 246, 0.05);">
                    <div style="width:8px; height:8px; border-radius:50%; background:var(--brand-primary); box-shadow:0 0 8px var(--brand-primary);"></div> SYSTEM MONITORING
                </div>
            </header>

            <div class="grid-4 mb-8">
                <div class="glass-panel stat-card" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">ACTIVE ALERTS</div>
                    <div style="font-size:2rem; font-weight:bold; color:var(--text-main);">0</div>
                </div>
                <div class="glass-panel stat-card" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">VALIDATED ALERTS</div>
                    <div style="font-size:2rem; font-weight:bold; color:var(--text-main);">0</div>
                </div>
                <div class="glass-panel stat-card" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">EXPERIMENTAL RISKS</div>
                    <div style="font-size:2rem; font-weight:bold; color:var(--brand-secondary);">${Array.isArray(historyRes) && historyRes.length > 0 ? highRiskCount : 'N/A'}</div>
                </div>
                <div class="glass-panel stat-card" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">SYSTEM STATUS</div>
                    <div style="font-size:1.2rem; font-weight:bold; color:var(--success); margin-top:8px;">MONITORING</div>
                </div>
            </div>

            <div class="glass-panel text-center mb-8" style="padding: 48px; border: 1px solid var(--glass-border);">
                <div style="width:80px; height:80px; background:var(--bg-main); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 24px; box-shadow:0 8px 32px rgba(16, 185, 129, 0.15);">
                    <i data-lucide="shield-check" style="width:40px;height:40px;color:var(--success);"></i>
                </div>
                <h3 class="text-xl font-bold mb-2" style="color:var(--text-main); text-transform:uppercase; letter-spacing:1px;">NO ACTIVE VALIDATED ALERTS</h3>
                <p class="text-muted" style="max-width:500px; margin:0 auto 32px;">No validated risk or alert condition is currently available from the system.</p>
                
                <div style="border-top:1px solid var(--glass-border); padding-top:32px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">SYSTEM IS MONITORING</div>
                    <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
                        <div style="background:var(--bg-main); padding:8px 16px; border-radius:12px; border:1px solid var(--glass-border); text-align:left; display:flex; align-items:center; gap:8px;">
                            <div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div>
                            <div>
                                <div style="font-weight:bold; font-size:0.85rem;">YOLOv11</div>
                                <div style="font-size:0.7rem; color:var(--text-muted);">Object Detection</div>
                            </div>
                        </div>
                        <div style="background:var(--bg-main); padding:8px 16px; border-radius:12px; border:1px solid var(--glass-border); text-align:left; display:flex; align-items:center; gap:8px;">
                            <div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div>
                            <div>
                                <div style="font-weight:bold; font-size:0.85rem;">XGBoost</div>
                                <div style="font-size:0.7rem; color:var(--text-muted);">Experimental Risk Assessment</div>
                            </div>
                        </div>
                        <div style="background:var(--bg-main); padding:8px 16px; border-radius:12px; border:1px solid var(--glass-border); text-align:left; display:flex; align-items:center; gap:8px;">
                            <div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div>
                            <div>
                                <div style="font-weight:bold; font-size:0.85rem;">SHAP</div>
                                <div style="font-size:0.7rem; color:var(--text-muted);">Explainability</div>
                            </div>
                        </div>
                        <div style="background:var(--bg-main); padding:8px 16px; border-radius:12px; border:1px solid var(--glass-border); text-align:left; display:flex; align-items:center; gap:8px;">
                            <div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div>
                            <div>
                                <div style="font-weight:bold; font-size:0.85rem;">Weather</div>
                                <div style="font-size:0.7rem; color:var(--text-muted);">Environmental Context</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="glass-panel mb-8" style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(249, 168, 212, 0.05) 100%); border: 1px solid var(--brand-light-violet);">
                <div style="display:flex; align-items:flex-start; gap:16px;">
                    <div style="background:#FFFFFF; width:48px; height:48px; border-radius:16px; display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 4px 12px rgba(139, 92, 246, 0.1);">
                        <i data-lucide="info" style="color:var(--brand-primary); width:24px; height:24px;"></i>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-bottom:8px;">
                            <h3 class="text-lg font-bold" style="text-transform:uppercase; letter-spacing:1px; margin:0;">EXPERIMENTAL RISK ASSESSMENT</h3>
                            <div style="font-size:0.7rem; font-weight:bold; background:#FFFFFF; color:var(--brand-secondary); padding:4px 12px; border-radius:12px; border:1px solid var(--brand-light-pink); text-transform:uppercase;">NOT SCIENTIFICALLY VALIDATED</div>
                        </div>
                        <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.6; margin-bottom:12px;">Current risk outputs are generated by an experimental, rule-derived XGBoost model.</p>
                        <div style="background:#FFFFFF; padding:16px; border-radius:12px; font-size:0.8rem; color:var(--text-muted); border:1px solid var(--glass-border); line-height:1.6;">
                            "The XGBoost risk model is trained using rule-derived experimental labels rather than scientifically validated rockfall ground truth. Therefore, its performance metrics must not be interpreted as real-world rockfall prediction accuracy."
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid-2 mb-8">
                <div class="glass-panel">
                    <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">HOW ALERTS ARE GENERATED</h3>
                    <div style="display:flex; flex-direction:column; gap:8px;">
                        <div style="display:flex; align-items:center; gap:16px; background:var(--bg-main); padding:12px 16px; border-radius:12px; border:1px solid var(--glass-border);">
                            <i data-lucide="image" style="color:var(--text-main); width:20px; height:20px;"></i>
                            <div style="font-weight:bold; font-size:0.9rem;">Image Analysis</div>
                        </div>
                        <div style="display:flex; justify-content:center;"><div style="width:2px; height:16px; background:var(--glass-border);"></div></div>
                        <div style="display:flex; align-items:center; gap:16px; background:var(--bg-main); padding:12px 16px; border-radius:12px; border:1px solid var(--glass-border);">
                            <i data-lucide="cpu" style="color:var(--brand-primary); width:20px; height:20px;"></i>
                            <div style="font-weight:bold; font-size:0.9rem;">YOLOv11 Detection</div>
                        </div>
                        <div style="display:flex; justify-content:center;"><div style="width:2px; height:16px; background:var(--glass-border);"></div></div>
                        <div style="display:flex; align-items:center; gap:16px; background:var(--bg-main); padding:12px 16px; border-radius:12px; border:1px solid var(--glass-border);">
                            <i data-lucide="list" style="color:var(--info); width:20px; height:20px;"></i>
                            <div style="font-weight:bold; font-size:0.9rem;">Feature Extraction</div>
                        </div>
                        <div style="display:flex; justify-content:center;"><div style="width:2px; height:16px; background:var(--glass-border);"></div></div>
                        <div style="display:flex; align-items:center; gap:16px; background:var(--bg-main); padding:12px 16px; border-radius:12px; border:1px solid var(--glass-border);">
                            <i data-lucide="zap" style="color:var(--brand-secondary); width:20px; height:20px;"></i>
                            <div style="font-weight:bold; font-size:0.9rem;">Experimental Risk Assessment</div>
                        </div>
                        <div style="display:flex; justify-content:center;"><div style="width:2px; height:16px; background:var(--glass-border);"></div></div>
                        <div style="display:flex; align-items:center; gap:16px; background:var(--bg-main); padding:12px 16px; border-radius:12px; border:1px solid var(--glass-border);">
                            <i data-lucide="check-circle" style="color:var(--success); width:20px; height:20px;"></i>
                            <div style="font-weight:bold; font-size:0.9rem;">Validation Check</div>
                        </div>
                        <div style="display:flex; justify-content:center;"><div style="width:2px; height:16px; background:var(--glass-border);"></div></div>
                        <div style="display:flex; align-items:center; gap:16px; background:var(--bg-main); padding:12px 16px; border-radius:12px; border:1px solid var(--glass-border);">
                            <i data-lucide="bell" style="color:var(--danger); width:20px; height:20px;"></i>
                            <div style="font-weight:bold; font-size:0.9rem;">Alert Status</div>
                        </div>
                    </div>
                </div>

                <div class="glass-panel">
                    <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">RECENT RISK ACTIVITY</h3>
                    ${Array.isArray(historyRes) && historyRes.length > 0 ? `
                        <div style="display:flex; flex-direction:column; gap:16px;">
                            ${historyRes.slice(0, 5).map(h => `
                                <div style="display:flex; align-items:center; justify-content:space-between; padding-bottom:16px; border-bottom:1px solid var(--glass-border);">
                                    <div style="display:flex; align-items:center; gap:12px;">
                                        <div style="width:10px; height:10px; border-radius:50%; background:${h.risk_status === 'HIGH' ? 'var(--danger)' : h.risk_status === 'MEDIUM' ? 'var(--warning)' : 'var(--success)'};"></div>
                                        <div>
                                            <div style="font-weight:bold; font-size:0.9rem; margin-bottom:2px;">${h.image_name}</div>
                                            <div style="font-size:0.75rem; color:var(--text-muted);">${h.source ? h.source.toUpperCase() : 'UNKNOWN'}</div>
                                        </div>
                                    </div>
                                    <div style="text-align:right;">
                                        <div style="font-size:0.75rem; font-weight:bold; color:${h.risk_status === 'HIGH' ? 'var(--danger)' : h.risk_status === 'MEDIUM' ? 'var(--warning)' : 'var(--success)'}; margin-bottom:2px;">${h.risk_status || 'N/A'}</div>
                                        <div style="font-size:0.75rem; color:var(--text-muted);">${new Date(h.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    ` : `
                        <div style="text-align:center; padding:32px; border:1px dashed var(--glass-border); border-radius:12px; background:var(--bg-main);">
                            <i data-lucide="inbox" style="color:var(--text-muted); width:32px; height:32px; margin-bottom:8px;"></i>
                            <p style="font-size:0.85rem; color:var(--text-muted);">No risk activity available.</p>
                        </div>
                    `}
                </div>
            </div>
        `;
        container.innerHTML = html;
        if (window.lucide) lucide.createIcons();
    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="notice-box danger"><h3 class="text-danger font-bold text-xl mb-2">Connection Error</h3><p>Could not load alert data from backend.</p></div>`;
    } finally {
        showLoading(false);
    }
}

'''

new_content = content[:start_idx] + new_function + content[end_idx:]

with open('frontend/js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated app.js successfully.')
