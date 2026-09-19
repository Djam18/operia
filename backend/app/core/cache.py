import time
import asyncio
from typing import Any, Optional, Dict, Tuple

class AsyncCache:
    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._hits = 0
        self._misses = 0
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._cache:
                val, expires_at = self._cache[key]
                if time.time() < expires_at:
                    self._hits += 1
                    return val
                else:
                    del self._cache[key]
            self._misses += 1
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 60) -> None:
        async with self._lock:
            self._cache[key] = (value, time.time() + ttl_seconds)

    async def invalidate(self, prefix: str) -> int:
        async with self._lock:
            to_remove = [k for k in self._cache.keys() if k.startswith(prefix)]
            for k in to_remove:
                del self._cache[k]
            return len(to_remove)

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()

    async def get_stats(self) -> dict:
        async with self._lock:
            # Clean expired
            now = time.time()
            active_keys = [k for k, (_, exp) in self._cache.items() if exp > now]
            total_req = self._hits + self._misses
            ratio = round((self._hits / total_req * 100), 1) if total_req > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "hit_ratio_percent": ratio,
                "active_keys_count": len(active_keys),
                "total_cached_entries": len(self._cache)
            }

app_cache = AsyncCache()
