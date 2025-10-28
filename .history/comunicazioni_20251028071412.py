"""
Modulo per la gestione delle comunicazioni scuola-famiglia.
Gestisce messaggi, notifiche, avvisi e chat tra insegnanti e genitori.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, date
from enum import Enum
import random


class TipoComunicazione(Enum):
    """Tipi di comunicazione disponibili."""
    NOTIFICA = "notifica"
    MESSAGGIO = "messaggio"
    AVVISO = "avviso"
    URGENTE = "urgente"
    GENERALE = "generale"


class StatoComunicazione(Enum):
    """Stati di una comunicazione."""
    INVIATA = "inviata"
    LETTA = "letta"
    RISPOSTA = "risposta"
    ARCHIVIATA = "archiviata"


class PrioritaComunicazione(Enum):
    """Priorità della comunicazione."""
    BASSA = "bassa"
    MEDIA = "media" 
    ALTA = "alta"
    URGENTE = "urgente"


@dataclass
class Comunicazione:
    """Rappresenta una comunicazione tra scuola e famiglia."""
    
    id: int
    mittente_id: int
    mittente_tipo: str  # "insegnante", "dirigente", "segreteria", "genitore"
    destinatario_id: int
    destinatario_tipo: str  # "genitore", "insegnante", "dirigente"
    studente_id: Optional[int]  # ID studente di riferimento
    tipo: TipoComunicazione
    priorita: PrioritaComunicazione
    oggetto: str
    messaggio: str
    data_invio: datetime
    data_lettura: Optional[datetime] = None
    stato: StatoComunicazione = StatoComunicazione.INVIATA
    allegati: List[str] = field(default_factory=list)
    risposta_a: Optional[int] = None  # ID comunicazione originale se è una risposta
    note_private: str = ""
    
    def __post_init__(self):
        """Inizializza campi dopo creazione."""
        if isinstance(self.data_invio, str):
            self.data_invio = datetime.fromisoformat(self.data_invio)
        if self.data_lettura and isinstance(self.data_lettura, str):
            self.data_lettura = datetime.fromisoformat(self.data_lettura)
    
    @property
    def is_letta(self) -> bool:
        """Verifica se la comunicazione è stata letta."""
        return self.data_lettura is not None
    
    @property
    def giorni_da_invio(self) -> int:
        """Calcola giorni passati dall'invio."""
        return (datetime.now() - self.data_invio).days
    
    def marca_come_letta(self) -> None:
        """Marca la comunicazione come letta."""
        self.data_lettura = datetime.now()
        self.stato = StatoComunicazione.LETTA
    
    def to_dict(self) -> Dict:
        """Converte in dizionario per JSON."""
        return {
            "id": self.id,
            "mittente_id": self.mittente_id,
            "mittente_tipo": self.mittente_tipo,
            "destinatario_id": self.destinatario_id,
            "destinatario_tipo": self.destinatario_tipo,
            "studente_id": self.studente_id,
            "tipo": self.tipo.value,
            "priorita": self.priorita.value,
            "oggetto": self.oggetto,
            "messaggio": self.messaggio,
            "data_invio": self.data_invio.isoformat(),
            "data_lettura": self.data_lettura.isoformat() if self.data_lettura else None,
            "stato": self.stato.value,
            "allegati": self.allegati,
            "risposta_a": self.risposta_a,
            "note_private": self.note_private,
            "is_letta": self.is_letta,
            "giorni_da_invio": self.giorni_da_invio
        }


@dataclass
class NotificaAutomatica:
    """Configurazione per notifiche automatiche."""
    
    id: int
    nome: str
    descrizione: str
    attiva: bool
    tipo_evento: str  # "voto_basso", "assenza", "ritardo", "comportamento"
    soglia: Optional[float]  # Soglia per attivare la notifica
    template_messaggio: str
    destinatari: List[str]  # ["genitori", "insegnanti", "dirigente"]
    frequenza: str  # "immediata", "giornaliera", "settimanale"
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descrizione": self.descrizione,
            "attiva": self.attiva,
            "tipo_evento": self.tipo_evento,
            "soglia": self.soglia,
            "template_messaggio": self.template_messaggio,
            "destinatari": self.destinatari,
            "frequenza": self.frequenza
        }


