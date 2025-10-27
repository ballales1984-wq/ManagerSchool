"""
Modulo per la gestione dell'anagrafica studenti.
Gestisce dati personali, reddito, salute e situazione familiare.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
import dati
from dati import CategoriaReddito, CondizioneSalute


@dataclass
class Studente:
    """Rappresenta uno studente nel sistema."""
    
    id: int
    nome: str
    cognome: str
    eta: int
    classe: str
    reddito_familiare: int
    categoria_reddito: CategoriaReddito
    condizione_salute: CondizioneSalute
    situazione_familiare: str
    note: str = ""
    
    @property
    def nome_completo(self) -> str:
        """Restituisce il nome completo dello studente."""
        return f"{self.nome} {self.cognome}"
    
    @property
    def fragilità_sociale(self) -> float:
        """Calcola un indice di fragilità sociale (0-100).
        
        Considera reddito, salute e situazione familiare.
        """
        fragilita = 0.0
        
        # Contributo reddito (0-40 punti)
        if self.categoria_reddito == CategoriaReddito.MOLTO_BASSO:
            fragilita += 40
        elif self.categoria_reddito == CategoriaReddito.BASSO:
            fragilita += 30
        elif self.categoria_reddito == CategoriaReddito.MEDIO:
            fragilita += 15
        elif self.categoria_reddito == CategoriaReddito.ALTO:
            fragilita += 5
        
        # Contributo salute (0-30 punti)
        if self.condizione_salute == CondizioneSalute.ECCELLENTE:
            fragilita += 0
        elif self.condizione_salute == CondizioneSalute.BUONA:
            fragilita += 5
        elif self.condizione_salute == CondizioneSalute.DISCRETA:
            fragilita += 10
        elif self.condizione_salute == CondizioneSalute.PROBLEMATICA:
            fragilita += 20
        elif self.condizione_salute == CondizioneSalute.CRITICA:
            fragilita += 30
        
        # Contributo situazione familiare (0-30 punti)
        if self.situazione_familiare == "Nucleo tradizionale":
            fragilita += 0
        elif self.situazione_familiare == "Allargata":
            fragilita += 5
        elif self.situazione_familiare in ["Monoparentale", "Genitori separati"]:
            fragilita += 15
        elif self.situazione_familiare == "Affidamento":
            fragilita += 30
        
        return min(100.0, round(fragilita, 1))
    
    def to_dict(self) -> Dict:
        """Converte lo studente in dizionario."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cognome": self.cognome,
            "nome_completo": self.nome_completo,
            "eta": self.eta,
            "classe": self.classe,
            "reddito": self.reddito_familiare,
            "categoria_reddito": self.categoria_reddito.name,
            "salute": self.condizione_salute.value,
            "famiglia": self.situazione_familiare,
            "fragilita": self.fragilità_sociale,
            "note": self.note
        }


