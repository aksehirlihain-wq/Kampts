# G0 Kapı Kontrol Listesi (G0 Governance Gate Checklist)

**Aşama:** P00 (Kurumsal Proje Temeli, Mimari Anayasa, Kanıt ve Karar Kayıtları)  
**Tarih:** 2026-10-30  
**Değerlendiren:** Kıdemli Çözüm Mimarı  
**Kapı Kararı:** **`NOT_APPROVED`** (G0 Onayı Verilmemiştir)  
**NO-GO Gerekçesi:** Kurumsal imza sirküleri, DEC-001 mali model kararı ve 8 açık kurumsal blokaj (BLK-001..BLK-008) henüz yetkili makamlarca onaylanmamıştır.

---

## 1. Mimari ve Anayasal Kriterler

| No | Kriter | Hedef Standart | Gerçek Durum | Sonuç |
|:---:|:---|:---|:---|:---:|
| 1 | Referans ve bağlamın doğrulanması | Referans paketi kontrolü | `REFERENCE_NOT_ACCESSIBLE` (Paket bulunamadı, şartnamedeki kesin kayıtlar üretildi) | TO_VERIFY |
| 2 | A1–A10 ve K-01–K-12 bütünlüğü | AGENTS.md ve foundational-invariants.md | Eksiksiz ve çelişkisiz bağlandı | PASS |
| 3 | Hedef teknoloji yığını netliği | .NET 10 LTS + PostgreSQL 16+ + React/TS | Modüler Monolit ve EF Core sabitlendi | PASS |
| 4 | ASManager fiziksel yetki yalıtımı | Doğrudan DB yazma yasağı (K-03) | Mimari sınır ve port kuralı tanımlandı | PASS |
| 5 | Gözlem ve kesin geçiş ayrımı | PLATE_RECOGNIZED vs PASSAGE_CONFIRMED | Nesne ve durum ayrımı yapıldı | PASS |
| 6 | Mali hak ve fiziksel erişim ayrımı | financial=ACTIVE vs access=VERIFIED_ACTIVE | İki durumun bağımsızlığı sabitlendi | PASS |
| 7 | Alt defter çift taraflı kayıt kuralı | POSTED silinemez, yalnız ters kayıt | Alt defter modeli ve ADR-003 onaylandı | PASS |

---

## 2. Kütük ve Sayım Bütünlüğü Kriterleri

| No | Kriter | Beklenen Sayı | Gerçekleşen Sayı | Durum |
|:---:|:---|:---:|:---:|:---:|
| 8 | Fonksiyonel Gereksinimler (requirements.csv) | 40 (REQ-001..040) | 40 tekil kayıt | PASS |
| 9 | Fonksiyonel Olmayan Gereksinimler (nfr.csv) | 16 (NFR-001..016) | 16 tekil kayıt | PASS |
| 10 | Karar Kayıtları (decisions.csv) | 31 (DEC-001..031) | 31 kayıt (Tümü DECISION_REQUIRED) | PASS |
| 11 | Risk Kayıtları (risks.csv) | 15 (RISK-001..015) | 15 kayıt | PASS |
| 12 | Açık Blokajlar (blockers.csv) | 8 (BLK-001..008) | 8 kayıt (Tümü OPEN) | PASS |
| 13 | Test Senaryoları (test-cases.csv) | 10 (TC-001..010) | 10 kayıt (Tümü NOT_RUN) | PASS |
| 14 | Uçtan Uca İzlenebilirlik (traceability.csv) | 56 (40 REQ + 16 NFR) | 56 satır (EVD=NONE) | PASS |
| 15 | Kalite Kapıları (gates.csv) | 10 (G0..G9) | 10 kapı (G0=NOT_APPROVED) | PASS |

---

## 3. Güvenlik ve Kurumsal Kriterler

| No | Kriter | Hedef Standart | Gerçek Durum | Sonuç |
|:---:|:---|:---|:---|:---:|
| 16 | Canlı operasyon bayrakları durumu | Tüm operasyonel bayraklar false | `config/features.example.json` içinde hepsi false | PASS |
| 17 | PCI-DSS kart verisi izolasyonu | Sıfır PAN/CVV saklama | Politika sabitlendi | PASS |
| 18 | KVKK log ve istemci maskeleme | Plaka ve PII maskeleme zorunluluğu | Güvenlik kontrolleri belgelendi | PASS |
| 19 | Kurumsal imza ve RACI atamaları | Yetkili kurumsal imza sirküleri | Henüz imzalanmadı (`TO_ASSIGN`) | **FAIL (BLOCKED)** |
| 20 | DEC-001 Kurumsal mali model onayı | Üniversite/Döner Sermaye resmi kararı | Karar henüz alınmadı | **FAIL (BLOCKED)** |

---

## Sonuç Özeti
G0 kapısının teknik ve dokümantasyonel hazırlığı tamamlanmıştır (`P00_SOURCE_READY`); ancak kurumsal yetki onayı ve blokajların çözülmesi gerçekleşmeden **G0 ONAYLANAMAZ (`NOT_APPROVED`)**.
