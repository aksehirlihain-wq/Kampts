# Değişiklik Yönetimi ve Kontrolü (Change Control Process)

**Aşama:** P00  
**İlgili Belgeler:** `templates/CR-template.md`, `templates/ADR-template.md`

---

## 1. Değişiklik Yönetim İlkeleri

1. **Geriye Dönük Sessiz Değişiklik Yasağı:** Proje kütüklerinde (`registries/*.csv`) yer alan hiçbir gereksinim, karar veya mimari kural gerekçesiz ve izsiz değiştirilemez veya silinemez.
2. **Kayıt ve Şeffaflık:** Her kapsam veya mimari değişiklik bir Değişiklik Talebi (`Change Request - CR`) veya Mimari Karar Kaydı (`ADR`) ile resmiyet kazanır.
3. **Etki Analizi:** Değişikliğin K-01..K-12 değişmezlerine, finansal durum makinesine ve ASManager izolasyonuna etkisi yazılı olarak analiz edilmelidir.

---

## 2. Değişiklik Yaşam Döngüsü

```text
[Yeni Talep] 
     │
     ▼
[CR Formu Tanzimi] ──▶ [Mali & Güvenlik Etki Analizi]
                             │
                             ▼
                    [Mimar ve Komite İncelemesi]
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
             [REJECTED]            [APPROVED]
                                        │
                                        ▼
                             [Kütük Güncelleme & ADR]
```

---

## 3. Acil Durum Değişiklikleri (Emergency Changes)
Üretim veya test ortamında güvenlik zaafiyeti veya veri kaybı riski durumunda mimarın onayıyla acil düzeltme yapılabilir. Düzeltme sonrası 24 saat içinde geriye dönük CR ve test kanıtı tamamlanmalıdır.
