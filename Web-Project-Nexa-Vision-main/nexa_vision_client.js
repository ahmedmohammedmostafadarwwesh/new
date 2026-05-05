"""
JavaScript API Client for Nexa Vision Frontend
Use this to call the dashboard API from your HTML/JS frontend
"""

class NexaVisionClient {
    constructor(apiUrl = 'http://localhost:8001') {
        this.apiUrl = apiUrl.replace(/\/$/, '');
        this.token = localStorage.getItem('nexavision_token');
        this.user = JSON.parse(localStorage.getItem('nexavision_user') || 'null');
    }

    // ==================== Authentication ====================
    
    async register(username, email, password) {
        const response = await fetch(`${this.apiUrl}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password, role: 'user' })
        });
        const data = await response.json();
        
        if (response.ok) {
            this.token = data.access_token;
            this.user = data.user;
            localStorage.setItem('nexavision_token', this.token);
            localStorage.setItem('nexavision_user', JSON.stringify(this.user));
            console.log('✅ Registered:', username);
        }
        return data;
    }

    async login(username, password) {
        const response = await fetch(`${this.apiUrl}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        
        if (response.ok) {
            this.token = data.access_token;
            this.user = data.user;
            localStorage.setItem('nexavision_token', this.token);
            localStorage.setItem('nexavision_user', JSON.stringify(this.user));
            console.log('✅ Logged in:', username);
        }
        return data;
    }

    async logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('nexavision_token');
        localStorage.removeItem('nexavision_user');
        console.log('✅ Logged out');
    }

    async getCurrentUser() {
        const response = await fetch(`${this.apiUrl}/api/auth/me`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    // ==================== Robot Control ====================
    
    async moveRobot(direction) {
        const response = await fetch(`${this.apiUrl}/api/robot/move`, {
            method: 'POST',
            headers: this._getHeaders(),
            body: JSON.stringify({ direction })
        });
        return await response.json();
    }

    async getRobotStatus() {
        const response = await fetch(`${this.apiUrl}/api/robot/status`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async getDistance() {
        const response = await fetch(`${this.apiUrl}/api/robot/distance`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async getEncoder() {
        const response = await fetch(`${this.apiUrl}/api/robot/encoder`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async runAI() {
        const response = await fetch(`${this.apiUrl}/api/robot/ai`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async getVideoStreamUrl() {
        const response = await fetch(`${this.apiUrl}/api/robot/video`, {
            headers: this._getHeaders()
        });
        const data = await response.json();
        return data.url;
    }

    // ==================== Dashboard Management ====================
    
    async getDashboard() {
        const response = await fetch(`${this.apiUrl}/api/dashboard`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async createDashboardRow(row) {
        const response = await fetch(`${this.apiUrl}/api/dashboard`, {
            method: 'POST',
            headers: this._getHeaders(),
            body: JSON.stringify(row)
        });
        return await response.json();
    }

    async updateDashboardRow(rowId, row) {
        const response = await fetch(`${this.apiUrl}/api/dashboard/${rowId}`, {
            method: 'PUT',
            headers: this._getHeaders(),
            body: JSON.stringify(row)
        });
        return await response.json();
    }

    async deleteDashboardRow(rowId) {
        const response = await fetch(`${this.apiUrl}/api/dashboard/${rowId}`, {
            method: 'DELETE',
            headers: this._getHeaders()
        });
        return await response.json();
    }

    // ==================== User Management (Admin) ====================
    
    async getAllUsers() {
        const response = await fetch(`${this.apiUrl}/api/users`, {
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async updateUserRole(username, newRole) {
        const response = await fetch(`${this.apiUrl}/api/users/${username}/role`, {
            method: 'PUT',
            headers: this._getHeaders(),
            body: JSON.stringify({ new_role: newRole })
        });
        return await response.json();
    }

    async activateUser(username) {
        const response = await fetch(`${this.apiUrl}/api/users/${username}/activate`, {
            method: 'PUT',
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async deactivateUser(username) {
        const response = await fetch(`${this.apiUrl}/api/users/${username}/deactivate`, {
            method: 'PUT',
            headers: this._getHeaders()
        });
        return await response.json();
    }

    async deleteUser(username) {
        const response = await fetch(`${this.apiUrl}/api/users/${username}`, {
            method: 'DELETE',
            headers: this._getHeaders()
        });
        return await response.json();
    }

    // ==================== Utilities ====================
    
    _getHeaders() {
        const headers = { 'Content-Type': 'application/json' };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    isAuthenticated() {
        return !!this.token;
    }

    isAdmin() {
        return this.user && this.user.role === 'admin';
    }
}

// Export for use in node environments
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = NexaVisionClient;
}
