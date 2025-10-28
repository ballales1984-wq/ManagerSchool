"""
Modulo per il backup e la sincronizzazione del registro scolastico.
Gestisce salvataggio automatico, ripristino e versionamento.
"""

import json
import os
import shutil
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import hashlib


class GestoreBackup:
    """Gestisce backup e ripristino del registro scolastico."""
    
    def __init__(self, directory_backup: str = "backup"):
        """Inizializza il gestore backup.
        
        Args:
            directory_backup: Directory dove salvare i backup
        """
        self.directory_backup = Path(directory_backup)
        self.directory_backup.mkdir(exist_ok=True)
        
        # Crea sottocartelle
        (self.directory_backup / "giornalieri").mkdir(exist_ok=True)
        (self.directory_backup / "settimanali").mkdir(exist_ok=True)
        (self.directory_backup / "mensili").mkdir(exist_ok=True)
    
    def salva_backup(self, registro, filepath: Optional[str] = None) -> str:
        """Salva il registro in un file JSON.
        
        Args:
            registro: Oggetto registro da salvare
            filepath: Percorso file (default: backup/data_ora.json)
            
        Returns:
            Percorso del file salvato
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(self.directory_backup / f"giornalieri/backup_{timestamp}.json")
        
        # Prepara i dati per il backup
        dati_backup = {
            "metadata": {
                "data_backup": datetime.now().isoformat(),
                "versione": "1.0",
                "tipo": "backup_completo"
            },
            "studenti": [s.to_dict() for s in registro.anagrafica.studenti],
            "insegnanti": [i.to_dict() for i in registro.insegnanti.insegnanti],
            "voti": [{
                "id_studente": v.id_studente,
                "materia": v.materia,
                "voto": v.voto,
                "tipo": v.tipo,
                "data": v.data,
                "note": v.note
            } for v in registro.voti.voti],
            "pagelle": [{
                "id_studente": p.id_studente,
                "quadrimestre": p.quadrimestre,
                "voti_materie": p.voti_materie,
                "media_generale": p.media_generale,
                "comportamento": p.comportamento,
                "assenze": p.assenze,
                "note": p.note
            } for p in registro.voti.pagelle],
            "statistiche": {
                "totale_studenti": len(registro.anagrafica.studenti),
                "totale_insegnanti": len(registro.insegnanti.insegnanti),
                "totale_voti": len(registro.voti.voti),
                "totale_pagelle": len(registro.voti.pagelle)
            }
        }
        
        # Calcola hash per integrità
        json_str = json.dumps(dati_backup, indent=2, ensure_ascii=False)
        hash_value = hashlib.sha256(json_str.encode()).hexdigest()
        dati_backup["metadata"]["hash"] = hash_value
        
        # Salva il file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dati_backup, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup salvato: {filepath}")
        print(f"📊 Studenti: {len(dati_backup['studenti'])}, Voti: {len(dati_backup['voti'])}")
        print(f"🔐 Hash integrità: {hash_value[:16]}...")
        
        return filepath
    
    def carica_backup(self, filepath: str) -> Dict:
        """Carica un backup dal file.
        
        Args:
            filepath: Percorso del file backup
            
        Returns:
            Dizionario con i dati del backup
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File backup non trovato: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            dati = json.load(f)
        
        # Verifica hash
        filepath_str = json.dumps(dati, indent=2, ensure_ascii=False)
        hash_calcolato = hashlib.sha256(filepath_str.encode()).hexdigest()
        hash_salvato = dati["metadata"].get("hash", "")
        
        if hash_salvato and hash_calcolato != hash_salvato:
            print("⚠️  ATTENZIONE: File backup potrebbe essere corrotto!")
        
        print(f"✅ Backup caricato: {filepath}")
        print(f"📅 Data backup: {dati['metadata']['data_backup']}")
        print(f"📊 Statistiche: {dati['statistiche']}")
        
        return dati
    
    def ripristina_da_backup(self, registro, filepath: str) -> bool:
        """Ripristina il registro da un backup.
        
        Args:
            registro: Oggetto registro da ripristinare
            filepath: Percorso del file backup
            
        Returns:
            True se riuscito
        """
        try:
            dati = self.carica_backup(filepath)
            
            # Import necessario
            from anagrafica import Studente, Anagrafica
            from insegnanti import Insegnante, GestioneInsegnanti
            from voti import Voto, Pagella, GestioneVoti
            from dati import CategoriaReddito, CondizioneSalute
            
            # Ripristina studenti
            registro.anagrafica.studenti = []
            for s_data in dati["studenti"]:
                # Ricrea oggetto Studente
                studente = Studente(
                    id=s_data["id"],
                    nome=s_data["nome"],
                    cognome=s_data["cognome"],
                    eta=s_data.get("eta", 15),
                    classe=s_data["classe"],
                    reddito_familiare=s_data.get("reddito", 30000),
                    categoria_reddito=CategoriaReddito.MEDIO,
                    condizione_salute=CondizioneSalute.BUONA,
                    situazione_familiare=s_data.get("famiglia", "Nucleo tradizionale")
                )
                registro.anagrafica.studenti.append(studente)
            
            # Ripristina insegnanti (sem semplificato)
            registro.insegnanti.insegnanti = []
            for i_data in dati["insegnanti"]:
                from insegnanti import Insegnante
                import random
                
                insegnante = Insegnante(
                    id=i_data["id"],
                    nome=i_data["nome"],
                    cognome=i_data["cognome"],
                    eta=i_data.get("eta", 40),
                    materie=i_data.get("materie", ["Generale"]),
                    ore_settimanali=i_data.get("ore_settimanali", {}),
                    anni_esperienza=i_data.get("anni_esperienza", 10),
                    sezioni_assegnate=i_data.get("sezioni_assegnate", [])
                )
                registro.insegnanti.insegnanti.append(insegnante)
            
            # Ripristina voti (semplificato)
            registro.voti.voti = []
            from voti import Voto
            for v_data in dati["voti"]:
                voto = Voto(
                    id_studente=v_data["id_studente"],
                    materia=v_data["materia"],
                    voto=v_data["voto"],
                    tipo=v_data["tipo"],
                    data=v_data["data"],
                    note=v_data.get("note", "")
                )
                registro.voti.voti.append(voto)
            
            print(f"✅ Registro ripristinato da backup!")
            print(f"📊 Ripristinati {len(registro.anagrafica.studenti)} studenti, {len(registro.voti.voti)} voti")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore nel ripristino: {e}")
            return False
    
    def lista_backup_disponibili(self, tipo: str = "giornalieri") -> List[Dict]:
        """Lista i backup disponibili.
        
        Args:
            tipo: Tipo di backup ('giornalieri', 'settimanali', 'mensili')
            
        Returns:
            Lista di dict con info backup
        """
        directory = self.directory_backup / tipo
        backup_disponibili = []
        
        if not directory.exists():
            return []
        
        for filepath in sorted(directory.glob("backup_*.json"), reverse=True):
            stat = filepath.stat()
            backup_disponibili.append({
                "file": str(filepath),
                "nome": filepath.name,
                "data": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "dimensione": stat.st_size
            })
        
        return backup_disponibili
    
    def pulizia_backup_vecchi(self, giorni_mantieni: int = 30):
        """Elimina backup più vecchi di N giorni.
        
        Args:
            giorni_mantieni: Numero di giorni da mantenere
        """
        cutoff_date = datetime.now() - timedelta(days=giorni_mantieni)
        eliminati = 0
        
        for tipo in ["giornalieri", "settimanali", "mensili"]:
            directory = self.directory_backup / tipo
            if not directory.exists():
                continue
            
            for filepath in directory.glob("backup_*.json"):
                if datetime.fromtimestamp(filepath.stat().st_mtime) < cutoff_date:
                    filepath.unlink()
                    eliminati += 1
        
        print(f"🧹 Eliminati {eliminati} backup vecchi (oltre {giorni_mantieni} giorni)")
    
    def backup_automatico(self, registro, tipo: str = "giornalieri"):
        """Esegue un backup automatico.
        
        Args:
            registro: Oggetto registro da salvare
            tipo: Tipo di backup
            
        Returns:
            Percorso file salvato
        """
        directory = self.directory_backup / tipo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = str(directory / f"backup_{timestamp}.json")
        
        return self.salva_backup(registro, filepath)
    
    def statistiche_backup(self) -> Dict:
        """Restituisce statistiche sui backup."""
        stats = {}
        
        for tipo in ["giornalieri", "settimanali", "mensili"]:
            directory = self.directory_backup / tipo
            if directory.exists():
                file_list = list(directory.glob("backup_*.json"))
                stats[tipo] = {
                    "conteggio": len(file_list),
                    "dimensione_totale": sum(f.stat().st_size for f in file_list)
                }
                
                if file_list:
                    # Trova più recente e più vecchio
                    files_sorted = sorted(file_list, key=lambda f: f.stat().st_mtime)
                    stats[tipo]["piu_recente"] = files_sorted[-1].name
                    stats[tipo]["piu_vecchio"] = files_sorted[0].name
            else:
                stats[tipo] = {"conteggio": 0, "dimensione_totale": 0}
        
        return stats


