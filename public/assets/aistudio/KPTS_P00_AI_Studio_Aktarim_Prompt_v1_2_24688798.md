# KAMPÜS PTS — P00 v1.2 KANONİK KAYNAK AKTARIMI VE BAĞIMSIZ KABUL PROMPTU

**YALNIZ P00. P01–P76 KODLAMASINA GEÇME.** Bu bir sıfırdan içerik üretim promptu değildir. Bana verilen `KPTS_P00_v1_2_kanonik_dogrulandi.zip` içindeki **gerçek kaynak dosyalarını aynı isim, yol ve içerikle koruyarak** AI Studio çalışma alanına aktarma ve doğrulama görevidir.

## 1 — İlk iş: erişim durumunu bildir

Bu pakette çalışma alanı kökünde şunlar bulunmalıdır:

- `P00_REFERENCE/` — seçilen 56 **değişmez orijinal** kaynak dosya.
- `file-sha256.json` — bu 56 dosyanın sabit SHA-256 kontrol listesi.
- `KampusPTS/` — 49 orijinal P00 çalışma dosyası + yeni ve ayrı denetim/görselleştirme araçları.
- `KampusPTS/tools/audit_source_integrity.py` — 56 referans ve 49 çalışma dosyasını **referansın sabit hash listesiyle** karşılaştırır.
- `KampusPTS/tools/validate_p00.py` — özgün P00 yapısal doğrulayıcı; kesinlikle üzerine yazma.
- `KampusPTS/tools/generate_p00_preview.py` — orijinal CSV/Markdown'dan önizleme anlık görüntüsünü türetir.
- `src/App.tsx` ve `src/data/p00-canonical.json` — yalnız React/TypeScript önizlemesi.
- `KampusPTS/docs/reviews/P00-independent-restoration-2026-10-30.md` — teknik kaynak taşıma incelemesi.
- `P00_IMPORT_AND_AUDIT.md` — aktarım ve denetim yönergeleri.

**ZIP'i gerçekten açıp dosya olarak erişemiyorsan** `REFERENCE_NOT_ACCESSIBLE` bildir ve sahte belgeler üretme. Dosyaları kullanıcının açıp kaynak depo olarak eklemesini iste; kaynakları sıfırdan oluşturma, komut çalıştırılmış gibi yapma. Bir ZIP dosyasının adını görmek içerdiği dosyaları okuduğun anlamına gelmez.

## 2 — Kesin kaynak üstünlüğü / silme yasağı

1. `P00_REFERENCE/**` ve `file-sha256.json` **hiç değiştirilemez**.
2. `KampusPTS/` altındaki 49 orijinal çalışma dosyası **bayt-bayt aynı kalmalıdır**. Orijinal hashler `file-sha256.json` içindedir.
3. Araç, önizleme veya yeni test gerekiyorsa **yeni dosyada** üret. 49 kanonik çalışma dosyasını kendi cümlelerinle yeniden yazma, CSV kolonlarını değiştirme, ID'leri farklı anlama kaydırma.
4. `README.md` ve `AGENTS.md` geçmiş P00–P76 bağlamından alıntı içerebilir; bunlar ilgili aşamaların bu yeni uygulamada tamamlandığına dair kanıt değildir.
5. `KampusPTS/docs/reviews/SUPERSEDED_P00-v1.1_AI_Studio.md` yanlış eski başarı iddialarını arşivler; onu güncel kurumsal kanıt olarak gösterme.
6. Beklenmeyen bir hash farkı varsa önce değişen dosyayı dosya yolu ve beklenen/elde edilen hash ile raporla; otomatik yeniden yazma.

## 3 — Kanonik anlamı değiştirme

Orijinal kolon ve kayıtları **aynı** tut:

- `requirements.csv` (40): `REQ-001` **Kapsam/Yönetişim**, `REQ-002` **Kurumsal otorite**.
- `nfr.csv` (16): `NFR-001` **Kimlik ve oturum**; `domain`, `target_status`, `verification` kolonlarını koru.
- `decisions.csv` (31): `DEC-001` konusu **Kurum türü ve gelir sahibi tüzel kişilik**, seçenekler **A Üniversite; B Döner sermaye; C Özel işletmeci; D Çoklu tüzel kişilik**. `DEC-002` ise e-Fatura/e-Arşiv belge türü ve düzenleme zamanı; ASManager protokolü değildir.
- `risks.csv` (15), `blockers.csv` (8), `test-cases.csv` (10), `traceability.csv` (56), `gates.csv` (10) orijinal kolon, ilişki ve durumlarını koru.
- `docs/governance/foundational-invariants.md` içinde `K-01 = Fiziksel ve mali otorite ayrılığı`, `K-02 = Marka bağımsızlığı`, `K-12 = Test ve kanıt doğruluğu`. A1–A10 ile K-01–K-12'yi numara eşlemesiyle birleştirme.
- `docs/governance/gates.md` aşama/kanıt/imza eşlemesinin otoritesidir; `gates.csv` onay durumlarının kaynağıdır: `G0=P00`, `G1=P01–P04`, `G2=P05–P06`, `G3=P07–P10`, `G4=P11–P15`, `G5=P16–P19`, `G6=P20–P22`, `G7=P23–P28`, `G8=P29–P31`, `G9=P32–P33`.
- `G0=NOT_APPROVED`, `G1..G9=NOT_STARTED`, `DECISION_REQUIRED=31`, `BLK OPEN=8`, `TC NOT_RUN=10`. `P00_SOURCE_READY` bir dosya-bütünlük sonucu olsa dahi kurum onayı değildir.

## 4 — Mimari ve güvenlik çerçevesi

