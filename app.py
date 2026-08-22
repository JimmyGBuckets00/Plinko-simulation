import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

st.set_page_config(page_title="Galton / Plinko Simülatörü", layout="wide")

st.title("🎰 Plinko / Galton Tahtası Simülasyonu & RTP Analizi")
st.markdown("Bu panel, olasılık dağılımı ve kasa avantajının (House Edge) bakiye üzerindeki uzun vadeli etkisini modeller.")

# Yan Panel - Parametreler
st.sidebar.header("Oyun Parametreleri")
initial_balance = st.sidebar.number_input("Başlangıç Bakiyesi (TL)", min_value=50, max_value=10000, value=500, step=50)
bet_amount = st.sidebar.number_input("Tur Başına Bahis (TL)", min_value=1, max_value=500, value=10, step=1)
max_rounds = st.sidebar.slider("Maksimum Tur Sayısı", min_value=10, max_value=500, value=100)
num_players = st.sidebar.slider("Simüle Edilecek Oyuncu Sayısı", min_value=10, max_value=100, value=50, step=10)

# 8 Satır Düşük Risk Çarpanları
multipliers = np.array([5.0, 1.0, 0.8, 0.5, 0.4, 0.6, 0.7, 1.5, 3.0])
rows = 8

# Binom Olasılıkları ve RTP Hesabı
k_values = np.arange(rows + 1)
probabilities = comb(rows, k_values) * (0.5 ** rows)
rtp = np.sum(probabilities * multipliers) * 100
house_edge = 100 - rtp

# Metrik Kartları
col1, col2, col3 = st.columns(3)
col1.metric("Teorik RTP", f"%{rtp:.2f}")
col2.metric("Kasa Avantajı (House Edge)", f"%{house_edge:.2f}")
col3.metric("Satır Sayısı", f"{rows} Satır")

# Monte Carlo Simülasyon Fonksiyonu
def run_simulation(start_bal, bet, rounds):
    balance = start_bal
    history = [balance]
    for _ in range(rounds):
        if balance < bet:
            break
        slot = np.random.binomial(rows, 0.5)
        balance = balance - bet + (bet * multipliers[slot])
        history.append(balance)
    return history

# Grafikler
st.subheader(f"Bakiye Değişim Eğrileri ({num_players} Oyuncu Monte Carlo Koridoru)")
fig, ax = plt.subplots(figsize=(10, 4))
for i in range(num_players):
    history = run_simulation(initial_balance, bet_amount, max_rounds)
    ax.plot(history, color="#1f77b4", alpha=0.25)

ax.axhline(initial_balance, color="red", linestyle="--", linewidth=1.5, label=f"Başlangıç ({initial_balance} TL)")
ax.set_xlabel("Oynanan Tur")
ax.set_ylabel("Bakiye (TL)")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

# Olasılık Dağılım Grafiği
st.subheader("Deliklere Düşme Olasılık Dağılımı (Binom)")
fig2, ax2 = plt.subplots(figsize=(10, 3))
delik_isimleri = [f"{m}x" for m in multipliers]
ax2.bar(delik_isimleri, probabilities * 100, color="skyblue", edgecolor="black")
ax2.set_ylabel("Olasılık (%)")
ax2.set_xlabel("Çarpan Delikleri")
st.pyplot(fig2)
