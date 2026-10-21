
import random
import time
import statistics


# ==================================================
# 1. 5000 KAYITLIK MUZIK VERI SETI OLUSTURMA
# ==================================================

def muzik_verisi_olustur(kayit_sayisi: int = 5000) -> list:
    random.seed(42)

    sarki_adlari = [
        "Blinding Lights",
        "Shape of You",
        "Dance Monkey",
        "Someone You Loved",
        "Perfect",
        "Believer",
        "Starboy",
        "Levitating",
        "As It Was",
        "Flowers",
        "Bad Guy",
        "Stay",
        "Despacito",
        "Watermelon Sugar",
        "Heat Waves",
        "Shallow",
        "Senorita",
        "Counting Stars",
        "Bohemian Rhapsody",
        "Smells Like Teen Spirit",
        "Lose Yourself",
        "Rolling in the Deep",
        "Hello",
        "Viva La Vida",
        "Take On Me",
        "Billie Jean",
        "Hotel California",
        "Imagine",
        "Wonderwall",
        "Yellow"
    ]

    sanatcilar = [
        "The Weeknd",
        "Ed Sheeran",
        "Tones and I",
        "Lewis Capaldi",
        "Ed Sheeran",
        "Imagine Dragons",
        "The Weeknd",
        "Dua Lipa",
        "Harry Styles",
        "Miley Cyrus",
        "Billie Eilish",
        "The Kid LAROI",
        "Luis Fonsi",
        "Harry Styles",
        "Glass Animals",
        "Lady Gaga",
        "Shawn Mendes",
        "OneRepublic",
        "Queen",
        "Nirvana",
        "Eminem",
        "Adele",
        "Adele",
        "Coldplay",
        "a-ha",
        "Michael Jackson",
        "Eagles",
        "John Lennon",
        "Oasis",
        "Coldplay"
    ]

    veriler = []

    for _ in range(kayit_sayisi):
        index = random.randint(0, len(sarki_adlari) - 1)

        sarki = {
            "sarki_adi": sarki_adlari[index],
            "sanatci": sanatcilar[index]
        }

        veriler.append(sarki)

    return veriler


# ==================================================
# 2. ESKI FONKSIYON: IC ICE DONGU
# ==================================================

def bul(veriler: list) -> list:
    sonuc = []

    for i in range(len(veriler)):
        for j in range(i + 1, len(veriler)):
            if veriler[i] == veriler[j] and veriler[i] not in sonuc:
                sonuc.append(veriler[i])

    return sonuc


# ==================================================
# 3. OPTIMIZE FONKSIYON: SET KULLANIMI
# ==================================================



def bul_optimize(veriler: list) -> list:
    son_gorulen = {}
    tekrarlar = set()

    for i, kayit in enumerate(veriler):
        anahtar = (
            kayit["sarki_adi"],
            kayit["sanatci"]
        )

        if anahtar in son_gorulen:
            tekrarlar.add(anahtar)
        else:
            son_gorulen[anahtar] = i

    sonuc = []
    eklenen = set()

    for kayit in veriler:
        anahtar = (
            kayit["sarki_adi"],
            kayit["sanatci"]
        )

        if anahtar in tekrarlar and anahtar not in eklenen:
            sonuc.append(kayit)
            eklenen.add(anahtar)

    return sonuc




# ==================================================
# 4. SURE OLCUM FONKSIYONU
# ==================================================

def sure_olc(fonksiyon, veriler: list, tekrar: int = 3) -> list:
    sureler = []

    for _ in range(tekrar):
        baslangic = time.perf_counter()
        fonksiyon(veriler)
        bitis = time.perf_counter()

        sureler.append(bitis - baslangic)

    return sureler


# ==================================================
# 5. DOGRULUK TESTLERI
# ==================================================

def dogruluk_testleri() -> bool:
    testler = [
        [],
        [{"sarki_adi": "A", "sanatci": "X"}],
        [
            {"sarki_adi": "A", "sanatci": "X"},
            {"sarki_adi": "B", "sanatci": "Y"},
            {"sarki_adi": "C", "sanatci": "Z"}
        ],
        [
            {"sarki_adi": "A", "sanatci": "X"},
            {"sarki_adi": "B", "sanatci": "Y"},
            {"sarki_adi": "A", "sanatci": "X"},
            {"sarki_adi": "C", "sanatci": "Z"},
            {"sarki_adi": "B", "sanatci": "Y"}
        ],
        [
            {"sarki_adi": "D", "sanatci": "W"},
            {"sarki_adi": "B", "sanatci": "Y"},
            {"sarki_adi": "B", "sanatci": "Y"},
            {"sarki_adi": "D", "sanatci": "W"},
            {"sarki_adi": "C", "sanatci": "Z"},
            {"sarki_adi": "C", "sanatci": "Z"}
        ]
    ]

    for veriler in testler:
        eski_sonuc = bul(veriler)
        yeni_sonuc = bul_optimize(veriler)

        assert eski_sonuc == yeni_sonuc, (
            f"Sonuclar eslesmedi! Veri: {veriler}"
        )

    print("Tum dogruluk testleri BASARILI.")
    return True


