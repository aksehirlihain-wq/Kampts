# KAMPÜS PTS — GOOGLE AI STUDIO P00 DÜZELTME PROMPTU v1.1
## Kanonik Kaynağa Sadakat, Mimari Anayasa Kurtarma, Önizleme Ayrımı ve Bağımsız Doğrulama

**KAPSAM SINIRI:** Yalnızca **P00 düzeltmesi**. P01–P76 işlevlerine, veritabanı migrasyonlarına, PSP/barier/e-belge/ERP canlı bağlantılarına geçme. Bu oturum sıfırdan yeni bir yazılım çizmek değil, mevcut P00 çalışma alanını **kaynak bütünlüğü korunarak** düzeltmektir.

### 0 — GİRDİLERİ TANI VE KESİN ÖNCELİK SIRASI

Bu mevcut AI Studio projesinde `src/App.tsx`, `KampusPTS/`, `KampusPTS_P00_v1.0.zip` ve diğer üretilmiş dosyalar vardır. Önce mevcut proje dosyalarını sakla; **bütün projeyi yeniden oluşturma veya çalışan önizlemeyi gerekçesiz silme**.

Aşağıdaki ek dosyaları bu isteğin yanında veya AI Studio projesine ayrı ayrı yükleyeceğim:

1. **`P00_Kanonik_Kaynak_GeriYukle.mjs`** — orijinal P00 kaynağındaki 56 dosyanın **orijinal baytlarını ve SHA-256 hash değerlerini içinde taşıyan**, yalnız Node.js yerel dosya sistemi kullanan kurtarma/denetim aracı. Aracın `--check` ve `--restore` seçenekleri vardır. Bu bir canlı üretim işlemi değildir.
2. **`P00_Kanonik_Referans_1_Kayitlar.md`** — P00 kanonik CSV kütüklerinin birebir metin karşılığı (9 dosya).
3. **`P00_Kanonik_Referans_2_YonetisimMimari.md`** — üst yönetişim, mimari ve bağlam dosyaları (32 dosya).
4. **`P00_Kanonik_Referans_3_AraclarSablonlar.md`** — doğrulama araçları, şablonlar ve CI kaynağı (15 dosya).
5. İsteğe bağlı `KPTS_P00_Referans_Dosyalar_v1.zip` özgün kaynağı. ZIP'i **gerçekten okumadan** okunduğunu söyleme.

**Kaynak üstünlüğü:** Kanonik 56 dosyanın gerçek içeriği > bu düzeltme promptu > daha önce üretilmiş P00 belgeleri > görsel önizleme. Aynı ID'nin başka anlama kayması, kolonların değiştirilmesi, yapay bir eşik veya yapay onay eklenmesi **yasaktır**.

**Erişim koşulu:** Yukarıdaki `P00_Kanonik_Kaynak_GeriYukle.mjs` dosyasına ve okunabilir `.md` referanslara erişemiyorsan yeni kaynak icat etme; `REFERENCE_NOT_ACCESSIBLE`, `P00_REVIEW_REQUIRED` yaz ve bu oturumda P01'e geçme.

### 1 — SORUNU DOĞRU TEŞHİS ET

Önceki P00 çıktısında kayıt **sayıları** uygun görünse de kayıt **şeması ve anlamı** korunmamıştır. Somut örnekler:

