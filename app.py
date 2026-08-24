import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.special import comb
from scipy.stats import binom

# Sayfa Yapılandırması
st.set_page_config(page_title="Probability & Casino Math Simulator", layout="wide", initial_sidebar_state="expanded")

# Koyu Tema Grafik Stili
plt.style.use('dark_background')

# Kenar Menüsü
st.sidebar.title("🎮 Oyun Seçimi")
game_mode = st.sidebar.radio("Analiz Edilecek Mod:", ["🎰 Galton Board (Plinko)", "💣 Mines (Mayın Tarlası)"])

# ==========================================
# 1. MOD: PLINKO SIMULASYONU
# ==========================================
if game_mode == "🎰 Galton Board (Plinko)":
    st.title("🎰 Galton Board (Plinko) Simülasyonu & RTP Analizi")
    st.markdown("Binom Dağılımı ve Monte Carlo yöntemiyle bakiye erime ve varyans analizi.")

    st.sidebar.header("⚙️ Plinko Parametreleri")
    initial_balance = st.sidebar.number_input("Başlangıç Bakiyesi (TL)", min_value=50, max_value=10000, value=500, step=50)
    bet_amount = st.sidebar.number_input("Tur Başına Bahis (TL)", min_value=1, max_value=500, value=10, step=1)
    max_rounds = st.sidebar.slider("Maksimum Tur Sayısı", min_value=10, max_value=500, value=100)
    num_players = st.sidebar.slider("Simüle Edilecek Oyuncu Sayısı", min_value=10, max_value=100, value=50, step=10)

    multipliers = np.array([5.0, 1.0, 0.8, 0.5, 0.4, 0.6, 0.7, 1.5, 3.0])
    rows = 8

    k_values = np.arange(rows + 1)
    probabilities = comb(rows, k_values) * (0.5 ** rows)
    expected_multiplier = np.sum(probabilities * multipliers)
    rtp = expected_multiplier * 100
    house_edge = 100 - rtp

    col1, col2 = st.columns(2)
    col1.metric(label="Teorik RTP (Oyuncuya Dönüş)", value=f"%{rtp:.2f}")
    col2.metric(label="Kasa Avantajı (House Edge)", value=f"%{house_edge:.2f}", delta_color="inverse")

    st.subheader("📊 8 Sıralı Piramit Olasılık Dağılımı")
    fig_prob, ax_prob = plt.subplots(figsize=(10, 3.5))
    fig_prob.patch.set_alpha(0.0)
    ax_prob.patch.set_alpha(0.0)
    
    bars = ax_prob.bar(k_values, probabilities, color='#00E676', edgecolor='white', alpha=0.85)
    ax_prob.set_xlabel("Slot Pozisyonu (0 = En Sol, 8 = En Sağ)")
    ax_prob.set_ylabel("Düşme Olasılığı")
    ax_prob.set_xticks(k_values)
    ax_prob.grid(axis='y', linestyle='--', alpha=0.3)

    for bar, mult in zip(bars, multipliers):
        yval = bar.get_height()
        ax_prob.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f"{mult}x", ha='center', va='bottom', fontsize=8, color='white', fontweight='bold')
    st.pyplot(fig_prob)

    st.subheader(f"📉 {num_players} Farklı Oyuncunun Bakiye Değişimi (Monte Carlo)")
    all_player_histories = []
    ruin_count = 0

    fig_sim, ax_sim = plt.subplots(figsize=(10, 4.5))
    fig_sim.patch.set_alpha(0.0)
    ax_sim.patch.set_alpha(0.0)

    for _ in range(num_players):
        balance = initial_balance
        history = [balance]
        for r in range(max_rounds):
            if balance < bet_amount:
                ruin_count += 1
                history.extend([balance] * (max_rounds - r))
                break
            balance -= bet_amount
            landed_slot = np.random.binomial(rows, 0.5)
            gain = bet_amount * multipliers[landed_slot]
            balance += gain
            history.append(balance)
        all_player_histories.append(history)
        ax_sim.plot(history, color='#90A4AE', alpha=0.25, linewidth=1)

    avg_history = np.mean(all_player_histories, axis=0)
    ax_sim.plot(avg_history, color='#29B6F6', linewidth=2.5, label='Ortalama Bakiye')
    ax_sim.axhline(y=initial_balance, color='#EF5350', linestyle='--', linewidth=1.5, label='Başlangıç Noktası')
    ax_sim.set_xlabel("Oynanan Tur Sayısı")
    ax_sim.set_ylabel("Bakiye (TL)")
    ax_sim.legend(loc='upper right')
    ax_sim.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig_sim)

    st.info(f"Simülasyon Çıktısı: Toplam **{num_players}** oyuncudan **{ruin_count}** tanesi tur bitmeden bakiyesini tüketti.")

