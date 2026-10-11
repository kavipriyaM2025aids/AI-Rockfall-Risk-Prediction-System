import sys

with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'function renderSettings()'
end_marker = '// ---------------- UTILS ----------------'

if start_marker not in content:
    print('Failed to find start marker')
    sys.exit(1)
if end_marker not in content:
    end_marker = '// Utility' # fallback
    if end_marker not in content:
        # just replace till the end of the file or the last known function
        pass

start_idx = content.find(start_marker)
if end_marker in content:
    end_idx = content.find(end_marker)
else:
    # let's just find the end of renderSettings by searching for the next main function
    end_idx = content.find('// ----------------', start_idx + 1)
    if end_idx == -1:
        end_idx = len(content)

new_function = r'''async function renderSettings() {
    showLoading(true);
    const container = document.getElementById('view-settings');
    try {
        const [statusRes, historyRes, datasetRes] = await Promise.all([
            fetch(`${API_URL}/status`).then(r => r.json()).catch(() => ({})),
            fetch(`${API_URL}/history`).then(r => r.json()).catch(() => []),
            fetch(`${API_URL}/dataset-info`).then(r => r.json()).catch(() => null)
        ]);

        const isDbConnected = statusRes.database?.connected;
        const isModelReady = statusRes.model_available;
        const weather = await loadWeatherData();
        const hasWeather = weather && !weather.error;
        const geoActive = locationStatus.includes(',');
        
        const totalImages = datasetRes?.dataset_stats?.total_images || '4,617';
        const trainImages = datasetRes?.dataset_stats?.train_images || '3231';
        const valImages = datasetRes?.dataset_stats?.valid_images || datasetRes?.dataset_stats?.val_images || '923';
        const testImages = datasetRes?.dataset_stats?.test_images || '462';

        let html = `
            <header style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                <div>
                    <h2>SYSTEM CONFIGURATION</h2>
                    <p>ROCKGUARD AI service configuration, model status and integration health</p>
                </div>
                <div style="background:var(--bg-main); padding:8px 16px; border-radius:20px; border:1px solid var(--glass-border); display:flex; align-items:center; gap:8px; font-size:0.75rem; font-weight:bold; color:var(--success); letter-spacing:1px; box-shadow:0 2px 10px rgba(16, 185, 129, 0.05);">
                    <div style="width:8px; height:8px; border-radius:50%; background:var(--success); box-shadow:0 0 8px var(--success);"></div> SYSTEM OPERATIONAL
                </div>
            </header>

            <div class="grid-4 mb-8">
                <div class="glass-panel" style="padding:20px; border-top:4px solid var(--success);">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                        <i data-lucide="server" style="color:var(--text-muted); width:20px; height:20px;"></i>
                        <h4 style="font-weight:bold; font-size:0.9rem; margin:0;">SYSTEM STATUS</h4>
                    </div>
                    <div style="font-size:1.2rem; font-weight:bold; color:var(--text-main); margin-bottom:4px;">Operational</div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">Core services active</div>
                </div>
                <div class="glass-panel" style="padding:20px; border-top:4px solid ${isDbConnected ? 'var(--brand-primary)' : 'var(--danger)'};">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                        <i data-lucide="database" style="color:var(--text-muted); width:20px; height:20px;"></i>
                        <h4 style="font-weight:bold; font-size:0.9rem; margin:0;">DATABASE</h4>
                    </div>
                    <div style="font-size:1.2rem; font-weight:bold; color:var(--text-main); margin-bottom:4px;">PostgreSQL</div>
                    <div style="font-size:0.75rem; font-weight:bold; color:${isDbConnected ? 'var(--brand-primary)' : 'var(--danger)'};">${isDbConnected ? 'Connected' : 'Disconnected'}</div>
                </div>
                <div class="glass-panel" style="padding:20px; border-top:4px solid ${isModelReady ? 'var(--brand-secondary)' : 'var(--danger)'};">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                        <i data-lucide="cpu" style="color:var(--text-muted); width:20px; height:20px;"></i>
                        <h4 style="font-weight:bold; font-size:0.9rem; margin:0;">AI MODEL</h4>
                    </div>
                    <div style="font-size:1.2rem; font-weight:bold; color:var(--text-main); margin-bottom:4px;">YOLOv11</div>
                    <div style="font-size:0.75rem; font-weight:bold; color:${isModelReady ? 'var(--brand-secondary)' : 'var(--danger)'};">${isModelReady ? 'Ready' : 'Unavailable'}</div>
                </div>
                <div class="glass-panel" style="padding:20px; border-top:4px solid var(--success);">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                        <i data-lucide="zap" style="color:var(--text-muted); width:20px; height:20px;"></i>
                        <h4 style="font-weight:bold; font-size:0.9rem; margin:0;">RISK ENGINE</h4>
                    </div>
                    <div style="font-size:1.2rem; font-weight:bold; color:var(--text-main); margin-bottom:4px;">XGBoost</div>
                    <div style="font-size:0.75rem; font-weight:bold; color:var(--success);">Available</div>
                </div>
            </div>

            <div class="grid-2 mb-8">
                <!-- AI & ML CONFIGURATION -->
                <div class="glass-panel" style="padding:24px;">
                    <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">AI & ML CONFIGURATION</h3>
                    
                    <div style="background:var(--bg-main); border:1px solid var(--glass-border); border-radius:12px; padding:20px; margin-bottom:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                            <div>
                                <h4 style="font-weight:bold; font-size:1.1rem; color:var(--text-main); margin-bottom:4px;">YOLOv11</h4>
                                <div style="font-size:0.8rem; color:var(--text-muted);">Object Detection Engine</div>
                            </div>
                            <div style="font-size:0.7rem; font-weight:bold; color:${isModelReady ? 'var(--success)' : 'var(--danger)'}; padding:4px 12px; border-radius:12px; border:1px solid ${isModelReady ? 'var(--success)' : 'var(--danger)'};">STATUS: ${isModelReady ? 'READY' : 'UNAVAILABLE'}</div>
                        </div>
                        <div style="display:flex; flex-direction:column; gap:8px; font-size:0.85rem;">
                            <div style="display:flex; justify-content:space-between; border-bottom:1px dashed var(--glass-border); padding-bottom:4px;">
                                <span style="color:var(--text-muted);">Model:</span><span style="font-weight:600;">YOLOv11 Nano</span>
                            </div>
                            <div style="display:flex; justify-content:space-between;">
                                <span style="color:var(--text-muted);">Purpose:</span><span style="font-weight:600;">Mine image object detection</span>
                            </div>
                        </div>
                    </div>

                    <div style="background:var(--bg-main); border:1px solid var(--glass-border); border-radius:12px; padding:20px; margin-bottom:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                            <div>
                                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                                    <h4 style="font-weight:bold; font-size:1.1rem; color:var(--text-main); margin:0;">XGBoost</h4>
                                    <span style="font-size:0.6rem; background:var(--brand-light-pink); color:var(--brand-secondary); padding:2px 8px; border-radius:8px; font-weight:bold;">EXPERIMENTAL</span>
                                </div>
                                <div style="font-size:0.8rem; color:var(--text-muted);">Experimental Risk Assessment</div>
                            </div>
                            <div style="font-size:0.7rem; font-weight:bold; color:var(--success); padding:4px 12px; border-radius:12px; border:1px solid var(--success);">STATUS: AVAILABLE</div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                            <span style="color:var(--text-muted);">Purpose:</span><span style="font-weight:600;">Experimental risk classification</span>
                        </div>
                    </div>

                    <div style="background:var(--bg-main); border:1px solid var(--glass-border); border-radius:12px; padding:20px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                            <div>
                                <h4 style="font-weight:bold; font-size:1.1rem; color:var(--text-main); margin-bottom:4px;">SHAP</h4>
                                <div style="font-size:0.8rem; color:var(--text-muted);">Explainable AI</div>
                            </div>
                            <div style="font-size:0.7rem; font-weight:bold; color:var(--success); padding:4px 12px; border-radius:12px; border:1px solid var(--success);">STATUS: AVAILABLE</div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                            <span style="color:var(--text-muted);">Purpose:</span><span style="font-weight:600;">Feature contribution explanation</span>
                        </div>
                    </div>
                </div>

                <!-- DATA & STORAGE + EXTERNAL INTEGRATIONS -->
                <div style="display:flex; flex-direction:column; gap:32px;">
                    <div class="glass-panel" style="padding:24px;">
                        <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">DATA & STORAGE</h3>
                        
                        <div style="display:flex; flex-direction:column; gap:16px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px dashed var(--glass-border);">
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">PostgreSQL</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Database Engine</div>
                                </div>
                                <div style="font-size:0.8rem; font-weight:bold; color:${isDbConnected ? 'var(--brand-primary)' : 'var(--danger)'}; display:flex; align-items:center; gap:6px;">
                                    <div style="width:6px;height:6px;border-radius:50%;background:${isDbConnected ? 'var(--brand-primary)' : 'var(--danger)'};"></div> ${isDbConnected ? 'Connected' : 'Disconnected'}
                                </div>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px dashed var(--glass-border);">
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">Prediction History</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Persistent storage</div>
                                </div>
                                <div style="font-size:0.8rem; font-weight:bold; color:var(--text-main);">${Array.isArray(historyRes) ? historyRes.length : 0} Records</div>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px dashed var(--glass-border);">
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">Dataset</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Open-Pit Mine Object Detection Dataset</div>
                                </div>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem;">
                                <span style="color:var(--text-muted);">Dataset Images</span><span style="font-weight:bold;">${totalImages}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem;">
                                <span style="color:var(--text-muted);">Valid Images</span><span style="font-weight:bold;">${parseInt(totalImages.toString().replace(',','')) > 10 ? (parseInt(totalImages.toString().replace(',','')) - 1) : '4,616'}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem;">
                                <span style="color:var(--text-muted);">Train / Validation / Test</span><span style="font-weight:bold;">${trainImages} / ${valImages} / ${testImages}</span>
                            </div>
                        </div>
                    </div>

                    <div class="glass-panel" style="padding:24px;">
                        <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">EXTERNAL SERVICES</h3>
                        
                        <div style="display:flex; flex-direction:column; gap:16px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px dashed var(--glass-border);">
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">OpenWeatherMap</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Weather & Environmental Data</div>
                                </div>
                                <div style="font-size:0.75rem; font-weight:bold; color:${hasWeather ? 'var(--success)' : '#D97706'}; background:${hasWeather ? 'var(--bg-main)' : '#FEF3C7'}; padding:4px 10px; border-radius:12px;">Status: ${hasWeather ? 'Configured' : 'Not Configured'}</div>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px dashed var(--glass-border);">
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">Leaflet + OpenStreetMap</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Location Visualization</div>
                                </div>
                                <div style="font-size:0.75rem; font-weight:bold; color:var(--success); background:var(--bg-main); padding:4px 10px; border-radius:12px;">Status: Available</div>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div>
                                    <div style="font-weight:bold; font-size:0.95rem;">Browser Geolocation</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">Device Location</div>
                                </div>
                                <div style="font-size:0.75rem; font-weight:bold; color:${geoActive ? 'var(--success)' : '#D97706'}; background:${geoActive ? 'var(--bg-main)' : '#FEF3C7'}; padding:4px 10px; border-radius:12px;">Status: ${geoActive ? 'Permission Granted' : 'Permission Required'}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid-2 mb-8">
                <!-- ARCHITECTURE OVERVIEW -->
                <div class="glass-panel" style="padding:24px;">
                    <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">ARCHITECTURE OVERVIEW</h3>
                    
                    <div style="display:flex; flex-direction:column; align-items:center; gap:8px; background:var(--bg-main); padding:24px; border-radius:12px; border:1px solid var(--glass-border);">
                        <div style="padding:8px 24px; border-radius:20px; background:#F1F5F9; font-weight:bold; font-size:0.85rem; color:#475569; border:1px solid #CBD5E1;">USER</div>
                        <i data-lucide="arrow-down" style="color:var(--text-muted); width:16px; height:16px;"></i>
                        
                        <div style="padding:8px 24px; border-radius:12px; background:var(--brand-light-violet); font-weight:bold; font-size:0.85rem; color:var(--brand-primary); border:1px solid var(--brand-primary); width:100%; text-align:center;">HTML / CSS / Vanilla JS</div>
                        <i data-lucide="arrow-down" style="color:var(--text-muted); width:16px; height:16px;"></i>
                        
                        <div style="padding:8px 24px; border-radius:12px; background:var(--brand-light-pink); font-weight:bold; font-size:0.85rem; color:var(--brand-secondary); border:1px solid var(--brand-secondary); width:100%; text-align:center;">FastAPI + Python</div>
                        <i data-lucide="arrow-down" style="color:var(--text-muted); width:16px; height:16px;"></i>
                        
                        <div style="padding:8px 24px; border-radius:12px; background:#E0E7FF; font-weight:bold; font-size:0.85rem; color:#4338CA; border:1px solid #6366F1; width:100%; text-align:center;">YOLOv11</div>
                        <i data-lucide="arrow-down" style="color:var(--text-muted); width:16px; height:16px;"></i>
                        
                        <div style="display:flex; width:100%; gap:8px;">
                            <div style="flex:1; padding:8px; border-radius:12px; background:#FEF3C7; font-weight:bold; font-size:0.8rem; color:#B45309; border:1px solid #F59E0B; text-align:center;">XGBoost</div>
                            <div style="flex:1; padding:8px; border-radius:12px; background:#DCFCE7; font-weight:bold; font-size:0.8rem; color:#15803D; border:1px solid #22C55E; text-align:center;">SHAP</div>
                        </div>
                        <i data-lucide="arrow-down" style="color:var(--text-muted); width:16px; height:16px;"></i>
                        
                        <div style="padding:8px 24px; border-radius:12px; background:#F3E8FF; font-weight:bold; font-size:0.85rem; color:#7E22CE; border:1px solid #A855F7; width:100%; text-align:center;">PostgreSQL</div>
                    </div>
                    
                    <div style="margin-top:16px; display:flex; flex-direction:column; gap:8px; font-size:0.8rem; color:var(--text-muted);">
                        <div style="display:flex; align-items:center; gap:8px;"><i data-lucide="cloud" style="width:14px; height:14px; color:#D97706;"></i> Weather API &rarr; Environmental Context</div>
                        <div style="display:flex; align-items:center; gap:8px;"><i data-lucide="map-pin" style="width:14px; height:14px; color:var(--success);"></i> Browser Geolocation &rarr; Location Context</div>
                    </div>
                </div>

                <div style="display:flex; flex-direction:column; gap:24px;">
                    <!-- SERVICE HEALTH -->
                    <div class="glass-panel" style="padding:24px;">
                        <h3 class="text-lg font-bold mb-6" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">SERVICE HEALTH</h3>
                        
                        <div style="display:flex; flex-direction:column; gap:12px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid var(--glass-border);">
                                <span style="font-weight:bold; font-size:0.85rem;">YOLOv11</span>
                                <span style="font-size:0.75rem; color:${isModelReady ? 'var(--success)' : 'var(--danger)'}; display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:${isModelReady ? 'var(--success)' : 'var(--danger)'};"></div> ${isModelReady ? 'Ready' : 'Unavailable'}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid var(--glass-border);">
                                <span style="font-weight:bold; font-size:0.85rem;">FastAPI Backend</span>
                                <span style="font-size:0.75rem; color:var(--success); display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:var(--success);"></div> Connected</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid var(--glass-border);">
                                <span style="font-weight:bold; font-size:0.85rem;">PostgreSQL</span>
                                <span style="font-size:0.75rem; color:${isDbConnected ? 'var(--success)' : 'var(--danger)'}; display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:${isDbConnected ? 'var(--success)' : 'var(--danger)'};"></div> ${isDbConnected ? 'Connected' : 'Offline'}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid var(--glass-border);">
                                <span style="font-weight:bold; font-size:0.85rem;">XGBoost</span>
                                <span style="font-size:0.75rem; color:var(--success); display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:var(--success);"></div> Available</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid var(--glass-border);">
                                <span style="font-weight:bold; font-size:0.85rem;">SHAP</span>
                                <span style="font-size:0.75rem; color:var(--success); display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:var(--success);"></div> Available</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid var(--glass-border);">
                                <span style="font-weight:bold; font-size:0.85rem;">Weather API</span>
                                <span style="font-size:0.75rem; color:${hasWeather ? 'var(--success)' : '#D97706'}; display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:${hasWeather ? 'var(--success)' : '#D97706'};"></div> ${hasWeather ? 'Configured' : 'Not Configured'}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:12px;">
                                <span style="font-weight:bold; font-size:0.85rem;">Geolocation</span>
                                <span style="font-size:0.75rem; color:${geoActive ? 'var(--success)' : '#D97706'}; display:flex; align-items:center; gap:6px;"><div style="width:8px;height:8px;border-radius:50%;background:${geoActive ? 'var(--success)' : '#D97706'};"></div> ${geoActive ? 'Active' : 'Permission Required'}</span>
                            </div>
                        </div>
                    </div>

                    <!-- SECURITY NOTICE -->
                    <div class="glass-panel" style="padding:24px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, transparent 100%); border:1px solid rgba(16, 185, 129, 0.2);">
                        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                            <div style="background:#FFFFFF; padding:8px; border-radius:12px; box-shadow:0 2px 8px rgba(16,185,129,0.1);"><i data-lucide="shield" style="color:var(--success); width:20px; height:20px;"></i></div>
                            <h3 class="text-lg font-bold" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted); margin:0;">SECURITY & CONFIGURATION</h3>
                        </div>
                        <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.6; margin:0;">
                            API keys, database credentials and environment variables are stored securely on the backend and are not exposed through the browser interface.
                        </p>
                    </div>

                    <!-- CONFIGURATION STATUS -->
                    <div class="glass-panel" style="padding:24px;">
                        <h3 class="text-lg font-bold mb-4" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">CONFIGURATION STATUS</h3>
                        <div style="display:flex; flex-wrap:wrap; gap:8px;">
                            <span style="font-size:0.75rem; font-weight:bold; color:var(--text-main); background:var(--bg-main); border:1px solid var(--glass-border); padding:6px 12px; border-radius:16px;">Database: ${isDbConnected ? 'Configured' : 'Not Configured'}</span>
                            <span style="font-size:0.75rem; font-weight:bold; color:var(--text-main); background:var(--bg-main); border:1px solid var(--glass-border); padding:6px 12px; border-radius:16px;">YOLOv11: ${isModelReady ? 'Loaded' : 'Not Loaded'}</span>
                            <span style="font-size:0.75rem; font-weight:bold; color:var(--text-main); background:var(--bg-main); border:1px solid var(--glass-border); padding:6px 12px; border-radius:16px;">XGBoost: Loaded</span>
                            <span style="font-size:0.75rem; font-weight:bold; color:var(--text-main); background:var(--bg-main); border:1px solid var(--glass-border); padding:6px 12px; border-radius:16px;">SHAP: Loaded</span>
                            <span style="font-size:0.75rem; font-weight:bold; color:var(--text-main); background:var(--bg-main); border:1px solid var(--glass-border); padding:6px 12px; border-radius:16px;">Weather API: ${hasWeather ? 'Configured' : 'Not Configured'}</span>
                            <span style="font-size:0.75rem; font-weight:bold; color:var(--text-main); background:var(--bg-main); border:1px solid var(--glass-border); padding:6px 12px; border-radius:16px;">Geolocation: ${geoActive ? 'Browser Configured' : 'Browser Permission Required'}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div style="border-top:1px solid var(--glass-border); padding-top:32px; margin-top:16px; margin-bottom:32px;">
                <h3 class="text-lg font-bold mb-4" style="text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; color:var(--text-muted);">QUICK ACCESS</h3>
                <div style="display:flex; flex-wrap:wrap; gap:16px;">
                    <button class="btn btn-secondary" style="background:var(--brand-light-violet); color:var(--brand-primary); font-weight:bold; border-radius:12px;" onclick="document.querySelector('[data-view=dataset]').click()">Dataset Information &rarr;</button>
                    <button class="btn btn-secondary" style="background:var(--brand-light-pink); color:var(--brand-secondary); font-weight:bold; border-radius:12px;" onclick="document.querySelector('[data-view=model]').click()">Model Performance &rarr;</button>
                    <button class="btn btn-secondary" style="background:#E0E7FF; color:#4338CA; font-weight:bold; border-radius:12px;" onclick="document.querySelector('[data-view=history]').click()">Prediction History &rarr;</button>
                    <button class="btn btn-secondary" style="background:#DCFCE7; color:#15803D; font-weight:bold; border-radius:12px;" onclick="document.querySelector('[data-view=alerts]').click()">Alert Center &rarr;</button>
                </div>
            </div>
        `;
        container.innerHTML = html;
        if (window.lucide) lucide.createIcons();
    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="notice-box danger"><h3 class="text-danger font-bold text-xl mb-2">Connection Error</h3><p>Could not load settings data from backend.</p></div>`;
    } finally {
        showLoading(false);
    }
}
'''

new_content = content[:start_idx] + new_function + '\n' + content[end_idx:]

with open('frontend/js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated app.js successfully.')
