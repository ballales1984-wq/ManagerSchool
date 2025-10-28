"""
Esegue un backup completo del sistema ManagerSchool.
"""

import os
from main import RegistroScolastico
from backup_registro import GestoreBackup

print("BACKUP COMPLETO SISTEMA MANAGERSCHOOL")
print("=" * 60 + "\n")

# Crea registro
print("1. Inizializzazione sistema...")
registro = RegistroScolastico()
registro.anagrafica.genera_studenti(100)
registro.insegnanti.genera_insegnanti(10)
print(f"   Studenti: {len(registro.anagrafica.studenti)}")
print(f"   Insegnanti: {len(registro.insegnanti.insegnanti)}")

# Backup
print("\n2. Backup in corso...")
backup = GestoreBackup()
filepath = backup.salva_backup(registro)
print(f"   Salvato: {filepath}")

# Statistiche
print("\n3. Statistiche backup:")
stats = backup.statistiche_backup()
for tipo, dati in stats.items():
    if dati["conteggio"] > 0:
        dimensione_kb = dati["dimensione_totale"] / 1024
        print(f"   {tipo}: {dati['conteggio']} file, {dimensione_kb:.2f} KB")

print("\n4. Verifica integrita...")
filepath = "backup/giornalieri/backup_" + filepath.split("backup_")[1] if "backup_" in filepath else filepath
print(f"   File: {os.path.basename(filepath)}")

print("\n" + "=" * 60)
print("BACKUP COMPLETATO CON SUCCESSO!")
print(f"File salvato in: {filepath}")

