"""
Script per generare pagelle complete con tutte le materie richieste
"""

import random
from anagrafica import Anagrafica
from voti import GestioneVoti, Voto, Pagella
from main import RegistroScolastico
import datetime

# Materie complete come richiesto
MATERIE_COMPLETE = [
    "Matematica",
    "Italiano", 
    "Inglese",
    "Storia",
    "Educazione Fisica",
    "Religione"
]

# Voto di condotta gestito separatamente

def genera_voti_materia(id_studente: int, materia: str, voti_sistema: GestioneVoti, 
                       fragilita_sociale: float) -> None:
    """Genera voti realistici per una materia specifica."""
    
    # Numero voti per materia (2-6 voti)
    num_voti = random.randint(2, 6)
    
    # Base voto influenzata da fragilità sociale
    base_voto = 6.8 - (fragilita_sociale / 100)
    
    # Parametri specifici per materia
    parametri_materie = {
        "Matematica": {"difficolta": 0.3, "varianza": 1.2},
        "Italiano": {"difficolta": 0.1, "varianza": 0.8},
        "Inglese": {"difficolta": 0.2, "varianza": 1.0},
        "Storia": {"difficolta": 0.1, "varianza": 0.9},
        "Educazione Fisica": {"difficolta": -0.4, "varianza": 0.6},  # Generalmente voti più alti
        "Religione": {"difficolta": -0.3, "varianza": 0.5}  # Voti tendenzialmente buoni
    }
    
    params = parametri_materie.get(materia, {"difficolta": 0.0, "varianza": 1.0})
    
    for i in range(num_voti):
        # Calcola voto con variabilità
        voto_base = base_voto - params["difficolta"]
        variazione = random.uniform(-params["varianza"], params["varianza"])
        voto_finale = max(3.0, min(10.0, voto_base + variazione))
        
        # Tipo di voto (mix realistico)
        tipi_voto = ["Prova scritta", "Prova orale", "Verifica", "Interrogazione", "Compito in classe"]
        if materia == "Educazione Fisica":
            tipi_voto = ["Prova pratica", "Test motorio", "Verifica pratica"]
        elif materia == "Religione":
            tipi_voto = ["Prova orale", "Elaborato", "Partecipazione"]
            
        tipo = random.choice(tipi_voto)
        
        # Data casuale negli ultimi 3 mesi
        giorni_fa = random.randint(1, 90)
        data = datetime.datetime.now() - datetime.timedelta(days=giorni_fa)
        data_str = data.strftime("%Y-%m-%d")
        
        # Crea voto
        voto = Voto(
            id_studente=id_studente,
            materia=materia,
            voto=round(voto_finale, 1),
            tipo=tipo,
            data=data_str,
            note=f"Voto {materia.lower()}"
        )
        
        voti_sistema.voti.append(voto)

def genera_voto_condotta(fragilita_sociale: float) -> float:
    """Genera un voto di condotta realistico."""
    
    # Base condotta: inversamente proporzionale alla fragilità
    base_condotta = 9.2 - (fragilita_sociale / 50)  # Scala ridotta per condotta
    
    # Variazione casuale limitata
    variazione = random.uniform(-0.5, 0.3)
    condotta = base_condotta + variazione
    
    # Vincoli realistici per condotta (raramente sotto 6 o sopra 10)
    condotta = max(6.0, min(10.0, condotta))
    
    return round(condotta, 1)

