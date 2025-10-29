"""
Profiler per identificare colli di bottiglia performance.
"""

import time
import cProfile
import pstats
from io import StringIO
from functools import wraps


class PerformanceProfiler:
    """Profiler per analizzare performance del codice."""
    
    def __init__(self):
        self.profiles = {}
    
    def profile_function(self, func_name: str = None):
        """Decorator per profiling di funzioni."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                pr = cProfile.Profile()
                pr.enable()
                
                result = func(*args, **kwargs)
                
                pr.disable()
                
                if func_name:
                    self.profiles[func_name] = pr
                else:
                    self.profiles[func.__name__] = pr
                
                return result
            return wrapper
        return decorator
    
    def print_stats(self, func_name: str, limit: int = 20):
        """Stampa statistiche di profiling."""
        if func_name in self.profiles:
            s = StringIO()
            ps = pstats.Stats(self.profiles[func_name], stream=s)
            ps.sort_stats('cumulative')
            ps.print_stats(limit)
            print(s.getvalue())


def log_performance(func):
    """Decorator semplice per loggare tempi di esecuzione."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        
        if elapsed > 0.1:  # Log solo se lento
            print(f"⚠️ {func.__name__}: {elapsed:.3f}s")
        
        return result
    return wrapper


if __name__ == "__main__":
    print("✅ Profiler utility caricato")
    print("   Usa @log_performance per tracciare performance")

