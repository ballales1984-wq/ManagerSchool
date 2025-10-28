"""
Modulo per la gestione del calendario scolastico italiano.
Gestisce anni scolastici, periodi, vacanze e festività.
"""

import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import calendar

class TipoPeriodo(Enum):
    """Tipi di periodo scolastico."""
    LEZIONI = "Lezioni"
    VACANZE = "Vacanze"
    FESTIVITA = "Festività"
    ESAMI = "Esami"
    RECUPERO = "Recupero"

class TipoVacanza(Enum):
    """Tipi di vacanza."""
    NATALE = "Vacanze di Natale"
    PASQUA = "Vacanze di Pasqua"
    ESTIVE = "Vacanze estive"
    CARNEVALE = "Vacanze di Carnevale"
    PONTE = "Ponte"
    LOCALE = "Festività locale"

@dataclass
class Periodo:
    """Rappresenta un periodo del calendario scolastico."""
    nome: str
    data_inizio: datetime.date
    data_fine: datetime.date
    tipo: TipoPeriodo
    descrizione: str = ""
    giorni_totali: int = 0
    
    def __post_init__(self):
        """Calcola i giorni totali del periodo."""
        if self.giorni_totali == 0:
            delta = self.data_fine - self.data_inizio
            self.giorni_totali = delta.days + 1
    
    def contiene_data(self, data: datetime.date) -> bool:
        """Verifica se una data è contenuta nel periodo."""
        return self.data_inizio <= data <= self.data_fine
    
    def giorni_lavorativi(self) -> int:
        """Calcola i giorni lavorativi (lun-sab) nel periodo."""
        giorni = 0
        data_corrente = self.data_inizio
        
        while data_corrente <= self.data_fine:
            # In Italia la scuola è aperta lunedì-sabato (0-5)
            if data_corrente.weekday() < 6:  # 0=lunedì, 6=domenica
                giorni += 1
            data_corrente += datetime.timedelta(days=1)
        
        return giorni

@dataclass 
class Festivita:
    """Rappresenta una festività."""
    nome: str
    data: datetime.date
    tipo: str  # "nazionale", "religiosa", "locale"
    scuola_chiusa: bool = True
    descrizione: str = ""

