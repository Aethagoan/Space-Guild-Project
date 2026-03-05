// ui.js
// UI rendering functions for all panels
console.log('ui.js loaded');

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return '';
    return String(unsafe)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/*
symbols conviniently at the top
*/
const location_icons = {
    'station': '⊕',
    'ground_station': '⊗',
    'space': '>',
    'resource_node': '◆',
    'unknown': '?'
}


/**
 * Main UI render function - re-renders all panels
 */
function renderUI() {
    console.log('renderUI called, isPlayerConnected:', gameState.isPlayerConnected);
    const gameContainer = document.querySelector('.game-container');
    
    // Handle OFF state (not connected to player)
    if (!gameState.isPlayerConnected) {
        gameContainer.classList.add('off');
        gameContainer.classList.remove('powering-up');
        renderConnectionScreen();
        return;
    }
    
    // Handle powering up animation
    if (gameState.isLoading) {
        gameContainer.classList.add('powering-up');
    } else {
        gameContainer.classList.remove('off');
        gameContainer.classList.remove('powering-up');
    }
    
    // Normal rendering
    renderLeftPanel();
    renderMiddlePanel();
    renderRightPanel();
    renderDisconnectButton();
}

/**
 * Render connection screen (when no player_id)
 */
function renderConnectionScreen() {
    console.log('renderConnectionScreen called');
    const leftPanel = document.getElementById('left-panel');
    const middlePanel = document.getElementById('middle-panel');
    const rightPanel = document.getElementById('right-panel');
    
    console.log('Panels found:', { leftPanel: !!leftPanel, middlePanel: !!middlePanel, rightPanel: !!rightPanel });
    
    if (!leftPanel || !middlePanel || !rightPanel) {
        console.error('One or more panels not found!');
        return;
    }
    
    // Clear all panels first
    leftPanel.innerHTML = '';
    middlePanel.innerHTML = '';
    rightPanel.innerHTML = '';
    
    console.log('gameState.isLoading:', gameState.isLoading);
    console.log('gameState.errorMessage:', gameState.errorMessage);
    
    // Show connection screen in middle panel
    if (gameState.isLoading) {
        console.log('Showing loading screen');
        middlePanel.innerHTML = `
            <div class="connection-screen">
                <div class="connection-screen-title">INITIALIZING...</div>
            </div>
        `;
    } else if (gameState.errorMessage) {
        console.log('Showing error screen');
        middlePanel.innerHTML = `
            <div class="connection-screen">
                <div class="connection-screen-title">CONNECTION ERROR</div>
                <div class="connection-screen-subtitle">${gameState.errorMessage}</div>
                <div class="connection-form">
                    <input type="text" 
                           id="player-name-input" 
                           class="player-name-input" 
                           placeholder="Enter pilot name"
                           maxlength="20">
                    <button class="connect-button" onclick="handleConnectToSpaceship()">
                        [Retry Connection]
                    </button>
                </div>
            </div>
        `;
    } else {
        console.log('Showing connection form');
        middlePanel.innerHTML = `
            <div class="connection-screen">
                <div class="connection-screen-title">SPACE GUILD</div>
                <div class="connection-screen-subtitle">TERMINAL OFFLINE</div>
                <div class="connection-form">
                    <input type="text" 
                           id="player-name-input" 
                           class="player-name-input" 
                           placeholder="Enter pilot name"
                           maxlength="20">
                    <button class="connect-button" onclick="handleConnectToSpaceship()">
                        [Connect to Spaceship]
                    </button>
                </div>
            </div>
        `;
    }
    console.log('Middle panel HTML set, length:', middlePanel.innerHTML.length);
}

/**
 * Render disconnect button (for testing)
 */
function renderDisconnectButton() {
    // Check if button already exists
    let disconnectBtn = document.querySelector('.disconnect-button');
    
    if (!disconnectBtn && gameState.isPlayerConnected) {
        disconnectBtn = document.createElement('button');
        disconnectBtn.className = 'disconnect-button';
        disconnectBtn.textContent = 'Disconnect';
        disconnectBtn.onclick = handleDisconnect;
        document.body.appendChild(disconnectBtn);
    } else if (disconnectBtn && !gameState.isPlayerConnected) {
        disconnectBtn.remove();
    }
}

/**
 * Render left navigation panel
 */
