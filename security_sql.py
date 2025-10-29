"""
Sistema di sicurezza SQL - prevenzione SQL injection.
"""

from typing import Any, Dict, List, Optional, Tuple
import sqlite3


class SecureDatabaseManager:
    """Database manager con query parametrizzate."""
    
    def __init__(self, db_path: str):
        """Inizializza database sicuro.
        
        Args:
            db_path: Percorso database
        """
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connette al database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def execute_safe(self, query: str, params: Tuple = ()) -> sqlite3.Cursor:
        """Esegue query SQL sicura con parametri.
        
        Args:
            query: Query SQL con placeholder ?
            params: Parametri da sostituire
            
        Returns:
            Cursor risultato
        """
        if self.conn is None:
            self.connect()
        
        return self.conn.execute(query, params)
    
    def execute_many_safe(self, query: str, params: List[Tuple]) -> sqlite3.Cursor:
        """Esegue query multiple sicure.
        
        Args:
            query: Query SQL con placeholder ?
            params: Lista parametri
            
        Returns:
            Cursor risultato
        """
        if self.conn is None:
            self.connect()
        
        return self.conn.executemany(query, params)
    
    def aggiungi_studente_safe(self, studente: Dict) -> int:
        """Aggiunge studente con query sicura.
        
        Args:
            studente: Dati studente
            
        Returns:
            ID studente inserito
        """
        query = """
        INSERT INTO studenti 
        (id, nome, cognome, eta, classe, reddito_familiare, categoria_reddito, 
         condizione_salute, situazione_familiare, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            studente.get('id'),
            studente.get('nome'),
            studente.get('cognome'),
            studente.get('eta'),
            studente.get('classe'),
            studente.get('reddito_familiare'),
            studente.get('categoria_reddito'),
            studente.get('condizione_salute'),
            studente.get('situazione_familiare'),
            studente.get('note', '')
        )
        
        cursor = self.execute_safe(query, params)
        self.conn.commit()
        return cursor.lastrowid
    
    def cerca_studente_safe(self, nome: str, classe: Optional[str] = None) -> List[Dict]:
        """Cerca studenti con query sicura.
        
        Args:
            nome: Nome da cercare
            classe: Classe opzionale
            
        Returns:
            Lista studenti trovati
        """
        if classe:
            query = "SELECT * FROM studenti WHERE nome LIKE ? AND classe = ?"
            params = (f'%{nome}%', classe)
        else:
            query = "SELECT * FROM studenti WHERE nome LIKE ?"
            params = (f'%{nome}%',)
        
        cursor = self.execute_safe(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def lista_studenti_classe_safe(self, classe: str) -> List[Dict]:
        """Lista studenti di una classe con query sicura.
        
        Args:
            classe: Classe da filtrare
            
        Returns:
            Lista studenti
        """
        query = "SELECT * FROM studenti WHERE classe = ? ORDER BY cognome, nome"
        cursor = self.execute_safe(query, (classe,))
        return [dict(row) for row in cursor.fetchall()]
    
    def statistiche_classe_safe(self, classe: str) -> Dict:
        """Statistiche classe con query sicura.
        
        Args:
            classe: Classe
            
        Returns:
            Statistiche
        """
        # Numero studenti
        query_count = "SELECT COUNT(*) as totale FROM studenti WHERE classe = ?"
        cursor = self.execute_safe(query_count, (classe,))
        totale = cursor.fetchone()['totale']
        
        # Range età
        query_eta = "SELECT MIN(eta) as min_eta, MAX(eta) as max_eta FROM studenti WHERE classe = ?"
        cursor = self.execute_safe(query_eta, (classe,))
        eta_data = cursor.fetchone()
        
        return {
            'classe': classe,
            'totale_studenti': totale,
            'eta_min': eta_data['min_eta'],
            'eta_max': eta_data['max_eta']
        }
    
    def close(self):
        """Chiude connessione database."""
        if self.conn:
            self.conn.close()


class SQLInjectionPrevention:
    """Utilities per prevenire SQL injection."""
    
    @staticmethod
    def sanitize_input(input_str: str, max_length: int = 255) -> str:
        """Pulisce input utente.
        
        Args:
            input_str: Stringa da pulire
            max_length: Lunghezza massima
            
        Returns:
            Stringa pulita
        """
        # Rimuovi caratteri pericolosi
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
        
        cleaned = input_str
        for char in dangerous_chars:
            cleaned = cleaned.replace(char, "")
        
        # Limita lunghezza
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
        
        return cleaned
    
    @staticmethod
    def valida_parametri(*params):
        """Valida parametri per query.
        
        Args:
            params: Parametri da validare
            
        Returns:
            True se validi
        """
        for param in params:
            # Non permettere None se non esplicitamente consentito
            if param is None:
                continue
            
            # Converti a string per controllo
            param_str = str(param)
            
            # Controlla SQL injection patterns
            dangerous_patterns = [
                "SELECT", "INSERT", "UPDATE", "DELETE",
                "DROP", "CREATE", "ALTER", "EXEC",
                "UNION", "--", "/*", "*/"
            ]
            
            param_upper = param_str.upper()
            for pattern in dangerous_patterns:
                if pattern in param_upper:
                    raise ValueError(f"Parametro contiene pattern pericoloso: {pattern}")
        
        return True


if __name__ == "__main__":
    print("SISTEMA SICUREZZA SQL - TEST")
    print("=" * 60 + "\n")
    
    # Test sanitizzazione
    test_inputs = [
        "Mario Rossi",
        "O'Brien",
        "DROP TABLE studenti; --",
        "Robert'); DROP TABLE studenti; --",
        "Normal input 123"
    ]
    
    print("Test sanitizzazione input:")
    for inp in test_inputs:
        cleaned = SQLInjectionPrevention.sanitize_input(inp)
        print(f"  Input:   {inp}")
        print(f"  Pulito:  {cleaned}")
        print()
    
    # Test validazione
    print("Test validazione parametri:")
    try:
        SQLInjectionPrevention.valida_parametri("Mario", "Rossi", "2A")
        print("  ✓ Parametri validi")
    except ValueError as e:
        print(f"  ✗ {e}")
    
    try:
        SQLInjectionPrevention.valida_parametri("Mario'; DROP TABLE studenti; --", "Rossi")
        print("  ✗ Non dovrebbe essere valido")
    except ValueError as e:
        print(f"  ✓ SQL injection bloccato: {e}")

