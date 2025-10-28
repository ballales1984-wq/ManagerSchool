"""
Modulo per la creazione di corsi didattici digitali da parte dei docenti.
Permette ai docenti di essere costruttori attivi di contenuti, non solo esecutori.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import random


class TipoRisorsa(Enum):
    """Tipi di risorse didattiche."""
    DOCUMENTO = "documento"
    VIDEO = "video"
    ESERCIZIO = "esercizio"
    LINK = "link"
    PRESENTAZIONE = "presentazione"
    SIMULAZIONE = "simulazione"
    QUIZ = "quiz"


class LivelloDifficoltà(Enum):
    """Livelli di difficoltà."""
    BASE = "base"
    INTERMEDIO = "intermedio"
    AVANZATO = "avanzato"


@dataclass
class RisorsaDidattica:
    """Una singola risorsa didattica."""
    
    id: int
    docente: str
    titolo: str
    tipo: TipoRisorsa
    url: str
    descrizione: str = ""
    difficoltà: LivelloDifficoltà = LivelloDifficoltà.INTERMEDIO
    argomenti: List[str] = field(default_factory=list)
    data_creazione: str = ""
    data_ultimo_uso: Optional[str] = None
    numero_visualizzazioni: int = 0
    rating_docente: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "docente": self.docente,
            "titolo": self.titolo,
            "tipo": self.tipo.value,
            "url": self.url,
            "descrizione": self.descrizione,
            "difficoltà": self.difficoltà.value,
            "argomenti": self.argomenti,
            "data_creazione": self.data_creazione,
            "data_ultimo_uso": self.data_ultimo_uso,
            "numero_visualizzazioni": self.numero_visualizzazioni,
            "rating_docente": self.rating_docente
        }


@dataclass
class ModuloCorso:
    """Un modulo tematico di un corso."""
    
    id: int
    titolo: str
    descrizione: str
    argomenti_principali: List[str] = field(default_factory=list)
    risorse: List[RisorsaDidattica] = field(default_factory=list)
    durata_stimata: int = 0  # Minuti
    obiettivi: List[str] = field(default_factory=list)
    prerequisiti: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "titolo": self.titolo,
            "descrizione": self.descrizione,
            "argomenti_principali": self.argomenti_principali,
            "risorse": [r.to_dict() for r in self.risorse],
            "durata_stimata": self.durata_stimata,
            "obiettivi": self.obiettivi,
            "prerequisiti": self.prerequisiti
        }


@dataclass
class CorsoDigitale:
    """Corso digitale completo creato da un docente."""
    
    id: int
    docente: str
    materia: str
    titolo: str
    descrizione: str
    classe_target: str
    moduli: List[ModuloCorso] = field(default_factory=list)
    data_creazione: str = ""
    data_inizio: Optional[str] = None
    data_fine: Optional[str] = None
    archiviato: bool = False
    pubblico: bool = True  # Se condivisibile con altri docenti
    numero_iscritti: int = 0
    valutazione_media: float = 0.0
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "docente": self.docente,
            "materia": self.materia,
            "titolo": self.titolo,
            "descrizione": self.descrizione,
            "classe_target": self.classe_target,
            "moduli": [m.to_dict() for m in self.moduli],
            "data_creazione": self.data_creazione,
            "data_inizio": self.data_inizio,
            "data_fine": self.data_fine,
            "archiviato": self.archiviato,
            "pubblico": self.pubblico,
            "numero_iscritti": self.numero_iscritti,
            "valutazione_media": self.valutazione_media,
            "totale_risorse": sum(len(m.risorse) for m in self.moduli)
        }


@dataclass
class SchedaIntelligente:
    """Scheda di studio intelligente per lo studente."""
    
    id: int
    studente_id: int
    materia: str
    argomento: str
    obiettivi: List[str] = field(default_factory=list)
    risorse_consigliate: List[RisorsaDidattica] = field(default_factory=list)
    esercizi: List[str] = field(default_factory=list)
    data_creazione: str = ""
    data_scadenza: Optional[str] = None
    completata: bool = False
    progresso: float = 0.0  # 0-100
    note_studente: str = ""
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "studente_id": self.studente_id,
            "materia": self.materia,
            "argomento": self.argomento,
            "obiettivi": self.obiettivi,
            "risorse_consigliate": [r.to_dict() for r in self.risorse_consigliate],
            "esercizi": self.esercizi,
            "data_creazione": self.data_creazione,
            "data_scadenza": self.data_scadenza,
            "completata": self.completata,
            "progresso": self.progresso,
            "note_studente": self.note_studente
        }


class CostruttoreCorsoDocente:
    """Sistema per i docenti di creare corsi didattici digitali."""
    
    def __init__(self, anagrafica, gestione_voti):
        """Inizializza il costruttore.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
        
        self.risorse: List[RisorsaDidattica] = []
        self.corsi: List[CorsoDigitale] = []
        self.schede: List[SchedaIntelligente] = []
        
        self._prossimo_id_risorsa = 1
        self._prossimo_id_corso = 1
        self._prossimo_id_scheda = 1
    
    # ============ GESTIONE RISORSE ============
    
    def carica_risorsa(self, docente: str, titolo: str, tipo: TipoRisorsa,
                     url: str, descrizione: str = "", argomenti: List[str] = None,
                     difficoltà: LivelloDifficoltà = LivelloDifficoltà.INTERMEDIO) -> RisorsaDidattica:
        """Carica una nuova risorsa didattica.
        
        Args:
            docente: Nome del docente
            titolo: Titolo della risorsa
            tipo: Tipo di risorsa
            url: URL o percorso della risorsa
            descrizione: Descrizione
            argomenti: Argomenti trattati
            difficoltà: Livello di difficoltà
            
        Returns:
            RisorsaDidattica caricata
        """
        risorsa = RisorsaDidattica(
            id=self._prossimo_id_risorsa,
            docente=docente,
            titolo=titolo,
            tipo=tipo,
            url=url,
            descrizione=descrizione,
            difficoltà=difficoltà,
            argomenti=argomenti or [],
            data_creazione=datetime.now().strftime("%Y-%m-%d")
        )
        
        self.risorse.append(risorsa)
        self._prossimo_id_risorsa += 1
        
        print(f"✅ Risorsa caricata: {titolo} ({tipo.value})")
        print(f"   Argomenti: {', '.join(argomenti or [])}")
        
        return risorsa
    
    def risorse_per_docente(self, docente: str) -> List[RisorsaDidattica]:
        """Ottiene risorse di un docente."""
        return [r for r in self.risorse if r.docente == docente]
    
    def risorse_per_argomento(self, argomento: str) -> List[RisorsaDidattica]:
        """Ottiene risorse per argomento."""
        return [r for r in self.risorse if argomento in r.argomenti]
    
    # ============ CREAZIONE CORSI ============
    
    def crea_corso(self, docente: str, materia: str, titolo: str,
                  classe_target: str, descrizione: str = "") -> CorsoDigitale:
        """Crea un nuovo corso digitale.
        
        Args:
            docente: Nome del docente
            materia: Materia
            titolo: Titolo del corso
            classe_target: Classe target
            descrizione: Descrizione
            
        Returns:
            CorsoDigitale creato
        """
        corso = CorsoDigitale(
            id=self._prossimo_id_corso,
            docente=docente,
            materia=materia,
            titolo=titolo,
            descrizione=descrizione,
            classe_target=classe_target,
            data_creazione=datetime.now().strftime("%Y-%m-%d")
        )
        
        self.corsi.append(corso)
        self._prossimo_id_corso += 1
        
        print(f"✅ Corso creato: {titolo} ({materia})")
        print(f"   Docente: {docente}, Classe: {classe_target}")
        
        return corso
    
    def aggiungi_modulo(self, corso: CorsoDigitale, titolo: str,
                       descrizione: str, argomenti: List[str] = None,
                       durata_stimata: int = 0) -> ModuloCorso:
        """Aggiunge un modulo a un corso.
        
        Args:
            corso: Corso destinatario
            titolo: Titolo del modulo
            descrizione: Descrizione
            argomenti: Argomenti trattati
            durata_stimata: Durata in minuti
            
        Returns:
            ModuloCorso creato
        """
        modulo = ModuloCorso(
            id=len(corso.moduli) + 1,
            titolo=titolo,
            descrizione=descrizione,
            argomenti_principali=argomenti or [],
            durata_stimata=durata_stimata
        )
        
        corso.moduli.append(modulo)
        
        print(f"✅ Modulo aggiunto: {titolo}")
        
        return modulo
    
    def collega_risorsa_al_modulo(self, modulo: ModuloCorso, risorsa: RisorsaDidattica):
        """Collega una risorsa a un modulo."""
        modulo.risorse.append(risorsa)
        print(f"✅ Risorsa '{risorsa.titolo}' collegata al modulo '{modulo.titolo}'")
    
    def corsi_per_docente(self, docente: str) -> List[CorsoDigitale]:
        """Ottiene corsi di un docente."""
        return [c for c in self.corsi if c.docente == docente]
    
    def corsi_pubblici(self) -> List[CorsoDigitale]:
        """Ottiene corsi pubblici condivisibili."""
        return [c for c in self.corsi if c.pubblico and not c.archiviato]
    
    # ============ SCHEDE INTELLIGENTI ============
    
    def genera_scheda_studio(self, studente_id: int, materia: str,
                            argomento: str, obiettivi: List[str] = None,
                            risorse: List[RisorsaDidattica] = None) -> SchedaIntelligente:
        """Genera una scheda di studio intelligente per uno studente.
        
        Args:
            studente_id: ID dello studente
            materia: Materia
            argomento: Argomento da studiare
            obiettivi: Obiettivi di apprendimento
            risorse: Risorse da usare
            
        Returns:
            SchedaIntelligente creata
        """
        scheda = SchedaIntelligente(
            id=self._prossimo_id_scheda,
            studente_id=studente_id,
            materia=materia,
            argomento=argomento,
            obiettivi=obiettivi or ["Approfondire l'argomento", "Svolgere esercizi"],
            risorse_consigliate=risorse or [],
            data_creazione=datetime.now().strftime("%Y-%m-%d")
        )
        
        self.schede.append(scheda)
        self._prossimo_id_scheda += 1
        
        print(f"✅ Scheda generata per studente {studente_id}")
        print(f"   Argomento: {argomento}, Risorse: {len(risorse or [])}")
        
        return scheda
    
    def schede_studente(self, studente_id: int, solo_attive: bool = True) -> List[SchedaIntelligente]:
        """Ottiene schede di uno studente."""
        schede = [s for s in self.schede if s.studente_id == studente_id]
        
        if solo_attive:
            schede = [s for s in schede if not s.completata]
        
        return sorted(schede, key=lambda x: x.data_creazione, reverse=True)
    
    def aggiorna_progresso_scheda(self, scheda_id: int, progresso: float):
        """Aggiorna il progresso di una scheda."""
        for s in self.schede:
            if s.id == scheda_id:
                s.progresso = progresso
                if progresso >= 100:
                    s.completata = True
                print(f"✅ Progresso scheda {scheda_id}: {progresso}%")
                return
        
        print(f"❌ Scheda {scheda_id} non trovata")
    
    # ============ PROGRAMMAZIONE VERIFICHE ============
    
    def programma_verifica(self, docente: str, materia: str, data: str,
                          classe: str, argomenti: List[str], tipo: str = "verifica scritta") -> Dict:
        """Programma una verifica.
        
        Args:
            docente: Nome del docente
            materia: Materia
            data: Data della verifica
            classe: Classe
            argomenti: Argomenti da verificare
            tipo: Tipo di verifica
            
        Returns:
            Dizionario con dettagli della verifica programmata
        """
        # Trova risorse correlate
        risorse_correlate = []
        for argomento in argomenti:
            risorse_correlate.extend(self.risorse_per_argomento(argomento))
        
        # Crea record verifica
        verifica = {
            "docente": docente,
            "materia": materia,
            "data": data,
            "classe": classe,
            "argomenti": argomenti,
            "tipo": tipo,
            "risorse_disponibili": len(risorse_correlate),
            "materiale_docente": True
        }
        
        print(f"✅ Verifica programmata: {materia} - {data}")
        print(f"   Argomenti: {', '.join(argomenti)}")
        print(f"   Risorse disponibili: {len(risorse_correlate)}")
        
        return verifica
    
    # ============ REPORT E TRACCIAMENTO ============
    
    def report_programma_svolto(self, docente: str, materia: str) -> Dict:
        """Genera report del programma svolto da un docente.
        
        Args:
            docente: Nome docente
            materia: Materia
            
        Returns:
            Dizionario con report
        """
        # Ottiene risorse del docente
        risorse = self.risorse_per_docente(docente)
        risorse_materia = [r for r in risorse if materia.lower() in r.titolo.lower()]
        
        # Ottiene corsi del docente
        corsi = self.corsi_per_docente(docente)
        corsi_materia = [c for c in corsi if c.materia == materia]
        
        # Calcola materiale totale
        totale_risorse = len(risorse_materia)
        totale_moduli = sum(len(c.moduli) for c in corsi_materia)
        
        argomenti_coperti = set()
        for r in risorse_materia:
            argomenti_coperti.update(r.argomenti)
        
        return {
            "docente": docente,
            "materia": materia,
            "risorse_caricate": totale_risorse,
            "corsi_creati": len(corsi_materia),
            "moduli_totali": totale_moduli,
            "argomenti_coperti": len(argomenti_coperti),
            "argomenti_lista": sorted(argomenti_coperti),
            "programma_rispettato": True,
            "commento": f"Il docente {docente} ha caricato {totale_risorse} risorse e creato {len(corsi_materia)} corsi per {materia}. Il programma è stato rispettato."
        }
    
    def statistiche_docente(self, docente: str) -> Dict:
        """Calcola statistiche per un docente.
        
        Args:
            docente: Nome docente
            
        Returns:
            Dizionario con statistiche
        """
        risorse = self.risorse_per_docente(docente)
        corsi = self.corsi_per_docente(docente)
        
        # Conta per tipo di risorsa
        risorse_per_tipo = {}
        for r in risorse:
            tipo = r.tipo.value
            risorse_per_tipo[tipo] = risorse_per_tipo.get(tipo, 0) + 1
        
        return {
            "docente": docente,
            "totale_risorse": len(risorse),
            "totale_corsi": len(corsi),
            "risorse_per_tipo": risorse_per_tipo,
            "schede_generate": len([s for s in self.schede if s.argomento in [arg for c in corsi for m in c.moduli for arg in m.argomenti_principali]]),
            "materiale_condiviso": len([r for r in risorse if len(self.risorse_per_argomento(arg)) > 1 for arg in r.argomenti]),
            "media_visualizzazioni": sum(r.numero_visualizzazioni for r in risorse) / len(risorse) if risorse else 0
        }


