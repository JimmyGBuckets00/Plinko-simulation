import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import binom

st.set_page_config(page_title="Probability & Simulation Dashboard", layout="wide")

# Kenar Menüsü
st.sidebar.title("🎮 Simülasyon Seçimi")
game_mode = st.sidebar.radio("Oyun Modu:", ["🎰 Galton Board (Plinko)", "💣 Mines (Mayın Tarlası)"])

# ==========================================
# 1. MOD: PLINKO
# ==========================================
if game_mode == "🎰 Galton Board (Plinko)":
    st.title("🎰 Galton Board (Plinko) Simülasyonu & RTP Analizi")
    st.markdown("Binom Dağılımı ve Monte Carlo yöntemiyle bakiye erime analizi.")

    rows = 8
    p = 0.5
    multipliers = [13.0, 3.0, 1.3, 0.7, 0.4, 0.7, 1.3, 3.0, 13.0]
    probs = [binom.pmf(k, rows, p) for k in range(rows + 1)]
    theoretical_rtp = sum(prob * mult for prob, mult in zip(probs, multipliers)) * 100
    house_edge = 100 - theoretical_rtp

    col1, col2 = st.columns(2)
    col1.metric("Teorik RTP", f"%{theoretical_rtp:.2f}")
    col2.metric("Kasa Avantajı (House Edge)", f"%{house_edge:.2f}", delta_color="inverse")

    st.subheader("📊 Slot Olasılıkları")
    fig, ax = plt.subplots(figsize=(8, 3.5))
    slots = list(range(rows + 1))
    ax.bar(slots, probs, color="#4CAF50", edgecolor="black")
    ax.set_xlabel("Slot Numarası")
    ax.set_ylabel("Olasılık")
    ax.set_xticks(slots)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)

# ==========================================
# 2. MOD: MINES
# ==========================================
else:
    st.title("💣 Mines (Mayın Tarlası) Katlama & İflas Simülasyonu")
    st.markdown("Yerine koymasız seçim (**Hipergeometrik Dağılım**) ile 1000 TL'yi 2000 TL yapma analizi.")

    def kombinasyon(n, r):
        if r < 0 or r > n: return 0
        return math.comb(n, r)

    def basari_ihtimali(adim, mayin=5):
        elmas = 25 - mayin
        if adim > elmas: return 0.0
        return kombinasyon(elmas, adim) / kombinasyon(25, adim)

    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.subheader("⚙️ Parametreler")
        baslangic = st.number_input("Başlangıç Bakiyesi (TL)", value=1000, step=100)
        hedef = st.number_input("Hedef Bakiye (TL)", value=2000, step=100)
        bahis = st.selectbox("Tur Başı Bahis (TL)", [25, 50, 100, 200, 250])
        hedef_adim = st.slider("Hedef Çıkış Karesi (Adım)", min_value=1, max_value=8, value=3)
        sim_sayisi = st.slider("Simüle Edilecek Oyuncu", min_value=500, max_value=3000, value=1000, step=500)

        carpan_tablosu = {1: 0.8124, 2: 1.024, 3: 1.312, 4: 1.708, 5: 2.260, 6: 3.05, 7: 4.20, 8: 6.00}
        secilen_carpan = carpan_tablosu.get(hedef_adim, 1.0)
        sans = basari_ihtimali(hedef_adim, 5)

        st.info(f"**{hedef_adim}. Kare Çarpanı:** {secilen_carpan}x\n\n**Kazanma Şansı:** %{sans*100:.2f}")

    with col_b:
        st.subheader("📈 Monte Carlo Bakiye Yolları")
        
        kazananlar = 0
        ornek_yollar = []

        for p_idx in range(sim_sayisi):
            bakiye = float(baslangic)
            yol = [bakiye]
            while bakiye >= bahis and bakiye < hedef and len(yol) < 200:
                bakiye -= bahis
                if np.random.rand() < sans:
                    bakiye += bahis * secilen_carpan
                yol.append(bakiye)
            
            if bakiye >= hedef:
                kazananlar += 1
            if p_idx < 30:
                ornek_yollar.append(yol)

        kazanma_orani = (kazananlar / sim_sayisi) * 100
        batma_orani = 100 - kazanma_orani

        m1, m2 = st.columns(2)
        m1.metric("2000 TL Yapanlar", f"%{kazanma_orani:.1f}")
        m2.metric("Sıfırlanıp Batanlar", f"%{batma_orani:.1f}", delta_color="inverse")

        fig, ax = plt.subplots(figsize=(8, 4))
        for yol in ornek_yollar:
            ax.plot(yol, alpha=0.35, linewidth=1)
        
        ax.axhline(hedef, color="green", linestyle="--", label="Hedef (2000 TL)")
        ax.axhline(0, color="red", linestyle="--", label="İflas (0 TL)")
        ax.set_xlabel("Tur Sayısı")
        ax.set_ylabel("Bakiye (TL)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
