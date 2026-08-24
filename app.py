import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.special import comb

# Sayfa ayarlari
st.set_page_config(page_title="Olasilik & Simulasyon Paneli", layout="wide")

# Kenar menusu - mod secimi
st.sidebar.title("🎮 Oyun Secimi")
secilen_oyun = st.sidebar.radio("Mod:", ["🎰 Plinko (Galton Board)", "💣 Mines (Mayin Tarlasi)"])

# ==========================================
# 1. MOD: PLINKO SIMULASYONU
# ==========================================
if secilen_oyun == "🎰 Plinko (Galton Board)":
    st.title("🎰 Plinko / Galton Tahtasi Simulasyonu")
    st.write("Binom dagilimi ve Monte Carlo simülasyonu ile kasanin uzun vadeli kazancinin incelenmesi.")

    st.sidebar.subheader("Ayarlar")
    bakiye = st.sidebar.number_input("Baslangic Bakiyesi (TL)", value=500, step=50)
    bahis = st.sidebar.number_input("Tur Basi Bahis (TL)", value=10, step=1)
    tur_sayisi = st.sidebar.slider("Maksimum Tur Sayisi", min_value=10, max_value=300, value=100)
    oyuncu_sayisi = st.sidebar.slider("Simule Edilecek Kisi Sayisi", min_value=10, max_value=100, value=50)

    # 8 sira icin standart carpanlar
    carpanlar = [5.0, 1.0, 0.8, 0.5, 0.4, 0.6, 0.7, 1.5, 3.0]
    satir = 8

    # Olasilik hesabi: C(8, k) * (0.5^8)
    slotlar = np.arange(satir + 1)
    ihtimaller = [comb(satir, k) * (0.5 ** satir) for k in slotlar]
    
    # Kasa avantaji ve RTP hesabi
    rtp = sum(p * m for p, m in zip(ihtimaller, carpanlar)) * 100
    kasa_payi = 100.0 - rtp

    col1, col2 = st.columns(2)
    col1.metric("Teorik RTP (Geri Odeme)", f"%{rtp:.2f}")
    col2.metric("Kasa Avantaji (House Edge)", f"%{kasa_payi:.2f}", delta_color="inverse")

    st.subheader("📊 Slotlara Dusme Olasiliklari")
    
    # 1. Grafik: Slot Olasiliklari (Koyu antrasit zemin & Neon Mor/Yesil)
    fig1, ax1 = plt.subplots(figsize=(10, 3.8))
    fig1.patch.set_facecolor('#1E222D')
    ax1.set_facecolor('#1E222D')
    
    bar_kutulari = ax1.bar(slotlar, ihtimaller, color='#00E5FF', edgecolor='white', alpha=0.85)
    ax1.set_xlabel("Slot Pozisyonu (0: En Sol, 8: En Sag)", color='white', fontsize=10)
    ax1.set_ylabel("Olasilik", color='white', fontsize=10)
    ax1.tick_params(colors='white')
    ax1.set_xticks(slotlar)
    ax1.grid(axis='y', linestyle='--', alpha=0.2, color='white')

    for bar, mult in zip(bar_kutulari, carpanlar):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, h + 0.005, f"{mult}x", ha='center', va='bottom', color='#FFD700', fontsize=9, fontweight='bold')
    st.pyplot(fig1)

    st.subheader(f"📉 {oyuncu_sayisi} Kisinin Bakiye Grafigi (Monte Carlo)")
    
    # 2. Grafik: Plinko Bakiye Degisimi
    fig2, ax2 = plt.subplots(figsize=(10, 4.5))
    fig2.patch.set_facecolor('#1E222D')
    ax2.set_facecolor('#1E222D')

    tum_yollar = []
    batan_sayisi = 0

    for _ in range(oyuncu_sayisi):
        kullanici_bakiye = float(bakiye)
        gecmis = [kullanici_bakiye]
        
        for r in range(tur_sayisi):
            if kullanici_bakiye < bahis:
                batan_sayisi += 1
                gecmis.extend([kullanici_bakiye] * (tur_sayisi - r))
                break
            kullanici_bakiye -= bahis
            dusen_slot = np.random.binomial(satir, 0.5)
            kullanici_bakiye += bahis * carpanlar[dusen_slot]
            gecmis.append(kullanici_bakiye)
        
        tum_yollar.append(gecmis)
        ax2.plot(gecmis, color='#9E9E9E', alpha=0.2, linewidth=1)

    ortalama_yol = np.mean(tum_yollar, axis=0)
    ax2.plot(ortalama_yol, color='#00E676', linewidth=2.5, label='Ortalama Bakiye')
    ax2.axhline(y=bakiye, color='#FF5252', linestyle='--', linewidth=1.5, label='Baslangic Bakiyesi')
    ax2.set_xlabel("Oynanan Tur", color='white')
    ax2.set_ylabel("Bakiye (TL)", color='white')
    ax2.tick_params(colors='white')
    ax2.legend(loc='upper right', facecolor='#2C303E', edgecolor='none', labelcolor='white')
    ax2.grid(True, linestyle='--', alpha=0.2, color='white')
    st.pyplot(fig2)

    st.info(f"Simulasyon bitti: Toplam **{oyuncu_sayisi}** kisiden **{batan_sayisi}** tanesi sifirlandi.")