class CalendarioScolastico:
    """Gestisce il calendario scolastico italiano."""
    
    def __init__(self, anno_scolastico: int = None):
        """
        Inizializza il calendario scolastico.
        
        Args:
            anno_scolastico: Anno di inizio (es: 2024 per 2024-2025)
        """
        if anno_scolastico is None:
            # Determina automaticamente l'anno scolastico corrente
            oggi = datetime.date.today()
            if oggi.month >= 9:  # Da settembre in poi = nuovo anno scolastico
                anno_scolastico = oggi.year
            else:  # Gennaio-agosto = anno scolastico precedente
                anno_scolastico = oggi.year - 1
        
        self.anno_scolastico = anno_scolastico
        self.anno_fine = anno_scolastico + 1
        
        # Inizializza periodi e festività
        self.periodi: List[Periodo] = []
        self.festivita: List[Festivita] = []
        
        # Genera calendario
        self._genera_calendario()
    
    def _genera_calendario(self):
        """Genera il calendario scolastico completo."""
        self._genera_periodi_principali()
        self._genera_festivita()
        self._genera_vacanze()
    
    def _genera_periodi_principali(self):
        """Genera i periodi principali dell'anno scolastico."""
        
        # Inizio anno scolastico (metà settembre)
        inizio_scuola = datetime.date(self.anno_scolastico, 9, 15)
        
        # Fine primo quadrimestre (31 gennaio)
        fine_primo_quad = datetime.date(self.anno_fine, 1, 31)
        
        # Inizio secondo quadrimestre (1 febbraio)
        inizio_secondo_quad = datetime.date(self.anno_fine, 2, 1)
        
        # Fine anno scolastico (8 giugno)
        fine_scuola = datetime.date(self.anno_fine, 6, 8)
        
        # Primo quadrimestre
        self.periodi.append(Periodo(
            nome="Primo Quadrimestre",
            data_inizio=inizio_scuola,
            data_fine=fine_primo_quad,
            tipo=TipoPeriodo.LEZIONI,
            descrizione="Primo periodo didattico dell'anno scolastico"
        ))
        
        # Secondo quadrimestre 
        self.periodi.append(Periodo(
            nome="Secondo Quadrimestre", 
            data_inizio=inizio_secondo_quad,
            data_fine=fine_scuola,
            tipo=TipoPeriodo.LEZIONI,
            descrizione="Secondo periodo didattico dell'anno scolastico"
        ))
        
        # Vacanze estive
        inizio_vacanze_estive = fine_scuola + datetime.timedelta(days=1)
        fine_vacanze_estive = datetime.date(self.anno_fine, 8, 31)
        
        self.periodi.append(Periodo(
            nome="Vacanze Estive",
            data_inizio=inizio_vacanze_estive,
            data_fine=fine_vacanze_estive,
            tipo=TipoPeriodo.VACANZE,
            descrizione="Vacanze estive"
        ))
    
    def _genera_festivita(self):
        """Genera le festività nazionali italiane."""
        
        festivita_fisse = [
            # Anno scolastico corrente (settembre-dicembre)
            ("Ognissanti", datetime.date(self.anno_scolastico, 11, 1), "nazionale"),
            ("Immacolata", datetime.date(self.anno_scolastico, 12, 8), "religiosa"),
            ("Natale", datetime.date(self.anno_scolastico, 12, 25), "nazionale"),
            ("Santo Stefano", datetime.date(self.anno_scolastico, 12, 26), "nazionale"),
            
            # Anno successivo (gennaio-giugno)
            ("Capodanno", datetime.date(self.anno_fine, 1, 1), "nazionale"),
            ("Epifania", datetime.date(self.anno_fine, 1, 6), "religiosa"),
            ("Festa della Liberazione", datetime.date(self.anno_fine, 4, 25), "nazionale"),
            ("Festa del Lavoro", datetime.date(self.anno_fine, 5, 1), "nazionale"),
            ("Festa della Repubblica", datetime.date(self.anno_fine, 6, 2), "nazionale"),
        ]
        
        for nome, data, tipo in festivita_fisse:
            self.festivita.append(Festivita(
                nome=nome,
                data=data,
                tipo=tipo,
                scuola_chiusa=True
            ))
        
        # Festività mobili (Pasqua e correlate)
        pasqua = self._calcola_pasqua(self.anno_fine)
        
        pasqua_festivita = [
            ("Lunedì dell'Angelo", pasqua + datetime.timedelta(days=1)),
            ("Venerdì Santo", pasqua - datetime.timedelta(days=2)),  # In alcune regioni
        ]
        
        for nome, data in pasqua_festivita:
            self.festivita.append(Festivita(
                nome=nome,
                data=data,
                tipo="religiosa",
                scuola_chiusa=True
            ))
    
    def _genera_vacanze(self):
        """Genera i periodi di vacanza."""
        
        # Vacanze di Natale (23 dicembre - 6 gennaio)
        self.periodi.append(Periodo(
            nome="Vacanze di Natale",
            data_inizio=datetime.date(self.anno_scolastico, 12, 23),
            data_fine=datetime.date(self.anno_fine, 1, 6),
            tipo=TipoPeriodo.VACANZE,
            descrizione="Vacanze natalizie"
        ))
        
        # Vacanze di Pasqua (variabili)
        pasqua = self._calcola_pasqua(self.anno_fine)
        inizio_vacanze_pasquali = pasqua - datetime.timedelta(days=3)  # Giovedì prima
        fine_vacanze_pasquali = pasqua + datetime.timedelta(days=1)    # Lunedì dopo
        
        self.periodi.append(Periodo(
            nome="Vacanze di Pasqua",
            data_inizio=inizio_vacanze_pasquali,
            data_fine=fine_vacanze_pasquali,
            tipo=TipoPeriodo.VACANZE,
            descrizione="Vacanze pasquali"
        ))
        
        # Ponti comuni
        ponti = [
            # Ponte di Ognissanti (se cade bene)
            ("Ponte di Ognissanti", datetime.date(self.anno_scolastico, 11, 2), 
             datetime.date(self.anno_scolastico, 11, 2)),
            
            # Ponte dell'Immacolata  
            ("Ponte dell'Immacolata", datetime.date(self.anno_scolastico, 12, 9),
             datetime.date(self.anno_scolastico, 12, 9)),
        ]
        
        for nome, inizio, fine in ponti:
            self.periodi.append(Periodo(
                nome=nome,
                data_inizio=inizio,
                data_fine=fine,
                tipo=TipoPeriodo.VACANZE,
                descrizione="Ponte"
            ))
    
    def _calcola_pasqua(self, anno: int) -> datetime.date:
        """Calcola la data della Pasqua per un dato anno."""
        # Algoritmo di calcolo della Pasqua
        a = anno % 19
        b = anno // 100
        c = anno % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        n = (h + l - 7 * m + 114) // 31
        p = (h + l - 7 * m + 114) % 31
        
        return datetime.date(anno, n, p + 1)
    
    def giorni_scuola_totali(self) -> int:
        """Calcola il totale dei giorni di scuola nell'anno."""
        giorni = 0
        for periodo in self.periodi:
            if periodo.tipo == TipoPeriodo.LEZIONI:
                giorni += periodo.giorni_lavorativi()
        
        # Sottrai le festività che cadono in giorni di scuola
        for festivita in self.festivita:
            if festivita.scuola_chiusa and self._e_giorno_scuola(festivita.data):
                giorni -= 1
        
        return giorni
    
    def _e_giorno_scuola(self, data: datetime.date) -> bool:
        """Verifica se una data è un giorno di scuola."""
        # Verifica se cade in un periodo di lezioni
        for periodo in self.periodi:
            if periodo.tipo == TipoPeriodo.LEZIONI and periodo.contiene_data(data):
                # Verifica che non sia domenica (lunedì=0, domenica=6)
                return data.weekday() < 6
        return False
    
    def prossime_festivita(self, n: int = 5) -> List[Festivita]:
        """Restituisce le prossime n festività."""
        oggi = datetime.date.today()
        future = [f for f in self.festivita if f.data >= oggi]
        future.sort(key=lambda x: x.data)
        return future[:n]
    
    def festivita_mese(self, mese: int, anno: int = None) -> List[Festivita]:
        """Restituisce le festività di un mese specifico."""
        if anno is None:
            anno = self.anno_scolastico if mese >= 9 else self.anno_fine
        
        return [f for f in self.festivita 
                if f.data.month == mese and f.data.year == anno]
    
    def periodo_corrente(self) -> Optional[Periodo]:
        """Restituisce il periodo corrente."""
        oggi = datetime.date.today()
        for periodo in self.periodi:
            if periodo.contiene_data(oggi):
                return periodo
        return None
    
    def giorni_mancanti_fine_periodo(self) -> int:
        """Giorni mancanti alla fine del periodo corrente."""
        periodo = self.periodo_corrente()
        if periodo:
            oggi = datetime.date.today()
            delta = periodo.data_fine - oggi
            return max(0, delta.days)
        return 0
    
    def statistiche_anno(self) -> Dict:
        """Restituisce statistiche dell'anno scolastico."""
        giorni_scuola = self.giorni_scuola_totali()
        giorni_vacanza = sum(p.giorni_totali for p in self.periodi 
                           if p.tipo == TipoPeriodo.VACANZE)
        
        return {
            "anno_scolastico": f"{self.anno_scolastico}-{self.anno_fine}",
            "giorni_scuola": giorni_scuola,
            "giorni_vacanza": giorni_vacanza,
            "totale_festivita": len(self.festivita),
            "periodi_didattici": len([p for p in self.periodi 
                                    if p.tipo == TipoPeriodo.LEZIONI]),
            "inizio_scuola": min(p.data_inizio for p in self.periodi 
                               if p.tipo == TipoPeriodo.LEZIONI),
            "fine_scuola": max(p.data_fine for p in self.periodi 
                             if p.tipo == TipoPeriodo.LEZIONI)
        }
    
    def genera_calendario_mensile(self, mese: int, anno: int = None) -> Dict:
        """Genera il calendario di un mese con evidenziate vacanze e festività."""
        if anno is None:
            anno = self.anno_scolastico if mese >= 9 else self.anno_fine
        
        # Crea calendario mensile
        cal = calendar.monthcalendar(anno, mese)
        
        # Raccogli informazioni per ogni giorno
        giorni_info = {}
        
        for settimana in cal:
            for giorno in settimana:
                if giorno == 0:  # Giorno vuoto
                    continue
                
                data = datetime.date(anno, mese, giorno)
                info = {
                    "data": data,
                    "tipo": "normale",
                    "eventi": [],
                    "scuola_aperta": self._e_giorno_scuola(data)
                }
                
                # Verifica se è una festività
                for festivita in self.festivita:
                    if festivita.data == data:
                        info["tipo"] = "festivita"
                        info["eventi"].append(festivita.nome)
                
                # Verifica se è in un periodo di vacanza
                for periodo in self.periodi:
                    if (periodo.tipo == TipoPeriodo.VACANZE and 
                        periodo.contiene_data(data)):
                        info["tipo"] = "vacanza"
                        info["eventi"].append(periodo.nome)
                
                giorni_info[giorno] = info
        
        return {
            "mese": mese,
            "anno": anno,
            "nome_mese": calendar.month_name[mese],
            "calendario": cal,
            "giorni_info": giorni_info
        }
    
    def esporta_json(self) -> Dict:
        """Esporta il calendario in formato JSON."""
        return {
            "anno_scolastico": f"{self.anno_scolastico}-{self.anno_fine}",
            "statistiche": self.statistiche_anno(),
            "periodi": [
                {
                    "nome": p.nome,
                    "data_inizio": p.data_inizio.isoformat(),
                    "data_fine": p.data_fine.isoformat(),
                    "tipo": p.tipo.value,
                    "descrizione": p.descrizione,
                    "giorni_totali": p.giorni_totali,
                    "giorni_lavorativi": p.giorni_lavorativi()
                }
                for p in self.periodi
            ],
            "festivita": [
                {
                    "nome": f.nome,
                    "data": f.data.isoformat(),
                    "tipo": f.tipo,
                    "scuola_chiusa": f.scuola_chiusa,
                    "descrizione": f.descrizione
                }
                for f in self.festivita
            ]
        }