Hedef: .NET 10 / ASP.NET Core, PostgreSQL 16+, React + TypeScript, sahada GV-ASManager 6.3.0/GV-LPR2812-DL üretici kanıtına bağlı adaptörler. P00'da .NET backend çalışıyor iddiasında bulunma; React UI sadece `PREVIEW_ONLY` statik bir pano.

Şunlar değişmez:

- GV-ASManager fiziksel yetki otoritesi, PTS mali/oturum sınırları, ERP resmi muhasebe otoritesi. ASManager DB'ye yazmak ve belgelenmemiş API hayal etmek yasaktır.
- `PLATE_RECOGNIZED ≠ PASSAGE_CONFIRMED ≠ GateAck`; `financial=ACTIVE ≠ access=VERIFIED_ACTIVE`.
- `CAPTURED ≠ SETTLED`; `Quote/Charge/PaymentIntent/PaymentTransaction/Settlement/Invoice/Journal/ERPPosting` ayrı gerçeklerdir. S2S banka teyidi olmadan ödeme `SUCCESS` olmaz.
- Yayımlanmış finans kayıtları silinmez, ters kayıt kullanılır; modül veri sahipliği korunur.
- İSG ve bariyer güvenlik sensörleri bypass edilmez; KVKK, en az veri, görev ayrılığı, audit, idempotency korunur.
- `config/features.example.json` içindeki **beş gerçek işlem bayrağı false** kalır. Gerçek cihaz, kart, TCKN, plaka, banka/PSP sırrı ve kişisel veriler uygulamaya eklenmez.
- `UNKNOWN ≠ FALSE`, `NOT_RUN ≠ PASS`, `DESIGNED ≠ TESTED`, `AI ≠ InstitutionalAuthority`.

## 5 — Önizleme ve veri kökeni

`src/App.tsx` mevcut modern, sade P00 önizlemesini korusun. `src/data/p00-canonical.json` **yalnızca** `KampusPTS/tools/generate_p00_preview.py` ile orijinal çalışma dosyalarından türetilir. Canlı API'ye bağlanma, kullanıcı bilgisi/sahte ekran kaydı ekleme, hayali onay veya test durumu yazma. Kayıt sayıları ve başlıklar doğrudan kaynak türetimiyle görünmeli. `P00_REFERENCE` orijinal hash kontrolünden geçmediğinde başarı rozeti gösterme.

Yeni frontend değişikliği gerekiyorsa erişilebilir, mobil uyumlu, sade ve ferah düzeni koru. Yetkisiz işlem yapabilen düğme ekleme; statik verilerle canlı ödeme/kapı çalışıyor izlenimi verme. P00 ekranı ileriki aşamaların gerçek uygulama paneli değildir.

## 6 — Komutları gerçekten çalıştır ve raporla

Repo kökünden:

```bash
cd KampusPTS
python3 tools/audit_source_integrity.py
python3 tools/validate_p00.py
python3 -m unittest discover -s tests -v
python3 tools/generate_p00_preview.py
python3 tools/build_manifest.py
sha256sum -c manifest.sha256
cd ..
npm install
npm run lint
npm run build
```

- `audit_source_integrity.py` sonucu **REFERENCE=56/56 WORKSPACE=49/49** olmadan `P00_SOURCE_READY` iddia etme.
- Orijinal P00 validator yalnız **yapısal** denetimdir; .NET build, gerçek PostgreSQL, PSP S2S, e-belge, ERP, bariyer, İSG, sahada pilot ve G0 onayı **ayrı ve bu aşamada NOT_RUN**.
- Her komut için gerçekten çalıştırılıp çalıştırılmadığını, çıkış kodunu, hata varsa gerçek stderr/stdout özetini yaz. Ortamda paketler yoksa `NOT_AVAILABLE` veya `NOT_RUN`; `PASS` uydurma.
- `npm install` çalıştırdıysan ve `package-lock.json` oluştuysa kilit dosyasını teslim et; bağımlılık kaynağı ve derleme sorunu varsa ayrı öner.
- `manifest.sha256` ile 56 kaynağın sabit hash listesi **farklı iki denetimdir**. Salt manifestin PASS olması 56/49 doğruluğu değildir.
- Önceki geçersiz `18/18` test sonucunu bu yeni paketin son test sonucu gibi aktarma.

## 7 — Teslim ve durma kuralı

Aşağıdakileri **tamamını** kullanıcıya göster:

1. Eksiksiz dosya envanteri (ilgili yollar, yüklenen/eksik dosyalar).
2. SHA-256 denetimi (56/56, 49/49) ve orijinal P00 validator sonucu.
3. Yeni unit/regresyon testlerinin gerçek sayısı; `npm run lint/build` sonucu veya NOT_RUN/NOT_AVAILABLE nedeni.
4. Kaynak verisinden türetilen `REQ-001`, `REQ-002`, `DEC-001`, `DEC-002`, `K-01`, `K-02`, `K-12`, `G1`, `G9` örnekleri.
5. `G0=NOT_APPROVED`, açık DEC/BLK ve tüm canlı özelliklerin kapalı olduğu bilgisi.
6. Kaynak ZIP'i, sadece ekran görüntüsünü değil. Yeni ZIP adı `KPTS_P00_v1.2_AIStudio_export.zip` olabilir. `P00_REFERENCE`, `file-sha256.json`, `KampusPTS`, `src`, `package.json`, `index.html` ve test araçları içinde bulunmalı.

**Geliştirme burada duracak.** Kullanıcı ChatGPT'de teknik çıktıyı bağımsız denetime sunmadan P01'e başlamayacaksın.
