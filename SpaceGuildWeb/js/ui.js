// ui.js
// UI rendering functions for all panels
console.log('ui.js loaded');

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
        
        // Disable vendors button if no vendors at location
        const isDisabled = view.id === 'vendors' && 
                          (!gameState.vendors || Object.keys(gameState.vendors).length === 0);
        const disabledClass = isDisabled ? 'disabled' : '';
        
        return `
            <button class="nav-button ${activeClass} ${disabledClass}" 
                    onclick="handleNavigation('${view.id}')"
                    ${isDisabled ? 'disabled' : ''}>
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
 * Render location view (ships and items)
 */
function renderLocationView(panel) {
    if (!gameState.location) {
        panel.innerHTML = '<div class="info">No location data</div>';
        return;
    }
    
    const ships = gameState.location.ships || [];
    const items = gameState.location.items || [];
    
    let html = `<div class="panel-header">Location: ${gameState.location.name}</div>`;
    
    // Ships section
    html += '<div class="section-header">Ships</div>';
    if (ships.length === 0) {
        html += '<div class="empty-message">No other ships here</div>';
    } else {
        html += '<div class="item-list">';
        ships.forEach(ship => {
            const isSelected = gameState.selectedItemType === 'ship' && 
                             gameState.selectedItem?.ship_id === ship.ship_id;
            const selectedClass = isSelected ? 'selected' : '';
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick='handleItemSelection(${JSON.stringify(ship)}, "ship")'>
                    <span class="item-icon">${ship.symbol || 'S'}</span>
                    <div class="item-info">
                        <div class="item-name">${ship.name}</div>
                        <div class="item-detail">Pilot: ${ship.player_name}</div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
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
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick='handleItemSelection(${JSON.stringify(item)}, "item")'>
                    <span class="item-icon">I</span>
                    <div class="item-info">
                        <div class="item-name">${item.name}</div>
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
    
    // Cargo section
    const cargoItems = ship.items || [];
    html += '<div class="section-header">Cargo</div>';
    if (cargoItems.length === 0) {
        html += '<div class="empty-message">Cargo is empty</div>';
    } else {
        html += '<div class="item-list">';
        cargoItems.forEach(itemId => {
            const isSelected = gameState.selectedItemType === 'cargo_item' && 
                             gameState.selectedItem?.item_id === itemId;
            const selectedClass = isSelected ? 'selected' : '';
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick='handleItemSelection(${JSON.stringify({item_id: itemId})}, "cargo_item")'>
                    <span class="item-icon">I</span>
                    <div class="item-info">
                        <div class="item-name">Item #${itemId}</div>
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
    html += `<div class="current-location">Current: ${gameState.location.name}</div>`;
    
    if (links.length === 0) {
        html += '<div class="empty-message">No destinations available</div>';
    } else {
        // Normalize links to objects (handle both old string format and new object format)
        const normalizedLinks = links.map(link => {
            if (typeof link === 'string') {
                // Old format: just a string
                return { name: link, type: 'unknown' };
            } else {
                // New format: object with name and type
                return link;
            }
        });
        
        // Sort links by type: stations first, then ground stations, then space
        const typeOrder = { 'station': 0, 'ground_station': 1, 'space': 2, 'unknown': 3 };
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
                    'unknown': 'Other'
                }[currentType] || 'Other';
                
                html += `</div><div class="section-header">${typeLabel}</div><div class="item-list">`;
            }
            
            const isSelected = gameState.selectedItemType === 'destination' && 
                             gameState.selectedItem?.name === destination.name;
            const selectedClass = isSelected ? 'selected' : '';
            
            // Choose icon based on type
            const icon = {
                'station': '⊕',
                'ground_station': '⊗',
                'space': '>',
                'unknown': '?'
            }[destination.type] || '>';
            
            html += `
                <div class="item-card ${selectedClass}" 
                     onclick='handleItemSelection(${JSON.stringify({name: destination.name, type: destination.type})}, "destination")'>
                    <span class="item-icon">${icon}</span>
                    <div class="item-info">
                        <div class="item-name">${destination.name}</div>
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
    
    const html = gameState.shipLog.map(entry => {
        // Handle different log entry formats
        const message = entry.message || entry;
        const type = entry.type || 'info';
        
        return `<div class="log-entry log-${type}">${message}</div>`;
    }).join('');
    
    logContainer.innerHTML = html;
    
    // Auto-scroll to bottom
    logContainer.scrollTop = logContainer.scrollHeight;
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
        case 'vendor':
            html = renderVendorDetails(gameState.selectedItem);
            break;
        default:
            html = '<div class="empty-message">Unknown item type</div>';
    }
    
    detailsContainer.innerHTML = html;
}