- Kanonik `requirements.csv`: `id,phase,title,requirement,acceptance,status,owner_role,gate`. Üretilen dosya `Id,Title,Category,Priority,Description,Module,Status` kolonlarıyla bunu değiştirdi. Kanonik `REQ-001` «Kapsam/Yönetişim» iken üretilen `REQ-001` «Plaka Okuma ve Olay Yakalama» oldu. Kanonik `REQ-001` `DESIGNED`; üretilen `APPROVED`. Bu düzeyde içerik kayması kabul edilemez.
- Kanonik `nfr.csv` `NFR-001` «Kimlik ve oturum» iken üretilen NFR-001 «Plaka Okuma ve Tanıma Gecikmesi» ve `P99 < 500 ms` oldu. Karar verilmemiş performans eşiği icat etme.
- Kanonik `DEC-001` alternatifleri: **A Üniversite; B Döner sermaye; C Özel işletmeci; D Çoklu tüzel kişilik**. Üretilen A/B/C/D eşlemesi farklı. Bu hukuki/mali bağlamı değiştiren kritik hatadır.
- Kanonik `G1` P01–P04'ü, `G2` P05–P06'yı, `G3` P07–P10'u, `G4` P11–P15'i, `G5` P16–P19'u, `G6` P20–P22'yi, `G7` P23–P28'i, `G8` P29–P31'i, `G9` P32–P33'ü kapsar. Üretilen «G1=P01, G2=P02, ...» tablosu yanlıştır. G0=P00 ve G0=`NOT_APPROVED` kalmalı.
- Kanonik `K-12` test ve kanıt doğruluğudur. Üretilen arayüzde «72 saatlik yerel arabellek» diye tanımlanmış. Onaylanmamış cihaz/kapasite eşiği ekleme.
- Kanonik `config/features.example.json` kök alanları `environment`, `features`, `safety`, `testData`; üretilen `system`/`flags` şeması farklı. Emniyet bayraklarını kapalı tutmak doğrudur ama **orijinal arayüz kontratını değiştirmeden** yap.
- Üretilen yerel Python doğrulayıcı ve 11 test kendi uydurduğu kolonları doğruluyor. Bu testlerin geçmesi referansa sadakati doğrulamaz. Onları kanonik yapıya uyarla; kanonik validator'ı eksiksiz geri getir.

### 2 — KANONİK KAYNAĞI GERİ YÜKLE, ORİJİNALİ DONDUR

Bu projenin **AI Studio çalışma alanı kökünde**, `KampusPTS/` dizininin yanında aşağıdaki komutları çalıştırabiliyorsan çalıştır:

```bash
node P00_Kanonik_Kaynak_GeriYukle.mjs --check
node P00_Kanonik_Kaynak_GeriYukle.mjs --restore
node P00_Kanonik_Kaynak_GeriYukle.mjs --check
```

İlk `--check` başarısız olabilir; bu beklenen mevcut kaynak kaymasıdır. `--restore` şu şekilde davranmalıdır:

- **56 gerçek kaynak dosyasını** `P00_REFERENCE/` altında orijinal baytlarıyla korur. Bu referans dizini gelecekte **salt-okunur kabul edilir**.
- Bunların **49 P00 çalışma dosyasını** aynı göreli yollarla `KampusPTS/` içine geri yükler. Önceki oluşturulan sürümleri **`P00_PRE_RESTORE_BACKUP/`** içinde saklar, silmez.
- Yedi ileri-aşama bağlam dosyasını yalnız `P00_REFERENCE/` altında korur; yeni P01–P76 modül işlevleri çalıştırmaz.
- Gömülü her kaynağın SHA-256 bütünlüğünü kontrol eder. `--check` sonunda `reference_exact=56`, `working_p00_exact=49` görülmelidir. Bu bir **dosya bütünlüğü kanıtıdır**, kurumsal onay veya uygulama testi değildir.

Eğer terminal/Node çalıştırma yetkin yoksa öncelikle yüklediğim üç **okunabilir `.md` dosyasını** kullanarak aynı kanonik içeriği ilgili yollara aktar. `.md` dosyalarındaki çevreleyen başlık ve kod bloklarını hedef dosyanın içine koyma. Başlık/sütun/ID/anlam ve metni kaydırma. UTF-8 ve varsa BOM gibi bayt ayrıntılarını **doğrulayamıyorsan** `BYTE_EXACT_NOT_VERIFIED` olarak bildir; `SOURCE_INTEGRITY_PASS` iddia etme. Çalışma alanına harici kaynak aktarılamıyorsa *uydurma tamamlama yapma*.

Önemli: `P00_REFERENCE/` dışındaki P00 çalışma dosyalarında herhangi bir işlevsel genişletme yapmak zorundaysan **mevcut kanonik dosyayı yeniden yazmak yerine** `docs/extensions/` altında ek dosya oluştur ve değişikliği `CR` taslağıyla belgele. Kullanıcı onayı olmadan kanonik kayıtların anlamlarını veya kapı eşlemelerini değiştirme.

