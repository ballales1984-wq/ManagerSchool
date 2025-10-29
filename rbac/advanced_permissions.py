"""
Advanced RBAC System - ManagerSchool
Sistema avanzato di Role-Based Access Control
"""

from typing import Dict, Set, List, Optional
from dataclasses import dataclass
from enum import Enum


class Permission(str, Enum):
    """Permessi nel sistema."""
    # Studenti
    VIEW_STUDENTS = "view_students"
    EDIT_STUDENTS = "edit_students"
    DELETE_STUDENTS = "delete_students"
    ADD_STUDENTS = "add_students"
    
    # Voti
    VIEW_GRADES = "view_grades"
    ADD_GRADES = "add_grades"
    EDIT_GRADES = "edit_grades"
    DELETE_GRADES = "delete_grades"
    
    # Report
    VIEW_REPORTS = "view_reports"
    GENERATE_REPORTS = "generate_reports"
    EXPORT_REPORTS = "export_reports"
    
    # Presenze
    VIEW_ATTENDANCE = "view_attendance"
    MANAGE_ATTENDANCE = "manage_attendance"
    
    # Comunicazioni
    SEND_COMMUNICATIONS = "send_communications"
    VIEW_COMMUNICATIONS = "view_communications"
    
    # Amministrazione
    MANAGE_BACKUPS = "manage_backups"
    MANAGE_USERS = "manage_users"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_SETTINGS = "manage_settings"


@dataclass
class Role:
    """Ruolo con permessi."""
    name: str
    permissions: Set[Permission]
    description: str = ""


