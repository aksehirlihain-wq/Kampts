# KAMPÜS PTS — GOOGLE AI STUDIO GELİŞTİRME PROMPTU
## P00 / Kurumsal Proje Temeli, Mimari Anayasa, Kanıt ve Karar Kayıtları

**Görev sınırı:** YALNIZCA P00. P01–P76'ya kendiliğinden geçme.

### 1. Üstlendiğin rol ve teslim şekli

Kurumsal ölçekte yazılım geliştiren kıdemli solution architect, .NET 10 mimarı, React/TypeScript mühendisi, PostgreSQL veri mimarı, ödeme/finans uzmanı, güvenlik/KVKK/İSG analisti, test mimarı ve teknik dokümantasyon sorumlusu olarak hareket et. Türkçe iletişim ve Türkçe son kullanıcı arayüz etiketleri kullan; kaynak kodu, API, tablo, olay ve dosya adları genel olarak İngilizce olsun.

Yalnızca fikir, ekran resmi veya açıklama üretme: **proje çalışma alanında gerçek dosyaları oluştur/güncelle**, bunları düzenlenebilir olarak teslim et ve ZIP/GitHub ile dışa aktarılabilir durumda bırak. Bu aşamada uygulamanın iş modüllerini, sahte finansal işlem akışlarını veya canlı servis entegrasyonlarını üretme. Önce mimari ve yönetişim temelini kur.

### 2. Referans kaynağı ve çalışma stratejisi

Referans olarak yüklenen **`KPTS_P00_Referans_Dosyalar_v1.zip`** içindeki `P00_REFERENCE/` dizinini kullan. Bu paket P00–P76 tarihsel kaynak deposundan ayıklanmış P00 belgelerini ve sonraki aşamalar için sınırlı bağlamı içerir. Özellikle aşağıdaki dosyaları, sırayla ve bütünüyle incele:

1. `AGENTS.md` ve `docs/governance/foundational-invariants.md`.
2. `docs/charter.md`, `docs/financial-authority-matrix.md`.
3. `docs/registries/README.md` ve tüm `docs/registries/*.csv`.
4. `docs/governance/gates.md`, `docs/gates/G0-checklist.md`, `docs/gates/P00-delivery-report.md`.
5. `docs/architecture/overview.md`, `docs/architecture/financial-domain.md`, `docs/architecture/event-envelope.schema.json`.
6. `config/features.example.json`, `tools/validate_p00.py`, `tests/test_validate_p00.py`.
7. Yalnız bağlam için `P01-README.md`, `docs/p05/01-architecture-blueprint.md`, `docs/p76/FINAL-HANDOFF.md`.

Referans dosyaları silme, kısaltma, anlamsal olarak yeniden icat etme veya geriye dönük karar/onay üretme. Yeni projede `P00_REFERENCE/` okunur referans olarak kalabilir; üzerinde çalışılan asıl proje kökü `KampusPTS/` olsun. Referans paketi içeriğini gerçekten okuyamadıysan **`REFERENCE_NOT_ACCESSIBLE`** olarak belirt; okuduğunu iddia etme. Referans dışındaki eksik kritik bir gerçek bilgiyi asla tahmin ederek doldurma.

Mevcut 2.200 dosyalık v1.76 kaynak paketinin kapanmış olması üretim kabulü değildir. Bu aşama **temiz, kontrollü yeniden geliştirme ve kanıtlı devamlılık** başlangıcıdır. Önceki kodu rastgele kopyalayıp çalışıyor olarak sunma.

### 3. Ürünün amacı ve değişmez yetki sınırları

Ürün: **Kampüs PTS Gelir Yönetim Platformu**. Çoklu kampüs ve çoklu yasal işletme yapısında plaka gözlemi, gerçek geçiş kanıtı, otopark mali oturumu, abonelik, mali hak, tarife, ücret/tahakkuk, PSP üzerinden ödeme, e-Fatura/e-Arşiv, PTS alt defteri, ERP aktarımı, mutabakat, istisna, bildirim, denetim ve raporlama işlevleri için uzun vadeli platform tasarlanır.

Aşağıdaki hükümler tartışmasız mimari kısıttır:

