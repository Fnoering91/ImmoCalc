import streamlit as st

def berechne_exit_option(inputs, df):
    exit_jahr = inputs["exit_nach"]
    if exit_jahr > len(df):
        st.warning("Exit-Zeitpunkt liegt außerhalb der Finanzierungsdauer.")
        return

    # Immobilienwert mit Wertsteigerung
    immowert_exit = inputs["kaufpreis"] * (1 + inputs["annahme_wertsteigerung"] / 100) ** exit_jahr

    # Inflation bereinigt
    realwert_exit = immowert_exit / (1 + inputs["annahme_inflation"] / 100) ** exit_jahr

    # Restschuld zu dem Zeitpunkt
    restschuld_exit = df.loc[df["Jahr"] == exit_jahr, "Restschuld"].values[0]

    # Steuerersparnis bei steuerfreiem Verkauf (angenommen: 25 % Steuer auf Gewinn, ohne Freibeträge etc.)
    hypothetische_steuer = (immowert_exit - inputs["kaufpreis"]) * 0.25 if exit_jahr < 10 else 0

    # Nettoerlös
    nettogewinn = immowert_exit - restschuld_exit

    # Return on Equity (ROE)
    roe = (nettogewinn - inputs["eigenkapital"]) / inputs["eigenkapital"] if inputs["eigenkapital"] > 0 else 0

    # st.subheader(f"📤 Exit nach {exit_jahr} Jahren")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Immobilienwert (Exit)", f"{immowert_exit:,.0f} €")
        st.metric("Steuerersparnis", f"{hypothetische_steuer:,.0f} €")
    with col2:
        st.metric("Restschuld", f"{restschuld_exit:,.0f} €")
        st.metric("Wert in heutiger Kaufkraft", f"{realwert_exit:,.0f} €")
    with col3:
        st.metric("Gewinn nach Kredit", f"{nettogewinn:,.0f} €")
        st.metric("ROE", f"{roe*100:.1f} %")

    return {
        "immowert_exit": immowert_exit,
        "restschuld_exit": restschuld_exit,
        "nettogewinn": nettogewinn,
        "steuerersparnis": hypothetische_steuer,
        "roe": roe
    }
