"""
Modulo per la generazione di report aggregati.
Crea report completi su vari aspetti del sistema scolastico.
"""

from typing import Dict, List, Optional
from datetime import datetime
import utils


class GeneratoreReport:
    """Genera report aggregati sul sistema scolastico."""
    
    def __init__(self, anagrafica, gestione_voti, gestione_insegnanti, 
                 analisi_didattica, calcolatore_indicatori):
        """Inizializza il generatore di report.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
            gestione_insegnanti: Istanza di GestioneInsegnanti
            analisi_didattica: Istanza di AnalisiDidattica
            calcolatore_indicatori: Istanza di CalcolatoreIndicatori
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
        self.gestione_insegnanti = gestione_insegnanti
        self.analisi_didattica = analisi_didattica
        self.calcolatore_indicatori = calcolatore_indicatori
    
    def report_annuale(self) -> Dict:
        """Genera un report annuale completo.
        
        Returns:
            Dizionario con report annuale
        """
        return {
            "anno": datetime.now().year,
            "data_generazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "riepilogo_generale": self._riepilogo_generale(),
            "statistiche_studenti": self.anagrafica.statistiche_generali(),
            "statistiche_voti": self.gestione_voti.statistiche_generali(),
            "statistiche_insegnanti": self.gestione_insegnanti.statistiche_generali(),
            "graduatorie": {
                "top_10_studenti": self.analisi_didattica.graduatoria_studenti()[:10],
                "top_5_insegnanti": self.analisi_didattica.graduatoria_insegnanti(
                    self.gestione_insegnanti
                )[:5]
            },
            "analisi_equita": self.analisi_didattica.impatto_didattico_fragili(),
            "correlazione_reddito": self.analisi_didattica.correlazione_reddito_rendimento(),
            "indicatori": self.calcolatore_indicatori.sintesi_indicatori()
        }
    
    def report_classe(self, classe: str) -> Dict:
        """Genera un report per una classe specifica.
        
        Args:
            classe: Nome della classe
            
        Returns:
            Dizionario con report classe
        """
        studenti_classe = self.anagrafica.studenti_per_classe(classe)
        
        if not studenti_classe:
            return {"errore": f"Classe {classe} non trovata"}
        
        # Calcola statistiche
        medie = []
        for studente in studenti_classe:
            media = self.gestione_voti.media_studente(studente.id)
            if media > 0:
                medie.append(media)
        
        media_classe = utils.calcola_media(medie) if medie else 0
        
        return {
            "classe": classe,
            "data_generazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "numero_studenti": len(studenti_classe),
            "media_classe": round(media_classe, 2),
            "statistiche_studenti": {
                "media_eta": round(utils.calcola_media([s.eta for s in studenti_classe]), 1),
                "numero_maschi": sum(1 for s in studenti_classe if s.nome[-1] == 'o'),
                "numero_femmine": sum(1 for s in studenti_classe if s.nome[-1] == 'a')
            },
            "distribuzione_fragilita": self._distribuzione_fragilita(studenti_classe),
            "top_3_studenti": self._top_studenti_classe(classe, 3)
        }
    
    def report_insegnante(self, insegnante_id: int) -> Dict:
        """Genera un report per un insegnante specifico.
        
        Args:
            insegnante_id: ID insegnante
            
        Returns:
            Dizionario con report insegnante
        """
        insegnante = self.gestione_insegnanti.trova_insegnante(insegnante_id)
        
        if not insegnante:
            return {"errore": f"Insegnante {insegnante_id} non trovato"}
        
        # Voti dati dall'insegnante
        voti_prof = [
            v for v in self.gestione_voti.voti
            if v.materia in insegnante.materie
        ]
        
        return {
            "insegnante": {
                "id": insegnante.id,
                "nome": insegnante.nome_completo,
                "materie": insegnante.materie,
                "esperienza": insegnante.anni_esperienza,
                "carico_lavoro": insegnante.carico_lavoro
            },
            "data_generazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "statistiche_voti": {
                "totale_voti": len(voti_prof),
                "media_voti": round(utils.calcola_media([v.voto for v in voti_prof]), 2),
                "voti_insufficienza": sum(1 for v in voti_prof if v.voto < 6),
                "voti_sufficienza": sum(1 for v in voti_prof if v.voto >= 6)
            },
            "distribuzione_voti": self._distribuzione_voti(voti_prof),
            "orario_settimanale": insegnante.totale_ore_settimanali
        }
    
    def report_equita_educativa(self) -> Dict:
        """Genera un report sull'equità educativa.
        
        Returns:
            Dizionario con report equità
        """
        impatto = self.analisi_didattica.impatto_didattico_fragili()
        correlazione = self.analisi_didattica.correlazione_reddito_rendimento()
        
        return {
            "tipo": "Report Equità Educativa",
            "data_generazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gap_pedagogico": {
                "valore": impatto.get("gap_pedagogico", 0),
                "interpretazione": "Fragili" if impatto.get("gap_pedagogico", 0) > 1.5 
                                 else "Equilibrato" if impatto.get("gap_pedagogico", 0) < 1.0 
                                 else "Attenzione richiesta"
            },
            "correlazione_reddito": correlazione,
            "distribuzione_reddito": self._distribuzione_reddito(),
            "indicatori_equita": self.calcolatore_indicatori.indice_equita_educativa(),
            "raccomandazioni": self._raccomandazioni_equita(impatto)
        }
    
    def report_performance(self) -> Dict:
        """Genera un report sulle performance complessive.
        
        Returns:
            Dizionario con report performance
        """
        graduatoria = self.analisi_didattica.graduatoria_studenti()
        
        return {
            "tipo": "Report Performance",
            "data_generazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "performance_generale": {
                "media_totale": self.gestione_voti.statistiche_generali().get("media_generale", 0),
                "numero_studenti": len(self.anagrafica.studenti),
                "eccellenti": sum(1 for s in graduatoria if s["media"] >= 9),
                "buoni": sum(1 for s in graduatoria if 7 <= s["media"] < 9),
                "sufficienti": sum(1 for s in graduatoria if 6 <= s["media"] < 7),
                "insufficienti": sum(1 for s in graduatoria if s["media"] < 6)
            },
            "classi_performance": self._classi_performance(),
            "trend_materie": self._trend_materie(),
            "indicatori_qualita": self.calcolatore_indicatori.indice_qualita_scolastica()
        }
    
    def report_sintetico(self) -> str:
        """Genera un report testuale sintetico.
        
        Returns:
            Stringa con report sintetico
        """
        riepilogo = self._riepilogo_generale()
        
        report = "="*80 + "\n"
        report += "REGISTRO SCOLASTICO - REPORT SINTETICO".center(80) + "\n"
        report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += "="*80 + "\n\n"
        
        report += f"📊 RIEPILOGO GENERALE\n"
        report += f"-"*80 + "\n"
        report += f"Studenti: {riepilogo['totale_studenti']}\n"
        report += f"Insegnanti: {riepilogo['totale_insegnanti']}\n"
        report += f"Classi: {riepilogo['totale_classi']}\n"
        report += f"Media generale: {riepilogo['media_generale']}\n\n"
        
        report += f"📈 INDICATORI\n"
        report += f"-"*80 + "\n"
        indicatori = self.calcolatore_indicatori.sintesi_indicatori()
        report += f"Valutazione generale: {indicatori['valutazione']}\n"
        report += f"Punteggio medio: {indicatori['media_generale']}/100\n\n"
        
        report += f"🎯 RACCOMANDAZIONI\n"
        report += f"-"*80 + "\n"
        for racc in indicatori['raccomandazioni']:
            report += f"• {racc}\n"
        
        report += "\n" + "="*80 + "\n"
        
        return report
    
    def _riepilogo_generale(self) -> Dict:
        """Calcola il riepilogo generale."""
        return {
            "totale_studenti": len(self.anagrafica.studenti),
            "totale_insegnanti": len(self.gestione_insegnanti.insegnanti),
            "totale_classi": len(set(s.classe for s in self.anagrafica.studenti)),
            "media_generale": round(
                self.gestione_voti.statistiche_generali().get("media_generale", 0), 2
            )
        }
    
    def _distribuzione_fragilita(self, studenti: List) -> Dict:
        """Calcola la distribuzione della fragilità."""
        fragili_alte = sum(1 for s in studenti if s.fragilità_sociale >= 60)
        fragili_medie = sum(1 for s in studenti if 30 <= s.fragilità_sociale < 60)
        fragili_basse = sum(1 for s in studenti if s.fragilità_sociale < 30)
        
        return {
            "alta": fragili_alte,
            "media": fragili_medie,
            "bassa": fragili_basse
        }
    
    def _top_studenti_classe(self, classe: str, limit: int = 3) -> List[Dict]:
        """Restituisce i top studenti di una classe."""
        studenti_classe = self.anagrafica.studenti_per_classe(classe)
        
        risultati = []
        for studente in studenti_classe:
            media = self.gestione_voti.media_studente(studente.id)
            if media > 0:
                risultati.append({
                    "nome": studente.nome_completo,
                    "media": round(media, 2)
                })
        
        # Ordina per media
        risultati.sort(key=lambda x: x["media"], reverse=True)
        return risultati[:limit]
    
    def _distribuzione_voti(self, voti: List) -> Dict:
        """Calcola la distribuzione dei voti."""
        distribuzione = {}
        for voto in voti:
            fascia = f"{int(voto.voto)}-{int(voto.voto)+0.9}"
            distribuzione[fascia] = distribuzione.get(fascia, 0) + 1
        return distribuzione
    
    def _distribuzione_reddito(self) -> Dict:
        """Calcola la distribuzione del reddito."""
        categorie = {}
        for studente in self.anagrafica.studenti:
            cat = studente.categoria_reddito.name
            categorie[cat] = categorie.get(cat, 0) + 1
        return categorie
    
    def _classi_performance(self) -> List[Dict]:
        """Restituisce le classi ordinate per performance."""
        classi_performance = []
        
        for classe in set(s.classe for s in self.anagrafica.studenti):
            studenti = self.anagrafica.studenti_per_classe(classe)
            medie = []
            for studente in studenti:
                media = self.gestione_voti.media_studente(studente.id)
                if media > 0:
                    medie.append(media)
            
            if medie:
                classi_performance.append({
                    "classe": classe,
                    "media": round(utils.calcola_media(medie), 2),
                    "studenti": len(studenti)
                })
        
        # Ordina per media
        classi_performance.sort(key=lambda x: x["media"], reverse=True)
        return classi_performance
    
    def _trend_materie(self) -> Dict:
        """Analizza le performance per materia."""
        materie_performance = {}
        
        for voto in self.gestione_voti.voti:
            materia = voto.materia
            if materia not in materie_performance:
                materie_performance[materia] = []
            materie_performance[materia].append(voto.voto)
        
        # Calcola medie
        trend = {}
        for materia, voti in materie_performance.items():
            trend[materia] = {
                "media": round(utils.calcola_media(voti), 2),
                "numero_voti": len(voti)
            }
        
        return trend
    
    def _raccomandazioni_equita(self, impatto: Dict) -> List[str]:
        """Genera raccomandazioni basate sull'impatto."""
        raccomandazioni = []
        
        gap = impatto.get("gap_pedagogico", 0)
        
        if gap > 2.0:
            raccomandazioni.append("Gap pedagogico critico: implementare programmi di recupero urgenti")
        elif gap > 1.0:
            raccomandazioni.append("Gap pedagogico significativo: aumentare supporto agli studenti fragili")
        else:
            raccomandazioni.append("Equità educativa in buono stato: continuare a monitorare")
        
        return raccomandazioni
