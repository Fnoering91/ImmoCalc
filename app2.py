
import streamlit as st
from modules.inputs import eingabeformular
from modules.berechnung import berechne_finanzierung
from modules.berechnung import zeige_Finanzierungsplan
from modules.zusammenfassung import zeige_zusammenfassung
from modules.plots import plot_kaufpreis_vs_miete
from modules.gpt_experte import experteneinschaetzung_gpt
from modules.exit_berechnung import berechne_exit_option


st.set_page_config(page_title="Immobilien-Rechner", layout="centered")
st.title("🏠 Immobilien-Investment Rechner")

# Eingabeformular anzeigen
submitted, inputs = eingabeformular()

# Berechnung und Darstellung
if submitted:
    df, kpis = berechne_finanzierung(inputs)
    # st.subheader("Berechnungsergebnisse")

    with st.expander("## 📊 Zusammenfassung Vollfinanzierung"):
        zeige_zusammenfassung(df, kpis, inputs)

    with st.expander("## Finanzierungsplan"):
        zeige_Finanzierungsplan(df)

    if inputs["exit_aktiv"]:
        st.markdown("---")
        with st.expander("## 📊 Zusammenfassung Exit-Option"):
        berechne_exit_option(inputs, df)
    
    st.markdown("---")
    # st.subheader("📈 Tragfähiger Kaufpreis je nach Mieteinnahme")
    with st.expander("## 📈 Tragfähiger Kaufpreis je nach Mieteinnahme"):
        plot_kaufpreis_vs_miete(
            zinssatz=inputs["zinssatz"],
            laufzeit_jahre=inputs["laufzeit_jahre"],
            eigenkapital=inputs["eigenkapital"],
            nebenkosten_kauf=inputs["nebenkosten_kauf"],
            wohnfläche=inputs["wohnfläche"],
            nebenkosten_mtl_pro_m2=inputs["nicht_umlagefaehige_kosten"] / 12
        )

    if inputs["experteneinschaetzung_aktiv"]:
        st.markdown("---")
        st.subheader("🧠 Experteneinschätzung (GPT)")
        finanzdaten = {
            "Kaufpreis": inputs["kaufpreis"],
            "Eigenkapital": inputs["eigenkapital"],
            "Zinssatz": inputs["zinssatz"],
            "Laufzeit": inputs["laufzeit_jahre"],
            "Wohnfläche": inputs["wohnfläche"],
            "Kaltmiete": inputs["kaltmiete"],
            "Reale Monatskosten": round(kpis["reale_monatskosten"], 2),
            "Mieteinnahmen (jährlich)": round(kpis["mieteinnahmen"], 2),
            "Steuervorteil (real)": round(kpis["steuerlicher_vorteil"], 2),
        }

        lageinfo = {
            "Region": inputs["region"],
            "Lagequalität": "nicht angegeben",
            "Marktumfeld": "nicht spezifiziert"
        }

        with st.spinner("GPT bewertet dein Vorhaben..."):
            expertenmeinung = experteneinschaetzung_gpt(finanzdaten, lageinfo)
        st.info(expertenmeinung)
