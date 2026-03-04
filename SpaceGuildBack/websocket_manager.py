# SpaceGuildBack/websocket_manager.py
# WebSocket connection manager for handling up to 1M concurrent connections
# Uses async/await for efficient connection management

from typing import Dict, Set, Optional, Any
from fastapi import WebSocket
import asyncio
import logging
import json

logger = logging.getLogger('websocket_manager')


class ConnectionManager:
    """
    Manages WebSocket connections for the Space Guild game.
    
    Design for scale:
    - Each connection is an async task (5-10KB overhead)
    - Can handle 100k-200k concurrent connections per server instance
    - Broadcasts tick updates to all connected clients efficiently
    """
    
    def __init__(self):
        # Active connections: ship_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}
        
        # Lock for thread-safe connection management
        self._lock = asyncio.Lock()
        
        logger.info("ConnectionManager initialized")
    
    async def connect(self, ship_id: int, websocket: WebSocket):
        """
        Register a new WebSocket connection for a ship.
        
        Args:
            ship_id: The ship's unique ID
            websocket: The WebSocket connection object
        """
        await websocket.accept()
        
        async with self._lock:
            # If ship already has a connection, close the old one
            if ship_id in self.active_connections:
                old_ws = self.active_connections[ship_id]
                try:
                    await old_ws.close(code=1000, reason="New connection established")
                except Exception:
                    pass  # Old connection may already be closed
            
            self.active_connections[ship_id] = websocket
            logger.info(f"Ship {ship_id} connected. Total connections: {len(self.active_connections)}")
    
    async def disconnect(self, ship_id: int):
        """
        Remove a WebSocket connection.
        
        Args:
            ship_id: The ship's unique ID
        """
        async with self._lock:
            if ship_id in self.active_connections:
                del self.active_connections[ship_id]
                logger.info(f"Ship {ship_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_to_ship(self, ship_id: int, message: dict) -> bool:
        """
        Send a message to a specific ship's WebSocket.
        
        Args:
            ship_id: The ship's unique ID
            message: Dictionary to send as JSON
            
        Returns:
            True if sent successfully, False if ship not connected
        """
        if ship_id not in self.active_connections:
            return False
        
        websocket = self.active_connections[ship_id]
        try:
            await websocket.send_json(message)
            return True
        except Exception as e:
            logger.error(f"Error sending to ship {ship_id}: {e}")
            # Connection is broken, remove it
            await self.disconnect(ship_id)
            return False
    
    async def broadcast_tick(self, tick_number: int, ship_updates: Optional[Dict[int, dict]] = None):
        """
        Broadcast tick completion to all connected clients.
        
        This is called after each game tick completes. It sends updates to all
        connected ships, with optional ship-specific data.
        
        Args:
            tick_number: The completed tick number
            ship_updates: Optional dict of ship_id -> ship-specific update data
        """
        if not self.active_connections:
            return  # No one to notify
        
        disconnected_ships = []
        
        # Get snapshot of connections to avoid holding lock during sends
        async with self._lock:
            connections_snapshot = list(self.active_connections.items())
        
        logger.debug(f"Broadcasting tick {tick_number} to {len(connections_snapshot)} ships")
        
        # Send updates concurrently to all connections
        send_tasks = []
        for ship_id, websocket in connections_snapshot:
            # Build message for this ship
            message = {
                "type": "tick_complete",
                "tick": tick_number,
                "timestamp": None  # Can add timestamp if needed
            }
            
            # Add ship-specific data if available
            if ship_updates and ship_id in ship_updates:
                message["data"] = ship_updates[ship_id]
            
            # Create async task to send
            send_tasks.append(self._send_with_error_handling(ship_id, websocket, message, disconnected_ships))
        
        # Execute all sends concurrently
        await asyncio.gather(*send_tasks, return_exceptions=True)
        
        # Clean up disconnected ships
        if disconnected_ships:
            async with self._lock:
                for ship_id in disconnected_ships:
                    if ship_id in self.active_connections:
                        del self.active_connections[ship_id]
            logger.info(f"Cleaned up {len(disconnected_ships)} disconnected ships")
    
    async def _send_with_error_handling(self, ship_id: int, websocket: WebSocket, message: dict, disconnected_list: list):
        """Helper to send message with error handling."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send to ship {ship_id}: {e}")
            disconnected_list.append(ship_id)
    
    async def broadcast_message(self, message: dict, ship_ids: Optional[Set[int]] = None):
        """
        Broadcast a message to all or specific ships.
        
        Args:
            message: Dictionary to send as JSON
            ship_ids: Optional set of ship IDs to send to. If None, sends to all.
        """
        disconnected_ships = []
        
        async with self._lock:
            if ship_ids is None:
                # Send to all
                connections_snapshot = list(self.active_connections.items())
            else:
                # Send to specific ships
                connections_snapshot = [(sid, ws) for sid, ws in self.active_connections.items() if sid in ship_ids]
        
        # Send concurrently
        send_tasks = [
            self._send_with_error_handling(ship_id, websocket, message, disconnected_ships)
            for ship_id, websocket in connections_snapshot
        ]
        await asyncio.gather(*send_tasks, return_exceptions=True)
        
        # Clean up disconnected
        if disconnected_ships:
            async with self._lock:
                for ship_id in disconnected_ships:
                    if ship_id in self.active_connections:
                        del self.active_connections[ship_id]
    
    def get_connection_count(self) -> int:
        """Get the current number of active connections."""
        return len(self.active_connections)
    
    def is_connected(self, ship_id: int) -> bool:
        """Check if a ship is currently connected."""
        return ship_id in self.active_connections


# Global singleton instance
# Will be imported by api_fastapi.py and program.py
connection_manager = ConnectionManager()