### 3 — KANONİK KÜTÜK VE KURUMSAL GERÇEKLİK

Kanonik CSV'lerin **tüm orijinal kolon ve satırlarını** birebir koru. Sayısal kontrol:

| Dosya | Kanonik kayıt sayısı | Zorunlu anlam |
|---|---:|---|
| requirements.csv | 40 | `REQ-001..040`, kaynakta `DESIGNED`; kurgusal `APPROVED` yok |
| nfr.csv | 16 | `NFR-001..016`, eşikler `TO_DEFINE_OR_VERIFY`, doğrulama `NOT_RUN` |
| decisions.csv | 31 | `DEC-001..031`, `DECISION_REQUIRED`, `actual_owner=TO_ASSIGN`, `due_date=TBD`, `evidence=NONE` |
| risks.csv | 15 | `RISK-001..015`, varsayımsal risk skorları `OPEN_ASSUMED` |
| blockers.csv | 8 | `BLK-001..008`, `OPEN`, özgün karar/gereksinim/kapı bağları |
| test-cases.csv | 10 | `TC-001..010`, `NOT_RUN`, `evidence=NONE` |
| traceability.csv | 56 | 40 REQ + 16 NFR; kanıtsız `DESIGNED_NOT_TESTED`, gerçek TC/EVD icat etme |
| gates.csv | 10 | `G0=NOT_APPROVED`, `G1..G9=NOT_STARTED`, özgün aşama mantığı |

**Özel denetimler:** `DEC-001`, `DEC-008`, `DEC-009`, `DEC-014`, `DEC-026`, `DEC-027`, `DEC-028`, `DEC-031` içeriklerini referanslarından yeniden getir. Özellikle `DEC-001` A/B/C/D model harfleri, `DEC-008` bariyer kumanda belirsizliği ve `DEC-027` ücretlendirme yetkisi kararı değiştirilmemelidir. `BLK-001..008` ile ilgili `decision_ids`, `requirement_ids`, `gates`, `blocks` alanlarını geri getir. `G0..G9` kanıt, onay ve mali/fiziksel NO-GO bağlantılarını koru.

### 4 — A1–A10, K-01–K-12 ve MALİ / FİZİKSEL OTORİTE

Üretilen `AGENTS.md` ve `foundational-invariants.md` içindeki iyi niyetli açıklamalar, orijinal numaralı kuralların yerine geçemez. **Orijinal dosyaları geri yükle;** görsel özetleri bu kaynaklardan yeniden oluştur.

- GV-ASManager 6.3.0 personel fiziksel geçiş haklarının otoritesidir. PTS, ASManager DB'ye yazmaz ve dokümansız cihaz/API alanları icat etmez. GV-LPR2812-DL gerçek SDK doğrulaması yapılmadan fiziksel geçiş kanıtı kabul edilmez.
- `PLATE_RECOGNIZED ≠ PASSAGE_CONFIRMED ≠ GATE_ACK`. Plaka görünmesi bariyerin açıldığını veya aracın geçtiğini ispatlamaz.
- `financial=ACTIVE ≠ access=VERIFIED_ACTIVE`. PTS mali hak fiziksel erişim izni değildir.
- `Quote ≠ Charge ≠ PaymentIntent ≠ PaymentTransaction ≠ ProviderSettlement ≠ Invoice ≠ JournalEntry ≠ ERPPosting`. Ödeme S2S doğrulanmadan `SUCCESS` olamaz; `CAPTURED ≠ SETTLED`.
- Tüzel kişi rolleri ayrı: `RevenueOwner`, `Collector`, `MerchantOfRecord`, `SettlementBeneficiary`, `InvoiceIssuer`, `AccountingAuthority`, `TaxPolicyOwner`. `DEC-001` çözümlenmiş gibi davranma.
- `POSTED` finansal hareketler immutable; düzeltme ters kayıtla; ERP nihai resmi muhasebe otoritesidir.
- `Fact Owner = Command Owner = Domain Event Owner`; modül dışı doğrudan şema/tablo yazımı yasak.
- İSG donanımları, fotosel, yangın, tahliye, anti-sıkışma yazılımla asla devre dışı bırakılamaz.
- `UNKNOWN≠FALSE`, `DESIGNED≠TESTED`, `NOT_RUN≠PASS`, `AI≠InstitutionalAuthority`.
- Erişim/kişisel veri ve sır politikaları: gerçek PAN/CVV, plaka, fotoğraf, TCKN veya API key'i istemciye/fixture/log'a koyma.