# ==================================================
# 6. ANA PROGRAM
# ==================================================

def main():
    print("=" * 55)
    print("MUZIK VERI SETI - KOD PERFORMANS LABORATUVARI")
    print("=" * 55)

    veriler = muzik_verisi_olustur(5000)

    print(f"Toplam muzik kaydi: {len(veriler)}")
    print("Sure olcumleri yapiliyor...")

    # Fonksiyonlarin ayni sonucu verdigini kontrol et
    sonuc_eski = bul(veriler)
    sonuc_yeni = bul_optimize(veriler)

    assert sonuc_eski == sonuc_yeni, (
        "Eski ve optimize fonksiyonlarin sonuclari farkli!"
    )

    print("5000 kayit icin sonuc karsilastirmasi BASARILI.")

    # En az 3 olcum
    eski_sureler = sure_olc(bul, veriler, 3)
    yeni_sureler = sure_olc(bul_optimize, veriler, 3)

    eski_ortalama = statistics.mean(eski_sureler)
    yeni_ortalama = statistics.mean(yeni_sureler)

    if yeni_ortalama > 0:
        hizlanma = eski_ortalama / yeni_ortalama
    else:
        hizlanma = 0

    # Dogruluk testleri
    test_durumu = dogruluk_testleri()

    # TXT raporunu olustur
    with open(
        "performans_raporu.txt",
        "w",
        encoding="utf-8"
    ) as dosya:

        dosya.write("KOD PERFORMANS RAPORU\n")
        dosya.write("=" * 40 + "\n")
        dosya.write("Proje: Muzik Veri Setinde Tekrar Analizi\n")
        dosya.write(f"Veri sayisi: {len(veriler)}\n\n")

        dosya.write("ESKI KOD SURELERI\n")
        for i, sure in enumerate(eski_sureler, start=1):
            dosya.write(f"{i}. olcum: {sure:.6f} saniye\n")

        dosya.write(
            f"Eski kod ortalama suresi: "
            f"{eski_ortalama:.6f} saniye\n\n"
        )

        dosya.write("OPTIMIZE KOD SURELERI\n")
        for i, sure in enumerate(yeni_sureler, start=1):
            dosya.write(f"{i}. olcum: {sure:.6f} saniye\n")

        dosya.write(
            f"Optimize kod ortalama suresi: "
            f"{yeni_ortalama:.6f} saniye\n"
        )

        dosya.write(f"Hizlanma: {hizlanma:.2f} kat\n")
        dosya.write(
            "Dogruluk testi: "
            + ("BASARILI" if test_durumu else "BASARISIZ")
            + "\n"
        )

        dosya.write("\nKISA YORUM:\n")

        if hizlanma > 1:
            dosya.write(
                "Optimize fonksiyon, ortalama olcumde daha hizli "
                "calismistir. Set kullanimi tekrar aramalarini "
                "azaltmistir.\n"
            )
        elif hizlanma > 0:
            dosya.write(
                "Bu olcumde optimize fonksiyon daha hizli cikmamistir. "
                "Sonuclar bilgisayar ve veri yapisina gore degisebilir.\n"
            )
        else:
            dosya.write(
                "Hizlanma hesaplanamadi; olcumleri kontrol edin.\n"
            )

        dosya.write(
            "Her iki fonksiyonun sonucunun ayni oldugu assert "
            "testleriyle kontrol edilmistir.\n"
        )

    print()
    print("-" * 55)
    print(f"Eski kod ortalamasi: {eski_ortalama:.6f} saniye")
    print(f"Yeni kod ortalamasi: {yeni_ortalama:.6f} saniye")
    print(f"Hizlanma: {hizlanma:.2f} kat")
    print("Dogruluk testi: BASARILI")
    print("Rapor kaydedildi: performans_raporu.txt")
    print("=" * 55)


if __name__ == "__main__":
    main()
