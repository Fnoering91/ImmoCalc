
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Immobilien-Rechner", layout="centered")
st.title("Immobilien-Investment Rechner")

# with st.expander("**Spaltenbeschreibung anzeigen**"):
#     st.markdown("""
#     - **Restschuld**: Verbleibender Kreditbetrag am Jahresende  
#     - **Zinskosten**: Im Jahr gezahlte Kreditzinsen  
#     - **Tilgung**: Im Jahr getilgter Kreditbetrag  
#     - **Mieteinnahmen**: Jahresmiete (mit dynamischer Erhöhung)  
#     - **AfA**: Abschreibung, 2 % auf 80 % des Kaufpreises  
#     - **Nebenkosten**: Nicht umlagefähige Kosten (jährlich)  
#     - **Steuerlicher Vorteil (real)**: steuerlicher Verlust × Steuersatz  
#     - **Reale Monatskosten**: (Zinsen + Tilgung + Nebenkosten – Mieteinnahmen – Steuervorteil) / 12
#     """)

with st.form("eingabe_formular"):
    st.subheader("Berechnungsgrundlagen")

    col1, col2 = st.columns(2)

    with col1:
        kaufpreis = st.number_input("Kaufpreis (€)", min_value=10000, value=316000, step=10000, help="= Kaufpreis OHNE Kaufnebenkosten")
        eigenkapital = st.number_input("Eigenkapital (€)", min_value=0, value=30000, step=10000, help="= Eigenkapital, welches den notwendigen Kreditrahmen reduziert")
        zinssatz = st.number_input("Zinssatz (p.a.)", min_value=0.1, max_value=10.0, value=3.8, step=0.1, help="= Zinssatz für Kredit")
        laufzeit_jahre = st.number_input("Laufzeit (Jahre)", min_value=5, max_value=40, value=20, help="= Laufzeit des Kredits")
        nebenkosten_kauf = st.number_input("Kaufnebenkosten (%)", min_value=0.0, max_value=20.0, value=7.0, help="= prozentualer Wert des Kaufpreises -> Grunderwerbsteuer (3,5-6,5%), Maklerkosten (5-7%) sowie Notar- und Grundbuchkosten (1-1,5%)")
        region = st.text_input("Region der Immobilie", value = "Hamburg", help="= Stadt oder Ballungsraum. Wird nur für die Expertenmeinung verwendet.")
        experteneinschaetzung_aktiv = st.checkbox("GPT-Experteneinschätzung aktivieren", value=False)

    with col2:
        wohnfläche = st.number_input("Wohnfläche (m²)", min_value=10, value=56, help="")
        miete_pro_m2 = st.number_input("Miete pro m² (€)", min_value=1.0, value=16.0, step=0.5, help="")
        mieterhoehung = st.number_input("Jährliche Mieterhöhung (%)", min_value=0.0, max_value=10.0, value=1.0, help="")
        nebenkosten = st.number_input("Nicht umlagefähige Nebenkosten (€/Monat)", min_value=0, value=250, help="Verwaltungs- oder Instandhaltungskosten sowie einmalige Ausgaben, etwa die Neuanlage eines Gartens oder die Installation neuer Feuerlöscher")
        steuersatz = st.number_input("Persönlicher Steuersatz (%)", min_value=0.0, max_value=50.0, value=42.0, help="")
        stadtteil = st.text_input("Stadtteil der Immobilie", value = "Bergedorf", help="Wird nur für die Expertenmeinung verwendet.")

    berechnen = st.form_submit_button("Neu berechnen")

