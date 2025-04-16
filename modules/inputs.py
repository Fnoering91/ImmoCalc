
import streamlit as st

def eingabeformular():
    with st.form("eingabe_formular"):
        st.subheader("Berechnungsgrundlagen")

        col1, col2 = st.columns(2)

         with col1:
            kaufpreis = st.number_input("Kaufpreis (€)", min_value=10000, key="kaufpreis")
            eigenkapital = st.number_input("Eigenkapital (€)", min_value=0, step=10000, help="= Eigenkapital, welches den notwendigen Kreditrahmen reduziert", key="eigenkapital")
            zinssatz = st.number_input("Zinssatz (p.a.)", min_value=0.1, max_value=10.0, step=0.1, help="= Zinssatz für Kredit", key="zinssatz")
            laufzeit_jahre = st.number_input("Laufzeit (Jahre)", min_value=5, max_value=40, help="= Laufzeit des Kredits", key="laufzeit_jahre")
            nebenkosten_kauf = st.number_input("Kaufnebenkosten (%)", min_value=0.0, max_value=20.0, help="= Grunderwerbsteuer, Makler, Notar etc.", key="nebenkosten_kauf")                
        
        with col2:            
            wohnfläche = st.number_input("Wohnfläche (m²)", min_value=10, help="= zur Berechnung von Mieteinnahmen", key="wohnfläche")
            kaltmiete = st.number_input("Kaltmiete (€/m²)", min_value=1.0, step=0.1, help="= durchschnittlicher Mietpreis", key="kaltmiete")
            mieterhoehung = st.slider("Jährliche Mieterhöhung (%)", 0.0, 5.0, step=0.1, key="mieterhoehung")
            region = st.text_input("Region der Immobilie", help="= Stadt oder Ballungsraum. Wird nur für die Expertenmeinung verwendet.", key="region")
            stadtteil = st.text_input("Stadtteil der Immobilie", help="Wird nur für die Expertenmeinung verwendet.", key="stadtteil")

        st.markdown("---")
        col21, col22 = st.columns(2)
        with col21:
            steuersatz = st.slider("Persönlicher Steuersatz (%)", 0, 50, key="steuersatz")
            nicht_umlagefaehige_kosten = st.number_input("Nicht umlagefähige Nebenkosten (€/m² p.a.)", min_value=0.0, step=1.0, help = "Diese fallen regelmäßig an und können nicht auf den Mieter umgelegt werden (Höhe typischerweise ca. 20–30 €/m²/Jahr). Dazu zählen u.a. Verwaltungskosten (z. B. Hausverwaltung), Instandhaltungsrücklage, Reparaturkosten, Bankgebühren, ggf. Leerstandskosten (z. B. Mietausfallversicherung)", key="nicht_umlagefaehige_kosten")            
        with col22:
            annahme_wertsteigerung = st.slider("Wertsteigerung der Immobilie pro Jahr (%)", -5.0, 5.0, step=0.1, help="Nominal = OHNE Einbezug von Inflation. --> Nominal, also ohne Berücksichtigung der Inflation, stiegen die Immobilienpreise in Deutschland seit 1975 um etwa 215 %. Das entspricht einer durchschnittlichen jährlichen Steigerung von ungefähr 2,7 %. ", key="annahme_wertsteigerung")
            annahme_inflation = st.slider("Inflation pro Jahr (%)", -5.0, 5.0, step=0.1, help="", key="annahme_inflation")                

        st.markdown("---")
        col31, col32 = st.columns(2)
        with col31:
            exit_aktiv = st.checkbox("Exit Option berechnen", help="Exit bezeichnet die Möglichkeit frühzeitig aus dem Kredit auszusteigen, indem die Immobilie verkauft wird und der steuerfreie Gewinn durch Wertsteigerung realisiert wird.", key="exit_aktiv")
        with col32:
            exit_nach = st.number_input("Exit nach (Jahre)", min_value=10, max_value=30, help=" nach 10 Jahren Haltedauer sind die Gewinne durch Verkauf steuerfrei!", key="exit_nach")
        
        st.markdown("---")
        col41, col42 = st.columns(2)
        with col41:
            experteneinschaetzung_aktiv = st.checkbox("GPT-Experteneinschätzung aktivieren", key="experteneinschaetzung_aktiv")
        
        # with col1:
        #     kaufpreis = st.number_input("Kaufpreis (€)", min_value=10000, value=st.session_state.get("kaufpreis", 316000), step=10000, help="= Kaufpreis OHNE Kaufnebenkosten", key="kaufpreis")
        #     eigenkapital = st.number_input("Eigenkapital (€)", min_value=0, value=st.session_state.get("eigenkapital", 30000), step=10000, help="= Eigenkapital, welches den notwendigen Kreditrahmen reduziert", key="eigenkapital")
        #     zinssatz = st.number_input("Zinssatz (p.a.)", min_value=0.1, max_value=10.0, value=st.session_state.get("zinssatz", 3.8), step=0.1, help="= Zinssatz für Kredit", key="zinssatz")
        #     laufzeit_jahre = st.number_input("Laufzeit (Jahre)", min_value=5, max_value=40, value=st.session_state.get("laufzeit_jahre", 25), help="= Laufzeit des Kredits", key="laufzeit_jahre")
        #     nebenkosten_kauf = st.number_input("Kaufnebenkosten (%)", min_value=0.0, max_value=20.0, value=st.session_state.get("nebenkosten_kauf", 7.0), help="= Grunderwerbsteuer, Makler, Notar etc.", key="nebenkosten_kauf")                
        
        # with col2:            
        #     wohnfläche = st.number_input("Wohnfläche (m²)", min_value=10, value=st.session_state.get("wohnfläche", 56), help="= zur Berechnung von Mieteinnahmen", key="wohnfläche")
        #     kaltmiete = st.number_input("Kaltmiete (€/m²)", min_value=1.0, value=st.session_state.get("kaltmiete", 16.0), step=0.1, help="= durchschnittlicher Mietpreis", key="kaltmiete")
        #     mieterhoehung = st.slider("Jährliche Mieterhöhung (%)", 0.0, 5.0, value=st.session_state.get("mieterhoehung", 1.0), step=0.1, key="mieterhoehung")
        #     region = st.text_input("Region der Immobilie", value=st.session_state.get("region", "Hamburg"), help="= Stadt oder Ballungsraum. Wird nur für die Expertenmeinung verwendet.", key="region")
        #     stadtteil = st.text_input("Stadtteil der Immobilie", value = st.session_state.get("stadtteil", "Bergedorf"), help="Wird nur für die Expertenmeinung verwendet.", key="stadtteil")

        # st.markdown("---")
        # col21, col22 = st.columns(2)
        # with col21:
        #     steuersatz = st.slider("Persönlicher Steuersatz (%)", 0, 50, value=int(st.session_state.get("steuersatz", 42)), key="steuersatz")
        #     nicht_umlagefaehige_kosten = st.number_input("Nicht umlagefähige Nebenkosten (€/m² p.a.)", min_value=0.0, value=st.session_state.get("nicht_umlagefaehige_kosten", 25.0), step=1.0, help = "Diese fallen regelmäßig an und können nicht auf den Mieter umgelegt werden (Höhe typischerweise ca. 20–30 €/m²/Jahr). Dazu zählen u.a. Verwaltungskosten (z. B. Hausverwaltung), Instandhaltungsrücklage, Reparaturkosten, Bankgebühren, ggf. Leerstandskosten (z. B. Mietausfallversicherung)", key="nicht_umlagefaehige_kosten")            
        # with col22:
        #     annahme_wertsteigerung = st.slider("Wertsteigerung der Immobilie pro Jahr (%)", -5.0, 5.0, value=st.session_state.get("annahme_wertsteigerung", 0.0), step=0.1, help="Nominal = OHNE Einbezug von Inflation. --> Nominal, also ohne Berücksichtigung der Inflation, stiegen die Immobilienpreise in Deutschland seit 1975 um etwa 215 %. Das entspricht einer durchschnittlichen jährlichen Steigerung von ungefähr 2,7 %. ", key="annahme_wertsteigerung")
        #     annahme_inflation = st.slider("Inflation pro Jahr (%)", -5.0, 5.0, value=st.session_state.get("annahme_inflation", 1.0), step=0.1, help="", key="annahme_inflation")                

        # st.markdown("---")
        # col31, col32 = st.columns(2)
        # with col31:
        #     exit_aktiv = st.checkbox("Exit Option berechnen", value=st.session_state.get("exit_aktiv", False), help="Exit bezeichnet die Möglichkeit frühzeitig aus dem Kredit auszusteigen, indem die Immobilie verkauft wird und der steuerfreie Gewinn durch Wertsteigerung realisiert wird.", key="exit_aktiv")
        # with col32:
        #     exit_nach = st.number_input("Exit nach (Jahre)", min_value=10, max_value=30, value=st.session_state.get("exit_nach", 10), help=" nach 10 Jahren Haltedauer sind die Gewinne durch Verkauf steuerfrei!", key="exit_nach")
        
        # st.markdown("---")
        # col41, col42 = st.columns(2)
        # with col41:
        #     experteneinschaetzung_aktiv = st.checkbox("GPT-Experteneinschätzung aktivieren", value=st.session_state.get("experteneinschaetzung_aktiv", False), key="experteneinschaetzung_aktiv")
        
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
        "stadtteil": stadtteil, 
        "annahme_wertsteigerung":annahme_wertsteigerung, 
        "annahme_inflation":annahme_inflation,
        "exit_aktiv": exit_aktiv,
        "exit_nach":exit_nach
    }
