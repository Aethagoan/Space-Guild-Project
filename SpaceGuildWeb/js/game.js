// game.js
// Main game state management and update loop

// Global game state
const gameState = {
    ship: null,              // Ship data from /ship endpoint
    location: null,          // Location data from /location endpoint
    vendors: null,           // Vendors data from /vendors endpoint
    shipLog: [],             // Ship log messages
    scanData: null,          // Last scan result (cached)
    
    // UI state
    selectedView: 'location', // Current left panel selection: 'location', 'ship', 'vendors', 'navigation'
    selectedItem: null,       // Currently selected item from middle panel
    selectedItemType: null,   // Type of selected item: 'ship', 'item', 'component', 'vendor', 'destination'
    
    // Action state
    queuedAction: null,       // Currently queued action (shown in UI as "Action Queued")
    
    // Connection state
    isPlayerConnected: false, // Has player_id in localStorage
    isConnected: false,       // Connected to backend and game data loaded
    isLoading: true,
    errorMessage: null
};

// Update loop state
let updateLoopRunning = false;
let shipWebSocket = null;

/**
 * Initialize the game - check for player, show connection screen or load game
 */
async function initGame() {
    console.log('Initializing Space Guild...');
    gameState.isLoading = true;
    renderUI();
    
    try {
        // Check backend health first
        await healthCheck();
        console.log('Backend connected');
        
        // Check if player is already connected (has player_id)
        gameState.isPlayerConnected = isPlayerConnected();
        
        if (!gameState.isPlayerConnected) {
            // Show connection screen
            console.log('No player ID found, showing connection screen');
            gameState.isLoading = false;
            renderUI();
            return;
        }
        
        // Player exists, load game data
        console.log('Player ID found:', getPlayerId());
        await loadInitialData();
        
        // Start WebSocket update connection
        startUpdateLoop();
        
        gameState.isConnected = true;
        gameState.isLoading = false;
        gameState.errorMessage = null;
        
        console.log('Game initialized successfully');
        renderUI();
        
    } catch (error) {
        console.error('Failed to initialize game:', error);
        gameState.isLoading = false;
        gameState.errorMessage = `Failed to connect to server: ${error.message}`;
        renderUI();
    }
}

/**
 * Handle connecting to a spaceship (creating a new player)
 */
async function handleConnectToSpaceship() {
    try {
        console.log('Creating new player...');
        
        // Get player name from input FIRST, before re-rendering
        const nameInput = document.getElementById('player-name-input');
        const playerName = nameInput?.value.trim() || '';
        
        console.log('Player name from input:', playerName);
        
        // Validate name
        if (!playerName || playerName.length === 0) {
            gameState.errorMessage = 'Please enter a pilot name';
            renderUI();
            return;
        }
        
        // Now set loading state and re-render
        gameState.isLoading = true;
        renderUI();
        
        // Create new player
        console.log('Calling spawnPlayer with name:', playerName);
        const playerData = await spawnPlayer(playerName);
        console.log('Player created:', playerData);
        console.log('Player ID:', playerData.player_id);
        console.log('Ship ID:', playerData.ship_id);
        
        // Store player ID
        setPlayerId(playerData.player_id);
        console.log('Stored player_id in localStorage:', getPlayerId());
        gameState.isPlayerConnected = true;
        
        // Load game data
        await loadInitialData();
        
        // Start WebSocket update connection
        startUpdateLoop();
        
        gameState.isConnected = true;
        gameState.isLoading = false;
        gameState.errorMessage = null;
        
        console.log('Connected to spaceship successfully!');
        renderUI();
        
    } catch (error) {
        console.error('Failed to connect to spaceship:', error);
        gameState.isLoading = false;
        gameState.errorMessage = `Failed to create player: ${error.message}`;
        renderUI();
    }
}

/**
 * Disconnect from current player (for testing - clears localStorage)
 */
function handleDisconnect() {
    if (confirm('Disconnect from current spaceship? This will clear your connection.')) {
        stopUpdateLoop();
        clearPlayerId();
        gameState.isPlayerConnected = false;
        gameState.isConnected = false;
        gameState.ship = null;
        gameState.location = null;
        gameState.vendors = null;
        gameState.shipLog = [];
        gameState.scanData = null;
        gameState.selectedView = 'location';
        gameState.selectedItem = null;
        gameState.selectedItemType = null;
        gameState.queuedAction = null;
        console.log('Disconnected from spaceship');
        renderUI();
    }
}

/**
 * Load initial game data (ship, location, vendors)
 */
