"""
Test di integrazione tra i diversi moduli.
Verifica che i moduli funzionino insieme correttamente.
"""

import unittest
from anagrafica import Anagrafica
from insegnanti import GestioneInsegnanti, Insegnante
from voti import GestioneVoti
from analisi import AnalisiDidattica
from interventi import SimulatoreInterventi, TipoIntervento, IntensitàIntervento
from indicatori import CalcolatoreIndicatori
from accesso import GestoreAccessi, Ruolo


class TestIntegrazione(unittest.TestCase):
    """Test di integrazione tra moduli."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.anagrafica = Anagrafica()
        self.gestione_voti = GestioneVoti()
        self.insegnanti = GestioneInsegnanti()
        
        # Crea dati di test
        self._popola_dati()
    
    def _popola_dati(self):
        """Popola il sistema con dati di test."""
        # Aggiungi studenti
        for i in range(5):
            studente = self.anagrafica.crea_studente_casuale("3A")
            
            # Aggiungi voti
            self.gestione_voti.aggiungi_voto(studente.id, "Matematica", 7.0 + i*0.5)
            self.gestione_voti.aggiungi_voto(studente.id, "Italiano", 6.5)
        
        # Aggiungi insegnanti
        insegnante = Insegnante(
            id=1,
            nome="Mario",
            cognome="Bianchi",
            materia="Matematica",
            anni_esperienza=10
        )
        self.insegnanti.aggiungi_insegnante(insegnante)
    
    def test_integrazione_anagrafica_voti(self):
        """Test integrazione tra anagrafica e voti."""
        studente = self.anagrafica.studenti[0]
        
        # Aggiungi voto
        self.gestione_voti.aggiungi_voto(studente.id, "Storia", 8.0)
        
        # Verifica media
        media = self.gestione_voti.media_studente(studente.id)
        self.assertGreater(media, 0)
    
    def test_analisi_didattica_integrata(self):
        """Test analisi didattica con anagrafica e voti."""
        analisi = AnalisiDidattica(self.anagrafica, self.gestione_voti)
        
        # Test graduatoria studenti
        graduatoria = analisi.graduatoria_studenti()
        self.assertGreater(len(graduatoria), 0)
        
        # Test impatto fragili
        impatto = analisi.impatto_didattico_fragili()
        self.assertIn("gap_pedagogico", impatto)
    
    def test_interventi_integrazione(self):
        """Test integrazione simulatore interventi."""
        simulatore = SimulatoreInterventi(self.anagrafica, self.gestione_voti)
        
        studente = self.anagrafica.studenti[0]
        
        # Simula intervento
        risultato = simulatore.simula_intervento_studente(
            studente,
            TipoIntervento.AUMENTO_REDDITO,
            IntensitàIntervento.MEDIA
        )
        
        # Verifica risultati
        self.assertIsNotNone(risultato)
        self.assertGreater(risultato.efficacia, 0)
    
    def test_indicatori_integrazione(self):
        """Test integrazione calcolo indicatori."""
        analisi = AnalisiDidattica(self.anagrafica, self.gestione_voti)
        
        calcolatore = CalcolatoreIndicatori(
            self.anagrafica,
            self.gestione_voti,
            self.insegnanti,
            analisi
        )
        
        # Calcola indicatore
        indice = calcolatore.indice_qualita_scolastica()
        
        # Verifica struttura
        self.assertIn("Indice Qualità Scolastica", indice.nome)
        self.assertGreaterEqual(indice.valore, 0)
        self.assertLessEqual(indice.valore, 100)
    
    def test_accesso_rbac(self):
        """Test sistema di accesso con ruoli."""
        gestore = GestoreAccessi()
        
        # Registra utente
        successo = gestore.registra_utente(
            "test",
            "password",
            Ruolo.INSEGNANTE,
            "Test User"
        )
        
        self.assertTrue(successo)
        
        # Autentica
        autenticato = gestore.autentica("test", "password")
        self.assertTrue(autenticato)
        
        # Verifica permessi
        ha_permesso = gestore.verifica_permesso("gestione_voti")
        self.assertTrue(ha_permesso)
    
    def test_sistema_completo(self):
        """Test del sistema completo end-to-end."""
        # Crea sistema completo
        analisi = AnalisiDidattica(self.anagrafica, self.gestione_voti)
        calcolatore = CalcolatoreIndicatori(
            self.anagrafica,
            self.gestione_voti,
            self.insegnanti,
            analisi
        )
        
        # Calcola tutti gli indicatori
        quadro = calcolatore.quadro_indicatori_completo()
        
        # Verifica struttura
        self.assertIn("qualita_scolastica", quadro)
        self.assertIn("equita_educativa", quadro)
        self.assertIn("efficacia_didattica", quadro)
        
        # Calcola sintesi
        sintesi = calcolatore.sintesi_indicatori()
        self.assertIn("media_generale", sintesi)
        self.assertIn("valutazione", sintesi)
        self.assertIn("raccomandazioni", sintesi)


if __name__ == '__main__':
    unittest.main()

