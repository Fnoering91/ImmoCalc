import streamlit as st
from modules.inputs import eingabeformular
from modules.berechnung import berechne_finanzierung, zeige_Finanzierungsplan
from modules.zusammenfassung import zeige_zusammenfassung
from modules.plots import plot_kaufpreis_vs_miete
from modules.gpt_experte import experteneinschaetzung_gpt
from modules.exit_berechnung import berechne_exit_option
from modules.speicher import speichere_immobilie, lade_immobilie, liste_immobilien, loesche_immobilie

st.set_page_config(page_title="Immobilien-Rechner", layout="centered")
st.title("🏠 Immobilien-Investment Rechner")

# Früh prüfen, ob eine Übernahme im Gange ist, bevor das Formular gerendert wird
if "uebernahme" in st.session_state:
    uebernommene_daten = st.session_state.pop("uebernahme")
    for key, value in uebernommene_daten.items():
        st.session_state[key] = value
    st.session_state["nach_uebernahme_info"] = st.session_state.pop("uebernahme_name", "unbekannt")
    st.rerun()

# Defaults ergänzen, falls Felder fehlen
default_inputs = {
    "kaufpreis": 316000,
    "eigenkapital": 30000,
    "zinssatz": 3.8,
    "laufzeit_jahre": 25,
    "nebenkosten_kauf": 7,
    "wohnfläche": 56,
    "kaltmiete": 16.0,
    "mieterhoehung": 1,
    "steuersatz": 42,
    "nicht_umlagefaehige_kosten": 25.0,
    "region": "Hamburg",
    "stadtteil": "Bergedorf",
    "annahme_wertsteigerung": 1,
    "annahme_inflation": 1,
    "exit_aktiv": False,
    "exit_nach": 10,
    "experteneinschaetzung_aktiv": False
}

for key, value in default_inputs.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Sidebar: Immobilien-Liste mit Lade-/Löschfunktion
st.sidebar.header("💾 Gespeicherte Immobilien")
immos = liste_immobilien()

if immos:
    auswahl = st.sidebar.selectbox("📂 Immobilie laden", immos)

    col1, col2 = st.sidebar.columns([0.6, 0.4])
    if col1.button("✅ Übernehmen", key="übernehmen"):
        st.session_state["uebernahme"] = lade_immobilie(auswahl)
        st.session_state["uebernahme_name"] = auswahl
        st.rerun()

    if col2.button("🗑️ Löschen", key="löschen"):
        loesche_immobilie(auswahl)
        st.rerun()

# for name in immos:
#     cols = st.sidebar.columns([0.75, 0.25])
#     if cols[0].button(name):
#         if st.sidebar.button(f"✅ Übernehmen '{name}'", key=f"confirm_{name}"):
#             st.session_state["uebernahme"] = lade_immobilie(name)
#             st.session_state["uebernahme_name"] = name
#             st.rerun()
#     if cols[1].button("🗑️", key=f"delete_{name}"):
#         if st.sidebar.button(f"⚠️ Löschen '{name}'", key=f"really_delete_{name}"):
#             loesche_immobilie(name)
#             st.rerun()

# Eingabeformular anzeigen
submitted, inputs = eingabeformular()

# Nachträgliche Info anzeigen nach Übernahme
if "nach_uebernahme_info" in st.session_state:
    st.info(f"Daten von '{st.session_state.pop('nach_uebernahme_info')}' übernommen.")

# Eingabe zum Speichern vorbereiten
with st.form("speichern_formular"):
    immoname = st.text_input("Name für diese Immobilie eingeben:", key="immosave")
    save_clicked = st.form_submit_button("💾 Immobilie speichern")

if save_clicked and immoname:
    speichere_immobilie(immoname, inputs)
    st.success(f"'{immoname}' gespeichert.")
    st.rerun()

# Berechnung und Darstellung
if submitted:
    df, kpis = berechne_finanzierung(inputs)

    with st.expander("## 📊 Zusammenfassung Vollfinanzierung"):
        zeige_zusammenfassung(df, kpis, inputs)

    with st.expander("## Finanzierungsplan"):
        zeige_Finanzierungsplan(df)

    if inputs["exit_aktiv"]:
        st.markdown("---")
        with st.expander("## 📊 Zusammenfassung Exit-Option"):
            berechne_exit_option(inputs, df)

    st.markdown("---")
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
