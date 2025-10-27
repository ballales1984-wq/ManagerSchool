"""
Modulo per la gestione dei voti.
Gestisce voti provvisori, pagelle e calcolo medie.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import dati


@dataclass
class Voto:
    """Rappresenta un voto assegnato a uno studente."""
    
    id_studente: int
    materia: str
    voto: float
    tipo: str  # 'Prova scritta', 'Prova orale', 'Comportamento', ecc.
    data: str
    note: str = ""
    
    def __post_init__(self):
        """Valida che il voto sia in un range valido."""
        if self.voto < 3.0 or self.voto > 10.0:
            raise ValueError(f"Voto deve essere tra 3.0 e 10.0, ricevuto: {self.voto}")


@dataclass
class Pagella:
    """Rappresenta la pagella di uno studente."""
    
    id_studente: int
    quadrimestre: int  # 1 o 2
    voti_materie: Dict[str, float]  # Materia -> voto finale
    media_generale: float
    comportamento: float
    assenze: int
    note: str = ""
    
    def __post_init__(self):
        """Calcola la media se non fornita."""
        if not self.voti_materie:
            self.media_generale = 0.0
        else:
            voti = list(self.voti_materie.values())
            self.media_generale = sum(voti) / len(voti)


class GestioneVoti:
    """Gestisce i voti degli studenti."""
    
    def __init__(self):
        """Inizializza la gestione voti."""
        self.voti: List[Voto] = []
        self.pagelle: List[Pagella] = []
    
    def aggiungi_voto(self, id_studente: int, materia: str, voto: float, 
                     tipo: str = "Prova scritta", data: str = None, 
                     note: str = "") -> Voto:
        """Aggiunge un voto per uno studente.
        
        Args:
            id_studente: ID dello studente
            materia: Materia del voto
            voto: Valore del voto (3.0-10.0)
            tipo: Tipo di valutazione
            data: Data del voto (se None, usa oggi)
            note: Note aggiuntive
            
        Returns:
            Voto creato
        """
        if data is None:
            data = datetime.now().strftime("%Y-%m-%d")
        
        voto_obj = Voto(
            id_studente=id_studente,
            materia=materia,
            voto=voto,
            tipo=tipo,
            data=data,
            note=note
        )
        
        self.voti.append(voto_obj)
        return voto_obj
    
    def aggiungi_voto_casuale(self, id_studente: int, materia: str, 
                              base: float = 6.0) -> Voto:
        """Aggiunge un voto casuale per uno studente.
        
        Args:
            id_studente: ID dello studente
            materia: Materia del voto
            base: Voto base per la generazione
            
        Returns:
            Voto creato
        """
        voto = dati.voto_casuale(base)
        tipo = dati.booleano(0.7) and "Prova scritta" or "Prova orale"
        
        return self.aggiungi_voto(id_studente, materia, voto, tipo)
    
    def voti_studente(self, id_studente: int, materia: Optional[str] = None) -> List[Voto]:
        """Ottiene i voti di uno studente.
        
        Args:
            id_studente: ID dello studente
            materia: Materia specifica (opzionale)
            
        Returns:
            Lista di voti
        """
        if materia:
            return [v for v in self.voti 
                   if v.id_studente == id_studente and v.materia == materia]
        return [v for v in self.voti if v.id_studente == id_studente]
    
    def media_studente(self, id_studente: int, materia: Optional[str] = None) -> float:
        """Calcola la media di uno studente.
        
        Args:
            id_studente: ID dello studente
            materia: Materia specifica (opzionale)
            
        Returns:
            Media aritmetica
        """
        voti_studente = self.voti_studente(id_studente, materia)
        
        if not voti_studente:
            return 0.0
        
        return sum(v.voto for v in voti_studente) / len(voti_studente)
    
    def medie_per_materia(self, id_studente: int) -> Dict[str, float]:
        """Ottiene le medie di uno studente per ogni materia.
        
        Args:
            id_studente: ID dello studente
            
        Returns:
            Dizionario Materia -> media
        """
        materie = set(v.materia for v in self.voti if v.id_studente == id_studente)
        return {materia: self.media_studente(id_studente, materia) for materia in materie}
    
    def crea_pagella(self, id_studente: int, quadrimestre: int, 
                    assenze: int = 0, comportamento: float = 8.0, 
                    note: str = "") -> Pagella:
        """Crea una pagella per uno studente.
        
        Args:
            id_studente: ID dello studente
            quadrimestre: Quadrimestre (1 o 2)
            assenze: Numero di assenze
            comportamento: Voto di comportamento
            note: Note generali
            
        Returns:
            Pagella creata
        """
        voti_materie = self.medie_per_materia(id_studente)
        
        pagella = Pagella(
            id_studente=id_studente,
            quadrimestre=quadrimestre,
            voti_materie=voti_materie,
            media_generale=0.0,  # Sarà calcolata automaticamente
            comportamento=comportamento,
            assenze=assenze,
            note=note
        )
        
        self.pagelle.append(pagella)
        return pagella
    
    def pagella_studente(self, id_studente: int, quadrimestre: int = 1) -> Optional[Pagella]:
        """Trova la pagella di uno studente.
        
        Args:
            id_studente: ID dello studente
            quadrimestre: Quadrimestre
            
        Returns:
            Pagella trovata o None
        """
        for pagella in self.pagelle:
            if pagella.id_studente == id_studente and pagella.quadrimestre == quadrimestre:
                return pagella
        return None
    
    def rimuovi_voto(self, voto: Voto) -> bool:
        """Rimuove un voto.
        
        Args:
            voto: Voto da rimuovere
            
        Returns:
            True se rimosso, False se non trovato
        """
        if voto in self.voti:
            self.voti.remove(voto)
            return True
        return False
    
    def statistiche_materia(self, materia: str) -> Dict:
        """Calcola statistiche per una materia.
        
        Args:
            materia: Nome della materia
            
        Returns:
            Dizionario con statistiche
        """
        voti_materia = [v.voto for v in self.voti if v.materia == materia]
        
        if not voti_materia:
            return {"messaggio": f"Nessun voto per {materia}"}
        
        return {
            "materia": materia,
            "numero_voti": len(voti_materia),
            "media": sum(voti_materia) / len(voti_materia),
            "min": min(voti_materia),
            "max": max(voti_materia)
        }
    
    def statistiche_generali(self) -> Dict:
        """Calcola statistiche generali sui voti.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.voti:
            return {"messaggio": "Nessun voto registrato"}
        
        tutti_i_voti = [v.voto for v in self.voti]
        
        # Distribuzione per fascia
        eccellenti = sum(1 for v in tutti_i_voti if v >= 9.0)
        buoni = sum(1 for v in tutti_i_voti if 7.5 <= v < 9.0)
        sufficienti = sum(1 for v in tutti_i_voti if 6.0 <= v < 7.5)
        insufficienti = sum(1 for v in tutti_i_voti if v < 6.0)
        
        return {
            "totale_voti": len(self.voti),
            "voto_medio": sum(tutti_i_voti) / len(tutti_i_voti),
            "voto_min": min(tutti_i_voti),
            "voto_max": max(tutti_i_voti),
            "distribuzione": {
                "Eccellenti (>= 9.0)": eccellenti,
                "Buoni (7.5-8.9)": buoni,
                "Sufficienti (6.0-7.4)": sufficienti,
                "Insufficienti (< 6.0)": insufficienti
            }
        }
    
    def __len__(self) -> int:
        """Restituisce il numero di voti."""
        return len(self.voti)
    
    def __repr__(self) -> str:
        """Rappresentazione stringa."""
        return f"GestioneVoti({len(self.voti)} voti, {len(self.pagelle)} pagelle)"