class GestioneComunicazioni:
    """Gestisce tutte le comunicazioni scuola-famiglia."""
    
    def __init__(self):
        """Inizializza il sistema comunicazioni."""
        self.comunicazioni: List[Comunicazione] = []
        self.notifiche_automatiche: List[NotificaAutomatica] = []
        self._prossimo_id = 1
        self._prossimo_id_notifica = 1
        self._inizializza_notifiche_default()
    
    def _inizializza_notifiche_default(self):
        """Crea notifiche automatiche di default."""
        notifiche_default = [
            NotificaAutomatica(
                id=1,
                nome="Voto Insufficiente",
                descrizione="Notifica ai genitori per voti sotto il 6",
                attiva=True,
                tipo_evento="voto_basso",
                soglia=6.0,
                template_messaggio="Gentile genitore, il vostro figlio/a {nome_studente} ha ricevuto un voto insufficiente ({voto}) in {materia}. Vi invitiamo a contattare l'insegnante per maggiori informazioni.",
                destinatari=["genitori"],
                frequenza="immediata"
            ),
            NotificaAutomatica(
                id=2,
                nome="Assenza Non Giustificata",
                descrizione="Avviso per assenze non giustificate dopo 3 giorni",
                attiva=True,
                tipo_evento="assenza",
                soglia=3.0,
                template_messaggio="Gentile genitore, risulta un'assenza non giustificata di {nome_studente} in data {data}. Vi preghiamo di provvedere alla giustificazione.",
                destinatari=["genitori"],
                frequenza="giornaliera"
            ),
            NotificaAutomatica(
                id=3,
                nome="Ritardi Frequenti",
                descrizione="Avviso per più di 5 ritardi nel mese",
                attiva=True,
                tipo_evento="ritardo",
                soglia=5.0,
                template_messaggio="Gentile genitore, {nome_studente} ha accumulato {numero_ritardi} ritardi questo mese. Vi invitiamo a prestare maggiore attenzione alla puntualità.",
                destinatari=["genitori"],
                frequenza="settimanale"
            ),
            NotificaAutomatica(
                id=4,
                nome="Nota Disciplinare",
                descrizione="Comunicazione immediata per note disciplinari",
                attiva=True,
                tipo_evento="comportamento",
                soglia=None,
                template_messaggio="Gentile genitore, {nome_studente} ha ricevuto una nota disciplinare: {descrizione_nota}. Vi preghiamo di prendere visione e eventualmente di contattare la scuola.",
                destinatari=["genitori"],
                frequenza="immediata"
            )
        ]
        
        self.notifiche_automatiche.extend(notifiche_default)
        self._prossimo_id_notifica = 5
    
    def crea_comunicazione(self, mittente_id: int, mittente_tipo: str,
                          destinatario_id: int, destinatario_tipo: str,
                          oggetto: str, messaggio: str,
                          tipo: TipoComunicazione = TipoComunicazione.MESSAGGIO,
                          priorita: PrioritaComunicazione = PrioritaComunicazione.MEDIA,
                          studente_id: Optional[int] = None,
                          risposta_a: Optional[int] = None) -> Comunicazione:
        """Crea una nuova comunicazione."""
        
        comunicazione = Comunicazione(
            id=self._prossimo_id,
            mittente_id=mittente_id,
            mittente_tipo=mittente_tipo,
            destinatario_id=destinatario_id,
            destinatario_tipo=destinatario_tipo,
            studente_id=studente_id,
            tipo=tipo,
            priorita=priorita,
            oggetto=oggetto,
            messaggio=messaggio,
            data_invio=datetime.now(),
            risposta_a=risposta_a
        )
        
        self.comunicazioni.append(comunicazione)
        self._prossimo_id += 1
        
        return comunicazione
    
    def invia_notifica_automatica(self, tipo_evento: str, studente_id: int, 
                                 dati_evento: Dict) -> List[Comunicazione]:
        """Invia notifiche automatiche basate su eventi."""
        notifiche_inviate = []
        
        # Trova notifiche attive per questo tipo di evento
        notifiche_attive = [n for n in self.notifiche_automatiche 
                           if n.attiva and n.tipo_evento == tipo_evento]
        
        for notifica in notifiche_attive:
            # Verifica soglia se presente
            if notifica.soglia is not None:
                valore_evento = dati_evento.get("valore", 0)
                if tipo_evento == "voto_basso" and valore_evento >= notifica.soglia:
                    continue
                elif tipo_evento in ["assenza", "ritardo"] and valore_evento < notifica.soglia:
                    continue
            
            # Personalizza messaggio
            messaggio = notifica.template_messaggio.format(**dati_evento)
            
            # Invia ai destinatari configurati
            if "genitori" in notifica.destinatari:
                # Simula invio ai genitori (qui useresti IDs reali)
                genitore_id = studente_id + 1000  # Convenzione fittizia
                
                comunicazione = self.crea_comunicazione(
                    mittente_id=1,  # Sistema automatico
                    mittente_tipo="sistema",
                    destinatario_id=genitore_id,
                    destinatario_tipo="genitore",
                    oggetto=notifica.nome,
                    messaggio=messaggio,
                    tipo=TipoComunicazione.NOTIFICA,
                    priorita=PrioritaComunicazione.ALTA,
                    studente_id=studente_id
                )
                
                notifiche_inviate.append(comunicazione)
        
        return notifiche_inviate
    
    def get_comunicazioni_per_utente(self, user_id: int, tipo_utente: str, 
                                   solo_non_lette: bool = False) -> List[Comunicazione]:
        """Ottiene comunicazioni per un utente specifico."""
        comunicazioni_utente = []
        
        for com in self.comunicazioni:
            # Controlla se l'utente è destinatario
            if (com.destinatario_id == user_id and com.destinatario_tipo == tipo_utente):
                if solo_non_lette and com.is_letta:
                    continue
                comunicazioni_utente.append(com)
            # Controlla se l'utente è mittente
            elif (com.mittente_id == user_id and com.mittente_tipo == tipo_utente):
                comunicazioni_utente.append(com)
        
        # Ordina per data (più recenti prima)
        comunicazioni_utente.sort(key=lambda x: x.data_invio, reverse=True)
        return comunicazioni_utente
    
    def get_comunicazioni_studente(self, studente_id: int) -> List[Comunicazione]:
        """Ottiene comunicazioni relative a uno studente."""
        return [com for com in self.comunicazioni if com.studente_id == studente_id]
    
    def marca_come_letta(self, comunicazione_id: int, user_id: int) -> bool:
        """Marca una comunicazione come letta."""
        for com in self.comunicazioni:
            if (com.id == comunicazione_id and 
                com.destinatario_id == user_id and 
                not com.is_letta):
                com.marca_come_letta()
                return True
        return False
    
    def crea_risposta(self, comunicazione_originale_id: int, mittente_id: int,
                     mittente_tipo: str, messaggio: str) -> Optional[Comunicazione]:
        """Crea una risposta a una comunicazione."""
        # Trova comunicazione originale
        originale = None
        for com in self.comunicazioni:
            if com.id == comunicazione_originale_id:
                originale = com
                break
        
        if not originale:
            return None
        
        # Crea risposta
        risposta = self.crea_comunicazione(
            mittente_id=mittente_id,
            mittente_tipo=mittente_tipo,
            destinatario_id=originale.mittente_id,
            destinatario_tipo=originale.mittente_tipo,
            oggetto=f"Re: {originale.oggetto}",
            messaggio=messaggio,
            tipo=TipoComunicazione.MESSAGGIO,
            priorita=originale.priorita,
            studente_id=originale.studente_id,
            risposta_a=comunicazione_originale_id
        )
        
        return risposta
    
    def get_statistiche_comunicazioni(self) -> Dict:
        """Restituisce statistiche sulle comunicazioni."""
        totali = len(self.comunicazioni)
        if totali == 0:
            return {"totale": 0, "lette": 0, "non_lette": 0, "percentuale_lettura": 0}
        
        lette = len([c for c in self.comunicazioni if c.is_letta])
        non_lette = totali - lette
        
        # Statistiche per tipo
        per_tipo = {}
        for tipo in TipoComunicazione:
            count = len([c for c in self.comunicazioni if c.tipo == tipo])
            per_tipo[tipo.value] = count
        
        # Statistiche per priorità
        per_priorita = {}
        for priorita in PrioritaComunicazione:
            count = len([c for c in self.comunicazioni if c.priorita == priorita])
            per_priorita[priorita.value] = count
        
        return {
            "totale": totali,
            "lette": lette,
            "non_lette": non_lette,
            "percentuale_lettura": round((lette / totali) * 100, 2),
            "per_tipo": per_tipo,
            "per_priorita": per_priorita,
            "comunicazioni_oggi": len([c for c in self.comunicazioni 
                                     if c.data_invio.date() == date.today()]),
            "comunicazioni_settimana": len([c for c in self.comunicazioni 
                                          if (datetime.now() - c.data_invio).days <= 7])
        }
    
    def genera_comunicazioni_demo(self, studenti_ids: List[int], insegnanti_ids: List[int]):
        """Genera comunicazioni demo per test."""
        oggetti_demo = [
            "Colloquio con i genitori",
            "Verifica di matematica",
            "Uscita didattica",
            "Riunione di classe",
            "Consiglio di classe",
            "Comunicazione assenze",
            "Progetto scolastico",
            "Attività extracurriculare"
        ]
        
        messaggi_demo = [
            "Si comunica che è necessario un colloquio per discutere del rendimento scolastico.",
            "Gentile genitore, la informiamo sui progressi di suo/a figlio/a.",
            "È prevista un'uscita didattica. Si prega di firmare l'autorizzazione.",
            "La invitiamo alla riunione per discutere l'andamento della classe.",
            "Convocazione per il consiglio di classe straordinario.",
            "Si prega di giustificare le assenze accumulate.",
            "Proposta di partecipazione al progetto interdisciplinare.",
            "Opportunità di partecipazione ad attività pomeridiane."
        ]
        
        # Genera 20 comunicazioni casuali
        for _ in range(20):
            studente_id = random.choice(studenti_ids)
            insegnante_id = random.choice(insegnanti_ids)
            genitore_id = studente_id + 1000  # Convenzione fittizia
            
            oggetto = random.choice(oggetti_demo)
            messaggio = random.choice(messaggi_demo)
            
            tipo = random.choice(list(TipoComunicazione))
            priorita = random.choice(list(PrioritaComunicazione))
            
            # Crea comunicazione da insegnante a genitore
            com = self.crea_comunicazione(
                mittente_id=insegnante_id,
                mittente_tipo="insegnante",
                destinatario_id=genitore_id,
                destinatario_tipo="genitore",
                oggetto=oggetto,
                messaggio=messaggio,
                tipo=tipo,
                priorita=priorita,
                studente_id=studente_id
            )
            
            # Simula che alcune siano già state lette
            if random.random() < 0.6:  # 60% di probabilità
                com.marca_come_letta()
            
            # Simula alcune risposte
            if random.random() < 0.3:  # 30% di probabilità
                self.crea_risposta(
                    comunicazione_originale_id=com.id,
                    mittente_id=genitore_id,
                    mittente_tipo="genitore",
                    messaggio="Grazie per la comunicazione. Prendo atto e resto a disposizione."
                )
    
    def __len__(self) -> int:
        """Restituisce il numero di comunicazioni."""
        return len(self.comunicazioni)
    
    def __repr__(self) -> str:
        """Rappresentazione stringa."""
        return f"GestioneComunicazioni({len(self.comunicazioni)} comunicazioni)"


