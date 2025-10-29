"""
Ottimizzazioni database per performance.
Indici, query ottimizzate, supporto PostgreSQL.
"""

import sqlite3
from typing import List, Dict, Optional
from database_manager import DatabaseManager


class PerformanceDatabaseManager(DatabaseManager):
    """Database manager con ottimizzazioni performance."""
    
    def __init__(self, db_path: str):
        """Inizializza con indici."""
        super().__init__(db_path)
        self.crea_indici_performance()
    
    def crea_indici_performance(self):
        """Crea indici per migliorare performance query."""
        cursor = self.conn.cursor()
        
        # Indice su studenti per classe (query frequente)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_studenti_classe 
            ON studenti(classe)
        """)
        
        # Indice su studenti per nome/cognome (ricerca)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_studenti_nome 
            ON studenti(cognome, nome)
        """)
        
        # Indice su voti per studente (query frequente)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_voti_studente 
            ON voti(id_studente)
        """)
        
        # Indice su voti per materia
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_voti_materia 
            ON voti(materia)
        """)
        
        # Indice composito su voti per data
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_voti_data 
            ON voti(data)
        """)
        
        # Indice composito su voti per studente + materia
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_voti_studente_materia 
            ON voti(id_studente, materia)
        """)
        
        # Indice su presenze
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_presenze_studente 
            ON presenze(id_studente)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_presenze_data 
            ON presenze(data)
        """)
        
        self.conn.commit()
        print("✅ Indici performance creati")
    
    def statistiche_indici(self) -> Dict:
        """Ottiene statistiche sugli indici.
        
        Returns:
            Statistiche indici
        """
        cursor = self.conn.cursor()
        
        # Lista indici
        cursor.execute("""
            SELECT name, tbl_name, sql 
            FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
        """)
        
        indici = [{'nome': row[0], 'tabella': row[1], 'definizione': row[2]} 
                 for row in cursor.fetchall()]
        
        return {
            'totale_indici': len(indici),
            'indici': indici
        }
    
    def query_ottimizzata_studenti_classe(self, classe: str) -> List[Dict]:
        """Query ottimizzata per studenti per classe.
        
        Args:
            classe: Classe da cercare
            
        Returns:
            Lista studenti
        """
        # Usa indice idx_studenti_classe
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM studenti WHERE classe = ? ORDER BY cognome, nome", (classe,))
        return [dict(row) for row in cursor.fetchall()]
    
    def query_ottimizzata_voti_studente(self, id_studente: int) -> List[Dict]:
        """Query ottimizzata per voti studente.
        
        Args:
            id_studente: ID studente
            
        Returns:
            Lista voti
        """
        # Usa indice idx_voti_studente
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM voti 
            WHERE id_studente = ? 
            ORDER BY data DESC
        """, (id_studente,))
        return [dict(row) for row in cursor.fetchall()]
    
    def query_ottimizzata_media_per_materia(self, id_studente: int, 
                                            materia: str) -> float:
        """Query ottimizzata media per materia.
        
        Args:
            id_studente: ID studente
            materia: Materia
            
        Returns:
            Media
        """
        # Usa indice composito idx_voti_studente_materia
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT AVG(voto) as media 
            FROM voti 
            WHERE id_studente = ? AND materia = ?
        """, (id_studente, materia))
        
        result = cursor.fetchone()
        return result['media'] if result and result['media'] else 0.0


if __name__ == "__main__":
    print("PERFORMANCE DATABASE - TEST")
    print("=" * 60 + "\n")
    
    # Test database ottimizzato
    import os
    if os.path.exists("test_perf.db"):
        os.remove("test_perf.db")
    
    db = PerformanceDatabaseManager("test_perf.db")
    
    # Test indici
    stats = db.statistiche_indici()
    print(f"Indici creati: {stats['totale_indici']}")
    print(f"  {', '.join([i['nome'] for i in stats['indici']])}")
    
    # Test query ottimizzate
    print("\nQuery ottimizzate disponibili:")
    print("  - query_ottimizzata_studenti_classe()")
    print("  - query_ottimizzata_voti_studente()")
    print("  - query_ottimizzata_media_per_materia()")
    
    db.close()

