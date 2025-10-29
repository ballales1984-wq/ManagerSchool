"""
Sistema di sicurezza JWT per ManagerSchool.
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from functools import wraps
from flask import request, jsonify, g
import secrets


class JWTAuth:
    """Gestione autenticazione JWT."""
    
    def __init__(self, secret_key: Optional[str] = None):
        """Inizializza gestore JWT.
        
        Args:
            secret_key: Chiave segreta (default: auto-generata)
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = 'HS256'
        self.token_expiry = timedelta(hours=8)
    
    def genera_token(self, user_id: int, username: str, ruolo: str) -> str:
        """Genera token JWT.
        
        Args:
            user_id: ID utente
            username: Nome utente
            ruolo: Ruolo (docente, dirigente, segreteria)
            
        Returns:
            Token JWT
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'ruolo': ruolo,
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verifica_token(self, token: str) -> Optional[Dict]:
        """Verifica e decodifica token JWT.
        
        Args:
            token: Token da verificare
            
        Returns:
            Payload decodificato o None
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def richiede_autenticazione(self, f):
        """Decorator per richiedere autenticazione JWT."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Prova a ottenere token da header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(' ')[1]  # "Bearer <token>"
                except IndexError:
                    return jsonify({'errore': 'Token malformato'}), 401
            
            if not token:
                return jsonify({'errore': 'Token mancante'}), 401
            
            # Verifica token
            payload = self.verifica_token(token)
            if payload is None:
                return jsonify({'errore': 'Token non valido o scaduto'}), 401
            
            # Aggiungi info utente a g
            g.current_user = payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    def richiede_ruolo(self, *ruoli_richiesti):
        """Decorator per richiedere ruoli specifici.
        
        Args:
            ruoli_richiesti: Ruoli permessi
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Assumendo che richiede_autenticazione sia già applicato
                user_ruolo = g.current_user.get('ruolo')
                
                if user_ruolo not in ruoli_richiesti:
                    return jsonify({
                        'errore': f'Ruolo insufficiente. Richiesto: {ruoli_richiesti}'
                    }), 403
                
                return f(*args, **kwargs)
            
            return decorated_function
        return decorator


# Istanza globale
jwt_auth = JWTAuth()


if __name__ == "__main__":
    print("SISTEMA SICUREZZA JWT - TEST")
    print("=" * 60 + "\n")
    
    # Test generazione token
    token = jwt_auth.genera_token(1, "profdemo", "docente")
    print(f"Token generato: {token[:50]}...")
    
    # Test verifica token
    payload = jwt_auth.verifica_token(token)
    if payload:
        print(f"Token valido!")
        print(f"   User ID: {payload['user_id']}")
        print(f"   Username: {payload['username']}")
        print(f"   Ruolo: {payload['ruolo']}")
    else:
        print("Token non valido")

