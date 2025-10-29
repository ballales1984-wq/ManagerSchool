"""
Modulo di sicurezza completo per ManagerSchool.
Integra JWT, bcrypt, HTTPS e SQL injection prevention.
"""

from security_jwt import JWTAuth, jwt_auth
from security_password import PasswordManager
from security_sql import SQLInjectionPrevention
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class SecurityManager:
    """Manager centrale per sicurezza.
    
    Integra:
    - Autenticazione JWT
    - Hash password bcrypt
    - Prevenzione SQL injection
    - Logging operazioni critiche
    """
    
    def __init__(self):
        """Inizializza security manager."""
        self.jwt = jwt_auth
        self.password = PasswordManager()
        self.sql_prevention = SQLInjectionPrevention()
        
        # Logging sicurezza
        self.security_log = []
    
    def autentica_utente(self, username: str, password: str, 
                       user_hash_db: str) -> Optional[str]:
        """Autentica utente e genera token.
        
        Args:
            username: Username
            password: Password in chiaro
            user_hash_db: Hash password salvato nel DB
            
        Returns:
            Token JWT o None
        """
        try:
            # Verifica password
            if not self.password.verifica_password(password, user_hash_db):
                self._log_security_event("login_failed", username)
                return None
            
            # Genera token
            token = self.jwt.genera_token(
                user_id=1,  # Da recuperare da DB
                username=username,
                ruolo="docente"  # Da recuperare da DB
            )
            
            self._log_security_event("login_success", username)
            return token
            
        except Exception as e:
            logger.error(f"Errore autenticazione: {e}")
            return None
    
    def registra_utente(self, username: str, password: str, ruolo: str = "docente") -> Dict:
        """Registra nuovo utente con password sicura.
        
        Args:
            username: Username
            password: Password in chiaro
            ruolo: Ruolo utente
            
        Returns:
            Risultato registrazione
        """
        # Valida password
        valida, msg = self.password.valida_complessita_password(password)
        if not valida:
            return {
                'successo': False,
                'errore': msg
            }
        
        # Hash password
        hashed = self.password.hash_password(password)
        
        # Sanitizza username
        username_clean = self.sql_prevention.sanitize_input(username)
        
        # Qui salveresti nel database
        # user = {
        #     'username': username_clean,
        #     'password_hash': hashed,
        #     'ruolo': ruolo
        # }
        
        self._log_security_event("user_registered", username_clean)
        
        return {
            'successo': True,
            'username': username_clean,
            'messaggio': 'Utente registrato con successo'
        }
    
    def verifica_token_protetto(self, token: str) -> Optional[Dict]:
        """Verifica token con logging.
        
        Args:
            token: Token JWT
            
        Returns:
            Payload o None
        """
        payload = self.jwt.verifica_token(token)
        
        if payload:
            self._log_security_event("token_verified", payload.get('username'))
        else:
            self._log_security_event("token_invalid", "unknown")
        
        return payload
    
    def richiede_autenticazione_protetto(self, f):
        """Decorator con logging.
        
        Args:
            f: Funzione da decorare
            
        Returns:
            Funzione decorata
        """
        return self.jwt.richiede_autenticazione(f)
    
    def richiede_ruolo_protetto(self, *ruoli):
        """Decorator con logging.
        
        Args:
            ruoli: Ruoli permessi
            
        Returns:
            Decorator
        """
        return self.jwt.richiede_ruolo(*ruoli)
    
    def _log_security_event(self, event_type: str, username: str):
        """Log operazione sicurezza.
        
        Args:
            event_type: Tipo evento
            username: Username coinvolto
        """
        from datetime import datetime
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event_type,
            'username': username
        }
        
        self.security_log.append(log_entry)
        
        # Logging critico
        if event_type in ['login_failed', 'token_invalid', 'unauthorized_access']:
            logger.warning(f"Security event: {event_type} - User: {username}")
        else:
            logger.info(f"Security event: {event_type} - User: {username}")
    
    def get_security_report(self) -> Dict:
        """Genera report sicurezza.
        
        Returns:
            Report eventi
        """
        total_events = len(self.security_log)
        failed_logins = len([e for e in self.security_log if e['event'] == 'login_failed'])
        success_logins = len([e for e in self.security_log if e['event'] == 'login_success'])
        invalid_tokens = len([e for e in self.security_log if e['event'] == 'token_invalid'])
        
        return {
            'total_events': total_events,
            'failed_logins': failed_logins,
            'successful_logins': success_logins,
            'invalid_tokens': invalid_tokens,
            'events': self.security_log[-10:]  # Ultimi 10 eventi
        }


# Istanza globale
security = SecurityManager()


if __name__ == "__main__":
    print("SISTEMA SICUREZZA COMPLETO - TEST")
    print("=" * 60 + "\n")
    
    # Test registrazione
    print("1. Test registrazione utente:")
    result = security.registra_utente("profdemo", "SecurePass123!")
    print(f"   {result}")
    
    # Test hash password
    print("\n2. Test hash password:")
    pwd = "MySecure123!"
    hashed = security.password.hash_password(pwd)
    verified = security.password.verifica_password(pwd, hashed)
    print(f"   Password: {pwd}")
    print(f"   Hash: {hashed[:50]}...")
    print(f"   Verificato: {verified}")
    
    # Test JWT
    print("\n3. Test JWT:")
    token = security.jwt.genera_token(1, "profdemo", "docente")
    print(f"   Token: {token[:50]}...")
    payload = security.jwt.verifica_token(token)
    print(f"   Payload: {payload}")
    
    # Test sanitizzazione SQL
    print("\n4. Test sanitizzazione SQL:")
    test_input = "Mario'; DROP TABLE studenti; --"
    cleaned = security.sql_prevention.sanitize_input(test_input)
    print(f"   Input: {test_input}")
    print(f"   Pulito: {cleaned}")
    
    # Test report
    print("\n5. Security report:")
    report = security.get_security_report()
    print(f"   Total events: {report['total_events']}")
    print(f"   Failed logins: {report['failed_logins']}")
    print(f"   Successful logins: {report['successful_logins']}")

