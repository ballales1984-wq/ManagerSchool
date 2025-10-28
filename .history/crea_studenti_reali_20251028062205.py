"""
Script per inserire studenti reali nel sistema managerschool
"""

from anagrafica import Anagrafica, Studente
from insegnanti import GestioneInsegnanti, Insegnante
from voti import GestioneVoti
from dati import CategoriaReddito, CondizioneSalute, SituazioneFamiliare

def crea_studenti_reali():
    """Crea studenti con dati reali specificati."""
    
    # Inizializza sistema
    anagrafica = Anagrafica()
    voti = GestioneVoti()
    
    # ===== STUDENTI REALI =====
    
    # Studente 1: Mario Rossi
    mario = Studente(
        id=0,  # Assegnato automaticamente
        nome="Mario",
        cognome="Rossi", 
        eta=16,
        classe="3A",
        reddito_familiare=35000,
        categoria_reddito=CategoriaReddito.MEDIO,
        condizione_salute=CondizioneSalute.BUONA,
        situazione_familiare=SituazioneFamiliare.STABILE
    )
    anagrafica.aggiungi_studente(mario)
    
    # Studente 2: Giulia Bianchi
    giulia = Studente(
        id=0,
        nome="Giulia",
        cognome="Bianchi",
        eta=17,
        classe="3A", 
        reddito_familiare=28000,
        categoria_reddito=CategoriaReddito.MEDIO_BASSO,
        condizione_salute=CondizioneSalute.BUONA,
        situazione_familiare=SituazioneFamiliare.STABILE
    )
    anagrafica.aggiungi_studente(giulia)
    
    # Studente 3: Francesco Verde (situazione difficile)
    francesco = Studente(
        id=0,
        nome="Francesco", 
        cognome="Verde",
        eta=15,
        classe="2B",
        reddito_familiare=18000,
        categoria_reddito=CategoriaReddito.BASSO,
        condizione_salute=CondizioneSalute.PROBLEMATICA,
        situazione_familiare=SituazioneFamiliare.DIFFICILE
    )
    anagrafica.aggiungi_studente(francesco)
    
    # ===== VOTI REALI =====
    
    # Voti Mario Rossi (bravo studente)
    materie_mario = {
        "Matematica": [8.0, 7.5, 8.5],
        "Italiano": [7.0, 7.5, 7.0], 
        "Inglese": [9.0, 8.5, 9.0],
        "Storia": [7.5, 8.0, 7.0],
        "Scienze": [8.0, 8.5, 8.0]
    }
    
    for materia, voti_list in materie_mario.items():
        for voto in voti_list:
            voti.aggiungi_voto(mario.id, materia, voto, "scritto")
    
    # Voti Giulia Bianchi (studentessa media)
    materie_giulia = {
        "Matematica": [6.5, 7.0, 6.0],
        "Italiano": [8.0, 7.5, 8.5],
        "Inglese": [7.0, 6.5, 7.5],
        "Storia": [7.5, 8.0, 7.0],
        "Scienze": [6.0, 6.5, 6.0]
    }
    
    for materia, voti_list in materie_giulia.items():
        for voto in voti_list:
            voti.aggiungi_voto(giulia.id, materia, voto, "scritto")
    
    # Voti Francesco Verde (studente in difficoltà)
    materie_francesco = {
        "Matematica": [5.0, 5.5, 4.5],
        "Italiano": [6.0, 5.5, 6.0],
        "Inglese": [4.5, 5.0, 5.0],
        "Storia": [5.5, 6.0, 5.0],
        "Scienze": [5.0, 4.5, 5.5]
    }
    
    for materia, voti_list in materie_francesco.items():
        for voto in voti_list:
            voti.aggiungi_voto(francesco.id, materia, voto, "scritto")
    
    # ===== RISULTATI =====
    print("="*60)
    print("✅ STUDENTI REALI CREATI")
    print("="*60)
    
    for studente in anagrafica.studenti:
        media = voti.media_studente(studente.id)
        print(f"\n👤 {studente.nome_completo}")
        print(f"   Classe: {studente.classe}")
        print(f"   Età: {studente.eta} anni")
        print(f"   Reddito: €{studente.reddito_familiare:,}")
        print(f"   Fragilità: {studente.fragilità_sociale:.1f}/100")
        print(f"   Media voti: {media:.2f}")
    
    return anagrafica, voti

def crea_insegnanti_reali():
    """Crea insegnanti con dati reali."""
    
    insegnanti = GestioneInsegnanti()
    
    # Prof.ssa Maria Conti - Matematica
    maria = Insegnante(
        id=0,
        nome="Maria",
        cognome="Conti",
        eta=45,
        materie=["Matematica", "Fisica"],
        ore_settimanali={"Matematica": 4, "Fisica": 3},
        anni_esperienza=20,
        note="Specializzata in recupero studenti in difficoltà"
    )
    insegnanti.aggiungi_insegnante(maria)
    
    # Prof. Giovanni Neri - Lettere
    giovanni = Insegnante(
        id=0,
        nome="Giovanni", 
        cognome="Neri",
        eta=52,
        materie=["Italiano", "Storia"],
        ore_settimanali={"Italiano": 4, "Storia": 3},
        anni_esperienza=25,
        note="Coordinatore didattico"
    )
    insegnanti.aggiungi_insegnante(giovanni)
    
    print("\n" + "="*60)
    print("✅ INSEGNANTI REALI CREATI")
    print("="*60)
    
    for ins in insegnanti.insegnanti:
        print(f"\n👨‍🏫 {ins.nome_completo}")
        print(f"   Materie: {', '.join(ins.materie)}")
        print(f"   Ore totali: {ins.totale_ore_settimanali}")
        print(f"   Esperienza: {ins.anni_esperienza} anni")
        print(f"   Note: {ins.note}")
    
    return insegnanti

if __name__ == "__main__":
    print("🏫 INSERIMENTO DATI REALI MANAGERSCHOOL")
    print("="*60)
    
    # Crea studenti reali
    anagrafica, voti = crea_studenti_reali()
    
    # Crea insegnanti reali
    insegnanti = crea_insegnanti_reali()
    
    print(f"\n🎉 COMPLETATO!")
    print(f"   • {len(anagrafica.studenti)} studenti inseriti")
    print(f"   • {len(insegnanti.insegnanti)} insegnanti inseriti")
    print(f"   • {len(voti.voti)} voti inseriti")
