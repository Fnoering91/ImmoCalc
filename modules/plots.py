
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    r = zinssatz
    n = laufzeit_jahre
    a = (r * (1 + r)**n) / ((1 + r)**n - 1)

    miete_pro_m2 = np.linspace(miete_min, miete_max, schritte)
    P = ((miete_pro_m2 - nebenkosten_mtl_pro_m2) * wohnfläche * 12 + eigenkapital * a) / (wohnfläche * (1 + nebenkosten_kauf) * a)
    kaufpreis_gesamt = P * wohnfläche

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=miete_pro_m2, y=P, name="Max. Kaufpreis €/m²", line=dict(color="blue")), secondary_y=False)
    fig.add_trace(go.Scatter(x=miete_pro_m2, y=kaufpreis_gesamt, name="Kaufpreis gesamt (€)", line=dict(color="green", dash="dash")), secondary_y=True)

    fig.update_layout(
        title="🔍 Miete vs. maximal tragbarer Kaufpreis",
        xaxis_title="Miete pro m² (€)",
        yaxis_title="Max. Kaufpreis pro m² (€)",
        yaxis2_title="Kaufpreis gesamt (€)",
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=60, r=60, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