- Mevcut **GV-ASManager 6.3.0**, personelin fiziksel geçiş haklarının otoritesidir; PTS, ASManager veritabanına hiçbir şekilde doğrudan yazmaz, şemasını tersine mühendislikle değiştirip baypas etmez. Saha sistemi olarak **GV-LPR2812-DL** referans gösterilir; doğrulanmamış vendor endpoint, SDK alanı veya cihaz kabiliyeti icat edilmez.
- PTS'nin finansal abonelik hakkı fiziksel erişim hakkını kendiliğinden aktif etmez. `financial=ACTIVE` ile `access=VERIFIED_ACTIVE` ayrıdır. ASManager yetki tanımı onaylı iş emri veya doğrulanmış resmi kanal üzerinden yürütülür.
- `PlateObservation` / `PLATE_RECOGNIZED`, `PassageEvidence` / `PASSAGE_CONFIRMED`, `GateCommand` ve `GateAck` ayrı olgulardır. Salt plaka görüntüsüyle kesin giriş-çıkış, tahakkuk veya bariyer başarısı ilan edilmez.
- PTS mali çıkış kararı üretebilir; gerçek bariyer kumanda otoritesi `DEC-008` çözülene kadar `UNKNOWN` kalır. Fotosel, tahliye, yangın ve sıkışma güvenlik zinciri hiçbir yazılım akışıyla baypas edilmez.
- `Quote`, `Charge`, `PaymentIntent`, `PaymentTransaction`, `ProviderSettlement`, `Invoice`, `JournalEntry`, `ERPPosting` ayrı nesnelerdir. Ödeme, doğrulanmış sunucu-sunucu sağlayıcı sonucundan önce `SUCCESS` olmaz; `CAPTURED` bankada `SETTLED` anlamına gelmez. Çift tahsilat ve tekrarlı callback idempotency ile önlenir.
- `RevenueOwner`, `Collector`, `MerchantOfRecord`, `SettlementBeneficiary`, `InvoiceIssuer`, `AccountingAuthority` ve `TaxPolicyOwner` birbirinden ayrı tanımlanır. Üniversite, döner sermaye, özel işletmeci, çoklu tüzel kişilik için A/B/C/D seçenekleri korunur; **`DEC-001` çözümlenmiş varsayılmaz**. Hukuki yetkisi doğrulanmamış otopark dışı/yaya hizmeti ücretlendirilmez (`DEC-027`).
- `POSTED` alt defter fişi silinmez, düzeltilmesi ters kayıtla olur; mali fiş dengesi sağlanır. Nihai yasal muhasebe kaynağı PTS değil, onaylanmış ERP/muhasebe otoritesidir.
- `Fact Owner = Command Owner = Domain Event Owner`; modüller başka modülün tablosuna doğrudan yazmaz. Projeksiyon/raporlama hakikatin sahibi değildir.
- `UNKNOWN ≠ FALSE`, `DESIGNED ≠ TESTED`, `NOT_RUN ≠ PASS`, `AI ≠ Institutional Authority`. Eksik koşullar açıkça `DECISION_REQUIRED`, `TO_VERIFY`, `BLOCKER` veya `NOT_AVAILABLE` olarak görünür.
- Kart PAN/CVV saklanmaz. Gerçek plaka, kimlik bilgisi, kişisel fotoğraf, banka sırrı ve API anahtarı test fixture'ına veya istemci koduna konulmaz.

### 4. Teknoloji ve mimari kararı

P00'dan itibaren hedef mimariyi sabitle:

- Backend: **ASP.NET Core / .NET 10 LTS**, modüler monolit, C#, OpenAPI 3.1.
- Veri: **PostgreSQL 16+**, EF Core, modül başına mantıksal şema ve veri sahipliği, uygun kapsamda tenant/legalEntity izolasyonu.
- Worker: inbox/outbox, durable event delivery, idempotent tüketiciler ve periyodik mutabakat.
- Frontend: **React + TypeScript**, modüler sayfa, temiz tasarım sistemi, Türkçe arayüz ve rol bazlı gezinme.
- Bağımlılık: `Hosts.Api / Hosts.Worker → Modules.*.Application → Modules.*.Domain`; Infrastructure uygulama portlarını uygular; modüller birbirinin Infrastructure/DB nesnelerine bağlanmaz. `SharedKernel` yalnız teknik primitive tutar.
- Olay zarfı: en az `eventId, eventType, schemaVersion, occurredAtUtc, receivedAtUtc, sourceSystem, correlationId, causationId, idempotencyKey, payloadHash, tenantId, legalEntityId, payload` tasarım alanlarını koru; onaylanmış kontrat/JSON Schema sürümü kullan.
- Zaman: veritabanında UTC ve `timestamptz`; arayüzde `Europe/Istanbul`. Para: TRY kuruş için `bigint` minor-unit, vergi/indirim için `decimal`; finans hesabında `float` kullanma. Rounding politikası yetkili karar alınana kadar belirlenmiş gibi davranma.
- Üretici/PSP/e-belge/ERP adaptörleri için doğrulanmış gerçek entegrasyona kadar port/kontrat tasarla; kesin endpoint yazma.

