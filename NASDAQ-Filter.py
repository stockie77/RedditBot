import pandas as pd

# Pfad zur Excel-Datei
file_path = r'C:\Users\IHR-PFAD\Nasdaq1.xlsx'

# Excel-Datei laden
df = pd.read_excel(file_path)

# Duplikate basierend auf der zweiten Spalte (Unternehmen) identifizieren
# Nur die erste Zeile jedes Unternehmens behalten
unique_df = df.drop_duplicates(subset=df.columns[1], keep='first')

# Die restlichen Duplikate in ein separates DataFrame verschieben
duplicates_df = df[df.duplicated(subset=df.columns[1], keep='first')]

# Neue Excel-Datei mit zwei Blättern erstellen
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    unique_df.to_excel(writer, sheet_name='Tabelle1', index=False)
    duplicates_df.to_excel(writer, sheet_name='Tabelle2', index=False)

print(f"Verarbeitung abgeschlossen!")
print(f"Eindeutige Unternehmen: {len(unique_df)} Zeilen")
print(f"Duplikate verschoben: {len(duplicates_df)} Zeilen")
