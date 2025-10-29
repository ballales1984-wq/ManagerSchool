"""
WebSocket Server per Realtime Sync - ManagerSchool
Usa Flask-SocketIO per sincronizzazione real-time
"""

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from typing import Dict, List, Any
import json


class RealtimeServer:
    """Server WebSocket per sincronizzazione real-time."""
    
    def __init__(self, app=None):
        """Inizializza server WebSocket.
        
        Args:
            app: Flask app
        """
        self.socketio = None
        self.app = app
        self.connected_clients = {}  # session_id -> user_info
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Inizializza Flask-SocketIO su app.
        
        Args:
            app: Flask app
        """
        self.app = app
        
        # Configurazione SocketIO
        self.socketio = SocketIO(
            app,
            cors_allowed_origins="*",
            async_mode='threading',
            logger=True,
            engineio_logger=True
        )
        
        # Registra event handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Registra event handlers."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Gestisce connessione client."""
            print(f"✅ Client connesso: {self.socketio.server.session}")
            emit('connected', {'message': 'Connesso al server real-time'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Gestisce disconnessione client."""
            print(f"❌ Client disconnesso")
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            """Gestisce sottoscrizione a evento."""
            event_type = data.get('event')
            room = f"event_{event_type}"
            join_room(room)
            emit('subscribed', {'event': event_type, 'room': room})
        
        @self.socketio.on('unsubscribe')
        def handle_unsubscribe(data):
            """Gestisce rimozione sottoscrizione."""
            event_type = data.get('event')
            room = f"event_{event_type}"
            leave_room(room)
            emit('unsubscribed', {'event': event_type})
        
        @self.socketio.on('join_room')
        def handle_join_room(data):
            """Gestisce join in room."""
            room = data.get('room')
            if room:
                join_room(room)
                emit('room_joined', {'room': room})
        
        @self.socketio.on('leave_room')
        def handle_leave_room(data):
            """Gestisce leave da room."""
            room = data.get('room')
            if room:
                leave_room(room)
                emit('room_left', {'room': room})
    
    def broadcast_event(self, event_type: str, data: Any):
        """Broadcast evento a tutti i client sottoscritti.
        
        Args:
            event_type: Tipo evento
            data: Dati evento
        """
        if not self.socketio:
            return
        
        room = f"event_{event_type}"
        self.socketio.emit('event', {
            'type': event_type,
            'data': data
        }, room=room)
    
    def notify_voto_inserito(self, voto_data: Dict):
        """Notifica nuovo voto inserito.
        
        Args:
            voto_data: Dati voto
        """
        self.broadcast_event('nuovo_voto', voto_data)
    
    def notify_studente_modificato(self, studente_data: Dict):
        """Notifica modifica studente.
        
        Args:
            studente_data: Dati studente
        """
        self.broadcast_event('studente_modificato', studente_data)
    
    def notify_presenza_registrata(self, presenza_data: Dict):
        """Notifica presenza registrata.
        
        Args:
            presenza_data: Dati presenza
        """
        self.broadcast_event('presenza_registrata', presenza_data)
    
    def notify_comunicazione_inviata(self, comunicazione_data: Dict):
        """Notifica nuova comunicazione.
        
        Args:
            comunicazione_data: Dati comunicazione
        """
        self.broadcast_event('nuova_comunicazione', comunicazione_data)
    
    def get_connected_clients(self) -> int:
        """Ottiene numero client connessi.
        
        Returns:
            Numero client
        """
        if self.socketio:
            # Flask-SocketIO doesn't provide direct client count
            # This is a simplified version
            return len(self.connected_clients)
        return 0


# Instanza globale
realtime_server = None


def init_realtime(app: Flask) -> RealtimeServer:
    """Inizializza realtime server.
    
    Args:
        app: Flask app
        
    Returns:
        RealtimeServer instance
    """
    global realtime_server
    realtime_server = RealtimeServer(app)
    return realtime_server


if __name__ == "__main__":
    print("REALTIME WEBSOCKET SERVER - TEST")
    print("=" * 60 + "\n")
    
    # Test setup
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    server = RealtimeServer(app)
    
    print("✅ Server WebSocket inizializzato")
    print("   Eventi supportati:")
    print("   - nuovo_voto")
    print("   - studente_modificato")
    print("   - presenza_registrata")
    print("   - nuova_comunicazione")
    
    print("\nPer usare il server:")
    print("   server.notify_voto_inserito({'voto': 8, 'materia': 'Matematica'})")

