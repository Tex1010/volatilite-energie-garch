from matplotlib import pyplot as plt
import pandas as pd
from arch import arch_model

# Charger données
df = pd.read_csv("data/energy_data.csv")

# calcul returns
df["returns"] = df["price"].pct_change().dropna()

returns = df["returns"].dropna()

# modèle GARCH(1,1)
model = arch_model(returns, vol="Garch", p=1, q=1)

result = model.fit()

print(result.summary())

# =========================
# VOLATILITÉ GARCH
# =========================

plt.figure()
plt.plot(result.conditional_volatility)
plt.title("Volatilité estimée par GARCH(1,1)")
plt.show()