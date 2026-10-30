# Kalite Puan Kartı ve Ölçütler (Quality Scorecard)

**Aşama:** P00  
**Hedef Kriter:** %100 Yapısal Bütünlük, Doğrulanmış Kayıt Sayımları, Dürüst Durum Raporlaması

---

## 1. P00 Kalite Metrikleri

| Metrik Alanı | Hedef Değer | P00 Gerçekleşen Değer | Durum |
|:---|:---:|:---:|:---:|
| **Zorunlu Dosya Bütünlüğü** | Eksiksiz ağaç | 100% Eksiksiz | PASS |
| **Gereksinim Sayımı (REQ)** | 40 tekil kayıt | 40 kayıt | PASS |
| **Fonksiyonel Olmayan Gereksinim (NFR)** | 16 tekil kayıt | 16 kayıt | PASS |
| **Karar Kayıtları (DEC)** | 31 kayıt (tümü DECISION_REQUIRED) | 31 kayıt | PASS |
| **Risk Kayıtları (RISK)** | 15 kayıt | 15 kayıt | PASS |
| **Açık Blokajlar (BLK)** | 8 kayıt (tümü OPEN) | 8 kayıt | PASS |
| **Test Senaryoları (TC)** | 10 kayıt (tümü NOT_RUN) | 10 kayıt | PASS |
| **İzlenebilirlik Satırları** | 56 bağımsız kayıt | 56 kayıt | PASS |
| **Yönetişim Kapıları (GATE)** | 10 kapı (G0=NOT_APPROVED) | 10 kapı | PASS |
| **Özellik Bayrakları Güvenliği** | Tüm canlı bayraklar `false` | Tüm canlı bayraklar `false` | PASS |
| **Kriptografik Bütünlük** | SHA-256 Manifest doğrulaması | Üretildi ve Doğrulandı | PASS |

---

## 2. Epistemik Dürüstlük Kuralı
P00 aşamasında testler koşulmadığı için hiçbir işlevsel test sonucu "PASS" ilan edilmemiştir. P00 doğrulaması salt statik yapısal ve kütük bütünlüğü testidir.
