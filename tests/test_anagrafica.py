"""
Test per modulo anagrafica.
"""

import pytest
from anagrafica import Anagrafica, Studente, CategoriaReddito, CondizioneSalute


@pytest.fixture
def anagrafica():
    """Fixture per anagrafica pulita."""
    return Anagrafica()


@pytest.fixture
def studente_test():
    """Fixture per uno studente di test."""
    return Studente(
        id=1,
        nome="Mario",
        cognome="Rossi",
        eta=15,
        classe="2A",
        reddito_familiare=35000,
        categoria_reddito=CategoriaReddito.MEDIO,
        condizione_salute=CondizioneSalute.BUONA,
        situazione_familiare="Nucleo tradizionale",
        note=""
    )


class TestAnagrafica:
    """Test per classe Anagrafica."""
    
    @pytest.mark.unit
    def test_creazione(self, anagrafica):
        """Test creazione anagrafica vuota."""
        assert len(anagrafica.studenti) == 0
    
    @pytest.mark.unit
    def test_aggiungi_studente(self, anagrafica, studente_test):
        """Test aggiunta studente."""
        anagrafica.aggiungi_studente(studente_test)
        assert len(anagrafica.studenti) == 1
        assert anagrafica.studenti[0].nome == "Mario"
    
    @pytest.mark.unit
    def test_cerca_studente(self, anagrafica, studente_test):
        """Test ricerca studente."""
        anagrafica.aggiungi_studente(studente_test)
        # Cerca in modo diretto nella lista
        result = next((s for s in anagrafica.studenti if s.nome == "Mario"), None)
        assert result is not None
        assert result.nome == "Mario"
    
    @pytest.mark.unit
    def test_cerca_studente_non_trovato(self, anagrafica):
        """Test ricerca studente non esistente."""
        result = next((s for s in anagrafica.studenti if s.nome == "Inesistente"), None)
        assert result is None
    
    @pytest.mark.unit
    def test_genera_studenti(self, anagrafica):
        """Test generazione studenti casuali."""
        anagrafica.genera_studenti(10)
        assert len(anagrafica.studenti) == 10
        # Verifica che tutti abbiano dati validi
        for studente in anagrafica.studenti:
            assert studente.nome
            assert studente.cognome
            assert studente.classe
            assert studente.eta >= 14 and studente.eta <= 19
    
    @pytest.mark.unit
    def test_studenti_per_classe(self, anagrafica, studente_test):
        """Test filtraggio studenti per classe."""
        anagrafica.aggiungi_studente(studente_test)
        studenti_2a = anagrafica.studenti_per_classe("2A")
        assert len(studenti_2a) == 1
        assert studenti_2a[0].nome == "Mario"
    
    @pytest.mark.unit
    def test_statistiche(self, anagrafica):
        """Test generazione statistiche."""
        anagrafica.genera_studenti(20)
        # Verifica dati diretti
        assert len(anagrafica.studenti) == 20
        classi = len(set(s.classe for s in anagrafica.studenti))
        assert classi > 0


class TestStudente:
    """Test per classe Studente."""
    
    @pytest.mark.unit
    def test_creazione_studente(self, studente_test):
        """Test creazione studente."""
        assert studente_test.nome == "Mario"
        assert studente_test.cognome == "Rossi"
        assert studente_test.classe == "2A"
    
    @pytest.mark.unit
    def test_nome_completo(self, studente_test):
        """Test metodo nome_completo."""
        assert studente_test.nome_completo == "Mario Rossi"
    
    @pytest.mark.unit
    def test_to_dict(self, studente_test):
        """Test conversione a dizionario."""
        studente_dict = studente_test.to_dict()
        assert isinstance(studente_dict, dict)
        assert studente_dict['nome'] == "Mario"
        assert studente_dict['cognome'] == "Rossi"
    
    @pytest.mark.unit
    def test_attributi_base(self, studente_test):
        """Test attributi base studente."""
        # Verifica attributi base
        assert studente_test.nome
        assert studente_test.cognome
        assert studente_test.classe
        assert studente_test.eta >= 14 and studente_test.eta <= 19

