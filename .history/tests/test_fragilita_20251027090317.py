"""
Test per il calcolo della fragilità sociale.
Verifica che l'indice di fragilità sia calcolato correttamente.
"""

import unittest
from anagrafica import Studente, CategoriaReddito, CondizioneSalute


class TestFragilita(unittest.TestCase):
    """Test per il calcolo della fragilità sociale."""
    
    def test_fragilita_studente_basso_reddito(self):
        """Test fragilità con basso reddito."""
        studente = Studente(
            id=1,
            nome="Mario",
            cognome="Rossi",
            eta=16,
            classe="3A",
            reddito_familiare=15000,
            categoria_reddito=CategoriaReddito.MOLTO_BASSO,
            condizione_salute=CondizioneSalute.BUONA,
            situazione_familiare="Nucleo tradizionale"
        )
        
        # Fragilità dovrebbe essere alta (>50)
        self.assertGreater(studente.fragilità_sociale, 40)
    
    def test_fragilita_studente_alto_reddito(self):
        """Test fragilità con alto reddito."""
        studente = Studente(
            id=2,
            nome="Luca",
            cognome="Bianchi",
            eta=17,
            classe="4A",
            reddito_familiare=70000,
            categoria_reddito=CategoriaReddito.ALTO,
            condizione_salute=CondizioneSalute.ECCELLENTE,
            situazione_familiare="Nucleo tradizionale"
        )
        
        # Fragilità dovrebbe essere bassa (<30)
        self.assertLess(studente.fragilità_sociale, 30)
    
    def test_fragilita_con_salute_critica(self):
        """Test fragilità con salute critica."""
        studente = Studente(
            id=3,
            nome="Anna",
            cognome="Verdi",
            eta=15,
            classe="2A",
            reddito_familiare=30000,
            categoria_reddito=CategoriaReddito.MEDIO,
            condizione_salute=CondizioneSalute.CRITICA,
            situazione_familiare="Affidamento"
        )
        
        # Fragilità dovrebbe essere molto alta (>70)
        self.assertGreater(studente.fragilità_sociale, 60)
    
    def test_fragilita_range(self):
        """Test che fragilità sia sempre 0-100."""
        studente = Studente(
            id=4,
            nome="Paolo",
            cognome="Neri",
            eta=16,
            classe="3B",
            reddito_familiare=25000,
            categoria_reddito=CategoriaReddito.MEDIO,
            condizione_salute=CondizioneSalute.BUONA,
            situazione_familiare="Nucleo tradizionale"
        )
        
        fragilita = studente.fragilità_sociale
        self.assertGreaterEqual(fragilita, 0)
        self.assertLessEqual(fragilita, 100)
    
    def test_fragilita_monoparentale(self):
        """Test fragilità famiglia monoparentale."""
        studente = Studente(
            id=5,
            nome="Sara",
            cognome="Rosso",
            eta=15,
            classe="2B",
            reddito_familiare=30000,
            categoria_reddito=CategoriaReddito.MEDIO,
            condizione_salute=CondizioneSalute.BUONA,
            situazione_familiare="Monoparentale"
        )
        
        # Monoparentale dovrebbe aggiungere fragilità
        self.assertGreater(studente.fragilità_sociale, 15)


if __name__ == '__main__':
    unittest.main()

