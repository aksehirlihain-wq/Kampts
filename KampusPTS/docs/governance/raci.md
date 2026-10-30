# Sorumluluk Matrisi (RACI Matrix) — Kampüs PTS

Bu belge, proje süreçlerindeki rollerin sorumluluk seviyelerini (R: Sorumlu, A: Onaylayan, C: Danışılan, I: Bilgilendirilen) tanımlar. Kurumsal dürüstlük ilkesi gereği gerçek kişi adları atanmamış; roller kurumsal pozisyonlar bazında tanımlanmıştır.

| Süreç / Karar Alanı | Çözüm Mimarı | Güvenlik / KVKK Yetkilisi | Mali / Döner Sermaye Otoritesi | ASManager / Fiziksel Güvenlik Sorumlusu | Yazılım Geliştirici | Test / QA Mimarı |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mimari Anayasa & K-01..K-12** | **A / R** | C | C | C | I | I |
| **Mali Model Seçimi (DEC-001)** | C | I | **A / R** | I | I | I |
| **Bariyer Otoritesi Kararı (DEC-008)** | R | C | I | **A** | I | C |
| **ASManager Entegrasyon Sınırları** | R | I | I | **A / R** | C | I |
| **Veri Şeması ve EF Core Tasarımı** | A | C | I | I | **R** | C |
| **Ödeme ve İdempotency Mekanizması** | A | C | C | I | **R** | C |
| **G0 Kapı Onayı** | R | C | C | C | I | I |
| **Birim ve Doğrulama Testleri** | A | I | I | I | R | **R** |
| **Canlıya Geçiş (G9) Kararı** | C | C | A | A | I | C |

*Not: Nihai isim bazlı onay atamaları kurumsal yönetim kurulu tarafından tanzim edilecektir (`TO_ASSIGN`).*