### 5 — `features.example.json` VE EK GÜVENLİK

Kanonik `features` nesnesindeki aşağıdaki bayraklar **kesinlikle false** kalır:

- `gateRealCommandsEnabled`
- `paymentRealCaptureEnabled`
- `eDocumentRealIssueEnabled`
- `erpRealPostingEnabled`
- `multiEntitySplitSettlementEnabled`

Kanonik `safety` alanındaki imzalı geçiş ve dört göz onayı gibi değerleri koru. Önceki AI üretiminde bulunan `enable_safety_interlock_bypass=false` gibi ikincil emniyet fikrini kanonik şemayı değiştirmek için kullanma; gerekiyorsa ayrı öneri belgesinde tanımla. Hiçbir emniyet bayrağı aktif bypass yetkisi yaratamaz.

### 6 — GOOGLE AI STUDIO ÖNİZLEMESİNİ DÜZELT

`src/App.tsx` P00 için **salt okunur, Türkçe, ferah, anlaşılır** önizleme olarak kalabilir; gerçek .NET backend veya erişim/ödeme/bariyer ürünü gibi sunulamaz. Aşağıdaki hataları gider:

1. `K-01..K-12` başlık/açıklamalarını orijinal `foundational-invariants.md` ile eşleştir. **K-12 = Test ve kanıt doğruluğu**; «72 saat offline arabellek» ifadesini sil. A1–A10'la yanlış birebir eşleme varsayma.
2. `REQ-001`, `NFR-001`, `DEC-001`, `BLK-001`, `TC-001` örneklerini **orijinal CSV satırlarından** göster. Kategori veya teknoloji varsayımı ekleme.
3. `G0..G9` tablosunu kanonik `docs/governance/gates.md` kapsamlarına göre göster; `G1=P01–P04`, `G9=P32–P33`. Gerçek olmayan onay rolü, tarih, blocker count üretme.
4. `APPROVED` statüsü, gerçek sahibi varmış gibi atanmış isimler, uydurma SLA/P99 eşikleri, hayali entegrasyon veya cihaz kabiliyetleri önizlemeye girmesin.
5. `G0=NOT_APPROVED`, `DECISION_REQUIRED=31`, `BLK OPEN=8`, `TC NOT_RUN=10`, `REFERENCE_EXACT=56/56` yalnız **check gerçek çalıştırıldıktan** sonra gösterilebilir. Çalıştırılmadıysa `NOT_VERIFIED` göster.
6. Mümkünse UI kayıtları doğrudan `KampusPTS/docs/registries` ve `docs/governance` kanonik dosyalarından türetilmiş **yerel, sentetik olmayan ve doğrulanabilir** bir read-only özet JSON'undan beslensin. Sadece «40/16/31» sayısını gömerek belgeyi yeniden yanlış tarif etme. Kaynağın SHA-256'sını özet metaverisine koy.
7. `src/App.tsx` ile `KampusPTS/web/preview-only` ilişkisini belgele. Gerçek frontend altyapısı bu aşamada tasarlanmış gibi gösterme; önizleme **PREVIEW_ONLY** olsun.
8. Mevcut modern tasarım temizliğini koru: açık yüzeyler, seyrek kartlar, kontrollü tipografi, az renk ve ikon, responsif davranış; fazla sekme/kalabalık ekran ekleme.

### 7 — TESTLERİ GERÇEK KAYNAĞA BAĞLA

Kanonik `KampusPTS/tools/validate_p00.py`, `KampusPTS/tools/build_manifest.py`, `KampusPTS/tests/test_validate_p00.py` dosyalarını **orijinal olarak** koru. Önceki ilave 11 test değerli olabilir fakat yanlış CSV şemasına göre yazılmıştır; doğrudan çalıştırıldığında yanlış pozitif verir. Gerekirse bunları `tests/test_p00_additional.py` gibi **ayrı** dosyaya aktar, kanonik kolonlara uyarla.