class Anagrafica:
    """Gestisce l'anagrafica degli studenti."""
    
    def __init__(self):
        """Inizializza l'anagrafica."""
        self.studenti: List[Studente] = []
        self._prossimo_id = 1
    
    def aggiungi_studente(self, studente: Studente) -> None:
        """Aggiunge uno studente all'anagrafica."""
        if studente.id == 0:
            studente.id = self._prossimo_id
            self._prossimo_id += 1
        
        self.studenti.append(studente)
    
    def crea_studente_casuale(self, classe: Optional[str] = None) -> Studente:
        """Crea uno studente con dati casuali.
        
        Args:
            classe: Classe dello studente (se None, generata casualmente)
            
        Returns:
            Studente creato
        """
        reddito = dati.reddito_familiare()
        
        studente = Studente(
            id=0,  # Sarà assegnato automaticamente
            nome=dati.nome_casuale(),
            cognome=dati.cognome_casuale(),
            eta=dati.eta_casuale(),
            classe=classe if classe else dati.classe_casuale(),
            reddito_familiare=reddito,
            categoria_reddito=dati.categoria_reddito(reddito),
            condizione_salute=dati.condizione_salute(),
            situazione_familiare=dati.situazione_familiare()
        )
        
        self.aggiungi_studente(studente)
        return studente
    
    def genera_studenti(self, numero: int, classe: Optional[str] = None) -> List[Studente]:
        """Genera più studenti casuali.
        
        Args:
            numero: Numero di studenti da generare
            classe: Classe degli studenti (se None, generata casualmente per ciascuno)
            
        Returns:
            Lista di studenti creati
        """
        studenti_creati = []
        for _ in range(numero):
            studente = self.crea_studente_casuale(classe)
            studenti_creati.append(studente)
        return studenti_creati
    
    def trova_studente(self, id: int) -> Optional[Studente]:
        """Trova uno studente per ID.
        
        Args:
            id: ID dello studente
            
        Returns:
            Studente trovato o None
        """
        for studente in self.studenti:
            if studente.id == id:
                return studente
        return None
    
    def trova_per_nome(self, nome_cercato: str) -> List[Studente]:
        """Trova studenti per nome o cognome.
        
        Args:
            nome_cercato: Nome o parte di nome da cercare (case insensitive)
            
        Returns:
            Lista di studenti trovati
        """
        nome_cercato = nome_cercato.lower()
        return [
            s for s in self.studenti
            if nome_cercato in s.nome.lower() or nome_cercato in s.cognome.lower()
        ]
    
    def studenti_per_classe(self, classe: str) -> List[Studente]:
        """Ottiene tutti gli studenti di una classe.
        
        Args:
            classe: Nome della classe
            
        Returns:
            Lista di studenti della classe
        """
        return [s for s in self.studenti if s.classe == classe]
    
    def studenti_per_fragilita(self, min_fragilita: float = 0, 
                                max_fragilita: float = 100) -> List[Studente]:
        """Ottiene studenti in un range di fragilità sociale.
        
        Args:
            min_fragilita: Fragilità minima
            max_fragilita: Fragilità massima
            
        Returns:
            Lista di studenti nel range
        """
        return [
            s for s in self.studenti
            if min_fragilita <= s.fragilità_sociale <= max_fragilita
        ]
    
    def statistica_fragilita(self) -> Dict:
        """Calcola statistiche sulla fragilità sociale.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.studenti:
            return {
                "totale": 0,
                "media": 0,
                "min": 0,
                "max": 0,
                "alta_fragilita": 0,
                "media_fragilita": 0,
                "bassa_fragilita": 0
            }
        
        fragilita = [s.fragilità_sociale for s in self.studenti]
        
        alta_fragilita = sum(1 for f in fragilita if f >= 60)
        media_fragilita = sum(1 for f in fragilita if 30 <= f < 60)
        bassa_fragilita = sum(1 for f in fragilita if f < 30)
        
        return {
            "totale": len(self.studenti),
            "media": round(sum(fragilita) / len(fragilita), 2),
            "min": min(fragilita),
            "max": max(fragilita),
            "alta_fragilita": alta_fragilita,
            "percentuale_alta": round((alta_fragilita / len(self.studenti)) * 100, 1),
            "media_fragilita": media_fragilita,
            "percentuale_media": round((media_fragilita / len(self.studenti)) * 100, 1),
            "bassa_fragilita": bassa_fragilita,
            "percentuale_bassa": round((bassa_fragilita / len(self.studenti)) * 100, 1)
        }
    
    def rimuovi_studente(self, id: int) -> bool:
        """Rimuove uno studente dall'anagrafica.
        
        Args:
            id: ID dello studente da rimuovere
            
        Returns:
            True se rimosso, False se non trovato
        """
        studente = self.trova_studente(id)
        if studente:
            self.studenti.remove(studente)
            return True
        return False
    
    def statistiche_generali(self) -> Dict:
        """Calcola statistiche generali sull'anagrafica.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.studenti:
            return {"messaggio": "Nessuno studente registrato"}
        
        # Raggruppa per classe
        classi = {}
        for studente in self.studenti:
            if studente.classe not in classi:
                classi[studente.classe] = 0
            classi[studente.classe] += 1
        
        # Redditi
        redditi = [s.reddito_familiare for s in self.studenti]
        
        # Condizioni di salute
        condizioni_salute = {}
        for studente in self.studenti:
            condizione = studente.condizione_salute.value
            condizioni_salute[condizione] = condizioni_salute.get(condizione, 0) + 1
        
        return {
            "totale_studenti": len(self.studenti),
            "classi": classi,
            "numero_classi": len(classi),
            "reddito_medio": int(sum(redditi) / len(redditi)),
            "reddito_min": min(redditi),
            "reddito_max": max(redditi),
            "condizioni_salute": condizioni_salute,
            "statistica_fragilita": self.statistica_fragilita()
        }
    
    def to_lista_dict(self) -> List[Dict]:
        """Converte tutti gli studenti in una lista di dizionari."""
        return [s.to_dict() for s in self.studenti]
    
    def __len__(self) -> int:
        """Restituisce il numero di studenti."""
        return len(self.studenti)
    
    def __repr__(self) -> str:
        """Rappresentazione stringa dell'anagrafica."""
        return f"Anagrafica({len(self.studenti)} studenti)"
