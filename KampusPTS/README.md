# Kampüs PTS — Gelir Yönetim Platformu

**Aşama:** P00 / Kurumsal Proje Temeli, Mimari Anayasa, Kanıt ve Karar Kayıtları  
**Hedef Backend:** ASP.NET Core / .NET 10 LTS (Modüler Monolit, C#)  
**Hedef Veritabanı:** PostgreSQL 16+ (EF Core, Mantıksal Şema İzolasyonu, Timestamptz UTC, Minor-Unit Para Birimi)  
**Hedef Web İstemcisi:** React + TypeScript (Tailwind CSS, Modüler Arayüz)  
**Mevcut Durum:** `G0 = NOT_APPROVED` | `P00_SOURCE_READY` | `CANLI DEĞİL / TASLAK`

---

## 1. Proje Amacı ve Kapsam

Kampüs PTS Gelir Yönetim Platformu; çoklu kampüs ve çoklu tüzel işletme yapısında:
- Plaka tanıma ve gözlem (`PlateObservation`)
- Çift döngü/sensör ile fiziksel geçiş kanıtı (`PassageEvidence`)
- Otopark mali oturumu yönetimi (`ParkingSession`)
- Abonelik ve tarife kuralları
- PSP üzerinden ödeme tahsilatı (sanal POS, QR, mobil)
- e-Fatura / e-Arşiv entegrasyonu
- PTS alt defteri (`Sub-ledger`) ve çift taraflı kayıt
- ERP muhasebe aktarımı ve mutabakat
- İstisna ve ihlal yönetimi

işlevlerini kurumsal güvenlik, denetlenebilirlik ve yüksek güvenilirlikle yönetmek üzere tasarlanan yeni nesil finansal gelir yönetim altyapısıdır.

---

## 2. P00 Aşama Sınırları ve Disiplini

Bu aşama **yalnızca P00** temelidir:
1. **İş Modülü Kodu Yoktur:** P00 kapsamında sahte CRUD kodları, mock ödeme ağ geçitleri veya sahte bariyer motorları üretilmez. Gerçek iş mantığı ve modül kodları P07 ve sonraki fazlarda adım adım inşa edilecektir.
2. **Referans Paketi Durumu:** Referans ZIP dosyası ortamda fiziksel olarak bulunmadığından dürüstlük ilkesi gereği **`REFERENCE_NOT_ACCESSIBLE`** olarak kaydedilmiştir; eksik bilgiler tahmin edilmemiş, prompt şartnamesindeki kesin kayıtlar (40 REQ, 16 NFR, 31 DEC, 15 RISK, 8 BLK, 10 TC, 56 Traceability, 10 Gates) kanonik olarak oluşturulmuştur.
3. **Önizleme Sınırı (`PREVIEW_ONLY`):** AI Studio çalışma ortamındaki React arayüzü yalnızca yönetişim, kayıt ve durum izleme amaçlı bir önizleme panelidir; gerçek bir .NET backend veya çalışan finansal motor değildir.
4. **Varsayılan Güvenli Yapılandırma:** Tüm dış entegrasyon ve operasyonel bayraklar (`enable_real_barrier_commands`, `enable_psp_live_capture`, `enable_einvoice_live_issuance`, `enable_erp_live_posting`) `false` olarak kilitlenmiştir.

---

## 3. Mimari Temel İlkeler

- **ASManager 6.3.0 Ayrılığı:** Fiziksel erişim haklarının tek otoritesi ASManager'dır. PTS veritabanına doğrudan SQL yazamaz.
- **Mali Hak ≠ Fiziksel Yetki:** `financial=ACTIVE` durumu `access=VERIFIED_ACTIVE` anlamına gelmez.
- **Gözlem ≠ Geçiş Kanıtı:** Kamera plaka okuması (`PLATE_RECOGNIZED`), fiziksel geçiş kanıtı (`PASSAGE_CONFIRMED`) ve bariyer teyidi (`GATE_ACK`) ayrı olgulardır.
- **Değişmez Alt Defter:** Kesinleşen kayıtlar silinemez, düzeltme ters kayıtla yapılır.
- **Epistemik Dürüstlük:** `UNKNOWN ≠ FALSE`, `DESIGNED ≠ TESTED`, `NOT_RUN ≠ PASS`.

---

## 4. Dizin Yapısı

```text
KampusPTS/
  AGENTS.md                         # Mimari Değişmezler A1-A10
  README.md                         # Proje Başlangıç ve Sınırlar
  Directory.Build.props             # .NET 10 LTS Yapılandırması
  .editorconfig                     # Kod Standartları
  .gitattributes / .gitignore       # Sürüm Kontrol Kuralları
  docs/
    charter.md                      # Proje Beratı ve Sınırlar
    financial-authority-matrix.md   # Mali Yetki Matrisi (DEC-001)
    governance/                     # K-01..K-12, Gates, RACI, Güvenlik
    architecture/                   # Mimari Genel Bakış, Event Envelope, ADR'lar
    registries/                     # REQ, NFR, DEC, RISK, BLK, TC, GATE CSV Kayıtları
    templates/                      # Standart Dokümantasyon Şablonları
    gates/                          # G0 ve G1 Kontrol Listeleri, Teslim Raporu
  config/
    features.example.json           # Güvenli Özellik Bayrakları (Hepsi False)
  tools/
    validate_p00.py                 # Otomatik P00 Doğrulama Motoru
    build_manifest.py               # SHA-256 Bütünlük Manifest Oluşturucu
  tests/
    test_validate_p00.py            # P00 Doğrulama Birim Testleri
  evidence/P00/                     # P00 Kanıt Deposu
  manifest.sha256                   # Kriptografik Dosya Bütünlük İmzaları
```

---

## 5. Doğrulama Komutları

```bash
# 1. P00 Kayıt ve Şema Doğrulaması
python3 tools/validate_p00.py

# 2. P00 Doğrulama Birim Testleri
python3 -m unittest tests.test_validate_p00 -v

# 3. SHA-256 Manifest Üretimi
python3 tools/build_manifest.py

# 4. JSON Format Doğrulaması
python3 -m json.tool config/features.example.json
python3 -m json.tool docs/architecture/event-envelope.schema.json
```

---

## 6. Gelecek Aşama Yol Haritası

- **P00:** Kurumsal Proje Temeli, Yönetişim ve Karar Kayıtları (MEVCUT AŞAMA - G0 NOT_APPROVED)
- **P01:** Saha Keşfi, Cihaz Envanteri ve ASManager Entegrasyon Sınırlarının Tespiti
- **P02–P06:** Sistem Tasarımı, Veri Modeli ve Güvenlik Altyapısı
- **P07+:** Modüler Monolit Çekirdek Uygulaması ve Domain Servisleri