function renderLeftPanel() {
    const leftPanel = document.getElementById('left-panel');
    if (!leftPanel) return;
    
    const views = [
        { id: 'location', label: 'Location'},
        { id: 'ship', label: 'Ship Status'},
        { id: 'navigation', label: 'Navigation'},
        { id: 'vendors', label: 'Vendors'}
    ];
    
    leftPanel.innerHTML = views.map(view => {
        const isActive = gameState.selectedView === view.id;
        const activeClass = isActive ? 'active' : '';
        
        return `
            <button class="nav-button ${activeClass}" 
                    onclick="handleNavigation('${view.id}')">
                <span class="nav-label">${view.label}</span>
            </button>
        `;
    }).join('');
}

/**
 * Render middle contextual panel
 */
function renderMiddlePanel() {
    const middlePanel = document.getElementById('middle-panel');
    if (!middlePanel) return;
    
    if (gameState.isLoading) {
        middlePanel.innerHTML = '<div class="loading">Loading...</div>';
        return;
    }
    
    if (gameState.errorMessage) {
        middlePanel.innerHTML = `<div class="error">${gameState.errorMessage}</div>`;
        return;
    }
    
    switch (gameState.selectedView) {
        case 'location':
            renderLocationView(middlePanel);
            break;
        case 'ship':
            renderShipView(middlePanel);
            break;
        case 'navigation':
            renderNavigationView(middlePanel);
            break;
        case 'vendors':
            renderVendorsView(middlePanel);
            break;
        default:
            middlePanel.innerHTML = '<div class="info">Select a view</div>';
    }
}

/**
 * Render location view (ships and items at current location)
 */
