"""
Esempio di utilizzo programmatico del Registro Scolastico
"""

from anagrafica import Anagrafica, Studente
from insegnanti import GestioneInsegnanti, Insegnante
from voti import GestioneVoti
from analisi import AnalisiDidattica


def esempio_basico():
    """Esempio base di utilizzo del sistema."""
    
    print("="*60)
    print("ESEMPIO 1: Creazione e gestione studenti")
    print("="*60)
    
    # Crea anagrafica
    anagrafica = Anagrafica()
    
    # Genera 5 studenti casuali
    anagrafica.genera_studenti(5)
    
    # Visualizza studenti
    print(f"\n✅ Creati {len(anagrafica.studenti)} studenti:")
    for studente in anagrafica.studenti:
        print(f"  • {studente.nome_completo} - Classe: {studente.classe} - Fragilità: {studente.fragilità_sociale}")
    
    # Statistiche
    stats = anagrafica.statistiche_generali()
    print(f"\n📊 Statistiche:")
    print(f"  Totale studenti: {stats['totale_studenti']}")
    print(f"  Reddito medio: €{stats['reddito_medio']:,}")
    
    print("\n" + "="*60)


def esempio_voti():
    """Esempio di gestione voti."""
    
    print("\n" + "="*60)
    print("ESEMPIO 2: Sistema voti e medie")
    print("="*60)
    
    # Crea anagrafica e voti
    anagrafica = Anagrafica()
    voti = GestioneVoti()
    
    # Genera uno studente
    studente = anagrafica.crea_studente_casuale()
    print(f"\n✅ Creato studente: {studente.nome_completo}")
    
    # Aggiungi voti
    materie = ["Matematica", "Italiano", "Inglese"]
    for materia in materie:
        voti.aggiungi_voto_casuale(studente.id, materia, base=6.5)
    
    print(f"\n📝 Aggiunti voti per {len(materie)} materie")
    
    # Calcola medie
    for materia in materie:
        media = voti.media_studente(studente.id, materia)
        print(f"  {materia}: {media:.2f}")
    
    media_generale = voti.media_studente(studente.id)
    print(f"\n📊 Media generale: {media_generale:.2f}")
    
    print("\n" + "="*60)


def esempio_analisi():
    """Esempio di analisi avanzate."""
    
    print("\n" + "="*60)
    print("ESEMPIO 3: Analisi didattica")
    print("="*60)
    
    # Setup sistema completo
    anagrafica = Anagrafica()
    insegnanti = GestioneInsegnanti()
    voti = GestioneVoti()
    analisi = AnalisiDidattica(anagrafica, voti)
    
    # Genera dati
    print("\n📚 Generando dati...")
    anagrafica.genera_studenti(10)
    insegnanti.genera_insegnanti(3)
    
    # Assegna voti
    materie = ["Matematica", "Italiano"]
    for studente in anagrafica.studenti:
        for materia in materie:
            voti.aggiungi_voto_casuale(studente.id, materia)
    
    # Analisi
    print("\n📊 Analisi:")
    
    # Graduatoria
    graduatoria = analisi.graduatoria_studenti()[:5]
    print("\n🏆 Top 5 studenti:")
    for i, s in enumerate(graduatoria, 1):
        print(f"  {i}. {s['nome']} - Media: {s['media']:.2f}")
    
    # Fragilità
    fragili = analisi.impatto_didattico_fragili()
    print(f"\n🎯 Analisi fragilità:")
    print(f"  Gap pedagogico: {fragili['gap_pedagogico']:.2f}")
    print(f"  Equità: {fragili['equita_educativa']}")
    
    # Classe migliore
    classe_migliore = analisi.classe_piu_brillante()
    print(f"\n🌟 Classe migliore: {classe_migliore['classe']} (Media: {classe_migliore['media']:.2f})")
    
    print("\n" + "="*60)


def esempio_completo():
    """Simulazione completa del sistema."""
    
    print("\n" + "="*60)
    print("ESEMPIO 4: Simulazione completa")
    print("="*60)
    
    # Inizializza componenti
    anagrafica = Anagrafica()
    insegnanti = GestioneInsegnanti()
    voti = GestioneVoti()
    analisi = AnalisiDidattica(anagrafica, voti)
    
    # Genera dati realistici
    print("\n🎲 Generando simulazione...")
    
    # Studenti
    anagrafica.genera_studenti(20)
    print(f"  ✅ {len(anagrafica.studenti)} studenti creati")
    
    # Insegnanti
    insegnanti.genera_insegnanti(5)
    print(f"  ✅ {len(insegnanti.insegnanti)} insegnanti creati")
    
    # Voti
    materie = ["Matematica", "Italiano", "Inglese", "Storia", "Scienze"]
    totale_voti = 0
    for studente in anagrafica.studenti:
        for materia in materie:
            import random
            for _ in range(random.randint(2, 4)):
                voti.aggiungi_voto_casuale(studente.id, materia)
                totale_voti += 1
    
    print(f"  ✅ {totale_voti} voti assegnati")
    
    # Statistiche complete
    print("\n" + "="*60)
    print("📊 RISULTATI SIMULAZIONE")
    print("="*60)
    
    # Anagrafica
    stats = anagrafica.statistiche_generali()
    print(f"\n👥 Studenti: {stats['totale_studenti']}")
    print(f"💶 Reddito medio: €{stats['reddito_medio']:,}")
    frag = stats['statistica_fragilita']
    print(f"🎯 Fragilità media: {frag['media']:.1f}")
    
    # Voti
    stats_voti = voti.statistiche_generali()
    print(f"\n📝 Voti totali: {stats_voti['totale_voti']}")
    print(f"📊 Media voti: {stats_voti['voto_medio']:.2f}")
    
    # Analisi
    graduatoria = analisi.graduatoria_studenti()[:3]
    print(f"\n🏆 Top 3 studenti:")
    for s in graduatoria:
        print(f"   {s['posizione']}. {s['nome']} - {s['media']:.2f}")
    
    impatto = analisi.impatto_didattico_fragili()
    print(f"\n🎯 Equità educativa: {impatto['equita_educativa']}")
    
    print("\n" + "="*60)
    print("✅ Simulazione completata!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Esegui tutti gli esempi
    esempio_basico()
    esempio_voti()
    esempio_analisi()
    esempio_completo()
    
    print("\n💡 Per usare l'interfaccia interattiva, esegui: python main.py")
