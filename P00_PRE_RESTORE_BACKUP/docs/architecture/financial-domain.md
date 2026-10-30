# Finansal Etki Alanı ve Durum Makinesi (Financial Domain Model)

Bu belge, Kampüs PTS Gelir Yönetim Platformu'nun finansal nesnelerini, durum geçişlerini ve alt defter muhasebe mantığını açıklar (K-06, K-08).

---

## 1. Finansal Nesne Yaşam Döngüsü

Her finansal işlem birbirinden bağımsız ve kesin sınırlarla ayrılmış şu 8 aşamalı yaşam döngüsünü takip eder:

```text
[Quote] ──▶ [Charge] ──▶ [PaymentIntent] ──▶ [PaymentTransaction]
                                                      │
                                                      ▼
[ERPPosting] ◀── [JournalEntry] ◀── [Invoice] ◀── [ProviderSettlement]
```

### Aşama Tanımları:
1. **Quote (Teklif):** Aracın otoparkta kaldığı süre ve uygulanan tarifeye göre hesaplanan tahmini ücret. Fatura veya borç doğurmaz.
2. **Charge (Borç Tahakkuku):** Geçiş kanıtı ile kesinleşen mali oturum sonucu aboneye veya misafire tahakkuk ettirilen nihai alacak tutarı.
3. **PaymentIntent (Ödeme Niyeti):** Ödeme oturumu başlatıldığında üretilen, kriptografik `idempotencyKey` taşıyan rezervasyon nesnesi.
4. **PaymentTransaction (Ödeme Hareketi):** Lisanslı PSP'ye gönderilen istek ve sağlayıcıdan dönen ham işlem referansı.
5. **ProviderSettlement (Sağlayıcı Takası):** PSP tarafından paranın tahsil edildiği ve banka hesabına aktarım sürecine alındığı teyidi (`CAPTURED` ≠ `SETTLED`).
6. **Invoice (Fatura):** VUK uyarınca GİB formatında düzenlenen e-Fatura veya e-Arşiv faturası.
7. **JournalEntry (Alt Defter Fişi):** PTS alt defterine işlenen, borç ve alacak hesapları denk (`double-entry`), silinemez yevmiye kaydı.
8. **ERPPosting (ERP Muhasebe Aktarımı):** Kurumsal ERP sistemine resmi defter kaydı olarak gönderilen ve ERP fiş numarası ile eşleşen durum.

---

## 2. Alt Defter (Sub-ledger) Çift Taraflı Kayıt Örneği

Örnek 100,00 TL otopark tahsilatı için PTS alt defter fiş yapısı:

| Hesap Kodu | Hesap Adı | Borç (Minor Unit: Kuruş) | Alacak (Minor Unit: Kuruş) |
|:---|:---|:---:|:---:|
| **108.01.001** | Sanal POS Takas Hesabı (PSP) | 10.000 | 0 |
| **600.01.001** | Otopark Gelirleri Hesabı | 0 | 8.333 |
| **391.01.020** | Hesaplanan KDV (%20) | 0 | 1.667 |
| **TOPLAM** | Denk Fiş (`Balanced`) | **10.000** | **10.000** |

### Ters Kayıt (Reversal) İlkesi:
İptal veya iade durumunda mevcut fiş silinmez veya güncellenmez. Sistem otomatik olarak orijinal fiş referansıyla eşit ve ters yönde yeni bir fiş üretir:
- 108.01.001 Alacak: 10.000 kuruş
- 600.01.001 Borç: 8.333 kuruş
- 391.01.020 Borç: 1.667 kuruş
