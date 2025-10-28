"""
Modulo per la gestione degli insegnanti.
Gestisce professori, materie e ore settimanali.
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
import dati


@dataclass
class Insegnante:
    """Rappresenta un insegnante nel sistema."""
    
    id: int
    nome: str
    cognome: str
    eta: int
    materie: List[str]  # Lista di materie insegnate
    ore_settimanali: Dict[str, int]  # Materia -> ore settimanali
    anni_esperienza: int
    sezioni_assegnate: List[str] = None  # Sezioni dove insegna (es. ["A", "B"])
    note: str = ""
    
    def __post_init__(self):
        """Inizializza il dizionario ore_settimanali e sezioni_assegnate se non forniti."""
        if not self.ore_settimanali:
            self.ore_settimanali = {mat: dati.orario_settimanale_materia() for mat in self.materie}
        if self.sezioni_assegnate is None:
            self.sezioni_assegnate = []
    
    @property
    def nome_completo(self) -> str:
        """Restituisce il nome completo dell'insegnante."""
        return f"{self.nome} {self.cognome}"
    
    @property
    def totale_ore_settimanali(self) -> int:
        """Calcola il totale delle ore settimanali."""
        return sum(self.ore_settimanali.values())
    
    @property
    def materia_principale(self) -> str:
        """Restituisce la materia con più ore."""
        if not self.ore_settimanali:
            return ""
        return max(self.ore_settimanali.items(), key=lambda x: x[1])[0]
    
    @property
    def carico_lavoro(self) -> str:
        """Determina il carico di lavoro dell'insegnante.
        
        Returns:
            'Leggero', 'Normale', 'Pesante' o 'Molto Pesante'
        """
        ore = self.totale_ore_settimanali
        if ore <= 10:
            return "Leggero"
        elif ore <= 16:
            return "Normale"
        elif ore <= 22:
            return "Pesante"
        else:
            return "Molto Pesante"
    
    def insegna_materia(self, materia: str) -> bool:
        """Verifica se l'insegnante insegna una materia.
        
        Args:
            materia: Nome della materia
            
        Returns:
            True se insegna la materia, False altrimenti
        """
        return materia in self.materie
    
    def aggiungi_materia(self, materia: str, ore: int) -> None:
        """Aggiunge una materia all'insegnante.
        
        Args:
            materia: Nome della materia
            ore: Ore settimanali per la materia
        """
        if materia not in self.materie:
            self.materie.append(materia)
            self.ore_settimanali[materia] = ore
    
    def rimuovi_materia(self, materia: str) -> bool:
        """Rimuove una materia dall'insegnante.
        
        Args:
            materia: Nome della materia da rimuovere
            
        Returns:
            True se rimossa, False se non trovata
        """
        if materia in self.materie:
            self.materie.remove(materia)
            if materia in self.ore_settimanali:
                del self.ore_settimanali[materia]
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Converte l'insegnante in dizionario."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cognome": self.cognome,
            "nome_completo": self.nome_completo,
            "eta": self.eta,
            "materie": self.materie,
            "ore_settimanali": self.ore_settimanali,
            "totale_ore": self.totale_ore_settimanali,
            "carico_lavoro": self.carico_lavoro,
            "anni_esperienza": self.anni_esperienza,
            "sezioni_assegnate": self.sezioni_assegnate,
            "note": self.note
        }


