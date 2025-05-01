
import streamlit as st
import matplotlib.pyplot as plt

def zeige_zusammenfassung(df, kpis, inputs):
    # st.markdown("## 📊 Zusammenfassung Vollfinanzierung")

    col1, col2, col3 = st.columns(3)
    with col1:
        # st.metric("Reale Monatskosten", f"{kpis['reale_monatskosten']:.2f} €", help="= (Zinsen + Tilgung + Nebenkosten – Mieteinnahmen – Steuervorteil) / 12")
        st.metric("mtl. Kreditrate", f"{round(kpis["rate"], 2):,.0f} €", help="= Zinsen + Tilgung")
        st.metric("⌀ mtl. Mieteinnahmen", f"{round(df["Mieteinnahmen"].sum()/inputs["laufzeit_jahre"]/12, 2):,.0f} €", help="= Mietpreis pro qm * Wohnungsgröße (Im Durchschnitt bei dynamischer Mietpreissteigerung)")
        st.metric("⌀ mtl. Belastung abzgl. Mieteinnahmen & Steuern", f"{round(df["Reale Monatskosten"].sum()/inputs["laufzeit_jahre"], 2):,.0f} €", help="= (Zinsen + Tilgung + Nebenkosten – Mieteinnahmen – Steuervorteil) / 12 (Durchschnitt über Laufzeit, da sich bis auf die Nebenkosten alle Werte dynamisch verändern)")

    with col2:
        # st.metric("Jährliche Mieteinnahmen", f"{kpis['mieteinnahmen']:.2f} €")
        st.metric("Gesamtkosten Kredit & Vermietung ", f"{ df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum():,.0f} €", help=" Summe der Zinsen, Tilgung und Nebenkosten für Vermietung über die gesamte Laufzeit")
        st.metric("Davon Tilgung", f"{ df["Tilgung"].sum():,.0f} €", help=" Tilgung über die gesamte Laufzeit")
        st.metric("Davon Zinskosten", f"{ df["Zinskosten"].sum():,.0f} €", help=" Zinskosten über die gesamte Laufzeit")
        st.metric("Davon Nebenkosten", f"{ df["Nebenkosten"].sum():,.0f} €", help=" Nebenkosten über die gesamte Laufzeit")
        
    with col3:
        # st.metric("Jährlicher Steuervorteil", f"{kpis['steuerlicher_vorteil']:.2f} €")
        st.metric("Mieteinnahmen über Laufzeit", f"{ df["Mieteinnahmen"].sum():,.0f} €", help=" Mieteinnahmen über die gesamte Laufzeit")   
        
        steuervorteil = df["Steuerlicher Vorteil (real)"].sum()
        farbe = "green" if steuervorteil < 0 else "red" 

        st.markdown(f"""
        <div style='text-align: left; padding: 0.2em 0;'>
            <div style='font-size: 0.85rem; color: #6c757d;'>Steuervorteil über Laufzeit</div>
            <div style='font-size: 1.75rem; font-weight: 600; color: {farbe};'>{steuervorteil:,.0f} €</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    col21, col22, col23 = st.columns(3)
    with col21:
        preisproqm = inputs["kaufpreis"]/inputs["wohnfläche"]
        st.metric("Preis pro m²", f"{ preisproqm:,.0f} €", help="Kaufpreis pro Quadratmeter Wohnfläche")          

        Kaufpreis_Miet_Verhältnis = inputs["kaufpreis"] / (inputs["kaltmiete"]*inputs["wohnfläche"]*12)
        farbe = "green" if Kaufpreis_Miet_Verhältnis <= 20 else "red" 

        st.markdown(f"""
            <div style='text-align: left; padding: 0.2em 0;'>
                <div style='font-size: 0.85rem; color: #6c757d;'>
                    <span title="Verhältnis von Kaufpreis zu Jahresmiete – grober Indikator für Wirtschaftlichkeit. Unter 20 gilt oft als günstig.">
                        Kaufpreis-Miet-Verhältnis ℹ️
                    </span>
                </div>
                <div style='font-size: 1.75rem; font-weight: 600; color: {farbe};'>{Kaufpreis_Miet_Verhältnis:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col22:
        zinslast = df["Zinskosten"].sum()/(df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum())
        st.metric("Zinslast gesamt", f"{ zinslast*100:.1f} %", help="Anteil der Zinskosten an den Gesamtkosten der Finanzierung")     

        tilgung_1st_year = df["Tilgung"][1]/(df["Restschuld"][1] + df["Tilgung"][1])
        farbe = "green" if tilgung_1st_year <= 0.025 and tilgung_1st_year >= 0.015 else "red" 

        st.markdown(f"""
            <div style='text-align: left; padding: 0.2em 0;'>
                <div style='font-size: 0.85rem; color: #6c757d;'>
                    <span title="Tilgung sollte im ersten Jahr zwischen 1.5 und 2.5% liegen.">
                        Tilgung im ersten Jahr [%] ℹ️
                    </span>
                </div>
                <div style='font-size: 1.75rem; font-weight: 600; color: {farbe};'>{tilgung_1st_year*100:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)            
    
    with col23:
        steuerquote = -df["Steuerlicher Vorteil (real)"].sum()/(df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum())
        st.metric("Steuerquote", f"{ steuerquote*100:.1f} %", help="Anteil der Gesamtkosten, die durch Steuern reduziert werden können.")   
        mietrendite = df["Mieteinnahmen"].sum()/(df["Zinskosten"].sum() + df["Tilgung"].sum() + df["Nebenkosten"].sum())
        st.metric("Mietrendite", f"{ mietrendite*100:.1f} %", help="Verhältnis von Mieteinnahmen zu Gesamtkosten der Finanzierung.")   

    st.markdown("---")
    col31, col32, col33 = st.columns(3)
    with col31:
        immowert = inputs["kaufpreis"]*(1+inputs["annahme_wertsteigerung"]/100) ** inputs["laufzeit_jahre"]
        st.metric("Immobilienpreis inkl. Wertsteigerung", f"{ immowert:,.0f} €", help="nach Kreditlaufzeit")            

    with col32:
        realer_immowert = immowert / (1 + inputs["annahme_inflation"]/100) ** inputs["laufzeit_jahre"]
        st.metric("Kaufkraft in heutigen Preisen", f"{ realer_immowert:,.0f} €", help="Immobilienwert (inkl. Wertsteigerung) reduziert um Inflation")            

    # with col33:
    
    st.markdown("---")
    # st.subheader("🔢 Monatswerte")
    # st.write(f"- **Reale Monatskosten**: {kpis['reale_monatskosten']:.2f} €")
    # st.write(f"- **Mieteinnahmen pro Monat**: {kpis['mieteinnahmen'] / 12:.2f} €")

    # st.subheader("📅 Jahreswerte")
    # st.write(f"- **Mieteinnahmen (brutto)**: {kpis['mieteinnahmen']:.2f} €")
    # st.write(f"- **AfA**: {kpis['afa']:.2f} €")
    # st.write(f"- **Nebenkosten (nicht umlagefähig)**: {kpis['nebenkosten']:.2f} €")
    # st.write(f"- **Steuervorteil (realistisch)**: {kpis['steuerlicher_vorteil']:.2f} €")

    # st.subheader(f"📈 Gesamtwerte über {inputs["laufzeit_jahre"]} Jahre")
    # gesamt_steuer_vorteil = kpis['steuerlicher_vorteil'] * inputs["laufzeit_jahre"]
    # st.write(f"- **Gesamter Steuervorteil**: {gesamt_steuer_vorteil:.2f} €")

    # # Diagramm: Restschuld-Verlauf
    # if 'Restschuld' in df.columns:
    #     st.markdown("### 📉 Restschuld-Verlauf")
    #     fig, ax = plt.subplots()
    #     ax.plot(df['Jahr'], df['Restschuld'], marker='o')
    #     ax.set_xlabel("Jahr")
    #     ax.set_ylabel("Restschuld (€)")
    #     ax.set_title("Entwicklung der Restschuld über die Jahre")
    #     ax.grid(True)
    #     st.pyplot(fig)
    return