**Önemli Google AI Studio uyumluluk notu:** AI Studio Build'in web önizlemesi React ve Node.js çalışma ortamına dayanır. **Node.js'i sessizce kurumsal .NET backend'in yerine geçirme.** P00'da .NET mimarisini belgeler ve gelecek proje yerleşimini tanımlarsın. Gerekirse sadece önizleme amacıyla izole, `PREVIEW_ONLY` etiketli, sentetik veri kullanan hafif React sayfası oluştur; onu gerçek API, çalışan mali backend veya kabul kanıtı olarak gösterme. .NET/PG runtime ortamda yoksa `NOT_AVAILABLE`, ilgili build/testler `NOT_RUN` kaydedilir.

### 5. P00'da oluşturulacak proje ve dosyalar

**Referansın gerçek içerik ve kayıtlarını koruyarak** en az aşağıdaki çalışma ağacını oluştur. Yerinde korunacak dosyalar varsa yalnız değişiklik ihtiyacını kanıtlayarak düzenle:

```text
KampusPTS/
  AGENTS.md
  README.md
  .editorconfig
  .gitignore
  .gitattributes
  Directory.Build.props
  docs/
    charter.md
    financial-authority-matrix.md
    governance/
      foundational-invariants.md
      gates.md
      raci.md
      change-control.md
      security-controls.md
      quality-scorecard.md
    architecture/
      overview.md
      financial-domain.md
      system-context.mmd
      event-envelope.schema.json
      adr/ADR-001.md
      adr/ADR-002.md
      adr/ADR-003.md
    registries/
      README.md
      requirements.csv
      nfr.csv
      decisions.csv
      risks.csv
      blockers.csv
      traceability.csv
      test-cases.csv
      gates.csv
    templates/
      REQ-template.md
      NFR-template.md
      DEC-template.md
      ADR-template.md
      RISK-template.md
      BLK-template.md
      TC-template.md
      EVD-template.md
      CR-template.md
      GATE-template.md
      BR-template.md
    gates/
      G0-checklist.md
      G1-input-checklist.md
      P00-delivery-report.md
  config/
    features.example.json
  tools/
    validate_p00.py
    build_manifest.py
  tests/
    test_validate_p00.py
  evidence/
    P00/.gitkeep
  src/.gitkeep
  web/.gitkeep
  .github/workflows/p00-validation.yml
  manifest.sha256
```

Gelecek modüllere ait gerçek kod P07 ve sonraki aşamalarda üretilir. P00 içine tüm modüllerin sahte CRUD implementasyonunu sıkıştırma. `README.md` içinde çalışma dizini, referans/prod ayrımı, faz durumu, ileri aşama haritası ve gerçek sınırlamalar açık yazılsın.

### 6. P00 kayıtlarının birebir korunması

Referansın temel kimlik ve içerik sürekliliğini koru:

- `REQ-001..040`: **40** kayıt.
- `NFR-001..016`: **16** kayıt.
- `DEC-001..031`: **31** kayıt; tümü `DECISION_REQUIRED`, gerçek karar sahibi `TO_ASSIGN`, gerçek karar tarihi `TBD`.
- `RISK-001..015`: **15** risk; taslak skorlar kesin veri değildir.
- `BLK-001..008`: **8** açık blokaj.
- `TC-001..010`: **10** tasarlanmış ancak `NOT_RUN` test.
- `traceability.csv`: 40 REQ + 16 NFR = **56** bağımsız kayıt; gerçek EVD yoksa `NONE`.
- `G0..G9`: **10** kapı; `G0=NOT_APPROVED`, diğerleri `NOT_STARTED`.

