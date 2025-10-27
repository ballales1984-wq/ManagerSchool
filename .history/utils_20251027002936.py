"""
Modulo di utilità per funzioni di supporto generiche.
"""

from typing import List, Dict, Any, Callable
from functools import wraps
import time


def stampa_separatore(carattere: str = "=", lunghezza: int = 80) -> None:
    """Stampa un separatore visivo.
    
    Args:
        carattere: Carattere da usare per il separatore
        lunghezza: Lunghezza del separatore
    """
    print(carattere * lunghezza)


def formatta_voto(voto: float) -> str:
    """Formatta un voto in modo leggibile.
    
    Args:
        voto: Voto da formattare
        
    Returns:
        Voto formattato come stringa
    """
    return f"{voto:.1f}"


def formatta_percentuale(valore: float) -> str:
    """Formatta una percentuale.
    
    Args:
        valore: Valore percentuale
        
    Returns:
        Percentuale formattata con 2 decimali
    """
    return f"{valore:.2f}%"


def formatta_euro(valore: int) -> str:
    """Formatta un valore monetario in euro.
    
    Args:
        valore: Valore in euro
        
    Returns:
        Valore formattato come stringa
    """
    return f"€ {valore:,}".replace(",", ".")


def centra_testo(testo: str, larghezza: int = 80) -> str:
    """Centra un testo in una stringa di larghezza specificata.
    
    Args:
        testo: Testo da centrare
        larghezza: Larghezza totale della stringa
        
    Returns:
        Testo centrato
    """
    return testo.center(larghezza)


def formatta_lista(lista: List[Any], separatore: str = ", ") -> str:
    """Formatta una lista come stringa.
    
    Args:
        lista: Lista da formattare
        separatore: Separatore tra gli elementi
        
    Returns:
        Lista formattata come stringa
    """
    return separatore.join(str(item) for item in lista)


def calcola_media(numeri: List[float]) -> float:
    """Calcola la media di una lista di numeri.
    
    Args:
        numeri: Lista di numeri
        
    Returns:
        Media aritmetica (0 se lista vuota)
    """
    if not numeri:
        return 0.0
    return sum(numeri) / len(numeri)


def calcola_deviazione_standard(numeri: List[float]) -> float:
    """Calcola la deviazione standard di una lista di numeri.
    
    Args:
        numeri: Lista di numeri
        
    Returns:
        Deviazione standard (0 se lista vuota o un solo elemento)
    """
    if len(numeri) <= 1:
        return 0.0
    
    media = calcola_media(numeri)
    varianza = sum((x - media) ** 2 for x in numeri) / len(numeri)
    return varianza ** 0.5


def trova_minimo_maximo(lista: List[float]) -> tuple[float, float]:
    """Trova il minimo e il massimo in una lista.
    
    Args:
        lista: Lista di numeri
        
    Returns:
        Tupla (minimo, massimo). Restituisce (0, 0) se lista vuota
    """
    if not lista:
        return (0.0, 0.0)
    return (min(lista), max(lista))


def ordina_per_chiave(lista: List[Dict], chiave: str, reverse: bool = False) -> List[Dict]:
    """Ordina una lista di dizionari per una chiave specifica.
    
    Args:
        lista: Lista di dizionari
        chiave: Chiave per cui ordinare
        reverse: Se True ordina in ordine decrescente
        
    Returns:
        Lista ordinata
    """
    return sorted(lista, key=lambda x: x.get(chiave, 0), reverse=reverse)


def filtra_per_condizione(lista: List[Any], condizione: Callable) -> List[Any]:
    """Filtra una lista secondo una condizione.
    
    Args:
        lista: Lista da filtrare
        condizione: Funzione che restituisce True per elementi da mantenere
        
    Returns:
        Lista filtrata
    """
    return [item for item in lista if condizione(item)]


def raggruppa_per_chiave(lista: List[Dict], chiave: str) -> Dict[Any, List[Dict]]:
    """Raggruppa una lista di dizionari per una chiave specifica.
    
    Args:
        lista: Lista di dizionari
        chiave: Chiave per raggruppare
        
    Returns:
        Dizionario con chiavi univoche e liste di elementi corrispondenti
    """
    risultato = {}
    for elemento in lista:
        valore_chiave = elemento.get(chiave)
        if valore_chiave not in risultato:
            risultato[valore_chiave] = []
        risultato[valore_chiave].append(elemento)
    return risultato


def conta_occorrenze(lista: List[Any]) -> Dict[Any, int]:
    """Conta le occorrenze di ogni elemento in una lista.
    
    Args:
        lista: Lista di elementi
        
    Returns:
        Dizionario con conteggio occorrenze
    """
    conteggio = {}
    for elemento in lista:
        conteggio[elemento] = conteggio.get(elemento, 0) + 1
    return conteggio


