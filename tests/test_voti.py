"""
Test per modulo voti.
"""

import pytest
from voti import GestioneVoti, Voto
from anagrafica import Anagrafica


@pytest.fixture
def gestione_voti():
    """Fixture per gestione voti."""
    return GestioneVoti()


@pytest.fixture
def anagrafica():
    """Fixture per anagrafica con studenti."""
    anagrafica = Anagrafica()
    anagrafica.genera_studenti(5)
    return anagrafica


class TestGestioneVoti:
    """Test per classe GestioneVoti."""
    
    @pytest.mark.unit
    def test_creazione(self, gestione_voti):
        """Test creazione gestione voti vuota."""
        assert len(gestione_voti.voti) == 0
    
    @pytest.mark.unit
    def test_aggiungi_voto(self, gestione_voti):
        """Test aggiunta voto."""
        from datetime import date
        
        voto = gestione_voti.aggiungi_voto(
            id_studente=1,
            materia="Matematica",
            voto=8.0,
            tipo="Interrogazione",
            data=date.today().isoformat(),
            note="Ottimo"
        )
        
        assert voto is not None
        assert voto.voto == 8.0
        assert voto.materia == "Matematica"
        assert len(gestione_voti.voti) == 1
    
    @pytest.mark.unit
    def test_voti_studente(self, gestione_voti):
        """Test recupero voti studente."""
        from datetime import date
        today = date.today().isoformat()
        
        # Aggiungi voti per studente 1
        gestione_voti.aggiungi_voto(1, "Matematica", 8.0, "Interrogazione", today)
        gestione_voti.aggiungi_voto(1, "Italiano", 7.5, "Verifica", today)
        gestione_voti.aggiungi_voto(2, "Matematica", 6.0, "Interrogazione", today)
        
        voti_studente1 = gestione_voti.voti_studente(1)
        assert len(voti_studente1) == 2
    
    @pytest.mark.unit
    def test_media_studente(self, gestione_voti):
        """Test calcolo media studente."""
        from datetime import date
        today = date.today().isoformat()
        
        gestione_voti.aggiungi_voto(1, "Matematica", 8.0, "Interrogazione", today)
        gestione_voti.aggiungi_voto(1, "Italiano", 7.0, "Verifica", today)
        gestione_voti.aggiungi_voto(1, "Scienze", 9.0, "Compito", today)
        
        media = gestione_voti.media_studente(1)
        assert media == 8.0  # (8 + 7 + 9) / 3
    
    @pytest.mark.unit
    def test_media_materia(self, gestione_voti):
        """Test calcolo media per materia."""
        from datetime import date
        today = date.today().isoformat()
        
        gestione_voti.aggiungi_voto(1, "Matematica", 8.0, "Interrogazione", today)
        gestione_voti.aggiungi_voto(1, "Matematica", 9.0, "Verifica", today)
        
        # Calcola media manualmente
        voti_materia = [v for v in gestione_voti.voti_studente(1) if v.materia == "Matematica"]
        media = sum(v.voto for v in voti_materia) / len(voti_materia)
        assert media == 8.5
    
    @pytest.mark.unit
    def test_multiple_studenti(self, gestione_voti):
        """Test gestione voti per più studenti."""
        from datetime import date
        today = date.today().isoformat()
        
        gestione_voti.aggiungi_voto(1, "Matematica", 8.0, "Interrogazione", today)
        gestione_voti.aggiungi_voto(2, "Italiano", 7.5, "Verifica", today)
        
        # Verifica voti separati per studente
        voti_1 = gestione_voti.voti_studente(1)
        voti_2 = gestione_voti.voti_studente(2)
        
        assert len(voti_1) == 1
        assert len(voti_2) == 1
        assert voti_1[0].id_studente == 1
        assert voti_2[0].id_studente == 2


class TestVoto:
    """Test per classe Voto."""
    
    @pytest.mark.unit
    def test_creazione_voto(self):
        """Test creazione voto."""
        voto = Voto(
            id_studente=1,
            materia="Matematica",
            voto=8.5,
            tipo="Interrogazione",
            data="2025-10-28",
            note="Ottimo"
        )
        
        assert voto.voto == 8.5
        assert voto.materia == "Matematica"
        assert voto.id_studente == 1
    
    @pytest.mark.unit
    def test_validazione_voto(self):
        """Test validazione range voto."""
        # Voto troppo basso
        with pytest.raises(ValueError):
            Voto(1, "Matematica", 2.0, "Interrogazione", "2025-10-28")
        
        # Voto troppo alto
        with pytest.raises(ValueError):
            Voto(1, "Matematica", 11.0, "Interrogazione", "2025-10-28")
        
        # Voto valido
        voto = Voto(1, "Matematica", 8.0, "Interrogazione", "2025-10-28")
        assert voto.voto == 8.0

