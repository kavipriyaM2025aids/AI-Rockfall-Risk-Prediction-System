import sys

with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = -1
end = -1
for i, line in enumerate(lines):
    if 'let html = `' in line and 'ROCKGUARD AI Dashboard' in ''.join(lines[i:i+5]):
        start = i
        break
for i in range(start, len(lines)):
    if 'container.innerHTML = html;' in lines[i]:
        end = i - 1
        break

if start == -1 or end == -1:
    print('Failed to find replace boundaries')
    sys.exit(1)

new_html = r'''
        let html = `
            <header style="background: linear-gradient(135deg, #f8f7ff 0%, #ede9fe 100%); padding:32px; border-radius:24px; margin-bottom:32px; border:1px solid var(--brand-light-violet); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:24px; position:relative; overflow:hidden;">
                <div style="position:absolute; top:-50px; right:10%; width:200px; height:200px; background:radial-gradient(circle, var(--brand-light-pink) 0%, transparent 70%); opacity:0.3; pointer-events:none;"></div>
                <div style="position:absolute; bottom:-50px; left:10%; width:200px; height:200px; background:radial-gradient(circle, var(--brand-light-violet) 0%, transparent 70%); opacity:0.3; pointer-events:none;"></div>
                <div style="position:relative; z-index:1;">
                    <h2 style="font-size:2.2rem; font-weight:800; color:var(--text-main); margin-bottom:8px;">ROCKGUARD AI<br><span style="font-size:1.4rem; font-weight:500; color:var(--brand-primary);">Smart Rockfall Prediction & Safety Monitoring</span></h2>
                    <p style="color:var(--text-muted); font-size:0.95rem; max-width:600px; line-height:1.5;">AI-powered mine image analysis, experimental risk assessment, environmental monitoring and safety intelligence.</p>
                </div>
                <div style="background:var(--bg-main); padding:16px 24px; border-radius:16px; border:1px solid var(--glass-border); box-shadow:0 4px 20px rgba(139, 92, 246, 0.05); min-width:250px; position:relative; z-index:1;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--success); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                        <div style="width:8px; height:8px; border-radius:50%; background:var(--success); box-shadow:0 0 8px var(--success);"></div> SYSTEM OPERATIONAL
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--glass-border); padding-bottom:8px; margin-bottom:8px;">
                        <span style="font-size:0.85rem; color:var(--text-muted);">YOLOv11</span>
                        <span style="font-size:0.75rem; font-weight:bold; color:${isModelReady ? 'var(--success)' : 'var(--danger)'}">${isModelReady ? 'READY' : 'OFFLINE'}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.85rem; color:var(--text-muted);">PostgreSQL</span>
                        <span style="font-size:0.75rem; font-weight:bold; color:${isDbConnected ? 'var(--success)' : 'var(--danger)'}">${isDbConnected ? 'CONNECTED' : 'OFFLINE'}</span>
                    </div>
                </div>
            </header>
            
            <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">KEY PERFORMANCE INDICATORS</div>
            <div class="grid-4 mb-8">
                <div class="glass-panel stat-card" style="position:relative; overflow:hidden; padding:24px;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, var(--brand-light-violet) 0%, transparent 70%); opacity:0.5; pointer-events:none;"></div>
                    <div class="stat-header" style="margin-bottom:16px;">
                        <div style="background:var(--brand-light-violet); border-radius:12px; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
                            <i data-lucide="activity" class="stat-icon" style="width:20px; height:20px; color:var(--brand-primary);"></i>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted); font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:4px;">TOTAL PREDICTIONS</div>
                    <div class="stat-value" style="font-size:2.2rem;">${historyRes.length}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px;">Stored image analyses</div>
                </div>
                
                <div class="glass-panel stat-card" style="position:relative; overflow:hidden; padding:24px;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, var(--brand-light-pink) 0%, transparent 70%); opacity:0.5; pointer-events:none;"></div>
                    <div class="stat-header" style="margin-bottom:16px;">
                        <div style="background:var(--brand-light-pink); border-radius:12px; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
                            <i data-lucide="target" class="stat-icon" style="color:var(--brand-secondary); width:20px; height:20px;"></i>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted); font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:4px;">OBJECTS DETECTED</div>
                    <div class="stat-value text-brand" style="font-size:2.2rem; color:var(--brand-secondary);">${objectsDetected}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px;">Total historical detections</div>
                </div>

                <div class="glass-panel stat-card" style="position:relative; overflow:hidden; padding:24px;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, #E0E7FF 0%, transparent 70%); opacity:0.5; pointer-events:none;"></div>
                    <div class="stat-header" style="margin-bottom:16px;">
                        <div style="background:#E0E7FF; border-radius:12px; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
                            <i data-lucide="database" class="stat-icon" style="color:#6366F1; width:20px; height:20px;"></i>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted); font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:4px;">DATABASE STATUS</div>
                    <div class="stat-value ${isDbConnected ? 'success' : 'danger'}" style="font-size:1.8rem; margin-top:4px;">${isDbConnected ? 'Connected' : 'Offline'}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px;">PostgreSQL connection</div>
                </div>

                <div class="glass-panel stat-card" style="position:relative; overflow:hidden; padding:24px;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, #FCE7F3 0%, transparent 70%); opacity:0.5; pointer-events:none;"></div>
                    <div class="stat-header" style="margin-bottom:16px;">
                        <div style="background:#FCE7F3; border-radius:12px; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
                            <i data-lucide="cpu" class="stat-icon" style="color:#DB2777; width:20px; height:20px;"></i>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted); font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:4px;">YOLOv11 STATUS</div>
                    <div class="stat-value ${isModelReady ? 'success' : 'danger'}" style="font-size:1.8rem; margin-top:4px;">${isModelReady ? 'Ready' : 'Unavailable'}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px;">Object detection engine</div>
                </div>
            </div>

            <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">QUICK ACTIONS</div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:24px; margin-bottom:32px;">
                <div class="glass-panel stat-card" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; padding:24px; transition:transform 0.2s, box-shadow 0.2s;" onclick="document.querySelector('[data-view=prediction]').click()">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <div style="background:var(--brand-light-violet); padding:12px; border-radius:12px;"><i data-lucide="camera" style="color:var(--brand-primary);"></i></div>
                        <div>
                            <h4 style="font-weight:bold; margin-bottom:4px; font-size:1rem;">Upload Image</h4>
                            <p style="font-size:0.85rem; color:var(--text-muted);">Analyze a mine image</p>
                        </div>
                    </div>
                    <i data-lucide="arrow-right" style="color:var(--text-muted);"></i>
                </div>
                <div class="glass-panel stat-card" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; padding:24px; transition:transform 0.2s, box-shadow 0.2s;" onclick="document.querySelector('[data-view=simulation]').click()">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <div style="background:var(--brand-light-pink); padding:12px; border-radius:12px;"><i data-lucide="play-square" style="color:var(--brand-secondary);"></i></div>
                        <div>
                            <h4 style="font-weight:bold; margin-bottom:4px; font-size:1rem;">Dataset Simulation</h4>
                            <p style="font-size:0.85rem; color:var(--text-muted);">Process next dataset image</p>
                        </div>
                    </div>
                    <i data-lucide="arrow-right" style="color:var(--text-muted);"></i>
                </div>
                <div class="glass-panel stat-card" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; padding:24px; transition:transform 0.2s, box-shadow 0.2s;" onclick="document.querySelector('[data-view=history]').click()">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <div style="background:#E0E7FF; padding:12px; border-radius:12px;"><i data-lucide="history" style="color:#6366F1;"></i></div>
                        <div>
                            <h4 style="font-weight:bold; margin-bottom:4px; font-size:1rem;">Prediction History</h4>
                            <p style="font-size:0.85rem; color:var(--text-muted);">View previous analyses</p>
                        </div>
                    </div>
                    <i data-lucide="arrow-right" style="color:var(--text-muted);"></i>
                </div>
            </div>

            <div class="grid-2 mb-8">
                <div>
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">LATEST ANALYSIS</div>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">Most recent image processed by ROCKGUARD AI</p>
                    <div class="glass-panel" style="padding:24px; border:1px solid var(--brand-light-violet);">
                        ${latest ? `
                            <div style="position:relative; margin-bottom:24px;">
                                <img src="${HOST_URL}/api/images/${latest.image_name}" onerror="this.src=''" style="width:100%; height:250px; object-fit:cover; border-radius:16px; border:1px solid var(--brand-light-violet); box-shadow:0 8px 24px rgba(139,92,246,0.1);">
                                <div style="position:absolute; top:12px; left:12px; background:rgba(255,255,255,0.9); padding:6px 12px; border-radius:8px; font-size:0.75rem; font-weight:bold; color:var(--brand-primary); box-shadow:0 2px 8px rgba(0,0,0,0.1); border:1px solid var(--glass-border);">${latest.source.toUpperCase() === 'USER UPLOAD' ? 'USER UPLOAD' : 'DATASET'}</div>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                                <div>
                                    <h4 style="font-weight:bold; font-size:1.2rem;">${latest.image_name}</h4>
                                    <p style="font-size:0.85rem; color:var(--text-muted);">${new Date(latest.timestamp).toLocaleString()}</p>
                                </div>
                                <div class="badge ${latest.risk_status === 'HIGH' ? 'danger' : latest.risk_status === 'MEDIUM' ? 'warning' : 'info'}" style="padding:8px 16px; font-size:0.85rem; font-weight:bold; border-radius:12px;">${latest.risk_status || 'NOT_AVAILABLE'}</div>
                            </div>
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; border-top:1px solid var(--glass-border); padding-top:16px;">
                                <div style="background:var(--bg-main); padding:12px; border-radius:12px;">
                                    <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:bold; margin-bottom:4px;">Detections</div>
                                    <div style="font-size:1.2rem; font-weight:bold;">${(JSON.parse(latest.detected_classes || '[]')).length}</div>
                                </div>
                                <div style="background:var(--bg-main); padding:12px; border-radius:12px;">
                                    <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:bold; margin-bottom:4px;">Max Confidence</div>
                                    <div style="font-size:1.2rem; font-weight:bold; color:var(--brand-primary);">${(JSON.parse(latest.confidence || '[]')).length > 0 ? (Math.max(...JSON.parse(latest.confidence || '[]')) * 100).toFixed(1) + '%' : '-'}</div>
                                </div>
                            </div>
                        ` : `
                            <div style="background: var(--bg-main); padding: 48px; border-radius: 16px; text-align:center; border:1px dashed var(--glass-border);">
                                <i data-lucide="image-off" style="width:48px;height:48px;color:var(--text-muted);margin:0 auto 16px;"></i>
                                <p style="font-weight:500; font-size:1rem;">No prediction available yet.</p>
                            </div>
                        `}
                    </div>
                </div>

                <div>
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">AI ANALYSIS SUMMARY</div>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">System intelligence components overview</p>

                    <div class="glass-panel" style="padding:24px; display:flex; flex-direction:column; gap:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:16px; border-bottom:1px solid var(--glass-border);">
                            <div style="display:flex; align-items:center; gap:12px;">
                                <div style="background:var(--brand-light-violet); border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="cpu" style="width:18px;height:18px;color:var(--brand-primary);"></i>
                                </div>
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">YOLOv11</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Object detection engine</div>
                                </div>
                            </div>
                            <div style="font-size:0.75rem; font-weight:bold; color:${isModelReady ? 'var(--success)' : 'var(--danger)'};">${isModelReady ? 'READY' : 'UNAVAILABLE'}</div>
                        </div>

                        <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:16px; border-bottom:1px solid var(--glass-border);">
                            <div style="display:flex; align-items:center; gap:12px;">
                                <div style="background:var(--brand-light-pink); border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="zap" style="width:18px;height:18px;color:var(--brand-secondary);"></i>
                                </div>
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">XGBoost</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Experimental risk layer</div>
                                </div>
                            </div>
                            <div style="font-size:0.75rem; font-weight:bold; color:var(--success);">AVAILABLE</div>
                        </div>

                        <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:16px; border-bottom:1px solid var(--glass-border);">
                            <div style="display:flex; align-items:center; gap:12px;">
                                <div style="background:#E0E7FF; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="git-branch" style="width:18px;height:18px;color:#6366F1;"></i>
                                </div>
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">SHAP</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Explainability</div>
                                </div>
                            </div>
                            <div style="font-size:0.75rem; font-weight:bold; color:var(--success);">AVAILABLE</div>
                        </div>

                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="display:flex; align-items:center; gap:12px;">
                                <div style="background:#FEF3C7; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="cloud" style="width:18px;height:18px;color:#D97706;"></i>
                                </div>
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">Weather</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Environmental context</div>
                                </div>
                            </div>
                            <div style="font-size:0.75rem; font-weight:bold; color:${weather && !weather.error ? 'var(--success)' : 'var(--text-muted)'};">${weather && !weather.error ? 'CONFIGURED' : 'NOT CONFIGURED'}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid-3 mb-8">
                <div class="glass-panel" style="padding:24px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:24px; align-self:flex-start;">RISK ASSESSMENT</div>
                    ${latest && latest.risk_status ? `
                        <div style="width:120px; height:120px; border-radius:50%; border:8px solid ${latest.risk_status === 'HIGH' ? 'var(--danger)' : latest.risk_status === 'MEDIUM' ? 'var(--warning)' : 'var(--success)'}; display:flex; align-items:center; justify-content:center; margin-bottom:24px;">
                            <div style="text-align:center;">
                                <div style="font-weight:bold; font-size:1.2rem; color:var(--text-main);">${latest.risk_status}</div>
                                <div style="font-size:0.6rem; color:var(--text-muted); text-transform:uppercase;">Experimental</div>
                            </div>
                        </div>
                        <h4 style="font-weight:bold; font-size:1rem; margin-bottom:4px;">XGBoost Risk Assessment</h4>
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">Rule-derived experimental model based on detection and environmental features.</p>
                    ` : `
                        <div style="width:120px; height:120px; border-radius:50%; border:8px solid var(--glass-border); display:flex; align-items:center; justify-content:center; margin-bottom:24px;">
                            <div style="text-align:center;">
                                <div style="font-weight:bold; font-size:0.8rem; color:var(--text-muted);">N/A</div>
                            </div>
                        </div>
                        <h4 style="font-weight:bold; font-size:1rem; margin-bottom:4px;">Risk Assessment</h4>
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">Not Available</p>
                    `}
                    <p style="font-size:0.7rem; color:var(--text-muted); font-style:italic; border-top:1px solid var(--glass-border); padding-top:16px; width:100%;">Experimental and not scientifically validated for real-world rockfall prediction.</p>
                </div>

                <div class="glass-panel" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:24px;">ENVIRONMENTAL MONITORING</div>
                    ${weather && !weather.error ? `
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:16px;">
                            <div style="background:var(--brand-light-violet); padding:16px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                                <div style="background:#FFFFFF; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="thermometer" style="color:var(--brand-primary); width:16px; height:16px;"></i>
                                </div>
                                <div>
                                    <div style="font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; font-weight:600;">Temperature</div>
                                    <div style="font-weight:bold; font-size:1rem; color:var(--text-main);">${weather.temperature}°C</div>
                                </div>
                            </div>
                            <div style="background:var(--brand-light-pink); padding:16px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                                <div style="background:#FFFFFF; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="wind" style="color:var(--brand-secondary); width:16px; height:16px;"></i>
                                </div>
                                <div>
                                    <div style="font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; font-weight:600;">Wind Speed</div>
                                    <div style="font-weight:bold; font-size:1rem; color:var(--text-main);">${weather.wind_speed} m/s</div>
                                </div>
                            </div>
                            <div style="background:#E0E7FF; padding:16px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                                <div style="background:#FFFFFF; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="droplets" style="color:#6366F1; width:16px; height:16px;"></i>
                                </div>
                                <div>
                                    <div style="font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; font-weight:600;">Humidity</div>
                                    <div style="font-weight:bold; font-size:1rem; color:var(--text-main);">${weather.humidity}%</div>
                                </div>
                            </div>
                            <div style="background:#FEF3C7; padding:16px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                                <div style="background:#FFFFFF; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="cloud" style="color:#D97706; width:16px; height:16px;"></i>
                                </div>
                                <div>
                                    <div style="font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; font-weight:600;">Condition</div>
                                    <div style="font-weight:bold; font-size:1rem; color:var(--text-main);">${weather.weather_condition}</div>
                                </div>
                            </div>
                        </div>
                    ` : `
                        <div style="background: var(--bg-main); padding: 24px; border-radius: 12px; margin-bottom: 16px; border: 1px dashed var(--glass-border); text-align:center;">
                            <i data-lucide="cloud-off" style="color:var(--text-muted); width:32px; height:32px; margin-bottom:8px;"></i>
                            <p style="font-weight: 500; color:var(--text-muted); font-size:0.9rem;">Weather service not configured</p>
                        </div>
                    `}
                    <div style="background:var(--bg-main); border:1px solid var(--glass-border); border-radius:12px; padding:16px; margin-top:16px; display:flex; align-items:center; justify-content:space-between;">
                        <div>
                            <div style="font-size:0.7rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase;">LOCATION</div>
                            <div style="font-weight:500; font-size:0.9rem; margin-top:4px;">${locationStatus.includes(',') ? locationStatus : (locationStatus === 'Pending permission...' ? 'Pending permission...' : 'Location permission required')}</div>
                        </div>
                        <div style="background:var(--brand-light-violet); width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center;"><i data-lucide="map-pin" style="width:16px; height:16px; color:var(--brand-primary);"></i></div>
                    </div>
                </div>

                <div class="glass-panel" style="padding:24px; display:flex; flex-direction:column;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:24px;">MINE LOCATION</div>
                    <div style="flex:1; border-radius:12px; overflow:hidden; border:1px solid var(--glass-border); background:var(--bg-main); position:relative; min-height:200px;" id="map-container">
                        ${locationStatus.includes(',') ? `` : `<div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; flex-direction:column; color:var(--text-muted);"><i data-lucide="map" style="width:32px; height:32px; margin-bottom:8px;"></i><p style="font-size:0.85rem;">Location data unavailable</p></div>`}
                    </div>
                </div>
            </div>

            <div class="grid-2 mb-8">
                <div class="glass-panel" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:24px;">RECENT ACTIVITY</div>
                    <div style="display:flex; flex-direction:column; gap:16px; margin-bottom:24px;">
                        ${historyRes.slice(0,5).map(h => `
                            <div style="display:flex; align-items:flex-start; gap:16px;">
                                <div style="width:12px; height:12px; border-radius:50%; background:var(--brand-primary); margin-top:6px; box-shadow:0 0 8px rgba(139,92,246,0.3);"></div>
                                <div style="flex:1; border-bottom:1px solid var(--glass-border); padding-bottom:12px;">
                                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                                        <span style="font-weight:bold; font-size:0.95rem;">${h.image_name}</span>
                                        <span style="font-size:0.85rem; color:var(--text-muted);">${new Date(h.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span style="font-size:0.85rem; color:var(--text-muted);">${h.source}</span>
                                        <span style="font-size:0.75rem; font-weight:bold; color:${h.risk_status === 'HIGH' ? 'var(--danger)' : h.risk_status === 'MEDIUM' ? 'var(--warning)' : 'var(--success)'};">${h.risk_status || '-'}</span>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                        ${historyRes.length === 0 ? `<div style="text-align:center; padding:24px; color:var(--text-muted); font-size:0.85rem;">No recent activity</div>` : ''}
                    </div>
                    <button class="btn btn-secondary" style="width:100%; border-radius:12px; background:var(--brand-light-violet); color:var(--brand-primary);" onclick="document.querySelector('[data-view=history]').click()">View Full History &rarr;</button>
                </div>

                <div class="glass-panel" style="padding:24px;">
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">MODEL PERFORMANCE</div>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:24px;">YOLOv11 Test Set Metrics (Object detection evaluation only)</p>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-bottom:24px;">
                        <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:16px; border-radius:12px;">
                            <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:bold; margin-bottom:4px;">Precision</div>
                            <div style="font-size:1.5rem; font-weight:bold;">79.1%</div>
                        </div>
                        <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:16px; border-radius:12px;">
                            <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:bold; margin-bottom:4px;">Recall</div>
                            <div style="font-size:1.5rem; font-weight:bold;">24.0%</div>
                        </div>
                        <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:16px; border-radius:12px;">
                            <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:bold; margin-bottom:4px;">mAP@50</div>
                            <div style="font-size:1.5rem; font-weight:bold;">26.6%</div>
                        </div>
                        <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:16px; border-radius:12px;">
                            <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; font-weight:bold; margin-bottom:4px;">mAP@50-95</div>
                            <div style="font-size:1.5rem; font-weight:bold;">15.2%</div>
                        </div>
                    </div>
                    <button class="btn btn-secondary" style="width:100%; border-radius:12px; background:var(--brand-light-pink); color:var(--brand-secondary);" onclick="document.querySelector('[data-view=model]').click()">View Full Performance &rarr;</button>
                </div>
            </div>

            <div style="font-size:0.75rem; font-weight:bold; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">SYSTEM HEALTH</div>
            <div style="display:flex; flex-wrap:wrap; gap:16px; margin-bottom:32px;">
                <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:12px 24px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:0.85rem; font-weight:bold;">YOLOv11</span>
                    <span style="font-size:0.75rem; color:${isModelReady ? 'var(--success)' : 'var(--danger)'}; display:flex; align-items:center; gap:4px;"><div style="width:6px;height:6px;border-radius:50%;background:${isModelReady ? 'var(--success)' : 'var(--danger)'};"></div> ${isModelReady ? 'Ready' : 'Unavailable'}</span>
                </div>
                <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:12px 24px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:0.85rem; font-weight:bold;">PostgreSQL</span>
                    <span style="font-size:0.75rem; color:${isDbConnected ? 'var(--success)' : 'var(--danger)'}; display:flex; align-items:center; gap:4px;"><div style="width:6px;height:6px;border-radius:50%;background:${isDbConnected ? 'var(--success)' : 'var(--danger)'};"></div> ${isDbConnected ? 'Connected' : 'Offline'}</span>
                </div>
                <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:12px 24px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:0.85rem; font-weight:bold;">XGBoost</span>
                    <span style="font-size:0.75rem; color:var(--success); display:flex; align-items:center; gap:4px;"><div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div> Available</span>
                </div>
                <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:12px 24px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:0.85rem; font-weight:bold;">SHAP</span>
                    <span style="font-size:0.75rem; color:var(--success); display:flex; align-items:center; gap:4px;"><div style="width:6px;height:6px;border-radius:50%;background:var(--success);"></div> Available</span>
                </div>
                <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:12px 24px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:0.85rem; font-weight:bold;">Weather API</span>
                    <span style="font-size:0.75rem; color:${weather && !weather.error ? 'var(--success)' : 'var(--text-muted)'}; display:flex; align-items:center; gap:4px;"><div style="width:6px;height:6px;border-radius:50%;background:${weather && !weather.error ? 'var(--success)' : 'var(--text-muted)'};"></div> ${weather && !weather.error ? 'Configured' : 'Not Configured'}</span>
                </div>
                <div style="background:var(--bg-main); border:1px solid var(--glass-border); padding:12px 24px; border-radius:12px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:0.85rem; font-weight:bold;">Geolocation</span>
                    <span style="font-size:0.75rem; color:${locationStatus.includes(',') ? 'var(--success)' : 'var(--warning)'}; display:flex; align-items:center; gap:4px;"><div style="width:6px;height:6px;border-radius:50%;background:${locationStatus.includes(',') ? 'var(--success)' : 'var(--warning)'};"></div> ${locationStatus.includes(',') ? 'Active' : 'Permission Required'}</span>
                </div>
            </div>
        `;
'''

leaflet_logic = r'''
        if (locationStatus.includes(',')) {
            setTimeout(() => {
                try {
                    const coords = locationStatus.split(',');
                    const mapContainer = document.getElementById('map-container');
                    if (mapContainer && window.L) {
                        const map = L.map('map-container').setView([parseFloat(coords[0]), parseFloat(coords[1])], 13);
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                        L.marker([parseFloat(coords[0]), parseFloat(coords[1])]).addTo(map);
                    }
                } catch (e) {
                    console.error("Map load error:", e);
                }
            }, 200);
        }
'''

new_content = lines[:start] + [new_html] + lines[end:end+1] + [leaflet_logic] + lines[end+1:]

with open('frontend/js/app.js', 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print('Successfully replaced dashboard logic.')
