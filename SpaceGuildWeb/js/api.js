// api.js
// API wrapper functions for Space Guild backend

// Auto-detect backend URL based on query parameter or use localhost default
const urlParams = new URLSearchParams(window.location.search);
const backendHost = urlParams.get('backend') || window.location.hostname || 'localhost';
const backendPort = urlParams.get('port') || '8000';

const API_BASE = `http://${backendHost}:${backendPort}`;
const WS_BASE = `ws://${backendHost}:${backendPort}`;
const PLAYER_ID_KEY = 'spaceguild_player_id';

console.log('Backend API configured:', API_BASE);
console.log('Backend WebSocket configured:', WS_BASE);

/**
 * Get the current player ID from localStorage
 * @returns {string|null} Player ID as string or null if not set
 */
function getPlayerId() {
    return localStorage.getItem(PLAYER_ID_KEY);
}

/**
 * Set the player ID in localStorage
 * @param {number|string} playerId - Player ID to store
 */
function setPlayerId(playerId) {
    console.log('setPlayerId called with:', playerId, 'type:', typeof playerId);
    // Store as string to preserve precision of large integers
    localStorage.setItem(PLAYER_ID_KEY, playerId.toString());
    console.log('Stored in localStorage, retrieving to verify:', getPlayerId());
}

/**
 * Clear the player ID from localStorage
 */
function clearPlayerId() {
    localStorage.removeItem(PLAYER_ID_KEY);
}

/**
 * Check if player is connected (has player_id)
 * @returns {boolean} True if player ID exists
 */
function isPlayerConnected() {
    return getPlayerId() !== null;
}

/**
 * Wrapper for fetch with error handling
 */
async function apiFetch(url, options = {}) {
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.error || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * GET /health - Health check
 */
async function healthCheck() {
    return apiFetch(`${API_BASE}/health`);
}

/**
 * POST /spawn_player - Create a new player with a ship
 * @param {string} name - Player name (optional, defaults to "Pilot")
 * @returns {Promise<{player_id: number, ship_id: number, name: string, location: string}>}
 */
async function spawnPlayer(name = 'Pilot') {
    return apiFetch(`${API_BASE}/spawn_player`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    });
}

/**
 * GET /ship?player_id=X - Get player's ship information
 */
async function getShip() {
    const playerId = getPlayerId();
    console.log('getShip: Retrieved player_id from localStorage:', playerId, 'type:', typeof playerId);
    if (!playerId) throw new Error('No player ID');
    const url = `${API_BASE}/ship?player_id=${playerId}`;
    console.log('getShip: Calling API with URL:', url);
    return apiFetch(url);
}

/**
 * GET /location?player_id=X - Get current location information
 */
async function getLocation() {
    const playerId = getPlayerId();
    if (!playerId) throw new Error('No player ID');
    return apiFetch(`${API_BASE}/location?player_id=${playerId}`);
}

/**
 * GET /vendors?player_id=X - Get vendors at current location
 */
async function getVendors() {
    const playerId = getPlayerId();
    if (!playerId) throw new Error('No player ID');
    return apiFetch(`${API_BASE}/vendors?player_id=${playerId}`);
}

/**
 * Connect to the WebSocket for real-time tick updates.
 * @param {number|string} shipId - The ship ID to subscribe to
 * @param {object} handlers - Event handlers: { onMessage, onClose, onError }
 * @returns {WebSocket} The WebSocket instance
 */
function connectShipWebSocket(shipId, { onMessage, onClose, onError } = {}) {
    const ws = new WebSocket(`${WS_BASE}/ws/${shipId}`);

    ws.addEventListener('message', (event) => {
        try {
            const msg = JSON.parse(event.data);
            if (onMessage) onMessage(msg);
        } catch (err) {
            console.error('WS parse error:', err);
        }
    });

    ws.addEventListener('close', (event) => {
        console.log('WS closed:', event.code, event.reason);
        if (onClose) onClose(event);
    });

    ws.addEventListener('error', (event) => {
        console.error('WS error:', event);
        if (onError) onError(event);
    });

    return ws;
}

/**
 * POST /action - Queue an action for the next tick
 * @param {string} actionType - Type of action (scan, attack_ship, move, collect, etc.)
 * @param {number|string} target - Target ID (ship_id, item_id) or location name
 * @param {string} targetData - Optional additional data (component slot, scan type, etc.)
 */
async function queueAction(actionType, target, targetData = null) {
    const playerId = getPlayerId();
    if (!playerId) throw new Error('No player ID');
    
    const body = {
        player_id: playerId,
        action_type: actionType,
        target: target
    };
    
    if (targetData !== null) {
        body.target_data = targetData;
    }
    
    return apiFetch(`${API_BASE}/action`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
}

/**
 * POST /repair/component - Repair a component
 * @param {number} itemId - Component item ID to repair
 */
async function repairComponent(itemId) {
    const playerId = getPlayerId();
    if (!playerId) throw new Error('No player ID');
    
    return apiFetch(`${API_BASE}/repair/component`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            player_id: playerId,
            item_id: itemId
        })
    });
}
