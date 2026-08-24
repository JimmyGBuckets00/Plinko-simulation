#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;

// Kombinasyon hesabi
long long kombinasyon(int n, int r) {
    if (r < 0 || r > n) return 0;
    if (r == 0 || r == n) return 1;
    if (r > n / 2) r = n - r;
    
    long long sonuc = 1;
    for (int i = 1; i <= r; i++) {
        sonuc = sonuc * (n - i + 1) / i;
    }
    return sonuc;
}

// 5 mayin (20 elmas) olan tahtada adim sayisina gore sans hesabi
double basari_ihtimali(int adim) {
    if (adim > 20) return 0.0;
    return (double)kombinasyon(20, adim) / kombinasyon(25, adim);
}

// Tek bir oyuncunun hedefe ulasip ulasmadigini simule eden fonksiyon
bool oyuncuyu_dene(double baslangic, double hedef, double bahis, double sans, double carpan, int &tur) {
    double bakiye = baslangic;
    tur = 0;

    while (bakiye >= bahis && bakiye < hedef) {
        tur++;
        bakiye -= bahis;
        
        double zar = (double)rand() / RAND_MAX;
        if (zar < sans) {
            bakiye += bahis * carpan;
        }
    }
    return (bakiye >= hedef);
}

int main() {
    srand(time(NULL));

    double baslangic = 1000.0;
    double hedef = 2000.0;
    int toplam_oyuncu = 10000;

    string isimler[3] = {
        "1. Taktik (200 TL Bahis - 3. Kare Cikis)",
        "2. Taktik (200 TL Bahis - 5. Kare Cikis)",
        "3. Taktik (100 TL Bahis - 4. Kare Cikis)"
    };
    
    double bahisler[3] = {200.0, 200.0, 100.0};
    int hedefler[3] = {3, 5, 4};
    double carpanlar[3] = {1.312, 2.260, 1.708};

    cout << fixed << setprecision(2);
    cout << "=== 1000 TL -> 2000 TL KATLAMA TESTI (10.000 Kisi) ===\n\n";

    for (int t = 0; t < 3; t++) {
        double sans = basari_ihtimali(hedefler[t]);
        int kazanan = 0;
        int toplam_tur = 0;

        for (int i = 0; i < toplam_oyuncu; i++) {
            int tur_sayisi = 0;
            if (oyuncuyu_dene(baslangic, hedef, bahisler[t], sans, carpanlar[t], tur_sayisi)) {
                kazanan++;
            }
            toplam_tur += tur_sayisi;
        }

        cout << isimler[t] << endl;
        cout << "  - Tek tur sansi      : %" << (sans * 100) << endl;
        cout << "  - 2000 TL yapanlar   : %" << ((double)kazanan / toplam_oyuncu) * 100 << " (" << kazanan << " kisi)" << endl;
        cout << "  - Batanlar           : %" << 100.0 - (((double)kazanan / toplam_oyuncu) * 100) << endl;
        cout << "  - Ort. oynanan tur   : " << (double)toplam_tur / toplam_oyuncu << " tur" << endl;
        cout << "--------------------------------------------------------" << endl;
    }

    system("pause");
    return 0;
}
