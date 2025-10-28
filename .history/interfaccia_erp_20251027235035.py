"""
Modulo per interfacce ERP web-based.
Implementa una dashboard web con Flask per gestione completa del sistema scolastico.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from typing import Dict
import os

# Import dei moduli esistenti
from anagrafica import Anagrafica
from insegnanti import GestioneInsegnanti
from voti import GestioneVoti
from orari import GestioneOrari
from analisi import AnalisiDidattica
from accesso import GestoreAccessi, Ruolo
from indicatori import CalcolatoreIndicatori
from report import GeneratoreReport
from interventi import SimulatoreInterventi
from macro_dati import GestoreMacroDati


class InterfacciaERP:
    """Interfaccia web ERP per il sistema scolastico."""
    
    def __init__(self):
        """Inizializza l'applicazione Flask."""
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        
        # Inizializza i moduli del sistema
        self.anagrafica = Anagrafica()
        self.insegnanti = GestioneInsegnanti()
        self.voti = GestioneVoti()
        self.orari = GestioneOrari()
        self.analisi = AnalisiDidattica(self.anagrafica, self.voti)
        self.accesso = GestoreAccessi()
        self.gestore_macro_dati = GestoreMacroDati(self.anagrafica)
        
        # Calcolatori
        self.calcolatore_indicatori = CalcolatoreIndicatori(
            self.anagrafica, self.voti, self.insegnanti, self.analisi
        )
        try:
            self.generatore_report = GeneratoreReport(
                self.anagrafica, self.voti, self.insegnanti, 
                self.analisi, self.calcolatore_indicatori
            )
        except TypeError:
            # Fallback se GeneratoreReport non accetta tutti i parametri
            self.generatore_report = None
        self.simulatore_interventi = SimulatoreInterventi(
            self.anagrafica, self.voti
        )
        
        # Crea utenti demo
        self._crea_utenti_demo()
        
        # Registra le routes
        self._registra_routes()
    
    def _crea_utenti_demo(self):
        """Crea utenti demo per testing."""
        self.accesso.registra_utente("admin", "admin123", Ruolo.AMMINISTRATORE, "Amministratore Sistema")
        self.accesso.registra_utente("dirigente", "dirigente123", Ruolo.DIRIGENTE, "Dirigente Scolastico")
        self.accesso.registra_utente("insegnante", "insegnante123", Ruolo.INSEGNANTE, "Prof. Mario Rossi")
        self.accesso.registra_utente("studente", "studente123", Ruolo.STUDENTE, "Studente Demo")
    
    def _registra_routes(self):
        """Registra tutte le routes dell'applicazione."""
        
        # ============ ROUTES PUBBLICHE ============
        
        @self.app.route('/')
        def home():
            """Home page pubblica."""
            return render_template('home.html',
                                 totale_studenti=len(self.anagrafica.studenti))
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            """Login page."""
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                if self.accesso.autentica(username, password):
                    session['username'] = username
                    session['ruolo'] = self.accesso.get_ruolo_corrente().value
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('login.html', 
                                         errore="Credenziali non valide")
            
            return render_template('login.html')
        
        @self.app.route('/logout')
        def logout():
            """Logout."""
            self.accesso.disconnetti()
            session.clear()
            return redirect(url_for('home'))
        
        # ============ ROUTES DASHBOARD ============
        
        @self.app.route('/dashboard')
        @self.richiede_accesso
        def dashboard():
            """Dashboard principale."""
            stats = self._calcola_statistiche_dashboard()
            return render_template('dashboard.html', stats=stats)
        
        # ============ API STUDENTI ============
        
        @self.app.route('/api/studenti')
        @self.richiede_accesso
        def api_studenti():
            """API: Lista studenti."""
            studenti = [s.to_dict() for s in self.anagrafica.studenti]
            return jsonify(studenti)
        
        @self.app.route('/api/studenti/<int:studente_id>')
        @self.richiede_accesso
        def api_studente_dettaglio(studente_id):
            """API: Dettaglio studente."""
            studente = self.anagrafica.trova_studente(studente_id)
            if not studente:
                return jsonify({"errore": "Studente non trovato"}), 404
            
            voti = self.voti.voti_studente(studente_id)
            media = self.voti.media_studente(studente_id)
            
            return jsonify({
                "studente": studente.to_dict(),
                "voti": [{"materia": v.materia, "voto": v.voto} for v in voti[:10]],
                "media": media
            })
        
        @self.app.route('/api/studenti', methods=['POST'])
        @self.richiede_permesso("gestione_studenti")
        def api_crea_studente():
            """API: Crea studente."""
            data = request.json
            studente = self.anagrafica.crea_studente_casuale()
            # Qui potresti aggiornare con i dati forniti
            return jsonify({"successo": True, "studente": studente.to_dict()})
        
        # ============ API INSEGNANTI ============
        
        @self.app.route('/api/insegnanti')
        @self.richiede_accesso
        def api_insegnanti():
            """API: Lista insegnanti."""
            insegnanti = [i.to_dict() for i in self.insegnanti.insegnanti]
            return jsonify(insegnanti)
        
        # ============ API VOTI ============
        
        @self.app.route('/api/voti')
        @self.richiede_accesso
        def api_voti():
            """API: Lista voti."""
            voti = []
            for studente in self.anagrafica.studenti:
                voti_studente = self.voti.voti_studente(studente.id)
                for v in voti_studente[:5]:
                    voti.append({
                        "studente": studente.nome_completo,
                        "materia": v.materia,
                        "voto": v.voto
                    })
            return jsonify(voti)
        
        # ============ API ANALISI ============
        
        @self.app.route('/api/analisi/graduatoria')
        @self.richiede_accesso
        def api_graduatoria():
            """API: Graduatoria studenti."""
            grad = self.analisi.graduatoria_studenti()[:20]
            return jsonify(grad)
        
        @self.app.route('/api/analisi/fragilita')
        @self.richiede_accesso
        def api_analisi_fragilita():
            """API: Analisi fragilità."""
            analisi = self.analisi.impatto_didattico_fragili()
            return jsonify(analisi)
        
        @self.app.route('/api/analisi/correlazione')
        @self.richiede_accesso
        def api_correlazione():
            """API: Correlazione reddito-rendimento."""
            correl = self.analisi.correlazione_reddito_rendimento()
            return jsonify(correl)
        
        # ============ API INDICATORI ============
        
        @self.app.route('/api/indicatori')
        @self.richiede_permesso("visualizza_indicatori_privati")
        def api_indicatori():
            """API: Tutti gli indicatori sintetici."""
            quadro = self.calcolatore_indicatori.quadro_indicatori_completo()
            return jsonify({
                k: {
                    "nome": v.nome,
                    "valore": v.valore,
                    "componenti": v.componenti
                }
                for k, v in quadro.items()
            })
        
        @self.app.route('/api/indicatori/<indice_name>')
        @self.richiede_permesso("visualizza_indicatori_privati")
        def api_indice_singolo(indice_name):
            """API: Singolo indicatore."""
            metodi = {
                "qualita": self.calcolatore_indicatori.indice_qualita_scolastica,
                "equita": self.calcolatore_indicatori.indice_equita_educativa,
                "efficacia": self.calcolatore_indicatori.indice_efficacia_didattica,
                "coesione": self.calcolatore_indicatori.indice_coesione_sociale,
                "benessere": self.calcolatore_indicatori.indice_benessere_scolastico
            }
            
            if indice_name in metodi:
                indice = metodi[indice_name]()
                return jsonify({
                    "nome": indice.nome,
                    "valore": indice.valore,
                    "componenti": indice.componenti
                })
            
            return jsonify({"errore": "Indice non trovato"}), 404
        
        # ============ API REPORT ============
        
        @self.app.route('/api/report/annuale')
        @self.richiede_permesso("visualizza_report_completi")
        def api_report_annuale():
            """API: Report annuale."""
            report = self.generatore_report.report_annuale()
            return jsonify(report)
        
        @self.app.route('/api/report/equita')
        @self.richiede_permesso("visualizza_report_completi")
        def api_report_equita():
            """API: Report equità educativa."""
            report = self.generatore_report.report_equita_educativa()
            return jsonify(report)
        
        # ============ API INTERVENTI ============
        
        @self.app.route('/api/interventi/prioritari')
        @self.richiede_permesso("visualizza_report_completi")
        def api_interventi_prioritari():
            """API: Studenti prioritari per interventi."""
            limit = request.args.get('limit', 10, type=int)
            report = self.simulatore_interventi.report_interventi_prioritari(limit)
            return jsonify(report)
        
        # ============ API MACRO-DATI ============
        
        @self.app.route('/api/macro-dati')
        @self.richiede_accesso
        def api_macro_dati():
            """API: Macro-dati territoriali."""
            return jsonify(self.gestore_macro_dati.to_dict())
        
        # ============ API STATISTICHE DASHBOARD ============
        
        @self.app.route('/api/dashboard/stats')
        @self.richiede_accesso
        def api_stats_dashboard():
            """API: Statistiche per dashboard."""
            return jsonify(self._calcola_statistiche_dashboard())
    
    def _calcola_statistiche_dashboard(self) -> Dict:
        """Calcola statistiche per la dashboard."""
        stats_generali = self.anagrafica.statistiche_generali()
        fragilita_stats = self.anagrafica.statistica_fragilita()
        
        return {
            "studenti_totali": len(self.anagrafica.studenti),
            "insegnanti_totali": len(self.insegnanti.insegnanti),
            "classi_totali": stats_generali.get("numero_classi", 0),
            "reddito_medio": stats_generali.get("reddito_medio", 0),
            "fragilita_media": fragilita_stats.get("media", 0),
            "fragilita_alta": fragilita_stats.get("percentuale_alta", 0)
        }
    
    # ============ DECORATORS ============
    
    def richiede_accesso(self, f):
        """Decorator per richiedere autenticazione."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Ricostruisci sessione dallo storage
            if not self.accesso.get_utente_corrente():
                username = session.get('username')
                if username in self.accesso.utenti:
                    self.accesso.sessione_corrente = self.accesso.utenti[username]
            
            return f(*args, **kwargs)
        return decorated_function
    
    def richiede_permesso(self, permesso: str):
        """Decorator per richiedere un permesso specifico."""
        def decorator(f):
            @wraps(f)
            @self.richiede_accesso
            def decorated_function(*args, **kwargs):
                if not self.accesso.verifica_permesso(permesso):
                    return jsonify({"errore": "Permesso negato"}), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Avvia il server Flask."""
        print(f"\n{'='*80}")
        print("🚀 INTERFACCIA ERP WEB".center(80))
        print(f"{'='*80}")
        print(f"\n✅ Server avviato su: http://{host}:{port}")
        print(f"\n👤 Utenti demo:")
        print(f"   - admin/admin123 (Amministratore)")
        print(f"   - dirigente/dirigente123 (Dirigente)")
        print(f"   - insegnante/insegnante123 (Insegnante)")
        print(f"   - studente/studente123 (Studente)")
        print(f"\n{'='*80}\n")
        
        self.app.run(host=host, port=port, debug=debug)


# Funzione per creare le directory dei template
def _crea_template_dir():
    """Crea la directory templates se non esiste."""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        print(f"📁 Creata directory: {template_dir}")
    
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"📁 Creata directory: {static_dir}")


if __name__ == "__main__":
    # Crea directory necessarie
    _crea_template_dir()
    
    # Crea e avvia l'interfaccia ERP
    erp = InterfacciaERP()
    erp.run()

