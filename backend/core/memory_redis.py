"""
In-memory Redis replacement for demo purposes.

This module provides a simple in-memory implementation of Redis functionality
for development and demo environments where Redis is not available.
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class MemoryRedis:
    """In-memory Redis-like implementation."""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
        self._subscribers: Dict[str, List] = {}
        
    async def ping(self) -> bool:
        """Ping the server."""
        return True
    
    async def get(self, key: str) -> Optional[str]:
        """Get a value by key."""
        if self._is_expired(key):
            self._delete_key(key)
            return None
        return self._data.get(key)
    
    async def set(self, key: str, value: str) -> bool:
        """Set a key-value pair."""
        self._data[key] = value
        return True
    
    async def setex(self, key: str, ttl: int, value: str) -> bool:
        """Set a key-value pair with TTL."""
        self._data[key] = value
        self._expiry[key] = time.time() + ttl
        return True
    
    async def delete(self, key: str) -> int:
        """Delete a key."""
        if key in self._data:
            self._delete_key(key)
            return 1
        return 0
    
    async def lpush(self, key: str, value: str) -> int:
        """Push to the left of a list."""
        if key not in self._data:
            self._data[key] = []
        self._data[key].insert(0, value)
        return len(self._data[key])
    
    async def brpop(self, key: str, timeout: int = 0) -> Optional[tuple]:
        """Blocking right pop from list."""
        start_time = time.time()
        
        while True:
            if key in self._data and self._data[key]:
                value = self._data[key].pop()
                return (key.encode(), value.encode())
            
            if timeout > 0 and (time.time() - start_time) >= timeout:
                return None
                
            await asyncio.sleep(0.1)
    
    async def publish(self, channel: str, message: str) -> int:
        """Publish a message to a channel."""
        if channel in self._subscribers:
            for subscriber in self._subscribers[channel]:
                await subscriber.put({
                    'type': 'message',
                    'channel': channel,
                    'data': message
                })
            return len(self._subscribers[channel])
        return 0
    
    def _is_expired(self, key: str) -> bool:
        """Check if a key has expired."""
        if key in self._expiry:
            return time.time() > self._expiry[key]
        return False
    
    def _delete_key(self, key: str) -> None:
        """Delete a key and its expiry."""
        self._data.pop(key, None)
        self._expiry.pop(key, None)


class MemoryPubSub:
    """In-memory pub/sub implementation."""
    
    def __init__(self, redis_instance: MemoryRedis):
        self.redis = redis_instance
        self.channels = set()
        self.queue = asyncio.Queue()
    
    async def subscribe(self, channel: str):
        """Subscribe to a channel."""
        self.channels.add(channel)
        if channel not in self.redis._subscribers:
            self.redis._subscribers[channel] = []
        self.redis._subscribers[channel].append(self.queue)
    
    async def listen(self):
        """Listen for messages."""
        while True:
            message = await self.queue.get()
            yield message


# Global instance
_memory_redis = MemoryRedis()


def get_memory_redis() -> MemoryRedis:
    """Get the global memory Redis instance."""
    return _memory_redis