class GestioneInsegnanti:
    """Gestisce gli insegnanti della scuola."""
    
    def __init__(self):
        """Inizializza la gestione insegnanti."""
        self.insegnanti: List[Insegnante] = []
        self._prossimo_id = 1
    
    def aggiungi_insegnante(self, insegnante: Insegnante) -> None:
        """Aggiunge un insegnante.
        
        Args:
            insegnante: Insegnante da aggiungere
        """
        if insegnante.id == 0:
            insegnante.id = self._prossimo_id
            self._prossimo_id += 1
        
        self.insegnanti.append(insegnante)
    
    def crea_insegnante_casuale(self, numero_materie: int = 2) -> Insegnante:
        """Crea un insegnante con dati casuali.
        
        Args:
            numero_materie: Numero di materie che insegna (default: 2)
            
        Returns:
            Insegnante creato
        """
        materie = dati.materie_casuali(numero_materie)
        ore_settimanali = {
            materia: dati.orario_settimanale_materia() 
            for materia in materie
        }
        
        insegnante = Insegnante(
            id=0,  # Sarà assegnato automaticamente
            nome=dati.nome_casuale(),
            cognome=dati.cognome_casuale(),
            eta=random.randint(30, 65),
            materie=materie,
            ore_settimanali=ore_settimanali,
            anni_esperienza=random.randint(0, 35)
        )
        
        self.aggiungi_insegnante(insegnante)
        return insegnante
    
    def genera_insegnanti(self, numero: int, numero_materie: int = 2) -> List[Insegnante]:
        """Genera più insegnanti casuali.
        
        Args:
            numero: Numero di insegnanti da generare
            numero_materie: Numero medio di materie per insegnante
            
        Returns:
            Lista di insegnanti creati
        """
        insegnanti_creati = []
        for _ in range(numero):
            insegnante = self.crea_insegnante_casuale(numero_materie)
            insegnanti_creati.append(insegnante)
        return insegnanti_creati
    
    def genera_insegnanti_per_materia(self) -> List[Insegnante]:
        """Genera insegnanti specifici per materia con assegnazioni alle sezioni.
        
        Crea due squadre di insegnanti:
        - Squadra 1: Sezioni A e B
        - Squadra 2: Sezioni C e D
        
        Ogni squadra ha un insegnante per ciascuna materia.
        
        Returns:
            Lista di 12 insegnanti creati (6 per squadra)
        """
        materie = ["Matematica", "Italiano", "Inglese", "Storia", "Educazione Fisica", "Religione"]
        
        # Nomi specifici per gli insegnanti
        nomi_squadra_ab = [
            ("Mario", "Rossi"),      # Matematica
            ("Laura", "Bianchi"),    # Italiano  
            ("James", "Wilson"),     # Inglese
            ("Giuseppe", "Verdi"),   # Storia
            ("Luca", "Sportivo"),    # Educazione Fisica
            ("Maria", "Santini")     # Religione
        ]
        
        nomi_squadra_cd = [
            ("Anna", "Fibonacci"),   # Matematica
            ("Paolo", "Manzoni"),    # Italiano
            ("Emma", "Smith"),       # Inglese
            ("Carlo", "Storici"),    # Storia
            ("Marco", "Atletico"),   # Educazione Fisica
            ("Sofia", "Benedetti")   # Religione
        ]
        
        insegnanti_creati = []
        
        # Crea squadra A-B
        for i, (nome, cognome) in enumerate(nomi_squadra_ab):
            materia = materie[i]
            
            # Ore specifiche per materia
            ore_materia = {
                "Matematica": 5,
                "Italiano": 5, 
                "Inglese": 3,
                "Storia": 3,
                "Educazione Fisica": 2,
                "Religione": 1
            }
            
            insegnante = Insegnante(
                id=0,  # Sarà assegnato automaticamente
                nome=nome,
                cognome=cognome,
                eta=random.randint(28, 55),
                materie=[materia],
                ore_settimanali={materia: ore_materia[materia]},
                anni_esperienza=random.randint(2, 25),
                sezioni_assegnate=["A", "B"],
                note=f"Responsabile {materia} - Sezioni A/B"
            )
            
            self.aggiungi_insegnante(insegnante)
            insegnanti_creati.append(insegnante)
        
        # Crea squadra C-D
        for i, (nome, cognome) in enumerate(nomi_squadra_cd):
            materia = materie[i]
            
            # Ore specifiche per materia
            ore_materia = {
                "Matematica": 5,
                "Italiano": 5,
                "Inglese": 3, 
                "Storia": 3,
                "Educazione Fisica": 2,
                "Religione": 1
            }
            
            insegnante = Insegnante(
                id=0,  # Sarà assegnato automaticamente
                nome=nome,
                cognome=cognome,
                eta=random.randint(28, 55),
                materie=[materia],
                ore_settimanali={materia: ore_materia[materia]},
                anni_esperienza=random.randint(2, 25),
                sezioni_assegnate=["C", "D"],
                note=f"Responsabile {materia} - Sezioni C/D"
            )
            
            self.aggiungi_insegnante(insegnante)
            insegnanti_creati.append(insegnante)
        
        return insegnanti_creati
    
    def trova_insegnante(self, id: int) -> Optional[Insegnante]:
        """Trova un insegnante per ID.
        
        Args:
            id: ID dell'insegnante
            
        Returns:
            Insegnante trovato o None
        """
        for insegnante in self.insegnanti:
            if insegnante.id == id:
                return insegnante
        return None
    
    def trova_per_nome(self, nome_cercato: str) -> List[Insegnante]:
        """Trova insegnanti per nome o cognome.
        
        Args:
            nome_cercato: Nome o parte di nome da cercare
            
        Returns:
            Lista di insegnanti trovati
        """
        nome_cercato = nome_cercato.lower()
        return [
            i for i in self.insegnanti
            if nome_cercato in i.nome.lower() or nome_cercato in i.cognome.lower()
        ]
    
    def insegna_materia(self, materia: str) -> List[Insegnante]:
        """Trova tutti gli insegnanti che insegnano una materia.
        
        Args:
            materia: Nome della materia
            
        Returns:
            Lista di insegnanti che insegnano la materia
        """
        return [i for i in self.insegnanti if i.insegna_materia(materia)]
    
    def insegnanti_per_carico(self, carico: str) -> List[Insegnante]:
        """Ottiene insegnanti con un determinato carico di lavoro.
        
        Args:
            carico: Carico di lavoro ('Leggero', 'Normale', 'Pesante', 'Molto Pesante')
            
        Returns:
            Lista di insegnanti con quel carico
        """
        return [i for i in self.insegnanti if i.carico_lavoro == carico]
    
    def statistiche_carico_lavoro(self) -> Dict:
        """Calcola statistiche sul carico di lavoro.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.insegnanti:
            return {"messaggio": "Nessun insegnante registrato"}
        
        carichi = [i.carico_lavoro for i in self.insegnanti]
        ore_totali = [i.totale_ore_settimanali for i in self.insegnanti]
        
        return {
            "totale_insegnanti": len(self.insegnanti),
            "ore_medie": round(sum(ore_totali) / len(ore_totali), 1),
            "ore_min": min(ore_totali),
            "ore_max": max(ore_totali),
            "distribuzione_carico": {
                carico: carichi.count(carico) 
                for carico in ["Leggero", "Normale", "Pesante", "Molto Pesante"]
            }
        }
    
    def materie_coperte(self) -> Dict[str, int]:
        """Trova tutte le materie insegnate e quanti insegnanti per ciascuna.
        
        Returns:
            Dizionario Materia -> numero insegnanti
        """
        materie_coperte = {}
        for insegnante in self.insegnanti:
            for materia in insegnante.materie:
                materie_coperte[materia] = materie_coperte.get(materia, 0) + 1
        return materie_coperte
    
    def statistiche_esperienza(self) -> Dict:
        """Calcola statistiche sull'esperienza degli insegnanti.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.insegnanti:
            return {"messaggio": "Nessun insegnante registrato"}
        
        esperienza = [i.anni_esperienza for i in self.insegnanti]
        
        # Categorizza per esperienza
        junior = sum(1 for e in esperienza if e < 5)
        mid = sum(1 for e in esperienza if 5 <= e < 15)
        senior = sum(1 for e in esperienza if 15 <= e < 25)
        veteran = sum(1 for e in esperienza if e >= 25)
        
        return {
            "media_esperienza": round(sum(esperienza) / len(esperienza), 1),
            "min": min(esperienza),
            "max": max(esperienza),
            "distribuzione": {
                "Junior (< 5 anni)": junior,
                "Mid (5-15 anni)": mid,
                "Senior (15-25 anni)": senior,
                "Veteran (>= 25 anni)": veteran
            }
        }
    
    def rimuovi_insegnante(self, id: int) -> bool:
        """Rimuove un insegnante.
        
        Args:
            id: ID dell'insegnante da rimuovere
            
        Returns:
            True se rimosso, False se non trovato
        """
        insegnante = self.trova_insegnante(id)
        if insegnante:
            self.insegnanti.remove(insegnante)
            return True
        return False
    
    def statistiche_generali(self) -> Dict:
        """Calcola statistiche generali.
        
        Returns:
            Dizionario con statistiche
        """
        return {
            **self.statistiche_carico_lavoro(),
            **self.statistiche_esperienza(),
            "materie_coperte": self.materie_coperte(),
            "numero_materie_uniche": len(self.materie_coperte())
        }
    
    def to_lista_dict(self) -> List[Dict]:
        """Converte tutti gli insegnanti in una lista di dizionari."""
        return [i.to_dict() for i in self.insegnanti]
    
    def __len__(self) -> int:
        """Restituisce il numero di insegnanti."""
        return len(self.insegnanti)
    
    def __repr__(self) -> str:
        """Rappresentazione stringa."""
        return f"GestioneInsegnanti({len(self.insegnanti)} insegnanti)"


# Import necessario per random
import random
