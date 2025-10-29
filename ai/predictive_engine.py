"""
AI Predittiva Leggera - ManagerSchool
Sistema di machine learning per predizioni educative
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class PredictionResult:
    """Risultato predizione."""
    
    rischio_insufficienza: float  # 0-100
    probabilita_miglioramento: float  # 0-100
    previsione_voto_finale: float  # 3-10
    raccomandazioni: List[str]
    livello_fiducia: float  # 0-100


class PredictiveEngine:
    """Motore AI per predizioni educative."""
    
    def __init__(self):
        """Inizializza motore predittivo."""
        self.models = {}
    
    def predict_rischio_insufficienza(self, studente_data: Dict, voti: List[float]) -> float:
        """Predice rischio insufficienza studente.
        
        Args:
            studente_data: Dati studente
            voti: Lista voti recenti
            
        Returns:
            Rischio 0-100
        """
        if not voti:
            return 50.0  # Neutro se nessun voto
        
        # Media voti
        media = sum(voti) / len(voti)
        
        # Trend (differenza ultimi 2 voti)
        trend = 0
        if len(voti) >= 2:
            trend = voti[-1] - voti[-2]
        
        # Fragilità
        fragilita = studente_data.get('fragilita', 50)
        
        # Fattori rischio
        fattori = []
        
        # Media bassa
        if media < 6:
            fattori.append(abs(6 - media) * 10)
        
        # Trend negativo
        if trend < -0.5:
            fattori.append(abs(trend) * 15)
        
        # Fragilità alta
        if fragilita > 70:
            fattori.append((fragilita - 70) / 3)
        
        # Assenze (simulato)
        assenze_rate = studente_data.get('assenze_rate', 0)
        if assenze_rate > 0.1:  # >10%
            fattori.append(assenze_rate * 20)
        
        # Calcola rischio
        rischio = sum(fattori)
        rischio = min(100, max(0, rischio))
        
        return rischio
    
    def predict_miglioramento(self, studente_data: Dict, voti: List[float]) -> float:
        """Predice probabilità miglioramento.
        
        Args:
            studente_data: Dati studente
            voti: Lista voti recenti
            
        Returns:
            Probabilità 0-100
        """
        if not voti:
            return 50.0
        
        media = sum(voti) / len(voti)
        trend = 0
        if len(voti) >= 2:
            trend = voti[-1] - voti[0]
        
        # Fattori positivi
        probabilità = 50.0
        
        # Trend positivo
        if trend > 0:
            probabilità += trend * 10
        
        # Fragilità medio-bassa
        fragilita = studente_data.get('fragilita', 50)
        if fragilita < 50:
            probabilità += (50 - fragilita) / 2
        
        # Interventi ricevuti
        interventi = studente_data.get('interventi_count', 0)
        probabilità += interventi * 5
        
        # Media decente
        if media >= 5.5:
            probabilità += 10
        
        probabilità = min(100, max(0, probabilità))
        
        return probabilità
    
    def predict_voto_finale(self, voti: List[float], trend: float = 0) -> float:
        """Predice voto finale.
        
        Args:
            voti: Lista voti
            trend: Trend attuale
            
        Returns:
            Voto previsto 3-10
        """
        if not voti:
            return 5.0
        
        media = sum(voti) / len(voti)
        
        # Applica trend se presente
        previsione = media + (trend * 0.3)
        
        # Limita range
        previsione = max(3.0, min(10.0, previsione))
        
        return round(previsione, 1)
    
    def generate_raccomandazioni(self, studente_data: Dict, rischio: float) -> List[str]:
        """Genera raccomandazioni personalizzate.
        
        Args:
            studente_data: Dati studente
            rischio: Rischio insufficienza
            
        Returns:
            Lista raccomandazioni
        """
        raccomandazioni = []
        
        if rischio > 70:
            raccomandazioni.append("⚠️ Rischio alto - Richiedi colloquio urgente con famiglia")
            raccomandazioni.append("📞 Attiva supporto psicologico se necessario")
            raccomandazioni.append("📋 Programma interventi didattici mirati")
        elif rischio > 40:
            raccomandazioni.append("🔔 Monitoraggio attentivo consigliato")
            raccomandazioni.append("📚 Assegna esercizi di recupero")
            raccomandazioni.append("👥 Richiedi supporto peer learning")
        else:
            raccomandazioni.append("✅ Situazione stabile - Continua monitoraggio")
        
        # Fragilità alta
        if studente_data.get('fragilita', 0) > 70:
            raccomandazioni.append("💚 Supporto sociale necessario")
        
        # Assenze
        if studente_data.get('assenze_rate', 0) > 0.15:
            raccomandazioni.append("📅 Controlla assenze frequenti")
        
        return raccomandazioni
    
    def predict_complete(self, studente_data: Dict, voti: List[float]) -> PredictionResult:
        """Predizione completa per studente.
        
        Args:
            studente_data: Dati studente
            voti: Lista voti
            
        Returns:
            PredictionResult
        """
        # Calcola metriche
        rischio = self.predict_rischio_insufficienza(studente_data, voti)
        miglioramento = self.predict_miglioramento(studente_data, voti)
        
        # Trend
        trend = 0
        if len(voti) >= 2:
            trend = voti[-1] - voti[-2]
        
        previsione_voto = self.predict_voto_finale(voti, trend)
        
        # Raccomandazioni
        raccomandazioni = self.generate_raccomandazioni(studente_data, rischio)
        
        # Livello fiducia (basato su numero voti)
        num_voti = len(voti)
        fiducia = min(100, num_voti * 10)
        
        return PredictionResult(
            rischio_insufficienza=round(rischio, 1),
            probabilita_miglioramento=round(miglioramento, 1),
            previsione_voto_finale=previsione_voto,
            raccomandazioni=raccomandazioni,
            livello_fiducia=round(fiducia, 1)
        )
    
    def early_warning_system(self, classi: List[Dict]) -> List[Dict]:
        """Sistema early warning per classe.
        
        Args:
            classi: Lista dati classi
            
        Returns:
            Lista studenti a rischio
        """
        warning_list = []
        
        for classe_data in classi:
            studenti = classe_data.get('studenti', [])
            
            for studente in studenti:
                predizione = self.predict_complete(
                    studente,
                    studente.get('voti', [])
                )
                
                if predizione.rischio_insufficienza > 60:
                    warning_list.append({
                        'studente': studente.get('nome_completo', 'Unknown'),
                        'classe': classe_data.get('classe', 'Unknown'),
                        'rischio': predizione.rischio_insufficienza,
                        'voto_previsto': predizione.previsione_voto_finale,
                        'raccomandazioni': predizione.raccomandazioni[:2]  # Prime 2
                    })
        
        # Ordina per rischio
        warning_list.sort(key=lambda x: x['rischio'], reverse=True)
        
        return warning_list


# Istanza globale
predictive_engine = PredictiveEngine()


if __name__ == "__main__":
    print("AI PREDITTIVA - TEST")
    print("=" * 60 + "\n")
    
    # Test studente
    studente = {
        'fragilita': 75,
        'assenze_rate': 0.15,
        'interventi_count': 2
    }
    voti = [5.0, 5.5, 6.0, 5.5, 5.0]
    
    # Predizione completa
    predizione = predictive_engine.predict_complete(studente, voti)
    
    print(f"Rischio Insufficienza: {predizione.rischio_insufficienza}%")
    print(f"Probabilità Miglioramento: {predizione.probabilita_miglioramento}%")
    print(f"Voto Previsto: {predizione.previsione_voto_finale}")
    print(f"Livello Fiducia: {predizione.livello_fiducia}%")
    print(f"\nRaccomandazioni:")
    for racc in predizione.raccomandazioni:
        print(f"  • {racc}")

