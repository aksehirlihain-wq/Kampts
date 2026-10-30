# Kurumsal Temel Değişmezler (Foundational Invariants K-01 — K-12)

Bu belge, Kampüs PTS Gelir Yönetim Platformu'nun teknik, hukuki ve operasyonel değişmezlerini (K-01 ila K-12) tanımlar. AGENTS.md içindeki A1–A10 mimari kuralları ile tam bir uyum içindedir.

---

### K-01: Tek Gerçek Kaynağı ve Modül Bağımsızlığı (Single Source of Truth)
Her veri alanının (`Domain Entity`) tek bir sahibi modül vardır. Hiçbir modül başka bir modülün veritabanı şemasına doğrudan sorgu atamaz veya kayıt ekleyemez (`Fact Owner = Command Owner = Domain Event Owner`). Modüller arası veri aktarımı yalnızca domain olayları ve uygulama portları üzerinden gerçekleşir.

### K-02: Fiziksel Güvenlik ve İSG Önceliği (Safety Interlocks Overwrite Software)
Saha güvenliği, araç sıkışma koruması (fotosel), yangın tahliye otomasyonu ve acil durum butonu gibi fiziksel güvenlik donanımları tüm yazılım komutlarının mutlak üstündedir. PTS yazılımı donanımsal güvenlik zincirini hiçbir koşulda baypas edemez.

### K-03: ASManager Entegrasyon Sınırı ve Veritabanı Yalıtımı (ASManager DB Isolation)
Mevcut GV-ASManager 6.3.0 sistemi personelin fiziksel geçiş haklarının tek otoritesidir. PTS, ASManager veritabanına doğrudan yazmaz, veritabanı şemasını tersine mühendislikle değiştirmez. İletişim resmi API / onaylı iş emri kanalları üzerinden yürütülür.

### K-04: Mali Hak ile Fiziksel Hak Ayrımı (Financial vs Access Rights Separation)
Finansal bir aboneliğin aktif olması (`financial=ACTIVE`), fiziksel bariyer geçiş yetkisini kendiliğinden açmaz (`access=VERIFIED_ACTIVE`). Fiziksel yetkilendirme ASManager tarafından doğrulanmış iş emri teyidine kadar ayrı bir durum olarak izlenir.

### K-05: Gözlem ile Kesin Geçiş Kanıtı Ayrımı (Observation vs Confirmed Passage)
Kameranın plakayı okuması (`PlateObservation` / `PLATE_RECOGNIZED`), aracın bariyeri fiziksel olarak aştığını kanıtlamaz (`PassageEvidence` / `PASSAGE_CONFIRMED`). Mali oturum başlatma/kapatma ve ücretlendirme işlemleri yalnızca doğrulanmış geçiş kanıtı ile kesinleşir.

### K-06: Ödeme Idempotency ve Durum Geçişleri (Payment Idempotency & Lifecycle)
Ödeme nesneleri sıralı ve katı bir durum makinesine tabidir (`Quote` → `Charge` → `PaymentIntent` → `PaymentTransaction` → `ProviderSettlement` → `Invoice` → `JournalEntry` → `ERPPosting`). PSP sunucusundan doğrulanmış webhook/callback teyidi gelmeden işlem `SUCCESS` kabul edilemez. Mükerrer ödemeler `idempotencyKey` ile önlenir.

### K-07: Mali Yetki Matrisi ve Rol Ayrılığı (Financial Authority Matrix & SoD)
Gelir Sahibi (`RevenueOwner`), Tahsilatçı (`Collector`), Kayıtlı Satıcı (`MerchantOfRecord`), Hakediş Sahibi (`SettlementBeneficiary`), Fatura Düzenleyen (`InvoiceIssuer`) ve Muhasebe Otoritesi (`AccountingAuthority`) birbirinden bağımsız tanımlanır. DEC-001 onaylanana kadar hiçbir model kesin kabul edilmez.

### K-08: Değişmez Alt Defter ve Ters Kayıt Disiplini (Immutable Sub-ledger & Reversals)
PTS alt defterinde `POSTED` statüsüne geçen hiçbir muhasebe kaydı silinemez veya değiştirilemez. Hatalı işlemler yalnızca eşit ve zıt bir ters kayıt (`reversal`) ile dengelenir. Borç/alacak denkliği korunur. Nihai yasal muhasebe otoritesi kurumsal ERP'dir.

### K-09: Bilgi Durumu Dürüstlüğü (Epistemic Truth)
Bilinmeyen durum yanlış değildir (`UNKNOWN ≠ FALSE`). Tasarlanan test koşulmuş test değildir (`DESIGNED ≠ TESTED`). Koşulmamış test geçmiş sayılamaz (`NOT_RUN ≠ PASS`). Yapay zeka veya varsayımlar kurumsal otorite yerine geçemez (`AI ≠ Institutional Authority`).

### K-10: Hassas Veri ve KVKK/PCI-DSS Koruması (PII & Cardholder Protection)
Kredi kartı PAN/CVV verisi hiçbir şekilde sistemde saklanmaz. Gerçek plaka, kimlik numarası, telefon numarası ve banka hesap verileri loglara, istemci taraflı koda veya test fixture'larına maskesiz konulamaz.

### K-11: Dayanıklı Mesajlaşma ve Outbox Deseni (Durable Outbox & Event Envelope)
Modüller arası tüm asenkron iletişim `Transactional Outbox` deseni ile garantiye alınır. Olaylar standart `event-envelope.schema.json` formatında yayımlanır; kayıpsız iletim, at-least-once teslim ve tüketici tarafında idempotent işleme zorunludur.

### K-12: Çevrimdışı Çalışma ve Yerel Arabellek Güvencesi (Offline Resilience & Gate Buffer)
Kampüs ağ kesintisi veya sunucu arızası durumunda kapı uç birimleri (gate controllers) yerel arabellek (`local buffer`) ile gözlem ve geçiş kayıtlarını kuyruğa alır. Ağ bağlantısı sağlandığında kayıtlar sıra numarası ve hash kontrolüyle sunucuya güvenle aktarılır.
