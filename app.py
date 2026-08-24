import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import comb

# Sayfa basligi
st.set_page_config(page_title="Olasilik Simulasyon Projesi", layout="wide")

st.sidebar.title("Menü")
secim = st.sidebar.radio("Oyun Sec:", ["Plinko (Galton)", "Mines (Mayin Tarlasi)"])

# -------------------------------------------------------------
# 1. PLINKO KISMI
# -------------------------------------------------------------
if secim == "Plinko (Galton)":
    st.title("Plinko / Galton Tahtasi Deneyi")
    st.write("Binom dagilimi kullanarak topun dusme olasiliklarini ve kasa kayip oranini hesaplar.")

    st.sidebar.subheader("Parametreler")
    para = st.sidebar.number_input("Baslangic Parasi", value=500, step=50)
    bahis = st.sidebar.number_input("Bahis Miktari", value=10, step=1)
    tur = st.sidebar.slider("Kac Tur Oynansin?", 10, 300, 100)
    kisi = st.sidebar.slider("Kac Kisi Oynasin?", 10, 100, 50)

    # 8 sira icin carpanlar
    carpanlar = [5.0, 1.0, 0.8, 0.5, 0.4, 0.6, 0.7, 1.5, 3.0]
    n = 8

    # Olasilik hesabi: C(8, k) * (0.5^8)
    slotlar = list(range(n + 1))
    ihtimaller = []
    for k in slotlar:
        p = comb(n, k) * (0.5 ** n)
        ihtimaller.append(p)

    # RTP ve House edge hesabi
    toplam_beklenti = 0
    for i in range(len(slotlar)):
        toplam_beklenti += ihtimaller[i] * carpanlar[i]
    
    rtp = toplam_beklenti * 100
    kasa_avantaji = 100.0 - rtp

    col1, col2 = st.columns(2)
    col1.metric("Teorik RTP", f"%{rtp:.2f}")
    col2.metric("Kasa Payi", f"%{kasa_avantaji:.2f}")

    # Grafik 1 - Cubuk Grafigi
    st.subheader("Slotlara Dusme Sanslari")
    fig1, ax1 = plt.subplots(figsize=(9, 3.5))
    ax1.bar(slotlar, ihtimaller, color='cyan', edgecolor='black')
    ax1.set_xlabel("Slotlar (0-8)")
    ax1.set_ylabel("Olasilik")
    ax1.set_xticks(slotlar)
    ax1.grid(True, linestyle='--', alpha=0.3)

    for i in range(len(slotlar)):
        ax1.text(slotlar[i], ihtimaller[i] + 0.005, f"{carpanlar[i]}x", ha='center', fontsize=8)
    st.pyplot(fig1)

    # Monte Carlo Simulasyonu
    st.subheader(f"{kisi} Farkli Kisinin Bakiye Grafigi")
    fig2, ax2 = plt.subplots(figsize=(9, 4))

    hepsi = []
    batan_sayisi = 0

    for _ in range(kisi):
        bakiye = float(para)
        gecmis = [bakiye]
        for t in range(tur):
            if bakiye < bahis:
                batan_sayisi += 1
                # parasi bitince sabit kalsin
                gecmis.extend([bakiye] * (tur - t))
                break
            bakiye -= bahis
            slot = np.random.binomial(n, 0.5)
            kazanc = bahis * carpanlar[slot]
            bakiye += kazanc
            gecmis.append(bakiye)
        
        hepsi.append(gecmis)
        ax2.plot(gecmis, color='gray', alpha=0.3)

    ortalamalar = np.mean(hepsi, axis=0)
    ax2.plot(ortalamalar, color='green', linewidth=2, label="Ortalama Bakiye")
    ax2.axhline(para, color='red', linestyle='--', label="Baslangic")
    ax2.set_xlabel("Tur")
    ax2.set_ylabel("TL")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig2)

    st.write(f"Sonuc: {kisi} kisiden {batan_sayisi} tanesi tamamen sifirlandi.")