class AdvancedRBAC:
    """Sistema RBAC avanzato."""
    
    def __init__(self):
        """Inizializza RBAC."""
        self.roles = self._initialize_roles()
    
    def _initialize_roles(self) -> Dict[str, Role]:
        """Inizializza ruoli predefiniti."""
        return {
            'amministratore': Role(
                name='Amministratore',
                permissions={Permission.VIEW_STUDENTS, Permission.EDIT_STUDENTS,
                           Permission.DELETE_STUDENTS, Permission.ADD_STUDENTS,
                           Permission.VIEW_GRADES, Permission.ADD_GRADES,
                           Permission.EDIT_GRADES, Permission.DELETE_GRADES,
                           Permission.VIEW_REPORTS, Permission.GENERATE_REPORTS,
                           Permission.EXPORT_REPORTS, Permission.VIEW_ATTENDANCE,
                           Permission.MANAGE_ATTENDANCE, Permission.SEND_COMMUNICATIONS,
                           Permission.VIEW_COMMUNICATIONS, Permission.MANAGE_BACKUPS,
                           Permission.MANAGE_USERS, Permission.VIEW_ANALYTICS,
                           Permission.MANAGE_SETTINGS},
                description='Accesso completo al sistema'
            ),
            'dirigente': Role(
                name='Dirigente',
                permissions={Permission.VIEW_STUDENTS, Permission.VIEW_GRADES,
                           Permission.VIEW_REPORTS, Permission.GENERATE_REPORTS,
                           Permission.EXPORT_REPORTS, Permission.VIEW_ATTENDANCE,
                           Permission.VIEW_ANALYTICS, Permission.MANAGE_SETTINGS},
                description='Visualizzazione completa e configurazione'
            ),
            'docente': Role(
                name='Docente',
                permissions={Permission.VIEW_STUDENTS, Permission.VIEW_GRADES,
                           Permission.ADD_GRADES, Permission.EDIT_GRADES,
                           Permission.VIEW_REPORTS, Permission.VIEW_ATTENDANCE,
                           Permission.MANAGE_ATTENDANCE, Permission.SEND_COMMUNICATIONS,
                           Permission.VIEW_COMMUNICATIONS},
                description='Gestione classi e voti'
            ),
            'segreteria': Role(
                name='Segreteria',
                permissions={Permission.VIEW_STUDENTS, Permission.EDIT_STUDENTS,
                           Permission.ADD_STUDENTS, Permission.VIEW_GRADES,
                           Permission.VIEW_REPORTS, Permission.VIEW_ATTENDANCE,
                           Permission.MANAGE_ATTENDANCE, Permission.SEND_COMMUNICATIONS,
                           Permission.VIEW_COMMUNICATIONS},
                description='Gestione anagrafica e comunicazioni'
            ),
            'genitore': Role(
                name='Genitore',
                permissions={Permission.VIEW_STUDENTS, Permission.VIEW_GRADES,
                           Permission.VIEW_REPORTS, Permission.VIEW_ATTENDANCE,
                           Permission.VIEW_COMMUNICATIONS},
                description='Visualizzazione dati del figlio'
            ),
            'studente': Role(
                name='Studente',
                permissions={Permission.VIEW_GRADES, Permission.VIEW_REPORTS,
                           Permission.VIEW_ATTENDANCE},
                description='Visualizzazione propri voti'
            )
        }
    
    def has_permission(self, ruolo: str, permission: Permission) -> bool:
        """Controlla se un ruolo ha un permesso.
        
        Args:
            ruolo: Nome ruolo
            permission: Permesso da controllare
            
        Returns:
            True se ha permesso
        """
        if ruolo not in self.roles:
            return False
        
        return permission in self.roles[ruolo].permissions
    
    def get_role_permissions(self, ruolo: str) -> Set[Permission]:
        """Ottiene tutti i permessi di un ruolo.
        
        Args:
            ruolo: Nome ruolo
            
        Returns:
            Set permessi
        """
        if ruolo not in self.roles:
            return set()
        
        return self.roles[ruolo].permissions
    
    def add_role(self, name: str, permissions: Set[Permission], description: str = ""):
        """Aggiunge un nuovo ruolo.
        
        Args:
            name: Nome ruolo
            permissions: Permessi
            description: Descrizione
        """
        self.roles[name] = Role(name, permissions, description)
    
    def remove_permission_from_role(self, ruolo: str, permission: Permission):
        """Rimuove permesso da ruolo.
        
        Args:
            ruolo: Nome ruolo
            permission: Permesso da rimuovere
        """
        if ruolo in self.roles:
            self.roles[ruolo].permissions.discard(permission)
    
    def add_permission_to_role(self, ruolo: str, permission: Permission):
        """Aggiunge permesso a ruolo.
        
        Args:
            ruolo: Nome ruolo
            permission: Permesso da aggiungere
        """
        if ruolo in self.roles:
            self.roles[ruolo].permissions.add(permission)
    
    def check_access(self, ruolo: str, required_permissions: List[Permission]) -> Dict:
        """Controlla accesso multi-permesso.
        
        Args:
            ruolo: Nome ruolo
            required_permissions: Lista permessi richiesti
            
        Returns:
            Risultato controllo
        """
        if ruolo not in self.roles:
            return {
                'granted': False,
                'reason': f'Ruolo {ruolo} non esiste'
            }
        
        user_permissions = self.roles[ruolo].permissions
        missing = [p for p in required_permissions if p not in user_permissions]
        
        return {
            'granted': len(missing) == 0,
            'missing': missing,
            'user_permissions': list(user_permissions)
        }


# Istanza globale
rbac = AdvancedRBAC()


if __name__ == "__main__":
    print("ADVANCED RBAC - TEST")
    print("=" * 60 + "\n")
    
    # Test permessi docente
    result = rbac.check_access('docente', [Permission.ADD_GRADES, Permission.VIEW_GRADES])
    print(f"Docente - Aggiungi/Visualizza voti: {result['granted']}")
    
    result = rbac.check_access('docente', [Permission.DELETE_STUDENTS])
    print(f"Docente - Elimina studenti: {result['granted']}")
    
    # Test permessi dirigente
    result = rbac.check_access('dirigente', [Permission.VIEW_ANALYTICS])
    print(f"Dirigente - View analytics: {result['granted']}")
    
    # Test permessi studente
    result = rbac.check_access('studente', [Permission.ADD_GRADES])
    print(f"Studente - Aggiungi voti: {result['granted']}")
    
    print("\n✅ RBAC test completato!")