async function loadInitialData() {
    try {
        // Load ship data
        gameState.ship = await getShip();
        console.log('Ship loaded:', gameState.ship);
        
        // Load location data
        gameState.location = await getLocation();
        console.log('Location loaded:', gameState.location);
        
        // Try to load vendors (may not exist at current location)
        try {
            const vendorData = await getVendors();
            gameState.vendors = vendorData.vendors;
            console.log('Vendors loaded:', gameState.vendors);
        } catch (error) {
            console.log('No vendors at current location');
            gameState.vendors = {};
        }
        
    } catch (error) {
        console.error('Error loading initial data:', error);
        throw error;
    }
}


/**
 * Stop the update loop
 */
function stopUpdateLoop() {
    updateLoopRunning = false;
    if (shipWebSocket) {
        shipWebSocket.close(1000, 'User disconnected');
        shipWebSocket = null;
    }
    console.log('WebSocket update connection stopped');
}

/**
 * Start the WebSocket update connection.
 * Connects to ws/ship using the ship_id from gameState.ship.
 */
function startUpdateLoop() {
    if (updateLoopRunning) {
        console.log('Update connection already running');
        return;
    }

    const shipId = gameState.ship && gameState.ship.ship_id;
    if (!shipId) {
        console.error('startUpdateLoop: no ship_id available');
        return;
    }

    updateLoopRunning = true;
    console.log('Connecting WebSocket for ship', shipId, '...');

    shipWebSocket = connectShipWebSocket(shipId, {
        onMessage(msg) {
            if (msg.type === 'tick_complete' && msg.data) {
                processUpdates(msg.data);
                renderUI();
            }
        },
        onClose(event) {
            updateLoopRunning = false;
            shipWebSocket = null;

            if (event.code === 1000) {
                // Clean intentional close — no reconnect
                return;
            }

            console.warn('WS closed unexpectedly, reconnecting in 2s...');
            gameState.errorMessage = 'Connection lost — reconnecting...';
            renderUI();

            setTimeout(() => {
                if (!updateLoopRunning && gameState.isConnected) {
                    gameState.errorMessage = null;
                    startUpdateLoop();
                }
            }, 2000);
        },
        onError() {
            gameState.errorMessage = 'WebSocket error — check server connection';
            renderUI();
        }
    });
}

/**
 * Process updates from a WebSocket tick_complete message
 */
function processUpdates(updates) {
    console.log('Processing updates:', updates);
    
    // Update ship state
    if (updates.ship_state) {
        gameState.ship = updates.ship_state;
    }
    
    // Update location state
    if (updates.location_state) {
        gameState.location = updates.location_state;
    }
    
    // Update ship log
    if (updates.ship_log && Array.isArray(updates.ship_log)) {
        gameState.shipLog = updates.ship_log;
    }
    
    // Process action results
    if (updates.scan_data) {
        gameState.scanData = updates.scan_data;
        console.log('Scan data received:', updates.scan_data);
    }
    
    if (updates.attack_result) {
        console.log('Attack result:', updates.attack_result);
    }
    
    if (updates.collect_result) {
        console.log('Collect result:', updates.collect_result);
    }
    
    if (updates.move_result) {
        console.log('Move result:', updates.move_result);
        // Reload vendors after moving
        reloadVendors();
    }
    
    // Clear queued action since tick completed
    if (gameState.queuedAction) {
        console.log('Action processed:', gameState.queuedAction);
        gameState.queuedAction = null;
    }
}

/**
 * Reload vendors at current location
 */
async function reloadVendors() {
    try {
        const vendorData = await getVendors();
        gameState.vendors = vendorData.vendors;
    } catch (error) {
        console.log('No vendors at new location');
        gameState.vendors = {};
    }
}

/**
 * Queue an action
 */
async function handleAction(actionType, target, targetData = null) {
    try {
        console.log('Queueing action:', actionType, target, targetData);
        
        const result = await queueAction(actionType, target, targetData);
        
        // Store queued action for UI feedback
        gameState.queuedAction = {
            type: actionType,
            target: target,
            targetData: targetData
        };
        
        console.log('Action queued successfully:', result);
        renderUI();
        
    } catch (error) {
        console.error('Failed to queue action:', error);
        addLogMessage(`Error: ${error.message}`, 'error');
        renderUI();
    }
}

/**
 * Handle navigation (left panel button clicks)
 */
function handleNavigation(view) {
    console.log('Navigating to view:', view);
    gameState.selectedView = view;
    gameState.selectedItem = null;
    gameState.selectedItemType = null;
    renderUI();
}

/**
 * Handle item selection from middle panel
 */
function handleItemSelection(item, itemType) {
    console.log('Selected item:', item, 'Type:', itemType);
    gameState.selectedItem = item;
    gameState.selectedItemType = itemType;
    renderUI();
}

/**
 * Add a message to ship log (for local errors/info)
 */
function addLogMessage(message, type = 'info') {
    gameState.shipLog.push({
        message: message,
        type: type,
        timestamp: Date.now()
    });
}

/**
 * Utility: Sleep function
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM ready, initializing game...');
    initGame();
});
