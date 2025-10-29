"""
Sistema di hash password con bcrypt.
"""

import bcrypt
from typing import Tuple, Optional


class PasswordManager:
    """Gestisce hash e verifica password."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash password con bcrypt.
        
        Args:
            password: Password in chiaro
            
        Returns:
            Hash password
        """
        # Genera salt e hash
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verifica_password(password: str, hash_password: str) -> bool:
        """Verifica password contro hash.
        
        Args:
            password: Password in chiaro
            hash_password: Hash salvato
            
        Returns:
            True se password corretta
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hash_password.encode('utf-8')
        )
    
    @staticmethod
    def valida_complessita_password(password: str) -> Tuple[bool, str]:
        """Valida complessità password.
        
        Args:
            password: Password da validare
            
        Returns:
            (valida, messaggio)
        """
        if len(password) < 8:
            return False, "Password deve avere almeno 8 caratteri"
        
        if not any(c.isupper() for c in password):
            return False, "Password deve contenere almeno una maiuscola"
        
        if not any(c.islower() for c in password):
            return False, "Password deve contenere almeno una minuscola"
        
        if not any(c.isdigit() for c in password):
            return False, "Password deve contenere almeno un numero"
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password deve contenere almeno un carattere speciale"
        
        return True, "Password valida"
    
    @staticmethod
    def genera_password_sicura(length: int = 16) -> str:
        """Genera password sicura casuale.
        
        Args:
            length: Lunghezza password
            
        Returns:
            Password generata
        """
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        return password


if __name__ == "__main__":
    print("SISTEMA SICUREZZA PASSWORD - TEST")
    print("=" * 60 + "\n")
    
    # Test hash
    password = "MySecure123!"
    hashed = PasswordManager.hash_password(password)
    print(f"Password originale: {password}")
    print(f"Hash generato: {hashed}")
    
    # Test verifica
    is_valid = PasswordManager.verifica_password(password, hashed)
    print(f"\nVerifica password: {'✓ Corretto' if is_valid else '✗ Errato'}")
    
    # Test validazione
    test_passwords = [
        "weak",
        "weakNoSpecial",
        "WeakNoSpecial123",
        "StrongPass123!",
        "VeryStrongPass123!@#"
    ]
    
    print("\nTest validazione password:")
    for pwd in test_passwords:
        valida, msg = PasswordManager.valida_complessita_password(pwd)
        status = "✓" if valida else "✗"
        print(f"  {status} '{pwd}' -> {msg}")
    
    # Test generazione
    print("\nPassword sicure generate:")
    for _ in range(3):
        safe_pwd = PasswordManager.genera_password_sicura(16)
        print(f"  {safe_pwd}")

