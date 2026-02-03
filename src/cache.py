import json
import os
import time
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_dir="data/.cache", default_ttl=300):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        self.memory_cache = {}
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_file(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def set(self, key, value, ttl=None, ttl_seconds=None):
        # Accept either ttl (seconds) or ttl_seconds for backwards compatibility
        if ttl_seconds is not None and ttl is None:
            ttl = ttl_seconds
        ttl = ttl or self.default_ttl
        timestamp = datetime.now()
        expiry = timestamp + timedelta(seconds=ttl)
        
        cache_data = {
            "value": value,
            "timestamp": timestamp.isoformat(),
            "expiry": expiry.isoformat()
        }
        
        self.memory_cache[key] = cache_data
        
        try:
            with open(self._get_cache_file(key), "w", encoding="utf-8") as f:
                json.dump(cache_data, f)
        except:
            pass

# Module-level instance for convenience

    def get(self, key):
        if key in self.memory_cache:
            data = self.memory_cache[key]
            if datetime.fromisoformat(data["expiry"]) > datetime.now():
                return data["value"]
            else:
                del self.memory_cache[key]
        
        cache_file = self._get_cache_file(key)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if datetime.fromisoformat(data["expiry"]) > datetime.now():
                    self.memory_cache[key] = data
                    return data["value"]
                else:
                    os.remove(cache_file)
            except:
                pass
        
        return None
    
    def clear(self):
        self.memory_cache.clear()
        for f in os.listdir(self.cache_dir):
            try:
                os.remove(os.path.join(self.cache_dir, f))
            except:
                pass
    
    def get_ttl_remaining(self, key):
        if key in self.memory_cache:
            expiry = datetime.fromisoformat(self.memory_cache[key]["expiry"])
            remaining = (expiry - datetime.now()).total_seconds()
            return max(0, remaining)
        return 0
    
    def get_stats(self):
        return {
            "memory_items": len(self.memory_cache),
            "disk_items": len([f for f in os.listdir(self.cache_dir) if f.endswith(".json")])
        }

# Module-level instance for convenience
cache_manager = CacheManager()
