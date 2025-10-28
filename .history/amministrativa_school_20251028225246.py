"""
Modulo per la gestione amministrativa della scuola.
Gestisce alunni, personale, presenze/assenze e documenti amministrativi.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from enum import Enum
import random


class TipoPresenza(Enum):
    """Tipi di registrazione di presenza."""
    PRESENTE = "presente"
    ASSENTE = "assente"
    RITARDO = "ritardo"
    USCITA_ANTICIPATA = "uscita anticipata"
    GIUSTIFICATO = "giustificato"
    NON_GIUSTIFICATO = "non giustificato"


class TipoDocumento(Enum):
    """Tipi di documenti amministrativi."""
    CIRCOLARE = "circolare"
    PROTOCOLLO = "protocollo"
    COMUNICAZIONE = "comunicazione"
    ORDINANZA = "ordinanza"
    DELIBERA = "delibera"


@dataclass
class AnagraficaAlunno:
    """Profilo anagrafico completo di un alunno."""
    
    id: int
    nome: str
    cognome: str
    data_nascita: str  # YYYY-MM-DD
    luogo_nascita: str
    codice_fiscale: str
    classe: str
    indirizzo: str
    telefono: str
    email: Optional[str] = None
    genitore1_nome: str = ""
    genitore1_tel: str = ""
    genitore2_nome: str = ""
    genitore2_tel: str = ""
    note: str = ""
    
    @property
    def nome_completo(self) -> str:
        """Restituisce il nome completo."""
        return f"{self.nome} {self.cognome}"
    
    @property
    def età(self) -> int:
        """Calcola l'età dell'alunno."""
        birth_date = datetime.strptime(self.data_nascita, "%Y-%m-%d")
        today = datetime.now()
        return (today - birth_date).days // 365
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cognome": self.cognome,
            "nome_completo": self.nome_completo,
            "data_nascita": self.data_nascita,
            "luogo_nascita": self.luogo_nascita,
            "codice_fiscale": self.codice_fiscale,
            "classe": self.classe,
            "indirizzo": self.indirizzo,
            "telefono": self.telefono,
            "email": self.email,
            "genitore1_nome": self.genitore1_nome,
            "genitore1_tel": self.genitore1_tel,
            "genitore2_nome": self.genitore2_nome,
            "genitore2_tel": self.genitore2_tel,
            "note": self.note,
            "età": self.età
        }


@dataclass
class Presenza:
    """Registrazione di presenza/assenza."""
    
    id: int
    studente_id: int
    data: str  # YYYY-MM-DD
    ora: Optional[str] = None  # Per ritardi/entrate
    tipo: TipoPresenza = TipoPresenza.PRESENTE
    motivo: str = ""
    giustificato: bool = False
    data_giustifica: Optional[str] = None
    docente_registrante: str = ""
    note: str = ""
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "studente_id": self.studente_id,
            "data": self.data,
            "ora": self.ora,
            "tipo": self.tipo.value,
            "motivo": self.motivo,
            "giustificato": self.giustificato,
            "data_giustifica": self.data_giustifica,
            "docente_registrante": self.docente_registrante,
            "note": self.note
        }


@dataclass
class DocumentoAmministrativo:
    """Documento amministrativo (circolare, protocollo, etc)."""
    
    id: int
    titolo: str
    tipo: TipoDocumento
    data: str  # YYYY-MM-DD
    protocollo: Optional[str] = None
    mittente: str = ""
    destinatari: List[str] = field(default_factory=list)
    contenuto: str = ""
    allegati: List[str] = field(default_factory=list)
    firmato_da: str = ""
    data_firma: Optional[str] = None
    pubblico: bool = True
    note: str = ""
    
    def to_dict(self) -> Dict:
        """Converte in dizionario."""
        return {
            "id": self.id,
            "titolo": self.titolo,
            "tipo": self.tipo.value,
            "data": self.data,
            "protocollo": self.protocollo,
            "mittente": self.mittente,
            "destinatari": self.destinatari,
            "contenuto": self.contenuto,
            "allegati": self.allegati,
            "firmato_da": self.firmato_da,
            "data_firma": self.data_firma,
            "pubblico": self.pubblico,
            "note": self.note
        }


class GestionePersonale:
    """Gestisce il personale della scuola."""
    
    def __init__(self):
        """Inizializza la gestione personale."""
        self.personale: Dict[str, Dict] = {}
    
    def aggiungi_persona(self, nome: str, ruolo: str, materia: str = "",
                        classi: List[str] = None, telefono: str = "") -> None:
        """Aggiunge una persona al personale.
        
        Args:
            nome: Nome completo
            ruolo: Ruolo (docente, ATA, dirigente, ecc.)
            materia: Materia insegnata (per docenti)
            classi: Lista di classi assegnate
            telefono: Numero di telefono
        """
        self.personale[nome] = {
            "nome": nome,
            "ruolo": ruolo,
            "materia": materia,
            "classi": classi or [],
            "telefono": telefono,
            "data_registro": datetime.now().strftime("%Y-%m-%d")
        }
    
    def trova_persona(self, nome: str) -> Optional[Dict]:
        """Trova una persona per nome."""
        return self.personale.get(nome)
    
    def personale_per_ruolo(self, ruolo: str) -> List[Dict]:
        """Ottiene personale per ruolo."""
        return [p for p in self.personale.values() if p["ruolo"] == ruolo]
    
    def statistiche_personale(self) -> Dict:
        """Calcola statistiche sul personale."""
        totali = len(self.personale)
        per_ruolo = {}
        
        for persona in self.personale.values():
            ruolo = persona["ruolo"]
            per_ruolo[ruolo] = per_ruolo.get(ruolo, 0) + 1
        
        return {
            "totale": totali,
            "per_ruolo": per_ruolo
        }


class AmministrativaSchool:
    """Gestione completa del registro amministrativo scolastico."""
    
    def __init__(self):
        """Inizializza il sistema amministrativo."""
        self.alunni: Dict[int, AnagraficaAlunno] = {}
        self.personale_manager = GestionePersonale()
        self.presenze: List[Presenza] = []
        self.documenti: List[DocumentoAmministrativo] = []
        self._prossimo_id_alunno = 1
        self._prossimo_id_presenza = 1
        self._prossimo_id_documento = 1
    
    # ============ GESTIONE ALUNNI ============
    
    def aggiungi_alunno(self, nome: str, cognome: str, data_nascita: str,
                       luogo_nascita: str, classe: str, codice_fiscale: str = "",
                       indirizzo: str = "", telefono: str = "") -> AnagraficaAlunno:
        """Aggiunge un alunno all'anagrafica.
        
        Args:
            nome: Nome dell'alunno
            cognome: Cognome dell'alunno
            data_nascita: Data di nascita (YYYY-MM-DD)
            luogo_nascita: Luogo di nascita
            classe: Classe di appartenenza
            codice_fiscale: Codice fiscale
            indirizzo: Indirizzo di residenza
            telefono: Numero di telefono
            
        Returns:
            AnagraficaAlunno creata
        """
        alunno = AnagraficaAlunno(
            id=self._prossimo_id_alunno,
            nome=nome,
            cognome=cognome,
            data_nascita=data_nascita,
            luogo_nascita=luogo_nascita,
            codice_fiscale=codice_fiscale or self._genera_codice_fiscale(nome, cognome, data_nascita),
            classe=classe,
            indirizzo=indirizzo,
            telefono=telefono
        )
        
        self.alunni[self._prossimo_id_alunno] = alunno
        self._prossimo_id_alunno += 1
        
        return alunno
    
    def _genera_codice_fiscale(self, nome: str, cognome: str, data_nascita: str) -> str:
        """Genera un codice fiscale semplificato (solo per demo)."""
        # Versione semplificata - in produzione usare libreria specifica
        cf_base = f"{cognome[:3]}{nome[:3]}{data_nascita.replace('-', '')}"
        return cf_base.upper()
    
    def trova_alunno_per_nome(self, nome: str) -> List[AnagraficaAlunno]:
        """Trova alunni per nome."""
        risultati = []
        nome_lower = nome.lower()
        for alunno in self.alunni.values():
            if nome_lower in alunno.nome.lower() or nome_lower in alunno.cognome.lower():
                risultati.append(alunno)
        return risultati
    
    def alunni_per_classe(self, classe: str) -> List[AnagraficaAlunno]:
        """Ottiene alunni di una classe."""
        return [a for a in self.alunni.values() if a.classe == classe]
    
    # ============ GESTIONE PRESENZE ============
    
    def registra_presenza(self, studente_id: int, tipo: TipoPresenza,
                         data: Optional[str] = None, ora: Optional[str] = None,
                         motivo: str = "", docente: str = "") -> Presenza:
        """Registra presenza/assenza di uno studente.
        
        Args:
            studente_id: ID dello studente
            tipo: Tipo di presenza/assenza
            data: Data (default: oggi)
            ora: Ora per ritardi/entrate
            motivo: Motivo dell'assenza/ritardo
            docente: Docente che registra
            
        Returns:
            Presenza registrata
        """
        if data is None:
            data = datetime.now().strftime("%Y-%m-%d")
        
        if ora is None and tipo in [TipoPresenza.RITARDO, TipoPresenza.USCITA_ANTICIPATA]:
            ora = datetime.now().strftime("%H:%M")
        
        presenza = Presenza(
            id=self._prossimo_id_presenza,
            studente_id=studente_id,
            data=data,
            ora=ora,
            tipo=tipo,
            motivo=motivo,
            giustificato=False,
            docente_registrante=docente
        )
        
        self.presenze.append(presenza)
        self._prossimo_id_presenza += 1
        
        return presenza
    
    def presenze_studente(self, studente_id: int, data_inizio: Optional[str] = None,
                         data_fine: Optional[str] = None) -> List[Presenza]:
        """Ottiene presenze/assenze di uno studente in un periodo.
        
        Args:
            studente_id: ID dello studente
            data_inizio: Data inizio periodo (default: inizio anno)
            data_fine: Data fine periodo (default: oggi)
            
        Returns:
            Lista di presenze
        """
        if data_inizio is None:
            data_inizio = f"{datetime.now().year}-09-01"
        
        if data_fine is None:
            data_fine = datetime.now().strftime("%Y-%m-%d")
        
        presenze = [p for p in self.presenze 
                   if (p.studente_id == studente_id and 
                       data_inizio <= p.data <= data_fine)]
        
        presenze.sort(key=lambda x: x.data, reverse=True)
        return presenze
    
    def statistiche_presenze(self, classe: Optional[str] = None) -> Dict:
        """Calcola statistiche sulle presenze.
        
        Args:
            classe: Classe specifica (opzionale)
            
        Returns:
            Dizionario con statistiche
        """
        presenze_filtrate = self.presenze
        
        if classe:
            # Filtra per classe
            alunni_classe = [a.id for a in self.alunni.values() if a.classe == classe]
            presenze_filtrate = [p for p in self.presenze if p.studente_id in alunni_classe]
        
        if not presenze_filtrate:
            return {"messaggio": "Nessuna presenza registrata"}
        
        totali = len(presenze_filtrate)
        assenze = len([p for p in presenze_filtrate if p.tipo == TipoPresenza.ASSENTE])
        ritardi = len([p for p in presenze_filtrate if p.tipo == TipoPresenza.RITARDO])
        giustificate = len([p for p in presenze_filtrate if p.giustificato])
        non_giustificate = assenze - giustificate
        
        return {
            "totale_registrazioni": totali,
            "assenze": assenze,
            "percentuale_assenze": round((assenze / totali) * 100, 2) if totali > 0 else 0,
            "ritardi": ritardi,
            "percentuale_ritardi": round((ritardi / totali) * 100, 2) if totali > 0 else 0,
            "giustificate": giustificate,
            "non_giustificate": non_giustificate,
            "percentuale_giustificazioni": round((giustificate / assenze) * 100, 2) if assenze > 0 else 0
        }
    
    # ============ GESTIONE DOCUMENTI ============
    
    def aggiungi_documento(self, titolo: str, tipo: TipoDocumento,
                          destinatari: List[str], contenuto: str,
                          mittente: str = "Segreteria", protocollo: Optional[str] = None) -> DocumentoAmministrativo:
        """Aggiunge un documento amministrativo.
        
        Args:
            titolo: Titolo del documento
            tipo: Tipo di documento
            destinatari: Lista destinatari
            contenuto: Contenuto del documento
            mittente: Mittente
            protocollo: Numero protocollo
            
        Returns:
            DocumentoAmministrativo creato
        """
        if protocollo is None:
            protocollo = f"PROT-{datetime.now().strftime('%Y%m%d')}-{self._prossimo_id_documento:03d}"
        
        documento = DocumentoAmministrativo(
            id=self._prossimo_id_documento,
            titolo=titolo,
            tipo=tipo,
            data=datetime.now().strftime("%Y-%m-%d"),
            protocollo=protocollo,
            mittente=mittente,
            destinatari=destinatari,
            contenuto=contenuto
        )
        
        self.documenti.append(documento)
        self._prossimo_id_documento += 1
        
        return documento
    
    def get_documenti_recenti(self, limit: int = 10) -> List[DocumentoAmministrativo]:
        """Ottiene i documenti più recenti."""
        documenti_ordinati = sorted(self.documenti, key=lambda d: d.data, reverse=True)
        return documenti_ordinati[:limit]
    
    def statistiche_documenti(self) -> Dict:
        """Calcola statistiche sui documenti."""
        if not self.documenti:
            return {"messaggio": "Nessun documento disponibile"}
        
        per_tipo = {}
        for doc in self.documenti:
            tipo = doc.tipo.value
            per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
        
        # Documenti questo mese
        oggi = datetime.now()
        questo_mese = [d for d in self.documenti if d.data.startswith(oggi.strftime("%Y-%m"))]
        
        return {
            "totale": len(self.documenti),
            "per_tipo": per_tipo,
            "questo_mese": len(questo_mese),
            "firmati": len([d for d in self.documenti if d.data_firma])
        }
    
    # ============ METODI DI COLLEGAMENTO ============
    
    def collega_con_anagrafica(self, anagrafica_sistema):
        """Collega con il sistema di anagrafica esistente.
        
        Args:
            anagrafica_sistema: Istanza di Anagrafica da main.py
        """
        # Sincronizza alunni dal sistema esistente
        for studente in anagrafica_sistema.studenti:
            if studente.id not in self.alunni:
                # Genera dati completi
                alunno = AnagraficaAlunno(
                    id=studente.id,
                    nome=studente.nome,
                    cognome=studente.cognome,
                    data_nascita=f"{2005 + studente.id % 10}-03-15",
                    luogo_nascita="Città",
                    codice_fiscale=self._genera_codice_fiscale(studente.nome, studente.cognome, f"{2005 + studente.id % 10}-03-15"),
                    classe=studente.classe,
                    indirizzo="Via Example, 123",
                    telefono=f"+39 333 {studente.id:06d}"
                )
                self.alunni[studente.id] = alunno


if __name__ == "__main__":
    print("📋 TEST MODULO AMMINISTRATIVA SCHOOL")
    print("=" * 60 + "\n")
    
    # Crea sistema
    admin = AmministrativaSchool()
    
    # Aggiungi personale
    admin.personale_manager.aggiungi_persona(
        "Prof.ssa Bianchi", "docente", "Scienze", ["2A", "3B"], "+39 333 1234567"
    )
    admin.personale_manager.aggiungi_persona(
        "Prof. Rossi", "docente", "Matematica", ["2A", "2B"], "+39 333 7654321"
    )
    admin.personale_manager.aggiungi_persona(
        "Mario Segretario", "ATA", classi=[], telefono="+39 333 9999999"
    )
    
    # Aggiungi alunni
    alunno1 = admin.aggiungi_alunno(
        "Marco", "Verdi", "2011-03-15", "Milano", "2A",
        indirizzo="Via Roma 10", telefono="+39 333 1111111"
    )
    alunno2 = admin.aggiungi_alunno(
        "Sofia", "Rossi", "2010-06-20", "Roma", "2B",
        indirizzo="Via Milano 25", telefono="+39 333 2222222"
    )
    
    print(f"✅ Aggiunti {len(admin.alunni)} alunni")
    print(f"✅ Aggiunto {len(admin.personale_manager.personale)} nel personale")
    
    # Registra presenze
    admin.registra_presenza(alunno1.id, TipoPresenza.PRESENTE, docente="Prof.ssa Bianchi")
    admin.registra_presenza(alunno2.id, TipoPresenza.ASSENTE, motivo="febbre", docente="Prof.ssa Bianchi")
    admin.registra_presenza(alunno1.id, TipoPresenza.RITARDO, ora="08:30", motivo="traffico", docente="Prof. Rossi")
    
    print(f"✅ Registrate {len(admin.presenze)} presenze")
    
    # Aggiungi documento
    doc = admin.aggiungi_documento(
        "Circolare n.12 - Riunione genitori",
        TipoDocumento.CIRCOLARE,
        ["genitori", "docenti"],
        "Si comunica che è prevista una riunione con i genitori..."
    )
    print(f"✅ Creato documento: {doc.titolo}")
    
    # Statistiche
    print("\n📊 STATISTICHE PRESENZE:")
    stats = admin.statistiche_presenze()
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    print("\n✅ Modulo AmministrativaSchool funzionante!")

