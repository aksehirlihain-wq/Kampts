# Kampüs PTS Proje Kütükleri (Registries)

Bu dizin, Kampüs PTS Gelir Yönetim Platformu'nun tüm resmi gereksinim, karar, risk, blokaj, test ve izlenebilirlik kütüklerini içerir.

## Kütük Dosyaları ve Sayım Kuralları

| Dosya Adı | Açıklama | Kayıt Sayısı | Durum Kuralı |
|:---|:---|:---:|:---|
| `requirements.csv` | Fonksiyonel İş Gereksinimleri | **40** (REQ-001..REQ-040) | Dondurulmuş / P00 |
| `nfr.csv` | Fonksiyonel Olmayan Gereksinimler | **16** (NFR-001..NFR-016) | Dondurulmuş / P00 |
| `decisions.csv` | Kurumsal Karar Kütüğü | **31** (DEC-001..DEC-031) | Tümü `DECISION_REQUIRED` |
| `risks.csv` | Risk Kayıtları ve Değerlendirmeleri | **15** (RISK-001..RISK-015) | İzleme Altında |
| `blockers.csv` | Açık Mimari ve Kurumsal Blokajlar | **8** (BLK-001..BLK-008) | Tümü `OPEN` |
| `traceability.csv` | Uçtan Uca İzlenebilirlik Matrisi | **56** (40 REQ + 16 NFR) | Gerçek EVD yoksa `NONE` |
| `test-cases.csv` | Tasarlanmış Test Senaryoları | **10** (TC-001..TC-010) | Tümü `NOT_RUN` |
| `gates.csv` | Kalite ve Aşama Kapıları | **10** (G0..G9) | G0: `NOT_APPROVED`, G1-G9: `NOT_STARTED` |

### Bütünlük Kuralları:
1. Kayıt ID'leri ve kolon başlıkları asla değiştirilemez.
2. Excel uyumluluğu için UTF-8 kodlaması korunur.
3. Gerçek kanıtı (`EVD`) olmayan hiçbir test `PASS` olarak işaretlenemez.
