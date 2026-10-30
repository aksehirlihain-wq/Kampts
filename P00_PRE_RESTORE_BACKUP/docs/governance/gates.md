# Kalite ve Yönetişim Kapıları (Quality & Governance Gates G0 — G9)

Kampüs PTS Gelir Yönetim Platformu geliştirme ve devreye alma yaşam döngüsü 10 bağımsız kapı ile denetlenir. Bir kapı resmi olarak onaylanmadan (`APPROVED`) sonraki aşamanın canlı operasyonlarına geçilemez.

---

## Kapı Listesi ve Güncel Durum

| Kapı | Aşama | Başlık | Gerekli Kanıt / İnceleme | Sorumlu Yetkili Rol | Güncel Durum | NO-GO Gerekçesi |
|:---|:---|:---|:---|:---|:---|:---|
| **G0** | P00 | Kurumsal Proje Temeli & Mimari Anayasa | Anayasa, K-01..K-12, Registries, G0 Checklist, SHA-256 Manifest | Çözüm Mimarı, Baş Hukukçu, Mali Komite | **NOT_APPROVED** | Resmi kurumsal imza ve DEC-001 yetki onayı henüz tanzim edilmedi. |
| **G1** | P01 | Saha Keşfi & Cihaz Envanteri Kabulü | Saha LPR inceleme raporu, ASManager 6.3.0 protokol dökümü | Saha Mühendisi, Güvenlik Şube Müdürü | **NOT_STARTED** | P00 henüz onaylanmadı; saha keşfi başlatılmadı. |
| **G2** | P02 | Veri Modeli & Şema Dondurma | EF Core şema tasarımları, ADR kayıtları, KVKK veri haritası | Veri Mimarı, Bilgi Güvenliği Sorumlusu | **NOT_STARTED** | Önceki kapılar tamamlanmadı. |
| **G3** | P03 | Güvenlik & KVKK / PCI-DSS Denetimi | Statik güvenlik analiz raporu (SAST), sızma testi tasarım onayı | Bilgi Güvenliği Yetkilisi (CISO) | **NOT_STARTED** | Geliştirme öncesi aşama. |
| **G4** | P04 | Entegrasyon Portları & Kontrat Doğrulama | PSP, e-Fatura, ASManager ve ERP OpenAPI sözleşme testleri | Entegrasyon Mimarı, ERP Sorumlusu | **NOT_STARTED** | Port testleri henüz koşulmadı. |
| **G5** | P05 | Modüler Monolit Temel İnşası | Çekirdek modül unit testleri, Transactional Outbox testleri | Baş Yazılım Mimarı | **NOT_STARTED** | Çekirdek kodlama henüz başlamadı. |
| **G6** | P06 | DEV-LAB Simülasyon Kabulü | Sanal kapı, sahte yük ve idempotency simülasyon sonuçları | Test Mimarı, Kalite Güvence Lideri | **NOT_STARTED** | Simülasyon ortamı henüz hazır değil. |
| **G7** | P07 | Pilot Saha Kurulumu & Donanım Eşleşmesi | Pilot kapıda çift döngü ve bariyer kontrol test kanıtları | Saha Kurulum Lideri, Donanım Uzmanı | **NOT_STARTED** | Pilot saha tanımlanmadı. |
| **G8** | P08 | Mali Mutabakat & UAT Kabulü | 1000 örnek işlem ERP ve banka alt defter mutabakat kanıtı | Döner Sermaye Müdürü, Mali Denetçi | **NOT_STARTED** | UAT aşamasına gelinmedi. |
| **G9** | P09 | Canlıya Geçiş (Go-Live) | Tüm kapı kanıtları, geri dönüş (rollback) planı, SLA protokolü | İcra Kurulu / Rektörlük | **NOT_STARTED** | Nihai üretim onayı henüz gündemde değil. |

---

## Kapı Geçiş Kuralı
1. Hiçbir kapı için "zımni" veya "varsayılan" onay verilemez.
2. Kanıt dosyası (`EVD-*`) fiziksel olarak mevcut ve hash doğrulaması yapılmış olmalıdır.
3. Rol ataması yapılmamış (`TO_ASSIGN`) kararlar kapı onayına engel teşkil eder.
