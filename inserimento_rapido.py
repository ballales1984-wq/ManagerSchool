"""
Modulo per l'inserimento rapido voti tramite interpretazione linguistica.
Permette ai docenti di inserire voti usando linguaggio naturale.
"""

from typing import Dict, Optional
from datetime import datetime
import re


class InterpreteDocente:
    """Interpreta frasi naturali per l'inserimento voti."""
    
    def __init__(self):
        """Inizializza l'interprete."""
        self.vocabolario_materie = {
            "matematica": "Matematica",
            "italiano": "Italiano",
            "inglese": "Inglese",
            "storia": "Storia",
            "scienze": "Scienze",
            "educazione fisica": "Educazione Fisica",
            "religione": "Religione",
            "geografia": "Geografia",
            "arte": "Arte"
        }
        
        self.vocabolario_tipi = {
            "interrogazione": "interrogazione",
            "interroga": "interrogazione",
            "verifica": "verifica scritta",
            "compito": "verifica scritta",
            "scritto": "verifica scritta",
            "orale": "interrogazione",
            "compito in classe": "verifica scritta"
        }
    
    def interpreta(self, frase: str) -> Dict:
        """Interpreta una frase in linguaggio naturale.
        
        Args:
            frase: Frase da interpretare (es: "Matematica interrogazione allunno Marco voto 8")
            
        Returns:
            Dizionario con dati estratti o errore
        """
        frase_lower = frase.lower()
        
        # Controlla se è un comando "carica lezione"
        if "carica" in frase_lower and "lezione" in frase_lower:
            return self._interpreta_lezione(frase_lower)
        
        # Pattern base: [materia] [tipo] allunno [nome] voto [numero]
        pattern = r"(\w+)\s+(interroga[zi]*|verifica|compito|scritto|orale)\s+allunno\s+(\w+)\s+voto\s+(\d+(?:[.,]\d+)?)"
        
        match = re.search(pattern, frase_lower)
        
        if not match:
            return {"errore": "Formato non riconosciuto. Esempio: 'Matematica interrogazione allunno Marco voto 8'"}
        
        materia_key, tipo_key, studente, voto_str = match.groups()
        
        # Normalizza voto
        voto = float(voto_str.replace(',', '.'))
        if voto < 1 or voto > 10:
            return {"errore": f"Voto deve essere tra 1 e 10, ricevuto: {voto}"}
        
        # Normalizza materia
        materia = self.vocabolario_materie.get(materia_key, materia_key.capitalize())
        
        # Normalizza tipo
        tipo = self.vocabolario_tipi.get(tipo_key, tipo_key)
        
        # Data e ora
        ora_attuale = datetime.now()
        
        return {
            "materia": materia,
            "tipo": tipo,
            "studente": studente.capitalize(),
            "voto": voto,
            "data": ora_attuale.strftime("%Y-%m-%d"),
            "ora": ora_attuale.strftime("%H:%M")
        }
    
    def _interpreta_lezione(self, frase_lower: str) -> Dict:
        """Interpreta comando caricamento lezione.
        
        Args:
            frase_lower: Frase in minuscolo
            
        Returns:
            Dizionario con dati lezione
        """
        # Cerca materia
        materia = None
        for mat_key, mat_val in self.vocabolario_materie.items():
            if mat_key in frase_lower:
                materia = mat_val
                break
        
        # Cerca classe
        classe_match = re.search(r'classe\s+(\d+[a-z])', frase_lower)
        classe = classe_match.group(1).upper() if classe_match else None
        
        # Cerca argomento (dopo "su" o "riguardo")
        argomento_match = re.search(r'(?:su|riguardo|argomento)\s+(.+?)(?:con|\.|$)', frase_lower)
        argomento = argomento_match.group(1).strip() if argomento_match else ""
        
        # Cerca file allegati
        file_match = re.search(r'(?:file|allegato|pdf|video)\s+([^\s]+)', frase_lower)
        file_allegato = file_match.group(1) if file_match else None
        
        return {
            "tipo": "lezione",
            "materia": materia,
            "classe": classe,
            "argomento": argomento,
            "file_allegato": file_allegato,
            "data": datetime.now().strftime("%Y-%m-%d")
        }
    
    def suggerisci_completamento(self, testo_parziale: str) -> list:
        """Suggerisce completamenti per un testo parziale.
        
        Args:
            testo_parziale: Testo inserito finora
            
        Returns:
            Lista di suggerimenti
        """
        suggerimenti = []
        testo_lower = testo_parziale.lower()
        
        # Se è vuoto o inizia, suggerisci materie
        if not testo_parziale or len(testo_parziale.split()) == 0:
            suggerimenti = list(self.vocabolario_materie.keys())[:5]
        
        # Se ha materia, suggerisci tipi
        elif any(m in testo_lower for m in self.vocabolario_materie.keys()):
            suggerimenti = list(self.vocabolario_tipi.keys())[:3]
        
        return suggerimenti


