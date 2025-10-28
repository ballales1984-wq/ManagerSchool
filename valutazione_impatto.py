"""
Modulo per la valutazione dell'impatto educativo del sistema.
Dimostra l'efficacia di ManagerSchool, valorizza il lavoro del docente e accompagna lo studente.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
import random


class TipoAttività(Enum):
    """Tipi di attività tracciate."""
    SCHEDA_INTELLIGENTE = "scheda_intelligente"
    RIPASSO_COPILOT = "ripasso_copilot"
    ESERCIZI_SVOLTI = "esercizi_svolti"
    CONSIGLIO_RICEVUTO = "consiglio_ricevuto"
    MATERIALE_STUDIATO = "materiale_studiato"
    VIDEO_LESSON = "video_lesson"


class LivelloImpatto(Enum):
    """Livelli di impatto del sistema."""
    ALTISSIMO = "altissimo"
    ALTO = "alto"
    MEDIO = "medio"
    BASSO = "basso"
    NULLO = "nullo"


@dataclass
class MaterialeEsame:
    """Materiale preparato dal docente per una verifica."""
    
    id: int
    docente: str
    materia: str
    data_verifica: str
    argomenti: List[str] = field(default_factory=list)
    esercizi_caricati: List[str] = field(default_factory=list)
    link_copilot: Optional[str] = None
    video_lezioni: List[str] = field(default_factory=list)
    note_docente: str = ""
    programma_rispettato: bool = True
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "docente": self.docente,
            "materia": self.materia,
            "data_verifica": self.data_verifica,
            "argomenti": self.argomenti,
            "esercizi_caricati": self.esercizi_caricati,
            "link_copilot": self.link_copilot,
            "video_lezioni": self.video_lezioni,
            "note_docente": self.note_docente,
            "programma_rispettato": self.programma_rispettato
        }


@dataclass
class AttivitàStudente:
    """Attività svolta da uno studente."""
    
    id: int
    studente_id: int
    tipo: TipoAttività
    data: str
    dettagli: str = ""
    risultato: Optional[float] = None  # Voto o punteggio ottenuto
    feedback: str = ""
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "studente_id": self.studente_id,
            "tipo": self.tipo.value,
            "data": self.data,
            "dettagli": self.dettagli,
            "risultato": self.risultato,
            "feedback": self.feedback
        }


@dataclass
class TracciamentoMiglioramento:
    """Traccia il miglioramento di uno studente."""
    
    studente_id: int
    materia: str
    voto_precedente: Optional[float] = None
    voto_attuale: Optional[float] = None
    attività_svolte: List[AttivitàStudente] = field(default_factory=list)
    materiale_studiato: List[MaterialeEsame] = field(default_factory=list)
    giorni_studio: int = 0
    frequenza_uso: float = 0.0  # 0-1
    miglioramento: float = 0.0
    livello_impatto: LivelloImpatto = LivelloImpatto.NULLO
    commento_automatico: str = ""
    
    def calcola_miglioramento(self):
        """Calcola il miglioramento confrontando i voti."""
        if self.voto_precedente is not None and self.voto_attuale is not None:
            self.miglioramento = self.voto_attuale - self.voto_precedente
            
            # Determina livello di impatto
            if self.voto_attuale >= 8 and self.miglioramento >= 2:
                self.livello_impatto = LivelloImpatto.ALTISSIMO
            elif self.miglioramento >= 1:
                self.livello_impatto = LivelloImpatto.ALTO
            elif self.miglioramento > 0:
                self.livello_impatto = LivelloImpatto.MEDIO
            elif self.miglioramento == 0:
                self.livello_impatto = LivelloImpatto.BASSO
            else:
                self.livello_impatto = LivelloImpatto.NULLO
    
    def genera_commento(self) -> str:
        """Genera un commento automatico sul miglioramento."""
        if self.livello_impatto == LivelloImpatto.ALTISSIMO:
            return f"Miglioramento eccellente (+{self.miglioramento:.1f}). Lo studente ha utilizzato attivamente gli strumenti di ManagerSchool. L'impatto educativo è stato molto positivo."
        elif self.livello_impatto == LivelloImpatto.ALTO:
            return f"Miglioramento significativo (+{self.miglioramento:.1f}). L'uso del sistema ha contribuito positivamente al rendimento."
        elif self.livello_impatto == LivelloImpatto.MEDIO:
            return f"Miglioramento moderato (+{self.miglioramento:.1f}). Lo studente sta beneficiando dell'uso del sistema."
        elif self.livello_impatto == LivelloImpatto.BASSO:
            return f"Il voto è rimasto stabile. Incoraggiare un uso più continuativo degli strumenti disponibili."
        else:
            return f"Rendimento in calo (-{abs(self.miglioramento):.1f}). Servono strategie di supporto personalizzate."
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "studente_id": self.studente_id,
            "materia": self.materia,
            "voto_precedente": self.voto_precedente,
            "voto_attuale": self.voto_attuale,
            "attività_svolte": [a.to_dict() for a in self.attività_svolte],
            "materiale_studiato": [m.to_dict() for m in self.materiale_studiato],
            "giorni_studio": self.giorni_studio,
            "frequenza_uso": self.frequenza_uso,
            "miglioramento": self.miglioramento,
            "livello_impatto": self.livello_impatto.value,
            "commento_automatico": self.commento_automatico or self.genera_commento()
        }


class ValutazioneImpattoEducativo:
    """Valuta l'impatto educativo di ManagerSchool."""
    
    def __init__(self, anagrafica, gestione_voti):
        """Inizializza la valutazione di impatto.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
        
        self.materiale_esame: List[MaterialeEsame] = []
        self.attività_studenti: List[AttivitàStudente] = []
        self.tracciamenti: List[TracciamentoMiglioramento] = []
        
        self._prossimo_id_materiale = 1
        self._prossimo_id_attività = 1
    
    # ============ GESTIONE MATERIALE DOCENTE ============
    
    def registra_materiale_esame(self, docente: str, materia: str, data_verifica: str,
                                 argomenti: List[str] = None, esercizi: List[str] = None,
                                 link_copilot: Optional[str] = None) -> MaterialeEsame:
        """Registra il materiale preparato dal docente.
        
        Args:
            docente: Nome del docente
            materia: Materia
            data_verifica: Data della verifica
            argomenti: Lista argomenti trattati
            esercizi: Lista esercizi caricati
            link_copilot: Link Copilot fornito
            
        Returns:
            MaterialeEsame registrato
        """
        materiale = MaterialeEsame(
            id=self._prossimo_id_materiale,
            docente=docente,
            materia=materia,
            data_verifica=data_verifica,
            argomenti=argomenti or [],
            esercizi_caricati=esercizi or [],
            link_copilot=link_copilot
        )
        
        self.materiale_esame.append(materiale)
        self._prossimo_id_materiale += 1
        
        print(f"✅ Materiale registrato per {materia} - Verifica del {data_verifica}")
        print(f"   Docente: {docente}")
        print(f"   Argomenti: {len(argomenti or [])}, Esercizi: {len(esercizi or [])}")
        
        return materiale
    
    def materiale_per_materia(self, materia: str) -> List[MaterialeEsame]:
        """Ottiene materiale per una materia."""
        return [m for m in self.materiale_esame if m.materia == materia]
    
    def materiale_per_docente(self, docente: str) -> List[MaterialeEsame]:
        """Ottiene materiale di un docente."""
        return [m for m in self.materiale_esame if m.docente == docente]
    
    # ============ TRACCIAMENTO ATTIVITÀ STUDENTI ============
    
    def traccia_studio_studente(self, studente_id: int, tipo: TipoAttività,
                               dettagli: str = "", risultato: Optional[float] = None) -> AttivitàStudente:
        """Traccia un'attività svolta da uno studente.
        
        Args:
            studente_id: ID dello studente
            tipo: Tipo di attività
            dettagli: Dettagli attività
            risultato: Risultato ottenuto (opzionale)
            
        Returns:
            AttivitàStudente registrata
        """
        attività = AttivitàStudente(
            id=self._prossimo_id_attività,
            studente_id=studente_id,
            tipo=tipo,
            data=datetime.now().strftime("%Y-%m-%d"),
            dettagli=dettagli,
            risultato=risultato
        )
        
        self.attività_studenti.append(attività)
        self._prossimo_id_attività += 1
        
        return attività
    
    def attività_studente(self, studente_id: int, materia: Optional[str] = None) -> List[AttivitàStudente]:
        """Ottiene attività di uno studente."""
        attività = [a for a in self.attività_studenti if a.studente_id == studente_id]
        
        if materia:
            # Filtra per materia (semplificato)
            pass
        
        return sorted(attività, key=lambda x: x.data, reverse=True)
    
    def frequenza_uso_studente(self, studente_id: int, giorni_limite: int = 30) -> float:
        """Calcola la frequenza d'uso del sistema da parte di uno studente.
        
        Args:
            studente_id: ID dello studente
            giorni_limite: Giorni da considerare
            
        Returns:
            Frequenza d'uso (0-1)
        """
        data_limite = (datetime.now() - timedelta(days=giorni_limite)).strftime("%Y-%m-%d")
        
        attività_periodo = [a for a in self.attività_studenti 
                           if a.studente_id == studente_id and a.data >= data_limite]
        
        # Frequenza = numero attività / giorni considerati
        return min(1.0, len(attività_periodo) / giorni_limite)
    
    # ============ VALUTAZIONE MIGLIORAMENTO ============
    
    def valuta_miglioramento(self, studente_id: int, materia: str) -> TracciamentoMiglioramento:
        """Valuta il miglioramento di uno studente in una materia.
        
        Args:
            studente_id: ID dello studente
            materia: Materia
            
        Returns:
            TracciamentoMiglioramento
        """
        # Ottiene voti dello studente nella materia
        voti_materia = [v for v in self.gestione_voti.voti 
                       if v.id_studente == studente_id and v.materia == materia]
        
        if len(voti_materia) < 2:
            return None
        
        # Ordina per data
        voti_materia.sort(key=lambda v: v.data)
        
        # Voto precedente (secondo più recente)
        voto_precedente = voti_materia[-2].voto
        
        # Voto attuale (più recente)
        voto_attuale = voti_materia[-1].voto
        
        # Crea tracciamento
        tracciamento = TracciamentoMiglioramento(
            studente_id=studente_id,
            materia=materia,
            voto_precedente=voto_precedente,
            voto_attuale=voto_attuale
        )
        
        # Ottiene attività dello studente
        tracciamento.attività_svolte = self.attività_studente(studente_id, materia)
        tracciamento.frequenza_uso = self.frequenza_uso_studio_studente(studente_id)
        
        # Calcola miglioramento
        tracciamento.calcola_miglioramento()
        tracciamento.commento_automatico = tracciamento.genera_commento()
        
        self.tracciamenti.append(tracciamento)
        
        return tracciamento
    
    def frequenza_uso_studio_studente(self, studente_id: int) -> float:
        """Calcola frequenza d'uso (versione interna)."""
        return self.frequenza_uso_studente(studente_id)
    
    # ============ REPORT E STATISTICHE ============
    
    def genera_report_studente(self, studente_id: int, materia: str) -> Dict:
        """Genera un report dettagliato per uno studente.
        
        Args:
            studente_id: ID dello studente
            materia: Materia
            
        Returns:
            Dizionario con report
        """
        studente = self.anagrafica.trova_studente(studente_id)
        if not studente:
            return {"errore": "Studente non trovato"}
        
        tracciamento = self.valuta_miglioramento(studente_id, materia)
        attività = self.attività_studente(studente_id, materia)
        
        return {
            "studente": studente.to_dict(),
            "materia": materia,
            "tracciamento": tracciamento.to_dict() if tracciamento else None,
            "attività_recenti": [a.to_dict() for a in attività[:5]],
            "frequenza_uso": self.frequenza_uso_studente(studente_id),
            "materiale_disponibile": [m.to_dict() for m in self.materiale_per_materia(materia)]
        }
    
    def genera_report_classe(self, classe: str, materia: str) -> Dict:
        """Genera report per tutta una classe.
        
        Args:
            classe: Nome classe
            materia: Materia
            
        Returns:
            Dizionario con report classe
        """
        studenti_classe = self.anagrafica.studenti_per_classe(classe)
        report_studenti = []
        
        for studente in studenti_classe:
            tracciamento = self.valuta_miglioramento(studente.id, materia)
            if tracciamento:
                report_studenti.append({
                    "studente": studente.to_dict(),
                    "miglioramento": tracciamento.miglioramento,
                    "livello_impatto": tracciamento.livello_impatto.value,
                    "commento": tracciamento.commento_automatico
                })
        
        # Statistiche aggregate
        medie_miglioramento = [r["miglioramento"] for r in report_studenti if "miglioramento" in r]
        
        return {
            "classe": classe,
            "materia": materia,
            "studenti": report_studenti,
            "statistiche": {
                "totale_studenti": len(report_studenti),
                "media_miglioramento": sum(medie_miglioramento) / len(medie_miglioramento) if medie_miglioramento else 0,
                "studenti_migliorati": len([r for r in report_studenti if r.get("miglioramento", 0) > 0]),
                "studenti_peggiorati": len([r for r in report_studenti if r.get("miglioramento", 0) < 0])
            }
        }
    
    def genera_report_docente(self, docente: str) -> Dict:
        """Genera report per un docente.
        
        Args:
            docente: Nome docente
            
        Returns:
            Dizionario con report
        """
        materiale = self.materiale_per_docente(docente)
        
        statistiche = {
            "materiale_caricato": len(materiale),
            "verifiche_programmate": len(materiale),
            "esercizi_totali": sum(len(m.esercizi_caricati) for m in materiale),
            "link_copilot_forniti": len([m for m in materiale if m.link_copilot]),
            "programma_rispettato": all(m.programma_rispettato for m in materiale)
        }
        
        return {
            "docente": docente,
            "materiale": [m.to_dict() for m in materiale],
            "statistiche": statistiche,
            "commento": self._genera_commento_docente(docente, statistiche)
        }
    
    def _genera_commento_docente(self, docente: str, stats: Dict) -> str:
        """Genera commento automatico per il docente."""
        if stats["programma_rispettato"]:
            return f"Il docente {docente} ha rispettato il programma e ha caricato {stats['materiale_caricato']} materiali. Ha fornito supporto efficace agli studenti con esercizi e risorse didattiche."
        else:
            return f"Il docente {docente} ha caricato materiale ma alcuni argomenti del programma richiedono maggiore attenzione."
    
    def statistiche_impatto_generale(self) -> Dict:
        """Calcola statistiche generali sull'impatto del sistema."""
        if not self.tracciamenti:
            return {"messaggio": "Nessun tracciamento disponibile"}
        
        # Statistiche sui livelli di impatto
        per_livello = {}
        for livello in LivelloImpatto:
            per_livello[livello.value] = len([t for t in self.tracciamenti if t.livello_impatto == livello])
        
        # Media miglioramento
        miglioramenti = [t.miglioramento for t in self.tracciamenti if t.miglioramento is not None]
        media_miglioramento = sum(miglioramenti) / len(miglioramenti) if miglioramenti else 0
        
        return {
            "totale_tracciamenti": len(self.tracciamenti),
            "livelli_impatto": per_livello,
            "media_miglioramento": round(media_miglioramento, 2),
            "materiale_totale": len(self.materiale_esame),
            "attività_totali": len(self.attività_studenti),
            "studenti_attivi": len(set(a.studente_id for a in self.attività_studenti))
        }


if __name__ == "__main__":
    print("📊 TEST MODULO VALUTAZIONE IMPATTO EDUCATIVO")
    print("=" * 60 + "\n")
    
    # Simula sistema
    from anagrafica import Anagrafica
    from voti import GestioneVoti
    
    anagrafica = Anagrafica()
    anagrafica.genera_studenti(10)
    
    gestione_voti = GestioneVoti(anagrafica)
    
    # Crea valutatore
    valutatore = ValutazioneImpattoEducativo(anagrafica, gestione_voti)
    
    # Simula materiale docente
    materiale = valutatore.registra_materiale_esame(
        docente="Prof.ssa Bianchi",
        materia="Matematica",
        data_verifica="2025-10-30",
        argomenti=["Equazioni", "Funzioni"],
        esercizi=["Es. 1 pag 45", "Es. 2 pag 48"],
        link_copilot="https://copilot.microsoft.com/..."
    )
    
    print(f"\n✅ Materiale registrato: {materiale.titolo}")
    print(f"📝 Statistiche: {valutatore.statistiche_impatto_generale()}")
    print("\n✅ Test completato!")

