"""
Data Versioning System - ManagerSchool
Tracciamento modifiche e storico dati
"""

from typing import Dict, List, Optional
from datetime import datetime
import json


class DataVersioning:
    """Sistema di versioning dati con storico completo."""
    
    def __init__(self):
        """Inizializza sistema versioning."""
        self.history = []  # Lista di tutte le modifiche
        self.version_counter = 0
    
    def register_change(self, entity_type: str, entity_id: int, 
                       old_value: Dict, new_value: Dict,
                       user: str, action: str = "update"):
        """Registra modifica nei dati.
        
        Args:
            entity_type: Tipo entità (studente, voto, etc)
            entity_id: ID entità
            old_value: Valore precedente
            new_value: Valore nuovo
            user: Utente che ha modificato
            action: Azione (create, update, delete)
        """
        change_record = {
            'version': self.version_counter + 1,
            'timestamp': datetime.now().isoformat(),
            'entity_type': entity_type,
            'entity_id': entity_id,
            'action': action,
            'user': user,
            'old_value': old_value,
            'new_value': new_value,
            'changes': self._calculate_diff(old_value, new_value)
        }
        
        self.history.append(change_record)
        self.version_counter += 1
    
    def _calculate_diff(self, old: Dict, new: Dict) -> Dict:
        """Calcola differenze tra vecchio e nuovo.
        
        Args:
            old: Valore vecchio
            new: Valore nuovo
            
        Returns:
            Dict con differenze
        """
        diff = {}
        
        # Controlla campi modificati
        all_keys = set(old.keys()) | set(new.keys())
        
        for key in all_keys:
            old_val = old.get(key)
            new_val = new.get(key)
            
            if old_val != new_val:
                diff[key] = {
                    'from': old_val,
                    'to': new_val
                }
        
        return diff
    
    def get_entity_history(self, entity_type: str, entity_id: int) -> List[Dict]:
        """Ottiene storico modifiche per entità.
        
        Args:
            entity_type: Tipo entità
            entity_id: ID entità
            
        Returns:
            Lista modifiche
        """
        return [h for h in self.history 
                if h['entity_type'] == entity_type and h['entity_id'] == entity_id]
    
    def get_user_changes(self, user: str) -> List[Dict]:
        """Ottiene modifiche di un utente.
        
        Args:
            user: Username
            
        Returns:
            Lista modifiche
        """
        return [h for h in self.history if h['user'] == user]
    
    def revert_to_version(self, entity_type: str, entity_id: int, 
                         version: int) -> Optional[Dict]:
        """Ripristina a versione specifica.
        
        Args:
            entity_type: Tipo entità
            entity_id: ID entità
            version: Numero versione
            
        Returns:
            Valore versione
        """
        entity_history = self.get_entity_history(entity_type, entity_id)
        
        for change in entity_history:
            if change['version'] == version:
                return change['old_value']
        
        return None
    
    def export_audit_log(self, output_path: str = "audit_log.json"):
        """Esporta log audit completo.
        
        Args:
            output_path: Percorso output
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_changes': len(self.history),
                'changes': self.history
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Audit log esportato: {output_path}")
        return output_path


# Istanza globale
versioning = DataVersioning()


if __name__ == "__main__":
    print("DATA VERSIONING - TEST")
    print("=" * 60 + "\n")
    
    # Simula modifiche
    versioning.register_change(
        'studente', 1,
        {'nome': 'Mario', 'classe': '2A'},
        {'nome': 'Mario', 'classe': '3A'},
        'docente1',
        'update'
    )
    
    versioning.register_change(
        'voto', 1,
        {'voto': 7.0, 'materia': 'Matematica'},
        {'voto': 8.0, 'materia': 'Matematica'},
        'docente1',
        'update'
    )
    
    # Visualizza storico
    history = versioning.get_entity_history('studente', 1)
    print(f"Storico modifiche studente 1: {len(history)} entrate")
    
    # Export audit
    versioning.export_audit_log("test_audit.json")
    
    print("\n✅ Test completato!")

