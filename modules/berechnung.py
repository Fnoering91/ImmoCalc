import streamlit as st
import pandas as pd

def berechne_finanzierung(inputs):
    kaufpreis = inputs["kaufpreis"]
    eigenkapital = inputs["eigenkapital"]
    zinssatz = inputs["zinssatz"]/100
    laufzeit_jahre = inputs["laufzeit_jahre"]
    nebenkosten_kauf = inputs["nebenkosten_kauf"]/100
    wohnfläche = inputs["wohnfläche"]
    kaltmiete = inputs["kaltmiete"]
    mieterhoehung = inputs["mieterhoehung"]/100
    steuersatz = inputs["steuersatz"]/100
    nicht_umlagefaehige_kosten = inputs["nicht_umlagefaehige_kosten"]

    # Berechnungen
    nebenkosten = kaufpreis * nebenkosten_kauf
    gesamtkosten = kaufpreis + nebenkosten
    darlehen = gesamtkosten - eigenkapital

    r = zinssatz
    n = laufzeit_jahre
    a = (r * (1 + r)**n) / ((1 + r)**n - 1)  # Annuität
    zins_monat = zinssatz / 12
    monate = laufzeit_jahre * 12
    try:
        rate = darlehen * (zins_monat / (1 - (1 + zins_monat) ** -monate))
    except ZeroDivisionError:
        st.error("Zinssatz darf nicht 0 sein!")
        st.stop()
    
    # AfA: 2 % auf 80 % des Kaufpreises (ohne NK)
    afa_berechnungsbasis = kaufpreis * 0.8
    afa = afa_berechnungsbasis * 0.02

    rows = []
    restschuld = darlehen
    
    for jahr in range(1, laufzeit_jahre + 1):
        zinsen = restschuld * r
        tilgung = (darlehen * a) - zinsen
        restschuld -= tilgung
        mieteinnahmen = kaltmiete * wohnfläche * 12 * ((1 + mieterhoehung) ** (jahr - 1))
        nebenkosten_real = wohnfläche * nicht_umlagefaehige_kosten
        verlust = zinsen + nebenkosten_real - mieteinnahmen - afa
        steuerlich_absetzbar = mieteinnahmen - (zinsen + afa + nebenkosten_real)
        steuerlicher_vorteil = steuerlich_absetzbar * steuersatz
        reale_monatskosten = (zinsen + tilgung + nebenkosten_real - mieteinnahmen + steuerlicher_vorteil) / 12 # + Steuervorteil, da  negative Zahl bei Steuervorteil
        reale_monatskosten_excl_Steuervorteil = (zinsen + tilgung + nebenkosten_real - mieteinnahmen) / 12    

        rows.append({
            "Jahr": jahr,
            "Restschuld": round(restschuld, 2),
            "Zinskosten": round(zinsen, 2),
            "Tilgung": round(tilgung, 2),
            "Mieteinnahmen": round(mieteinnahmen, 2),
            "AfA": round(afa, 2),
            "Nebenkosten": round(nebenkosten_real, 2),
            "Steuerlicher Vorteil (real)": round(steuerlicher_vorteil, 2),
            "Reale Monatskosten": round(reale_monatskosten, 2),
            "Monatskosten (exkl. Steuervorteil)": round(reale_monatskosten_excl_Steuervorteil, 2)
        })

    df = pd.DataFrame(rows)

    return df, {
        "afa": afa,
        "steuerlicher_vorteil": steuerlicher_vorteil,
        "reale_monatskosten": reale_monatskosten,
        "mieteinnahmen": mieteinnahmen,
        "nebenkosten": nebenkosten_real, 
        "rate": rate
    }
def zeige_Finanzierungsplan(df):
    
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
                        help="2 % Abschreibung auf 80 % des Kaufpreises. Steuerlich absetzbar."
                    ),
                    "Nebenkosten": st.column_config.NumberColumn(
                        "Nebenkosten (€)",
                        help="Nicht umlagefähige Kosten (jährlich). Steuerlich absetzbar. (Instandhaltungsrücklage, Verwaltergebühren, Mietausufallversicherung, Bankgebühren, Hausstrom, Treppenhausreinigung, etc.)"
                    ),
                    "Steuerlicher Vorteil (real)": st.column_config.NumberColumn(
                        "Steuern (€)",
                        help="(Mieteinnahmen - (Zinsen + Afa + Nebenkosten_real)) × Steuersatz. negativ: Steuervorteil, positiv: zusätzliche Steuerbelastung"
                    ),
                    "Reale Monatskosten": st.column_config.NumberColumn(
                        "Reale Monatskosten (€)",
                        help="(Zinsen + Tilgung + Nebenkosten – Mieteinnahmen + Steuern) / 12. "
                    ),
                    "Monatskosten (exkl. Steuervorteil)": st.column_config.NumberColumn(
                        "Monatskosten exkl. Steuervorteil (€)",
                        help="(Zinsen + Tilgung + Nebenkosten – Mieteinnahmen) / 12"
                    )
                }
            )
    return
    
