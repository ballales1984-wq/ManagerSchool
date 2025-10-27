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
