
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Immobilien-Rechner", layout="wide")
st.title("Immobilien-Investment Rechner")

st.sidebar.header("Eingabedaten")

# Eingaben vom Nutzer
kaufpreis = st.sidebar.number_input("Kaufpreis (€)", min_value=10000, value=500000, step=10000)
eigenkapital = st.sidebar.number_input("Eigenkapital (€)", min_value=0, value=50000, step=10000)
zins = st.sidebar.number_input("Zinssatz (p.a.)", min_value=0.1, max_value=10.0, value=4.0, step=0.1) / 100
laufzeit_jahre = st.sidebar.number_input("Laufzeit (Jahre)", min_value=5, max_value=40, value=20)
wohnfläche = st.sidebar.number_input("Wohnfläche (m²)", min_value=10, value=120)
miete_pro_m2 = st.sidebar.number_input("Miete pro m² (€)", min_value=1.0, value=11.0, step=0.5)
nebenkosten = st.sidebar.number_input("Nebenkosten nicht umlagefähig (€/Monat)", min_value=0, value=250)
steuersatz = st.sidebar.number_input("Persönlicher Steuersatz (%)", min_value=0.0, max_value=50.0, value=42.0) / 100

# Abgeleitete Werte
darlehen = kaufpreis - eigenkapital
zins_monat = zins / 12
monate = laufzeit_jahre * 12
try:
    rate = darlehen * (zins_monat / (1 - (1 + zins_monat) ** -monate))
except ZeroDivisionError:
    st.error("Zinssatz darf nicht 0 sein!")
    st.stop()

afa_basis = kaufpreis * 0.8
abschreibung = afa_basis * 0.02
miete_pro_monat = wohnfläche * miete_pro_m2

# Simulation
saldo = darlehen
daten = []

for jahr in range(1, laufzeit_jahre + 1):
    zinskosten = 0
    tilgung = 0
    for monat in range(12):
        zinsanteil = saldo * zins_monat
        tilgungsanteil = rate - zinsanteil
        saldo -= tilgungsanteil
        zinskosten += zinsanteil
        tilgung += tilgungsanteil
    mieteinnahmen = miete_pro_monat * 12
    betriebskosten = nebenkosten * 12
    gesamtaufwand = zinskosten + abschreibung + betriebskosten
    steuerlich_absetzbar = mieteinnahmen - gesamtaufwand
    steuerersparnis = gesamtaufwand * steuersatz
    daten.append([
        jahr, round(saldo, 2), round(zinskosten, 2), round(tilgung, 2),
        round(mieteinnahmen, 2), round(abschreibung, 2), round(betriebskosten, 2),
        round(steuerlich_absetzbar, 2), round(steuerersparnis, 2)
    ])

df = pd.DataFrame(daten, columns=[
    "Jahr", "Restschuld", "Zinskosten", "Tilgung",
    "Mieteinnahmen", "AfA", "Nebenkosten",
    "Steuerlicher Verlust", "Steuerersparnis"
])

# Gesamtsummen
gesamt = df[["Zinskosten", "Tilgung", "Mieteinnahmen", "Nebenkosten", "Steuerersparnis"]].sum().to_frame().T
gesamt["Gesamtaufwand"] = gesamt["Zinskosten"] + gesamt["Nebenkosten"]
gesamt["Kapitalfluss (netto)"] = gesamt["Mieteinnahmen"] - gesamt["Gesamtaufwand"]

st.subheader("Berechnungsergebnisse pro Jahr")
st.dataframe(df.style.format("{:,.2f}"))

st.subheader("Summen über die Laufzeit")
st.dataframe(gesamt.style.format("{:,.2f}"))

# Download als Excel
st.subheader("Daten exportieren")
def convert_df_to_excel(data: pd.DataFrame):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        data.to_excel(writer, sheet_name="Jahrestabelle", index=False)
        gesamt.to_excel(writer, sheet_name="Summen", index=False)
    return output.getvalue()

excel_data = convert_df_to_excel(df)
st.download_button("Excel-Datei herunterladen", data=excel_data, file_name="Immobilienmodell.xlsx")
