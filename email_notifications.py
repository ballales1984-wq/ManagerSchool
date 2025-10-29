"""
Sistema di notifiche email per ManagerSchool.
Simula invio email per eventi scolastici.
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@dataclass
class Email:
    """Rappresenta un'email."""
    
    mittente: str
    destinatario: str
    oggetto: str
    corpo: str
    data_invio: datetime
    inviata: bool = False


class EmailNotifier:
    """Gestisce invio email per notifiche automatiche."""
    
    def __init__(self, smtp_host: str = "smtp.gmail.com", smtp_port: int = 587):
        """Inizializza il notificatore email.
        
        Args:
            smtp_host: Server SMTP
            smtp_port: Porta SMTP
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.cronologia: List[Email] = []
        self.demo_mode = True  # Modalità demo (no invio reale)
    
    def invia_email(self, destinatario: str, oggetto: str, corpo: str, mittente: str = "noreply@managerschool.it") -> bool:
        """Invia un'email.
        
        Args:
            destinatario: Email destinatario
            oggetto: Oggetto email
            corpo: Corpo email
            mittente: Email mittente
            
        Returns:
            True se inviata
        """
        email = Email(
            mittente=mittente,
            destinatario=destinatario,
            oggetto=oggetto,
            corpo=corpo,
            data_invio=datetime.now()
        )
        
        if self.demo_mode:
            # Modalità demo - stampa invece di inviare
            print(f"📧 EMAIL (DEMO MODE)")
            print(f"   Da: {mittente}")
            print(f"   A: {destinatario}")
            print(f"   Oggetto: {oggetto}")
            print(f"   Corpo: {corpo[:100]}...")
            email.inviata = True
            self.cronologia.append(email)
            return True
        else:
            # Invio reale (da configurare)
            try:
                msg = MIMEMultipart()
                msg['From'] = mittente
                msg['To'] = destinatario
                msg['Subject'] = oggetto
                msg.attach(MIMEText(corpo, 'html'))
                
                # server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                # server.starttls()
                # server.login(username, password)
                # server.sendmail(mittente, destinatario, msg.as_string())
                # server.quit()
                
                email.inviata = True
                self.cronologia.append(email)
                return True
            except Exception as e:
                print(f"❌ Errore invio email: {e}")
                return False
    
    def notifica_voto_inserito(self, studente: Dict, voto: Dict, genitore_email: str):
        """Notifica genitore per voto inserito."""
        oggetto = f"Nuovo voto per {studente.get('nome', '')} {studente.get('cognome', '')}"
        corpo = f"""
Caro Genitore,

Abbiamo inserito un nuovo voto per {studente.get('nome_completo', '')}:

📚 Materia: {voto.get('materia', '')}
⭐ Voto: {voto.get('voto', 0):.1f}
📝 Tipo: {voto.get('tipo', '')}
📅 Data: {voto.get('data', '')}

Nota: {voto.get('note', 'Nessuna nota')}

Cordiali saluti,
Istituto Scolastico
        """
        return self.invia_email(genitore_email, oggetto, corpo)
    
    def notifica_assenza(self, studente: Dict, presenza: Dict, genitore_email: str):
        """Notifica genitore per assenza non giustificata."""
        oggetto = f"Assenza per {studente.get('nome', '')} {studente.get('cognome', '')}"
        corpo = f"""
Caro Genitore,

Comunichiamo un'assenza per {studente.get('nome_completo', '')}:

📅 Data: {presenza.get('data', '')}
⏰ Ora: {presenza.get('ora', 'N/A')}
📋 Tipo: {presenza.get('tipo', '')}
💡 Motivo: {presenza.get('motivo', 'Non specificato')}

{'' if presenza.get('giustificato') else '⚠️ Assenza non ancora giustificata'}

Cordiali saluti,
Istituto Scolastico
        """
        return self.invia_email(genitore_email, oggetto, corpo)
    
    def notifica_pagella_disponibile(self, studente: Dict, genitore_email: str, periodo: str):
        """Notifica genitore per pagella disponibile."""
        oggetto = f"Pagella {periodo} disponibile per {studente.get('nome', '')}"
        corpo = f"""
Caro Genitore,

La pagella di {periodo} per {studente.get('nome_completo', '')} è disponibile.

È possibile consultarla sul registro elettronico ManagerSchool.

Cordiali saluti,
Istituto Scolastico
        """
        return self.invia_email(genitore_email, oggetto, corpo)
    
    def notifica_comportamento(self, studente: Dict, nota: str, genitore_email: str):
        """Notifica genitore per nota comportamentale."""
        oggetto = f"Comunicazione importante per {studente.get('nome', '')}"
        corpo = f"""
Caro Genitore,

Abbiamo una comunicazione importante riguardo {studente.get('nome_completo', '')}:

📋 Nota: {nota}

Vi invitiamo a prendere contatto con la scuola.

Cordiali saluti,
Istituto Scolastico
        """
        return self.invia_email(genitore_email, oggetto, corpo)
    
    def get_statistiche_email(self) -> Dict:
        """Ottiene statistiche sulle email inviate."""
        totali = len(self.cronologia)
        inviate = len([e for e in self.cronologia if e.inviata])
        
        return {
            "totale_email": totali,
            "email_inviate": inviate,
            "email_fallite": totali - inviate,
            "percentuale_successo": round((inviate / totali) * 100, 2) if totali > 0 else 0
        }


if __name__ == "__main__":
    print("EMAIL NOTIFICATIONS - TEST")
    print("=" * 60 + "\n")
    
    notifier = EmailNotifier()
    
    # Test notifiche
    studente = {
        'nome': 'Mario',
        'cognome': 'Rossi',
        'nome_completo': 'Mario Rossi',
        'classe': '2A'
    }
    
    voto = {
        'materia': 'Matematica',
        'voto': 8.0,
        'tipo': 'Interrogazione',
        'data': '2025-10-28',
        'note': 'Ottimo lavoro'
    }
    
    # Simula notifica voto
    notifier.notifica_voto_inserito(studente, voto, "genitore.rossi@email.com")
    
    print(f"\n✅ Email processata")
    
    stats = notifier.get_statistiche_email()
    print(f"\n📊 Statistiche:")
    print(f"   Email inviate: {stats['email_inviate']}")
    print(f"   Successo: {stats['percentuale_successo']}%")

