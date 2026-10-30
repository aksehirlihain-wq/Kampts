# Proje Beratı (Project Charter) — Kampüs PTS Gelir Yönetim Platformu

**Proje Kodu:** KPTS  
**Aşama:** P00  
**Tarih:** 2026-10-30  
**Durum:** TASLAK / ONAY BEKLİYOR (`G0 = NOT_APPROVED`)

---

## 1. Projenin Amacı ve Vizyonu

Kampüs PTS, üniversite kampüslerinde otopark ve geçiş kontrol süreçlerinin mali yönetimini modern, güvenilir, mevzuata tam uyumlu ve denetlenebilir bir yazılım mimarisiyle dijitalleştirmeyi amaçlar. Proje, plaka tanıma kameralarından gelen gözlem verilerini sahadaki fiziksel geçiş kanıtlarıyla eşleştirerek güvenilir otopark mali oturumları oluşturur; ücretlendirme, tahsilat, e-belge düzenleme ve kurumsal ERP muhasebe kayıtlarını tam mutabakat disipliniyle yürütür.

---

## 2. Kapsam Dahili (In-Scope)

1. **Plaka Gözlemi ve Geçiş Kanıtı Ayrıştırma:** LPR kameralarından (`GV-LPR2812-DL`) gelen plaka okumaları ile sensör/döngü geçiş kanıtlarının korelasyonu.
2. **Otopark Mali Oturum Yönetimi:** Giriş-çıkış zamanlarının tespiti, süre hesabı, serbest süre ve tolerans kuralları.
3. **Mali Hak ve Tarife Motoru:** Abone, personel, öğrenci, misafir ve ticari araçlar için tarife kuralları, istisnalar ve indirimler.
4. **Çoklu Tahsilat Altyapısı (PSP Entegrasyon Portları):** Sanal POS, mobil ödeme ve temassız QR ödeme süreçleri için güvenli, idempotent adaptör arayüzleri.
5. **e-Fatura / e-Arşiv Portları:** 509 Sıra No'lu VUK Genel Tebliği ve GİB standartlarına uygun mali belge üretim sözleşmeleri.
6. **PTS Alt Defteri (Sub-ledger):** Çift taraflı muhasebe kaydı (`double-entry`), silinemez yevmiye hareketleri ve ters kayıt (`reversal`) disiplini.
7. **ERP Entegrasyonu:** Kurumsal muhasebe sistemine periyodik veya anlık fiş aktarımı ve mutabakat raporları.
8. **Denetim ve İhlal Takibi:** Yetkisiz geçiş, bariyer ihlali, kaçak geçiş tespiti ve uyuşmazlık çözümü.

---

## 3. Kapsam Dışı (Out-of-Scope)

Aşağıdaki unsurlar kesinlikle Kampüs PTS yazılım kapsamı dışındadır:
1. **ASManager Veritabanına Doğrudan Müdahale:** ASManager 6.3.0 fiziksel erişim yetkilerinin tek sahibidir; PTS asla ASManager veritabanına SQL yazmaz veya iç tablolarını değiştirmez.
2. **Fiziksel İSG ve Donanım Güvenlik Sensörlerinin İptali:** Yangın, deprem, elektrik kesintisi veya araç sıkışma sensörlerinin (fotosel/loop) yazılımla bypass edilmesi yasaktır.
3. **Kart Bilgisi Saklama:** Kredi kartı PAN/CVV bilgileri sistem veritabanlarında kesinlikle saklanmaz (PCI-DSS Kapsam İzolasyonu).
4. **Hukuki Dayanağı Olmayan Otopark Dışı Ücretlendirme:** İdari ve hukuki onayı bulunmayan yaya, yemekhane veya kampüs içi diğer hizmetler PTS üzerinden ücretlendirilemez (`DEC-027`).
5. **Nihai Yasal Muhasebe Defteri Olma:** PTS bir alt defterdir (`sub-ledger`); kurumun nihai yasal bilançosu ve mizanı yetkili kurumsal ERP üzerinde tutulur.

---

## 4. Temel Paydaşlar ve Yetki Alanları

| Paydaş Rolü | Temsil Ettiği Alan | Yetki ve Sorumluluk |
|:---|:---|:---|
| Rektörlük / Üst Yönetim | Kampüs İdaresi | Nihai mali model (DEC-001) ve tarife onayı |
| Döner Sermaye İşletmesi | Mali Otorite | Hasılat sahibi, e-belge düzenleyici ve banka hesabı yetkilisi |
| Bilgi İşlem Daire Başkanlığı | BT Altyapısı | Sunucu, ağ, yedekleme ve sistem güvenliği |
| Güvenlik Şube Müdürlüğü | Fiziksel Güvenlik | Saha güvenliği, kapı geçişleri ve ASManager operasyonu |
| Yüklenici / Özel İşletmeci | Operatör (Opsiyonel) | Sözleşmeye bağlı işletme ve ilk seviye saha desteği |
| ERP / Finans Ekibi | Muhasebe | Alt defter hesap planı eşleşmesi ve mutabakat onayı |

---

## 5. Proje Başarı Kriterleri

- **Sıfır Çift Tahsilat:** Idempotency anahtarlarıyla mükerrer çekim riskinin %0 olması.
- **Kayıpsız Mali İzlenebilirlik:** Her tahakkuk ve ödemenin değişmez alt defter fişiyle ERP'ye bağlanabilmesi.
- **Yüksek Süreklilik:** Ağ kesintisinde yerel arabellek (`local buffer`) ile veri kaybı yaşanmaması.
- **Tam Mevzuat Uyumu:** KVKK, VUK ve PCI-DSS ilkelerine tam riayet.