class GestoreInserimentoVeloce:
    """Gestisce l'inserimento veloce dei voti."""
    
    def __init__(self, anagrafica, gestione_voti):
        """Inizializza il gestore.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
        self.interprete = InterpreteDocente()
        self.cronologia_voci = []
    
    def inserisci_da_frase(self, frase: str, docente: str, classe: str) -> Dict:
        """Inserisce un voto a partire da una frase.
        
        Args:
            frase: Frase in linguaggio naturale
            docente: Nome del docente
            classe: Classe corrente
            
        Returns:
            Dizionario con risultato
        """
        # Interpreta la frase
        dati = self.interprete.interpreta(frase)
        
        if "errore" in dati:
            return dati
        
        # Trova lo studente
        studente = self.anagrafica.trova_per_nome(dati["studente"])
        
        if not studente:
            return {"errore": f"Studente '{dati['studente']}' non trovato"}
        
        if len(studente) > 1:
            return {"errore": f"Trovati {len(studente)} studenti con nome '{dati['studente']}'"}
        
        studente = studente[0]
        
        # Aggiungi il voto
        voto = self.gestione_voti.aggiungi_voto(
            id_studente=studente.id,
            materia=dati["materia"],
            voto=dati["voto"],
            tipo=dati["tipo"],
            data=dati["data"],
            note=f"Inserito da {docente}"
        )
        
        # Aggiungi alla cronologia
        voce = {
            "docente": docente,
            "classe": classe,
            "studente": dati["studente"],
            "materia": dati["materia"],
            "tipo": dati["tipo"],
            "voto": dati["voto"],
            "data": dati["data"],
            "ora": dati["ora"]
        }
        self.cronologia_voci.append(voce)
        
        return {
            "successo": True,
            "messaggio": f"Voto {dati['voto']} in {dati['materia']} registrato per {dati['studente']}",
            "voce": voce
        }
    
    def visualizza_cronologia(self, limit: int = 10) -> list:
        """Visualizza le ultime voci inserite.
        
        Args:
            limit: Numero di voci da mostrare
            
        Returns:
            Lista di voci
        """
        return self.cronologia_voci[-limit:]
    
    def carica_lezione_da_frase(self, frase: str, docente: str, gestore_lezioni) -> Dict:
        """Carica una lezione da frase in linguaggio naturale.
        
        Args:
            frase: Frase comando
            docente: Nome docente
            gestore_lezioni: Istanza GestoreLezioni
            
        Returns:
            Risultato caricamento
        """
        # Interpreta
        dati = self.interprete.interpreta(frase)
        
        if "errore" in dati or dati.get("tipo") != "lezione":
            return {"errore": "Comando lezione non riconosciuto"}
        
        # Carica lezione
        from lezioni_docente import Visibilita
        
        lezione = gestore_lezioni.carica_lezione(
            docente=docente,
            titolo=f"Lezione {dati.get('materia', '')}",
            materia=dati.get('materia', ''),
            classe=dati.get('classe', ''),
            argomento=dati.get('argomento', ''),
            data_lezione=dati.get('data', ''),
            tag=[dati.get('materia', '').lower()],
            visibilita=Visibilita.PUBBLICA,
            note=f"Caricata via interprete: {frase}"
        )
        
        return {
            "successo": True,
            "lezione_id": lezione.id,
            "messaggio": f"Lezione caricata: {lezione.titolo}"
        }
    
    def cerca_studenti(self, query: str) -> list:
        """Cerca studenti per autocompletamento.
        
        Args:
            query: Testo di ricerca
            
        Returns:
            Lista di studenti trovati
        """
        risultati = self.anagrafica.trova_per_nome(query)
        return [{"id": s.id, "nome": s.nome_completo, "classe": s.classe} for s in risultati[:5]]

