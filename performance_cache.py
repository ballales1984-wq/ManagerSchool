"""
Sistema di caching per Flask con Flask-Caching.
"""

from flask import Flask, g
try:
    from flask_caching import Cache
except ImportError:
    # Fallback se Flask-Caching non disponibile
    Cache = None
from typing import Any, Optional, Dict
from functools import wraps
import time


# Configurazione cache
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minuti
}


def get_cache_timeout(seconds: int = 300):
    """Ottiene configurazione timeout cache.
    
    Args:
        seconds: Secondi timeout
        
    Returns:
        Configurazione timeout
    """
    return {'timeout': seconds}


class CacheManager:
    """Manager per sistema caching."""
    
    def __init__(self, app: Optional[Flask] = None):
        """Inizializza cache manager.
        
        Args:
            app: Flask app
        """
        self.cache = None
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Inizializza cache su app Flask.
        
        Args:
            app: Flask app
        """
        app.config.from_mapping(cache_config)
        self.cache = Cache(app)
    
    def cached(self, timeout: int = 300, key_prefix: str = ""):
        """Decorator per cacheare risultato funzione.
        
        Args:
            timeout: Timeout in secondi
            key_prefix: Prefisso chiave
            
        Returns:
            Funzione decorata
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.cache:
                    return f(*args, **kwargs)
                
                # Genera chiave cache
                cache_key = f"{key_prefix}:{f.__name__}"
                if args:
                    cache_key += f":{args}"
                if kwargs:
                    cache_key += f":{sorted(kwargs.items())}"
                
                # Prova a recuperare da cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Esegui funzione e salva in cache
                result = f(*args, **kwargs)
                self.cache.set(cache_key, result, timeout=timeout)
                return result
            
            return decorated_function
        return decorator
    
    def clear_all(self):
        """Pulisce tutta la cache."""
        if self.cache:
            self.cache.clear()
    
    def statistiche(self) -> Dict:
        """Ottiene statistiche cache.
        
        Returns:
            Statistiche
        """
        if not self.cache:
            return {'errore': 'Cache non inizializzata'}
        
        # Statistiche base (dipendono dal backend cache)
        return {
            'type': cache_config.get('CACHE_TYPE', 'unknown'),
            'timeout': cache_config.get('CACHE_DEFAULT_TIMEOUT', 0),
            'status': 'active'
        }


# Esempi di utilizzo
def esempio_studenti_classe_cached(anagrafica, classe: str):
    """Esempio: cache su query studenti per classe."""
    # Questa funzione dovrebbe essere decorata con @cache_manager.cached()
    studenti = anagrafica.studenti_per_classe(classe)
    return [s.to_dict() for s in studenti]


def esempio_voti_studente_cached(gestione_voti, id_studente: int):
    """Esempio: cache su query voti studente."""
    # Questa funzione dovrebbe essere decorata con @cache_manager.cached()
    voti = gestione_voti.voti_studente(id_studente)
    return [v.to_dict() for v in voti]


if __name__ == "__main__":
    print("PERFORMANCE CACHE - TEST")
    print("=" * 60 + "\n")
    
    from flask import Flask
    
    app = Flask(__name__)
    cache_manager = CacheManager(app)
    
    # Test statistiche
    stats = cache_manager.statistiche()
    print(f"Cache configurata:")
    print(f"  Type: {stats['type']}")
    print(f"  Timeout: {stats['timeout']}s")
    print(f"  Status: {stats['status']}")
    
    # Esempio di uso
    print("\nPer usare caching su funzioni:")
    print("""
    @cache_manager.cached(timeout=300, key_prefix="studenti")
    def get_studenti_classe(classe):
        return query_ottimizzata_studenti_classe(classe)
    """)
    
    print("\n✅ Cache setup completato!")

