import pandas as pd
import pickle
import os

cwd=""
# Pfad zur Excel-Datei
cwd = os.getcwd()

df = pd.read_excel(cwd+"\\NAS-NYSE-bereinigt.xlsx")
symbols_list = df.iloc[0:, 0].dropna().tolist()

# Als normale Liste speichern
pickle.dump(symbols_list, open(cwd+"\\symbols_list2.pkl", 'wb'))
print("Erledigt.")

with open(cwd+"\\symbols_list2.pkl", 'rb') as f:
    
    meine_posts = pickle.load(f)   
    
print(meine_posts)