class GestoreSincronizzazione:
    """Gestisce la sincronizzazione con archivi esterni."""
    
    def __init__(self, gestore_backup: GestoreBackup):
        """Inizializza il gestore sincronizzazione.
        
        Args:
            gestore_backup: Istanza di GestoreBackup
        """
        self.gestore_backup = gestore_backup
    
    def sincronizza_con_directory(self, registro, directory_esterna: str) -> bool:
        """Sincronizza il backup con una directory esterna.
        
        Args:
            registro: Oggetto registro da sincronizzare
            directory_esterna: Percorso directory esterna
            
        Returns:
            True se riuscito
        """
        try:
            # Crea backup
            filepath = self.gestore_backup.backup_automatico(registro, "giornalieri")
            
            # Copia nella directory esterna
            directory_esterna_path = Path(directory_esterna)
            directory_esterna_path.mkdir(parents=True, exist_ok=True)
            
            filename = Path(filepath).name
            dest = directory_esterna_path / filename
            
            shutil.copy2(filepath, dest)
            
            print(f"✅ Sincronizzato con: {directory_esterna}")
            print(f"📁 File: {dest}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore sincronizzazione: {e}")
            return False
    
    def verifica_integrita(self, filepath: str) -> bool:
        """Verifica l'integrità di un file backup.
        
        Args:
            filepath: Percorso del file
            
        Returns:
            True se il file è integro
        """
        try:
            dati = self.gestore_backup.carica_backup(filepath)
            
            # Ricrea JSON e verifica hash
            json_str = json.dumps(dati, indent=2, ensure_ascii=False)
            hash_calcolato = hashlib.sha256(json_str.encode()).hexdigest()
            hash_salvato = dati["metadata"].get("hash", "")
            
            return hash_calcolato == hash_salvato
            
        except Exception:
            return False


