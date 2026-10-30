# G1 Giriş Kontrol Listesi (G1 Input Checklist)

**Hedef Aşama:** P01 (Saha Keşfi, Cihaz Envanteri ve Entegrasyon Sınırları)  
**Ön Koşul:** G0 Kapısının Şartlı veya Tam Kabulü  
**Mevcut Durum:** `NOT_STARTED` (G0 henüz onaylanmadığı için P01 başlatılamaz)

---

## P01 Başlatılması İçin Gerekli Girdiler ve Bilgi İhtiyacı

Aşağıdaki veriler sahada veya ilgili birimlerce resmi olarak temin edilmeden P01 saha keşfi tamamlanamaz:

1. **Saha Kamera ve Kapı Envanteri:**
   - [ ] Mevcut tüm kapıların LPR kamera modelleri ve yazılım sürümleri (Örn: `GV-LPR2812-DL`).
   - [ ] Şerit genişlikleri, kamera montaj açıları ve aydınlatma durumu.
   - [ ] Manyetik döngü (loop) sensörlerinin fiziksel varlığı ve kontrol kartı bağlantı şeması.

2. **ASManager 6.3.0 Altyapı Bilgileri:**
   - [ ] ASManager sunucusunun IP adresi, ağ segmenti ve güvenlik duvarı kuralları.
   - [ ] Vendor tarafından onaylanmış SDK/API dokümantasyonu veya iş emri dosya protokolü.
   - [ ] Personel fiziksel kart ve plaka veri sözlüğü.

3. **Bariyer ve Güvenlik Donanımı İncelemesi:**
   - [ ] Bariyer motoru ve kontrol kartı marka/modeli (Örn: CAME, BFT, Magnetic).
   - [ ] Fotosel emniyet rölesi kuru kontak bağlantı noktaları.
   - [ ] Yangın alarm paneli tahliye rölesi arayüzü.

4. **Elektrik ve Ağ Altyapısı:**
   - [ ] Kapı kulübeleri KGK (UPS) yedekleme süresi ve jeneratör bağlantısı.
   - [ ] Fiber omurga ve yerel switch port kapasiteleri.
