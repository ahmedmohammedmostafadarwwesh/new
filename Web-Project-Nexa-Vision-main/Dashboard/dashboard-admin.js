// Admin Dashboard User Management System
const API_BASE = 'http://localhost:8001';
let currentUser = null;
let currentToken = null;
let currentAction = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    // Skip authentication check and directly show dashboard
    showDashboard();
    loadUsers();
});

async function checkAuth() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        showAuthForm();
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const userData = await response.json();
            
            if (userData.role !== 'admin') {
                showError('Access denied. Only admins can access this page.');
                localStorage.removeItem('token');
                showAuthForm();
                return;
            }
            
            currentUser = userData;
            currentToken = token;
            showDashboard();
            loadUsers();
        } else {
            localStorage.removeItem('token');
            showAuthForm();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        showAuthForm();
    }
}

function showAuthForm() {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('auth-form-container').classList.remove('hidden');
}

function showDashboard() {
    document.getElementById('auth-form-container').classList.add('hidden');
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('current-user').textContent = 'Administrator';
}

function showLoginForm() {
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
    clearMessages();
}

function showRegisterForm() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
    clearMessages();
}

function clearMessages() {
    document.getElementById('error-message').classList.add('hidden');
    document.getElementById('success-message').classList.add('hidden');
}

function showError(msg) {
    const errorEl = document.getElementById('error-message');
    errorEl.textContent = msg;
    errorEl.classList.remove('hidden');
    setTimeout(() => errorEl.classList.add('hidden'), 5000);
}

function showSuccess(msg) {
    const successEl = document.getElementById('success-message');
    successEl.textContent = msg;
    successEl.classList.remove('hidden');
    setTimeout(() => successEl.classList.add('hidden'), 5000);
}

async function handleLogin() {
    clearMessages();
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    
    if (!username || !password) {
        showError('Please fill in all fields');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.user.role !== 'admin') {
                showError('Admin access required');
                return;
            }
            
            localStorage.setItem('token', data.access_token);
            currentUser = data.user;
            currentToken = data.access_token;
            
            showSuccess('Login successful!');
            setTimeout(() => {
                showDashboard();
                loadUsers();
            }, 1000);
        } else {
            const error = await response.json();
            showError(error.detail || 'Login failed');
        }
    } catch (error) {
        showError('Login failed: ' + error.message);
    }
}

