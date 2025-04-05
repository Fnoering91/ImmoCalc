
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def plot_kaufpreis_vs_miete(
    zinssatz: float,
    laufzeit_jahre: int,
    eigenkapital: float,
    nebenkosten_kauf: float,
    wohnfläche: float,
    nebenkosten_mtl_pro_m2: float = 1.0,
    miete_min: float = 8.0,
    miete_max: float = 20.0,
    schritte: int = 100
):
    """
    Zeichnet eine Grafik: Miete pro m² vs. maximal tragbarer Kaufpreis pro m²
    """

    # Annuitätsfaktor
    r = zinssatz
    n = laufzeit_jahre
    a = (r * (1 + r)**n) / ((1 + r)**n - 1)

    # Miete pro m² durchsimulieren
    miete_pro_m2 = np.linspace(miete_min, miete_max, schritte)

    # Max. Kaufpreis €/m² berechnen
    P = ((miete_pro_m2 - nebenkosten_mtl_pro_m2) * wohnfläche * 12 + eigenkapital * a) / (wohnfläche * (1 + nebenkosten_kauf) * a)
    kaufpreis_gesamt = P * wohnfläche

    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color1 = 'tab:blue'
    ax1.set_xlabel("Miete pro m² (€)")
    ax1.set_ylabel("Max. Kaufpreis pro m² (€)", color=color1)
    ax1.plot(miete_pro_m2, P, color=color1, label="Max. Kaufpreis €/m²")
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True)

    # Zweite Y-Achse
    ax2 = ax1.twinx()
    color2 = 'tab:green'
    ax2.set_ylabel("Max. Kaufpreis gesamt (€)", color=color2)
    ax2.plot(miete_pro_m2, kaufpreis_gesamt, color=color2, linestyle='--', label="Kaufpreis gesamt")
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()
    ax1.set_title("🔍 Miete vs. maximal tragbarer Kaufpreis (Formelbasiert)")
    st.pyplot(fig)