if __name__ == "__main__":
    print("💾 TEST SISTEMA BACKUP E SINCRONIZZAZIONE")
    print("=" * 60 + "\n")
    
    # Crea gestore backup
    gestore = GestoreBackup()
    
    # Crea registro di test
    from main import RegistroScolastico
    registro_test = RegistroScolastico()
    registro_test.anagrafica.genera_studenti(5)
    
    # Backup automatico
    print("📦 Backup automatico...")
    filepath = gestore.backup_automatico(registro_test, "giornalieri")
    
    # Lista backup disponibili
    print("\n📋 Backup disponibili:")
    backup_lista = gestore.lista_backup_disponibili()
    for backup in backup_lista[:3]:
        print(f"   - {backup['nome']} ({backup['dimensione']} bytes)")
    
    # Statistiche
    print("\n📊 Statistiche backup:")
    stats = gestore.statistiche_backup()
    for tipo, dati in stats.items():
        if dati["conteggio"] > 0:
            print(f"   {tipo}: {dati['conteggio']} file, {dati['dimensione_totale']} bytes")
    
    # Verifica integrità
    print("\n🔐 Verifica integrità:")
    sincro = GestoreSincronizzazione(gestore)
    integrita = sincro.verifica_integrita(filepath)
    print(f"   File integro: {'✅ Sì' if integrita else '❌ No'}")
    
    print("\n✅ Test completato!")

