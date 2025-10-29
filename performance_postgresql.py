"""
Supporto PostgreSQL per scalabilità.
"""

from typing import Optional, Dict, List, Any
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    # Fallback se psycopg2 non disponibile
    psycopg2 = None

from contextlib import contextmanager


class PostgreSQLManager:
    """Manager per connessione PostgreSQL."""
    
    def __init__(self, database: str, user: str, password: str, 
                 host: str = "localhost", port: int = 5432):
        """Inizializza connessione PostgreSQL.
        
        Args:
            database: Nome database
            user: Username
            password: Password
            host: Host
            port: Porta
        """
        self.conn_params = {
            'database': database,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.conn = None
    
    def connect(self):
        """Connette a PostgreSQL."""
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 non disponibile. Installa con: pip install psycopg2-binary")
        
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("✅ Connesso a PostgreSQL")
        except Exception as e:
            print(f"❌ Errore connessione: {e}")
            raise
    
    def disconnect(self):
        """Disconnette da PostgreSQL."""
        if self.conn:
            self.conn.close()
            print("✅ Disconnesso da PostgreSQL")
    
    @contextmanager
    def transaction(self):
        """Context manager per transazioni."""
        if not self.conn:
            self.connect()
        
        try:
            yield self.conn
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Esegue query SELECT.
        
        Args:
            query: Query SQL
            params: Parametri
            
        Returns:
            Lista risultati
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 non disponibile")
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Esegue query UPDATE/INSERT/DELETE.
        
        Args:
            query: Query SQL
            params: Parametri
            
        Returns:
            Numero righe modificate
        """
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount
    
    def crea_tabelle(self):
        """Crea tabelle base."""
        tables = """
        CREATE TABLE IF NOT EXISTS studenti (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cognome VARCHAR(100) NOT NULL,
            eta INTEGER,
            classe VARCHAR(10),
            reddito_familiare DECIMAL,
            categoria_reddito VARCHAR(50),
            condizione_salute VARCHAR(50),
            situazione_familiare TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS voti (
            id SERIAL PRIMARY KEY,
            id_studente INTEGER REFERENCES studenti(id),
            materia VARCHAR(100),
            voto DECIMAL(3,1),
            tipo VARCHAR(50),
            data DATE,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS presenze (
            id SERIAL PRIMARY KEY,
            id_studente INTEGER REFERENCES studenti(id),
            data DATE,
            tipo VARCHAR(50),
            motivo TEXT,
            giustificato BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with self.transaction():
            self.conn.cursor().execute(tables)
    
    def crea_indici_performance(self):
        """Crea indici per performance."""
        indexes = """
        CREATE INDEX IF NOT EXISTS idx_studenti_classe ON studenti(classe);
        CREATE INDEX IF NOT EXISTS idx_studenti_nome ON studenti(cognome, nome);
        CREATE INDEX IF NOT EXISTS idx_voti_studente ON voti(id_studente);
        CREATE INDEX IF NOT EXISTS idx_voti_materia ON voti(materia);
        CREATE INDEX IF NOT EXISTS idx_voti_data ON voti(data);
        CREATE INDEX IF NOT EXISTS idx_voti_composito ON voti(id_studente, materia);
        CREATE INDEX IF NOT EXISTS idx_presenze_studente ON presenze(id_studente);
        CREATE INDEX IF NOT EXISTS idx_presenze_data ON presenze(data);
        """
        
        with self.transaction():
            self.conn.cursor().execute(indexes)
        print("✅ Indici PostgreSQL creati")
    
    def migra_da_sqlite(self, sqlite_db: str):
        """Migra dati da SQLite a PostgreSQL.
        
        Args:
            sqlite_db: Percorso database SQLite
        """
        import sqlite3
        
        # Connetti a SQLite
        sqlite_conn = sqlite3.connect(sqlite_db)
        sqlite_conn.row_factory = sqlite3.Row
        
        try:
            # Migra studenti
            sqlite_cursor = sqlite_conn.execute("SELECT * FROM studenti")
            for row in sqlite_cursor:
                self.execute_update("""
                    INSERT INTO studenti (id, nome, cognome, eta, classe, 
                                         reddito_familiare, categoria_reddito,
                                         condizione_salute, situazione_familiare, note)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (row['id'], row['nome'], row['cognome'], row['eta'],
                      row['classe'], row['reddito_familiare'], row['categoria_reddito'],
                      row['condizione_salute'], row['situazione_familiare'], row['note']))
            
            # Migra voti
            sqlite_cursor = sqlite_conn.execute("SELECT * FROM voti")
            for row in sqlite_cursor:
                self.execute_update("""
                    INSERT INTO voti (id_studente, materia, voto, tipo, data, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (row['id_studente'], row['materia'], row['voto'],
                      row['tipo'], row['data'], row['note']))
            
            print("✅ Migrazione SQLite -> PostgreSQL completata")
            
        finally:
            sqlite_conn.close()
            if self.conn:
                self.conn.commit()


if __name__ == "__main__":
    print("POSTGRESQL SUPPORT - TEST")
    print("=" * 60 + "\n")
    
    print("Per usare PostgreSQL:")
    print("""
    # Connessione
    pg_manager = PostgreSQLManager(
        database="managerschool",
        user="postgres",
        password="password",
        host="localhost",
        port=5432
    )
    
    # Crea tabelle e indici
    pg_manager.connect()
    pg_manager.crea_tabelle()
    pg_manager.crea_indici_performance()
    
    # Migra da SQLite (opzionale)
    pg_manager.migra_da_sqlite("managerschool.db")
    
    # Query
    studenti = pg_manager.execute_query("SELECT * FROM studenti WHERE classe = %s", ("2A",))
    """)
    
    print("\n✅ PostgreSQL support ready!")

