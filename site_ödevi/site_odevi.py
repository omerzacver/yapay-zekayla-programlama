import os
import re
import google.generativeai as genai

# 1. Gemini API Bağlantısı
API_KEY = "AQ.Ab8RN6JTee7eTRmra1gdVjZL1RswUkPhQez3yHu0et-9D2Liow"
genai.configure(api_key=API_KEY)

# Model yapılandırması (PDF yönergesine uygun parametreler)
model = genai.GenerativeModel(model_name="gemini-3.5-flash-lite")

# 2. Senin Hazırladığın Sistem Talimatı (System Prompt)
sistem_mesaji = """Sen kıdemli bir arayüz (UI/UX) ve ön yüz (Frontend) geliştiricisisin.
Kullanıcının tasarım talebine uygun, birbiriyle tutarlı karanlık temalı (Dark Mode), modern, mobil uyumlu (responsive) üç adet tam HTML sayfası üret.
Tüm CSS ve JavaScript kodlarını harici dosyalara bölmeden doğrudan ilgili HTML dosyalarının içine (<style> ve <script> etiketleriyle) göm.

Çıktı formatı için kesin kurallar:
1. Yanıtında yalnızca şu üç bölümü ve ayıraçları kullan; başında veya sonunda ekstra açıklama yazma:
===INDEX.HTML===
(buraya index.html kodunu yaz)
===FORGOT_PASSWORD.HTML===
(buraya forgot_password.html kodunu yaz)
===SIGNUP.HTML===
(buraya signup.html kodunu yaz)

2. Sayfalar arası bağlantılar (`href`) tam olarak `index.html`, `forgot_password.html` ve `signup.html` dosyalarına yönlensin.
3. Butonların üzerine gelindiğinde (`:hover`) belirgin parlama/ışık efekti oluştur.
4. JavaScript ile form gönderiminde (`submit`) boş alan kontrolü, geçerli e-posta formatı kontrolü ve şifre/şifre tekrar eşleşme kontrolü yap; şifre alanlarına göster/gizle butonu ekle.

Sayfa bileşenleri:
- `index.html`: E-posta alanı, şifre alanı (göster/gizle dahil), "Giriş Yap" butonu, "Şifremi Unuttum" bağlantısı (`forgot_password.html`) ve "Üye Ol" bağlantısı (`signup.html`).
- `forgot_password.html`: "Şifremi Unuttum" başlığı, e-posta adresi alanı, "Şifre sıfırlama bağlantısı gönder" butonu ve giriş sayfasına dön bağlantısı (`index.html`).
- `signup.html`: "Ad Soyad" alanı, e-posta alanı, şifre alanı (göster/gizle dahil), şifre tekrar alanı (göster/gizle dahil), "Üye Ol" butonu ve giriş sayfasına dön bağlantısı (`index.html`).
"""

# 3. Kullanıcıdan Tasarım Talebi Alma (Boş geçilirse PDF'teki örnek talep kullanılır)
varsayilan_talep = (
    "Modern, profesyonel, karanlık temalı bir üyelik sistemi oluştur. "
    "Mor ve mavi neon renkler kullan. Login, Forgot Password ve Signup sayfaları "
    "aynı tasarım dilini kullansın. Sayfalar arasında geçişler çalışsın. "
    "Butonların üzerine gelindiğinde parlama efekti oluşsun."
)

print("Web sitesi tasarım talebinizi girin (Varsayılan tasarım için direkt Enter'a basın):")
kullanici_girdisi = input("> ").strip()
tasarim_talebi = kullanici_girdisi if kullanici_girdisi else varsayilan_talep

print("\nGemini API'ye bağlanılıyor ve sayfalar üretiliyor, lütfen bekleyin...")

# 4. API İsteği Gönderme
tam_istek = f"{sistem_mesaji}\n\nKullanıcı talebi:\n{tasarim_talebi}"
response = model.generate_content(
    tam_istek,
    generation_config={
        "temperature": 0.5,
        "max_output_tokens": 16000
    }
)

sonuc = response.text

# 5. Çıktıyı Ayrıştırma (Parsing) ve Dosyalara Kaydetme
ayiraclar = [
    ("index.html", "===INDEX.HTML==="),
    ("forgot_password.html", "===FORGOT_PASSWORD.HTML==="),
    ("signup.html", "===SIGNUP.HTML===")
]

def temizle_html(ham_metin: str) -> str:
    # Olası ```html veya ``` markdown bloklarını temizler
    temiz = re.sub(r"^```html\s*", "", ham_metin.strip(), flags=re.IGNORECASE)
    temiz = re.sub(r"^```\s*", "", temiz)
    temiz = re.sub(r"\s*```$", "", temiz)
    return temiz.strip()

kaydedilen_sayisi = 0

for i, (dosya_adi, baslangic_etiketi) in enumerate(ayiraclar):
    if baslangic_etiketi not in sonuc:
        print(f"UYARI: '{baslangic_etiketi}' etiketi model yanıtında bulunamadı!")
        continue

    baslangic_idx = sonuc.index(baslangic_etiketi) + len(baslangic_etiketi)

    # Bir sonraki etiketin konumunu bul (son dosya ise metnin sonuna kadar al)
    if i + 1 < len(ayiraclar) and ayiraclar[i + 1][1] in sonuc:
        bitis_etiketi = ayiraclar[i + 1][1]
        bitis_idx = sonuc.index(bitis_etiketi)
        ham_html = sonuc[baslangic_idx:bitis_idx]
    else:
        ham_html = sonuc[baslangic_idx:]

    saf_html = temizle_html(ham_html)

    # UTF-8 kodlamasıyla kaydet
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        dosya.write(saf_html)

    print(f"[BAŞARILI] {dosya_adi} oluşturuldu ({len(saf_html)} karakter).")
    kaydedilen_sayisi += 1

if kaydedilen_sayisi == 3:
    print("\nTüm sayfalar eksiksiz oluşturuldu! Klasördeki 'index.html' dosyasına çift tıklayarak test edebilirsin.")
else:
    print("\nBazı dosyalar eksik oluştu. Ham çıktıyı kontrol etmek için 'ham_cikti.txt' kaydediliyor...")
    with open("ham_cikti.txt", "w", encoding="utf-8") as f:
        f.write(sonuc)