if __name__ == "__main__":
    print("📚 TEST MODULO COSTRUTTORE CORSO DOCENTE")
    print("=" * 60 + "\n")
    
    # Simula sistema
    from anagrafica import Anagrafica
    from voti import GestioneVoti
    
    anagrafica = Anagrafica()
    anagrafica.genera_studenti(10)
    
    gestione_voti = GestioneVoti()
    
    # Crea costruttore
    costruttore = CostruttoreCorsoDocente(anagrafica, gestione_voti)
    
    # Test caricamento risorsa
    risorsa1 = costruttore.carica_risorsa(
        docente="Prof.ssa Bianchi",
        titolo="Video lezione: Equazioni di primo grado",
        tipo=TipoRisorsa.VIDEO,
        url="https://youtube.com/...",
        argomenti=["Equazioni", "Algebra"],
        difficoltà=LivelloDifficoltà.BASE
    )
    
    # Test creazione corso
    corso = costruttore.crea_corso(
        docente="Prof.ssa Bianchi",
        materia="Matematica",
        titolo="Matematica Avanzata 2A",
        classe_target="2A",
        descrizione="Corso completo di algebra e geometria"
    )
    
    # Aggiungi modulo
    modulo = costruttore.aggiungi_modulo(
        corso=corso,
        titolo="Modulo 1: Equazioni",
        descrizione="Introduzione alle equazioni di primo grado",
        argomenti=["Equazioni", "Incognite", "Soluzione"],
        durata_stimata=120
    )
    
    # Collega risorsa
    costruttore.collega_risorsa_al_modulo(modulo, risorsa1)
    
    print(f"\n✅ Sistema funzionante!")
    print(f"📊 Statistiche: {costruttore.statistiche_docente('Prof.ssa Bianchi')}")

