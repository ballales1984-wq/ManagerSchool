"""
Integrazione Database nel sistema ManagerSchool.
Mantiene compatibilità con il codice esistente.
"""

from database_manager import DatabaseManager
from typing import List, Dict
import json


class DatabaseIntegration:
    """Integrazione database che mantiene compatibilità con il sistema esistente."""
    
    def __init__(self, anagrafica, gestione_voti):
        """Inizializza l'integrazione.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
        self.db = DatabaseManager("managerschool.db")
        
        # Sincronizza dati esistenti
        if not self.db.conta_studenti():
            self.sincronizza_dati_esistenti()
    
    def sincronizza_dati_esistenti(self):
        """Sincronizza i dati in-memory con il database."""
        print("🔄 Sincronizzazione dati esistenti...")
        
        # Sincronizza studenti
        for studente in self.anagrafica.studenti:
            studente_dict = {
                'id': studente.id,
                'nome': studente.nome,
                'cognome': studente.cognome,
                'eta': studente.eta,
                'classe': studente.classe,
                'reddito_familiare': studente.reddito_familiare,
                'categoria_reddito': studente.categoria_reddito.value,
                'condizione_salute': studente.condizione_salute.value,
                'situazione_familiare': studente.situazione_familiare,
                'note': studente.note
            }
            try:
                self.db.aggiungi_studente(studente_dict)
            except:
                pass  # Già esiste
        
        # Sincronizza voti
        for voto in self.gestione_voti.voti:
            voto_dict = {
                'id_studente': voto.id_studente,
                'materia': voto.materia,
                'voto': voto.voto,
                'tipo': voto.tipo,
                'data': voto.data,
                'note': voto.note
            }
            try:
                self.db.aggiungi_voto(voto_dict)
            except:
                pass  # Già esiste
        
        print(f"✅ Sincronizzati {self.db.conta_studenti()} studenti")
    
    def salva_studente(self, studente):
        """Salva uno studente nel database."""
        studente_dict = {
            'id': studente.id,
            'nome': studente.nome,
            'cognome': studente.cognome,
            'eta': studente.eta,
            'classe': studente.classe,
            'reddito_familiare': studente.reddito_familiare,
            'categoria_reddito': studente.categoria_reddito.value,
            'condizione_salute': studente.condizione_salute.value,
            'situazione_familiare': studente.situazione_familiare,
            'note': studente.note
        }
        return self.db.aggiungi_studente(studente_dict)
    
    def salva_voto(self, voto):
        """Salva un voto nel database."""
        voto_dict = {
            'id_studente': voto.id_studente,
            'materia': voto.materia,
            'voto': voto.voto,
            'tipo': voto.tipo,
            'data': voto.data,
            'note': voto.note
        }
        return self.db.aggiungi_voto(voto_dict)
    
    def ottieni_statistiche(self) -> Dict:
        """Ottiene statistiche dal database."""
        return self.db.statistiche_database()
    
    def backup(self, percorso: str = None) -> str:
        """Crea backup del database."""
        return self.db.backup_database(percorso)
    
    def carica_dati_esistenti(self):
        """Carica dati dal database nei moduli esistenti."""
        # Carica studenti
        studenti_db = self.db.ottieni_studenti()
        
        from dati import CategoriaReddito, CondizioneSalute
        from anagrafica import Studente
        
        # Converti da database a oggetti
        for studente_dict in studenti_db:
            try:
                studente = Studente(
                    id=studente_dict['id'],
                    nome=studente_dict['nome'],
                    cognome=studente_dict['cognome'],
                    eta=studente_dict['eta'],
                    classe=studente_dict['classe'],
                    reddito_familiare=studente_dict.get('reddito_familiare', 30000),
                    categoria_reddito=CategoriaReddito.MEDIO,
                    condizione_salute=CondizioneSalute.BUONA,
                    situazione_familiare=studente_dict.get('situazione_familiare', '')
                )
                # Aggiungi solo se non esiste già
                if not any(s.id == studente.id for s in self.anagrafica.studenti):
                    self.anagrafica.studenti.append(studente)
            except Exception as e:
                print(f"⚠️ Errore caricamento studente: {e}")


def enable_database_mode():
    """Abilita modalità database per il sistema."""
    print("✅ Modalità database attivata")
    print("   I dati saranno persistenti tra le sessioni")
    return DatabaseIntegration

