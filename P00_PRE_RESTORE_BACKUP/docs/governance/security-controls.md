# Güvenlik, KVKK ve Denetim Kontrolleri (Security Controls & Compliance)

Bu belge, Kampüs PTS Gelir Yönetim Platformu'nun bilgi güvenliği, kişisel verilerin korunması (KVKK 6698), PCI-DSS kapsam izolasyonu ve görevler ayrılığı (SoD) ilkelerini belirler.

---

## 1. Kart Hamili Verisi ve PCI-DSS Sınırları
- **Kart Bilgisi Saklama Yasağı:** Sistem PAN, CVV, CVV2 veya son kullanma tarihi gibi hassas kart hamili verilerini veritabanında, önbellekte veya diskte ASLA saklamaz.
- **Sağlayıcı Formu ve Tokenizasyon:** Ödeme işlemleri yalnızca lisanslı PSP'lerin Hosted Checkout veya iframe tokenizasyon altyapısı üzerinden gerçekleştirilir. PTS yalnızca sağlayıcı işlem referansını (`ProviderTransactionId`) tutar.

---

## 2. Kişisel Verilerin Korunması (KVKK) ve Maskeleme
- **Plaka Verisi:** Plaka bilgisi mevzuat gereği kişisel veri kapsamında değerlendirilir.
- **Log Maskeleme:** Log ve metrik akışlarında plakalar ilk iki ve son iki karakter haricinde yıldızlanır (Örn: `34***78`).
- **Telefon ve TC Kimlik:** Veritabanında şifrelenmiş (`AES-256-GCM`) tutulur; loglara asla düz metin yazılmaz.
- **Veri Saklama ve İmha:** Otopark geçiş kayıtları kurumsal saklama politikası süresince saklanır; süre dolduğunda kriptografik veya fiziksel imha uygulanır (`DECISION_REQUIRED: Saklama Süresi`).

---

## 3. Görevler Ayrılığı (Segregation of Duties - SoD)
- Finansal tarife tanımlayan rol, tarife indirimini onaylayamaz.
- Sistem yöneticisi veya yazılımcı alt defter fişlerini doğrudan silemez veya veritabanından güncelleyemez.
- İptal ve iade işlemleri en az iki kademeli onay akışına (maker-checker) tabidir.

---

## 4. Denetim İzi (Audit Trail)
- Tüm yetkili işlemler, tarife değişiklikleri, manuel bariyer açma istekleri ve iade talepleri değiştirilemez denetim günlüğüne (`AuditLog`) zaman damgalı (`timestamptz UTC`) olarak kaydedilir.
