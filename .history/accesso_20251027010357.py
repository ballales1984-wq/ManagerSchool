"""
Modulo per la gestione dell'accesso pubblico e privato.
Implementa controllo degli accessi basato su ruoli e permessi.
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Ruolo(Enum):
    """Ruoli nel sistema scolastico."""
    PUBBLICO = "Pubblico"
    STUDENTE = "Studente"
    INSEGNANTE = "Insegnante"
    DIRIGENTE = "Dirigente"
    AMMINISTRATORE = "Amministratore"


@dataclass
class Utente:
    """Rappresenta un utente del sistema."""
    username: str
    password: str
    ruolo: Ruolo
    nome_completo: str
    associato_id: Optional[int] = None  # ID studente o insegnante associato
    ultimo_accesso: Optional[datetime] = None
    attivo: bool = True
    
    def to_dict(self) -> Dict:
        """Converte l'utente in dizionario (senza password)."""
        return {
            "username": self.username,
            "ruolo": self.ruolo.value,
            "nome": self.nome_completo,
            "associato_id": self.associato_id,
            "ultimo_accesso": str(self.ultimo_accesso) if self.ultimo_accesso else None,
            "attivo": self.attivo
        }


class GestoreAccessi:
    """Gestisce gli accessi e le autorizzazioni nel sistema."""
    
    # Definizione dei permessi per ruolo
    PERMESSI: Dict[Ruolo, Set[str]] = {
        Ruolo.PUBBLICO: {
            "visualizza_statistiche_generali",
            "visualizza_graduatorie_pubbliche",
            "visualizza_orari_pubblici"
        },
        Ruolo.STUDENTE: {
            "visualizza_statistiche_generali",
            "visualizza_graduatorie_pubbliche",
            "visualizza_orari_pubblici",
            "visualizza_propri_voti",
            "visualizza_propria_pagella",
            "visualizza_propri_dati"
        },
        Ruolo.INSEGNANTE: {
            "visualizza_statistiche_generali",
            "visualizza_graduatorie_pubbliche",
            "visualizza_orari_pubblici",
            "visualizza_propri_voti",
            "visualizza_propria_pagella",
            "visualizza_propri_dati",
            "gestione_voti",
            "visualizza_studenti_classe",
            "visualizza_statistiche_classe",
            "modifica_orari_assegnati"
        },
        Ruolo.DIRIGENTE: {
            "visualizza_statistiche_generali",
            "visualizza_graduatorie_pubbliche",
            "visualizza_orari_pubblici",
            "visualizza_propri_voti",
            "visualizza_propria_pagella",
            "visualizza_propri_dati",
            "gestione_voti",
            "visualizza_studenti_classe",
            "visualizza_statistiche_classe",
            "modifica_orari_assegnati",
            "gestione_studenti",
            "gestione_insegnanti",
            "visualizza_report_completi",
            "genera_report_aggregati",
            "visualizza_indicatori_privati"
        },
        Ruolo.AMMINISTRATORE: {
            "visualizza_statistiche_generali",
            "visualizza_graduatorie_pubbliche",
            "visualizza_orari_pubblici",
            "visualizza_propri_voti",
            "visualizza_propria_pagella",
            "visualizza_propri_dati",
            "gestione_voti",
            "visualizza_studenti_classe",
            "visualizza_statistiche_classe",
            "modifica_orari_assegnati",
            "gestione_studenti",
            "gestione_insegnanti",
            "visualizza_report_completi",
            "genera_report_aggregati",
            "visualizza_indicatori_privati",
            "gestione_utenti",
            "gestione_permessi",
            "accesso_dati_completi",
            "modifica_configurazione"
        }
    }
    
    def __init__(self):
        """Inizializza il gestore degli accessi."""
        self.utenti: Dict[str, Utente] = {}
        self.sessione_corrente: Optional[Utente] = None
    
    def registra_utente(self, username: str, password: str, ruolo: Ruolo,
                       nome_completo: str, associato_id: Optional[int] = None) -> bool:
        """Registra un nuovo utente.
        
        Args:
            username: Nome utente
            password: Password
            ruolo: Ruolo dell'utente
            nome_completo: Nome completo
            associato_id: ID studente o insegnante associato
            
        Returns:
            True se registrato, False se username già esistente
        """
        if username in self.utenti:
            return False
        
        self.utenti[username] = Utente(
            username=username,
            password=password,  # In produzione, usare hashing!
            ruolo=ruolo,
            nome_completo=nome_completo,
            associato_id=associato_id
        )
        return True
    
    def autentica(self, username: str, password: str) -> bool:
        """Autentica un utente.
        
        Args:
            username: Nome utente
            password: Password
            
        Returns:
            True se autenticato, False altrimenti
        """
        if username not in self.utenti:
            return False
        
        utente = self.utenti[username]
        
        if not utente.attivo:
            return False
        
        if utente.password != password:
            return False
        
        # Aggiorna ultimo accesso
        utente.ultimo_accesso = datetime.now()
        self.sessione_corrente = utente
        return True
    
    def disconnetti(self) -> None:
        """Disconnette l'utente corrente."""
        self.sessione_corrente = None
    
    def verifica_permesso(self, permesso: str) -> bool:
        """Verifica se l'utente corrente ha un permesso.
        
        Args:
            permesso: Nome del permesso da verificare
            
        Returns:
            True se ha il permesso, False altrimenti
        """
        if not self.sessione_corrente:
            return False
        
        return permesso in self.PERMESSI.get(self.sessione_corrente.ruolo, set())
    
    def get_utente_corrente(self) -> Optional[Utente]:
        """Restituisce l'utente corrente."""
        return self.sessione_corrente
    
    def get_ruolo_corrente(self) -> Optional[Ruolo]:
        """Restituisce il ruolo dell'utente corrente."""
        if self.sessione_corrente:
            return self.sessione_corrente.ruolo
        return None
    
    def lista_utenti(self) -> List[Dict]:
        """Restituisce la lista degli utenti registrati (senza password)."""
        return [u.to_dict() for u in self.utenti.values()]
    
    def modifica_utente(self, username: str, attivo: Optional[bool] = None,
                       ruolo: Optional[Ruolo] = None) -> bool:
        """Modifica le informazioni di un utente.
        
        Args:
            username: Nome utente da modificare
            attivo: Nuovo stato attivo (None per non modificare)
            ruolo: Nuovo ruolo (None per non modificare)
            
        Returns:
            True se modificato, False se non trovato
        """
        if username not in self.utenti:
            return False
        
        utente = self.utenti[username]
        
        if attivo is not None:
            utente.attivo = attivo
        
        if ruolo is not None:
            utente.ruolo = ruolo
        
        return True
    
    def rimuovi_utente(self, username: str) -> bool:
        """Rimuove un utente dal sistema.
        
        Args:
            username: Nome utente da rimuovere
            
        Returns:
            True se rimosso, False se non trovato
        """
        if username not in self.utenti:
            return False
        
        del self.utenti[username]
        return True
    
    def statistiche_accessi(self) -> Dict:
        """Calcola statistiche sugli accessi.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.utenti:
            return {"messaggio": "Nessun utente registrato"}
        
        ruoli_conteggio = {}
        attivi = 0
        
        for utente in self.utenti.values():
            ruolo = utente.ruolo.value
            ruoli_conteggio[ruolo] = ruoli_conteggio.get(ruolo, 0) + 1
            
            if utente.attivo:
                attivi += 1
        
        return {
            "totale_utenti": len(self.utenti),
            "utenti_attivi": attivi,
            "utenti_disattivi": len(self.utenti) - attivi,
            "distribuzione_ruoli": ruoli_conteggio,
            "utente_corrente": self.sessione_corrente.username if self.sessione_corrente else None
        }


class VistaPubblica:
    """Implementa le viste pubbliche del sistema."""
    
    @staticmethod
    def visualizza_statistiche_generali(anagrafica, gestione_voti) -> Dict:
        """Restituisce statistiche generali pubbliche.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
            
        Returns:
            Dizionario con statistiche pubbliche
        """
        return {
            "totale_studenti": len(anagrafica.studenti),
            "totale_classi": len(set(s.classe for s in anagrafica.studenti)),
            "media_generale": round(gestione_voti.statistiche_generali().get("media_generale", 0), 2)
        }
    
    @staticmethod
    def visualizza_graduatorie_pubbliche(analisi_didattica, limit: int = 10) -> List[Dict]:
        """Restituisce una graduatoria pubblica (top studenti).
        
        Args:
            analisi_didattica: Istanza di AnalisiDidattica
            limit: Numero di studenti da mostrare
            
        Returns:
            Lista con top studenti
        """
        graduatoria = analisi_didattica.graduatoria_studenti()[:limit]
        
        # Restituisci solo nome e posizione (senza voti specifici per privacy)
        return [
            {
                "posizione": s["posizione"],
                "nome": s["nome"].split()[0]  # Solo nome, senza cognome
            }
            for s in graduatoria
        ]


class VistaPrivata:
    """Implementa le viste private del sistema."""
    
    @staticmethod
    def visualizza_dati_completi(gestore_accessi, anagrafica, gestione_voti,
                                 gestione_insegnanti, studente_id: Optional[int] = None) -> Dict:
        """Restituisce dati completi per utente autenticato.
        
        Args:
            gestore_accessi: Istanza di GestoreAccessi
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
            gestione_insegnanti: Istanza di GestioneInsegnanti
            studente_id: ID studente (opzionale, usa ID utente se None)
            
        Returns:
            Dizionario con dati completi
        """
        utente = gestore_accessi.get_utente_corrente()
        if not utente:
            return {"errore": "Utente non autenticato"}
        
        # Solo amministratori possono vedere dati di altri
        if studente_id and utente.ruolo != Ruolo.AMMINISTRATORE:
            return {"errore": "Permesso negato"}
        
        # Se non specificato, usa ID associato
        if studente_id is None:
            studente_id = utente.associato_id
        
        if not studente_id:
            return {"errore": "ID studente non disponibile"}
        
        studente = anagrafica.trova_studente(studente_id)
        if not studente:
            return {"errore": "Studente non trovato"}
        
        return {
            "studente": studente.to_dict(),
            "voti": gestione_voti.voti_studente(studente_id),
            "pagella": gestione_voti.pagella_studente(studente_id),
            "media": gestione_voti.media_studente(studente_id)
        }
