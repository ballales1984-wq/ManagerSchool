"""
Modulo per la gestione degli orari settimanali.
Gestisce la distribuzione delle lezioni e degli insegnanti.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import dati


@dataclass
class Lezione:
    """Rappresenta una lezione nell'orario."""
    
    giorno: str
    ora: int  # Ora di inizio (8-14)
    materia: str
    id_insegnante: int
    classe: str


class GestioneOrari:
    """Gestisce gli orari settimanali."""
    
    def __init__(self):
        """Inizializza la gestione orari."""
        self.orario: List[Lezione] = []
        self.giorni_settimana = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        self.ore_giornaliere = [8, 9, 10, 11, 13, 14]  # Esclusa pausa pranzo
    
    def aggiungi_lezione(self, classe: str, giorno: str, ora: int, 
                        materia: str, id_insegnante: int) -> Lezione:
        """Aggiunge una lezione all'orario.
        
        Args:
            classe: Classe che segue la lezione
            giorno: Giorno della settimana
            ora: Ora di inizio
            materia: Materia insegnata
            id_insegnante: ID dell'insegnante
            
        Returns:
            Lezione creata
        """
        lezione = Lezione(
            giorno=giorno,
            ora=ora,
            materia=materia,
            id_insegnante=id_insegnante,
            classe=classe
        )
        
        self.orario.append(lezione)
        return lezione
    
    def orario_classe(self, classe: str) -> List[Lezione]:
        """Ottiene l'orario di una classe.
        
        Args:
            classe: Nome della classe
            
        Returns:
            Lista di lezioni della classe
        """
        return [l for l in self.orario if l.classe == classe]
    
    def orario_insegnante(self, id_insegnante: int) -> List[Lezione]:
        """Ottiene l'orario di un insegnante.
        
        Args:
            id_insegnante: ID dell'insegnante
            
        Returns:
            Lista di lezioni dell'insegnante
        """
        return [l for l in self.orario if l.id_insegnante == id_insegnante]
    
    def orario_materia(self, classe: str, materia: str) -> List[Lezione]:
        """Ottiene le lezioni di una materia per una classe.
        
        Args:
            classe: Nome della classe
            materia: Nome della materia
            
        Returns:
            Lista di lezioni
        """
        return [l for l in self.orario if l.classe == classe and l.materia == materia]
    
    def ore_settimanali_materia(self, classe: str, materia: str) -> int:
        """Conta le ore settimanali di una materia per una classe.
        
        Args:
            classe: Nome della classe
            materia: Nome della materia
            
        Returns:
            Numero di ore settimanali
        """
        return len(self.orario_materia(classe, materia))
    
    def conflitti_insegnante(self, id_insegnante: int) -> List[List[Lezione]]:
        """Trova conflitti temporali per un insegnante.
        
        Args:
            id_insegnante: ID dell'insegnante
            
        Returns:
            Lista di conflitti (liste di lezioni sovrapposte)
        """
        lezioni = self.orario_insegnante(id_insegnante)
        conflitti = []
        
        # Verifica sovrapposizioni
        for i, lez1 in enumerate(lezioni):
            conflitto = [lez1]
            for lez2 in lezioni[i+1:]:
                if lez1.giorno == lez2.giorno and lez1.ora == lez2.ora:
                    if lez2 not in conflitto:
                        conflitto.append(lez2)
            
            if len(conflitto) > 1:
                if conflitto not in conflitti:
                    conflitti.append(conflitto)
        
        return conflitti
    
    def carico_orario_insegnante(self, id_insegnante: int) -> int:
        """Calcola il carico orario settimanale di un insegnante.
        
        Args:
            id_insegnante: ID dell'insegnante
            
        Returns:
            Numero di ore settimanali
        """
        return len(self.orario_insegnante(id_insegnante))
    
    def statistiche_orario(self) -> Dict:
        """Calcola statistiche generali sull'orario.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.orario:
            return {"messaggio": "Nessuna lezione programmata"}
        
        # Ore per giorno
        ore_per_giorno = {}
        for giorno in self.giorni_settimana:
            ore_per_giorno[giorno] = sum(1 for l in self.orario if l.giorno == giorno)
        
        # Ore per materia (in media)
        materie = set(l.materia for l in self.orario)
        ore_per_materia = {mat: sum(1 for l in self.orario if l.materia == mat) 
                          for mat in materie}
        
        return {
            "totale_lezioni": len(self.orario),
            "ore_per_giorno": ore_per_giorno,
            "ore_per_materia": ore_per_materia,
            "numero_materie": len(materie)
        }
    
    def __len__(self) -> int:
        """Restituisce il numero di lezioni."""
        return len(self.orario)
    
    def __repr__(self) -> str:
        """Rappresentazione stringa."""
        return f"GestioneOrari({len(self.orario)} lezioni)"


# Gestione semplificata - potrebbe essere estesa con generazione automatica orari
class GeneratoreOrari:
    """Genera orari automaticamente."""
    
    @staticmethod
    def genera_orario_classe(gestione_orari: GestioneOrari, classe: str,
                            materie: Dict[str, int]) -> None:
        """Genera un orario per una classe.
        
        Args:
            gestione_orari: Istanza di GestioneOrari
            classe: Nome della classe
            materie: Dizionario Materia -> ore settimanali
        """
        giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        
        for materia, ore_settimanali in materie.items():
            for _ in range(ore_settimanali):
                giorno = dati.giorno_settimana()
                ora = dati.ora_lezione()[0]
                # In una implementazione completa, qui dovrebbe esserci
                # l'assegnazione dell'insegnante
                pass
