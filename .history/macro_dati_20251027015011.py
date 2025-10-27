"""
Modulo per l'integrazione di macro-dati educativi e sociali.
Collega dati ISTAT, MIUR, Eurostat agli studenti in base al territorio.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import random


@dataclass
class ZonaTerritoriale:
    """Rappresenta una zona territoriale con i suoi macro-dati."""
    nome: str
    regione: str
    reddito_medio_familiare: float
    percentuale_monogenitoriali: float
    tasso_abbandono_scolastico: float
    livello_istruzione_medio: float  # Anni medi di istruzione
    accesso_servizi_educativi: float  # 0-1
    accesso_servizi_sanitari: float   # 0-1
    indice_sviluppo_umano: float      # 0-1


class GestoreMacroDati:
    """Gestisce macro-dati educativi e sociali per zone territoriali."""
    
    # Dati predefiniti basati su statistiche reali (ISTAT/MIUR)
    ZONE_PREDEFINITE = {
        "Nord_Ovest": ZonaTerritoriale(
            nome="Nord Ovest",
            regione="Lombardia",
            reddito_medio_familiare=45000,
            percentuale_monogenitoriali=18,
            tasso_abbandono_scolastico=12,
            livello_istruzione_medio=11.5,
            accesso_servizi_educativi=0.85,
            accesso_servizi_sanitari=0.90,
            indice_sviluppo_umano=0.88
        ),
        "Nord_Est": ZonaTerritoriale(
            nome="Nord Est",
            regione="Veneto",
            reddito_medio_familiare=42000,
            percentuale_monogenitoriali=17,
            tasso_abbandono_scolastico=11,
            livello_istruzione_medio=11.2,
            accesso_servizi_educativi=0.83,
            accesso_servizi_sanitari=0.89,
            indice_sviluppo_umano=0.87
        ),
        "Centro": ZonaTerritoriale(
            nome="Centro",
            regione="Lazio",
            reddito_medio_familiare=38000,
            percentuale_monogenitoriali=22,
            tasso_abbandono_scolastico=15,
            livello_istruzione_medio=10.8,
            accesso_servizi_educativi=0.75,
            accesso_servizi_sanitari=0.82,
            indice_sviluppo_umano=0.82
        ),
        "Sud": ZonaTerritoriale(
            nome="Sud",
            regione="Campania",
            reddito_medio_familiare=28000,
            percentuale_monogenitoriali=28,
            tasso_abbandono_scolastico=25,
            livello_istruzione_medio=9.5,
            accesso_servizi_educativi=0.65,
            accesso_servizi_sanitari=0.72,
            indice_sviluppo_umano=0.72
        ),
        "Isole": ZonaTerritoriale(
            nome="Isole",
            regione="Sicilia",
            reddito_medio_familiare=26000,
            percentuale_monogenitoriali=30,
            tasso_abbandono_scolastico=28,
            livello_istruzione_medio=9.2,
            accesso_servizi_educativi=0.60,
            accesso_servizi_sanitari=0.68,
            indice_sviluppo_umano=0.70
        )
    }
    
    def __init__(self):
        """Inizializza il gestore macro-dati."""
        self.zone: Dict[str, ZonaTerritoriale] = self.ZONE_PREDEFINITE.copy()
        self.assegnazioni_studenti: Dict[int, str] = {}  # studente_id -> zona
    
    def aggiungi_zona(self, zona: ZonaTerritoriale) -> None:
        """Aggiunge una nuova zona territoriale.
        
        Args:
            zona: ZonaTerritoriale da aggiungere
        """
        self.zone[zona.nome] = zona
    
    def ottieni_zona(self, nome_zona: str) -> Optional[ZonaTerritoriale]:
        """Restituisce una zona per nome.
        
        Args:
            nome_zona: Nome della zona
            
        Returns:
            ZonaTerritoriale o None
        """
        return self.zone.get(nome_zona)
    
    def assegna_studente_a_zona(self, studente_id: int, zona: str) -> bool:
        """Assegna uno studente a una zona territoriale.
        
        Args:
            studente_id: ID dello studente
            zona: Nome della zona
            
        Returns:
            True se assegnato, False se zona non esistente
        """
        if zona not in self.zone:
            return False
        
        self.assegnazioni_studenti[studente_id] = zona
        return True
    
    def assegna_studente_casuale(self, studente_id: int) -> str:
        """Assegna uno studente a una zona casuale (con distribuzione realistica).
        
        Args:
            studente_id: ID dello studente
            
        Returns:
            Nome della zona assegnata
        """
        # Distribuzione realistica popolazione italiana
        pesi_zone = {
            "Nord_Ovest": 0.25,
            "Nord_Est": 0.20,
            "Centro": 0.22,
            "Sud": 0.22,
            "Isole": 0.11
        }
        
        zone = list(pesi_zone.keys())
        pesi = list(pesi_zone.values())
        
        zona_scelta = random.choices(zone, weights=pesi)[0]
        self.assegnazioni_studenti[studente_id] = zona_scelta
        
        return zona_scelta
    
    def macro_dati_studente(self, studente_id: int) -> Optional[ZonaTerritoriale]:
        """Restituisce i macro-dati per uno studente.
        
        Args:
            studente_id: ID dello studente
            
        Returns:
            ZonaTerritoriale o None
        """
        zona_nome = self.assegnazioni_studenti.get(studente_id)
        if zona_nome:
            return self.zone[zona_nome]
        return None
    
    def calcola_indice_fragilita_territoriale(self, zona: str) -> float:
        """Calcola un indice di fragilità territoriale (0-100).
        
        Args:
            zona: Nome della zona
            
        Returns:
            Indice di fragilità (0 = nessuna, 100 = massima)
        """
        if zona not in self.zone:
            return 0
        
        z = self.zone[zona]
        
        # Componenti dell'indice di fragilità
        fragilita_reddito = 1 - min(z.reddito_medio_familiare / 45000, 1)  # 0-1
        fragilita_famiglia = z.percentuale_monogenitoriali / 30  # Normalizzato
        fragilita_scolastica = z.tasso_abbandono_scolastico / 30
        fragilita_servizi = 1 - ((z.accesso_servizi_educativi + z.accesso_servizi_sanitari) / 2)
        
        # Media pesata
        indice = (
            fragilita_reddito * 0.30 +
            fragilita_famiglia * 0.20 +
            fragilita_scolastica * 0.25 +
            fragilita_servizi * 0.25
        )
        
        return round(indice * 100, 2)
    
    def calcola_impatto_reddito_territoriale(self, zona: str) -> float:
        """Calcola un fattore di impatto del reddito territoriale sui voti.
        
        Args:
            zona: Nome della zona
            
        Returns:
            Fattore di impatto (-2 a +2 voti)
        """
        if zona not in self.zone:
            return 0
        
        z = self.zone[zona]
        
        # Redditi bassi penalizzano, redditi alti aiutano
        impatto = (z.reddito_medio_familiare - 35000) / 20000  # Normalizzato
        
        return round(impatto, 2)
    
    def statistiche_zone(self) -> Dict:
        """Restituisce statistiche aggregate sulle zone.
        
        Returns:
            Dizionario con statistiche per zona
        """
        statistica = {}
        
        for nome, zona in self.zone.items():
            studenti_zona = sum(1 for z in self.assegnazioni_studenti.values() if z == nome)
            
            statistica[nome] = {
                "studenti": studenti_zona,
                "reddito_medio": zona.reddito_medio_familiare,
                "fragilita_territoriale": self.calcola_indice_fragilita_territoriale(nome),
                "indice_sviluppo": zona.indice_sviluppo_umano
            }
        
        return statistica
    
    def salva_su_file(self, nome_file: str = "macro_dati.json") -> None:
        """Salva i macro-dati e le assegnazioni su file JSON.
        
        Args:
            nome_file: Nome del file di output
        """
        dati = {
            "zone": {
                nome: {
                    "nome": z.nome,
                    "regione": z.regione,
                    "reddito_medio_familiare": z.reddito_medio_familiare,
                    "percentuale_monogenitoriali": z.percentuale_monogenitoriali,
                    "tasso_abbandono_scolastico": z.tasso_abbandono_scolastico,
                    "livello_istruzione_medio": z.livello_istruzione_medio,
                    "accesso_servizi_educativi": z.accesso_servizi_educativi,
                    "accesso_servizi_sanitari": z.accesso_servizi_sanitari,
                    "indice_sviluppo_umano": z.indice_sviluppo_umano
                }
                for nome, z in self.zone.items()
            },
            "assegnazioni": self.assegnazioni_studenti
        }
        
        with open(nome_file, 'w', encoding='utf-8') as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)
    
    def carica_da_file(self, nome_file: str = "macro_dati.json") -> bool:
        """Carica macro-dati e assegnazioni da file JSON.
        
        Args:
            nome_file: Nome del file da caricare
            
        Returns:
            True se caricato, False se errore
        """
        try:
            with open(nome_file, 'r', encoding='utf-8') as f:
                dati = json.load(f)
            
            # Ricostruisci zone
            for nome, info in dati["zone"].items():
                zona = ZonaTerritoriale(**info)
                self.zone[nome] = zona
            
            # Ricostruisci assegnazioni
            self.assegnazioni_studenti = {
                int(k): v for k, v in dati["assegnazioni"].items()
            }
            
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False
    
    def report_comparativo_zone(self) -> List[Dict]:
        """Genera un report comparativo tra le zone.
        
        Returns:
            Lista di dizionari con confronto zone ordinate per indice sviluppo
        """
        confronto = []
        
        for nome, zona in self.zone.items():
            studenti_zona = sum(1 for z in self.assegnazioni_studenti.values() if z == nome)
            
            confronto.append({
                "zona": nome,
                "indice_sviluppo": zona.indice_sviluppo_umano,
                "reddito_medio": zona.reddito_medio_familiare,
                "fragilita_territoriale": self.calcola_indice_fragilita_territoriale(nome),
                "studenti": studenti_zona,
                "tasso_abbandono": zona.tasso_abbandono_scolastico
            })
        
        # Ordina per indice di sviluppo (decrescente)
        confronto.sort(key=lambda x: x["indice_sviluppo"], reverse=True)
        
        return confronto
