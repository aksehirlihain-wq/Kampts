# Mali Yetki ve Sorumluluk Matrisi (Financial Authority Matrix)

**Karar Referansı:** DEC-001, DEC-014, DEC-027, DEC-028  
**Durum:** `DECISION_REQUIRED` (Kurumsal Onay Bekleniyor)  
**Aşama:** P00  

---

## 1. Kavramsal Rol Ayrılığı İlkesi

Kampüs PTS mimarisinde finansal aktörler birbirine karıştırılamaz ve tek bir varlık olarak varsayılamaz. Her finansal işlemde aşağıdaki 7 rolün kim olduğu açık kontratlarla belirlenir:

1. **RevenueOwner (Gelir Sahibi):** Otopark gelirinin mülkiyetine yasal olarak sahip olan tüzel kişilik.
2. **Collector (Tahsilatçı):** Parayı ödeme aracından veya kasadan fiilen toplayan taraf.
3. **MerchantOfRecord - MoR (Kayıtlı Satıcı):** Ödeme kuruluşu veya banka nezdinde sanal POS hesabının sahibi olan, kart ekstrelerinde adı görünen tüzel kişilik.
4. **SettlementBeneficiary (Hakediş Sahibi):** Banka veya PSP takası sonrasında net tutarın aktarıldığı nihai banka hesabı sahibi.
5. **InvoiceIssuer (Fatura/e-Belge Düzenleyen):** VUK uyarınca e-Fatura veya e-Arşiv faturasını tanzim eden mükellef.
6. **AccountingAuthority (Muhasebe Otoritesi):** Geliri resmi bilançosuna ve defterikebirine kaydeden yasal muhasebe birimi.
7. **TaxPolicyOwner (Vergi Politikası Sahibi):** KDV muafiyeti, tevkifat veya vergi oranlarını yasal olarak belirleyen makam.

---

## 2. DEC-001 Kanonik Model Alternatifleri (A / B / C / D)

Kurumsal üst yönetim tarafından onaylanması gereken 4 kanonik seçenek:

| Model | Tanım | RevenueOwner | MerchantOfRecord | InvoiceIssuer | Açıklama |
|:---:|:---|:---|:---|:---|:---|
| **A** | **Üniversite (Özel Bütçe)** | Üniversite Rektörlüğü | Üniversite Rektörlüğü | Üniversite Rektörlüğü | Doğrudan kamu özel bütçesi üzerinden yürütülen model. |
| **B** | **Döner Sermaye** | Döner Sermaye İşletmesi | Döner Sermaye İşletmesi | Döner Sermaye İşletmesi | Otopark gelirlerinin üniversite döner sermaye işletmesine kaydedildiği klasik kamu modeli. |
| **C** | **Özel İşletmeci** | Özel İşletmeci A.Ş. | Özel İşletmeci A.Ş. | Özel İşletmeci A.Ş. | İhale veya kiralama usulüyle özel şirkete devredilen, üniversiteye hasılat payı/kira ödenen model. |
| **D** | **Çoklu Tüzel Kişilik** | Kampüs/Bölge Bazlı Ayrışık | Dinamik (Yetkili Şirket/Birim) | İlgili Yetkili Mükellef | Kampüslere veya kapılara göre döner sermaye ve işletmeci yapısının birlikte çalıştığı konsorsiyum modeli. |

> **UYARI:** DEC-001 kurumsal üst yönetim tarafından resmi olarak karara bağlanana kadar sistem hiçbir modeli varsayılan kabul etmez (`DECISION_REQUIRED`). Yazılım mimarisi `tenantId` ve `legalEntityId` alanlarını zorunlu kılarak 4 seçeneği de destekleyecek şekilde tasarlanmıştır.

---

## 3. Bağlantılı Kararlar ve Blokajlar

- **DEC-008:** Fiziksel bariyer kontrol otoritesi (Bariyer kumandası PTS mi, ASManager mı, bağımsız PLC mi?) → `UNKNOWN`.
- **DEC-014:** PSP seçimi ve hakediş dağıtımı (Split-settlement) kuralları → `DECISION_REQUIRED`.
- **DEC-027:** Otopark dışı kampüs içi hizmetlerin ücretlendirilmesinin hukuki sınırları → `DECISION_REQUIRED`.
- **DEC-028:** Kuruş yuvarlama politikası ve minor-unit hassasiyeti → `DECISION_REQUIRED`.
- **DEC-031:** Alt defter ERP mutabakat sıklığı ve modu → `DECISION_REQUIRED`.
- **BLK-001:** DEC-001 kurumsal onayının henüz verilmemiş olması açık blokajdır.
