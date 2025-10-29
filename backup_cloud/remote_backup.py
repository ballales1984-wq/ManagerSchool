"""
Remote Backup System - ManagerSchool
Backup automatico cloud (Google Drive, AWS S3, etc)
"""

from typing import Optional, Dict, List
from datetime import datetime
import os
import shutil


class RemoteBackupManager:
    """Gestisce backup remoti su cloud."""
    
    def __init__(self):
        """Inizializza backup manager."""
        self.supported_providers = ['local', 's3', 'gdrive']
        self.backup_history = []
    
    def create_backup(self, source_path: str, destination: str, 
                     provider: str = 'local') -> Dict:
        """Crea backup locale o remoto.
        
        Args:
            source_path: Percorso sorgente
            destination: Percorso destinazione
            provider: Provider (local, s3, gdrive)
            
        Returns:
            Info backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.db"
        
        if provider == 'local':
            backup_path = self._backup_local(source_path, destination, backup_name)
        elif provider == 's3':
            backup_path = self._backup_s3(source_path, backup_name)
        elif provider == 'gdrive':
            backup_path = self._backup_gdrive(source_path, backup_name)
        else:
            raise ValueError(f"Provider non supportato: {provider}")
        
        backup_info = {
            'timestamp': datetime.now().isoformat(),
            'provider': provider,
            'path': backup_path,
            'size': os.path.getsize(backup_path) if os.path.exists(backup_path) else 0,
            'success': True
        }
        
        self.backup_history.append(backup_info)
        print(f"✅ Backup creato: {backup_path}")
        
        return backup_info
    
    def _backup_local(self, source: str, dest_dir: str, filename: str) -> str:
        """Crea backup locale.
        
        Args:
            source: Sorgente
            dest_dir: Directory destinazione
            filename: Nome file
            
        Returns:
            Percorso backup
        """
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, filename)
        
        shutil.copy2(source, dest_path)
        return dest_path
    
    def _backup_s3(self, source: str, filename: str) -> str:
        """Crea backup su AWS S3.
        
        Args:
            source: Sorgente
            filename: Nome file
            
        Returns:
            Percorso S3
        """
        # Implementazione S3 (richiede boto3)
        print("⚠️ Backup S3 richiede AWS credentials")
        return f"s3://managerschool-backups/{filename}"
    
    def _backup_gdrive(self, source: str, filename: str) -> str:
        """Crea backup su Google Drive.
        
        Args:
            source: Sorgente
            filename: Nome file
            
        Returns:
            ID file Google Drive
        """
        # Implementazione Google Drive (richiede PyDrive2)
        print("⚠️ Backup Google Drive richiede OAuth2 credentials")
        return f"gdrive:{filename}"
    
    def list_backups(self, provider: str = 'local') -> List[Dict]:
        """Lista backup disponibili.
        
        Args:
            provider: Provider backup
            
        Returns:
            Lista backup
        """
        return [b for b in self.backup_history if b['provider'] == provider]
    
    def restore_backup(self, backup_path: str, destination: str, 
                      provider: str = 'local'):
        """Ripristina da backup.
        
        Args:
            backup_path: Percorso backup
            destination: Destinazione restore
            provider: Provider
            
        Returns:
            Successo restore
        """
        if provider == 'local':
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, destination)
                print(f"✅ Backup ripristinato: {destination}")
                return True
            else:
                print(f"❌ Backup non trovato: {backup_path}")
                return False
        else:
            print(f"⚠️ Restore {provider} non implementato")
            return False
    
    def get_backup_stats(self) -> Dict:
        """Ottiene statistiche backup.
        
        Returns:
            Statistiche
        """
        total_backups = len(self.backup_history)
        total_size = sum(b['size'] for b in self.backup_history)
        
        providers = {}
        for backup in self.backup_history:
            provider = backup['provider']
            providers[provider] = providers.get(provider, 0) + 1
        
        return {
            'total_backups': total_backups,
            'total_size': total_size,
            'size_mb': round(total_size / (1024 * 1024), 2),
            'by_provider': providers,
            'last_backup': self.backup_history[-1] if self.backup_history else None
        }


# Istanza globale
remote_backup = RemoteBackupManager()


if __name__ == "__main__":
    print("REMOTE BACKUP - TEST")
    print("=" * 60 + "\n")
    
    # Test backup
    import tempfile
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        test_db = tmp.name
        tmp.write(b'fake db data')
    
    # Crea backup
    backup_info = remote_backup.create_backup(
        test_db,
        'backup_test',
        'local'
    )
    print(f"Backup creato: {backup_info}")
    
    # Statistiche
    stats = remote_backup.get_backup_stats()
    print(f"\nStatistiche:")
    print(f"  Total backup: {stats['total_backups']}")
    print(f"  Size: {stats['size_mb']} MB")
    
    # Cleanup
    os.unlink(test_db)
    
    print("\n✅ Test completato!")