CSV'lerde mevcut kolon başlıklarını ve kayıt ID'lerini birebir koru. Türkçe Excel uyumluluğu için gerekliyse özgün UTF-8 BOM biçimini koru. Uydurma imza, sorumlu kişi, karar tarihi, entegrasyon sonucu veya TC/EVD üretme. Genişletme ihtiyacı varsa tarihli `CR`/`ADR` önerisi aç; önceki kaydı sessiz silme veya başka anlama çevirme.

### 7. Yönetişim ve teslim kuralları

- `AGENTS.md` içindeki **A1–A10** ile `foundational-invariants.md` içindeki **K-01–K-12** değişmezleri çelişkisiz bağla.
- G0–G9 için bağımsız kriterler, kanıt/inceleme ihtiyacı, yetkili rol, durum ve NO-GO gerekçelerini yaz. Gerçek imza yoksa G0 onayı verme.
- `DEC-001`, `DEC-008`, `DEC-009`, `DEC-014`, `DEC-026`, `DEC-027`, `DEC-028`, `DEC-031` gibi kararların bağlı mali/fiziksel blokajları matriste açıkça göster.
- Her gereksinim için ileride kullanılabilecek `REQ/NFR → UC → TC → EVD → GATE` izlenebilirliğini kur; test veya kanıt eksikliğini açık durumla göster.
- İsim/rol bazlı RACI taslağı yaz fakat gerçekte atanmış kişi icat etme.
- Kimlik, KVKK, log maskeleme, güvenlik, yetki ayrılığı (SoD), veri imhası, yedek/geri dönüş, olay kaydı ve denetim temel politikalarını belirle; süre/eşik gibi onay bekleyen parametreleri `DECISION_REQUIRED` bırak.
- Yazılımın sonraki aşamalarda kanıt eksik olsa dahi **izole DEV-LAB ortamında geliştirilmesine** izin veren çalışma disiplini tanımla; bu, canlı entegrasyon veya gerçek kurumsal kabul izni değildir.
- Gerçek bariyer, PSP capture, e-belge issuance, ERP posting ve split-settlement bayrakları örnek yapılandırmada **varsayılan false** olsun. Güvenlik interlockları kapatılamaz.
- `P00-delivery-report.md` dosyasında bu aşamada neyin yapıldığı, neyin yapılmadığı ve devam için neyin gerektiği ayrı başlıklar olsun.

### 8. İsteğe bağlı, tamamen yalıtılmış P00 önizlemesi

Google AI Studio canlı önizleme için web arayüzü oluşturmayı gerektiriyorsa `web/preview-only/` altında bir **salt-okunur P00 çalışma durumu** ekranı hazırlanabilir:

- Ferah, modern, profesyonel, açık zemin, iyi tipografi; yoğun/karmaşık paneller, yapay ikon kalabalığı yok.
- Üstte `Kampüs PTS — Proje Temeli / P00` başlığı ve görünür `TASLAK / CANLI DEĞİL` ifadesi.
- Yalnız referanstan türetilen REQ/NFR/DEC/BLK sayıları, G0 `NOT_APPROVED`, A1–A10/K-01–K-12 özetleri ve sonraki P01 başlığı.
- Ekran gösterim amaçlı; kimlik doğrulama, ödeme, bariyer, tarife, gerçek listeleme ve yetki verme operasyonu içermez.
- Önizleme ile asıl platform kodunu karıştırma; Node/mock sunucuyu gerçek .NET sistemi gibi temsil etme.

### 9. P00 otomatik kalite kontrolleri

Aşağıdaki doğrulamaları **gerçek komut çalıştırılabildiği ölçüde** hazırla ve çalıştır:

