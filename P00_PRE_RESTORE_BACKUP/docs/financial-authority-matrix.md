# Mali Yetki ve Sorumluluk Matrisi (Financial Authority Matrix)

**Karar Referansı:** DEC-001, DEC-014, DEC-027, DEC-028  
**Durum:** `DECISION_REQUIRED` (Kurumsal Onay Bekleniyor)  
**Aşama:** P00  

---

## 1. Kavramsal Rol Ayrılığı İlkesi

Kampüs PTS mimarisinde finansal aktörler birbirine karıştırılamaz ve tek bir varlık olarak varsayılamaz. Her finansal işlemde aşağıdaki 7 rolün kim olduğu açık kontratlarla belirlenir:

1. **RevenueOwner (Gelir Sahibi):** Otopark gelirinin mülkiyetine yasal olarak sahip olan tüzel kişilik.
2. **Collector (Tahsilatçı):** Parayı ödeme aracından veya nakit kasasından fiilen toplayan taraf.
3. **MerchantOfRecord - MoR (Kayıtlı Satıcı):** Ödeme kuruluşu veya banka nezdinde sanal POS hesabının sahibi olan, kart ekstrelerinde adı görünen tüzel kişilik.
4. **SettlementBeneficiary (Hakediş Sahibi):** Banka veya PSP takası sonrasında net tutarın aktarıldığı nihai banka hesabı sahibi.
5. **InvoiceIssuer (Fatura/e-Belge Düzenleyen):** VUK uyarınca e-Fatura veya e-Arşiv faturasını tanzim eden mükellef.
6. **AccountingAuthority (Muhasebe Otoritesi):** Geliri resmi bilançosuna ve defterikebirine kaydeden yasal muhasebe birimi.
7. **TaxPolicyOwner (Vergi Politikası Sahibi):** KDV muafiyeti, tevkifat veya vergi oranlarını yasal olarak belirleyen makam.

---

## 2. DEC-001 Çoklu Model Seçenekleri (A / B / C / D)

Kurum üst yönetimi tarafından onaylanması gereken 4 olası model şöyledir:

| Model | RevenueOwner | MerchantOfRecord | InvoiceIssuer | SettlementBeneficiary | Açıklama |
|:---|:---|:---|:---|:---|:---|
| **Model A: Doğrudan Döner Sermaye** | Üniversite Döner Sermaye İşletmesi | Döner Sermaye İşletmesi | Döner Sermaye İşletmesi | Döner Sermaye Hesabı | Klasik kamu modeli. Tüm tahsilat ve faturalandırma doğrudan döner sermaye üzerinden yürütülür. |
| **Model B: Üniversite Geliştirme Vakfı / İktisadi İşletme** | Üniversite Vakfı İktisadi İşletmesi | Vakıf İktisadi İşletmesi | Vakıf İktisadi İşletmesi | Vakıf Ticari Hesabı | Otopark gelirlerinin vakıf iktisadi işletmesine aktarıldığı yapı. |
| **Model C: Özel İşletmeci (Yüklenici / İmtiyaz)** | Özel Otopark İşletmecisi A.Ş. | Özel İşletmeci A.Ş. | Özel İşletmeci A.Ş. | Özel İşletmeci (Üniversiteye pay aktarılır) | Kamu-özel işbirliği veya kiralama modeli. Faturayı işletmeci keser, üniversiteye kira/hasılat payı öder. |
| **Model D: Çoklu Kampüs / Hibrit Konsorsiyum** | Kampüse Göre Ayrışık (Merkez: Döner Sermaye, Ek Kampüs: İşletmeci) | Kampüse / Kapıya Göre Dinamik | İlgili Yetkili Mükellef | Ayrıştırılmış Banka Hesapları | Çoklu tüzel kişiliğin aynı yazılım platformunda kampüs/bölge bazlı ayrıştığı yapı. |

> **UYARI:** DEC-001 kurumsal üst yönetim tarafından resmi olarak karara bağlanana kadar sistem hiçbir modeli varsayılan kabul etmez. Mimari `TenantId` ve `LegalEntityId` alanlarını her işlemde zorunlu kılarak 4 modeli de destekleyecek esneklikte tutulmuştur.

---

## 3. Bağlantılı Kararlar ve Blokajlar

- **DEC-008:** Fiziksel bariyer kontrol otoritesi (Bariyer kumandası PTS mi, ASManager mı, donanım kontrolörü mü?) → `UNKNOWN`.
- **DEC-014:** PSP seçimi ve hakediş dağıtımı (Split-settlement) kuralları → `DECISION_REQUIRED`.
- **DEC-027:** Otopark dışı kampüs hizmetlerinin ücretlendirme yetkisinin hukuki sınırları → `DECISION_REQUIRED`.
- **DEC-028:** Kuruş yuvarlama politikası ve minor-unit hassasiyeti → `DECISION_REQUIRED`.
- **BLK-001:** DEC-001 kurumsal onayının henüz verilmemiş olması açık blokajdır.