function renderLocationView(panel) {
    if (!gameState.location) {
        panel.innerHTML = '<div class="info">No location data</div>';
        return;
    }
    
    const ships = gameState.location.ships || [];
    const items = gameState.location.items || [];
    const shipCount = gameState.location.ship_count;
    const locationType = gameState.location.type || 'space';
    const isStation = locationType === 'station' || locationType === 'ground_station';
    
    // Make location name clickable
    const currentLocation = {
        name: gameState.location.name,
        type: locationType,
        description: gameState.location.description || '',
        isCurrent: true
    };
    const locationRegId = registerItem(currentLocation, 'location');
    
    let html = `
        <div class="panel-header clickable-header" onclick="handleItemSelectionById('${locationRegId}')">
            Location: ${escapeHtml(gameState.location.name)}
        </div>
    `;
    
    // Ships section
    html += '<div class="section-header">Ships</div>';
    
    // At stations, only show ship count
    if (isStation) {
        const count = shipCount !== undefined ? shipCount : 0;
        if (count === 0) {
            html += '<div class="empty-message">No other ships docked</div>';
        } else {
            html += `<div class="info-message">${count} ship${count !== 1 ? 's' : ''} docked at this station</div>`;
        }
    } else {
        // In space, show individual ships
        if (ships.length === 0) {
            html += '<div class="empty-message">No other ships here</div>';
        } else {
            html += '<div class="item-list">';
            ships.forEach(ship => {
                const isSelected = gameState.selectedItemType === 'ship' && 
                                 gameState.selectedItem?.ship_id === ship.ship_id;
                const selectedClass = isSelected ? 'selected' : '';
                const shipRegId = registerItem(ship, 'ship');
                
                html += `
                    <div class="item-card ${selectedClass}" 
                         onclick="handleItemSelectionById('${shipRegId}')">
                        <span class="item-icon">${escapeHtml(ship.symbol || 'S')}</span>
                        <div class="item-info">
                            <div class="item-name">${escapeHtml(ship.name)}</div>
                            <div class="item-detail">Pilot: ${escapeHtml(ship.player_name)}</div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }
    }
    
    // Items section
    html += '<div class="section-header">Items</div>';
    if (items.length === 0) {
        html += '<div class="empty-message">No items here</div>';
    } else {
        html += '<div class="item-list">';
        items.forEach(item => {
            const isSelected = gameState.selectedItemType === 'item' && 
                             gameState.selectedItem?.item_id === item.item_id;
            const selectedClass = isSelected ? 'selected' : '';
            const itemRegId = registerItem(item, 'item');
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick="handleItemSelectionById('${itemRegId}')">
                    <span class="item-icon">I</span>
                    <div class="item-info">
                        <div class="item-name">${escapeHtml(item.name)}</div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    panel.innerHTML = html;
}

/**
 * Render ship view (components and cargo)
 */
function renderShipView(panel) {
    if (!gameState.ship) {
        panel.innerHTML = '<div class="info">No ship data</div>';
        return;
    }
    
    const ship = gameState.ship;
    
    let html = `<div class="panel-header">Ship Status</div>`;
    
    // Ship stats
    html += `
        <div class="ship-stats">
            <div class="stat">HP: ${ship.hp.toFixed(1)} / ${ship.tier * 100}</div>
            <div class="stat">Shield: ${ship.shield_pool.toFixed(1)}</div>
            <div class="stat">Tier: ${ship.tier}</div>
            ${ship.is_stealthed ? '<div class="stat stealth">[STEALTHED]</div>' : ''}
        </div>
    `;
    
    // Components section
    html += '<div class="section-header">Components</div>';
    html += '<div class="item-list">';
    
    const components = [
        { id: ship.engine_id, type: 'Engine', icon: 'ENG', slot: 'engine_id' },
        { id: ship.weapon_id, type: 'Weapon', icon: 'WPN', slot: 'weapon_id' },
        { id: ship.shield_id, type: 'Shield', icon: 'SHD', slot: 'shield_id' },
        { id: ship.cargo_id, type: 'Cargo', icon: 'CRG', slot: 'cargo_id' },
        { id: ship.sensor_id, type: 'Sensor', icon: 'SNR', slot: 'sensor_id' },
        { id: ship.stealth_cloak_id, type: 'Stealth Cloak', icon: 'STL', slot: 'stealth_cloak_id' }
    ];
    
    components.forEach(comp => {
        if (comp.id) {
            const isSelected = gameState.selectedItemType === 'component' && 
                             gameState.selectedItem?.item_id === comp.id;
            const selectedClass = isSelected ? 'selected' : '';
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick='handleItemSelection(${JSON.stringify({item_id: comp.id, type: comp.type, slot: comp.slot})}, "component")'>
                    <span class="item-icon">${comp.icon}</span>
                    <div class="item-info">
                        <div class="item-name">${comp.type}</div>
                    </div>
                </div>
            `;
        }
    });
    
    html += '</div>';
    
    // Cargo section - use enriched cargo data if available
    const cargoItems = ship.cargo_items_enriched || [];
    html += '<div class="section-header">Cargo</div>';
    if (cargoItems.length === 0) {
        html += '<div class="empty-message">Cargo is empty</div>';
    } else {
        html += '<div class="item-list">';
        cargoItems.forEach(item => {
            // Normalize id to item_id for consistency
            const itemData = { item_id: item.id, ...item };
            
            const isSelected = gameState.selectedItemType === 'cargo_item' && 
                             gameState.selectedItem?.item_id === item.id;
            const selectedClass = isSelected ? 'selected' : '';
            
            // Display item name and type
            const itemName = item.name || `Item #${item.id}`;
            const itemType = item.type || 'unknown';
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick='handleItemSelection(${JSON.stringify(itemData)}, "cargo_item")'>
                    <span class="item-icon">I</span>
                    <div class="item-info">
                        <div class="item-name">${escapeHtml(itemName)}</div>
                        <div class="item-type">${escapeHtml(itemType)}</div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    panel.innerHTML = html;
}

/**
 * Render navigation view (destinations)
 */
function renderNavigationView(panel) {
    if (!gameState.location) {
        panel.innerHTML = '<div class="info">No location data</div>';
        return;
    }
    
    const links = gameState.location.links || [];
    
    let html = `<div class="panel-header">Navigation</div>`;
    
    // Add current location as a selectable item
    const currentLocation = {
        name: gameState.location.name,
        type: gameState.location.type || 'space',
        description: gameState.location.description || '',
        isCurrent: true
    };
    
    const isCurrentSelected = gameState.selectedItemType === 'location' && 
                              gameState.selectedItem?.name === currentLocation.name;
    const currentSelectedClass = isCurrentSelected ? 'selected' : '';
    const currentRegId = registerItem(currentLocation, 'location');
    
    // Icon for current location based on type
    const currentIcon = {
        'station': '⊕',
        'ground_station': '⊗',
        'space': '●',
        'resource_node': '◆',
        'unknown': '?'
    }[currentLocation.type] || '●';
    
    html += '<div class="section-header">Current Location</div>';
    html += '<div class="item-list">';
    html += `
        <div class="item-card ${currentSelectedClass}" 
             onclick="handleItemSelectionById('${currentRegId}')">
            <span class="item-icon">${currentIcon}</span>
            <div class="item-info">
                <div class="item-name">${escapeHtml(currentLocation.name)}</div>
                <div class="item-detail">[Current]</div>
            </div>
        </div>
    `;
    html += '</div>';
    
    // Destinations section
    if (links.length === 0) {
        html += '<div class="section-header">Destinations</div>';
        html += '<div class="empty-message">No destinations available</div>';
    } else {
        // Normalize links to objects (handle both old string format and new object format)
        const normalizedLinks = links.map(link => {
            if (typeof link === 'string') {
                // Old format: just a string
                return { name: link, type: 'unknown', description: '' };
            } else {
                // New format: object with name, type, and description
                return {
                    name: link.name,
                    type: link.type || 'unknown',
                    description: link.description || ''
                };
            }
        });
        
        // Sort links by type: stations first, then ground stations, then space
        const typeOrder = { 'station': 0, 'ground_station': 1, 'space': 2, 'resource_node': 3, 'unknown': 4 };
        const sortedLinks = [...normalizedLinks].sort((a, b) => {
            const aType = a.type || 'unknown';
            const bType = b.type || 'unknown';
            const orderA = typeOrder[aType] !== undefined ? typeOrder[aType] : 999;
            const orderB = typeOrder[bType] !== undefined ? typeOrder[bType] : 999;
            
            if (orderA !== orderB) {
                return orderA - orderB;
            }
            // If same type, sort alphabetically by name
            return a.name.localeCompare(b.name);
        });
        
        // Group destinations by type
        let currentType = null;
        html += '<div class="item-list">';
        
        sortedLinks.forEach(destination => {
            // Add section header when type changes
            if (currentType !== destination.type) {
                currentType = destination.type;
                const typeLabel = {
                    'station': 'Stations',
                    'ground_station': 'Ground Stations',
                    'space': 'Space',
                    'resource_node': 'Resource Nodes',
                    'unknown': 'Other'
                }[currentType] || 'Other';
                
                html += `</div><div class="section-header">${typeLabel}</div><div class="item-list">`;
            }
            
            const isSelected = gameState.selectedItemType === 'location' && 
                             gameState.selectedItem?.name === destination.name;
            const selectedClass = isSelected ? 'selected' : '';
            const destRegId = registerItem(destination, 'location');
            
            // Choose icon based on type
            const icon = {
                'station': '⊕',
                'ground_station': '⊗',
                'space': '>',
                'resource_node': '◆',
                'unknown': '?'
            }[destination.type] || '>';
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick="handleItemSelectionById('${destRegId}')">
                    <span class="item-icon">${icon}</span>
                    <div class="item-info">
                        <div class="item-name">${escapeHtml(destination.name)}</div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    panel.innerHTML = html;
}

/**
 * Render vendors view
 */
function renderVendorsView(panel) {
    if (!gameState.vendors || Object.keys(gameState.vendors).length === 0) {
        panel.innerHTML = '<div class="info">No vendors at this location</div>';
        return;
    }
    
    let html = `<div class="panel-header">Vendors</div>`;
    html += '<div class="item-list">';
    
    Object.entries(gameState.vendors).forEach(([vendorId, vendor]) => {
        const isSelected = gameState.selectedItemType === 'vendor' && 
                         gameState.selectedItem?.vendor_id === vendorId;
        const selectedClass = isSelected ? 'selected' : '';
        
        html += `
            <div class="item-card ${selectedClass}" 
                 onclick='handleItemSelection(${JSON.stringify({vendor_id: vendorId, ...vendor})}, "vendor")'>
                <span class="item-icon">V</span>
                <div class="item-info">
                    <div class="item-name">${vendor.vendor_type}</div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    panel.innerHTML = html;
}

/**
 * Render right panel (log, details, actions)
 */
function renderRightPanel() {
    const rightPanel = document.querySelector('.right-panel');
    if (!rightPanel) return;
    
    // Create the full structure
    rightPanel.innerHTML = `
        <!-- Ship Log Section -->
        <div class="right-section ship-log-section">
            <div class="section-title">Ship Log</div>
            <div id="ship-log" class="ship-log">
                <!-- Log messages will be rendered here -->
            </div>
        </div>

        <!-- Details Section -->
        <div class="right-section details-container">
            <div id="details-section" class="details-section">
                <!-- Details will be rendered here -->
            </div>
        </div>

        <!-- Actions Section -->
        <div class="right-section actions-container">
            <div id="actions-section" class="actions-section">
                <!-- Action buttons will be rendered here -->
            </div>
        </div>
    `;
    
    // Now render the content into each section
    renderShipLog();
    renderDetails();
    renderActions();
}

/**
 * Render ship log section
 */
function renderShipLog() {
    const logContainer = document.getElementById('ship-log');
    if (!logContainer) return;
    
    if (gameState.shipLog.length === 0) {
        logContainer.innerHTML = '<div class="empty-message">No messages</div>';
        return;
    }
    
    const html = [...gameState.shipLog].map((entry, index) => {
        // Use backend format: {type, content, source}
        const content = escapeHtml(entry.content || entry.message || entry);
        const type = entry.type || 'computer';
        const source = entry.source || null;
        
        // Determine if this entry is clickable
        const isClickable = source !== null;
        const clickableClass = isClickable ? 'log-clickable' : '';
        // Pass both source and raw content (unescaped) to handler
        const clickHandler = isClickable ? `onclick="handleLogEntryClick('${source}', '${escapeHtml(entry.content || '')}')"` : '';
        
        return `<div class="log-entry log-${type} ${clickableClass}" ${clickHandler}>${content}</div>`;
    }).join('');
    
    logContainer.innerHTML = html;
}

/**
 * Render details section
 */
function renderDetails() {
    const detailsContainer = document.getElementById('details-section');
    if (!detailsContainer) return;
    
    if (!gameState.selectedItem) {
        detailsContainer.innerHTML = '<div class="empty-message">Select an item to view details</div>';
        return;
    }
    
    let html = '';
    
    // Check if we're showing scan data - render full scan details
    if (gameState.isShowingScanData) {
        switch (gameState.selectedItemType) {
            case 'ship':
                html = renderScannedShipDetails(gameState.selectedItem);
                break;
            case 'item':
                html = renderScannedItemDetails(gameState.selectedItem);
                break;
            case 'location':
                html = renderScannedLocationDetails(gameState.selectedItem);
                break;
            default:
                html = '<div class="empty-message">Unknown scan type</div>';
        }
    } else {
        // Normal entity rendering (from location/middle panel selection)
        switch (gameState.selectedItemType) {
            case 'ship':
                html = renderShipDetails(gameState.selectedItem);
                break;
            case 'item':
                html = renderItemDetails(gameState.selectedItem);
                break;
            case 'component':
                html = renderComponentDetails(gameState.selectedItem);
                break;
            case 'cargo_item':
                html = renderCargoItemDetails(gameState.selectedItem);
                break;
            case 'destination':
                html = renderDestinationDetails(gameState.selectedItem);
                break;
            case 'location':
                html = renderLocationDetails(gameState.selectedItem);
                break;
            case 'vendor':
                html = renderVendorDetails(gameState.selectedItem);
                break;
            case 'unknown':
                html = '<div class="info-message">No information available for this entity</div>';
                break;
            default:
                html = '<div class="empty-message">Unknown item type</div>';
        }
    }
    
    detailsContainer.innerHTML = html;
}

/**
 * Render scanned ship details (full scan data with components and cargo)
 */
function renderScannedShipDetails(ship) {
    let html = `
        <div class="detail-header">[SCAN DATA]</div>
        <div class="detail-subheader">${escapeHtml(ship.name || 'Unknown Ship')}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Ship Art</div>
        </div>
        
        <div class="scan-data">
            <div class="scan-header">Ship Status</div>
            <div class="detail-row">HP: ${ship.hp?.toFixed(1) || 'Unknown'} / ${ship.max_hp?.toFixed(1) || '?'}</div>
            <div class="detail-row">Shield: ${ship.shield_pool?.toFixed(1) || '0.0'}</div>
            <div class="detail-row">Tier: ${ship.tier || 'Unknown'}</div>
            ${ship.is_stealthed ? '<div class="detail-row stealth">[STEALTHED]</div>' : ''}
        </div>
    `;
    
    // Render components if available
    if (ship.components) {
        html += '<div class="scan-data"><div class="scan-header">Components</div>';
        
        const componentOrder = ['engine', 'weapon', 'shield', 'cargo', 'sensor', 'stealth_cloak'];
        for (const slot of componentOrder) {
            const component = ship.components[slot];
            if (component) {
                html += `
                    <div class="detail-row">
                        <strong>${slot.replace('_', ' ').toUpperCase()}:</strong> ${escapeHtml(component.name || 'Unknown')}
                        ${component.health !== undefined ? ` (HP: ${component.health?.toFixed(1)}/${component.max_health?.toFixed(1)})` : ''}
                    </div>
                `;
            } else {
                html += `<div class="detail-row">${slot.replace('_', ' ').toUpperCase()}: [Empty]</div>`;
            }
        }
        
        html += '</div>';
    }
    
    // Render cargo items if available
    if (ship.cargo_items && ship.cargo_items.length > 0) {
        html += '<div class="scan-data"><div class="scan-header">Cargo</div>';
        for (const item of ship.cargo_items) {
            html += `<div class="detail-row">• ${escapeHtml(item.name || 'Unknown Item')}</div>`;
        }
        html += '</div>';
    } else {
        html += '<div class="scan-data"><div class="scan-header">Cargo</div><div class="detail-row">Empty</div></div>';
    }
    
    return html;
}

/**
 * Render scanned item details
 */
function renderScannedItemDetails(item) {
    let html = `
        <div class="detail-header">[SCAN DATA]</div>
        <div class="detail-subheader">${escapeHtml(item.name || 'Unknown Item')}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Item Art</div>
        </div>
        
        <div class="scan-data">
            <div class="scan-header">Item Information</div>
            ${item.tier ? `<div class="detail-row">Tier: ${item.tier}</div>` : ''}
            ${item.type ? `<div class="detail-row">Type: ${escapeHtml(item.type)}</div>` : ''}
            ${item.multiplier !== undefined ? `<div class="detail-row">Multiplier: ${item.multiplier.toFixed(2)}</div>` : ''}
            ${item.health !== undefined ? `<div class="detail-row">Health: ${item.health?.toFixed(1)}/${item.max_health?.toFixed(1)}</div>` : ''}
            ${item.description ? `<div class="detail-row description">${escapeHtml(item.description)}</div>` : ''}
        </div>
    `;
    
    return html;
}

/**
 * Render scanned location details
 */
function renderScannedLocationDetails(location) {
    let html = `
        <div class="detail-header">[SCAN DATA]</div>
        <div class="detail-subheader">${escapeHtml(location.name || 'Unknown Location')}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Location Art</div>
        </div>
        
        <div class="scan-data">
            <div class="scan-header">Location Information</div>
            <div class="detail-row">Type: ${escapeHtml(location.location_type || 'Unknown')}</div>
            ${location.description ? `<div class="detail-row description">${escapeHtml(location.description)}</div>` : ''}
        </div>
    `;
    
    // Show ship information
    if (location.ship_count !== undefined) {
        html += `
            <div class="scan-data">
                <div class="scan-header">Ships Present</div>
                <div class="detail-row">Ship Count: ${location.ship_count}</div>
            </div>
        `;
    } else {
        html += `
            <div class="scan-data">
                <div class="scan-header">Ships Present</div>
                <div class="detail-row">No ships detected</div>
            </div>
        `;
    }
    
    // Show spawnable resources if available
    if (location.spawnable_resources && location.spawnable_resources.length > 0) {
        html += `
            <div class="scan-data">
                <div class="scan-header">Resources</div>
                ${location.spawnable_resources.map(res => `<div class="detail-row">• ${escapeHtml(res)}</div>`).join('')}
            </div>
        `;
    }

    return html;
}

/**
 * Render ship details
 */
function renderShipDetails(ship) {
    let html = `
        <div class="detail-header">${escapeHtml(ship.name)}</div>
        <div class="detail-subheader">Pilot: ${escapeHtml(ship.player_name)}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Ship Art</div>
        </div>
    `;
    
    return html;
}

/**
 * Render item details
 */
function renderItemDetails(item) {
    let html = `
        <div class="detail-header">${escapeHtml(item.name)}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Item Art</div>
        </div>
    `;
    
    return html;
}

/**
 * Render component details
 */
function renderComponentDetails(component) {
    // Debug logging
    console.log('renderComponentDetails called with:', component);
    console.log('gameState.ship:', gameState.ship);
    console.log('gameState.ship?.components:', gameState.ship?.components);
    
    // Get the full component data from gameState.ship.components if available
    const componentData = gameState.ship?.components?.[component.slot];
    
    console.log('Looking for component slot:', component.slot);
    console.log('Found componentData:', componentData);
    
    if (!componentData) {
        return `
            <div class="detail-header">${component.type}</div>
            <div class="art-placeholder">
                <div class="art-placeholder-text">Component Art</div>
            </div>
            <div class="info-message">Component slot: ${component.slot}</div>
            <div class="info-message">No component data available. Try refreshing.</div>
        `;
    }
    
    // Calculate health percentage
    const healthPercent = componentData.maxhealth > 0 
        ? (componentData.health / componentData.maxhealth * 100).toFixed(1) 
        : 0;
    
    return `
        <div class="detail-header">${componentData.name}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Component Art</div>
        </div>
        <div class="info-message">Type: ${component.type}</div>
        <div class="info-message">Tier: ${componentData.tier}</div>
        <div class="info-message">Health: ${componentData.health.toFixed(1)} / ${componentData.maxhealth.toFixed(1)} (${healthPercent}%)</div>
        <div class="info-message">Multiplier: ${(componentData.multiplier * 100).toFixed(0)}%</div>
    `;
}

/**
 * Render cargo item details
 */
function renderCargoItemDetails(item) {
    const itemName = item.name || `Item #${item.item_id}`;
    const itemType = item.type || 'unknown';
    
    let html = `
        <div class="detail-header">${escapeHtml(itemName)}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Item Art</div>
        </div>
        <div class="detail-row">Type: ${escapeHtml(itemType)}</div>
    `;
    
    // Show tier if available
    if (item.tier !== undefined) {
        html += `<div class="detail-row">Tier: ${item.tier}</div>`;
    }
    
    // Show multiplier if available
    if (item.multiplier !== undefined) {
        html += `<div class="detail-row">Multiplier: ${item.multiplier.toFixed(2)}</div>`;
    }
    
    // Show health if available
    if (item.health !== undefined && item.maxhealth !== undefined) {
        html += `<div class="detail-row">Health: ${item.health}/${item.maxhealth}</div>`;
    }
    
    html += '<div class="info-message">Click Equip to install this component</div>';
    
    return html;
}

/**
 * Render destination details
 */
function renderDestinationDetails(destination) {
    let html = `
        <div class="detail-header">${escapeHtml(destination.name)}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Location Art</div>
        </div>
    `;
    
    if (destination.description) {
        html += `<div class="detail-row">${escapeHtml(destination.description)}</div>`;
    }
    
    return html;
}

/**
 * Render location details (for current location or selected location)
 */
function renderLocationDetails(location) {
    let html = `
        <div class="detail-header">${escapeHtml(location.name)}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Location Art</div>
        </div>
    `;
    
    if (location.description) {
        html += `<div class="detail-row">${escapeHtml(location.description)}</div>`;
    }
    
    if (location.isCurrent) {
        html += '<div class="info-message">[Current Location]</div>';
    } else {
        html += '<div class="info-message">Available destination</div>';
    }
    
    return html;
}

/**
 * Render vendor details
 */
function renderVendorDetails(vendor) {
    let html = `
        <div class="detail-header">${vendor.vendor_type}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Vendor Art</div>
        </div>
    `;


    
    html += '<div class="info-message">Vendor interaction coming soon...</div>';
    
    return html;
}




/**
 * Render actions section
 */
function renderActions() {
    const actionsContainer = document.getElementById('actions-section');
    if (!actionsContainer) return;
    
    // Show queued action indicator
    let html = '';
    if (gameState.queuedAction) {
        html += `
            <div class="queued-action">
                [ACTION QUEUED: ${gameState.queuedAction.type}]
            </div>
        `;
    }
    
    // If showing scan data, don't show action buttons
    if (gameState.isShowingScanData) {
        actionsContainer.innerHTML = html + '<div class="info-message">Scan data display - no actions available</div>';
        return;
    }
    
    // Show action buttons based on selected item
    if (!gameState.selectedItem) {
        actionsContainer.innerHTML = html + '<div class="empty-message">Select an item to see actions</div>';
        return;
    }
    
    html += '<div class="action-buttons">';
    
    switch (gameState.selectedItemType) {
        case 'ship':
            html += renderShipActions(gameState.selectedItem);
            break;
        case 'item':
            html += renderItemActions(gameState.selectedItem);
            break;
        case 'component':
            html += renderComponentActions(gameState.selectedItem);
            break;
        case 'cargo_item':
            html += renderCargoItemActions(gameState.selectedItem);
            break;
        case 'destination':
            html += renderDestinationActions(gameState.selectedItem);
            break;
        case 'location':
            html += renderLocationActions(gameState.selectedItem);
            break;
        case 'vendor':
            html += renderVendorActions(gameState.selectedItem);
            break;
        default:
            html += '<div class="empty-message">No actions available</div>';
    }
    
    html += '</div>';
    actionsContainer.innerHTML = html;
}

/**
 * Render ship action buttons
 */
function renderShipActions(ship) {
    let html = `
        <button class="action-btn" onclick="handleAction('scan', '${ship.ship_id}', {target_type: 'ship'})">
            [Scan Ship]
        </button>
        <button class="action-btn" onclick="handleAction('attack_ship', '${ship.ship_id}')">
            [Attack Ship]
        </button>
    `;
    
    // Add message button for player ships
    if (ship.player_id) {
        html += `
            <button class="action-btn" onclick="handleMessageShip('${ship.ship_id}', '${escapeHtml(ship.player_name)}')">
                [Message ${escapeHtml(ship.player_name)}]
            </button>
        `;
    }
    
    // Placeholder for dialogue options (not yet implemented)
    html += '<div class="dialogue-placeholder" style="display:none;"></div>';
    
    return html;
}

/**
 * Render item action buttons
 */
function renderItemActions(item) {
    return `
        <button class="action-btn" onclick="handleAction('scan', '${item.item_id}', {target_type: 'item'})">
            [Scan Item]
        </button>
        <button class="action-btn" onclick="handleAction('collect', '${item.item_id}')">
            [Collect Item]
        </button>
    `;
}

/**
 * Render component action buttons
 */
function renderComponentActions(component) {
    // Only show unequip if component is equipped (has an ID)
    const componentData = gameState.ship?.components?.[component.slot];
    
    if (componentData && componentData.id) {
        return `
            <button class="action-btn" onclick="handleUnequipComponent('${component.slot}')">
                [Unequip ${component.type}]
            </button>
            <div class="info-message">Component repairs available at repair shops</div>
        `;
    }
    
    return '<div class="info-message">Empty component slot</div>';
}

/**
 * Render cargo item action buttons
 */
function renderCargoItemActions(cargoItem) {
    return `
        <button class="action-btn" onclick="handleEquipItem('${cargoItem.item_id}')">
            [Equip Item]
        </button>
        <button class="action-btn" onclick="handleAction('drop', '${cargoItem.item_id}')">
            [Drop Item]
        </button>
        <div class="info-message">Install component from cargo</div>
    `;
}

/**
 * Render destination action buttons
 */
function renderDestinationActions(destination) {
    return `
        <button class="action-btn" onclick='handleAction("move", "${escapeHtml(destination.name)}")'>
            [Move to ${escapeHtml(destination.name)}]
        </button>
        <button class="action-btn" onclick='handleAction("scan", "${escapeHtml(destination.name)}", {target_type: "location"})'>
            [Scan Location]
        </button>
    `;
}

/**
 * Render location action buttons
 */
function renderLocationActions(location) {
    // If it's the current location, can't move to it or scan it
    if (location.isCurrent) {
        return '<div class="info-message">You are currently at this location</div>';
    }
    
    // Otherwise, show move and scan actions
    return `
        <button class="action-btn" onclick='handleAction("move", "${escapeHtml(location.name)}")'>
            [Jump to ${escapeHtml(location.name)}]
        </button>
        <button class="action-btn" onclick='handleAction("scan", "${escapeHtml(location.name)}", {target_type: "location"})'>
            [Scan Location]
        </button>
    `;
}

/**
 * Handle unequip component action
 */
async function handleUnequipComponent(slotName) {
    try {
        console.log('Unequipping component from slot:', slotName);
        await unequipItem(slotName);
        // Backend pushes an instant WS update with the new log entry and ship state
    } catch (error) {
        console.error('Failed to unequip component:', error);
        addLogMessage(`Failed to unequip: ${error.message}`, 'error');
        renderUI();
    }
}

/**
 * Handle equip item action
 */
async function handleEquipItem(itemId) {
    try {
        console.log('Equipping item:', itemId);
        await equipItem(itemId);
        // Backend pushes an instant WS update with the new log entry and ship state
    } catch (error) {
        console.error('Failed to equip:', error);
        addLogMessage(`Failed to equip: ${error.message}`, 'error');
        renderUI();
    }
}

/**
 * Render vendor action buttons
 */
function renderVendorActions(vendor) {
    return `
        <div class="info-message">Vendor actions coming soon...</div>
    `;
}

/**
 * Handle repair component action
 */
/**
 * Handle message ship action
 */
async function handleMessageShip(shipId, playerName) {
    const message = prompt(`Send message to ${playerName}:`);
    if (!message || message.trim() === '') {
        return;
    }
    
    try {
        console.log('Sending message to ship:', shipId, message);
        await handleAction('message_ship', shipId, {message: message.trim()});
        // Confirmation will arrive via the next tick update
    } catch (error) {
        console.error('Failed to send message:', error);
        addLogMessage(`Failed to send message: ${error.message}`, 'error');
    }
}
