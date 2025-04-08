
import streamlit as st

def eingabeformular():
    with st.form("eingabe_formular"):
        st.subheader("Berechnungsgrundlagen")

        col1, col2 = st.columns(2)

        with col1:
            kaufpreis = st.number_input("Kaufpreis (€)", min_value=10000, value=316000, step=10000, help="= Kaufpreis OHNE Kaufnebenkosten")
            eigenkapital = st.number_input("Eigenkapital (€)", min_value=0, value=30000, step=10000, help="= Eigenkapital, welches den notwendigen Kreditrahmen reduziert")
            zinssatz = st.number_input("Zinssatz (p.a.)", min_value=0.1, max_value=10.0, value=3.8, step=0.1, help="= Zinssatz für Kredit")
            laufzeit_jahre = st.number_input("Laufzeit (Jahre)", min_value=5, max_value=40, value=25, help="= Laufzeit des Kredits")
            nebenkosten_kauf = st.number_input("Kaufnebenkosten (%)", min_value=0.0, max_value=20.0, value=7.0, help="= Grunderwerbsteuer, Makler, Notar etc.")
            region = st.text_input("Region der Immobilie", value="Hamburg", help="= Stadt oder Ballungsraum. Wird nur für die Expertenmeinung verwendet.")
            stadtteil = st.text_input("Stadtteil der Immobilie", value = "Bergedorf", help="Wird nur für die Expertenmeinung verwendet.")
            experteneinschaetzung_aktiv = st.checkbox("GPT-Experteneinschätzung aktivieren", value=False)
        
        with col2:
            wohnfläche = st.number_input("Wohnfläche (m²)", min_value=10, value=56, help="= zur Berechnung von Mieteinnahmen")
            kaltmiete = st.number_input("Kaltmiete (€/m²)", min_value=1.0, value=16.0, step=0.1, help="= durchschnittlicher Mietpreis")
            mieterhoehung = st.slider("Jährliche Mieterhöhung (%)", 0.0, 5.0, value=1, step=0.1)
            steuersatz = st.slider("Persönlicher Steuersatz (%)", 0, 50, value=42)
            nicht_umlagefaehige_kosten = st.number_input("Nicht umlagefähige Nebenkosten (€/m² p.a.)", min_value=0.0, value=25.0, step=1.0)

        submitted = st.form_submit_button("Finanzierung berechnen")

    return submitted, {
        "kaufpreis": kaufpreis,
        "eigenkapital": eigenkapital,
        "zinssatz": zinssatz / 100,
        "laufzeit_jahre": laufzeit_jahre,
        "nebenkosten_kauf": nebenkosten_kauf / 100,
        "wohnfläche": wohnfläche,
        "kaltmiete": kaltmiete,
        "mieterhoehung": mieterhoehung / 100,
        "steuersatz": steuersatz / 100,
        "nicht_umlagefaehige_kosten": nicht_umlagefaehige_kosten,
        "region": region,
        "experteneinschaetzung_aktiv": experteneinschaetzung_aktiv,
        "stadtteil": stadtteil
    }
