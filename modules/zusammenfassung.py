
import streamlit as st
import matplotlib.pyplot as plt

def zeige_zusammenfassung(df, kpis, laufzeit_jahre):
    st.markdown("## 📊 Zusammenfassung der Finanzierung")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Reale Monatskosten", f"{kpis['reale_monatskosten']:.2f} €", help="= (Zinsen + Tilgung + Nebenkosten – Mieteinnahmen – Steuervorteil) / 12")
    with col2:
        st.metric("Jährliche Mieteinnahmen", f"{kpis['mieteinnahmen']:.2f} €")
    with col3:
        st.metric("Jährlicher Steuervorteil", f"{kpis['steuerlicher_vorteil']:.2f} €")

    st.markdown("---")
    st.subheader("🔢 Monatswerte")
    st.write(f"- **Reale Monatskosten**: {kpis['reale_monatskosten']:.2f} €")
    st.write(f"- **Mieteinnahmen pro Monat**: {kpis['mieteinnahmen'] / 12:.2f} €")

    st.subheader("📅 Jahreswerte")
    st.write(f"- **Mieteinnahmen (brutto)**: {kpis['mieteinnahmen']:.2f} €")
    st.write(f"- **AfA**: {kpis['afa']:.2f} €")
    st.write(f"- **Nebenkosten (nicht umlagefähig)**: {kpis['nebenkosten']:.2f} €")
    st.write(f"- **Steuervorteil (realistisch)**: {kpis['steuerlicher_vorteil']:.2f} €")

    st.subheader(f"📈 Gesamtwerte über {laufzeit_jahre} Jahre")
    gesamt_steuer_vorteil = kpis['steuerlicher_vorteil'] * laufzeit_jahre
    st.write(f"- **Gesamter Steuervorteil**: {gesamt_steuer_vorteil:.2f} €")

    # Diagramm: Restschuld-Verlauf
    if 'Restschuld' in df.columns:
        st.markdown("### 📉 Restschuld-Verlauf")
        fig, ax = plt.subplots()
        ax.plot(df['Jahr'], df['Restschuld'], marker='o')
        ax.set_xlabel("Jahr")
        ax.set_ylabel("Restschuld (€)")
        ax.set_title("Entwicklung der Restschuld über die Jahre")
        ax.grid(True)
        st.pyplot(fig)
