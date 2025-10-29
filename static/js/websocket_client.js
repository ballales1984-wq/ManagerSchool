/**
 * WEBSOCKET CLIENT - ManagerSchool
 * Client JavaScript per connessione real-time
 */

class WebSocketClient {
    constructor(url = '/') {
        this.url = url;
        this.socket = null;
        this.subscriptions = new Set();
        this.eventHandlers = new Map();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }
    
    connect() {
        console.log('🔌 Tentativo connessione WebSocket...');
        
        try {
            this.socket = io(this.url);
            
            this.socket.on('connect', () => {
                console.log('✅ Connesso al server real-time');
                this.reconnectAttempts = 0;
                this.onConnected();
            });
            
            this.socket.on('disconnect', () => {
                console.log('❌ Disconnesso dal server');
                this.onDisconnected();
                this.attemptReconnect();
            });
            
            this.socket.on('connected', (data) => {
                console.log('📡 Server:', data.message);
            });
            
            this.socket.on('event', (data) => {
                this.handleEvent(data.type, data.data);
            });
            
            this.socket.on('subscribed', (data) => {
                console.log('📢 Sottoscritto a:', data.event);
            });
            
        } catch (error) {
            console.error('❌ Errore connessione WebSocket:', error);
        }
    }
    
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            console.log('🔌 Disconnesso manualmente');
        }
    }
    
    subscribe(eventType) {
        if (!this.socket || !this.socket.connected) {
            console.error('❌ Socket non connesso');
            return;
        }
        
        this.subscriptions.add(eventType);
        this.socket.emit('subscribe', { event: eventType });
    }
    
    unsubscribe(eventType) {
        if (!this.socket || !this.socket.connected) {
            return;
        }
        
        this.subscriptions.delete(eventType);
        this.socket.emit('unsubscribe', { event: eventType });
    }
    
    on(eventType, handler) {
        if (!this.eventHandlers.has(eventType)) {
            this.eventHandlers.set(eventType, []);
        }
        this.eventHandlers.get(eventType).push(handler);
    }
    
    off(eventType, handler) {
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }
    
    handleEvent(eventType, data) {
        console.log(`📬 Evento ricevuto: ${eventType}`, data);
        
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            handlers.forEach(handler => handler(data));
        }
    }
    
    onConnected() {
        // Ricosottoscrivi a tutti gli eventi
        this.subscriptions.forEach(eventType => {
            this.subscribe(eventType);
        });
    }
    
    onDisconnected() {
        // Trigger disconnect handlers
        if (this.eventHandlers.has('disconnect')) {
            this.handleEvent('disconnect', {});
        }
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = 1000 * this.reconnectAttempts; // Exponential backoff
            
            console.log(`🔄 Reconnect tentativo ${this.reconnectAttempts}/${this.maxReconnectAttempts} tra ${delay}ms...`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('❌ Max tentativi riconnessione raggiunti');
        }
    }
    
    isConnected() {
        return this.socket && this.socket.connected;
    }
}


// ========================================
// HELPER FUNCTIONS
// ========================================

function initRealtimeSync() {
    const wsClient = new WebSocketClient();
    wsClient.connect();
    
    // Sottoscrivi agli eventi principali
    wsClient.subscribe('nuovo_voto');
    wsClient.subscribe('studente_modificato');
    wsClient.subscribe('presenza_registrata');
    wsClient.subscribe('nuova_comunicazione');
    
    // Event handlers
    wsClient.on('nuovo_voto', (data) => {
        console.log('📊 Nuovo voto inserito:', data);
        
        // Aggiorna UI
        if (typeof refreshVoti !== 'undefined') {
            refreshVoti();
        }
        
        // Mostra notifica
        showNotification('Nuovo voto inserito!', 'info');
    });
    
    wsClient.on('studente_modificato', (data) => {
        console.log('👤 Studente modificato:', data);
        
        // Aggiorna UI
        if (typeof refreshStudenti !== 'undefined') {
            refreshStudenti();
        }
    });
    
    wsClient.on('presenza_registrata', (data) => {
        console.log('📅 Presenza registrata:', data);
        
        showNotification('Presenza registrata!', 'success');
    });
    
    wsClient.on('nuova_comunicazione', (data) => {
        console.log('💬 Nuova comunicazione:', data);
        
        showNotification('Nuova comunicazione!', 'info');
    });
    
    // Esponi globalmente
    window.wsClient = wsClient;
    
    return wsClient;
}


function showNotification(message, type = 'info') {
    // Crea elemento notifica
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#43e97b' : type === 'error' ? '#f5576c' : '#667eea'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Rimuovi dopo 3 secondi
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}


// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inizializzazione Real-time Sync...');
    initRealtimeSync();
});


// ========================================
// EXPORTS
// ========================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        WebSocketClient,
        initRealtimeSync
    };
}

