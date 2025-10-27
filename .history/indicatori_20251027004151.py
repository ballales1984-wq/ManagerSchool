"""
Modulo per il calcolo di indici sintetici.
Genera indicatori compositi per valutare la qualità del sistema scolastico.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import utils


@dataclass
class IndiceSintetico:
    """Rappresenta un indice sintetico con componenti e peso."""
    nome: str
    valore: float
    componenti: Dict[str, float]
    peso: float = 1.0


class CalcolatoreIndicatori:
    """Calcola indicatori sintetici per il sistema scolastico."""
    
    def __init__(self, anagrafica, gestione_voti, gestione_insegnanti, analisi_didattica):
        """Inizializza il calcolatore di indicatori.
        
        Args:
            anagrafica: Istanza di Anagrafica
            gestione_voti: Istanza di GestioneVoti
            gestione_insegnanti: Istanza di GestioneInsegnanti
            analisi_didattica: Istanza di AnalisiDidattica
        """
        self.anagrafica = anagrafica
        self.gestione_voti = gestione_voti
        self.gestione_insegnanti = gestione_insegnanti
        self.analisi_didattica = analisi_didattica
    
    def indice_qualita_scolastica(self) -> IndiceSintetico:
        """Calcola l'indice di qualità scolastica generale (0-100).
        
        Componenti:
        - Media generale voti (40%)
        - Performance studenti fragili (30%)
        - Equità educativa (20%)
        - Grado copertura insegnanti (10%)
        
        Returns:
            IndiceSintetico con valore e componenti
        """
        # Media generale
        medie_studenti = []
        for studente in self.anagrafica.studenti:
            media = self.gestione_voti.media_studente(studente.id)
            if media > 0:
                medie_studenti.append(media)
        
        media_generale = utils.calcola_media(medie_studenti) if medie_studenti else 0.0
        componente_media = (media_generale / 10.0) * 40
        
        # Performance studenti fragili
        fragili = self.anagrafica.studenti_per_fragilita(min_fragilita=50)
        medie_fragili = []
        for studente in fragili:
            media = self.gestione_voti.media_studente(studente.id)
            if media > 0:
                medie_fragili.append(media)
        
        media_fragili = utils.calcola_media(medie_fragili) if medie_fragili else 0.0
        componente_fragili = (media_fragili / 10.0) * 30
        
        # Equità educativa
        impatto = self.analisi_didattica.impatto_didattico_fragili()
        gap = impatto.get("gap_pedagogico", 0)
        equita = max(0, 20 - (gap * 4))  # Minus per gap maggiore
        componente_equita = min(20, equita)
        
        # Copertura insegnanti
        totale_ore = sum(i.totale_ore_settimanali for i in self.gestione_insegnanti.insegnanti)
        ore_necessarie = len(self.anagrafica.studenti) * 10  # Stima
        copertura = min(100, (totale_ore / ore_necessarie) * 100) if ore_necessarie > 0 else 0
        componente_copertura = (copertura / 100.0) * 10
        
        valore_complessivo = componente_media + componente_fragili + componente_equita + componente_copertura
        
        return IndiceSintetico(
            nome="Indice Qualità Scolastica",
            valore=round(valore_complessivo, 2),
            componenti={
                "Media generale": round(componente_media, 2),
                "Performance fragili": round(componente_fragili, 2),
                "Equità educativa": round(componente_equita, 2),
                "Copertura insegnanti": round(componente_copertura, 2)
            }
        )
    
    def indice_equita_educativa(self) -> IndiceSintetico:
        """Calcola l'indice di equità educativa (0-100).
        
        Componenti:
        - Riduzione gap pedagogico (40%)
        - Dispersione sociale (30%)
        - Accessibilità reddito (30%)
        
        Returns:
            IndiceSintetico con valore e componenti
        """
        # Gap pedagogico (invertito: gap alto = equità bassa)
        impatto = self.analisi_didattica.impatto_didattico_fragili()
        gap = impatto.get("gap_pedagogico", 0)
        componente_gap = max(0, 40 - (gap * 8))
        
        # Dispersione sociale
        fragilità = [s.fragilità_sociale for s in self.anagrafica.studenti]
        if fragilità:
            deviazione = utils.calcola_deviazione_standard(fragilità)
            componente_disperione = max(0, 30 - (deviazione / 2))
        else:
            componente_disperione = 0
        
        # Accessibilità reddito
        correlazione = self.analisi_didattica.correlazione_reddito_rendimento()
        medie_fasce = []
        for fascia, dati in correlazione.items():
            if isinstance(dati, dict) and dati.get("media_rendimento", 0) > 0:
                medie_fasce.append(dati["media_rendimento"])
        
        if len(medie_fasce) > 1:
            range_rendimento = max(medie_fasce) - min(medie_fasce)
            componente_accessibilita = max(0, 30 - (range_rendimento * 5))
        else:
            componente_accessibilita = 15
        
        valore_complessivo = componente_gap + componente_disperione + componente_accessibilita
        
        return IndiceSintetico(
            nome="Indice Equità Educativa",
            valore=round(valore_complessivo, 2),
            componenti={
                "Riduzione gap": round(componente_gap, 2),
                "Dispersione sociale": round(componente_disperione, 2),
                "Accessibilità reddito": round(componente_accessibilita, 2)
            }
        )
    
    def indice_efficacia_didattica(self) -> IndiceSintetico:
        """Calcola l'indice di efficacia didattica (0-100).
        
        Componenti:
        - Media efficacia insegnanti (50%)
        - Crescita studenti fragili (30%)
        - Stabilità risultati (20%)
        
        Returns:
            IndiceSintetico con valore e componenti
        """
        # Media efficacia insegnanti
        graduatoria_insegnanti = self.analisi_didattica.graduatoria_insegnanti(
            self.gestione_insegnanti
        )
        if graduatoria_insegnanti:
            efficacie = [i["efficacia"] for i in graduatoria_insegnanti]
            media_efficacia = utils.calcola_media(efficacie)
            componente_insegnanti = (media_efficacia / 100.0) * 50
        else:
            componente_insegnanti = 0
        
        # Crescita studenti fragili
        fragili = self.anagrafica.studenti_per_fragilita(min_fragilita=50)
        if fragili:
            medie_fragili = [
                self.gestione_voti.media_studente(s.id) 
                for s in fragili
            ]
            media_fragile = utils.calcola_media([m for m in medie_fragili if m > 0])
            componente_crescita = (media_fragile / 10.0) * 30
        else:
            componente_crescita = 0
        
        # Stabilità risultati (variabilità media)
        medie_tutti = [
            self.gestione_voti.media_studente(s.id) 
            for s in self.anagrafica.studenti
        ]
        medie_valide = [m for m in medie_tutti if m > 0]
        if len(medie_valide) > 1:
            variabilita = utils.calcola_deviazione_standard(medie_valide)
            componente_stabilita = max(0, 20 - (variabilita * 2))
        else:
            componente_stabilita = 10
        
        valore_complessivo = componente_insegnanti + componente_crescita + componente_stabilita
        
        return IndiceSintetico(
            nome="Indice Efficacia Didattica",
            valore=round(valore_complessivo, 2),
            componenti={
                "Efficacia insegnanti": round(componente_insegnanti, 2),
                "Crescita fragili": round(componente_crescita, 2),
                "Stabilità risultati": round(componente_stabilita, 2)
            }
        )
    
    def indice_coesione_sociale(self) -> IndiceSintetico:
        """Calcola l'indice di coesione sociale (0-100).
        
        Componenti:
        - Distribuzione equa fragilità (40%)
        - Omogeneità classi (30%)
        - Integrazione inclusiva (30%)
        
        Returns:
            IndiceSintetico con valore e componenti
        """
        # Distribuzione fragilità
        statistiche = self.anagrafica.statistica_fragilita()
        tot = statistiche.get("totale", 0)
        if tot > 0:
            distribuzione_equa = 40 * (1 - abs(statistiche.get("percentuale_alta", 0) - 25) / 100)
            componente_distribuzione = max(0, distribuzione_equa)
        else:
            componente_distribuzione = 0
        
        # Omogeneità classi
        classi = set(s.classe for s in self.anagrafica.studenti)
        if classi:
            studenti_per_classe = [len(self.anagrafica.studenti_per_classe(c)) for c in classi]
            if studenti_per_classe:
                max_classe = max(studenti_per_classe)
                min_classe = min(studenti_per_classe)
                omogeneita = 30 * (1 - (max_classe - min_classe) / max_classe if max_classe > 0 else 1)
                componente_omogeneita = max(0, omogeneita)
            else:
                componente_omogeneita = 0
        else:
            componente_omogeneita = 0
        
        # Integrazione inclusiva
        totale_studenti = len(self.anagrafica.studenti)
        fragili = len(self.anagrafica.studenti_per_fragilita(min_fragilita=50))
        if totale_studenti > 0:
            integrazione = 30 * (1 - abs(fragili / totale_studenti - 0.25))
            componente_integrazione = max(0, integrazione)
        else:
            componente_integrazione = 0
        
        valore_complessivo = componente_distribuzione + componente_omogeneita + componente_integrazione
        
        return IndiceSintetico(
            nome="Indice Coesione Sociale",
            valore=round(valore_complessivo, 2),
            componenti={
                "Distribuzione fragilità": round(componente_distribuzione, 2),
                "Omogeneità classi": round(componente_omogeneita, 2),
                "Integrazione inclusiva": round(componente_integrazione, 2)
            }
        )
    
    def indice_benessere_scolastico(self) -> IndiceSintetico:
        """Calcola l'indice di benessere scolastico complessivo (0-100).
        
        Componenti:
        - Sicurezza reddito (30%)
        - Qualità salute (30%)
        - Supporto familiare (20%)
        - Rendimento scolastico (20%)
        
        Returns:
            IndiceSintetico con valore e componenti
        """
        # Sicurezza reddito
        redditi = [s.reddito_familiare for s in self.anagrafica.studenti]
        if redditi:
            media_reddito = utils.calcola_media(redditi)
            # Normalizza (considera €25000 come soglia sicurezza)
            componente_reddito = min(30, (media_reddito / 25000) * 30)
        else:
            componente_reddito = 0
        
        # Qualità salute
        eccellenti = sum(1 for s in self.anagrafica.studenti 
                        if s.condizione_salute.value == "Eccellente")
        buone = sum(1 for s in self.anagrafica.studenti 
                   if s.condizione_salute.value == "Buona")
        tot = len(self.anagrafica.studenti)
        if tot > 0:
            percentuale_salute = ((eccellenti + buone) / tot) * 100
            componente_salute = (percentuale_salute / 100) * 30
        else:
            componente_salute = 0
        
        # Supporto familiare
        nucleo_tradizionale = sum(1 for s in self.anagrafica.studenti 
                                  if s.situazione_familiare == "Nucleo tradizionale")
        if tot > 0:
            percentuale_famiglia = (nucleo_tradizionale / tot) * 100
            componente_famiglia = (percentuale_famiglia / 100) * 20
        else:
            componente_famiglia = 0
        
        # Rendimento scolastico
        medie = []
        for studente in self.anagrafica.studenti:
            media = self.gestione_voti.media_studente(studente.id)
            if media > 0:
                medie.append(media)
        
        if medie:
            media_rendimento = utils.calcola_media(medie)
            componente_rendimento = (media_rendimento / 10.0) * 20
        else:
            componente_rendimento = 0
        
        valore_complessivo = componente_reddito + componente_salute + componente_famiglia + componente_rendimento
        
        return IndiceSintetico(
            nome="Indice Benessere Scolastico",
            valore=round(valore_complessivo, 2),
            componenti={
                "Sicurezza reddito": round(componente_reddito, 2),
                "Qualità salute": round(componente_salute, 2),
                "Supporto familiare": round(componente_famiglia, 2),
                "Rendimento": round(componente_rendimento, 2)
            }
        )
    
    def quadro_indicatori_completo(self) -> Dict[str, IndiceSintetico]:
        """Calcola tutti gli indicatori sintetici.
        
        Returns:
            Dizionario con tutti gli indici
        """
        return {
            "qualita_scolastica": self.indice_qualita_scolastica(),
            "equita_educativa": self.indice_equita_educativa(),
            "efficacia_didattica": self.indice_efficacia_didattica(),
            "coesione_sociale": self.indice_coesione_sociale(),
            "benessere_scolastico": self.indice_benessere_scolastico()
        }
    
    def sintesi_indicatori(self) -> Dict:
        """Genera una sintesi testuale degli indicatori.
        
        Returns:
            Dizionario con sintesi e valutazione
        """
        indicatori = self.quadro_indicatori_completo()
        
        # Calcola media generale
        valori = [ind.valore for ind in indicatori.values()]
        media_generale = utils.calcola_media(valori) if valori else 0
        
        # Valutazione generale
        if media_generale >= 80:
            valutazione = "Eccellente"
        elif media_generale >= 65:
            valutazione = "Buona"
        elif media_generale >= 50:
            valutazione = "Sufficiente"
        elif media_generale >= 35:
            valutazione = "Insufficiente"
        else:
            valutazione = "Critica"
        
        return {
            "media_generale": round(media_generale, 2),
            "valutazione": valutazione,
            "indicatori": {
                k: {
                    "nome": v.nome,
                    "valore": v.valore,
                    "componenti": v.componenti
                }
                for k, v in indicatori.items()
            },
            "raccomandazioni": self._genera_raccomandazioni(indicatori)
        }
    
    def _genera_raccomandazioni(self, indicatori: Dict) -> List[str]:
        """Genera raccomandazioni basate sugli indicatori.
        
        Args:
            indicatori: Dizionario con tutti gli indici
            
        Returns:
            Lista di raccomandazioni
        """
        raccomandazioni = []
        
        for chiave, indice in indicatori.items():
            if indice.valore < 50:
                if chiave == "qualita_scolastica":
                    raccomandazioni.append("Investire in formazione docenti e supporto agli studenti più fragili")
                elif chiave == "equita_educativa":
                    raccomandazioni.append("Implementare programmi di sostegno per ridurre le disuguaglianze")
                elif chiave == "efficacia_didattica":
                    raccomandazioni.append("Valutare metodi didattici e aumentare supporto agli insegnanti")
                elif chiave == "coesione_sociale":
                    raccomandazioni.append("Promuovere attività inclusive e migliorare composizione classi")
                elif chiave == "benessere_scolastico":
                    raccomandazioni.append("Rafforzare supporto alle famiglie e monitorare condizioni studenti")
        
        if not raccomandazioni:
            raccomandazioni.append("Continua a monitorare gli indicatori e mantieni gli standard attuali")
        
        return raccomandazioni
