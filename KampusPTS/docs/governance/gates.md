# Kalite ve Yönetişim Kapıları (Quality & Governance Gates G0 — G9)

Kampüs PTS Gelir Yönetim Platformu geliştirme ve devreye alma yaşam döngüsü 10 bağımsız kurumsal kapı ile denetlenir. Bir kapı resmi olarak onaylanmadan (`APPROVED`) sonraki aşamanın canlı operasyonlarına geçilemez.

---

## Kanonik Kapı Listesi ve Aşama Kapsamları

| Kapı | Kapsadığı Aşama Aralığı | Kapı Başlığı | Gerekli Kanıt / İnceleme | Sorumlu Yetkili Rol | Güncel Durum | NO-GO Gerekçesi |
|:---|:---|:---|:---|:---|:---:|:---|
| **G0** | **P00** | Kurumsal Proje Temeli, Mimari Anayasa & Kanıt Kayıtları | Anayasa, K-01..K-12, Registries, G0 Checklist, SHA-256 Manifest | Çözüm Mimarı, Baş Hukukçu, Mali Komite | **NOT_APPROVED** | Resmi kurumsal imza ve DEC-001 yetki onayı henüz tanzim edilmedi. |
| **G1** | **P01–P04** | Saha Keşfi, Cihaz Envanteri ve Entegrasyon Sınırları | Saha LPR inceleme raporu, GV-ASManager 6.3.0 protokol dökümü | Saha Mühendisi, Güvenlik Şube Müdürü | **NOT_STARTED** | P00 henüz onaylanmadı; saha keşfi başlatılmadı. |
| **G2** | **P05–P06** | Veri Modeli, Şema Dondurma ve İletişim Protokolleri | EF Core şema tasarımları, ADR kayıtları, KVKK veri haritası | Veri Mimarı, Bilgi Güvenliği Sorumlusu | **NOT_STARTED** | G0 ve G1 aşamaları tamamlanmadı. |
| **G3** | **P07–P10** | Güvenlik, KVKK, PCI-DSS ve Dayanıklı Outbox | Statik güvenlik analiz raporu (SAST), sızma testi tasarım onayı | Bilgi Güvenliği Yetkilisi (CISO) | **NOT_STARTED** | Geliştirme öncesi aşama. |
| **G4** | **P11–P15** | Tarife Motoru, Abonelik ve Finansal Durum Makinesi | PSP, e-Fatura, ASManager ve ERP OpenAPI sözleşme testleri | Entegrasyon Mimarı, ERP Sorumlusu | **NOT_STARTED** | Port testleri henüz koşulmadı. |
| **G5** | **P16–P19** | PSP Entegrasyon Portları, e-Fatura ve Alt Defter | Çekirdek modül unit testleri, Transactional Outbox testleri | Baş Yazılım Mimarı | **NOT_STARTED** | Çekirdek kodlama henüz başlamadı. |
| **G6** | **P20–P22** | DEV-LAB Simülasyon, İdempotency ve Yük Kabulü | Sanal kapı, sahte yük ve idempotency simülasyon sonuçları | Test Mimarı, Kalite Güvence Lideri | **NOT_STARTED** | Simülasyon ortamı henüz hazır değil. |
| **G7** | **P23–P28** | Pilot Saha Entegrasyonu ve Donanım Eşleşmesi | Pilot kapıda çift döngü ve bariyer kontrol test kanıtları | Saha Kurulum Lideri, Donanım Uzmanı | **NOT_STARTED** | Pilot saha tanımlanmadı. |
| **G8** | **P29–P31** | UAT, ERP Mutabakatı ve Mali Kabul | 1000 örnek işlem ERP ve banka alt defter mutabakat kanıtı | Döner Sermaye Müdürü, Mali Denetçi | **NOT_STARTED** | UAT aşamasına gelinmedi. |
| **G9** | **P32–P33** | Canlıya Geçiş (Go-Live) ve Nihai Devir | Tüm kapı kanıtları, geri dönüş (rollback) planı, SLA protokolü | İcra Kurulu / Rektörlük | **NOT_STARTED** | Nihai üretim onayı henüz gündemde değil. |

---

## Kapı Geçiş Disiplini
1. **Zımni Onay Yasağı:** Hiçbir kapı için "varsayılan" veya "zımni" onay verilemez.
2. **Fiziksel Kanıt Şartı:** Kanıt dosyası (`EVD-*`) fiziksel olarak mevcut, imzalanmış ve hash doğrulaması yapılmış olmalıdır (K-12).
3. **Açık Blokaj Varlığı:** Ataması yapılmamış karar (`TO_ASSIGN`) veya açık blokaj (`BLK-*`) varken ilgili kapı onaylanamaz.
