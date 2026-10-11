document.addEventListener('DOMContentLoaded', async () => {
    const mapElement = document.getElementById('mine-map');
    const loadingElement = document.getElementById('map-loading');
    const gpsStatus = document.getElementById('gps-status');

    let map;

    // Default center if GPS fails or before locating
    const defaultCenter = [0, 0];

    // Helper: Risk color
    const getRiskColor = (risk) => {
        switch(risk?.toLowerCase()) {
            case 'safe': return '#22c55e';
            case 'moderate': return '#eab308';
            case 'early warning': return '#f97316';
            case 'high risk': return '#ef4444';
            default: return '#3b82f6';
        }
    };

    // Load Zones
    const zonesData = await window.api.getRiskZones();
    
    loadingElement.style.display = 'none';
    mapElement.style.display = 'block';

    if (!zonesData || !zonesData.center) {
        // Fallback initialization if backend fails
        map = L.map('mine-map').setView(defaultCenter, 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        console.warn('Backend data unavailable for zones. Map loaded with defaults.');
    } else {
        map = L.map('mine-map').setView(zonesData.center, 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Draw Zones
        if (zonesData.zones) {
            zonesData.zones.forEach(zone => {
                L.polygon(zone.coordinates, {
                    color: getRiskColor(zone.riskLevel),
                    fillColor: getRiskColor(zone.riskLevel),
                    fillOpacity: 0.3,
                    weight: 2
                }).addTo(map).bindPopup(`<b>${zone.name}</b><br>Risk: ${zone.riskLevel}`);
            });
        }
    }

    // Geolocation for Worker GPS
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;
                gpsStatus.textContent = 'Worker tracked (GPS Active)';
                gpsStatus.style.color = 'var(--safe)';
                
                // Add marker
                const workerIcon = L.divIcon({
                    className: 'custom-div-icon',
                    html: `<div style="background-color: var(--primary); width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>`,
                    iconSize: [14, 14],
                    iconAnchor: [7, 7]
                });
                
                L.marker([latitude, longitude], {icon: workerIcon}).addTo(map)
                    .bindPopup('<b>Worker Location</b><br>GPS Active').openPopup();
                
                map.setView([latitude, longitude], 16);

                // Send to backend
                await window.api.sendWorkerLocation({ lat: latitude, lng: longitude });
            },
            (error) => {
                console.error('GPS Error:', error);
                gpsStatus.textContent = 'Worker location unavailable';
                gpsStatus.style.color = 'var(--high-risk)';
            },
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    } else {
        gpsStatus.textContent = 'Worker location unavailable';
        gpsStatus.style.color = 'var(--high-risk)';
    }
});