def test_calendario():
    """Test del calendario scolastico."""
    print("📅 TEST CALENDARIO SCOLASTICO ITALIANO")
    print("="*60)
    
    # Crea calendario per anno corrente
    calendario = CalendarioScolastico()
    
    # Statistiche generali
    stats = calendario.statistiche_anno()
    print(f"\n📊 STATISTICHE ANNO {stats['anno_scolastico']}")
    print(f"   Giorni di scuola: {stats['giorni_scuola']}")
    print(f"   Giorni di vacanza: {stats['giorni_vacanza']}")
    print(f"   Festività totali: {stats['totale_festivita']}")
    print(f"   Inizio: {stats['inizio_scuola']}")
    print(f"   Fine: {stats['fine_scuola']}")
    
    # Periodo corrente
    periodo = calendario.periodo_corrente()
    if periodo:
        print("\n📆 PERIODO CORRENTE")
        print(f"   {periodo.nome}")
        print(f"   Dal {periodo.data_inizio} al {periodo.data_fine}")
        print(f"   Giorni mancanti: {calendario.giorni_mancanti_fine_periodo()}")
    
    # Prossime festività
    print("\n🎉 PROSSIME FESTIVITÀ")
    for fest in calendario.prossime_festivita(3):
        print(f"   {fest.data}: {fest.nome} ({fest.tipo})")
    
    # Calendario di dicembre (esempio)
    print(f"\n📅 CALENDARIO DICEMBRE {calendario.anno_scolastico}")
    cal_dic = calendario.genera_calendario_mensile(12)
    
    print(f"   {cal_dic['nome_mese']} {cal_dic['anno']}")
    print("   L  M  M  G  V  S  D")
    
    for settimana in cal_dic['calendario']:
        riga = "   "
        for giorno in settimana:
            if giorno == 0:
                riga += "   "
            else:
                info = cal_dic['giorni_info'].get(giorno, {})
                if info.get('tipo') == 'festivita':
                    riga += f"{giorno:2}*"
                elif info.get('tipo') == 'vacanza':
                    riga += f"{giorno:2}~"
                else:
                    riga += f"{giorno:2} "
        print(riga)
    
    print("   * = Festività, ~ = Vacanze")
    
    return calendario


if __name__ == "__main__":
    test_calendario()
