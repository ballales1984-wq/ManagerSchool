"""
Utility per caching dei risultati e ottimizzazione performance.
"""

from functools import lru_cache, wraps
from typing import Any, Callable
import time


class CacheManager:
    """Gestore cache in-memory per ottimizzare performance."""
    
    def __init__(self, max_size: int = 128, ttl_seconds: int = 300):
        """
        Args:
            max_size: Dimensione massima cache
            ttl_seconds: Time To Live in secondi
        """
        self._cache: dict = {}
        self.max_size = max_size
        self.ttl = ttl_seconds
        self._access_times: dict = {}
    
    def get(self, key: str) -> Any:
        """Ottiene un valore dalla cache."""
        if key in self._cache:
            # Controlla TTL
            if time.time() - self._access_times.get(key, 0) < self.ttl:
                return self._cache[key]
            else:
                # Rimuovi se scaduto
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Imposta un valore nella cache."""
        # Rimuovi il più vecchio se cache piena
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._access_times.items(), key=lambda x: x[1])[0]
            del self._cache[oldest_key]
            del self._access_times[oldest_key]
        
        self._cache[key] = value
        self._access_times[key] = time.time()
    
    def clear(self):
        """Svuota la cache."""
        self._cache.clear()
        self._access_times.clear()
    
    def size(self) -> int:
        """Ritorna dimensione cache."""
        return len(self._cache)


# Cache globale
_global_cache = CacheManager(max_size=256, ttl_seconds=300)


def cached(ttl: int = 300):
    """Decorator per cache automatica di funzioni.
    
    Args:
        ttl: Time to live in secondi
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Crea chiave cache
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Controlla cache
            cached_value = _global_cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Esegui funzione e salva in cache
            result = func(*args, **kwargs)
            _global_cache.set(key, result)
            return result
        
        return wrapper
    return decorator


# Funzioni di utilità per performance
def measure_time(func: Callable) -> Callable:
    """Decorator per misurare tempo esecuzione."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️ {func.__name__}: {elapsed:.3f}s")
        return result
    return wrapper


def batch_process(items: list, batch_size: int = 100, func: Callable = None):
    """Processa una lista in batch per ottimizzare memoria."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        if func:
            yield from func(batch)
        else:
            yield batch


if __name__ == "__main__":
    print("✅ Cache utility caricata")
    print(f"   Cache size: {_global_cache.size()}")
    print(f"   TTL: {_global_cache.ttl}s")
    print(f"   Max size: {_global_cache.max_size}")

