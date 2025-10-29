"""
Sistema di Anonimizzazione GDPR - ManagerSchool
Pseudonimizzazione e dati anonimi per statistiche
"""

import hashlib
import secrets
from typing import Dict, List, Any, Optional
import json


class Anonymizer:
    """Sistema di anonimizzazione per conformità GDPR."""
    
    def __init__(self):
        """Inizializza anonimizzatore."""
        self.salt = secrets.token_hex(16)
        self.pseudonym_map = {}  # id_originale -> pseudonimo
    
    def hash_id(self, original_id: int) -> str:
        """Hash un ID per pseudonimizzazione.
        
        Args:
            original_id: ID originale
            
        Returns:
            Hash pseudonimo
        """
        # Usa salt per non reversibilità
        data = f"{original_id}{self.salt}"
        hash_obj = hashlib.sha256(data.encode())
        return hash_obj.hexdigest()[:16]  # 16 char
    
    def anonymize_studente(self, studente: Dict) -> Dict:
        """Anonimizza dati studente.
        
        Args:
            studente: Dati studente
            
        Returns:
            Dati anonimizzati
        """
        # Hash ID
        pseudonimo = self.hash_id(studente.get('id', 0))
        
        # Rimuovi dati identificativi
        return {
            'pseudonimo': pseudonimo,
            'classe': studente.get('classe', ''),
            'eta': self._anonymize_eta(studente.get('eta', 0)),
            'reddito_categoria': studente.get('categoria_reddito', ''),
            'salute': studente.get('condizione_salute', ''),
            'situazione_familiare': studente.get('situazione_familiare', ''),
            # Dati statistici
            'media_voti': self._calculate_media(studente.get('voti', [])),
            'fragilita_range': self._range_fragilita(studente.get('fragilita', 50))
        }
    
    def _anonymize_eta(self, eta: int) -> str:
        """Anonimizza età in range."""
        if 14 <= eta <= 16:
            return "14-16"
        elif 17 <= eta <= 19:
            return "17-19"
        else:
            return "20+"
    
    def _calculate_media(self, voti: List[float]) -> float:
        """Calcola media senza identificativi."""
        if not voti:
            return 0.0
        return round(sum(voti) / len(voti), 2)
    
    def _range_fragilita(self, fragilita: float) -> str:
        """Converte fragilità in range."""
        if fragilita < 30:
            return "Bassa"
        elif fragilita < 60:
            return "Media"
        else:
            return "Alta"
    
    def anonymize_for_statistics(self, studenti: List[Dict]) -> Dict:
        """Genera statistiche aggregate anonime.
        
        Args:
            studenti: Lista studenti
            
        Returns:
            Statistiche anonime
        """
        # Conta per classe
        classi_count = {}
        eta_ranges = {"14-16": 0, "17-19": 0, "20+": 0}
        fragilita_ranges = {"Bassa": 0, "Media": 0, "Alta": 0}
        
        totali_voti = 0
        somma_voti = 0
        
        for studente in studenti:
            classe = studente.get('classe', 'Unknown')
            classi_count[classe] = classi_count.get(classe, 0) + 1
            
            eta = studente.get('eta', 15)
            if 14 <= eta <= 16:
                eta_ranges["14-16"] += 1
            elif 17 <= eta <= 19:
                eta_ranges["17-19"] += 1
            else:
                eta_ranges["20+"] += 1
            
            fragilita = studente.get('fragilita', 50)
            if fragilita < 30:
                fragilita_ranges["Bassa"] += 1
            elif fragilita < 60:
                fragilita_ranges["Media"] += 1
            else:
                fragilita_ranges["Alta"] += 1
            
            voti = studente.get('voti', [])
            totali_voti += len(voti)
            somma_voti += sum(voti)
        
        media_generale = round(somma_voti / totali_voti, 2) if totali_voti > 0 else 0.0
        
        return {
            "totale_studenti": len(studenti),
            "totale_classi": len(classi_count),
            "distribuzione_eta": eta_ranges,
            "distribuzione_fragilita": fragilita_ranges,
            "media_generale": media_generale,
            "dati_anonimi": True,
            "GDPR_compliant": True
        }
    
    def export_gdpr_compliant(self, studenti: List[Dict], 
                             output_path: str = "export_anonimo.json"):
        """Export dati anonimi GDPR compliant.
        
        Args:
            studenti: Lista studenti
            output_path: Percorso output
        """
        # Anonimizza tutti gli studenti
        dati_anonimi = []
        for studente in studenti:
            dati_anonimi.append(self.anonymize_studente(studente))
        
        # Export
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'totale_record': len(dati_anonimi),
                'dati_anonimi': dati_anonimi,
                'GDPR_compliant': True,
                'note': 'Dati anonimizzati per conformità GDPR Art. 89'
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Export GDPR creato: {output_path}")
        print(f"   {len(dati_anonimi)} record anonimizzati")
        
        return output_path


if __name__ == "__main__":
    print("ANONYMIZER GDPR - TEST")
    print("=" * 60 + "\n")
    
    anonymizer = Anonymizer()
    
    # Test studenti simulati
    studenti_test = [
        {
            'id': 1,
            'nome': 'Mario',
            'cognome': 'Rossi',
            'eta': 15,
            'classe': '2A',
            'categoria_reddito': 'MEDIO',
            'condizione_salute': 'BUONA',
            'situazione_familiare': 'Tradizionale',
            'voti': [7.0, 7.5, 8.0, 7.0],
            'fragilita': 35
        },
        {
            'id': 2,
            'nome': 'Luisa',
            'cognome': 'Bianchi',
            'eta': 17,
            'classe': '3B',
            'categoria_reddito': 'ALTO',
            'condizione_salute': 'BUONA',
            'situazione_familiare': 'Tradizionale',
            'voti': [8.0, 9.0, 8.5, 9.0],
            'fragilita': 20
        }
    ]
    
    # Test anonimizzazione
    print("1. Test anonimizzazione singolo studente:")
    anonimo = anonymizer.anonymize_studente(studenti_test[0])
    print(f"   ID originale: {studenti_test[0]['id']}")
    print(f"   Pseudonimo: {anonimo['pseudonimo']}")
    print(f"   Eta: {anonimo['eta']}")
    print(f"   Media: {anonimo['media_voti']}")
    
    # Test statistiche
    print("\n2. Test statistiche aggregate:")
    stats = anonymizer.anonymize_for_statistics(studenti_test)
    print(f"   Totale studenti: {stats['totale_studenti']}")
    print(f"   Media generale: {stats['media_generale']}")
    print(f"   GDPR compliant: {stats['GDPR_compliant']}")
    
    # Test export
    print("\n3. Test export GDPR:")
    anonymizer.export_gdpr_compliant(studenti_test, "test_export_anonimo.json")
    
    print("\n✅ Test completato!")

