"""
Event Broadcaster - ManagerSchool
Gestisce broadcast eventi real-time
"""

from typing import Dict, Any, Callable
from datetime import datetime
import json


class EventBroadcaster:
    """Broadcaster per eventi real-time."""
    
    def __init__(self):
        """Inizializza broadcaster."""
        self.handlers = {}  # event_type -> [handlers]
        self.event_history = []  # Cronologia eventi
        self.max_history = 100
    
    def register_handler(self, event_type: str, handler: Callable):
        """Registra handler per evento.
        
        Args:
            event_type: Tipo evento
            handler: Funzione handler
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        
        self.handlers[event_type].append(handler)
    
    def broadcast(self, event_type: str, data: Any):
        """Broadcast evento.
        
        Args:
            event_type: Tipo evento
            data: Dati evento
        """
        # Aggiungi a cronologia
        self.event_history.append({
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        
        # Mantieni solo ultimi eventi
        if len(self.event_history) > self.max_history:
            self.event_history = self.event_history[-self.max_history:]
        
        # Chiama handlers
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(event_type, data)
                except Exception as e:
                    print(f"❌ Errore handler {event_type}: {e}")
    
    def get_event_history(self, event_type: str = None, limit: int = 10) -> list:
        """Ottiene cronologia eventi.
        
        Args:
            event_type: Filtra per tipo (opzionale)
            limit: Limite risultati
            
        Returns:
            Lista eventi
        """
        events = self.event_history
        
        if event_type:
            events = [e for e in events if e['type'] == event_type]
        
        return events[-limit:]
    
    def clear_history(self):
        """Pulisce cronologia eventi."""
        self.event_history.clear()


# Istanza globale
event_broadcaster = EventBroadcaster()


# Eventi supportati
class RealtimeEvents:
    """Definizione eventi real-time."""
    
    NUOVO_VOTO = 'nuovo_voto'
    VOTO_MODIFICATO = 'voto_modificato'
    VOTO_ELIMINATO = 'voto_eliminato'
    
    STUDENTE_AGGIUNTO = 'studente_aggiunto'
    STUDENTE_MODIFICATO = 'studente_modificato'
    STUDENTE_ELIMINATO = 'studente_eliminato'
    
    PRESENZA_REGISTRATA = 'presenza_registrata'
    ASSENZA_REGISTRATA = 'assenza_registrata'
    
    COMUNICAZIONE_INVIATA = 'comunicazione_inviata'
    COMUNICAZIONE_LETTA = 'comunicazione_letta'
    
    BACKUP_CREATO = 'backup_creato'
    REPORT_GENERATO = 'report_generato'


if __name__ == "__main__":
    print("EVENT BROADCASTER - TEST")
    print("=" * 60 + "\n")
    
    # Test broadcaster
    def test_handler(event_type, data):
        print(f"📬 Evento ricevuto: {event_type}")
        print(f"   Dati: {data}")
    
    event_broadcaster.register_handler('nuovo_voto', test_handler)
    
    # Broadcast test
    event_broadcaster.broadcast('nuovo_voto', {
        'id_studente': 1,
        'materia': 'Matematica',
        'voto': 8.0
    })
    
    # Cronologia
    history = event_broadcaster.get_event_history('nuovo_voto')
    print(f"\n📜 Cronologia eventi: {len(history)} eventi")

