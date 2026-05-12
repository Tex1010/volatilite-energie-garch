# ⚡ Volatilité des flux commerciaux énergétiques (GARCH)

## 📌 Description du projet

Ce projet analyse la **volatilité des prix de l’énergie** en utilisant un modèle statistique avancé :  
👉 le **modèle GARCH (Generalized Autoregressive Conditional Heteroskedasticity)**.

L’objectif est de modéliser et comprendre la **volatilité des marchés énergétiques**, un élément clé en finance et en gestion des risques.

---

## 🎯 Objectifs

- Simuler des données de prix énergie
- Calculer les rendements financiers
- Analyser la volatilité des marchés
- Appliquer un modèle GARCH(1,1)
- Visualiser la volatilité conditionnelle

---

## 🛠️ Technologies utilisées

- Python
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- ARCH (GARCH model)

---

## 📊 Méthodologie

1. Génération / simulation des prix de l’énergie
2. Calcul des rendements logarithmiques
3. Analyse exploratoire des données
4. Modélisation avec GARCH(1,1)
5. Visualisation de la volatilité conditionnelle

---

## 📈 Résultats

Le modèle GARCH permet de :
- Capturer les périodes de forte volatilité
- Identifier les chocs de marché
- Modéliser le risque financier des actifs énergétiques

---

## 🚀 Exécution du projet

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le modèle
python src/train_garch.py

volatilite-energie-garch/
│
├── data/
├── notebooks/
├── src/
├── results/
├── requirements.txt
└── README.md