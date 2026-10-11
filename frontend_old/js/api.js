const API_BASE_URL = "http://localhost:8000";

const api = {
    async getDashboardStatistics() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/dashboard/statistics`);
            if (!response.ok) throw new Error('Failed to fetch statistics');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getRecentPredictions() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/dashboard/recent-predictions`);
            if (!response.ok) throw new Error('Failed to fetch recent predictions');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async uploadImage(file, isSimulation = false) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('simulationMode', isSimulation);

            const response = await fetch(`${API_BASE_URL}/api/predict`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) throw new Error('Failed to upload image');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getLatestPrediction() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/predict/latest`);
            if (!response.ok) throw new Error('Failed to fetch latest prediction');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getPredictionHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/predict/history`);
            if (!response.ok) throw new Error('Failed to fetch prediction history');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getAlerts() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/alerts`);
            if (!response.ok) throw new Error('Failed to fetch alerts');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getRiskZones() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/map/zones`);
            if (!response.ok) throw new Error('Failed to fetch risk zones');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async sendWorkerLocation(locationData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/map/worker-location`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(locationData)
            });
            if (!response.ok) throw new Error('Failed to send worker location');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getCurrentWeather() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/weather/current`);
            if (!response.ok) throw new Error('Failed to fetch weather');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getAnalyticsData() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/analytics`);
            if (!response.ok) throw new Error('Failed to fetch analytics');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getReportSummary() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/reports/summary`);
            if (!response.ok) throw new Error('Failed to fetch report summary');
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    }
};

window.api = api; // Make it available globally for the HTML pages
