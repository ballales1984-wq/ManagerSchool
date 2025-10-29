"""
Sistema di ottimizzazione performance completo.
Integra indici, cache, PostgreSQL.
"""

from performance_db import PerformanceDatabaseManager
from performance_cache import CacheManager
from performance_postgresql import PostgreSQLManager
from typing import Dict, Optional
import time


class PerformanceOptimizer:
    """Optimizer completo per performance."""
    
    def __init__(self, db_type: str = "sqlite", db_path: str = "managerschool.db"):
        """Inizializza optimizer.
        
        Args:
            db_type: Tipo database (sqlite/postgresql)
            db_path: Percorso database
        """
        self.db_type = db_type
        self.db = None
        self.cache = None
        
        if db_type == "sqlite":
            self.db = PerformanceDatabaseManager(db_path)
        else:
            # PostgreSQL sarà inizializzato separatamente
            self.db = None
    
    def setup_sqlite(self, db_path: str):
        """Setup SQLite ottimizzato."""
        self.db = PerformanceDatabaseManager(db_path)
        return self.db
    
    def setup_postgresql(self, database: str, user: str, password: str,
                        host: str = "localhost", port: int = 5432):
        """Setup PostgreSQL.
        
        Args:
            database: Nome database
            user: Username
            password: Password
            host: Host
            port: Porta
        """
        self.db = PostgreSQLManager(database, user, password, host, port)
        self.db.connect()
        self.db.crea_tabelle()
        self.db.crea_indici_performance()
        return self.db
    
    def benchmark_query(self, query_name: str, query_func, *args):
        """Benchmark di una query.
        
        Args:
            query_name: Nome query
            query_func: Funzione query
            args: Argomenti
            
        Returns:
            Risultato e tempo
        """
        start = time.time()
        result = query_func(*args)
        elapsed = time.time() - start
        
        return {
            'query': query_name,
            'tempo_ms': elapsed * 1000,
            'risultati': len(result) if isinstance(result, list) else 1,
            'risultati_al_sec': (len(result) / elapsed) if isinstance(result, list) and elapsed > 0 else 0
        }
    
    def report_performance(self) -> Dict:
        """Genera report performance.
        
        Returns:
            Report
        """
        report = {
            'database_type': self.db_type,
            'indici_attivi': True if self.db_type == 'sqlite' else False,
            'cache_attiva': self.cache is not None
        }
        
        if self.db_type == 'sqlite':
            stats = self.db.statistiche_indici()
            report['indici'] = stats['indici']
            report['totale_indici'] = stats['totale_indici']
        
        return report


def esempio_benchmark():
    """Esempio di benchmark performance."""
    print("PERFORMANCE BENCHMARK")
    print("=" * 60 + "\n")
    
    optimizer = PerformanceOptimizer()
    db = optimizer.setup_sqlite("test_perf.db")
    
    # Aggiungi dati test
    for i in range(1, 11):
        db.aggiungi_studente({
            'id': i,
            'nome': f'Nome{i}',
            'cognome': f'Cognome{i}',
            'eta': 15 + (i % 3),
            'classe': f'{(i % 3) + 1}A',
            'reddito_familiare': 30000 + (i * 1000),
            'categoria_reddito': 'MEDIO',
            'condizione_salute': 'BUONA',
            'situazione_familiare': 'Tradizionale',
            'note': ''
        })
    
    # Benchmark query
    print("Benchmark query ottimizzate:")
    
    result1 = optimizer.benchmark_query(
        "Studenti per classe",
        db.query_ottimizzata_studenti_classe,
        "1A"
    )
    print(f"  {result1['query']}: {result1['tempo_ms']:.2f}ms, "
          f"{result1['risultati']} risultati")
    
    result2 = optimizer.benchmark_query(
        "Voti studente",
        db.query_ottimizzata_voti_studente,
        1
    )
    print(f"  {result2['query']}: {result2['tempo_ms']:.2f}ms")
    
    # Report
    report = optimizer.report_performance()
    print(f"\nReport performance:")
    print(f"  Database: {report['database_type']}")
    print(f"  Indici: {report['totale_indici']}")


if __name__ == "__main__":
    esempio_benchmark()

