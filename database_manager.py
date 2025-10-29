"""
Gestore Database SQLite per persistenza dati.
Sostituisce il sistema JSON con un database relazionale.
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json


class DatabaseManager:
    """Gestisce il database SQLite per ManagerSchool."""
    
    def __init__(self, db_path: str = "managerschool.db"):
        """Inizializza il gestore database.
        
        Args:
            db_path: Percorso del file database
        """
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.init_database()
    
    def connect(self):
        """Stabilisce connessione con il database."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Accesso come dizionario
            print(f"[OK] Connesso al database: {self.db_path}")
        except Exception as e:
            print(f"[ERRORE] Errore connessione database: {e}")
    
    def close(self):
        """Chiude la connessione."""
        if self.conn:
            self.conn.close()
    
    def init_database(self):
        """Inizializza il database creando tutte le tabelle."""
        cursor = self.conn.cursor()
        
        # Tabella Studenti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS studenti (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                eta INTEGER NOT NULL,
                classe TEXT NOT NULL,
                reddito_familiare INTEGER,
                categoria_reddito TEXT,
                condizione_salute TEXT,
                situazione_familiare TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella Insegnanti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insegnanti (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                eta INTEGER NOT NULL,
                materie TEXT,  -- JSON array
                ore_settimanali TEXT,  -- JSON dict
                anni_esperienza INTEGER,
                sezioni_assegnate TEXT,  -- JSON array
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella Voti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_studente INTEGER NOT NULL,
                materia TEXT NOT NULL,
                voto REAL NOT NULL,
                tipo TEXT NOT NULL,
                data TEXT NOT NULL,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(id_studente) REFERENCES studenti(id)
            )
        """)
        
        # Tabella Pagelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagelle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_studente INTEGER NOT NULL,
                quadrimestre TEXT NOT NULL,
                voti_materie TEXT,  -- JSON dict
                media_generale REAL,
                comportamento INTEGER,
                assenze INTEGER,
                note TEXT,
                data_compilazione TEXT,
                FOREIGN KEY(id_studente) REFERENCES studenti(id)
            )
        """)
        
        # Tabella Presenze
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presenze (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_studente INTEGER NOT NULL,
                data TEXT NOT NULL,
                ora TEXT,
                tipo TEXT NOT NULL,
                motivo TEXT,
                giustificato INTEGER DEFAULT 0,
                data_giustifica TEXT,
                docente_registrante TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(id_studente) REFERENCES studenti(id)
            )
        """)
        
        # Tabella Comunicazioni
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comunicazioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mittente_id INTEGER,
                mittente_tipo TEXT,
                destinatario_id INTEGER,
                destinatario_tipo TEXT,
                studente_id INTEGER,
                tipo TEXT,
                priorita TEXT,
                oggetto TEXT NOT NULL,
                messaggio TEXT NOT NULL,
                data_invio TEXT NOT NULL,
                data_lettura TEXT,
                stato TEXT,
                allegati TEXT,  -- JSON array
                note_private TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella Backup Info
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL,
                dimensione INTEGER,
                hash TEXT,
                tipo TEXT,
                data_backup TEXT,
                note TEXT
            )
        """)
        
        # Tabella Materiale Didattico
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materiale_didattico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                docente TEXT NOT NULL,
                materia TEXT NOT NULL,
                data_verifica TEXT NOT NULL,
                argomenti TEXT,  -- JSON array
                esercizi_caricati TEXT,  -- JSON array
                link_copilot TEXT,
                note_docente TEXT,
                programma_rispettato INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Indici per performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_studenti_classe ON studenti(classe)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_voti_studente ON voti(id_studente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_voti_materia ON voti(materia)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_presenze_studente ON presenze(id_studente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_presenze_data ON presenze(data)")
        
        self.conn.commit()
        print(" Database inizializzato con successo")
    
    # ============ OPERAZIONI STUDENTI ============
    
    def aggiungi_studente(self, studente: Dict) -> int:
        """Aggiunge uno studente al database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO studenti (id, nome, cognome, eta, classe, reddito_familiare,
                                categoria_reddito, condizione_salute, situazione_familiare, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            studente['id'],
            studente['nome'],
            studente['cognome'],
            studente['eta'],
            studente['classe'],
            studente.get('reddito_familiare', 0),
            studente.get('categoria_reddito', 'MEDIO'),
            studente.get('condizione_salute', 'BUONA'),
            studente.get('situazione_familiare', ''),
            studente.get('note', '')
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def ottieni_studenti(self, classe: Optional[str] = None) -> List[Dict]:
        """Ottiene lista studenti."""
        cursor = self.conn.cursor()
        if classe:
            cursor.execute("SELECT * FROM studenti WHERE classe = ? ORDER BY cognome", (classe,))
        else:
            cursor.execute("SELECT * FROM studenti ORDER BY classe, cognome")
        return [dict(row) for row in cursor.fetchall()]
    
    def conta_studenti(self, classe: Optional[str] = None) -> int:
        """Conta studenti."""
        cursor = self.conn.cursor()
        if classe:
            cursor.execute("SELECT COUNT(*) FROM studenti WHERE classe = ?", (classe,))
        else:
            cursor.execute("SELECT COUNT(*) FROM studenti")
        return cursor.fetchone()[0]
    
    # ============ OPERAZIONI VOTI ============
    
    def aggiungi_voto(self, voto: Dict):
        """Aggiunge un voto al database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO voti (id_studente, materia, voto, tipo, data, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            voto['id_studente'],
            voto['materia'],
            voto['voto'],
            voto.get('tipo', 'Prova scritta'),
            voto.get('data', datetime.now().strftime('%Y-%m-%d')),
            voto.get('note', '')
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def ottieni_voti_studente(self, studente_id: int) -> List[Dict]:
        """Ottiene voti di uno studente."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM voti WHERE id_studente = ?
            ORDER BY data DESC
        """, (studente_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def media_studente(self, studente_id: int, materia: Optional[str] = None) -> float:
        """Calcola media voti di uno studente."""
        cursor = self.conn.cursor()
        if materia:
            cursor.execute("""
                SELECT AVG(voto) FROM voti
                WHERE id_studente = ? AND materia = ?
            """, (studente_id, materia))
        else:
            cursor.execute("""
                SELECT AVG(voto) FROM voti WHERE id_studente = ?
            """, (studente_id,))
        result = cursor.fetchone()[0]
        return result if result else 0.0
    
    # ============ OPERAZIONI PRESENZE ============
    
    def aggiungi_presenza(self, presenza: Dict):
        """Aggiunge una presenza al database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO presenze (id_studente, data, ora, tipo, motivo,
                                 giustificato, data_giustifica, docente_registrante, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            presenza['id_studente'],
            presenza['data'],
            presenza.get('ora'),
            presenza['tipo'],
            presenza.get('motivo', ''),
            1 if presenza.get('giustificato') else 0,
            presenza.get('data_giustifica'),
            presenza.get('docente_registrante', ''),
            presenza.get('note', '')
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def statistiche_presenze(self, classe: Optional[str] = None) -> Dict:
        """Calcola statistiche presenze."""
        cursor = self.conn.cursor()
        
        if classe:
            # Usa JOIN per filtrare per classe
            query = """
                SELECT 
                    COUNT(*) as totale,
                    SUM(CASE WHEN tipo = 'assente' THEN 1 ELSE 0 END) as assenze,
                    SUM(CASE WHEN tipo = 'ritardo' THEN 1 ELSE 0 END) as ritardi,
                    SUM(CASE WHEN giustificato = 1 THEN 1 ELSE 0 END) as giustificate
                FROM presenze p
                JOIN studenti s ON p.id_studente = s.id
                WHERE s.classe = ?
            """
            cursor.execute(query, (classe,))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as totale,
                    SUM(CASE WHEN tipo = 'assente' THEN 1 ELSE 0 END) as assenze,
                    SUM(CASE WHEN tipo = 'ritardo' THEN 1 ELSE 0 END) as ritardi,
                    SUM(CASE WHEN giustificato = 1 THEN 1 ELSE 0 END) as giustificate
                FROM presenze
            """)
        
        row = cursor.fetchone()
        if not row or row['totale'] == 0:
            return {"messaggio": "Nessuna presenza registrata"}
        
        return {
            "totale_registrazioni": row['totale'],
            "assenze": row['assenze'],
            "ritardi": row['ritardi'],
            "giustificate": row['giustificate'],
            "percentuale_assenze": round((row['assenze'] / row['totale']) * 100, 2),
            "percentuale_ritardi": round((row['ritardi'] / row['totale']) * 100, 2),
            "percentuale_giustificazioni": round((row['giustificate'] / row['assenze']) * 100, 2) if row['assenze'] > 0 else 0
        }
    
    # ============ MIGRAZIONE DATI ============
    
    def migra_da_json(self, dati: Dict):
        """Migra dati da formato JSON al database.
        
        Args:
            dati: Dizionario con dati JSON
        """
        print("🔄 Inizio migrazione dati...")
        
        # Migra studenti
        for studente in dati.get('studenti', []):
            try:
                self.aggiungi_studente(studente)
            except Exception as e:
                print(f"⚠️ Errore migrazione studente {studente.get('id')}: {e}")
        
        # Migra voti
        for voto in dati.get('voti', []):
            try:
                self.aggiungi_voto(voto)
            except Exception as e:
                print(f"⚠️ Errore migrazione voto: {e}")
        
        print(" Migrazione completata")
    
    def backup_database(self, backup_path: str = None) -> str:
        """Crea backup del database.
        
        Args:
            backup_path: Percorso backup (default: auto)
            
        Returns:
            Percorso file backup
        """
        if backup_path is None:
            backup_path = f"backup_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        backup_conn = sqlite3.connect(backup_path)
        self.conn.backup(backup_conn)
        backup_conn.close()
        
        print(f" Backup database creato: {backup_path}")
        return backup_path
    
    def statistiche_database(self) -> Dict:
        """Restituisce statistiche sul database."""
        cursor = self.conn.cursor()
        
        stats = {
            "studenti": self.conta_studenti(),
            "voti": cursor.execute("SELECT COUNT(*) FROM voti").fetchone()[0],
            "presenze": cursor.execute("SELECT COUNT(*) FROM presenze").fetchone()[0],
            "classi": len(cursor.execute("SELECT DISTINCT classe FROM studenti").fetchall()),
            "dimensione_db": sum(1 for _ in open(self.db_path, 'rb')) * 1024 if self.db_path else 0
        }
        
        return stats
    
    def __enter__(self):
        """Context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()


if __name__ == "__main__":
    # Test del database
    print("DATABASE MANAGER - TEST")
    print("=" * 60 + "\n")
    
    db = DatabaseManager("test.db")
    
    # Test aggiungi studente
    studente = {
        'id': 1,
        'nome': 'Mario',
        'cognome': 'Rossi',
        'eta': 15,
        'classe': '2A',
        'reddito_familiare': 30000,
        'categoria_reddito': 'MEDIO',
        'condizione_salute': 'BUONA',
        'situazione_familiare': 'Nucleo tradizionale',
        'note': ''
    }
    db.aggiungi_studente(studente)
    print(f"✓ Studente aggiunto")
    
    # Test aggiungi voto
    voto = {
        'id_studente': 1,
        'materia': 'Matematica',
        'voto': 8.0,
        'tipo': 'Interrogazione',
        'data': '2025-10-28',
        'note': 'Ottimo'
    }
    db.aggiungi_voto(voto)
    print(f"✓ Voto aggiunto")
    
    # Test statistiche
    stats = db.statistiche_database()
    print(f"\n Statistiche database:")
    print(f"   Studenti: {stats['studenti']}")
    print(f"   Voti: {stats['voti']}")
    print(f"   Presenze: {stats['presenze']}")
    print(f"   Classi: {stats['classi']}")
    
    db.close()
    print("\n Test completato!")