# ==========================================
# 2. MOD: MINES (MAYIN TARLASI)
# ==========================================
else:
    st.title("💣 Mines (Mayın Tarlası) Katlama & İflas Simülasyonu")
    st.markdown("Yerine koymasız seçim (**Hipergeometrik Dağılım**) ile sermaye katlama analizi.")

    def kombinasyon_hesapla(n, r):
        if r < 0 or r > n: return 0
        return math.comb(n, r)

    def basari_ihtimali(adim, mayin=5):
        elmas = 25 - mayin
        if adim > elmas: return 0.0
        return kombinasyon_hesapla(elmas, adim) / kombinasyon_hesapla(25, adim)

    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.subheader("⚙️ Mines Parametreleri")
        baslangic = st.number_input("Başlangıç Bakiyesi (TL)", value=1000, step=100)
        hedef = st.number_input("Hedef Bakiye (TL)", value=2000, step=100)
        bahis = st.selectbox("Tur Başı Bahis (TL)", [25, 50, 100, 200, 250, 500])
        hedef_adim = st.slider("Hedef Çıkış Karesi (Adım)", min_value=1, max_value=8, value=3)
        sim_sayisi = st.slider("Simüle Edilecek Oyuncu Sayısı", min_value=500, max_value=3000, value=1000, step=500)

        carpan_tablosu = {1: 0.8124, 2: 1.024, 3: 1.312, 4: 1.708, 5: 2.260, 6: 3.05, 7: 4.20, 8: 6.00}
        secilen_carpan = carpan_tablosu.get(hedef_adim, 1.0)
        sans = basari_ihtimali(hedef_adim, 5)

        st.info(f"**{hedef_adim}. Kare Çarpanı:** {secilen_carpan}x\n\n**Tek Tur Başarı Şansı:** %{sans*100:.2f}")

    with col_b:
        st.subheader("📈 Monte Carlo Bakiye Yolları")
        
        kazananlar = 0
        ornek_yollar = []

        for p_idx in range(sim_sayisi):
            bakiye = float(baslangic)
            yol = [bakiye]
            while bakiye >= bahis and bakiye < hedef and len(yol) < 250:
                bakiye -= bahis
                if np.random.rand() < sans:
                    bakiye += bahis * secilen_carpan
                yol.append(bakiye)
            
            if bakiye >= hedef:
                kazananlar += 1
            if p_idx < 35:
                ornek_yollar.append(yol)

        kazanma_orani = (kazananlar / sim_sayisi) * 100
        batma_orani = 100 - kazanma_orani

        m1, m2 = st.columns(2)
        m1.metric(f"Hedefe Ulaşan ({hedef} TL)", f"%{kazanma_orani:.1f}")
        m2.metric("Sıfırlanıp Batanlar", f"%{batma_orani:.1f}", delta_color="inverse")

        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        for yol in ornek_yollar:
            ax.plot(yol, alpha=0.35, linewidth=1)
        
        ax.axhline(hedef, color="#00E676", linestyle="--", linewidth=1.5, label=f"Hedef ({hedef} TL)")
        ax.axhline(0, color="#EF5350", linestyle="--", linewidth=1.5, label="İflas (0 TL)")
        ax.set_xlabel("Oynanan Tur")
        ax.set_ylabel("Bakiye (TL)")
        ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
