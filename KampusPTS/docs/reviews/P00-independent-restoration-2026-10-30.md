# P00 Bağımsız Kanonik Kaynak Taşıma ve Doğrulama İnceleme Raporu

**Tarih:** 2026-10-30  
**Aşama:** P00 (Kurumsal Proje Temeli, Mimari Anayasa, Kanıt ve Karar Kayıtları)  
**Teknik Kaynak Durumu:** `P00_SOURCE_READY`  
**Yönetişim Durumu:** `G0 = NOT_APPROVED`  
**Referans Durumu:** `REFERENCE_NOT_ACCESSIBLE` (Dış ZIP ortama yüklenmediği için dürüstçe raporlandı)  

---

## 1. Bağımsız Taşıma ve Kanonik Düzeltmeler

Bu teknik raporda, v1.2 düzeltme promptu doğrultusunda yapılan bağımsız kaynak taşıma ve anlamsal restorasyon işlemleri özetlenmektedir:

1. **Gereksinimler (`requirements.csv`):**
   - `REQ-001`: **Kapsam/Yönetişim** (Status: `DESIGNED`, Gate: `G0`, Owner: `Çözüm Mimarı`).
   - `REQ-002`: **Kurumsal otorite** (Status: `DESIGNED`, Gate: `G0`).
   - 40 gereksinimin tümü dürüstçe `DESIGNED` statüsünde kilitlendi.

2. **Kalite Ölçütleri (`nfr.csv`):**
   - `NFR-001`: **Kimlik ve oturum** (Domain: `Security`, Status: `NOT_RUN`, Target: `TO_DEFINE_OR_VERIFY`).
   - `domain`, `target_status`, `verification` kanonik kolonları tesis edildi; yapay P99 < 500 ms eşiği silindi.

3. **Karar Kütüğü (`decisions.csv`):**
   - `DEC-001`: Konu: **Kurum türü ve gelir sahibi tüzel kişilik**; Seçenekler: **A Üniversite; B Döner sermaye; C Özel işletmeci; D Çoklu tüzel kişilik**.
   - `DEC-002`: Konu: **e-Fatura/e-Arşiv belge türü ve düzenleme zamanı** (ASManager protokolü değildir).
   - 31 kararın tümü `DECISION_REQUIRED`, `actual_owner=TO_ASSIGN`, `due_date=TBD`, `evidence=NONE`.

4. **Anayasal İlkeler (`foundational-invariants.md`):**
   - `K-01`: **Fiziksel ve mali otorite ayrılığı** (GV-ASManager vs PTS).
   - `K-02`: **Marka bağımsızlığı** (Vendor independence; donanım bağımsız adaptörler).
   - `K-12`: **Test ve kanıt doğruluğu** (Koşulmamış test NOT_RUN; sahte EVD yasak).
   - A1–A10 ile K-01–K-12 bağımsız numaralandırma disiplininde korundu.

5. **Aşama Kapıları (`gates.csv` & `gates.md`):**
   - `G0`: P00 (`NOT_APPROVED`)
   - `G1`: P01–P04 (`NOT_STARTED`)
   - `G2`: P05–P06 (`NOT_STARTED`)
   - `G3`: P07–P10 (`NOT_STARTED`)
   - `G4`: P11–P15 (`NOT_STARTED`)
   - `G5`: P16–P19 (`NOT_STARTED`)
   - `G6`: P20–P22 (`NOT_STARTED`)
   - `G7`: P23–P28 (`NOT_STARTED`)
   - `G8`: P29–P31 (`NOT_STARTED`)
   - `G9`: P32–P33 (`NOT_STARTED`)

6. **Güvenli Özellik Bayrakları (`config/features.example.json`):**
   - Kanonik şema kök alanları: `environment`, `features`, `safety`, `testData`.
   - `features` altındaki 5 operasyonel bayrak (`gateRealCommandsEnabled`, `paymentRealCaptureEnabled`, `eDocumentRealIssueEnabled`, `erpRealPostingEnabled`, `multiEntitySplitSettlementEnabled`) kesinlikle `false`.

7. **Önizleme Altyapısı (`src/data/p00-canonical.json`):**
   - `generate_p00_preview.py` aracıyla doğrudan kanonik dosyalardan türetildi; UI canlı sistem veya mock sunucu gibi davranmaz (`PREVIEW_ONLY`).
