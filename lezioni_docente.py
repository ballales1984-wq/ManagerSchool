"""
Modulo LezioniDocente - ManagerSchool
Gestione caricamento lezioni e materiali didattici
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import os
import json


class TipoMateriale(str, Enum):
    """Tipi di materiale didattico."""
    PDF = "PDF"
    VIDEO = "Video"
    LINK = "Link"
    IMMAGINE = "Immagine"
    ZIP = "Archivio"
    TESTO = "Testo"


class Visibilita(str, Enum):
    """Visibilità contenuto."""
    PUBBLICA = "Pubblica"      # Studenti + Genitori
    PRIVATA = "Privata"         # Solo docente
    CLASSE = "Solo Classe"      # Solo studenti della classe


@dataclass
class Materiale:
    """Rappresenta un materiale didattico."""
    id: int
    tipo: TipoMateriale
    titolo: str
    descrizione: str
    url: str  # Percorso file o URL
    dimensione: int  # Bytes
    data_caricamento: str
    formato: str = ""  # jpg, pdf, mp4, etc


@dataclass
class Lezione:
    """Rappresenta una lezione caricata."""
    id: int
    docente: str
    titolo: str
    materia: str
    classe: str
    argomento: str
    data_lezione: str
    tag: Set[str]
    materiali: List[Materiale]
    visibilita: Visibilita
    note: str = ""
    collegamento_voti_id: Optional[int] = None  # Se è interrogazione/verifica
    
    def to_dict(self):
        """Converte in dizionario."""
        return {
            'id': self.id,
            'docente': self.docente,
            'titolo': self.titolo,
            'materia': self.materia,
            'classe': self.classe,
            'argomento': self.argomento,
            'data_lezione': self.data_lezione,
            'tag': list(self.tag),
            'materiali': [m.__dict__ for m in self.materiali],
            'visibilita': self.visibilita.value,
            'note': self.note,
            'collegamento_voti_id': self.collegamento_voti_id
        }


class GestoreLezioni:
    """Gestisce lezioni e materiali didattici."""
    
    def __init__(self):
        """Inizializza gestore lezioni."""
        self.lezioni = []
        self.materiali = []
        self._prossimo_id_lezione = 1
        self._prossimo_id_materiale = 1
        self.upload_dir = "uploads/lezioni"
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def carica_lezione(self, docente: str, titolo: str, materia: str,
                      classe: str, argomento: str, data_lezione: str,
                      tag: List[str] = None, visibilita: Visibilita = Visibilita.PUBBLICA,
                      note: str = "", materiali: List[Dict] = None) -> Lezione:
        """Carica una nuova lezione.
        
        Args:
            docente: Nome docente
            titolo: Titolo lezione
            materia: Materia
            classe: Classe target
            argomento: Argomento trattato
            data_lezione: Data lezione
            tag: Tag semantici
            visibilita: Visibilità
            note: Note aggiuntive
            materiali: Lista materiali
            
        Returns:
            Lezione creata
        """
        lezione = Lezione(
            id=self._prossimo_id_lezione,
            docente=docente,
            titolo=titolo,
            materia=materia,
            classe=classe,
            argomento=argomento,
            data_lezione=data_lezione,
            tag=set(tag or []),
            materiali=[],
            visibilita=visibilita,
            note=note
        )
        
        # Aggiungi materiali
        if materiali:
            for mat_data in materiali:
                materiale = self._crea_materiale(mat_data)
                lezione.materiali.append(materiale)
        
        self.lezioni.append(lezione)
        self._prossimo_id_lezione += 1
        
        print(f"✅ Lezione caricata: {titolo} - {materia} ({classe})")
        return lezione
    
    def _crea_materiale(self, mat_data: Dict) -> Materiale:
        """Crea oggetto materiale.
        
        Args:
            mat_data: Dati materiale
            
        Returns:
            Materiale
        """
        materiale = Materiale(
            id=self._prossimo_id_materiale,
            tipo=TipoMateriale(mat_data['tipo']),
            titolo=mat_data['titolo'],
            descrizione=mat_data.get('descrizione', ''),
            url=mat_data['url'],
            dimensione=mat_data.get('dimensione', 0),
            data_caricamento=datetime.now().isoformat(),
            formato=mat_data.get('formato', '')
        )
        
        self.materiali.append(materiale)
        self._prossimo_id_materiale += 1
        
        return materiale
    
    def lezioni_docente(self, docente: str) -> List[Lezione]:
        """Ottiene lezioni di un docente.
        
        Args:
            docente: Nome docente
            
        Returns:
            Lista lezioni
        """
        return [l for l in self.lezioni if l.docente == docente]
    
    def lezioni_classe(self, classe: str) -> List[Lezione]:
        """Ottiene lezioni per classe.
        
        Args:
            classe: Classe
            
        Returns:
            Lista lezioni
        """
        return [l for l in self.lezioni if l.classe == classe]
    
    def cerca_lezione_tag(self, tag: str) -> List[Lezione]:
        """Cerca lezioni per tag.
        
        Args:
            tag: Tag da cercare
            
        Returns:
            Lista lezioni
        """
        return [l for l in self.lezioni if tag.lower() in [t.lower() for t in l.tag]]
    
    def statistiche_docente(self, docente: str) -> Dict:
        """Genera statistiche per docente.
        
        Args:
            docente: Nome docente
            
        Returns:
            Statistiche
        """
        lezioni = self.lezioni_docente(docente)
        
        # Conta materiali
        materiali_count = sum(len(l.materiali) for l in lezioni)
        
        # Conta per materia
        materie = {}
        for lezione in lezioni:
            materie[lezione.materia] = materie.get(lezione.materia, 0) + 1
        
        return {
            'totale_lezioni': len(lezioni),
            'totale_materiali': materiali_count,
            'materie': materie,
            'classi_uniche': len(set(l.classe for l in lezioni))
        }
    
    def link_to_voto(self, lezione_id: int, voto_id: int):
        """Collega lezione a voto (per interrogazioni/verifiche).
        
        Args:
            lezione_id: ID lezione
            voto_id: ID voto
            
        Returns:
            Successo
        """
        lezione = next((l for l in self.lezioni if l.id == lezione_id), None)
        if lezione:
            lezione.collegamento_voti_id = voto_id
            print(f"✅ Lezione {lezione_id} collegata a voto {voto_id}")
            return True
        return False


# Instanza globale
gestore_lezioni = GestoreLezioni()


if __name__ == "__main__":
    print("GESTORE LEZIONI - TEST")
    print("=" * 60 + "\n")
    
    # Test caricamento lezione
    lezione = gestore_lezioni.carica_lezione(
        docente="Prof.ssa Bianchi",
        titolo="Triangoli e Teorema di Pitagora",
        materia="Matematica",
        classe="2B",
        argomento="Geometria: triangoli rettangoli",
        data_lezione="2025-10-30",
        tag=["geometria", "triangoli", "pitagora", "verifica"],
        visibilita=Visibilita.PUBBLICA,
        materiali=[
            {
                'tipo': 'PDF',
                'titolo': 'Dispensa triangoli.pdf',
                'url': 'uploads/lezioni/triangoli.pdf',
                'dimensione': 2048000,
                'formato': 'pdf',
                'descrizione': 'Dispensa completa sui triangoli'
            },
            {
                'tipo': 'Video',
                'titolo': 'Video spiegazione',
                'url': 'https://youtube.com/watch?v=xyz',
                'dimensione': 0,
                'formato': 'mp4',
                'descrizione': 'Video tutorial'
            }
        ]
    )
    
    print(f"Lezione ID: {lezione.id}")
    print(f"Materiali: {len(lezione.materiali)}")
    print(f"Tag: {lezione.tag}")
    
    # Statistiche
    stats = gestore_lezioni.statistiche_docente("Prof.ssa Bianchi")
    print(f"\nStatistiche Prof.ssa Bianchi:")
    print(f"  Lezioni: {stats['totale_lezioni']}")
    print(f"  Materiali: {stats['totale_materiali']}")
    
    print("\n✅ Test completato!")

