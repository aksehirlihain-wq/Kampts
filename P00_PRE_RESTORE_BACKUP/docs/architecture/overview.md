# Mimari Genel Bakış (Architecture Overview)

**Hedef Mimari:** Modüler Monolit (Modular Monolith)  
**Backend Çatısı:** ASP.NET Core / .NET 10 LTS (C# 13)  
**Veri Tabanı:** PostgreSQL 16+ (Entity Framework Core, Mantıksal Şema İzolasyonu)  
**İstemci:** React + TypeScript (Tailwind CSS)  
**Mesajlaşma:** Transactional Outbox + Dayanıklı Olay Zarfı (`event-envelope.schema.json`)

---

## 1. Modüler Monolit Yapısı ve Bağımlılık Yönü

Kampüs PTS, modüler monolit prensiplerine göre tasarlanmıştır. Her modül kendi bağımsız etki alanına (Domain) ve verisine sahiptir.

```text
               ┌───────────────────────────────┐
               │    Hosts.Api / Hosts.Worker   │
               └───────────────┬───────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌─────────────────────────┐           ┌─────────────────────────┐
│ Modules.LprObservation  │           │  Modules.FinancialCore  │
│  ├── Application        │           │   ├── Application       │
│  ├── Domain             │           │   ├── Domain            │
│  └── Infrastructure     │           │   └── Infrastructure    │
└─────────────────────────┘           └─────────────────────────┘
            │                                     │
            └──────────────────┬──────────────────┘
                               ▼
                   ┌───────────────────────┐
                   │     SharedKernel      │
                   │ (Teknik Primitifler)  │
                   └───────────────────────┘
```

### Bağımlılık Kuralları:
- `Hosts.Api / Hosts.Worker` → `Modules.*.Application` → `Modules.*.Domain`
- `Infrastructure`, `Application` katmanında tanımlı port ve arayüzleri uygular.
- Modüller hiçbir koşulda birbirlerinin `Infrastructure` veya veritabanı tablolarına bağlanamaz.
- `SharedKernel` yalnızca teknik primitifleri (idempotency tipleri, para birimi değer nesneleri, base entity, event envelope) içerir; iş kuralı içermez.

---

## 2. Modül Sorumlulukları

1. **Modules.LprObservation:** LPR kameralarından (`GV-LPR2812-DL`) gelen plaka okumalarını (`PLATE_RECOGNIZED`) alır, görüntü hash'ini ve metadata'yı saklar.
2. **Modules.PassageEvidence:** Sensör, fotosel ve döngü verilerini işler; gözlemle eşleştirerek kesin geçiş kanıtı (`PASSAGE_CONFIRMED`) üretir.
3. **Modules.GateControl:** Bariyer kumanda ve durum geri bildirimlerini (`GateCommand`, `GateAck`) yönetir. DEC-008 çözülene kadar bariyer kumanda yetkisi kapalı tutulur.
4. **Modules.AccessSync:** ASManager 6.3.0 ile asenkron yetki senkronizasyonunu onaylı iş emirleri üzerinden yönetir (K-03, K-04).
5. **Modules.TariffEngine:** Otopark oturumunun süresine, araç tipine ve abone haklarına göre fiyat teklifi (`Quote`) ve borç tahakkuku (`Charge`) hesaplar.
6. **Modules.Payments:** Lisanslı PSP'lerle sanal POS, QR ve mobil ödeme akışlarını güvenli, idempotent olarak yürütür.
7. **Modules.Invoicing:** e-Fatura ve e-Arşiv entegratörü portları üzerinden 509 sayılı VUK tebliğine uygun fatura düzenleme süreçlerini yönetir.
8. **Modules.Subledger:** Borç/alacak denkliğini sağlayan, silinemez yevmiye kayıtları tutar (`double-entry sub-ledger`).
9. **Modules.ErpSync:** Kurumsal muhasebe sistemi (ERP) ile periyodik veya olay bazlı mutabakat ve yevmiye fişi aktarımı yapar.
10. **Modules.AuditLogging:** KVKK ve denetim loglarını değiştirilemez olarak kaydeder.

---

## 3. Zaman ve Para Birimi Standartları
- **Zaman:** Veritabanında `timestamptz` formatında UTC saklanır; arayüzde `Europe/Istanbul` yerel saatine dönüştürülür.
- **Para Birimi:** TRY kuruş değerleri `bigint` minor-unit (100 kuruş = 1 TL) olarak saklanır; float kullanılmaz. Vergi ve indirim oranları için `decimal` tipi kullanılır.
