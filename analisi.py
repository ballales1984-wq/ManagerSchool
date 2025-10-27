"""
Modulo per analisi e statistiche avanzate.
Calcola graduatorie, impatto didattico, equità educativa.
"""

from typing import List, Dict, Optional
import utils


class AnalisiDidattica:
    """Esegue analisi didattiche avanzate."""
    
    def __init__(self, anagrafica, gestione_voti):
        """Inizializza l'analisi didattica.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
    
    def graduatoria_studenti(self, ordine: str = "decrescente") -> List[Dict]:
        """Genera una graduatoria degli studenti per media.
        
        Args:
            ordine: 'crescente' o 'decrescente'
            
        Returns:
            Lista di dizionari con informazioni studenti ordinati
        """
        risultati = []
        
        for studente in self.anagrafica.studenti:
            media = self.gestione_voti.media_studente(studente.id)
            risultati.append({
                "id": studente.id,
                "nome": studente.nome_completo,
                "classe": studente.classe,
                "media": media,
                "fragilita": studente.fragilità_sociale
            })
        
        # Ordina per media
        reverse = (ordine == "decrescente")
        risultati.sort(key=lambda x: x["media"], reverse=reverse)
        
        # Aggiungi posizione
        for i, risultato in enumerate(risultati, 1):
            risultato["posizione"] = i
        
        return risultati
    
    def graduatoria_insegnanti(self, gestione_insegnanti) -> List[Dict]:
        """Genera una graduatoria degli insegnanti per efficacia.
        
        Args:
            gestione_insegnanti: Istanza di GestioneInsegnanti
            
        Returns:
            Lista di insegnanti ordinati per efficacia didattica
        """
        risultati = []
        
        for insegnante in gestione_insegnanti.insegnanti:
            # Calcola la media dei voti dati dal professore
            voti_prof = [
                v.voto for v in self.gestione_voti.voti 
                if v.materia in insegnante.materie
            ]
            
            media_voti = utils.calcola_media(voti_prof) if voti_prof else 6.0
            
            efficacia = self._calcola_efficacia(insegnante, media_voti)
            
            risultati.append({
                "id": insegnante.id,
                "nome": insegnante.nome_completo,
                "materie": ", ".join(insegnante.materie),
                "media_voti": round(media_voti, 2),
                "esperienza": insegnante.anni_esperienza,
                "efficacia": round(efficacia, 2)
            })
        
        # Ordina per efficacia
        risultati.sort(key=lambda x: x["efficacia"], reverse=True)
        
        return risultati
    
    def _calcola_efficacia(self, insegnante, media_voti: float) -> float:
        """Calcola un indice di efficacia didattica.
        
        Args:
            insegnante: Insegnante da valutare
            media_voti: Media dei voti assegnati
            
        Returns:
            Indice di efficacia (0-100)
        """
        # Fattori: media voti (50%), esperienza (30%), carico lavoro (20%)
        peso_voti = media_voti / 10.0 * 50
        peso_esperienza = min(insegnante.anni_esperienza / 35.0, 1.0) * 30
        
        # Carico ottimale è considerato tra 14-18 ore
        ore = insegnante.totale_ore_settimanali
        if 14 <= ore <= 18:
            peso_carico = 20
        elif ore < 14:
            peso_carico = ore / 14.0 * 15
        else:
            peso_carico = max(0, 20 - (ore - 18) * 2)
        
        return peso_voti + peso_esperienza + peso_carico
    
    def impatto_didattico_fragili(self) -> Dict:
        """Analizza l'impatto didattico sugli studenti fragili.
        
        Returns:
            Dizionario con statistiche sull'impatto
        """
        studenti_fragili = self.anagrafica.studenti_per_fragilita(min_fragilita=50)
        studenti_non_fragili = self.anagrafica.studenti_per_fragilita(max_fragilita=50)
        
        # Calcola medie
        media_fragili = 0.0
        if studenti_fragili:
            medie = [self.gestione_voti.media_studente(s.id) for s in studenti_fragili]
            media_fragili = utils.calcola_media(medie) if medie else 0.0
        
        media_non_fragili = 0.0
        if studenti_non_fragili:
            medie = [self.gestione_voti.media_studente(s.id) for s in studenti_non_fragili]
            media_non_fragili = utils.calcola_media(medie) if medie else 0.0
        
        differenza = media_non_fragili - media_fragili if media_fragili > 0 else 0
        
        return {
            "studenti_fragili": len(studenti_fragili),
            "studenti_non_fragili": len(studenti_non_fragili),
            "media_fragili": round(media_fragili, 2),
            "media_non_fragili": round(media_non_fragili, 2),
            "gap_pedagogico": round(differenza, 2),
            "equita_educativa": "Buona" if differenza < 1.0 else "Da migliorare"
        }
    
    def correlazione_reddito_rendimento(self) -> Dict:
        """Analizza la correlazione tra reddito familiare e rendimento scolastico.
        
        Returns:
            Dizionario con risultati dell'analisi
        """
        fasce_reddito = {
            "Molto Basso": [],
            "Basso": [],
            "Medio": [],
            "Alto": []
        }
        
        for studente in self.anagrafica.studenti:
            media = self.gestione_voti.media_studente(studente.id)
            categoria = studente.categoria_reddito.name
            
            if categoria in fasce_reddito:
                fasce_reddito[categoria].append(media)
        
        risultati = {}
        for fascia, medie in fasce_reddito.items():
            risultati[fascia] = {
                "numero_studenti": len(medie),
                "media_rendimento": round(utils.calcola_media(medie), 2) if medie else 0.0
            }
        
        return risultati
    
    def classe_piu_brillante(self) -> Dict:
        """Identifica la classe con il rendimento migliore.
        
        Returns:
            Dizionario con informazioni sulla classe migliore
        """
        classi = {}
        
        for studente in self.anagrafica.studenti:
            classe = studente.classe
            if classe not in classi:
                classi[classe] = []
            
            media = self.gestione_voti.media_studente(studente.id)
            classi[classe].append(media)
        
        # Calcola media per classe
        medie_classi = {
            classe: utils.calcola_media(medie) 
            for classe, medie in classi.items()
        }
        
        if not medie_classi:
            return {"messaggio": "Nessuna classe disponibile"}
        
        migliore = max(medie_classi.items(), key=lambda x: x[1])
        
        return {
            "classe": migliore[0],
            "media": round(migliore[1], 2),
            "numero_studenti": len(classi[migliore[0]])
        }
    
    def analisi_completa(self, gestione_insegnanti) -> Dict:
        """Esegue un'analisi completa del sistema scolastico.
        
        Args:
            gestione_insegnanti: Istanza di GestioneInsegnanti
            
        Returns:
            Dizionario con tutti i risultati dell'analisi
        """
        return {
            "graduatoria_studenti": self.graduatoria_studenti()[:10],  # Top 10
            "graduatoria_insegnanti": self.graduatoria_insegnanti(gestione_insegnanti)[:5],
            "impatto_fragili": self.impatto_didattico_fragili(),
            "correlazione_reddito": self.correlazione_reddito_rendimento(),
            "classe_migliore": self.classe_piu_brillante(),
            "statistiche_voti": self.gestione_voti.statistiche_generali()
        }
    
    # ===== NUOVE FUNZIONALITÀ: ANALISI ETICHE E SOCIALI =====
    
    def calcola_indici_sintetici_studente(self, studente) -> Dict:
        """Calcola indici sintetici per un singolo studente.
        
        Args:
            studente: Istanza di Studente
            
        Returns:
            Dizionario con indici di fragilità e resilienza
        """
        punteggi = {}
        
        # Fragilità familiare
        famiglie_fragili = ["separati", "vedovo", "affidamento", "monoparentale"]
        punteggi["fragilità_familiare"] = 1 if studente.situazione_familiare in famiglie_fragili else 0
        
        # Fragilità economica (normalizzata)
        reddito = studente.reddito_familiare
        punteggi["fragilità_economica"] = round(1 - min(reddito / 45000, 1), 2)
        
        # Fragilità sanitaria
        condizioni_salute_numeric = {
            "Eccellente": 0,
            "Buona": 0.25,
            "Discreta": 0.5,
            "Scarsa": 0.75,
            "Critica": 1.0
        }
        punteggi["fragilità_sanitaria"] = condizioni_salute_numeric.get(
            studente.condizione_salute.value, 0
        )
        
        # Resilienza educativa
        media = self.gestione_voti.media_studente(studente.id)
        fragilità_totale = sum(punteggi.values())
        punteggi["resilienza_educativa"] = round(media / (1 + fragilità_totale), 2) if fragilità_totale > 0 else media
        
        return punteggi
    
    def dati_pubblici_studente(self, studente) -> Dict:
        """Restituisce solo i dati pubblicamente visibili.
        
        Args:
            studente: Istanza di Studente
            
        Returns:
            Dizionario con dati pubblici
        """
        media = self.gestione_voti.media_studente(studente.id)
        return {
            "nome": studente.nome,
            "cognome": studente.cognome,
            "classe": studente.classe,
            "media": round(media, 2)
        }
    
    def dati_privati_studente(self, studente) -> Dict:
        """Restituisce tutti i dati, inclusi quelli sensibili.
        
        Args:
            studente: Istanza di Studente
            
        Returns:
            Dizionario con tutti i dati dello studente
        """
        return studente.to_dict()
    
    def report_fragilita_sistema(self) -> Dict:
        """Restituisce un report aggregato sulla fragilità familiare ed economica.
        
        Returns:
            Dizionario con statistiche sulla fragilità
        """
        totale = len(self.anagrafica.studenti)
        
        if totale == 0:
            return {"messaggio": "Nessuno studente disponibile"}
        
        # Conta famiglie fragili
        famiglie_fragili_set = {"separati", "vedovo", "affidamento", "monoparentale"}
        separati = sum(1 for s in self.anagrafica.studenti 
                      if s.situazione_familiare in famiglie_fragili_set)
        
        # Reddito medio
        media_reddito = utils.calcola_media([s.reddito_familiare for s in self.anagrafica.studenti])
        
        return {
            "totale_studenti": totale,
            "percentuale_famiglie_fragili": round(separati / totale * 100, 2),
            "reddito_medio": round(media_reddito, 2),
            "student_famiglie_fragili": separati
        }
    
    def report_resilienza_sistema(self) -> Dict:
        """Restituisce la media della resilienza educativa nel sistema.
        
        Returns:
            Dizionario con statistiche sulla resilienza
        """
        valori_resilienza = []
        
        for studente in self.anagrafica.studenti:
            indici = self.calcola_indici_sintetici_studente(studente)
            valori_resilienza.append(indici["resilienza_educativa"])
        
        if not valori_resilienza:
            return {"messaggio": "Nessun dato disponibile"}
        
        media_resilienza = utils.calcola_media(valori_resilienza)
        
        return {
            "media_resilienza": round(media_resilienza, 2),
            "studenti_analizzati": len(valori_resilienza),
            "interpretazione": self._interpreta_resilienza(media_resilienza)
        }
    
    def _interpreta_resilienza(self, valore: float) -> str:
        """Interpreta il valore di resilienza.
        
        Args:
            valore: Valore di resilienza (0-10)
            
        Returns:
            Stringa interpretativa
        """
        if valore >= 8.0:
            return "Eccellente: sistema molto resiliente"
        elif valore >= 6.5:
            return "Buona: sistema resiliente"
        elif valore >= 5.0:
            return "Discreta: resilienza nella media"
        elif valore >= 3.5:
            return "Insufficiente: fragilità significativa"
        else:
            return "Critica: interventi urgenti necessari"
    
    def analisi_equita_completa(self) -> Dict:
        """Esegue un'analisi completa sull'equità del sistema.
        
        Returns:
            Dizionario con analisi di equità
        """
        report_frag = self.report_fragilita_sistema()
        report_resilienza = self.report_resilienza_sistema()
        impatto = self.impatto_didattico_fragili()
        correlazione = self.correlazione_reddito_rendimento()
        
        return {
            "fragilità_sistema": report_frag,
            "resilienza_educativa": report_resilienza,
            "gap_pedagogico": impatto.get("gap_pedagogico", 0),
            "correlazione_reddito": correlazione,
            "valutazione_complessiva": self._valuta_equita_complessiva(report_frag, impatto)
        }
    
    def _valuta_equita_complessiva(self, report_frag: Dict, impatto: Dict) -> str:
        """Valuta l'equità complessiva del sistema.
        
        Args:
            report_frag: Report sulla fragilità
            impatto: Dati sull'impatto didattico
            
        Returns:
            Valutazione testuale
        """
        gap = impatto.get("gap_pedagogico", 0)
        perc_fragili = report_frag.get("percentuale_famiglie_fragili", 50)
        
        if gap < 0.5 and perc_fragili < 20:
            return "Equità Eccellente"
        elif gap < 1.0 and perc_fragili < 30:
            return "Equità Buona"
        elif gap < 1.5 and perc_fragili < 40:
            return "Equità Discreta"
        else:
            return "Equità da Migliorare"
