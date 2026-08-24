# 🎲 Olasılık ve Kumarhane Matematiği Simülasyonları

Olasılık teorisi, binom ve hipergeometrik dağılımların şans oyunlarındaki karşılığını görmek için yaptığım bir simülasyon projesi. 

Plinko ve Mayın Tarlası (Mines) oyunlarında kasanın uzun vadede nasıl para kazandığını ve oyuncuların neden battığını matematiksel olarak modelliyor.

🔗 **Canlı Proje Linki:** [plinko-simulation.streamlit.app](https://plinko-simulation.streamlit.app)

---

## 📌 Neler Var?

### 1. 🎰 Plinko (Galton Tahtası)
* 8 sıralı piramitte topların slotlara düşme ihtimalleri Binom Dağılımı ($n=8, p=0.5$) ile hesaplanıyor.
* Kasa avantajı (House Edge) ve oyuncuya geri dönüş (RTP) değerleri çıkartılıyor.
* Monte Carlo yöntemiyle aynı anda onlarca kişinin paralarının nasıl eridiği simüle ediliyor.

### 2. 💣 Mayın Tarlası (Mines) - 2x Katlama Testi
* 25 kutu ve 5 mayın olan tahtada yerine koymasız seçim (kombinasyon) ile adım adım hayatta kalma şansı hesaplanıyor.
* **Problem:** 1000 TL parayı 2000 TL yapmak için ufak ufak oynamak mı yoksa agresif vur-kaç yapmak mı daha mantıklı?
* Simülasyonda 10.000 oyuncu yarıştırılıyor ve Dubins-Savage (Bold Play) kuralının pratikteki sonucu test ediliyor.

---

## 🛠️ Kullandığım Şeyler

* **Diller:** Python, C++
* **Arayüz:** Streamlit
* **Kütüphaneler:** NumPy, SciPy, Matplotlib, Pandas
* **Ortam:** Dev-C++, VS Code

---

## 💻 C++ Kodunu Çalıştırma

Mines simülasyonunun 10.000 kişilik C++ konsol kodunu Dev-C++'ta açıp `F11` ile çalıştırabilir ya da terminalden derleyebilirsiniz:

```bash
g++ mines_simulation.cpp -o mines
./mines
