import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from arch import arch_model
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.title("⚡ Analyse de volatilité énergétique (GARCH)- Par TENDRY")

os.makedirs("results", exist_ok=True)

# =========================
# SESSION STATE INIT
# =========================
if "df" not in st.session_state:
    st.session_state["df"] = None

if "result" not in st.session_state:
    st.session_state["result"] = None


# =========================
# FORMULAIRE
# =========================
st.sidebar.header("📊 Paramètres")

price0 = st.sidebar.number_input("Prix initial $", value=70.0)
vol = st.sidebar.slider("Volatilité", 0.005, 0.05, 0.015)
n = st.sidebar.slider("Jours", 200, 2000, 1000)
seed = st.sidebar.number_input("Seed", value=42)


# =========================
# ANALYSE
# =========================
if st.button("🚀 Lancer analyse"):

    np.random.seed(seed)

    returns = np.random.normal(0, vol, n)

    price = [price0]
    for r in returns:
        price.append(price[-1] * np.exp(r))

    price = price[1:]

    df = pd.DataFrame({"price": price})
    df["returns"] = df["price"].pct_change()

    model = arch_model(df["returns"].dropna(), vol="Garch", p=1, q=1)
    result = model.fit(disp="off")

    st.session_state["df"] = df
    st.session_state["result"] = result

    st.success("Analyse terminée ✔️")

df = st.session_state.get("df")
result = st.session_state.get("result")

if df is not None and result is not None:

    st.subheader("📈 Prix de l'énergie")
    fig, ax = plt.subplots()
    ax.plot(df["price"])
    st.pyplot(fig)

    st.subheader("📊 Volatilité GARCH")
    fig2, ax2 = plt.subplots()
    ax2.plot(result.conditional_volatility)
    st.pyplot(fig2)

    # =========================
    # INTERPRÉTATION TOUJOURS AFFICHÉE
    # =========================
    vol_moy = result.conditional_volatility.mean()

    st.subheader("🧠 Interprétation automatique")

    if vol_moy < 0.01:
        st.info("Marché très stable : faible volatilité.")
    elif vol_moy < 0.02:
        st.success("Marché normal : volatilité modérée.")
    else:
        st.warning("Marché instable : forte volatilité détectée.")

    st.write("📌 Analyse quantitative :")
    st.write(f"- Volatilité moyenne : {vol_moy:.4f}")
    st.write(f"- Prix final : {df['price'].iloc[-1]:.2f}")
    st.write(f"- Variation : {((df['price'].iloc[-1]/df['price'].iloc[0]) - 1)*100:.2f}%")


# =========================
# AFFICHAGE SI DONNÉES EXISTENT
# =========================
df = st.session_state["df"]
result = st.session_state["result"]

if df is not None and result is not None:

    st.subheader("📈 Prix")
    fig1, ax1 = plt.subplots()
    ax1.plot(df["price"])
    st.pyplot(fig1)

    st.subheader("📊 Volatilité GARCH")
    fig2, ax2 = plt.subplots()
    ax2.plot(result.conditional_volatility)
    st.pyplot(fig2)

    # INTERPRÉTATION
    vol_moy = result.conditional_volatility.mean()

    st.subheader("🧠 Interprétation")

    if vol_moy < 0.01:
        st.info("Marché stable")
    elif vol_moy < 0.02:
        st.success("Marché normal")
    else:
        st.warning("Marché instable")


# =========================
# PDF
# =========================
from io import BytesIO

def generate_pdf(vol_moy, last_price, variation):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Rapport GARCH - Énergie", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Volatilité moyenne : {vol_moy:.4f}", styles["Normal"]))
    content.append(Paragraph(f"Prix final : {last_price:.2f}", styles["Normal"]))
    content.append(Paragraph(f"Variation : {variation:.2f}%", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer


# =========================
# BOUTON DOWNLOAD
# =========================
df = st.session_state.get("df")
result = st.session_state.get("result")

if st.button("📄 Générer PDF"):

    if df is None or result is None:
        st.error("⚠️ Lance d'abord l'analyse")
    else:
        vol_moy = result.conditional_volatility.mean()
        last_price = df["price"].iloc[-1]
        variation = ((last_price / df["price"].iloc[0]) - 1) * 100

        pdf_buffer = generate_pdf(vol_moy, last_price, variation)

        st.download_button(
            label="📥 Télécharger rapport PDF",
            data=pdf_buffer,
            file_name="rapport_garch.pdf",
            mime="application/pdf"
        )