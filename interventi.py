"""
Modulo per la simulazione di interventi educativi.
Simula l'effetto di risorse aggiuntive su studenti fragili.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import anagrafica
from anagrafica import Studente, CondizioneSalute


class TipoIntervento(Enum):
    """Tipi di interventi disponibili."""
    AUMENTO_REDDITO = "Aumento Reddito"
    SUPPORTO_FAMILIARE = "Supporto Familiare"
    MIGLIORAMENTO_SALUTE = "Miglioramento Salute"
    INTERVENTO_COMPLETO = "Intervento Completo"


class IntensitàIntervento(Enum):
    """Intensità degli interventi."""
    BASSA = "Bassa"
    MEDIA = "Media"
    ALTA = "Alta"


@dataclass
class RisultatoIntervento:
    """Rappresenta il risultato di un intervento."""
    tipo: TipoIntervento
    intensità: IntensitàIntervento
    fragilita_ante: float
    fragilita_post: float
    miglioramento_fragilita: float
    media_voti_ante: float
    media_voti_post: float
    miglioramento_voti: float
    costo_stimato: float
    efficacia: float  # 0-100
    durata_effetto: str  # Mesi
    

@dataclass
class ScenarioIntervento:
    """Rappresenta uno scenario di intervento completo."""
    descrizione: str
    interventi: List[RisultatoIntervento]
    fragilita_media_iniziale: float
    fragilita_media_finale: float
    media_voti_iniziale: float
    media_voti_finale: float
    costo_totale: float
    rapporto_cost_benefit: float  # Miglioramento punti / Euro speso
    consigliato: bool


class SimulatoreInterventi:
    """Simula l'effetto di interventi educativi su studenti fragili."""
    
    # Costi interventi (Euro mensili)
    COSTI = {
        TipoIntervento.AUMENTO_REDDITO: {
            IntensitàIntervento.BASSA: 200,
            IntensitàIntervento.MEDIA: 500,
            IntensitàIntervento.ALTA: 1000
        },
        TipoIntervento.SUPPORTO_FAMILIARE: {
            IntensitàIntervento.BASSA: 150,
            IntensitàIntervento.MEDIA: 400,
            IntensitàIntervento.ALTA: 800
        },
        TipoIntervento.MIGLIORAMENTO_SALUTE: {
            IntensitàIntervento.BASSA: 100,
            IntensitàIntervento.MEDIA: 300,
            IntensitàIntervento.ALTA: 600
        },
        TipoIntervento.INTERVENTO_COMPLETO: {
            IntensitàIntervento.BASSA: 400,
            IntensitàIntervento.MEDIA: 1000,
            IntensitàIntervento.ALTA: 2000
        }
    }
    
    # Durata effetti (in mesi)
    DURATA_EFFETTI = {
        TipoIntervento.AUMENTO_REDDITO: 6,
        TipoIntervento.SUPPORTO_FAMILIARE: 12,
        TipoIntervento.MIGLIORAMENTO_SALUTE: 6,
        TipoIntervento.INTERVENTO_COMPLETO: 18
    }
    
    def __init__(self, anagrafica, gestione_voti):
        """Inizializza il simulatore.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
    
    def simula_intervento_studente(self, studente: Studente, 
                                   tipo: TipoIntervento, 
                                   intensità: IntensitàIntervento) -> RisultatoIntervento:
        """Simula un intervento su uno studente specifico.
        
        Args:
            studente: Studente su cui applicare l'intervento
            tipo: Tipo di intervento
            intensità: Intensità dell'intervento
            
        Returns:
            RisultatoIntervento con risultati della simulazione
        """
        # Salva stato iniziale
        fragilita_ante = studente.fragilità_sociale
        media_ante = self.gestione_voti.media_studente(studente.id)
        
        # Simula effetto intervento
        fragilita_nuova = self._calcola_nuova_fragilita(studente, tipo, intensità)
        media_nuova = self._calcola_nuova_media(studente, fragilita_ante, fragilita_nuova)
        
        # Calcola miglioramenti
        miglioramento_fragilita = fragilita_ante - fragilita_nuova
        miglioramento_voti = media_nuova - media_ante
        
        # Calcola costo ed efficacia
        costo = self._calcola_costo(tipo, intensità)
        efficacia = self._calcola_efficacia(miglioramento_fragilita, miglioramento_voti)
        
        return RisultatoIntervento(
            tipo=tipo,
            intensità=intensità,
            fragilita_ante=round(fragilita_ante, 1),
            fragilita_post=round(fragilita_nuova, 1),
            miglioramento_fragilita=round(miglioramento_fragilita, 1),
            media_voti_ante=round(media_ante, 2),
            media_voti_post=round(media_nuova, 2),
            miglioramento_voti=round(miglioramento_voti, 2),
            costo_stimato=round(costo, 2),
            efficacia=round(efficacia, 1),
            durata_effetto=f"{self.DURATA_EFFETTI[tipo]} mesi"
        )
    
    def simula_intervento_classe(self, classe: str,
                                 tipo: TipoIntervento,
                                 intensità: IntensitàIntervento) -> ScenarioIntervento:
        """Simula un intervento su tutta una classe.
        
        Args:
            classe: Nome della classe
            tipo: Tipo di intervento
            intensità: Intensità dell'intervento
            
        Returns:
            ScenarioIntervento con risultati completi
        """
        studenti = self.anagrafica.studenti_per_classe(classe)
        
        if not studenti:
            raise ValueError(f"Classe {classe} non trovata")
        
        # Stati iniziali
        fragilita_iniziale = sum(s.fragilità_sociale for s in studenti) / len(studenti)
        medie_iniziali = []
        for s in studenti:
            media = self.gestione_voti.media_studente(s.id)
            if media > 0:
                medie_iniziali.append(media)
        media_iniziale = sum(medie_iniziali) / len(medie_iniziali) if medie_iniziali else 0
        
        # Simula su ogni studente
        risultati = []
        for studente in studenti:
            risultato = self.simula_intervento_studente(studente, tipo, intensità)
            risultati.append(risultato)
        
        # Stati finali
        fragilita_finale = sum(r.fragilita_post for r in risultati) / len(risultati)
        media_finale = media_iniziale + sum(r.miglioramento_voti for r in risultati) / len(risultati)
        
        # Costi e benefici
        costo_totale = sum(r.costo_stimato for r in risultati)
        miglioramento_totale = sum(r.miglioramento_fragilita for r in risultati)
        rapporto_cost_benefit = miglioramento_totale / costo_totale if costo_totale > 0 else 0
        
        # Consiglio
        consigliato = rapporto_cost_benefit > 0.1 and media_finale > media_iniziale
        
        return ScenarioIntervento(
            descrizione=f"Intervento {tipo.value} ({intensità.value}) - Classe {classe}",
            interventi=risultati,
            fragilita_media_iniziale=round(fragilita_iniziale, 1),
            fragilita_media_finale=round(fragilita_finale, 1),
            media_voti_iniziale=round(media_iniziale, 2),
            media_voti_finale=round(media_finale, 2),
            costo_totale=round(costo_totale, 2),
            rapporto_cost_benefit=round(rapporto_cost_benefit, 4),
            consigliato=consigliato
        )
    
    def confronta_interventi(self, studente: Studente) -> Dict:
        """Confronta diversi tipi di interventi per uno studente.
        
        Args:
            studente: Studente da analizzare
            
        Returns:
            Dizionario con confronto interventi
        """
        risultati = {}
        
        for tipo in TipoIntervento:
            for intensità in IntensitàIntervento:
                risultato = self.simula_intervento_studente(studente, tipo, intensità)
                chiave = f"{tipo.value}_{intensità.value}"
                risultati[chiave] = risultato
        
        # Ordina per efficacia
        confronto = sorted(
            risultati.items(),
            key=lambda x: x[1].efficacia,
            reverse=True
        )
        
        return {
            "studente": {
                "nome": studente.nome_completo,
                "fragilita_attuale": studente.fragilità_sociale,
                "media_attuale": self.gestione_voti.media_studente(studente.id)
            },
            "confronto": confronto,
            "miglior_singolo": confronto[0] if confronto else None,
            "raccomandazione": self._genera_raccomandazione(confronto)
        }
    
    def _calcola_nuova_fragilita(self, studente: Studente, 
                                  tipo: TipoIntervento, 
                                  intensità: IntensitàIntervento) -> float:
        """Calcola la nuova fragilità dopo l'intervento."""
        
        # Valori di riduzione fragilità (in punti)
        riduzione = {
            TipoIntervento.AUMENTO_REDDITO: {
                IntensitàIntervento.BASSA: 5,
                IntensitàIntervento.MEDIA: 15,
                IntensitàIntervento.ALTA: 30
            },
            TipoIntervento.SUPPORTO_FAMILIARE: {
                IntensitàIntervento.BASSA: 3,
                IntensitàIntervento.MEDIA: 10,
                IntensitàIntervento.ALTA: 20
            },
            TipoIntervento.MIGLIORAMENTO_SALUTE: {
                IntensitàIntervento.BASSA: 4,
                IntensitàIntervento.MEDIA: 12,
                IntensitàIntervento.ALTA: 25
            },
            TipoIntervento.INTERVENTO_COMPLETO: {
                IntensitàIntervento.BASSA: 12,
                IntensitàIntervento.MEDIA: 35,
                IntensitàIntervento.ALTA: 60
            }
        }
        
        riduzione_valore = riduzione[tipo][intensità]
        nuova_fragilita = max(0, studente.fragilità_sociale - riduzione_valore)
        
        return nuova_fragilita
    
    def _calcola_nuova_media(self, studente: Studente, 
                            fragilita_ante: float, 
                            fragilita_post: float) -> float:
        """Calcola la nuova media voti dopo l'intervento."""
        
        media_ante = self.gestione_voti.media_studente(studente.id)
        
        # Miglioramento basato su riduzione fragilità
        riduzione_fragilita = fragilita_ante - fragilita_post
        
        # Formula: ogni 10 punti di fragilità = 0.5 punti di voto
        miglioramento_voti = (riduzione_fragilita / 10) * 0.5
        
        # Limita miglioramento realistico
        nuova_media = min(10, media_ante + miglioramento_voti)
        
        return nuova_media
    
    def _calcola_costo(self, tipo: TipoIntervento, intensità: IntensitàIntervento) -> float:
        """Calcola il costo dell'intervento."""
        return self.COSTI[tipo][intensità]
    
    def _calcola_efficacia(self, miglioramento_fragilita: float, 
                          miglioramento_voti: float) -> float:
        """Calcola l'efficacia complessiva dell'intervento (0-100)."""
        
        # Normalizza (considera max 50 punti di fragilità e 2 punti di voto)
        efficacia_fragilita = min(50, (miglioramento_fragilita / 50) * 100)
        efficacia_voti = min(50, (miglioramento_voti / 2) * 100)
        
        efficacia_totale = (efficacia_fragilita + efficacia_voti) / 2
        
        return max(0, min(100, efficacia_totale))
    
    def _genera_raccomandazione(self, confronto: List) -> str:
        """Genera una raccomandazione basata sul confronto."""
        
        if not confronto:
            return "Nessun intervento disponibile"
        
        # Trova migliore rapporto costo/beneficio
        migliore = min(confronto, key=lambda x: x[1].costo_stimato / (x[1].efficacia + 1))
        
        if migliore[1].efficacia < 20:
            return "Interventi di impatto limitato suggeriti"
        
        return f"Raccomandato: {migliore[1].tipo.value} ({migliore[1].intensità.value})"
    
    def report_interventi_prioritari(self, limit: int = 10) -> Dict:
        """Genera un report sugli studenti che beneficierebbero di più dagli interventi.
        
        Args:
            limit: Numero massimo di studenti da includere
            
        Returns:
            Dizionario con report studenti prioritari
        """
        studenti_fragili = self.anagrafica.studenti_per_fragilita(min_fragilita=50)
        
        risultati = []
        for studente in studenti_fragili:
            # Simula intervento completo media
            risultato = self.simula_intervento_studente(
                studente,
                TipoIntervento.INTERVENTO_COMPLETO,
                IntensitàIntervento.MEDIA
            )
            
            risultati.append({
                "studente": studente.to_dict(),
                "intervento": risultato,
                "priorità": studente.fragilità_sociale + risultato.efficacia
            })
        
        # Ordina per priorità
        risultati.sort(key=lambda x: x["priorità"], reverse=True)
        
        return {
            "totale_fragili": len(studenti_fragili),
            "studenti_prioritari": risultati[:limit],
            "costo_totale_stimato": sum(r["intervento"].costo_stimato for r in risultati[:limit]),
            "miglioramento_atteso": sum(r["intervento"].miglioramento_fragilita for r in risultati[:limit])
        }