if berechnen:
    zins = zinssatz / 100
    steuersatz = steuersatz / 100
    mieterhoehung = mieterhoehung / 100
    gesamtkosten = kaufpreis * (1 + nebenkosten_kauf / 100)
    darlehen = gesamtkosten - eigenkapital
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
        miete_pro_monat *= (1 + mieterhoehung)
        betriebskosten = nebenkosten * 12
        steuerlich_absetzbar = mieteinnahmen - (zinskosten + abschreibung + betriebskosten)
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
        "Monatliche Kreditrate": [round(rate, 2)],
        "Gesamtausgaben (inkl. Tilgung)": [df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum()],
        "Davon Zinsen": [df["Zinskosten"].sum()],
        "Davon Nebenkosten": [df["Nebenkosten"].sum()],
        "Davon Tilgung": [df["Tilgung"].sum()],
        "Gesamte Mieteinnahmen": [df["Mieteinnahmen"].sum()],
        "Steuervorteil (real)": [df["Steuerlicher Vorteil (real)"].sum()],
        "Monatliche Belastung (nach Steuern)": [((df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum() - df["Mieteinnahmen"].sum() + df["Steuerlicher Vorteil (real)"].sum()) / (len(df)*12))]
    })
    steuerlicher_vorteil = -df["Steuerlicher Vorteil (real)"].sum()

    st.subheader("Berechnungsergebnisse")
    st.dataframe(df.style.format("{:,.2f}"), use_container_width=True,
                column_config={
                    "Restschuld": st.column_config.NumberColumn(
                        "Restschuld (€)",
                        help="Verbleibender Kreditbetrag am Jahresende"
                    ),
                    "Zinskosten": st.column_config.NumberColumn(
                        "Zinskosten (€)",
                        help="Im Jahr gezahlte Kreditzinsen"
                    ),
                    "Tilgung": st.column_config.NumberColumn(
                        "Tilgung (€)",
                        help="Im Jahr getilgter Kreditbetrag"
                    ),
                    "Mieteinnahmen": st.column_config.NumberColumn(
                        "Mieteinnahmen (€)",
                        help="Jahresmiete inkl. Mieterhöhung"
                    ),
                    "AfA": st.column_config.NumberColumn(
                        "AfA (€)",
                        help="2 % Abschreibung auf 80 % des Kaufpreises"
                    ),
                    "Nebenkosten": st.column_config.NumberColumn(
                        "Nebenkosten (€)",
                        help="Nicht umlagefähige Kosten (jährlich)"
                    ),
                    "Steuerlicher Vorteil (real)": st.column_config.NumberColumn(
                        "Steuervorteil (€)",
                        help="Verlust × Steuersatz"
                    ),
                    "Reale Monatskosten": st.column_config.NumberColumn(
                        "Reale Monatskosten (€)",
                        help="(Zinsen + Tilgung + Nebenkosten – Mieteinnahmen – Steuervorteil) / 12"
                    )
                }
            )
    
    with st.expander("**Zusammenfassung **"):
        # --- Strukturierte Zusammenfassung ---

        # st.markdown("## 📊 Zusammenfassung der Finanzierung")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("mtl. Kreditrate", f"{round(rate, 2):,.2f} €", help="= Zinsen + Tilgung")
            st.metric("⌀ mtl. Mieteinnahmen", f"{round(df["Mieteinnahmen"].sum()/laufzeit_jahre/12, 2):,.2f} €", help="= Mietpreis pro qm * Wohnungsgröße (Im Durchschnitt bei dynamischer Mietpreissteigerung)")
            st.metric("⌀ mtl. Belastung abzgl. Mieteinnahmen & Steuern", f"{round(df["Reale Monatskosten"].sum()/laufzeit_jahre, 2):,.2f} €", help="= (Zinsen + Tilgung + Nebenkosten – Mieteinnahmen – Steuervorteil) / 12 (Durchschnitt über Laufzeit, da sich bis auf die Nebenkosten alle Werte dynamisch verändern)")
        
        with col2:
            st.metric("Gesamtkosten Kredit & Vermietung ", f"{ df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum():,.2f} €", help=" Summe der Zinsen, Tilgung und Nebenkosten für Vermietung über die gesamte Laufzeit")
            st.metric("Davon Tilgung", f"{ df["Tilgung"].sum():,.2f} €", help=" Tilgung über die gesamte Laufzeit")
            st.metric("Davon Zinskosten", f"{ df["Zinskosten"].sum():,.2f} €", help=" Zinskosten über die gesamte Laufzeit")
            st.metric("Davon Nebenkosten", f"{ df["Nebenkosten"].sum():,.2f} €", help=" Nebenkosten über die gesamte Laufzeit")

        with col3:
            st.metric("Mieteinnahmen über Laufzeit", f"{ df["Mieteinnahmen"].sum():,.2f} €", help=" Mieteinnahmen über die gesamte Laufzeit")            
            st.metric("Steuervorteil über Laufzeit", f"{df["Steuerlicher Vorteil (real)"].sum():,.2f} €", help="Summe der jährlichen Steuervor- oder Nachteile. Negativ: Steuervorteil, Positiv: Steuernachteil")


        col21, col22, col23 = st.columns(3)
        with col21:
            preisproqm = kaufpreis/wohnfläche
            st.metric("Preis pro m²", f"{ preisproqm:.2f} %", help="Kaufpreis pro Quadratmeter Wohnfläche")            

        with col22:
            zinslast = df["Zinskosten"].sum()/(df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum())
            st.metric("Zinslast gesamt", f"{ zinslast*100:.2f} %", help="Anteil der Zinskosten an den Gesamtkosten der Finanzierung")            
  
        with col23:
            steuerquote = -df["Steuerlicher Vorteil (real)"].sum()/(df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum())
            st.metric("Steuerquote", f"{ steuerquote*100:.2f} %", help="Anteil der Gesamtkosten, die durch Steuern reduziert werden können.")   
            mietrendite = df["Mieteinnahmen"].sum()/(df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum())
            st.metric("Mietrendite", f"{ mietrendite*100:.2f} %", help="Verhältnis von Mieteinnahmen zu Gesamtkosten der Finanzierung.")   
            
        # st.dataframe(gesamt.style.format("{:,.2f}"), use_container_width=True)    

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

    
    st.subheader("📈 Break-Even Analyse: Kaltmiete vs. monatliche Kosten")
    import plotly.graph_objects as go

    miete_values = []
    kosten_values = []

    for miete_test in range(5, 30):
        test_miete_pro_monat = wohnfläche * miete_test
        mieteinnahmen_total = 0
        saldo_test = darlehen
        for jahr in range(1, laufzeit_jahre + 1):
            for monat in range(12):
                zinsanteil = saldo_test * zins_monat
                tilgungsanteil = rate - zinsanteil
                saldo_test -= tilgungsanteil
            test_miete_pro_monat *= (1 + mieterhoehung)
            mieteinnahmen_total += test_miete_pro_monat * 12

        gesamt_zins = df["Zinskosten"].sum()
        gesamt_tilgung = df["Tilgung"].sum()
        gesamt_nebenkosten = df["Nebenkosten"].sum()
        gesamtausgaben = gesamt_zins + gesamt_tilgung + gesamt_nebenkosten
        monatl_kosten = gesamtausgaben / (laufzeit_jahre * 12)
        monatl_miete = mieteinnahmen_total / (laufzeit_jahre * 12)

        miete_values.append(miete_test)
        kosten_values.append(monatl_miete - monatl_kosten)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=miete_values, y=kosten_values, mode='lines+markers', name='Überschuss (Miete - Kosten)'))
    fig.add_hline(y=0, line=dict(dash='dash', color='red'), annotation_text="Break-even", annotation_position="bottom right")
    fig.update_layout(title="Break-even-Analyse: Miete pro m²",
                      xaxis_title="Kaltmiete pro m² (€)",
                      yaxis_title="Monatlicher Überschuss (€)",
                      showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


    # --- Experteneinschätzung mit GPT einholen ---
    import openai
    import streamlit as st
    
    client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])
    
    def experteneinschaetzung_gpt(berechnungsdaten):
        system_prompt = (
            "Du bist ein Immobilienfinanzierungsexperte. "
            "Bewerte die Tragfähigkeit und Wirtschaftlichkeit folgender Immobilienfinanzierung. "
            "Weise auf Risiken hin, nenne Verbesserungsvorschläge und vergleiche ggf. mit typischen Finanzierungskonzepten."
            "Bewerte den Immobilienkauf auch auf Basis der Lage der Immobilie. Ziehe die wenn möglich online Statistiken zu Miet- und Kaufpreisen zu dem angegebenen Ort und beziehe sie in deine Bewertung mit ein. Betrachte auch ob die Lage langfristige Wertzuwächse der Immobilie ermöglicht."
        )
    
        user_prompt = f"Hier sind die Eckdaten der Finanzierung:\n{berechnungsdaten}"
    
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Fehler beim Abrufen der Experteneinschätzung: {e}"
    
    
    
    # --- Experteneinschätzung anzeigen ---
    berechnungsdaten = {
        "Kaufpreis": kaufpreis,
        "Eigenkapital": eigenkapital,
        "Zinssatz": zinssatz,
        "Laufzeit (Jahre)": laufzeit_jahre,
        "Kaufnebenkosten (%)": nebenkosten_kauf,
        "Wohnfläche (m²)": wohnfläche,
        "Kaufpreis pro m²" : preisproqm,
        "Kreditrate pro Monat": rate,
        "⌀ mtl. Mieteinnahmen": df["Mieteinnahmen"].sum()/laufzeit_jahre/12,
        "⌀ mtl. Belastung abzgl. Mieteinnahmen & Steuern": df["Reale Monatskosten"].sum()/laufzeit_jahre,
        "Gesamtkosten Kredit & Vermietung": df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum(),
        "Gesamtkosten Tilgung": df["Tilgung"].sum(),
        "Gesamtkosten Zinskosten": df["Zinskosten"].sum(),
        "Gesamtkosten Nebenkosten": df["Nebenkosten"].sum(),
        "Mieteinnahmen über Laufzeit": df["Mieteinnahmen"].sum(),
        "Steuervorteil über Laufzeit": -df["Steuerlicher Vorteil (real)"].sum(),
        "Region der Immobilie": region ,
        "Stadtteil der Immobilie": stadtteil,
    }
    
    st.markdown("---")
    st.subheader("Experteneinschätzung (automatisch durch GPT)")
    if experteneinschaetzung_aktiv:
        with st.spinner("Wird analysiert..."):
            expertenmeinung = experteneinschaetzung_gpt(berechnungsdaten)
        st.info(expertenmeinung)
    else:
        st.info("Die GPT-Experteneinschätzung wurde nicht aktiviert.")