def genera_pagelle_complete():
    """Genera pagelle complete per tutti gli studenti."""
    
    print("="*70)
    print("🎓 GENERAZIONE PAGELLE COMPLETE")
    print("="*70)
    
    # Inizializza sistema
    registro = RegistroScolastico()
    
    # Assicurati che ci siano studenti
    if len(registro.anagrafica.studenti) == 0:
        print("⚠️  Nessuno studente trovato. Generando 20 studenti...")
        registro.anagrafica.genera_studenti(20)
    
    print(f"\n📚 Studenti nel sistema: {len(registro.anagrafica.studenti)}")
    print(f"📝 Materie per pagella: {', '.join(MATERIE_COMPLETE)}")
    
    # Pulisci voti esistenti per rigenerare completi
    print("\n🧹 Pulizia voti esistenti...")
    registro.voti.voti.clear()
    registro.voti.pagelle.clear()
    
    # Genera voti completi per ogni studente
    print("\n📝 Generazione voti per materie...")
    voti_totali = 0
    
    for studente in registro.anagrafica.studenti:
        print(f"   • {studente.nome_completo} (Fragilità: {studente.fragilità_sociale:.1f})")
        
        # Genera voti per ogni materia
        for materia in MATERIE_COMPLETE:
            genera_voti_materia(studente.id, materia, registro.voti, studente.fragilità_sociale)
        
        # Conta voti generati per questo studente
        voti_studente = len([v for v in registro.voti.voti if v.id_studente == studente.id])
        voti_totali += voti_studente
    
    print(f"\n✅ Generati {voti_totali} voti totali")
    
    # Crea pagelle per tutti gli studenti
    print("\n📋 Creazione pagelle...")
    
    pagelle_create = 0
    for studente in registro.anagrafica.studenti:
        
        # Genera voto di condotta
        voto_condotta = genera_voto_condotta(studente.fragilità_sociale)
        
        # Genera numero assenze realistico (correlato alla fragilità)
        assenze_base = int(studente.fragilità_sociale / 10)  # Più fragili = più assenze  
        assenze = random.randint(max(0, assenze_base - 3), assenze_base + 8)
        
        # Note personalizzate
        note_possibili = [
            "Studente diligente e partecipativo",
            "Buon impegno e risultati positivi", 
            "Necessita di maggiore impegno in alcune materie",
            "Eccellente rendimento generale",
            "Partecipazione attiva alle lezioni",
            "Richiede supporto in alcune discipline",
            "Ottimo comportamento e rendimento costante"
        ]
        
        # Seleziona nota basata sul rendimento
        media_studente = registro.voti.media_studente(studente.id)
        if media_studente >= 8.0:
            note = random.choice(note_possibili[:4])
        elif media_studente >= 6.5:
            note = random.choice(note_possibili[1:6])
        else:
            note = random.choice(note_possibili[2:7])
        
        # Crea pagella 1° quadrimestre
        pagella = registro.voti.crea_pagella(
            id_studente=studente.id,
            quadrimestre=1,
            assenze=assenze,
            comportamento=voto_condotta,
            note=note
        )
        
        pagelle_create += 1
        
        # Mostra dettaglio pagella
        print(f"   📋 {studente.nome_completo}:")
        print(f"      Media generale: {pagella.media_generale:.2f}")
        print(f"      Condotta: {pagella.comportamento}")
        print(f"      Assenze: {pagella.assenze}")
        
        # Mostra voti per materia
        for materia, voto in pagella.voti_materie.items():
            print(f"      {materia}: {voto:.1f}")
    
    print(f"\n✅ Create {pagelle_create} pagelle complete!")
    
    # Statistiche finali
    print("\n" + "="*70)
    print("📊 STATISTICHE PAGELLE")
    print("="*70)
    
    # Media generale classe
    medie_studenti = [p.media_generale for p in registro.voti.pagelle]
    media_classe = sum(medie_studenti) / len(medie_studenti)
    print(f"📈 Media generale classe: {media_classe:.2f}")
    
    # Distribuzione voti condotta
    voti_condotta = [p.comportamento for p in registro.voti.pagelle]
    media_condotta = sum(voti_condotta) / len(voti_condotta)
    print(f"👫 Media voti condotta: {media_condotta:.2f}")
    
    # Statistiche per materia
    print(f"\n📚 Medie per materia:")
    for materia in MATERIE_COMPLETE:
        voti_materia = []
        for pagella in registro.voti.pagelle:
            if materia in pagella.voti_materie:
                voti_materia.append(pagella.voti_materie[materia])
        
        if voti_materia:
            media_materia = sum(voti_materia) / len(voti_materia)
            print(f"   {materia}: {media_materia:.2f}")
    
    # Top 5 studenti
    print(f"\n🏆 TOP 5 STUDENTI:")
    pagelle_ordinate = sorted(registro.voti.pagelle, key=lambda p: p.media_generale, reverse=True)
    
    for i, pagella in enumerate(pagelle_ordinate[:5], 1):
        studente = next(s for s in registro.anagrafica.studenti if s.id == pagella.id_studente)
        print(f"   {i}. {studente.nome_completo}: {pagella.media_generale:.2f} (Condotta: {pagella.comportamento})")
    
    print(f"\n🎉 PAGELLE COMPLETE GENERATE!")
    print(f"   • {len(registro.anagrafica.studenti)} studenti")
    print(f"   • {len(MATERIE_COMPLETE)} materie per studente")
    print(f"   • {len(registro.voti.voti)} voti totali")
    print(f"   • {len(registro.voti.pagelle)} pagelle create")
    
    return registro

def salva_pagelle_json(registro):
    """Salva le pagelle in formato JSON."""
    import json
    
    pagelle_json = []
    
    for pagella in registro.voti.pagelle:
        studente = next(s for s in registro.anagrafica.studenti if s.id == pagella.id_studente)
        
        pagella_dict = {
            "studente": {
                "id": studente.id,
                "nome": studente.nome_completo,
                "classe": studente.classe,
                "eta": studente.eta
            },
            "quadrimestre": pagella.quadrimestre,
            "voti_materie": pagella.voti_materie,
            "media_generale": round(pagella.media_generale, 2),
            "voto_condotta": pagella.comportamento,
            "assenze": pagella.assenze,
            "note": pagella.note
        }
        
        pagelle_json.append(pagella_dict)
    
    # Salva in file
    with open('pagelle_complete.json', 'w', encoding='utf-8') as f:
        json.dump(pagelle_json, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Pagelle salvate in: pagelle_complete.json")

if __name__ == "__main__":
    # Genera pagelle complete
    registro = genera_pagelle_complete()
    
    # Salva in JSON
    salva_pagelle_json(registro)
    
    print(f"\n🎓 Sistema completo di pagelle generato!")
    print(f"   Puoi vedere le pagelle nell'interfaccia web su http://127.0.0.1:5000")
