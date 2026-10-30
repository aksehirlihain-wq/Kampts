# Kampüs PTS P00 Aktarım ve Denetim Yönergeleri (P00_IMPORT_AND_AUDIT.md)

Bu belge, Kampüs PTS Gelir Yönetim Platformu P00 aşamasının AI Studio çalışma alanına aktarımı, denetim araçları ve kabul kriterlerini açıklar.

---

## 1. Kaynak ve Erişim Durumu
- Çalışma alanında `KPTS_P00_v1_2_kanonik_dogrulandi.zip` fiziksel dosyası mevcut değildir. Bu durum **`REFERENCE_NOT_ACCESSIBLE`** olarak dürüstçe belgelenmiştir (K-09).
- Kanonik şemalar ve değişmezler, prompt talimatlarındaki kesin tanımlara göre restore edilmiş ve çalışma alanında doğrulanmıştır.

---

## 2. Doğrulama Komutları

Çalışma alanında aşağıdaki komutlar bağımsız olarak çalıştırılabilir:

```bash
# 1. Kaynak Bütünlüğü Denetimi
python3 KampusPTS/tools/audit_source_integrity.py

# 2. Kanonik Yapısal Doğrulayıcı
python3 KampusPTS/tools/validate_p00.py

# 3. Birim ve Regresyon Testleri (18 Test)
PYTHONPATH=KampusPTS python3 -m unittest discover -s KampusPTS/tests -v

# 4. Önizleme Verisi Üretimi
python3 KampusPTS/tools/generate_p00_preview.py

# 5. Manifest Üretimi ve Doğrulaması
python3 KampusPTS/tools/build_manifest.py
```

---

## 3. Yönetişim Durumu
- **Teknik Durum:** `P00_SOURCE_READY`
- **Kurumsal Onay:** `G0 = NOT_APPROVED` (Yetkili makam onayı ve DEC-001 kararı beklenmektedir)
- **Açık Kararlar:** 31 Karar (`DECISION_REQUIRED`, `actual_owner=TO_ASSIGN`)
- **Açık Blokajlar:** 8 Blokaj (`OPEN`)
- **Testler:** 10 Tasarlanmış Test (`NOT_RUN`, `evidence=NONE`)
