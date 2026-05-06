/**
 * Gurukul AI — Centralized API Integration Layer
 * 
 * Provides gurukulFetch() wrapper with auto-auth and token refresh.
 * Include this script BEFORE page-specific scripts in all templates.
 */

const API_BASE = window.location.origin;

// --- Token Management ---
function getToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = '/gurukul_ashram.html';
        return false;
    }
    return true;
}

// --- Core Fetch Wrapper ---
async function gurukulFetch(endpoint, options = {}) {
    const token = getToken();
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
    
    console.log("API CALL:", url);

    // Merge headers with auth
    const headers = {
        ...(options.headers || {}),
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    if (options.body && !(options.body instanceof FormData)) {
        headers['Content-Type'] = headers['Content-Type'] || 'application/json';
    }

    let response = await fetch(url, { ...options, headers });

    // On 401 — attempt silent token refresh
    if (response.status === 401 && getRefreshToken()) {
        const refreshed = await _tryRefreshToken();
        if (refreshed) {
            // Retry original request with new token
            headers['Authorization'] = `Bearer ${getToken()}`;
            response = await fetch(url, { ...options, headers });
        } else {
            clearTokens();
            window.location.href = '/gurukul_ashram.html';
            throw new Error('Session expired. Redirecting to login.');
        }
    }

    return response;
}

async function _tryRefreshToken() {
    try {
        const res = await fetch(`${API_BASE}/api/auth/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: getRefreshToken() })
        });
        if (res.ok) {
            const data = await res.json();
            setTokens(data.access, data.refresh || getRefreshToken());
            return true;
        }
    } catch (e) {
        console.error('Token refresh failed:', e);
    }
    return false;
}