if __name__ == "__main__":
    print("🔔 TEST SISTEMA COMUNICAZIONI SCUOLA-FAMIGLIA")
    print("=" * 60 + "\n")
    
    # Test del sistema
    comunicazioni = GestioneComunicazioni()
    
    # Simula alcuni IDs
    studenti = [1, 2, 3, 4, 5]
    insegnanti = [101, 102, 103]
    
    # Genera dati demo
    comunicazioni.genera_comunicazioni_demo(studenti, insegnanti)
    
    print(f"📊 STATISTICHE")
    stats = comunicazioni.get_statistiche_comunicazioni()
    for k, v in stats.items():
        if isinstance(v, dict):
            print(f"   {k.replace('_', ' ').title()}:")
            for sub_k, sub_v in v.items():
                print(f"     {sub_k}: {sub_v}")
        else:
            print(f"   {k.replace('_', ' ').title()}: {v}")
    
    print(f"\n📨 Comunicazioni totali: {len(comunicazioni)}")
    print(f"🔔 Notifiche automatiche attive: {len([n for n in comunicazioni.notifiche_automatiche if n.attiva])}")
    
    # Test notifica automatica
    print("\n🚨 TEST NOTIFICA AUTOMATICA")
    notifiche = comunicazioni.invia_notifica_automatica(
        tipo_evento="voto_basso",
        studente_id=1,
        dati_evento={
            "nome_studente": "Mario Rossi",
            "voto": 4.5,
            "materia": "Matematica",
            "valore": 4.5
        }
    )
    print(f"   Notifiche inviate: {len(notifiche)}")
