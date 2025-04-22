import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open("Immobilien").sheet1  # oder .worksheet("Tabelle1")

def lade_immobilien():
    rows = sheet.get_all_values()
    return {row[0]: json.loads(row[1]) for row in rows if row[0] and row[1]}

def speichere_immobilie(name, daten):
    immobilien = lade_immobilien()
    immobilien[name] = daten
    # Alles neu schreiben
    sheet.clear()
    for key, val in immobilien.items():
        sheet.append_row([key, json.dumps(val, ensure_ascii=False)])

def loesche_immobilie(name):
    immobilien = lade_immobilien()
    if name in immobilien:
        del immobilien[name]
        sheet.clear()
        for key, val in immobilien.items():
            sheet.append_row([key, json.dumps(val, ensure_ascii=False)])

def liste_immobilien():
    return list(lade_immobilien().keys())

def lade_immobilie(name):
    return lade_immobilien().get(name)
