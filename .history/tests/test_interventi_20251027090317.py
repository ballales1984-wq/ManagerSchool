"""
Test per il modulo interventi.py
Verifica simulazione di interventi educativi su studenti fragili.
"""

import unittest
from interventi import SimulatoreInterventi, TipoIntervento, IntensitàIntervento
from anagrafica import Studente, Anagrafica, CategoriaReddito, CondizioneSalute
from voti import GestioneVoti, Voto


class TestInterventi(unittest.TestCase):
    """Test per il simulatore di interventi."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.anagrafica = Anagrafica()
        self.gestione_voti = GestioneVoti()
        self.simulatore = SimulatoreInterventi(self.anagrafica, self.gestione_voti)
        
        # Crea studente test con alta fragilità
        reddito = 20000  # Basso reddito
        self.studente = Studente(
            id=1,
            nome="Mario",
            cognome="Rossi",
            eta=16,
            classe="3A",
            reddito_familiare=reddito,
            categoria_reddito=CategoriaReddito.BASSO,
            condizione_salute=CondizioneSalute.DISCRETA,
            situazione_familiare="Monoparentale"
        )
        self.anagrafica.aggiungi_studente(self.studente)
        
        # Aggiungi alcuni voti
        self.gestione_voti.aggiungi_voto(self.studente.id, "Matematica", 6.0)
        self.gestione_voti.aggiungi_voto(self.studente.id, "Italiano", 6.5)
        self.gestione_voti.aggiungi_voto(self.studente.id, "Storia", 5.5)
    
    def test_simula_intervento_studente(self):
        """Test simulazione intervento su studente singolo."""
        risultato = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.INTERVENTO_COMPLETO,
            IntensitàIntervento.MEDIA
        )
        
        # Verifiche fragilità
        self.assertLess(risultato.fragilita_post, risultato.fragilita_ante)
        self.assertGreater(risultato.miglioramento_fragilita, 0)
        
        # Verifiche voti
        self.assertGreaterEqual(risultato.media_voti_post, risultato.media_voti_ante)
        self.assertGreaterEqual(risultato.miglioramento_voti, 0)
        
        # Verifiche costi
        self.assertGreater(risultato.costo_stimato, 0)
        
        # Verifiche efficacia (0-100)
        self.assertGreaterEqual(risultato.efficacia, 0)
        self.assertLessEqual(risultato.efficacia, 100)
    
    def test_costo_intervento_aumento_reddito(self):
        """Test costo intervento aumento reddito."""
        risultato = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.AUMENTO_REDDITO,
            IntensitàIntervento.ALTA
        )
        
        # Costo atteso per ALTA: €1000
        self.assertEqual(risultato.costo_stimato, 1000.0)
    
    def test_riduzione_fragilita(self):
        """Test che l'intervento riduca effettivamente la fragilità."""
        fragilita_iniziale = self.studente.fragilità_sociale
        
        risultato = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.INTERVENTO_COMPLETO,
            IntensitàIntervento.ALTA
        )
        
        self.assertLess(risultato.fragilita_post, fragilita_iniziale)
        self.assertGreater(risultato.miglioramento_fragilita, 0)
    
    def test_effetto_intensita(self):
        """Test che intensità maggiore produca migliori risultati."""
        risultato_bassa = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.AUMENTO_REDDITO,
            IntensitàIntervento.BASSA
        )
        
        risultato_alta = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.AUMENTO_REDDITO,
            IntensitàIntervento.ALTA
        )
        
        # Alta intensità dovrebbe dare miglior risultato
        self.assertGreater(risultato_alta.miglioramento_fragilita, 
                          risultato_bassa.miglioramento_fragilita)
        self.assertGreater(risultato_alta.costo_stimato, 
                          risultato_bassa.costo_stimato)
    
    def test_intervento_classe(self):
        """Test simulazione intervento su classe."""
        # Aggiungi altri studenti
        for i in range(2, 6):
            studente = self.anagrafica.crea_studente_casuale("3A")
            self.gestione_voti.aggiungi_voto(studente.id, "Matematica", 6.0)
        
        scenario = self.simulatore.simula_intervento_classe(
            "3A",
            TipoIntervento.AUMENTO_REDDITO,
            IntensitàIntervento.MEDIA
        )
        
        # Verifica risultati
        self.assertLess(scenario.fragilita_media_finale, 
                       scenario.fragilita_media_iniziale)
        self.assertGreater(scenario.media_voti_finale, 
                          scenario.media_voti_iniziale)
        self.assertGreater(scenario.costo_totale, 0)
        self.assertGreater(scenario.rapporto_cost_benefit, 0)
    
    def test_confronta_interventi(self):
        """Test confronto interventi."""
        confronto = self.simulatore.confronta_interventi(self.studente)
        
        # Verifica struttura
        self.assertIn("studente", confronto)
        self.assertIn("confronto", confronto)
        self.assertIn("raccomandazione", confronto)
        
        # Verifica che ci siano risultati
        self.assertGreater(len(confronto["confronto"]), 0)
    
    def test_report_prioritari(self):
        """Test report studenti prioritari."""
        # Aggiungi studenti con diversi livelli di fragilità
        for _ in range(10):
            studente = self.anagrafica.crea_studente_casuale()
            self.gestione_voti.aggiungi_voto(studente.id, "Matematica", 6.0)
        
        report = self.simulatore.report_interventi_prioritari(limit=5)
        
        # Verifica struttura
        self.assertIn("totale_fragili", report)
        self.assertIn("studenti_prioritari", report)
        self.assertIn("costo_totale_stimato", report)
        
        # Verifica che abbia studenti
        self.assertGreaterEqual(len(report["studenti_prioritari"]), 0)
    
    def test_efficacia_range(self):
        """Test che efficacia sia sempre nel range 0-100."""
        for tipo in TipoIntervento:
            for intensita in IntensitàIntervento:
                risultato = self.simulatore.simula_intervento_studente(
                    self.studente,
                    tipo,
                    intensita
                )
                self.assertGreaterEqual(risultato.efficacia, 0)
                self.assertLessEqual(risultato.efficacia, 100)
    
    def test_fragilita_non_negativa(self):
        """Test che fragilità post non sia negativa."""
        risultato = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.INTERVENTO_COMPLETO,
            IntensitàIntervento.ALTA
        )
        
        self.assertGreaterEqual(risultato.fragilita_post, 0)
    
    def test_voti_boundary(self):
        """Test che media voti non superi 10."""
        risultato = self.simulatore.simula_intervento_studente(
            self.studente,
            TipoIntervento.INTERVENTO_COMPLETO,
            IntensitàIntervento.ALTA
        )
        
        self.assertLessEqual(risultato.media_voti_post, 10.0)


if __name__ == '__main__':
    unittest.main()

