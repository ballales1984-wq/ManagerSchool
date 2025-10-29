"""
Test per database SQLite.
"""

import pytest
import os
from database_manager import DatabaseManager
from anagrafica import Anagrafica
from voti import GestioneVoti


@pytest.fixture
def db():
    """Fixture per database di test."""
    db_path = "test_manager.db"
    db = DatabaseManager(db_path)
    
    # Cleanup dopo test
    yield db
    
    db.close()
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def studente_test():
    """Fixture per studente di test."""
    return {
        'id': 1,
        'nome': 'Mario',
        'cognome': 'Rossi',
        'eta': 15,
        'classe': '2A',
        'reddito_familiare': 35000,
        'categoria_reddito': 'MEDIO',
        'condizione_salute': 'BUONA',
        'situazione_familiare': 'Nucleo tradizionale',
        'note': ''
    }


class TestDatabaseManager:
    """Test per DatabaseManager."""
    
    @pytest.mark.database
    def test_inizializzazione(self, db):
        """Test inizializzazione database."""
        assert db is not None
        assert db.conn is not None
    
    @pytest.mark.database
    def test_aggiungi_studente(self, db, studente_test):
        """Test aggiunta studente al database."""
        db.aggiungi_studente(studente_test)
        
        # Verifica che lo studente sia stato aggiunto
        studenti = db.ottieni_studenti()
        assert len(studenti) == 1
        assert studenti[0]['nome'] == 'Mario'
    
    @pytest.mark.database
    def test_aggiungi_voto(self, db, studente_test):
        """Test aggiunta voto al database."""
        db.aggiungi_studente(studente_test)
        
        voto_test = {
            'id_studente': 1,
            'materia': 'Matematica',
            'voto': 8.0,
            'tipo': 'Interrogazione',
            'data': '2025-10-28',
            'note': 'Ottimo'
        }
        
        db.aggiungi_voto(voto_test)
        
        # Verifica che il voto sia stato aggiunto
        voti = db.ottieni_voti_studente(1)
        assert len(voti) == 1
        assert voti[0]['materia'] == 'Matematica'
    
    @pytest.mark.database
    def test_media_studente(self, db, studente_test):
        """Test calcolo media studente dal database."""
        db.aggiungi_studente(studente_test)
        
        db.aggiungi_voto({
            'id_studente': 1,
            'materia': 'Matematica',
            'voto': 8.0,
            'tipo': 'Interrogazione',
            'data': '2025-10-28'
        })
        
        db.aggiungi_voto({
            'id_studente': 1,
            'materia': 'Matematica',
            'voto': 9.0,
            'tipo': 'Verifica',
            'data': '2025-10-29'
        })
        
        media = db.media_studente(1)
        assert media == 8.5
    
    @pytest.mark.database
    def test_statistiche_database(self, db):
        """Test generazione statistiche database."""
        stats = db.statistiche_database()
        
        assert 'studenti' in stats
        assert 'voti' in stats
        assert 'presenze' in stats
        assert 'classi' in stats
    
    @pytest.mark.database
    def test_backup_database(self, db, studente_test):
        """Test backup database."""
        db.aggiungi_studente(studente_test)
        
        backup_path = db.backup_database()
        
        assert os.path.exists(backup_path)
        assert backup_path.endswith('.db')
    
    @pytest.mark.database
    def test_query_per_classe(self, db):
        """Test query studenti per classe."""
        # Aggiungi studenti di classi diverse
        for i, classe in enumerate(['2A', '2A', '3B'], 1):
            db.aggiungi_studente({
                'id': i,
                'nome': f'Nome{i}',
                'cognome': f'Cognome{i}',
                'eta': 15,
                'classe': classe,
                'reddito_familiare': 30000,
                'categoria_reddito': 'MEDIO',
                'condizione_salute': 'BUONA',
                'situazione_familiare': 'Tradizionale',
                'note': ''
            })
        
        studenti_2a = db.ottieni_studenti("2A")
        assert len(studenti_2a) == 2
        
        studenti_3b = db.ottieni_studenti("3B")
        assert len(studenti_3b) == 1