En az aşağıdaki **bağımsız regresyon kontrollerini** ilave et (standart kütüğü bozma):

- Orijinal 56 referans dosyanın hash karşılaştırması; P00 çalışma alanındaki 49 dosyanın hash karşılaştırması; fark varsa FAIL.
- Kanonik CSV **başlıklarının** ve yalnız sayının değil `REQ-001`, `NFR-001`, `DEC-001`, `DEC-031`, `K-12` gibi kilit anlamların kontrolü.
- `REQ-001.status=DESIGNED`; `NFR-001.verification=NOT_RUN`; `DEC-001.alternatives` orijinal seçenekleri; `G0=NOT_APPROVED`.
- `G1=P01–P04`, `G2=P05–P06`, ... `G9=P32–P33` semantik eşlemeleri; aşama/kapı kabulünü bir adım bir kapı gibi ele almama.
- `BLK` → `DEC`/`REQ`/`GATE`, `TC` → `REQ`, traceability → `REQ|NFR` başvuru tutarlılığı; gerçek olmayan test sonucu/EVD yasak.
- Özellik bayraklarında tek bir canlı true olmaması; kanonik `features` kontratının korunması.
- Özgün A1–A10/K-01–K-12 içeriklerinde tutarsızlığı saptayan kaynak bağlantısı denetimi.
- `src/App.tsx` ve türetilmiş UI verilerinin kanonik kütüklere aykırı hiçbir `APPROVED`, `72 saat`, yanlış GATE eşlemesi veya yanlış DEC-001 modeli göstermemesi.

Ortamda terminal varsa `KampusPTS` dizinine geçip gerçekten çalıştır:

```bash
python3 tools/validate_p00.py
python3 -m unittest discover -s tests -v
python3 -m json.tool config/features.example.json
python3 -m json.tool docs/architecture/event-envelope.schema.json
python3 tools/build_manifest.py
sha256sum -c manifest.sha256
```

Ardından çalışma alanı kökünde:

```bash
node P00_Kanonik_Kaynak_GeriYukle.mjs --check
```

Her komut için komut satırı, çıkış kodu, gerçek stdout/stderr ve çalışma ortamını raporla. Komut çalıştırmadıysan `NOT_RUN`; Python, .NET, Node vb. ortam bulunmuyorsa `NOT_AVAILABLE`; başarılı görünmesini istediğin için `EXECUTED_PASS` yazma.

**P00 yapısal testlerinin geçmesi** `.NET build`, React build, PostgreSQL migration, cihaz, ödeme, vergi belgesi, ERP ve kurumsal onayın geçtiği anlamına **gelmez**. Bunlar P00 sonunda yine `NOT_RUN` / `NOT_AVAILABLE` olmalıdır.

### 8 — MANİFEST, RAPOR VE TESLİMAT

- Son gerçek dosya değişikliklerinden sonra `KampusPTS/manifest.sha256` güncelle; kendisini içine alma. Kaynak hash listesi ile kanonik 56 dosyanın hash kontrolü **farklı iki denetim** olarak raporlanmalı.
- `KampusPTS/docs/gates/P00-delivery-report.md` dosyasını kanonik olarak koru. Bu oturumun yeni bilgilerini onu sessizce değiştirerek değil `KampusPTS/docs/reviews/P00-correction-2026-10-30.md` gibi **ek** inceleme raporuyla kaydet.
- Raporda: değişen/korunan dosyalar; 56/56 ve 49/49 sonuçları; 40/16/31/15/8/10/56/10 sayımları; özgün G0–G9 eşlemeleri; yanlış onayların silinmesi; tester sonuçları; P01'e taşınacak `TO_VERIFY`, `DECISION_REQUIRED`, `BLOCKER` alanları; gerçek ortam sınırlamaları olsun.
- `P00_REFERENCE/` kaynaklarını değiştirme ve ZIP içinde sakla. `P00_PRE_RESTORE_BACKUP/` yedeklerini gerekirse ayrı artefakt olarak ver; asıl çalışma paketi ile karıştırma.
- Çalışma alanı kökünden **düzenlenebilir bütün kaynakları** dışa aktar. Teslim adı `KampusPTS_P00_v1.1_canonical.zip` olabilir. Yalnız screenshot veya bir ekran kodu teslim sayılmaz.
- `G0=NOT_APPROVED` değişmemeli. P00 teknik kaynak durumunu ancak gerçek kanonik denetimler geçince `P00_SOURCE_READY / G0_NOT_APPROVED` olarak raporlayabilirsin. Herhangi bir kanonik bütünlük hatası veya testte başarısızlık varsa `P00_REVIEW_REQUIRED` yaz.