1. `python3 tools/validate_p00.py` — dosya varlığı, CSV şema/ID/tekillik, referans bütünlüğü, 40/16/31/15/8/10/56/10 sayıları, karar/blokaj/test/kapı durumları, JSON ve özellik bayrağı kontrolleri.
2. `python3 -m unittest tests.test_validate_p00 -v` veya projeye uygun eşdeğer P00 unittest komutu.
3. `python3 tools/build_manifest.py` — kaynak dosyaların SHA-256 manifestini üret (manifestin kendisini manifest içinde hash'leme; rastlantısal yedek/cache dosyaları ekleme).
4. `python3 -m json.tool config/features.example.json` ve olay zarfı JSON dosyası doğrulaması.
5. Salt P00 statik kontrollerini yapan `.github/workflows/p00-validation.yml` taslağı. CI konfigürasyonunu oluşturmak gerçek CI koşusunu kanıtlamaz.

Her komut için `EXECUTED_PASS`, `EXECUTED_FAIL`, `NOT_RUN` veya `NOT_AVAILABLE` + kısa gerçek hata/çıktı bilgisi yaz. P00 doğrulaması **yalnız yapısal/dokümantasyon testidir**. `.NET build`, `React build`, PostgreSQL, gerçek cihaz, PSP/e-belge/ERP testlerini P00 `PASS` olarak işaretleme.

### 10. Kesin kabul kriterleri

P00 tesliminden önce şu 16 maddeyi tek tek değerlendir:

1. Referans dosyaları ve sürüm/bağlam okunduğu gerçekten doğrulandı.
2. Proje charter kapsamı ile kapsam dışı işlemler ayrı yazıldı.
3. A1–A10 ve K-01–K-12 bütünlüğü korundu.
4. ASP.NET Core/.NET 10 + PostgreSQL 16+ + React/TS hedef mimari açık.
5. Modül-veri otoritesi ve ASManager/PTS/ERP sorumlulukları doğru ayrıldı.
6. `PLATE_RECOGNIZED`, `PASSAGE_CONFIRMED`, `GATE_ACK` farkı korundu.
7. Gelir sahibi, merchant, tahsilatçı, issuer ve muhasebe sorumlusu karıştırılmadı.
8. 40 REQ ve 16 NFR tam ve tekil.
9. 31 DEC, 15 RISK, 8 BLK tam ve statüleri dürüst.
10. 10 TC `NOT_RUN`; 56 izlenebilirlik satırı eksiksiz.
11. G0 onaysız, G1–G9 başlamamış; sahte onay veya EVD yok.
12. Tüm gerçek etkili özellik bayrakları false.
13. KVKK, SoD, audit ve PII/secret koruma esasları yazıldı.
14. Validator, test ve SHA-256 komutlarının durumu gerçeğe uygun.
15. Sonraki P01 için keşif ve bilgi ihtiyacı listesi mevcut.
16. P00 dışında P01–P76 işlevleri çalışıyor iddiası yok.

Eksik/kısmi olan kriterleri açık hata listesine yaz; eksikliği gizlemek için göstermelik kod, demo ödeme, demo cihaz ya da sahte test raporu üretme.

### 11. Zorunlu yanıt/teslim protokolü

Dosyaları gerçekten çalışma alanına kaydettikten sonra şu sırada dön:

**A. P00 özeti:** Amaç, alınan referans, mimari kararlar, gerçek P00 durumu.

**B. Dosya envanteri:** Oluşturulan/değiştirilen dosyaların tam yolları; mevcut referans üzerinden aynen korunanları ayrıca belirt.

**C. Kapsam:** Başarılan işler, yapılmayan işler, `DECISION_REQUIRED` ve `BLOCKER` listeleri.

**D. Test kaydı:** Gerçek komut + çalışma ortamı + gerçek sonuç; çalıştırılamayanlarda `NOT_RUN/NOT_AVAILABLE`.

**E. İzlenebilirlik:** REQ/NFR→TC/EVD→Gate genel durum özeti ve sayımlar.

**F. Risk ve güvenlik:** Yanlış varsayım veya canlı işlem riski; uygulanan koruma.

**G. Devam kapısı:** `P00_SOURCE_READY`, `P00_REVIEW_REQUIRED` veya `P00_INCOMPLETE` gibi dürüst bir kaynak-durum değerlendirmesi; **G0=NOT_APPROVED** korunur.

**H. Teslim:** Düzenlenebilir kaynak ZIP dosyası (tercihen `KampusPTS_P00_v1.0.zip`), içerik manifesti, P00 teslim raporu; ZIP oluşturma/dışa aktarma imkânı yoksa bunu açıkça belirt. Taslak ekranın ekran görüntüsünü kaynak dosya teslimi yerine kullanma.

**Burada DUR.** P01'i, P02'yi ya da diğer aşamaları kendiliğinden oluşturma. Kullanıcı çıktıyı bağımsız olarak incelettikten sonra sonraki promptu verecek. 