def misuri_tempo_esecuzione(func: Callable):
    """Decorator per misurare il tempo di esecuzione di una funzione.
    
    Args:
        func: Funzione da decorare
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        inizio = time.time()
        risultato = func(*args, **kwargs)
        fine = time.time()
        print(f"⏱️  Tempo esecuzione {func.__name__}: {fine - inizio:.4f} secondi")
        return risultato
    return wrapper


def stampa_tabella(righe: List[List[str]], intestazioni: List[str] = None, 
                   allinea: List[str] = None) -> None:
    """Stampa una tabella formattata.
    
    Args:
        righe: Lista di liste, ogni lista è una riga della tabella
        intestazioni: Lista di intestazioni (opzionale)
        allinea: Lista di allineamenti ('left', 'right', 'center') per ogni colonna
    """
    if not righe:
        print("Tabella vuota")
        return
    
    num_colonne = len(righe[0])
    
    # Determina la larghezza di ogni colonna
    larghezze = [0] * num_colonne
    
    if intestazioni:
        larghezze = [len(str(h)) for h in intestazioni]
    
    for riga in righe:
        for i, cella in enumerate(riga):
            larghezze[i] = max(larghezze[i], len(str(cella)))
    
    # Allineamenti di default
    if allinea is None:
        allinea = ['left'] * num_colonne
    
    # Stampa intestazioni
    if intestazioni:
        line = " | ".join(
            str(intestazioni[i]).ljust(larghezze[i]) 
            if allinea[i] == 'left' 
            else str(intestazioni[i]).rjust(larghezze[i])
            for i in range(num_colonne)
        )
        print(line)
        print("-" * len(line))
    
    # Stampa righe
    for riga in righe:
        line = " | ".join(
            str(cella).ljust(larghezze[i]) 
            if allinea[i] == 'left' 
            else str(cella).rjust(larghezze[i])
            for i, cella in enumerate(riga)
        )
        print(line)


def barra_progresso(attuale: int, totale: int, lunghezza: int = 40) -> str:
    """Genera una barra di progresso testuale.
    
    Args:
        attuale: Valore attuale
        totale: Valore totale
        lunghezza: Lunghezza della barra
        
    Returns:
        Stringa con la barra di progresso
    """
    if totale == 0:
        percentuale = 100
    else:
        percentuale = int((attuale / totale) * 100)
    
    completati = int((percentuale / 100) * lunghezza)
    barra = '█' * completati + '░' * (lunghezza - completati)
    
    return f"[{barra}] {percentuale}%"


def conferma_input(messaggio: str, default: bool = False) -> bool:
    """Richiede conferma all'utente.
    
    Args:
        messaggio: Messaggio da mostrare
        default: Valore di default se l'utente non inserisce nulla
        
    Returns:
        True se confermato, False altrimenti
    """
    risposta = input(f"{messaggio} (s/n): ").strip().lower()
    
    if not risposta:
        return default
    
    return risposta in ['s', 'si', 'sì', 'y', 'yes', 'true', '1']


def input_numerico(messaggio: str, minimo: float = None, massimo: float = None) -> float:
    """Richiede un input numerico all'utente con validazione.
    
    Args:
        messaggio: Messaggio da mostrare
        minimo: Valore minimo accettato (opzionale)
        massimo: Valore massimo accettato (opzionale)
        
    Returns:
        Numero inserito dall'utente
    """
    while True:
        try:
            valore = float(input(messaggio))
            
            if minimo is not None and valore < minimo:
                print(f"⚠️  Il valore deve essere maggiore o uguale a {minimo}")
                continue
            
            if massimo is not None and valore > massimo:
                print(f"⚠️  Il valore deve essere minore o uguale a {massimo}")
                continue
            
            return valore
            
        except ValueError:
            print("❌ Inserisci un numero valido")


def chiarisci_stampa(testo: str, lunghezza: int = 80) -> None:
    """Stampa un testo con box decorativo.
    
    Args:
        testo: Testo da mostrare
        lunghezza: Larghezza del box
    """
    print("┌" + "─" * (lunghezza - 2) + "┐")
    
    # Divide il testo in righe
    parole = testo.split()
    righe = []
    riga_corrente = ""
    
    for parola in parole:
        if len(riga_corrente + " " + parola) <= lunghezza - 4:
            riga_corrente += (" " + parola) if riga_corrente else parola
        else:
            if riga_corrente:
                righe.append(riga_corrente)
            riga_corrente = parola
    
    if riga_corrente:
        righe.append(riga_corrente)
    
    # Stampa le righe
    for riga in righe:
        print("│ " + riga.ljust(lunghezza - 4) + " │")
    
    print("└" + "─" * (lunghezza - 2) + "┘")