/**
 * Render ship details
 */
function renderShipDetails(ship) {
    let html = `
        <div class="detail-header">${ship.name}</div>
        <div class="detail-subheader">Pilot: ${ship.player_name}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Ship Art</div>
        </div>
    `;
    
    // Show scan data if available
    if (gameState.scanData && gameState.scanData.ship_id === ship.ship_id) {
        const scan = gameState.scanData;
        html += `
            <div class="scan-data">
                <div class="scan-header">Scan Data</div>
                <div class="detail-row">HP: ${scan.hp?.toFixed(1) || 'Unknown'}</div>
                <div class="detail-row">Tier: ${scan.tier || 'Unknown'}</div>
                <div class="detail-row">Shield: ${scan.shield_pool?.toFixed(1) || 'Unknown'}</div>
                ${scan.is_stealthed ? '<div class="detail-row stealth">[STEALTHED]</div>' : ''}
            </div>
        `;
    } else {
        html += '<div class="info-message">Scan ship for detailed information</div>';
    }
    
    return html;
}

/**
 * Render item details
 */
function renderItemDetails(item) {
    let html = `
        <div class="detail-header">${item.name}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Item Art</div>
        </div>
    `;
    
    // Show scan data if available
    if (gameState.scanData && gameState.scanData.item_id === item.item_id) {
        const scan = gameState.scanData;
        html += `
            <div class="scan-data">
                <div class="scan-header">Scan Data</div>
                ${scan.tier ? `<div class="detail-row">Tier: ${scan.tier}</div>` : ''}
                ${scan.type ? `<div class="detail-row">Type: ${scan.type}</div>` : ''}
                ${scan.multiplier ? `<div class="detail-row">Multiplier: ${scan.multiplier.toFixed(2)}</div>` : ''}
            </div>
        `;
    } else {
        html += '<div class="info-message">Scan item for detailed information</div>';
    }
    
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
    return `
        <div class="detail-header">Cargo Item</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Item Art</div>
        </div>
        <div class="info-message">Item ID: ${item.item_id}</div>
    `;
}

/**
 * Render destination details
 */
function renderDestinationDetails(destination) {
    return `
        <div class="detail-header">${destination.name}</div>
        <div class="art-placeholder">
            <div class="art-placeholder-text">Location Art</div>
        </div>
        <div class="info-message">Available destination</div>
    `;
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
    
    if (vendor.entry_dialogue) {
        html += `<div class="vendor-dialogue">"${vendor.entry_dialogue}"</div>`;
    }
    
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
        case 'destination':
            html += renderDestinationActions(gameState.selectedItem);
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
    return `
        <button class="action-btn" onclick="handleAction('scan', '${ship.ship_id}', 'ship')">
            [Scan Ship]
        </button>
        <button class="action-btn" onclick="handleAction('attack_ship', '${ship.ship_id}')">
            [Attack Ship]
        </button>
    `;
}

/**
 * Render item action buttons
 */
function renderItemActions(item) {
    return `
        <button class="action-btn" onclick="handleAction('scan', '${item.item_id}', 'item')">
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
    return `
        <button class="action-btn" onclick="handleRepairComponent('${component.item_id}')">
            [Repair Component]
        </button>
    `;
}

/**
 * Render destination action buttons
 */
function renderDestinationActions(destination) {
    return `
        <button class="action-btn" onclick='handleAction("move", "${destination.name}")'>
            [Move to ${destination.name}]
        </button>
    `;
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
async function handleRepairComponent(itemId) {
    try {
        console.log('Repairing component:', itemId);
        const result = await repairComponent(itemId);
        console.log('Repair result:', result);
        addLogMessage(`Component repaired! Health restored: ${result.health_restored.toFixed(1)}`, 'success');
        
        // Reload ship data
        gameState.ship = await getShip();
        renderUI();
        
    } catch (error) {
        console.error('Failed to repair component:', error);
        addLogMessage(`Repair failed: ${error.message}`, 'error');
        renderUI();
    }
}
