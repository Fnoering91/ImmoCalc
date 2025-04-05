
import numpy as np
import streamlit as st
import plotly.graph_objects as go

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
    Zeichnet eine interaktive Plotly-Grafik: Miete pro m² vs. maximal tragbarer Kaufpreis pro m²
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

    # Interaktives Plotly-Diagramm
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=miete_pro_m2,
        y=P,
        name="Max. Kaufpreis €/m²",
        yaxis="y1",
        line=dict(color="blue")
    ))

    fig.add_trace(go.Scatter(
        x=miete_pro_m2,
        y=kaufpreis_gesamt,
        name="Kaufpreis gesamt (€)",
        yaxis="y2",
        line=dict(color="green", dash="dash")
    ))

    fig.update_layout(
        title="🔍 Miete vs. maximal tragbarer Kaufpreis (Plotly)",
        xaxis=dict(title="Miete pro m² (€)"),
        yaxis=dict(
            title="Max. Kaufpreis pro m² (€)",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue")
        ),
        yaxis2=dict(
            title="Max. Kaufpreis gesamt (€)",
            titlefont=dict(color="green"),
            tickfont=dict(color="green"),
            overlaying="y",
            side="right"
        ),
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=60, r=60, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