### 9 — 16 MADDELİK KESİN KABUL KONTROLÜ

Aşağıdaki maddeleri `PASS / FAIL / NOT_VERIFIED` ile ayrı ayrı bildir. Sadece çalışan komutla veya kaynak göstererek PASS ver:

1. 56 kanonik orijinal referans dosyası bayt tamlığıyla korunuyor.
2. 49 P00 çalışma dosyası orijinal kaynağın hash değerlerine eşit.
3. `REQ-001`, `NFR-001`, `DEC-001`, `K-12` semantiği ve ilgili tüm kolon şemaları düzeltilmiş.
4. Sekiz kütükte 40/16/31/15/8/10/56/10 sayımı doğru; CSV başlıkları ve satır kimlikleri kanonik.
5. `DEC-001` dört tüzel kişilik seçeneği harfleri bozulmamış.
6. `G0..G9` kanonik aşama aralıkları, belge/kanıt ihtiyaçları doğru.
7. G0 onaylanmamış, G1–G9 başlamamış; uydurma sahip, tarih veya EVD yok.
8. `A1–A10` ve `K-01–K-12` orijinal anlamları korunmuş.
9. `PLATE_RECOGNIZED`, `PASSAGE_CONFIRMED`, `GateAck` ve bariyer yetkisi ayrılmış.
10. Mali hak, tahsilat, settlement, fatura, defter, ERP farklı otoritelerle ayrılmış.
11. Tüm gerçek işlemlere ilişkin `features` bayrakları false; güvenlik interlockları değişmemiş.
12. KVKK, veri minimizasyonu, idempotency, audit ve dört-göz kontrolü değişmezleri korunmuş.
13. Kanonik validator ve ondan bağımsız regresyon testleri gerçek çalıştırıldı/çalıştırılmadı olarak dürüst raporlanmış.
14. Son manifest dosyalarla tutarlı; kodun .NET/PSP cihaz testlerinin yapılmadığı belirtilmiş.
15. Önizlemede kanonik kaynağa aykırı statü/kapı/K12 veya onaylanmamış süre/eşik kalmamış.
16. P01–P76'ya geçilmemiş, yeni canlı özellik geliştirilmemiş; düzenlenebilir P00 ZIP'i hazır.

### 10 — ZORUNLU SON YANIT ŞEKLİ

Bana Türkçe, şu başlıklarda denetlenebilir sonuç ver:

1. **Kaynak erişimi ve restorasyon** (`--check` öncesi/sonrası; gerçek sonuç veya `NOT_RUN`).
2. **Kanonik farklar** (hangi yanlış kayıtlar ve belgeler düzeltildi, yedekler).
3. **Dosya envanteri** (tam göreli yollarla).
4. **Doğrulamalar ve komut çıktısı** (PASS/FAIL/NOT_RUN/NOT_AVAILABLE; kanıtsız iddia yok).
5. **16 maddelik kabul tablosu**.
6. **Açık kurumsal kararlar ve canlı işlem blokajları**.
7. **P00 teknik kaynak kararı** (`P00_SOURCE_READY` veya `P00_REVIEW_REQUIRED`) ve bağımsız `G0_NOT_APPROVED`.
8. **İndirilebilir düzenlenebilir `KampusPTS_P00_v1.1_canonical.zip`** ve kısa teslim özeti.

**BURADA DUR.** Benden gelecek teknik incelemeyi beklemeden P01'e geçme.