async function handleRegister() {
    clearMessages();
    const username = document.getElementById('reg-username').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value;
    
    if (!username || !email || !password) {
        showError('Please fill in all fields');
        return;
    }
    
    if (password.length < 6) {
        showError('Password must be at least 6 characters');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            currentUser = data.user;
            currentToken = data.access_token;
            
            showSuccess('Account created successfully!');
            setTimeout(() => {
                showDashboard();
                loadUsers();
            }, 1000);
        } else {
            const error = await response.json();
            showError(error.detail || 'Registration failed');
        }
    } catch (error) {
        showError('Registration failed: ' + error.message);
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/api/users`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }
        
        const users = await response.json();
        displayUsers(users);
        updateStats(users);
    } catch (error) {
        console.error('Error loading users:', error);
        showError('Failed to load users: ' + error.message);
    }
}

function displayUsers(users) {
    const tbody = document.getElementById('users-body');
    tbody.innerHTML = '';
    
    users.forEach((user, index) => {
        const joinedDate = new Date(user.created_at).toLocaleDateString();
        const row = document.createElement('tr');
        row.className = 'border-b border-slate-200 hover:bg-slate-50';
        row.innerHTML = `
            <td class="px-6 py-4 text-slate-500">${index + 1}</td>
            <td class="px-6 py-4 font-medium text-slate-900">${user.username}</td>
            <td class="px-6 py-4 text-slate-600">${user.email}</td>
            <td class="px-6 py-4">
                <span class="${user.role === 'admin' ? 'admin-badge' : 'user-badge'}">
                    ${user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                </span>
            </td>
            <td class="px-6 py-4">
                <span class="${user.is_active ? 'active-badge' : 'inactive-badge'}">
                    ${user.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td class="px-6 py-4 text-slate-600 text-sm">${joinedDate}</td>
            <td class="px-6 py-4">
                <div class="flex gap-2 justify-center">
                    <button onclick="changeRole('${user.username}', '${user.role === 'admin' ? 'user' : 'admin'}')" 
                        class="btn-sm bg-blue-600 text-white hover:bg-blue-700 rounded" 
                        title="Make ${user.role === 'admin' ? 'User' : 'Admin'}">
                        <i class="fas fa-${user.role === 'admin' ? 'user' : 'shield-alt'}"></i>
                    </button>
                    <button onclick="toggleUserStatus('${user.username}', ${user.is_active})" 
                        class="btn-sm bg-${user.is_active ? 'yellow' : 'green'}-600 text-white hover:bg-${user.is_active ? 'yellow' : 'green'}-700 rounded"
                        title="${user.is_active ? 'Deactivate' : 'Activate'}">
                        <i class="fas fa-${user.is_active ? 'ban' : 'check'}"></i>
                    </button>
                    <button onclick="deleteUserConfirm('${user.username}')" 
                        class="btn-sm bg-red-600 text-white hover:bg-red-700 rounded" 
                        title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateStats(users) {
    document.getElementById('total-users').textContent = users.length;
    document.getElementById('total-admins').textContent = users.filter(u => u.role === 'admin').length;
    document.getElementById('total-active').textContent = users.filter(u => u.is_active).length;
}

function openModal(title, message, action) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-message').textContent = message;
    currentAction = action;
    document.getElementById('action-modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('action-modal').classList.add('hidden');
    currentAction = null;
}

async function confirmAction() {
    if (!currentAction) return;
    
    try {
        closeModal();
        
        if (currentAction.type === 'role') {
            await updateUserRole(currentAction.username, currentAction.role);
        } else if (currentAction.type === 'deactivate') {
            await deactivateUser(currentAction.username);
        } else if (currentAction.type === 'activate') {
            await activateUser(currentAction.username);
        } else if (currentAction.type === 'delete') {
            await deleteUser(currentAction.username);
        }
        
        loadUsers();
    } catch (error) {
        showError('Action failed: ' + error.message);
    }
}

function changeRole(username, newRole) {
    openModal(
        'Change User Role',
        `Make ${username} a ${newRole}?`,
        { type: 'role', username, role: newRole }
    );
}

function toggleUserStatus(username, isActive) {
    if (isActive) {
        deactivateUserConfirm(username);
    } else {
        activateUserConfirm(username);
    }
}

function deactivateUserConfirm(username) {
    openModal(
        'Deactivate User',
        `Deactivate ${username}? They will not be able to login.`,
        { type: 'deactivate', username }
    );
}

function activateUserConfirm(username) {
    openModal(
        'Activate User',
        `Activate ${username}? They will be able to login again.`,
        { type: 'activate', username }
    );
}

function deleteUserConfirm(username) {
    openModal(
        'Delete User',
        `Permanently delete ${username}? This cannot be undone.`,
        { type: 'delete', username }
    );
}

async function updateUserRole(username, newRole) {
    const response = await fetch(`${API_BASE}/api/users/${username}/role`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ new_role: newRole })
    });
    
    if (!response.ok) {
        throw new Error('Failed to update role');
    }
    
    showSuccess(`${username} is now a ${newRole}`);
}

async function deactivateUser(username) {
    const response = await fetch(`${API_BASE}/api/users/${username}/deactivate`, {
        method: 'PUT'
    });
    
    if (!response.ok) {
        throw new Error('Failed to deactivate user');
    }
    
    showSuccess(`${username} has been deactivated`);
}

async function activateUser(username) {
    const response = await fetch(`${API_BASE}/api/users/${username}/activate`, {
        method: 'PUT'
    });
    
    if (!response.ok) {
        throw new Error('Failed to activate user');
    }
    
    showSuccess(`${username} has been activated`);
}

async function deleteUser(username) {
    const response = await fetch(`${API_BASE}/api/users/${username}`, {
        method: 'DELETE'
    });
    
    if (!response.ok) {
        throw new Error('Failed to delete user');
    }
    
    showSuccess(`${username} has been deleted`);
}

function logout() {
    if (confirm('Are you sure you want to refresh the dashboard?')) {
        // Clear any cached data and reload
        localStorage.removeItem('token');
        currentUser = null;
        currentToken = null;
        location.reload();
    }
}
}
