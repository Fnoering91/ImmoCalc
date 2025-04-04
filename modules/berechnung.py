
import pandas as pd

def berechne_finanzierung(inputs):
    kaufpreis = inputs["kaufpreis"]
    eigenkapital = inputs["eigenkapital"]
    zinssatz = inputs["zinssatz"]
    laufzeit_jahre = inputs["laufzeit_jahre"]
    nebenkosten_kauf = inputs["nebenkosten_kauf"]
    wohnfläche = inputs["wohnfläche"]
    kaltmiete = inputs["kaltmiete"]
    mieterhoehung = inputs["mieterhoehung"]
    steuersatz = inputs["steuersatz"]
    nicht_umlagefaehige_kosten = inputs["nicht_umlagefaehige_kosten"]

    # Berechnungen
    nebenkosten = kaufpreis * nebenkosten_kauf
    gesamtkosten = kaufpreis + nebenkosten
    darlehen = gesamtkosten - eigenkapital

    r = zinssatz
    n = laufzeit_jahre
    a = (r * (1 + r)**n) / ((1 + r)**n - 1)  # Annuität

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
        steuerlicher_vorteil = max(0, verlust * steuersatz)
        reale_monatskosten = (zinsen + tilgung + nebenkosten_real - mieteinnahmen - steuerlicher_vorteil) / 12

        rows.append({
            "Jahr": jahr,
            "Restschuld": round(restschuld, 2),
            "Zinskosten": round(zinsen, 2),
            "Tilgung": round(tilgung, 2),
            "Mieteinnahmen": round(mieteinnahmen, 2),
            "AfA": round(afa, 2),
            "Nebenkosten": round(nebenkosten_real, 2),
            "Steuerlicher Vorteil (real)": round(steuerlicher_vorteil, 2),
            "Reale Monatskosten": round(reale_monatskosten, 2)
        })

    df = pd.DataFrame(rows)

    return df, {
        "afa": afa,
        "steuerlicher_vorteil": steuerlicher_vorteil,
        "reale_monatskosten": reale_monatskosten,
        "mieteinnahmen": mieteinnahmen,
        "nebenkosten": nebenkosten_real
    }
