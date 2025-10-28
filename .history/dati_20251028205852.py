"""
Modulo per la generazione di dati casuali realistici
per il sistema scolastico.
"""

import random
from typing import List, Tuple
from enum import Enum


class CategoriaReddito(Enum):
    MOLTO_BASSO = (0, 15000)
    BASSO = (15000, 25000)
    MEDIO = (25000, 45000)
    ALTO = (45000, 75000)
    MOLTO_ALTO = (75000, 200000)


class CondizioneSalute(Enum):
    ECCELLENTE = "Eccellente"
    BUONA = "Buona"
    DISCRETA = "Discreta"
    PROBLEMATICA = "Problematica"
    CRITICA = "Critica"


NOMI_ITA = [
    "Giulia", "Francesco", "Sofia", "Lorenzo", "Alice", "Tommaso",
    "Emma", "Leonardo", "Ginevra", "Mattia", "Beatrice", "Andrea",
    "Aurora", "Riccardo", "Giorgia", "Gabriele", "Vittoria", "Davide",
    "Chiara", "Federico", "Elisa", "Luca", "Martina", "Alessandro",
    "Federica", "Marco", "Serena", "Matteo", "Valentina", "Nicolas"
]

COGNOMI_ITA = [
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano",
    "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo",
    "Conti", "De Luca", "Costa", "Fontana", "Caruso", "Mancini",
    "Rizzo", "Lombardi", "Moretti", "Barbieri", "Ferrara", "Galli",
    "Martelli", "Leone", "Santoro", "Rinaldi", "Longo", "Lombardo"
]

MATERIE = [
    "Matematica", "Italiano", "Inglese", "Storia", "Geografia",
    "Scienze", "Arte", "Musica", "Educazione Fisica", "Tecnologia",
    "Informatica", "Spagnolo", "Filosofia", "Fisica", "Chimica",
    "Biologia", "Lettere", "Diritto", "Economia"
]


def nome_casuale() -> str:
    """Genera un nome casuale italiano."""
    return random.choice(NOMI_ITA)


def cognome_casuale() -> str:
    """Genera un cognome casuale italiano."""
    return random.choice(COGNOMI_ITA)


def nome_completo() -> str:
    """Genera un nome completo casuale."""
    return f"{nome_casuale()} {cognome_casuale()}"


def eta_casuale(scuola: str = "superiore") -> int:
    """Genera un'età casuale in base al tipo di scuola.
    
    Args:
        scuola: Tipo di scuola ('media', 'superiore', 'università')
        
    Returns:
        Età casuale appropriata
    """
    if scuola == "media":
        return random.randint(11, 14)
    elif scuola == "superiore":
        return random.randint(14, 19)
    elif scuola == "università":
        return random.randint(19, 26)
    else:
        return random.randint(14, 19)


def reddito_familiare() -> int:
    """Genera un reddito familiare casuale tra 10000 e 100000 euro."""
    return random.randint(10000, 100000)


def categoria_reddito(reddito: int) -> CategoriaReddito:
    """Determina la categoria di reddito in base al valore.
    
    Args:
        reddito: Reddito familiare annuo
        
    Returns:
        Categoria di reddito corrispondente
    """
    if reddito < 15000:
        return CategoriaReddito.MOLTO_BASSO
    elif reddito < 25000:
        return CategoriaReddito.BASSO
    elif reddito < 45000:
        return CategoriaReddito.MEDIO
    elif reddito < 75000:
        return CategoriaReddito.ALTO
    else:
        return CategoriaReddito.MOLTO_ALTO


def condizione_salute() -> CondizioneSalute:
    """Genera una condizione di salute casuale."""
    pesi = [0.15, 0.35, 0.30, 0.15, 0.05]  # Probabilità rispettive
    return random.choices(
        list(CondizioneSalute),
        weights=pesi
    )[0]


def situazione_familiare() -> str:
    """Genera una situazione familiare casuale."""
    situazioni = [
        "Monoparentale",
        "Nucleo tradizionale",
        "Allargata",
        "Genitori separati",
        "Affidamento"
    ]
    pesi = [0.10, 0.60, 0.15, 0.10, 0.05]
    return random.choices(situazioni, weights=pesi)[0]


def voto_casuale(base: float = 6.0, varianza: float = 2.0) -> float:
    """Genera un voto casuale realistico.
    
    Args:
        base: Voto base (default 6.0)
        varianza: Variabilità del voto (default 2.0)
        
    Returns:
        Voto compreso tra 3.0 e 10.0
    """
    voto = random.gauss(base, varianza)
    return max(3.0, min(10.0, round(voto, 1)))


def materie_casuali(num_materie: int = 5) -> List[str]:
    """Genera una lista di materie casuali.
    
    Args:
        num_materie: Numero di materie da generare
        
    Returns:
        Lista di materie casuali
    """
    return random.sample(MATERIE, min(num_materie, len(MATERIE)))


def classe_casuale(tipo_scuola: str = "liceo") -> str:
    """Genera una classe casuale.
    
    Args:
        tipo_scuola: Tipo di scuola ('liceo', 'tecnico', 'professionale')
        
    Returns:
        Classe (es: "3A", "2B", "5C")
    """
    anno = random.randint(1, 5)
    sezione = random.choice(["A", "B", "C"])
    return f"{anno}{sezione}"


def orario_settimanale_materia(ore_min: int = 2, ore_max: int = 6) -> int:
    """Genera un numero di ore settimanali per una materia.
    
    Args:
        ore_min: Ore minime settimanali
        ore_max: Ore massime settimanali
        
    Returns:
        Numero di ore settimanali
    """
    return random.randint(ore_min, ore_max)


def giorno_settimana() -> str:
    """Restituisce un giorno della settimana casuale."""
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    return random.choice(giorni)


def ora_lezione() -> Tuple[int, int]:
    """Genera un orario di lezione.
    
    Returns:
        Tupla (ora inizio, ora fine) in formato 24h
    """
    ora_inizio = random.randint(8, 13)
    return (ora_inizio, ora_inizio + 1)


def percentuale() -> float:
    """Genera una percentuale casuale tra 0 e 100.
    
    Returns:
        Percentuale con 2 decimali
    """
    return round(random.uniform(0, 100), 2)


def booleano(probabilita_vero: float = 0.5) -> bool:
    """Genera un valore booleano casuale.
    
    Args:
        probabilita_vero: Probabilità che il risultato sia True (default 0.5)
        
    Returns:
        True o False
    """
    return random.random() < probabilita_vero