# ==========================================
# 2. MOD: MINES SIMULASYONU
# ==========================================
else:
    st.title("💣 Mines (Mayin Tarlasi) Katlama & Iflas Testi")
    st.write("5 mayinli tahtada 1000 TL'yi 2000 TL yapmaya calisan oyuncularin gercekci basari orani.")

    # Kombinasyon ve olasilik fonksiyonlari
    def kombinasyon(n, r):
        if r < 0 or r > n: return 0
        return math.comb(n, r)

    def sans_hesapla(adim, mayin=5):
        elmas = 25 - mayin
        if adim > elmas: return 0.0
        return kombinasyon(elmas, adim) / kombinasyon(25, adim)

    col_sol, col_sag = st.columns([1, 2])

    with col_sol:
        st.subheader("⚙️ Parametreler")
        baslangic = st.number_input("Baslangic Bakiyesi (TL)", value=1000, step=100)
        hedef = st.number_input("Hedef Bakiye (TL)", value=2000, step=100)
        bahis_miktari = st.selectbox("Tur Basi Bahis (TL)", [25, 50, 100, 200, 250, 500])
        hedef_kare = st.slider("Hangi Kutuda Cikilacak? (Adim)", min_value=1, max_value=8, value=3)
        kisi_sayisi = st.slider("Test Edilecek Kisi Sayisi", min_value=500, max_value=3000, value=1000, step=500)

        # Misli gercek carpanlari
        carpan_listesi = {1: 0.8124, 2: 1.024, 3: 1.312, 4: 1.708, 5: 2.260, 6: 3.05, 7: 4.20, 8: 6.00}
        carpan = carpan_listesi.get(hedef_kare, 1.0)
        tek_tur_sansi = sans_hesapla(hedef_kare, 5)

        st.warning(f"**{hedef_kare}. Kare Carpani:** {carpan}x\n\n**Kazanma Ihtimali:** %{tek_tur_sansi*100:.2f}")

    with col_sag:
        st.subheader("📈 Monte Carlo Bakiye Yollari")
        
        kazananlar = 0
        ornek_cizgiler = []

        for kisi in range(kisi_sayisi):
            bakiye_anlik = float(baslangic)
            yol = [bakiye_anlik]

            while bakiye_anlik >= bahis_miktari and bakiye_anlik < hedef and len(yol) < 250:
                bakiye_anlik -= bahis_miktari
                if np.random.rand() < tek_tur_sansi:
                    bakiye_anlik += bahis_miktari * carpan
                yol.append(bakiye_anlik)

            if bakiye_anlik >= hedef:
                kazananlar += 1
            if kisi < 35:
                ornek_cizgiler.append(yol)

        kazanma_yuzdesi = (kazananlar / kisi_sayisi) * 100
        batma_yuzdesi = 100.0 - kazanma_yuzdesi

        m1, m2 = st.columns(2)
        m1.metric(f"Hedefe Ulasan ({hedef} TL)", f"%{kazanma_yuzdesi:.1f}")
        m2.metric("Sifirlanan / Batan", f"%{batma_yuzdesi:.1f}", delta_color="inverse")

        # 3. Grafik: Mines Bakiye Yollari (Koyu antrasit & Parlak cizgiler)
        fig3, ax3 = plt.subplots(figsize=(9, 4.5))
        fig3.patch.set_facecolor('#1E222D')
        ax3.set_facecolor('#1E222D')

        renkler = ['#FFD54F', '#4FC3F7', '#BA68C8', '#4DB6AC', '#FF8A65']
        for idx, yol in enumerate(ornek_cizgiler):
            ax3.plot(yol, color=renkler[idx % len(renkler)], alpha=0.4, linewidth=1.2)

        ax3.axhline(hedef, color='#00E676', linestyle='--', linewidth=1.8, label=f"Hedef ({hedef} TL)")
        ax3.axhline(0, color='#FF5252', linestyle='--', linewidth=1.8, label="Iflas (0 TL)")
        ax3.set_xlabel("Oynanan Tur", color='white')
        ax3.set_ylabel("Bakiye (TL)", color='white')
        ax3.tick_params(colors='white')
        ax3.legend(loc='upper right', facecolor='#2C303E', edgecolor='none', labelcolor='white')
        ax3.grid(True, linestyle='--', alpha=0.2, color='white')
        st.pyplot(fig3)