# -------------------------------------------------------------
# 2. MINES KISMI
# -------------------------------------------------------------
else:
    st.title("Mayin Tarlasi (Mines) 2x Katlama Testi")
    st.write("Amac: 1000 TL parayi 2000 TL yapmaya calismak. Farkli taktikler deneniyor.")

    # Permutasyon/Kombinasyon ile hipergeometrik olasilik
    def sans_bul(adim):
        if adim > 20:
            return 0.0
        return comb(20, adim) / comb(25, adim)

    # Misli gercek carpan degerleri
    carpan_sozluk = {1: 0.8124, 2: 1.024, 3: 1.312, 4: 1.708, 5: 2.260, 6: 3.05, 7: 4.20, 8: 6.00}

    st.sidebar.subheader("Taktik Sablonu")
    taktik = st.sidebar.selectbox("Taktik Sec:", [
        "Taktik 1: 200 TL Bahis - 3. Kare (1.31x)",
        "Taktik 2: 200 TL Bahis - 5. Kare (2.26x)",
        "Taktik 3: 100 TL Bahis - 4. Kare (1.71x)",
        "Taktik 4: 25 TL Bahis - 3. Kare (Yavas Oyun)",
        "Manuel Ayar"
    ])

    if "Taktik 1" in taktik:
        varsayilan_bahis, varsayilan_kare = 200, 3
    elif "Taktik 2" in taktik:
        varsayilan_bahis, varsayilan_kare = 200, 5
    elif "Taktik 3" in taktik:
        varsayilan_bahis, varsayilan_kare = 100, 4
    elif "Taktik 4" in taktik:
        varsayilan_bahis, varsayilan_kare = 25, 3
    else:
        varsayilan_bahis, varsayilan_kare = 200, 3

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Girdiler")
        ana_para = st.number_input("Baslangic Parasi", value=1000, step=100)
        hedef_para = st.number_input("Hedef Para", value=2000, step=100)
        
        bahis_listesi = [25, 50, 100, 200, 250, 500]
        bahis_index = bahis_listesi.index(varsayilan_bahis) if varsayilan_bahis in bahis_listesi else 3
        secilen_bahis = st.selectbox("Tur Basi Bahis", bahis_listesi, index=bahis_index)
        
        secilen_kare = st.slider("Kacinci Karede Cekilecek?", 1, 8, varsayilan_kare)
        sim_kisi = st.slider("Test Edilecek Oyuncu", 500, 3000, 1000, step=500)

        carpan = carpan_sozluk.get(secilen_kare, 1.0)
        tur_sansi = sans_bul(secilen_kare)

        st.info(f"Secilen Adim: {secilen_kare}. Kare\n\nCarpan: {carpan}x\n\nTek Tur Kazanma Sansi: %{tur_sansi*100:.2f}")

    with col2:
        st.subheader("Simulasyon Sonuclari")
        
        kazananlar = 0
        ornek_yollar = []

        for p in range(sim_kisi):
            bakiye = float(ana_para)
            yol = [bakiye]

            while bakiye >= secilen_bahis and bakiye < hedef_para and len(yol) < 250:
                bakiye -= secilen_bahis
                # Rastgele zar
                if np.random.rand() < tur_sansi:
                    bakiye += secilen_bahis * carpan
                yol.append(bakiye)

            if bakiye >= hedef_para:
                kazananlar += 1
            if p < 30:
                ornek_yollar.append(yol)

        basari_yuzdesi = (kazananlar / sim_kisi) * 100
        batis_yuzdesi = 100.0 - basari_yuzdesi

        m1, m2 = st.columns(2)
        m1.metric("2000 TL Yapanlar", f"%{basari_yuzdesi:.1f}")
        m2.metric("Batanlar", f"%{batis_yuzdesi:.1f}")

        # Grafik
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        for yol in ornek_yollar:
            ax3.plot(yol, alpha=0.4)

        ax3.axhline(hedef_para, color='green', linestyle='--', label="Hedef (2000 TL)")
        ax3.axhline(0, color='red', linestyle='--', label="Iflas (0 TL)")
        ax3.set_xlabel("Tur Sayisi")
        ax3.set_ylabel("Bakiye")
        ax3.legend()
        ax3.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig3)

    # Genel Karsilastirma Tablosu
    st.subheader("Strateji Karsilastirmasi (Ozet)")
    tablo_bilgi = {
        "Taktik": [
            "25 TL Bahis - 3. Kare (Kucuk Oynama)",
            "100 TL Bahis - 4. Kare (10 Hak)",
            "200 TL Bahis - 3. Kare (Orta Risk)",
            "200 TL Bahis - 5. Kare (Agresif)",
            "500 TL Bahis - 5. Kare (Hizli)"
        ],
        "Bahis": ["25 TL", "100 TL", "200 TL", "200 TL", "500 TL"],
        "Hedef Adim": ["3. Kare", "4. Kare", "3. Kare", "5. Kare", "5. Kare"],
        "2000 TL Olma Sansi": ["%0.0 (Imkansiz)", "%0.1 - %0.5", "%0.0 - %0.2", "%4.0 - %6.0", "%18.0 - %22.0"],
        "Ort. Tur Sayisi": ["~150 Tur", "~30 Tur", "~15 Tur", "~12 Tur", "~3-4 Tur"],
        "Aciklama": ["Kasa payi parayi yutar", "Riskli", "Carpan kurtarmiyor", "Kisa vadeli sans", "En mantikli agresif taktik"]
    }
    st.table(pd.DataFrame(tablo_bilgi))
