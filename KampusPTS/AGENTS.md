# AGENTS.md — Kampüs PTS Mimari ve Yönetişim Anayasası

Bu belge, Kampüs PTS Gelir Yönetim Platformu üzerinde geliştirme, denetim veya mimari değerlendirme yapacak tüm mühendis ve otonom/yardımcı ajanlar için bağlayıcı üst anayasadır.

## 1. Temel Ajan Değişmezleri (A1 – A10)

### A1 — Sovereign Domain Boundaries (Egemen Alan Sınırları)
- **Kural:** Her iş modülü kendi verisinin ve komutlarının tek egemen sahibidir (`Fact Owner = Command Owner = Domain Event Owner`).
- **Uygulama:** Hiçbir modül başka bir modülün veritabanı şemasına doğrudan yazamaz veya bypass edemez. Modüller arası iletişim yalnızca onaylanmış Application portları, domain event'ler ve inbox/outbox desenleriyle gerçekleştirilir.
- **İlgili Değişmez:** K-01.

### A2 — Physical Safety Interlock Invariant (Fiziksel Güvenlik ve İSG Önceliği)
- **Kural:** Donanımsal ve fiziksel güvenlik zinciri (fotosel, yangın tahliye, mekanik sıkışma sensörü, acil stop) tüm yazılım komutlarının mutlak üstündedir.
- **Uygulama:** PTS yazılımı hiçbir şart altında donanım güvenlik interlocklarını bypass edemez veya geçersiz kılamaz. Yazılım acil durumda yalnızca tahliye modunu destekler.
- **İlgili Değişmez:** K-02.

### A3 — ASManager Access Control Decoupling (ASManager Yalıtımı)
- **Kural:** Sahadaki GV-ASManager 6.3.0 sistemi, personelin fiziksel geçiş haklarının yegane yetkili otoritesidir.
- **Uygulama:** PTS, ASManager veritabanına doğrudan SQL yazamaz; tersine mühendislikle şema manipülasyonu yapamaz. ASManager ile entegrasyon yalnızca onaylı iş emirleri veya doğrulanmış resmi entegrasyon kanalları üzerinden yürütülür.
- **İlgili Değişmez:** K-03.

### A4 — Financial vs Physical Separation (Mali Hak ile Fiziksel Hak Ayrımı)
- **Kural:** Finansal abonelik hakkı (`financial=ACTIVE`), fiziksel erişim hakkını kendiliğinden aktif edemez (`access=VERIFIED_ACTIVE`).
- **Uygulama:** Bir abonenin borç ödemiş olması veya plakasının sisteme kayıtlı olması doğrudan bariyer açma yetkisi doğurmaz; ASManager senkronizasyonu doğrulanmış bir iş emri teyidiyle sonuçlanana kadar iki durum bağımsız takip edilir.
- **İlgili Değişmez:** K-04.

### A5 — Passage Evidence Invariant (Gözlem ve Geçiş Kanıtı Ayrımı)
- **Kural:** Plaka gözlemi (`PlateObservation` / `PLATE_RECOGNIZED`), fiziksel geçiş kanıtı (`PassageEvidence` / `PASSAGE_CONFIRMED`), kapı komutu (`GateCommand`) ve bariyer teyidi (`GateAck`) kesinlikle ayrı olgulardır.
- **Uygulama:** Yalnızca kamera LPR görüntüsü okunmasıyla otopark oturumu başlatılamaz/kapatılamaz, ücret tahakkuku kesinleştirilemez veya bariyer başarıyla açıldı varsayılamaz. Çift döngü veya fotosel doğrulaması şarttır.
- **İlgili Değişmez:** K-05.

### A6 — Financial Idempotency & State Machine (Mali Durum Makinesi ve Mükerrerlik Koruması)
- **Kural:** Finansal nesneler bağımsız yaşam döngüsüne sahiptir: `Quote` → `Charge` → `PaymentIntent` → `PaymentTransaction` → `ProviderSettlement` → `Invoice` → `JournalEntry` → `ERPPosting`.
- **Uygulama:** Sağlayıcıdan sunucu-sunucu doğrulanmış yanıt alınmadan ödeme `SUCCESS` olamaz; `CAPTURED` bankada `SETTLED` anlamına gelmez. Mükerrer ödeme ve tekrarlanan webhook çağrıları kriptografik `idempotencyKey` ile engellenir.
- **İlgili Değişmez:** K-06.

### A7 — Entity Disaggregation Invariant (Çoklu Tüzel Kişilik ve Yetki Ayrılığı)
- **Kural:** Gelir Sahibi (`RevenueOwner`), Tahsilatçı (`Collector`), Kayıtlı Satıcı (`MerchantOfRecord`), Hakediş Sahibi (`SettlementBeneficiary`), Fatura Düzenleyen (`InvoiceIssuer`), Muhasebe Otoritesi (`AccountingAuthority`) ve Vergi Politikası Sahibi (`TaxPolicyOwner`) ayrı rollerdır.
- **Uygulama:** Üniversite, döner sermaye, vakıf ve özel işletmeci modelleri (A/B/C/D) açık tutulur; DEC-001 yetkili makamlarca onaylanana kadar sabit bir model varsayılmaz. Hukuki dayanağı doğrulanmamış hizmetler ücretlendirilemez (DEC-027).
- **İlgili Değişmez:** K-07.

### A8 — Immutable Sub-ledger (Değişmez Alt Defter ve Ters Kayıt)
- **Kural:** `POSTED` statüsüne geçmiş hiçbir alt defter yevmiye kaydı silinemez veya güncellenemez.
- **Uygulama:** Düzeltmeler yalnızca eşit ve zıt ters kayıt (`reversal`) veya düzeltme fişi ile yapılır; fiş borç/alacak dengesi (double-entry balance) her an korunur. Nihai yasal muhasebe kaynağı PTS değil, entegre kurumsal ERP'dir.
- **İlgili Değişmez:** K-08.

### A9 — Epistemic Integrity Invariant (Bilgi Durumu Dürüstlüğü)
- **Kural:** Bilinmeyen durum yanlış değildir (`UNKNOWN ≠ FALSE`); tasarlanmış test koşulmuş test değildir (`DESIGNED ≠ TESTED`); koşulmamış test geçmiş sayılamaz (`NOT_RUN ≠ PASS`); yapay zeka kurumsal onay makamı değildir (`AI ≠ Institutional Authority`).
- **Uygulama:** Eksik, henüz onaylanmamış veya test edilmemiş tüm unsurlar açıkça `DECISION_REQUIRED`, `TO_VERIFY`, `BLOCKER`, `NOT_RUN` veya `NOT_AVAILABLE` olarak etiketlenir.
- **İlgili Değişmez:** K-09.

### A10 — Zero-Trust Security & PII Protection (Sıfır Güven ve KVKK/PCI-DSS Disiplini)
- **Kural:** Kart PAN ve CVV verisi hiçbir şekilde sistemde saklanmaz. Gerçek kimlik, telefon, plaka ve banka verileri test ve log ortamlarına maskelenmeden aktarılamaz.
- **Uygulama:** Loglarda ve istemci yanıtlarında PII maskeleme zorunludur. Tüm API anahtarları ve sırlar çevre değişkenlerinde veya güvenli kasa (vault) içinde tutulur.
- **İlgili Değişmez:** K-10.
