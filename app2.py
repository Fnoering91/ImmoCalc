
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Immobilien-Rechner", layout="centered")
st.title("Immobilien-Investment Rechner")

with st.expander("**Spaltenbeschreibung anzeigen**"):
    st.markdown("""
    - **Restschuld**: Verbleibender Kreditbetrag am Jahresende  
    - **Zinskosten**: Im Jahr gezahlte Kreditzinsen  
    - **Tilgung**: Im Jahr getilgter Kreditbetrag  
    - **Mieteinnahmen**: Jahresmiete (Wohnfläche × Miete × 12)  
    - **AfA**: Abschreibung, 2 % auf 80 % des Kaufpreises  
    - **Nebenkosten**: Nicht umlagefähige Kosten (jährlich)  
    - **Steuerlicher Verlust**: Einnahmen – (Zinsen + AfA + Nebenkosten)  
    - **Steuerersparnis**: (Zinsen + AfA + Nebenkosten) × Steuersatz  
    - **Steuerlicher Vorteil (real)**: Steuerlicher Verlust × Steuersatz  
    - **Reale Monatskosten**: ((Zinsen + Tilgung – Mieteinnahmen + Nebenkosten – Steuerersparnis) / 12)
    """)

with st.form("eingabe_formular"):
    st.subheader("Berechnungsgrundlagen")

    col1, col2 = st.columns(2)

    with col1:
        kaufpreis = st.number_input("Kaufpreis (€)", min_value=10000, value=500000, step=10000)
        eigenkapital = st.number_input("Eigenkapital (€)", min_value=0, value=50000, step=10000)
        zinssatz = st.number_input("Zinssatz (p.a.)", min_value=0.1, max_value=10.0, value=4.0, step=0.1)
        laufzeit_jahre = st.number_input("Laufzeit (Jahre)", min_value=5, max_value=40, value=20)

    with col2:
        wohnfläche = st.number_input("Wohnfläche (m²)", min_value=10, value=120)
        miete_pro_m2 = st.number_input("Miete pro m² (€)", min_value=1.0, value=11.0, step=0.5)
        nebenkosten = st.number_input("Nicht umlagefähige Nebenkosten (€/Monat)", min_value=0, value=250)
        steuersatz = st.number_input("Persönlicher Steuersatz (%)", min_value=0.0, max_value=50.0, value=42.0)

    berechnen = st.form_submit_button("Neu berechnen")

if berechnen:
    zins = zinssatz / 100
    steuersatz = steuersatz / 100
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
        steuervorteil_real = steuerlich_absetzbar * steuersatz
        reale_monatskosten = (zinskosten + tilgung + betriebskosten - mieteinnahmen + steuervorteil_real) / 12
        daten.append([
            jahr, round(saldo, 2), round(zinskosten, 2), round(tilgung, 2),
            round(mieteinnahmen, 2), round(abschreibung, 2), round(betriebskosten, 2),
            
            round(steuervorteil_real, 2), round(reale_monatskosten, 2)
        ])

    df = pd.DataFrame(daten, columns=[
        "Jahr", "Restschuld", "Zinskosten", "Tilgung",
        "Mieteinnahmen", "AfA", "Nebenkosten",
        
        "Steuerlicher Vorteil (real)", "Reale Monatskosten"
    ])
 
    gesamt = pd.DataFrame({
    "Gesamtausgaben (inkl. Tilgung)": [df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum()],
    "Davon Zinsen": [df["Zinskosten"].sum()],
    "Davon Nebenkosten": [df["Nebenkosten"].sum()],
    "Davon Tilgung": [df["Tilgung"].sum()],
    "Gesamte Mieteinnahmen": [df["Mieteinnahmen"].sum()],
    "Steuervorteil (real)": [df["Steuerlicher Vorteil (real)"].sum()],
    "Monatliche Belastung (nach Steuern)": [((df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum() - df["Mieteinnahmen"].sum() - df["Steuerlicher Vorteil (real)"].sum()) / (len(df)*12))]
    })

    st.subheader("Berechnungsergebnisse")
    st.dataframe(df.style.format("{:,.2f}"), use_container_width=True)

    with st.expander("**Zusammenfassung & Berechnungsgrundlagen**"):
        st.dataframe(gesamt.style.format("{:,.2f}"), use_container_width=True)
        st.markdown("""
        **Berechnungsvorschriften:**
        - Monatliche Kreditrate: konstante Rate eines Annuitätendarlehens
        - Gesamtaufwand: Zinskosten + nicht umlagefähige Nebenkosten
        - Kapitalfluss (netto): Mieteinnahmen – Gesamtaufwand
        - Steuerlicher Vorteil (real): steuerlicher Verlust × Steuersatz
        - Reale Monatskosten: ((Zinsen + Tilgung – Mieteinnahmen + Nebenkosten – Steuerersparnis) / 12)
        - AfA: 2 % auf 80 % des Kaufpreises (jährlich konstant)
        """)

    st.subheader("Download als Excel-Datei")
    def convert_df_to_excel(data: pd.DataFrame):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            data.to_excel(writer, sheet_name="Jahrestabelle", index=False)
            gesamt.to_excel(writer, sheet_name="Summen", index=False)
        return output.getvalue()

    excel_data = convert_df_to_excel(df)
    st.download_button("Excel-Datei herunterladen", data=excel_data, file_name="Immobilienmodell.xlsx")
