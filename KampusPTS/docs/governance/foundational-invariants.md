# Kurumsal Temel Değişmezler (Foundational Invariants K-01 — K-12)

Bu belge, Kampüs PTS Gelir Yönetim Platformu'nun teknik, hukuki ve operasyonel değişmezlerini (K-01 ila K-12) tanımlar. AGENTS.md içindeki A1–A10 kuralları mimari ilkelerdir; K-01–K-12 kurumsal değişmezleri ile doğrudan numara eşlemesi yapılmaz.

---

### K-01: Fiziksel ve Mali Otorite Ayrılığı
Fiziksel erişim kontrolü ile mali gelir yönetimi iki ayrı egemen alandır. Fiziksel geçiş kontrolünün otoritesi sahadaki GV-ASManager 6.3.0 sistemidir; mali oturum, ücretlendirme ve tahsilatın otoritesi PTS platformudur. Bir alandaki hak veya durum diğer alanda otomatik olarak yetki doğurmaz.

### K-02: Marka Bağımsızlığı (Vendor Independence)
PTS platformu belirli bir donanım veya yazılım üreticisinin tescilli protokollerine sıkı sıkıya bağımlı tasarlanamaz. Saha cihazları (kamera, bariyer, döngü sensörü) ve geçiş kontrol yazılımları doğrulanmış açık portlar ve adaptör arayüzleri üzerinden sisteme bağlanır. Doğrulanmamış üretici alanları veya SDK özellikleri sisteme dahil edilemez.

### K-03: ASManager Yalıtımı ve Doğrudan Veritabanı Yazma Yasağı
PTS, ASManager veritabanına doğrudan SQL yazamaz; şemasını tersine mühendislikle değiştiremez veya baypas edemez. ASManager ile veri ve yetki iletişimi yalnızca doğrulanmış resmi API veya onaylı iş emri kanalları üzerinden yürütülür.

### K-04: Mali Hak ile Fiziksel Yetki Ayrımı
Bir abonenin finansal aboneliğinin aktif olması (`financial=ACTIVE`), fiziksel bariyer geçiş yetkisini kendiliğinden açmaz (`access=VERIFIED_ACTIVE`). Fiziksel erişim ASManager doğrulanmış iş emri teyidine kadar ayrı bir durum olarak bağımsız izlenir.

### K-05: Gözlem ile Kesin Geçiş Kanıtı Ayrımı
Kameranın plakayı okuması (`PlateObservation` / `PLATE_RECOGNIZED`), aracın bariyeri fiziksel olarak aştığını kanıtlamaz (`PassageEvidence` / `PASSAGE_CONFIRMED`). Bariyer kumandası (`GateCommand`) ve bariyer teyidi (`GateAck`) ayrı olgulardır. Salt plaka görüntüsüyle kesin oturum açılamaz, kapatılamaz veya ücret tahakkuk ettirilemez.

### K-06: Ödeme Idempotency ve Durum Makinesi
Ödeme nesneleri sıralı ve katı bir durum makinesine tabidir (`Quote` → `Charge` → `PaymentIntent` → `PaymentTransaction` → `ProviderSettlement` → `Invoice` → `JournalEntry` → `ERPPosting`). PSP sunucusundan sunucu-sunucu doğrulanmış yanıt alınmadan ödeme `SUCCESS` kabul edilemez; `CAPTURED` bankada `SETTLED` anlamına gelmez. Mükerrer ödemeler `idempotencyKey` ile engellenir.

### K-07: Mali Yetki Matrisi ve Rol Ayrılığı
Gelir Sahibi (`RevenueOwner`), Tahsilatçı (`Collector`), Kayıtlı Satıcı (`MerchantOfRecord`), Hakediş Sahibi (`SettlementBeneficiary`), Fatura Düzenleyen (`InvoiceIssuer`), Muhasebe Otoritesi (`AccountingAuthority`) ve Vergi Politikası Sahibi (`TaxPolicyOwner`) ayrı rollerdir. Kurumsal üst yönetimce DEC-001 (A/B/C/D seçenekleri) onaylanana kadar hiçbir model kesin kabul edilemez.

### K-08: Değişmez Alt Defter ve Ters Kayıt Disiplini
PTS alt defterinde `POSTED` statüsüne geçen hiçbir muhasebe kaydı silinemez veya güncellenemez. Hatalı işlemler yalnızca eşit ve zıt tutarlı bir ters kayıt (`reversal`) ile dengelenir. Çift taraflı borç/alacak denkliği korunur. Nihai yasal muhasebe otoritesi PTS değil, onaylanmış kurumsal ERP'dir.

### K-09: Bilgi Durumu Dürüstlüğü (Epistemic Truth)
Bilinmeyen durum yanlış değildir (`UNKNOWN ≠ FALSE`). Tasarlanan test koşulmuş test değildir (`DESIGNED ≠ TESTED`). Koşulmamış test geçmiş sayılamaz (`NOT_RUN ≠ PASS`). Yapay zeka veya varsayımlar kurumsal onay makamı yerine geçemez (`AI ≠ Institutional Authority`). Eksik tüm koşullar açıkça `DECISION_REQUIRED`, `TO_VERIFY`, `BLOCKER` veya `NOT_AVAILABLE` olarak gösterilir.

### K-10: Hassas Veri, KVKK ve PCI-DSS Koruması
Kredi kartı PAN/CVV verisi hiçbir şekilde sistemde saklanmaz. Gerçek plaka, kimlik numarası, telefon numarası, kişisel fotoğraf ve banka hesap verileri loglara, istemci taraflı koda veya test fixture'larına maskesiz konulamaz. Tüm API anahtarları sunucu tarafı güvenli kasalarda tutulur.

### K-11: Dayanıklı Mesajlaşma ve Outbox Deseni
Modüller arası tüm asenkron iletişim `Transactional Outbox` deseni ile garantiye alınır. Olaylar standart `event-envelope.schema.json` formatında yayımlanır; kayıpsız iletim, at-least-once teslim ve tüketici tarafında idempotent işleme zorunludur.

### K-12: Test ve Kanıt Doğruluğu (Test and Evidence Veracity)
Gerçekte koşulmamış hiçbir test için `PASS` sonucu veya sahte kanıt (`EVD-*`) üretilemez. Bir kalite kapısının (G0–G9) geçilebilmesi için fiziksel olarak mevcut, imzalanmış ve hash doğrulaması yapılmış kanıt zorunludur. Tasarlanmış testler koşulana kadar dürüstçe `NOT_RUN` ve `EVD=NONE` olarak raporlanır.
