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
from calendario_scolastico import CalendarioScolastico
from macro_dati import GestoreMacroDati
from comunicazioni import GestioneComunicazioni
from analytics_predittive import AnaliticaPredittiva
from inserimento_rapido import GestoreInserimentoVeloce
from amministrativa_school import AmministrativaSchool
from backup_registro import GestoreBackup
from valutazione_impatto import ValutazioneImpattoEducativo
from costruttore_corso import CostruttoreCorsoDocente
from database_manager import DatabaseManager
from database_integration import DatabaseIntegration


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
        self.calendario = CalendarioScolastico()
        self.comunicazioni = GestioneComunicazioni()
        self.accesso = GestoreAccessi()
        
        # Inizializza analytics (dopo che tutti i moduli sono pronti)
        self.analytics = None  # Sarà inizializzato dopo il caricamento dati
        try:
            self.gestore_macro_dati = GestoreMacroDati(self.anagrafica)
        except Exception:
            self.gestore_macro_dati = None
        
        # Calcolatori
        self.calcolatore_indicatori = CalcolatoreIndicatori(
            self.anagrafica, self.voti, self.insegnanti, self.analisi
        )
        
        # Inizializza analytics manualmente (sarà definito dopo)
        try:
            self.analytics = AnaliticaPredittiva(
                self.anagrafica, 
                self.voti, 
                self.insegnanti, 
                self.comunicazioni
            )
        except Exception as e:
            print(f"⚠️  Analytics non disponibile: {e}")
            self.analytics = None
        
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
        
        # Gestore inserimento rapido voti
        self.gestore_inserimento_rapido = GestoreInserimentoVeloce(
            self.anagrafica, self.voti
        )
        
        # Gestione amministrativa
        self.amministrativa = AmministrativaSchool()
        
        # Gestore backup
        self.gestore_backup = GestoreBackup()
        
        # Valutazione impatto educativo
        self.valutazione_impatto = ValutazioneImpattoEducativo(
            self.anagrafica, self.voti
        )
        
        # Costruttore corsi digitali
        self.costruttore_corso = CostruttoreCorsoDocente(
            self.anagrafica, self.voti
        )
        
        # Database SQLite per persistenza
        self.database = DatabaseManager("managerschool.db")
        self.db_integration = DatabaseIntegration(self.anagrafica, self.voti)
        
        # Crea utenti demo
        self._crea_utenti_demo()
        
        # Registra le routes
        self._registra_routes()
    
    def _crea_utenti_demo(self):
        """Crea utenti demo per testing."""
        # Controlla se gli utenti esistono già
        if "admin" not in self.accesso.utenti:
            self.accesso.registra_utente("admin", "admin123", Ruolo.AMMINISTRATORE, "Amministratore Sistema")
        if "dirigente" not in self.accesso.utenti:
            self.accesso.registra_utente("dirigente", "dirigente123", Ruolo.DIRIGENTE, "Dirigente Scolastico")
        if "insegnante" not in self.accesso.utenti:
            self.accesso.registra_utente("insegnante", "insegnante123", Ruolo.INSEGNANTE, "Prof. Mario Rossi")
        if "studente" not in self.accesso.utenti:
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
            # Ordina gli studenti per classe
            studenti_ordinati = sorted(self.anagrafica.studenti, key=lambda s: s.classe)
            studenti = [s.to_dict() for s in studenti_ordinati]
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
            # Qui potresti aggiornare con i dati forniti
            studente = self.anagrafica.crea_studente_casuale()
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
            if not self.gestore_macro_dati:
                return jsonify({"errore": "Macro-dati non disponibili"})
            
            zone_data = {}
            for zone_name, zone in self.gestore_macro_dati.ZONE_PREDEFINITE.items():
                zone_data[zone_name] = {
                    "nome": zone.nome,
                    "regione": zone.regione,
                    "reddito_medio": zone.reddito_medio_familiare,
                    "indice_sviluppo": zone.indice_sviluppo_umano
                }
            return jsonify(zone_data)
        
        # ============ API CALENDARIO SCOLASTICO ============
        
        @self.app.route('/api/calendario/statistiche')
        @self.richiede_accesso
        def api_calendario_statistiche():
            """API: Statistiche del calendario scolastico."""
            return jsonify(self.calendario.statistiche_anno())
        
        @self.app.route('/api/calendario/periodo-corrente')
        @self.richiede_accesso
        def api_periodo_corrente():
            """API: Periodo scolastico corrente."""
            periodo = self.calendario.periodo_corrente()
            if periodo:
                return jsonify({
                    "nome": periodo.nome,
                    "data_inizio": periodo.data_inizio.isoformat(),
                    "data_fine": periodo.data_fine.isoformat(),
                    "tipo": periodo.tipo.value,
                    "descrizione": periodo.descrizione,
                    "giorni_mancanti": self.calendario.giorni_mancanti_fine_periodo()
                })
            return jsonify({"periodo": None})
        
        @self.app.route('/api/calendario/festivita')
        @self.richiede_accesso
        def api_festivita():
            """API: Prossime festività."""
            n = request.args.get('n', 5, type=int)
            festivita = self.calendario.prossime_festivita(n)
            
            return jsonify([
                {
                    "nome": f.nome,
                    "data": f.data.isoformat(),
                    "tipo": f.tipo,
                    "scuola_chiusa": f.scuola_chiusa,
                    "descrizione": f.descrizione
                }
                for f in festivita
            ])
        
        @self.app.route('/api/calendario/mese/<int:mese>')
        @self.richiede_accesso
        def api_calendario_mese(mese):
            """API: Calendario di un mese specifico."""
            anno = request.args.get('anno', type=int)
            calendario_mese = self.calendario.genera_calendario_mensile(mese, anno)
            
            # Serializza per JSON
            result = {
                "mese": calendario_mese["mese"],
                "anno": calendario_mese["anno"],
                "nome_mese": calendario_mese["nome_mese"],
                "calendario": calendario_mese["calendario"],
                "giorni_info": {}
            }
            
            # Converte giorni_info per JSON
            for giorno, info in calendario_mese["giorni_info"].items():
                result["giorni_info"][str(giorno)] = {
                    "data": info["data"].isoformat(),
                    "tipo": info["tipo"],
                    "eventi": info["eventi"],
                    "scuola_aperta": info["scuola_aperta"]
                }
            
            return jsonify(result)
        
        @self.app.route('/api/calendario/export')
        @self.richiede_accesso
        def api_calendario_export():
            """API: Esporta calendario completo."""
            return jsonify(self.calendario.esporta_json())
        
        # ============ API PAGELLE E VOTI ============
        
        @self.app.route('/api/pagelle/genera', methods=['POST'])
        @self.richiede_accesso
        def api_genera_pagelle():
            """API: Genera pagelle complete per tutti gli studenti."""
            try:
                # Materie complete come nelle pagelle reali
                materie = ["Matematica", "Italiano", "Inglese", "Storia", "Educazione Fisica", "Religione"]
                
                # Pulisci voti e pagelle esistenti per rigenerare
                self.voti.voti.clear()
                self.voti.pagelle.clear()
                
                voti_creati = 0
                pagelle_create = 0
                
                # Genera voti per ogni studente
                for studente in self.anagrafica.studenti:
                    for materia in materie:
                        import random
                        n_voti = random.randint(2, 6)
                        
                        for _ in range(n_voti):
                            # Voto influenzato dalla fragilità sociale
                            base = 6.5 - (studente.fragilità_sociale / 100)
                            
                            # Aggiustamenti per materie specifiche
                            if materia == "Educazione Fisica":
                                base += 0.4
                            elif materia == "Religione":
                                base += 0.3
                            elif materia == "Matematica":
                                base -= 0.2  # Matematica più difficile
                            
                            # Variazione casuale
                            variazione = random.uniform(-1.0, 1.0)
                            voto_finale = max(3.0, min(10.0, base + variazione))
                            
                            # Crea voto
                            import datetime
                            giorni_fa = random.randint(1, 90)
                            data = datetime.datetime.now() - datetime.timedelta(days=giorni_fa)
                            
                            self.voti.aggiungi_voto(
                                studente.id, 
                                materia, 
                                round(voto_finale, 1),
                                random.choice(["Prova scritta", "Prova orale", "Verifica"]),
                                data.strftime("%Y-%m-%d")
                            )
                            voti_creati += 1
                
                # Crea pagelle per tutti gli studenti
                for studente in self.anagrafica.studenti:
                    # Genera voto di condotta basato sulla fragilità
                    condotta_base = 9.0 - (studente.fragilità_sociale / 50)
                    condotta = max(6.0, min(10.0, condotta_base + random.uniform(-0.3, 0.2)))
                    
                    # Genera assenze correlate alla fragilità
                    assenze_base = int(studente.fragilità_sociale / 10)
                    assenze = random.randint(max(0, assenze_base - 2), assenze_base + 6)
                    
                    # Note basate sul rendimento
                    media = self.voti.media_studente(studente.id)
                    if media >= 8.0:
                        note = "Ottimo rendimento e partecipazione attiva"
                    elif media >= 7.0:
                        note = "Buon rendimento generale"
                    elif media >= 6.0:
                        note = "Rendimento sufficiente"
                    else:
                        note = "Necessita di maggiore impegno e supporto"
                    
                    # Crea pagella
                    pagella = self.voti.crea_pagella(
                        studente.id,
                        quadrimestre=1,
                        assenze=assenze,
                        comportamento=round(condotta, 1),
                        note=note
                    )
                    pagelle_create += 1
                
                return jsonify({
                    "successo": True,
                    "messaggio": "Pagelle generate con successo",
                    "statistiche": {
                        "studenti": len(self.anagrafica.studenti),
                        "voti_creati": voti_creati,
                        "pagelle_create": pagelle_create,
                        "materie": len(materie)
                    }
                })
                
            except Exception as e:
                return jsonify({
                    "successo": False,
                    "errore": str(e)
                }), 500
        
        @self.app.route('/api/pagelle')
        @self.richiede_accesso
        def api_pagelle():
            """API: Lista tutte le pagelle create."""
            pagelle_data = []
            
            for pagella in self.voti.pagelle:
                # Trova lo studente corrispondente
                studente = next((s for s in self.anagrafica.studenti if s.id == pagella.id_studente), None)
                
                if studente:
                    pagelle_data.append({
                        "studente": {
                            "id": studente.id,
                            "nome": studente.nome_completo,
                            "classe": studente.classe,
                            "eta": studente.eta,
                            "fragilita": studente.fragilità_sociale
                        },
                        "pagella": {
                            "quadrimestre": pagella.quadrimestre,
                            "voti_materie": pagella.voti_materie,
                            "media_generale": round(pagella.media_generale, 2),
                            "voto_condotta": pagella.comportamento,
                            "assenze": pagella.assenze,
                            "note": pagella.note
                        }
                    })
            
            return jsonify(pagelle_data)
        
        @self.app.route('/api/pagelle/studente/<int:studente_id>')
        @self.richiede_accesso
        def api_pagella_studente(studente_id):
            """API: Pagella di uno studente specifico."""
            # Trova la pagella dello studente
            pagella = next((p for p in self.voti.pagelle if p.id_studente == studente_id), None)
            
            if not pagella:
                return jsonify({"errore": "Pagella non trovata per questo studente"}), 404
            
            # Trova lo studente
            studente = next((s for s in self.anagrafica.studenti if s.id == studente_id), None)
            
            if not studente:
                return jsonify({"errore": "Studente non trovato"}), 404
            
            return jsonify({
                "studente": {
                    "id": studente.id,
                    "nome": studente.nome_completo,
                    "classe": studente.classe,
                    "eta": studente.eta,
                    "fragilita": studente.fragilità_sociale
                },
                "pagella": {
                    "quadrimestre": pagella.quadrimestre,
                    "voti_materie": pagella.voti_materie,
                    "media_generale": round(pagella.media_generale, 2),
                    "voto_condotta": pagella.comportamento,
                    "assenze": pagella.assenze,
                    "note": pagella.note
                },
                "voti_dettagliati": [
                    {
                        "materia": v.materia,
                        "voto": v.voto,
                        "tipo": v.tipo,
                        "data": v.data,
                        "note": v.note
                    }
                    for v in self.voti.voti if v.id_studente == studente_id
                ]
            })
        
        @self.app.route('/api/pagelle/statistiche')
        @self.richiede_accesso
        def api_pagelle_statistiche():
            """API: Statistiche delle pagelle create."""
            if not self.voti.pagelle:
                return jsonify({
                    "messaggio": "Nessuna pagella creata",
                    "totale_pagelle": 0
                })
            
            # Calcola statistiche
            medie = [p.media_generale for p in self.voti.pagelle]
            condotte = [p.comportamento for p in self.voti.pagelle]
            assenze = [p.assenze for p in self.voti.pagelle]
            
            # Statistiche per materia
            materie_stats = {}
            for pagella in self.voti.pagelle:
                for materia, voto in pagella.voti_materie.items():
                    if materia not in materie_stats:
                        materie_stats[materia] = []
                    materie_stats[materia].append(voto)
            
            # Media per materia
            medie_materie = {}
            for materia, voti in materie_stats.items():
                medie_materie[materia] = round(sum(voti) / len(voti), 2)
            
            return jsonify({
                "totale_pagelle": len(self.voti.pagelle),
                "media_generale_classe": round(sum(medie) / len(medie), 2),
                "media_condotta_classe": round(sum(condotte) / len(condotte), 1),
                "media_assenze": round(sum(assenze) / len(assenze), 1),
                "medie_per_materia": medie_materie,
                "distribuzione_medie": {
                    "eccellenti": len([m for m in medie if m >= 9.0]),
                    "ottime": len([m for m in medie if 8.0 <= m < 9.0]),
                    "buone": len([m for m in medie if 7.0 <= m < 8.0]),
                    "sufficienti": len([m for m in medie if 6.0 <= m < 7.0]),
                    "insufficienti": len([m for m in medie if m < 6.0])
                }
            })
        
        # ============ API COMUNICAZIONI SCUOLA-FAMIGLIA ============
        
        @self.app.route('/api/comunicazioni')
        @self.richiede_accesso
        def api_comunicazioni():
            """API: Lista comunicazioni per l'utente corrente."""
            user_id = session.get('user_id', 1)  # Default per demo
            tipo_utente = session.get('ruolo', 'admin')
            
            solo_non_lette = request.args.get('non_lette', 'false').lower() == 'true'
            
            comunicazioni = self.comunicazioni.get_comunicazioni_per_utente(
                user_id, tipo_utente, solo_non_lette
            )
            
            return jsonify([com.to_dict() for com in comunicazioni])
        
        @self.app.route('/api/comunicazioni/invia', methods=['POST'])
        @self.richiede_accesso
        def api_invia_comunicazione():
            """API: Invia nuova comunicazione."""
            data = request.get_json()
            
            comunicazione = self.comunicazioni.crea_comunicazione(
                mittente_id=session.get('user_id', 1),
                mittente_tipo=session.get('ruolo', 'admin'),
                destinatario_id=data['destinatario_id'],
                destinatario_tipo=data['destinatario_tipo'],
                oggetto=data['oggetto'],
                messaggio=data['messaggio'],
                studente_id=data.get('studente_id')
            )
            
            return jsonify({
                "successo": True,
                "comunicazione_id": comunicazione.id,
                "messaggio": "Comunicazione inviata con successo"
            })
        
        @self.app.route('/api/comunicazioni/<int:comunicazione_id>/leggi', methods=['POST'])
        @self.richiede_accesso
        def api_leggi_comunicazione(comunicazione_id):
            """API: Marca comunicazione come letta."""
            user_id = session.get('user_id', 1)
            
            successo = self.comunicazioni.marca_come_letta(comunicazione_id, user_id)
            
            return jsonify({
                "successo": successo,
                "messaggio": "Comunicazione marcata come letta" if successo else "Errore nell'operazione"
            })
        
        @self.app.route('/api/comunicazioni/<int:comunicazione_id>/rispondi', methods=['POST'])
        @self.richiede_accesso
        def api_rispondi_comunicazione(comunicazione_id):
            """API: Risponde a una comunicazione."""
            data = request.get_json()
            
            risposta = self.comunicazioni.crea_risposta(
                comunicazione_originale_id=comunicazione_id,
                mittente_id=session.get('user_id', 1),
                mittente_tipo=session.get('ruolo', 'admin'),
                messaggio=data['messaggio']
            )
            
            if risposta:
                return jsonify({
                    "successo": True,
                    "risposta_id": risposta.id,
                    "messaggio": "Risposta inviata con successo"
                })
            else:
                return jsonify({
                    "successo": False,
                    "messaggio": "Errore nell'invio della risposta"
                }), 400
        
        @self.app.route('/api/comunicazioni/studente/<int:studente_id>')
        @self.richiede_accesso
        def api_comunicazioni_studente(studente_id):
            """API: Comunicazioni relative a uno studente."""
            comunicazioni = self.comunicazioni.get_comunicazioni_studente(studente_id)
            return jsonify([com.to_dict() for com in comunicazioni])
        
        @self.app.route('/api/comunicazioni/statistiche')
        @self.richiede_accesso
        def api_comunicazioni_statistiche():
            """API: Statistiche delle comunicazioni."""
            return jsonify(self.comunicazioni.get_statistiche_comunicazioni())
        
        @self.app.route('/api/comunicazioni/notifiche')
        @self.richiede_accesso
        def api_notifiche_automatiche():
            """API: Lista notifiche automatiche configurate."""
            return jsonify([n.to_dict() for n in self.comunicazioni.notifiche_automatiche])
        
        @self.app.route('/api/comunicazioni/genera-demo', methods=['POST'])
        @self.richiede_accesso
        def api_genera_comunicazioni_demo():
            """API: Genera comunicazioni demo per test."""
            studenti_ids = [s.id for s in self.anagrafica.studenti]
            insegnanti_ids = [i.id for i in self.insegnanti.insegnanti]
            
            comunicazioni_prima = len(self.comunicazioni)
            self.comunicazioni.genera_comunicazioni_demo(studenti_ids, insegnanti_ids)
            comunicazioni_dopo = len(self.comunicazioni)
            
            return jsonify({
                "successo": True,
                "comunicazioni_generate": comunicazioni_dopo - comunicazioni_prima,
                "messaggio": "Comunicazioni demo generate con successo"
            })
        
        # ============ API ANALYTICS E DASHBOARD DIRIGENZA ============
        
        @self.app.route('/api/analytics/report-ministeriale')
        @self.richiede_accesso
        def api_report_ministeriale():
            """API: Genera report ministeriale completo."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            report = self.analytics.genera_report_ministeriale()
            return jsonify(report)
        
        @self.app.route('/api/analytics/studenti-rischio')
        @self.richiede_accesso
        def api_studenti_rischio():
            """API: Lista studenti a rischio."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            soglia = request.args.get('soglia', 5.5, type=float)
            studenti = self.analytics.identifica_studenti_rischio(soglia)
            return jsonify(studenti)
        
        @self.app.route('/api/analytics/allerte')
        @self.richiede_accesso
        def api_allerte():
            """API: Lista allerte attive."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            solo_attive = request.args.get('solo_attive', 'true').lower() == 'true'
            allerte = self.analytics.get_allerte(solo_attive)
            return jsonify(allerte)
        
        @self.app.route('/api/analytics/genera-allerte', methods=['POST'])
        @self.richiede_accesso
        def api_genera_allerte():
            """API: Genera allerte automatiche."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            nuove_allerte = self.analytics.genera_allerte_automatiche()
            return jsonify({
                "successo": True,
                "allerte_generate": len(nuove_allerte),
                "allerte": [a.to_dict() for a in nuove_allerte]
            })
        
        @self.app.route('/api/analytics/trend-rendimento')
        @self.richiede_accesso
        def api_trend_rendimento():
            """API: Trend rendimento studenti."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            giorni = request.args.get('giorni', 30, type=int)
            trend = self.analytics.get_trend_rendimento(giorni)
            return jsonify(trend.to_dict())
        
        @self.app.route('/api/analytics/statistiche-scuola')
        @self.richiede_accesso
        def api_statistiche_scuola():
            """API: Statistiche generali della scuola."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            return jsonify({
                "media_generale": round(self.analytics.calcola_media_generale_scuola(), 2),
                "tasso_frequenza": round(self.analytics.calcola_tasso_frequenza(), 2),
                "totale_studenti": len(self.anagrafica.studenti),
                "totale_insegnanti": len(self.insegnanti.insegnanti),
                "studenti_rischio": len(self.analytics.identifica_studenti_rischio())
            })
        
        @self.app.route('/api/analytics/distribuzione-classi')
        @self.richiede_accesso
        def api_distribuzione_classi():
            """API: Distribuzione performance per classe."""
            if not self.analytics:
                return jsonify({"errore": "Analytics non disponibile"}), 503
            
            distribuzione = self.analytics._analizza_distribuzione_classi()
            return jsonify(distribuzione)
        
        # ============ ROUTES PAGINE WEB ============
        
        @self.app.route('/studenti')
        @self.richiede_accesso
        def pagina_studenti():
            """Pagina studenti."""
            # Ordina gli studenti per classe prima di convertirli in dizionari
            studenti_ordinati = sorted(self.anagrafica.studenti, key=lambda s: s.classe)
            studenti = [s.to_dict() for s in studenti_ordinati]
            return render_template('studenti.html', studenti=studenti)
        
        @self.app.route('/insegnanti')
        @self.richiede_accesso
        def pagina_insegnanti():
            """Pagina insegnanti."""
            insegnanti = [i.to_dict() for i in self.insegnanti.insegnanti]
            return render_template('insegnanti.html', insegnanti=insegnanti)
        
        @self.app.route('/voti')
        @self.richiede_accesso
        def pagina_voti():
            """Pagina voti."""
            return render_template('voti.html')
        
        @self.app.route('/analisi')
        @self.richiede_accesso
        def pagina_analisi():
            """Pagina analisi."""
            graduatoria = self.analisi.graduatoria_studenti()[:20]
            return render_template('analisi.html', graduatoria=graduatoria)
        
        @self.app.route('/indicatori')
        @self.richiede_accesso
        def pagina_indicatori():
            """Pagina indicatori."""
            try:
                quadro = self.calcolatore_indicatori.quadro_indicatori_completo()
                sintesi = self.calcolatore_indicatori.sintesi_indicatori()
            except (AttributeError, TypeError) as e:
                quadro = {}
                sintesi = {}
            return render_template('indicatori.html', quadro=quadro, sintesi=sintesi)
        
        @self.app.route('/report')
        @self.richiede_accesso
        def pagina_report():
            """Pagina report."""
            return render_template('report.html')
        
        @self.app.route('/calendario')
        @self.richiede_accesso
        def pagina_calendario():
            """Pagina calendario scolastico."""
            return render_template('calendario.html')
        
        @self.app.route('/comunicazioni')
        @self.richiede_accesso
        def pagina_comunicazioni():
            """Pagina comunicazioni scuola-famiglia."""
            return render_template('comunicazioni.html')
        
        @self.app.route('/dashboard-dirigenza')
        @self.richiede_accesso
        def pagina_dashboard_dirigenza():
            """Pagina dashboard dirigenza con analytics avanzate."""
            return render_template('dashboard_dirigenza.html')
        
        @self.app.route('/inserimento-voti')
        @self.richiede_accesso
        def pagina_inserimento_voti():
            """Pagina inserimento rapido voti."""
            return render_template('inserimento_voti.html')
        
        # ============ API INSERIMENTO RAPIDO ============
        
        @self.app.route('/api/inserimento-rapido/voto', methods=['POST'])
        @self.richiede_permesso("gestione_voti")
        def api_inserimento_rapido():
            """API: Inserisce voto tramite frase."""
            data = request.get_json()
            frase = data.get('frase', '')
            
            # Preleva dati utente dalla sessione
            docente = session.get('username', 'Docente')
            classe_corrente = request.args.get('classe', 'ClasseX')
            
            # Usa il gestore inserimento veloce
            risultato = self.gestore_inserimento_rapido.inserisci_da_frase(
                frase, docente, classe_corrente
            )
            
            return jsonify(risultato)
        
        @self.app.route('/api/inserimento-rapido/cronologia')
        @self.richiede_accesso
        def api_cronologia_inserimenti():
            """API: Cronologia inserimenti recenti."""
            limit = request.args.get('limit', 10, type=int)
            voci = self.gestore_inserimento_rapido.visualizza_cronologia(limit)
            return jsonify(voci)
        
        @self.app.route('/api/studenti/search')
        @self.richiede_accesso
        def api_search_studenti():
            """API: Ricerca studenti per autocompletamento."""
            query = request.args.get('q', '')
            risultati = self.gestore_inserimento_rapido.cerca_studenti(query)
            return jsonify(risultati)
        
        # ============ API AMMINISTRATIVA ============
        
        @self.app.route('/api/amministrativa/presenze')
        @self.richiede_accesso
        def api_presenze():
            """API: Statistiche presenze."""
            classe = request.args.get('classe', None)
            stats = self.amministrativa.statistiche_presenze(classe)
            return jsonify(stats)
        
        @self.app.route('/api/amministrativa/documenti')
        @self.richiede_accesso
        def api_documenti():
            """API: Lista documenti."""
            limit = request.args.get('limit', 10, type=int)
            documenti = self.amministrativa.get_documenti_recenti(limit)
            return jsonify([d.to_dict() for d in documenti])
        
        # ============ API BACKUP ============
        
        @self.app.route('/api/backup/lista')
        @self.richiede_permesso("gestione_studenti")
        def api_backup_lista():
            """API: Lista backup disponibili."""
            tipo = request.args.get('tipo', 'giornalieri')
            backup_lista = self.gestore_backup.lista_backup_disponibili(tipo)
            return jsonify(backup_lista)
        
        @self.app.route('/api/backup/crea', methods=['POST'])
        @self.richiede_permesso("gestione_studenti")
        def api_backup_crea():
            """API: Crea nuovo backup."""
            from main import RegistroScolastico
            registro = RegistroScolastico()
            registro.anagrafica = self.anagrafica
            registro.voti = self.voti
            registro.insegnanti = self.insegnanti
            
            filepath = self.gestore_backup.salva_backup(registro)
            return jsonify({"successo": True, "filepath": filepath})
        
        # ============ API VALUTAZIONE IMPATTO ============
        
        @self.app.route('/api/valutazione-impatto/report-studente')
        @self.richiede_accesso
        def api_report_studente():
            """API: Report studente."""
            studente_id = request.args.get('studente_id', type=int)
            materia = request.args.get('materia', '')
            if not studente_id or not materia:
                return jsonify({"errore": "Parametri mancanti"}), 400
            report = self.valutazione_impatto.genera_report_studente(studente_id, materia)
            return jsonify(report)
        
        @self.app.route('/api/valutazione-impatto/statistiche')
        @self.richiede_accesso
        def api_statistiche_impatto():
            """API: Statistiche impatto generale."""
            stats = self.valutazione_impatto.statistiche_impatto_generale()
            return jsonify(stats)
        
        # ============ API COSTRUTTORE CORSO ============
        
        @self.app.route('/api/corsi/risorse-docente')
        @self.richiede_accesso
        def api_risorse_docente():
            """API: Risorse di un docente."""
            docente = request.args.get('docente', '')
            if not docente:
                return jsonify({"errore": "Parametro docente mancante"}), 400
            risorse = self.costruttore_corso.risorse_per_docente(docente)
            return jsonify([r.to_dict() for r in risorse])
        
        @self.app.route('/api/corsi/corsi-pubblici')
        @self.richiede_accesso
        def api_corsi_pubblici():
            """API: Corsi pubblici."""
            corsi = self.costruttore_corso.corsi_pubblici()
            return jsonify([c.to_dict() for c in corsi])
        
        @self.app.route('/api/corsi/schede-studente')
        @self.richiede_accesso
        def api_schede_studente():
            """API: Schede di uno studente."""
            studente_id = request.args.get('studente_id', type=int)
            if not studente_id:
                return jsonify({"errore": "Parametro mancante"}), 400
            schede = self.costruttore_corso.schede_studente(studente_id)
            return jsonify([s.to_dict() for s in schede])
        
        # ============ API DATABASE ============
        
        @self.app.route('/api/database/stats')
        @self.richiede_accesso
        def api_database_stats():
            """API: Statistiche database."""
            stats = self.database.statistiche_database()
            return jsonify(stats)
        
        @self.app.route('/api/database/backup', methods=['POST'])
        @self.richiede_permesso("gestione_studenti")
        def api_database_backup():
            """API: Crea backup database."""
            backup_path = self.database.backup_database()
            return jsonify({"successo": True, "filepath": backup_path})
        
        @self.app.route('/api/database/sync', methods=['POST'])
        @self.richiede_permesso("gestione_studenti")
        def api_database_sync():
            """API: Sincronizza dati con database."""
            try:
                self.db_integration.sincronizza_dati_esistenti()
                return jsonify({"successo": True, "messaggio": "Sincronizzazione completata"})
            except Exception as e:
                return jsonify({"errore": str(e)}), 500
        
        @self.app.route('/api/database/voti')
        @self.richiede_accesso
        def api_database_voti():
            """API: Lista voti dal database."""
            studente_id = request.args.get('studente_id', type=int)
            if studente_id:
                voti = self.database.ottieni_voti_studente(studente_id)
            else:
                # Tutti i voti
                from database_manager import DatabaseManager
                cursor = self.database.conn.cursor()
                cursor.execute("SELECT * FROM voti ORDER BY data DESC LIMIT 100")
                voti = [dict(row) for row in cursor.fetchall()]
            return jsonify(voti)
        
        # ============ API STATISTICHE DASHBOARD ============
        
        @self.app.route('/api/dashboard/stats')
        @self.richiede_accesso
        def api_stats_dashboard():
            """API: Statistiche per dashboard."""
            return jsonify(self._calcola_statistiche_dashboard())
        
        @self.app.route('/api/dashboard/charts')
        @self.richiede_accesso
        def api_charts_dashboard():
            """API: Dati per grafici dashboard."""
            return jsonify(self._calcola_dati_grafici())
    
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
    
    def _calcola_dati_grafici(self) -> Dict:
        """Calcola dati per grafici interattivi."""
        # Distribuzione voti
        distribuzione = self._calcola_distribuzione_voti()
        
        # Trend andamento
        trend = self._calcola_trend_andamento()
        
        # Fragilità vs voti
        fragilita = self._calcola_fragilita_vs_voti()
        
        # Medie per materia
        medie = self._calcola_medie_per_materia()
        
        # Presenze
        presenze = self._calcola_presenze_chart()
        
        return {
            "distribuzione": distribuzione,
            "trend": trend,
            "fragilita": fragilita,
            "medie": medie,
            "presenze": presenze
        }
    
    def _calcola_distribuzione_voti(self) -> Dict:
        """Calcola distribuzione voti per intervalli."""
        voti = [v.voto for v in self.voti.voti]
        distribuzione = {f"{i}-{i+1}": 0 for i in range(0, 10)}
        
        for voto in voti:
            if 0 <= voto < 1:
                distribuzione["0-1"] += 1
            elif 1 <= voto < 2:
                distribuzione["1-2"] += 1
            elif 2 <= voto < 3:
                distribuzione["2-3"] += 1
            elif 3 <= voto < 4:
                distribuzione["3-4"] += 1
            elif 4 <= voto < 5:
                distribuzione["4-5"] += 1
            elif 5 <= voto < 6:
                distribuzione["5-6"] += 1
            elif 6 <= voto < 7:
                distribuzione["6-7"] += 1
            elif 7 <= voto < 8:
                distribuzione["7-8"] += 1
            elif 8 <= voto < 9:
                distribuzione["8-9"] += 1
            elif 9 <= voto <= 10:
                distribuzione["9-10"] += 1
        
        return {
            "labels": list(distribuzione.keys()),
            "values": list(distribuzione.values())
        }
    
    def _calcola_trend_andamento(self) -> Dict:
        """Calcola trend andamento media nel tempo."""
        # Calcola media per periodo
        labels = []
        medie = []
        
        # Simula trend (da implementare con dati reali)
        for i in range(10):
            labels.append(f"Settimana {i+1}")
            medie.append(6.5 + (i * 0.1))
        
        return {
            "labels": labels,
            "medie": medie
        }
    
    def _calcola_fragilita_vs_voti(self) -> Dict:
        """Calcola correlazione fragilità-voti."""
        points = []
        
        for studente in self.anagrafica.studenti[:20]:  # Limit a 20 studenti
            voti_stud = [v.voto for v in self.voti.voti_studente(studente.id)]
            if voti_stud:
                media = sum(voti_stud) / len(voti_stud)
                fragilita = getattr(studente, 'fragilita', 50)
                points.append({"x": fragilita, "y": media})
        
        return {"points": points}
    
    def _calcola_medie_per_materia(self) -> Dict:
        """Calcola medie per materia."""
        materie = {}
        
        for voto in self.voti.voti:
            if voto.materia not in materie:
                materie[voto.materia] = []
            materie[voto.materia].append(voto.voto)
        
        medie_calc = {m: sum(v) / len(v) for m, v in materie.items()}
        
        return {
            "labels": list(medie_calc.keys()),
            "values": list(medie_calc.values())
        }
    
    def _calcola_presenze_chart(self) -> Dict:
        """Calcola dati presenze per grafico."""
        classi = set(s.classe for s in self.anagrafica.studenti)
        
        presenze_data = []
        assenze_data = []
        
        for classe in sorted(classi):
            # Simula dati (da implementare con dati reali presenze)
            presenze_data.append(len([s for s in self.anagrafica.studenti if s.classe == classe]) * 0.9)
            assenze_data.append(len([s for s in self.anagrafica.studenti if s.classe == classe]) * 0.1)
        
        return {
            "labels": sorted(classi),
            "presenze": presenze_data,
            "assenze": assenze_data
        }
    
    # ============ DECORATORS ============
    
    def _init_analytics(self):
        """Inizializza il modulo analytics."""
        if self.comunicazioni is None:
            return
            
        try:
            self.analytics = AnaliticaPredittiva(
                self.anagrafica, 
                self.voti, 
                self.insegnanti, 
                self.comunicazioni
            )
        except Exception as e:
            print(f"⚠️  Analytics non disponibile: {e}")
            self.analytics = None
    
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
        print("   - admin/admin123 (Amministratore)")
        print("   - dirigente/dirigente123 (Dirigente)")
        print("   - insegnante/insegnante123 (Insegnante)")
        print("   - studente/studente123 (Studente)")
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

