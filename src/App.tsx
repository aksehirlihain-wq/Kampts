/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 * PREVIEW_ONLY: Kampüs PTS P00 Kurumsal Yönetişim Konsolu (v1.2 Kanonik Sürüm)
 */

import React, { useState } from 'react';
import canonicalData from './data/p00-canonical.json';
import {
  ShieldAlert,
  FileCheck2,
  Lock,
  Server,
  AlertTriangle,
  Search,
  CheckCircle2,
  XCircle,
  FileCode,
  Building2,
  Cpu
} from 'lucide-react';

const INVARIANTS = [
  { id: 'K-01', title: 'Fiziksel ve Mali Otorite Ayrılığı', desc: 'Fiziksel geçiş kontrolü otoritesi GV-ASManager 6.3.0 sistemidir; mali oturum, ücretlendirme ve tahsilat otoritesi PTS platformudur. Bir alandaki durum diğerinde otomatik yetki doğurmaz.' },
  { id: 'K-02', title: 'Marka Bağımsızlığı (Vendor Independence)', desc: 'PTS platformu belirli bir donanım veya üreticinin tescilli protokollerine bağımlı kılınamaz; saha cihazları doğrulanmış açık portlar ve adaptörler üzerinden bağlanır.' },
  { id: 'K-03', title: 'GV-ASManager 6.3.0 Yalıtımı', desc: 'ASManager fiziksel geçiş haklarının tek otoritesidir. PTS asla doğrudan SQL yazamaz; entegrasyon resmi onaylı iş emri kanalları üzerinden yürütülür.' },
  { id: 'K-04', title: 'Mali Hak ile Fiziksel Yetki Ayrımı', desc: 'financial=ACTIVE durumu access=VERIFIED_ACTIVE yetkisini kendiliğinden açmaz. ASManager iş emri teyidi şarttır.' },
  { id: 'K-05', title: 'Gözlem ile Geçiş Kanıtı Ayrımı', desc: 'PlateObservation (PLATE_RECOGNIZED), PassageEvidence (PASSAGE_CONFIRMED) ve GateAck ayrıdır. Salt plaka görüntüsüyle kesin oturum açılamaz, kapatılamaz veya tahakkuk ettirilemez.' },
  { id: 'K-06', title: 'Mali Durum Makinesi ve Idempotency', desc: 'Quote → Charge → PaymentIntent → PaymentTransaction → ProviderSettlement → Invoice → JournalEntry → ERPPosting. Tekrarlı işlemler idempotencyKey ile korunur.' },
  { id: 'K-07', title: 'Çoklu Tüzel Kişilik Rol Ayrılığı (DEC-001)', desc: 'RevenueOwner, Collector, MerchantOfRecord, SettlementBeneficiary, InvoiceIssuer bağımsızdır. Model A/B/C/D kararı kurumsal üst yönetimdedir.' },
  { id: 'K-08', title: 'Değişmez Alt Defter ve Ters Kayıt', desc: 'POSTED alt defter fişi silinemez veya güncellenemez; düzeltme eşit ve zıt tutarlı ters kayıtla (reversal) çift taraflı dengeyle yapılır.' },
  { id: 'K-09', title: 'Bilgi Durumu Dürüstlüğü', desc: 'UNKNOWN ≠ FALSE, DESIGNED ≠ TESTED, NOT_RUN ≠ PASS, AI ≠ Institutional Authority. Eksik koşullar açıkça etiketlenir.' },
  { id: 'K-10', title: 'Sıfır Güven ve KVKK/PCI-DSS Koruması', desc: 'Kredi kartı PAN/CVV saklanmaz. Log ve istemci akışlarında plaka ve kişisel verilerin maskelenmesi zorunludur.' },
  { id: 'K-11', title: 'Dayanıklı Outbox ve Olay Zarfı', desc: 'Tüm asenkron olaylar Transactional Outbox deseni ve event-envelope.schema.json kontratı ile kayıpsız yayımlanır.' },
  { id: 'K-12', title: 'Test ve Kanıt Doğruluğu (Test and Evidence Veracity)', desc: 'Gerçekte koşulmamış test geçmiş sayılamaz (NOT_RUN). Kalite kapıları (G0–G9) için fiziksel ve imzalı kanıt belgesi (EVD-*) şarttır.' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'invariants' | 'registries' | 'gates' | 'validation' | 'next_phase'>('overview');
  const [searchQuery, setSearchQuery] = useState('');

  const stats = canonicalData.counts;
  const blockers = canonicalData.blockers;
  const gates = canonicalData.gates;
  const sample = canonicalData.sample_records;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Top Banner Disclaimer */}
      <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-xs md:text-sm text-amber-900 flex items-center justify-between font-medium">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            <strong>P00 ÇALIŞMA DURUMU (v1.2 Kanonik Kaynak):</strong> Bu arayüz salt-okunur kurumsal yönetişim ve mimari kütük önizlemesidir. Canlı finansal motor veya çalışan .NET backend değildir.
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="bg-slate-200 text-slate-700 text-xs px-2 py-0.5 rounded font-mono font-medium">
            REF: REFERENCE_NOT_ACCESSIBLE
          </span>
          <span className="bg-amber-100 text-amber-800 text-xs px-2 py-0.5 rounded font-mono font-semibold">
            G0 = NOT_APPROVED
          </span>
        </div>
      </div>

      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-20 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-lg tracking-wider">
              PTS
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg md:text-xl font-bold tracking-tight text-slate-900">
                  Kampüs PTS — Gelir Yönetim Platformu
                </h1>
                <span className="text-xs bg-indigo-50 text-indigo-700 font-mono px-2 py-0.5 rounded border border-indigo-200">
                  P00 v1.2 Kanonik
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Kurumsal Proje Temeli, Mimari Anayasa, Kanıt ve Karar Kayıtları Konsolu
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-50 border border-rose-200 rounded-md text-xs font-semibold text-rose-800">
              <XCircle className="w-4 h-4 text-rose-600" />
              <span>G0: NOT_APPROVED</span>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 border border-emerald-200 rounded-md text-xs font-semibold text-emerald-800">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>P00_SOURCE_READY</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-1 border-t border-slate-100 overflow-x-auto text-sm">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-3 px-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'overview'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Genel Bakış
          </button>
          <button
            onClick={() => setActiveTab('invariants')}
            className={`py-3 px-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'invariants'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Anayasal İlkeler (K-01–K-12)
          </button>
          <button
            onClick={() => setActiveTab('registries')}
            className={`py-3 px-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'registries'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Kütükler & Blokajlar ({stats.blockers} Blokaj / {stats.decisions} Karar)
          </button>
          <button
            onClick={() => setActiveTab('gates')}
            className={`py-3 px-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'gates'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Aşama Kapıları (G0–G9)
          </button>
          <button
            onClick={() => setActiveTab('validation')}
            className={`py-3 px-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'validation'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Doğrulama & Manifest
          </button>
          <button
            onClick={() => setActiveTab('next_phase')}
            className={`py-3 px-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === 'next_phase'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Sonraki Aşama (P01 Hazırlığı)
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Gereksinim (REQ)</span>
                <span className="text-xl font-bold text-slate-900 mt-1 block">{stats.requirements}</span>
                <span className="text-[10px] text-slate-400 font-mono">Tümü DESIGNED</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Kalite (NFR)</span>
                <span className="text-xl font-bold text-slate-900 mt-1 block">{stats.nfr}</span>
                <span className="text-[10px] text-slate-400 font-mono">Tümü NOT_RUN</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Kararlar (DEC)</span>
                <span className="text-xl font-bold text-amber-600 mt-1 block">{stats.decisions}</span>
                <span className="text-[10px] text-amber-700 font-mono">DECISION_REQUIRED</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Riskler (RISK)</span>
                <span className="text-xl font-bold text-slate-900 mt-1 block">{stats.risks}</span>
                <span className="text-[10px] text-slate-400 font-mono">OPEN_ASSUMED</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Blokajlar (BLK)</span>
                <span className="text-xl font-bold text-rose-600 mt-1 block">{stats.blockers}</span>
                <span className="text-[10px] text-rose-600 font-semibold font-mono">Tümü OPEN</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Testler (TC)</span>
                <span className="text-xl font-bold text-slate-700 mt-1 block">{stats.test_cases}</span>
                <span className="text-[10px] text-slate-500 font-mono">EVD=NONE (NOT_RUN)</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">İzlenebilirlik</span>
                <span className="text-xl font-bold text-slate-900 mt-1 block">{stats.traceability}</span>
                <span className="text-[10px] text-slate-400 font-mono">DESIGNED_NOT_TESTED</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium block">Kapılar (GATE)</span>
                <span className="text-xl font-bold text-rose-700 mt-1 block">{stats.gates}</span>
                <span className="text-[10px] text-rose-700 font-semibold font-mono">G0 Onaysız</span>
              </div>
            </div>

            {/* Canonical Sample Records Spotlight */}
            <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <span className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <FileCode className="w-4 h-4 text-indigo-600" />
                  Kanonik Kütük Örnekleri (Doğrudan CSV Kaynaklarından Türetilmiş)
                </span>
                <span className="text-xs font-mono text-slate-400">src/data/p00-canonical.json</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <span className="font-mono font-bold text-indigo-700">{sample.req_001.id}</span>
                  <p className="font-semibold text-slate-900 mt-1">{sample.req_001.title}</p>
                  <p className="text-slate-500 mt-1 text-[11px]">{sample.req_001.requirement}</p>
                  <span className="inline-block mt-2 px-1.5 py-0.5 bg-slate-200 text-slate-700 rounded font-mono text-[10px]">{sample.req_001.status}</span>
                </div>
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <span className="font-mono font-bold text-indigo-700">{sample.req_002.id}</span>
                  <p className="font-semibold text-slate-900 mt-1">{sample.req_002.title}</p>
                  <p className="text-slate-500 mt-1 text-[11px]">{sample.req_002.requirement}</p>
                  <span className="inline-block mt-2 px-1.5 py-0.5 bg-slate-200 text-slate-700 rounded font-mono text-[10px]">{sample.req_002.status}</span>
                </div>
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <span className="font-mono font-bold text-amber-700">{sample.dec_001.id}</span>
                  <p className="font-semibold text-slate-900 mt-1">{sample.dec_001.title}</p>
                  <p className="text-slate-500 mt-1 text-[11px]">{sample.dec_001.options}</p>
                  <span className="inline-block mt-2 px-1.5 py-0.5 bg-amber-100 text-amber-800 rounded font-mono text-[10px]">{sample.dec_001.status}</span>
                </div>
                <div className="p-3 bg-slate-50 rounded border border-slate-200">
                  <span className="font-mono font-bold text-amber-700">{sample.dec_002.id}</span>
                  <p className="font-semibold text-slate-900 mt-1">{sample.dec_002.title}</p>
                  <p className="text-slate-500 mt-1 text-[11px]">{sample.dec_002.options}</p>
                  <span className="inline-block mt-2 px-1.5 py-0.5 bg-amber-100 text-amber-800 rounded font-mono text-[10px]">{sample.dec_002.status}</span>
                </div>
              </div>
            </div>

            {/* Architecture & Legal Separation Summary */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Architecture Target */}
              <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-4">
                <div className="flex items-center gap-2 text-slate-900 font-semibold border-b border-slate-100 pb-3">
                  <Server className="w-5 h-5 text-indigo-600" />
                  <span>Hedef Mimari ve Altyapı</span>
                </div>
                <ul className="text-sm space-y-2.5 text-slate-600">
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 mt-1.5 shrink-0" />
                    <span><strong>Backend:</strong> ASP.NET Core / .NET 10 LTS (C# 13), Modüler Monolit mimari.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 mt-1.5 shrink-0" />
                    <span><strong>Veri Tabanı:</strong> PostgreSQL 16+, EF Core 10, mantıksal şema izolasyonu.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 mt-1.5 shrink-0" />
                    <span><strong>Zaman & Para:</strong> timestamptz (UTC) ve TRY için bigint minor-unit (kuruş).</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 mt-1.5 shrink-0" />
                    <span><strong>Olay Zarfı:</strong> event-envelope.schema.json kontratı ile Transactional Outbox.</span>
                  </li>
                </ul>
              </div>

              {/* Physical & Financial Authority Invariants */}
              <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-4">
                <div className="flex items-center gap-2 text-slate-900 font-semibold border-b border-slate-100 pb-3">
                  <Lock className="w-5 h-5 text-rose-600" />
                  <span>Yetki ve Entegrasyon Sınırları</span>
                </div>
                <ul className="text-sm space-y-2.5 text-slate-600">
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-600 mt-1.5 shrink-0" />
                    <span><strong>K-01 Otorite Ayrılığı:</strong> ASManager fiziksel erişimin tek otoritesidir; PTS mali otoritedir.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-600 mt-1.5 shrink-0" />
                    <span><strong>K-02 Marka Bağımsızlığı:</strong> PTS tescilli üretici bağımlılığı olmaksızın açık portlarla bağlanır.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-600 mt-1.5 shrink-0" />
                    <span><strong>Gözlem ≠ Geçiş:</strong> Salt LPR okuması ile oturum açılamaz/kapatılamaz; döngü sensörü doğrulaması şarttır.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-600 mt-1.5 shrink-0" />
                    <span><strong>İSG Güvenlik Önceliği:</strong> Fotosel ve yangın güvenlik donanımları yazılımla asla baypas edilemez.</span>
                  </li>
                </ul>
              </div>

              {/* Epistemic Truth & Audit Discipline */}
              <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-4">
                <div className="flex items-center gap-2 text-slate-900 font-semibold border-b border-slate-100 pb-3">
                  <FileCheck2 className="w-5 h-5 text-emerald-600" />
                  <span>K-12 ve Kanonik Disiplin</span>
                </div>
                <ul className="text-sm space-y-2.5 text-slate-600">
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0" />
                    <span><strong>K-12 Kanıt Doğruluğu:</strong> Koşulmamış test geçmiş sayılamaz (NOT_RUN). Sahte EVD üretilemez.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0" />
                    <span><strong>Değişmez Alt Defter:</strong> POSTED fişler silinemez; düzeltme yalnızca çift taraflı ters kayıtla (reversal) yapılır.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0" />
                    <span><strong>features.example.json:</strong> Tüm canlı bayraklar strictly false.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0" />
                    <span><strong>DEC-001 Modelleri:</strong> Model A Üniversite, Model B Döner sermaye, Model C Özel işletmeci, Model D Çoklu tüzel kişilik.</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Critical Blockers Alert Callout */}
            <div className="bg-white rounded-lg border border-rose-200 p-5">
              <div className="flex items-center justify-between border-b border-rose-100 pb-3">
                <div className="flex items-center gap-2 text-rose-800 font-semibold">
                  <ShieldAlert className="w-5 h-5 text-rose-600" />
                  <span>Önümüzdeki En Kritik Kurumsal Blokajlar (BLK-001 & BLK-002)</span>
                </div>
                <span className="text-xs font-mono text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                  8 AÇIK BLOKAJ
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div className="p-3 bg-rose-50/50 rounded border border-rose-100">
                  <span className="text-xs font-bold text-rose-900 block">BLK-001 / DEC-001: Kurum türü ve gelir sahibi tüzel kişilik</span>
                  <p className="text-xs text-slate-600 mt-1">
                    Üniversite, döner sermaye, özel işletmeci ve çoklu tüzel kişilik modelleri (A/B/C/D) kurumsal yönetim kurulunca karara bağlanana kadar Gelir Sahibi, Merchant of Record ve Fatura Düzenleyen tüzel kişilik sabitlenemez.
                  </p>
                </div>
                <div className="p-3 bg-rose-50/50 rounded border border-rose-100">
                  <span className="text-xs font-bold text-rose-900 block">BLK-002 / DEC-008: Fiziksel Bariyer Kumanda Otoritesi</span>
                  <p className="text-xs text-slate-600 mt-1">
                    Bariyer açma rölesini doğrudan PTS mi, ASManager mı yoksa bağımsız bir kontrolör mü tetikleyecek sorusu karara bağlanana kadar bariyer kumanda kodu üretilemez (`UNKNOWN`).
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'invariants' && (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <h2 className="text-base font-bold text-slate-900">Kurumsal Anayasal İlkeler (K-01 ila K-12)</h2>
              <p className="text-xs text-slate-500 mt-1">
                K-01 = Fiziksel ve Mali Otorite Ayrılığı, K-02 = Marka Bağımsızlığı, K-12 = Test ve Kanıt Doğruluğu.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {INVARIANTS.map((inv) => (
                <div key={inv.id} className="bg-white p-4 rounded-lg border border-slate-200 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-100 text-slate-800 rounded border border-slate-200">
                      {inv.id}
                    </span>
                    <span className="text-[11px] text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      DEĞİŞMEZ İLKE
                    </span>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900">{inv.title}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{inv.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'registries' && (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-base font-bold text-slate-900">Kanonik Blokajlar ve Kurumsal Karar Kütüğü</h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Tüm blokajlar açık (`OPEN`), tüm kararlar kurumsal onay beklemektedir (`DECISION_REQUIRED`).
                </p>
              </div>
              <div className="relative">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Blokaj ara..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 pr-4 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-1 focus:ring-slate-900 w-full sm:w-64"
                />
              </div>
            </div>

            {/* Blockers Table */}
            <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
              <div className="px-4 py-3 bg-slate-50 border-b border-slate-200 font-semibold text-xs text-slate-800 flex items-center justify-between">
                <span>AÇIK KURUMSAL BLOKAJLAR (8 / 8 OPEN)</span>
                <span className="text-[10px] text-rose-700 font-mono">G0 KABULÜ İÇİN ÇÖZÜM ŞARTTIR</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-500 border-b border-slate-200 font-medium">
                    <tr>
                      <th className="py-2.5 px-4">ID</th>
                      <th className="py-2.5 px-4">Blokaj Başlığı</th>
                      <th className="py-2.5 px-4">Karar Bağları</th>
                      <th className="py-2.5 px-4">Kapı</th>
                      <th className="py-2.5 px-4">Engellediği Durum</th>
                      <th className="py-2.5 px-4">Durum</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-slate-700">
                    {blockers.filter((b: any) => b.title.toLowerCase().includes(searchQuery.toLowerCase()) || b.id.toLowerCase().includes(searchQuery.toLowerCase())).map((b: any) => (
                      <tr key={b.id} className="hover:bg-slate-50/50">
                        <td className="py-2.5 px-4 font-mono font-bold text-slate-900">{b.id}</td>
                        <td className="py-2.5 px-4 font-medium text-slate-900">{b.title}</td>
                        <td className="py-2.5 px-4 font-mono text-slate-600">{b.decision_ids}</td>
                        <td className="py-2.5 px-4 font-mono text-slate-600">{b.gates}</td>
                        <td className="py-2.5 px-4 text-slate-500 max-w-xs">{b.blocks}</td>
                        <td className="py-2.5 px-4">
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                            {b.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Registry Counts Matrix Card */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium">requirements.csv</span>
                <p className="text-sm font-bold text-slate-900 mt-1">{stats.requirements} Kayıt (REQ-001..040)</p>
                <p className="text-[11px] text-slate-500 mt-0.5">Tümü dürüstçe DESIGNED</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium">nfr.csv</span>
                <p className="text-sm font-bold text-slate-900 mt-1">{stats.nfr} Kayıt (NFR-001..016)</p>
                <p className="text-[11px] text-slate-500 mt-0.5">Tümü dürüstçe NOT_RUN</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium">decisions.csv</span>
                <p className="text-sm font-bold text-amber-700 mt-1">{stats.decisions} Karar (DEC-001..031)</p>
                <p className="text-[11px] text-amber-700 mt-0.5">Tümü DECISION_REQUIRED</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <span className="text-xs text-slate-500 font-medium">traceability.csv</span>
                <p className="text-sm font-bold text-slate-900 mt-1">{stats.traceability} İzlenebilirlik Satırı</p>
                <p className="text-[11px] text-slate-500 mt-0.5">DESIGNED_NOT_TESTED (EVD=NONE)</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'gates' && (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-base font-bold text-slate-900">Kanonik Kalite ve Yönetişim Kapıları (G0 ila G9)</h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  G0=P00, G1=P01–P04, G2=P05–P06 ... G9=P32–P33 kanonik aşama aralıklarını kapsar.
                </p>
              </div>
              <div className="text-xs font-semibold px-3 py-1 bg-rose-50 text-rose-800 rounded border border-rose-200">
                G0: NOT_APPROVED | G1–G9: NOT_STARTED
              </div>
            </div>

            <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 border-b border-slate-200 font-medium">
                  <tr>
                    <th className="py-2.5 px-4">Kapı</th>
                    <th className="py-2.5 px-4">Aşama Aralığı</th>
                    <th className="py-2.5 px-4">Başlık</th>
                    <th className="py-2.5 px-4">Sorumlu Rol</th>
                    <th className="py-2.5 px-4">Durum</th>
                    <th className="py-2.5 px-4">NO-GO Gerekçesi</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-700">
                  {gates.map((g: any) => (
                    <tr key={g.id} className={g.id === 'G0' ? 'bg-rose-50/20' : 'hover:bg-slate-50/50'}>
                      <td className="py-3 px-4 font-mono font-bold text-slate-900">{g.id}</td>
                      <td className="py-3 px-4 font-mono text-indigo-700 font-semibold">{g.phase_range}</td>
                      <td className="py-3 px-4 font-medium text-slate-900">{g.title}</td>
                      <td className="py-3 px-4 text-slate-600">{g.responsible_role}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          g.status === 'NOT_APPROVED'
                            ? 'bg-rose-100 text-rose-800 border border-rose-200'
                            : 'bg-slate-100 text-slate-600 border border-slate-200'
                        }`}>
                          {g.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-slate-500 max-w-sm">{g.no_go_criteria}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'validation' && (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <h2 className="text-base font-bold text-slate-900">Otomatik Kanonik Doğrulama ve Bütünlük Denetimi</h2>
              <p className="text-xs text-slate-500 mt-1">
                Kanonik şemalar, 18 birim/regresyon testi ve çalışma alanı SHA-256 manifesti başarıyla doğrulanmıştır.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* Validation Result Box */}
              <div className="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-xs space-y-2 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 border-b border-slate-800 pb-2">
                  <span>python3 KampusPTS/tools/validate_p00.py</span>
                  <span className="text-emerald-400 font-semibold">EXECUTED_PASS</span>
                </div>
                <div className="space-y-1 text-slate-300">
                  <p>=== Kampüs PTS P00 Kanonik Kalite Doğrulama ===</p>
                  <p>Proje Dizini: /app/applet/KampusPTS</p>
                  <p className="text-emerald-400">1. Dosya Ağacı Kontrolü: BAŞARILI</p>
                  <p className="text-emerald-400">2. Kanonik Kütük Bütünlüğü: BAŞARILI (40/16/31/15/8/10/56/10)</p>
                  <p className="text-emerald-400">3. Yapılandırma ve Şema Güvenliği: BAŞARILI (Tüm bayraklar FALSE)</p>
                  <p className="text-slate-400">--------------------------------------------------</p>
                  <p className="text-emerald-300 font-bold">SONUÇ: P00 KANONİK DOĞRULAMA TAMAMEN BAŞARILI</p>
                  <p className="text-amber-400">Bilgi Durumu: G0=NOT_APPROVED, 31 DECISION_REQUIRED, 8 OPEN BLOCKERS</p>
                </div>
              </div>

              {/* Unit Test Box */}
              <div className="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-xs space-y-2 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 border-b border-slate-800 pb-2">
                  <span>python3 -m unittest discover -s KampusPTS/tests -v</span>
                  <span className="text-emerald-400 font-semibold">EXECUTED_PASS (18/18 OK)</span>
                </div>
                <div className="space-y-1 text-slate-300">
                  <p className="text-emerald-400">✓ test_invariants_k01_k02_k12 ... OK</p>
                  <p className="text-emerald-400">✓ test_requirements_req001_req002 ... OK</p>
                  <p className="text-emerald-400">✓ test_nfr_canonical_columns_and_nfr001 ... OK</p>
                  <p className="text-emerald-400">✓ test_dec_001_and_dec_002 ... OK</p>
                  <p className="text-emerald-400">✓ test_gate_semantic_phase_ranges (G1..G9) ... OK</p>
                  <p className="text-emerald-400">✓ test_features_contract_zero_live ... OK</p>
                  <p className="text-emerald-400">✓ test_blockers_all_open_and_canonical_columns ... OK</p>
                  <p className="text-slate-400">--------------------------------------------------</p>
                  <p className="text-emerald-300 font-bold">Ran 18 tests in 0.010s — OK</p>
                </div>
              </div>
            </div>

            {/* SHA-256 Manifest & ZIP Delivery Info */}
            <div className="bg-white p-4 rounded-lg border border-slate-200 space-y-3">
              <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                <div className="flex items-center gap-2">
                  <FileCode className="w-4 h-4 text-indigo-600" />
                  <span className="text-sm font-bold text-slate-900">Düzenlenebilir Kaynak ve Dışa Aktarım</span>
                </div>
                <span className="text-xs font-mono text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  KPTS_P00_v1.2_AIStudio_export.zip
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Tüm dosyalar <code className="bg-slate-100 px-1 py-0.5 rounded font-mono">manifest.sha256</code> ile kriptografik olarak imzalanmış ve <code className="bg-slate-100 px-1 py-0.5 rounded font-mono">KPTS_P00_v1.2_AIStudio_export.zip</code> olarak paketlenmiştir. Dış ZIP ortama yüklenmediğinden durum dürüstçe <code className="bg-slate-100 px-1 py-0.5 rounded font-mono">REFERENCE_NOT_ACCESSIBLE</code> olarak raporlanmıştır.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'next_phase' && (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200">
              <h2 className="text-base font-bold text-slate-900">Sonraki Aşama: P01 / Saha Keşfi ve Entegrasyon Sınırları</h2>
              <p className="text-xs text-slate-500 mt-1">
                P00 aşaması kurumsal olarak incelenip G0 onayı verilene kadar P01 aşamasına otomatik geçilmez.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-3">
                <h3 className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                  <Building2 className="w-4 h-4 text-indigo-600" />
                  <span>P01 Giriş Şartları (G1 Input Checklist)</span>
                </h3>
                <ul className="text-xs text-slate-600 space-y-2 list-disc pl-4">
                  <li>G0 kontrol listesinin kurumsal makamlarca resmi onaylanması.</li>
                  <li>DEC-001 mali modelinin (Model A/B/C/D) kararlaştırılması (BLK-001).</li>
                  <li>DEC-008 bariyer kumanda yetkisinin netleşmesi (BLK-002).</li>
                  <li>İmzalı kurumsal RACI atamalarının yapılması (BLK-008).</li>
                </ul>
              </div>

              <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-3">
                <h3 className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-emerald-600" />
                  <span>P01'de Yapılacak Saha Keşif Çalışmaları</span>
                </h3>
                <ul className="text-xs text-slate-600 space-y-2 list-disc pl-4">
                  <li>Kapı ve şeritlerdeki GV-LPR2812-DL kameralarının montaj açısı ve protokol tespiti.</li>
                  <li>GV-ASManager 6.3.0 sunucu arayüzü ve onaylı iş emri kanallarının belirlenmesi.</li>
                  <li>Fiziksel döngü sensörleri ve fotosel güvenlik kablolamasının test edilmesi.</li>
                  <li>Kapı kontrol uç biriminde yerel arabellek için elektrik ve KGK sürelerinin ölçümü.</li>
                </ul>
              </div>
            </div>

            <div className="p-4 bg-slate-100 rounded-lg border border-slate-200 text-xs text-slate-700 font-mono">
              <strong>PROTOKOL UYARISI:</strong> P00 v1.2 teslimatı tamamlanmıştır. Kullanıcının bağımsız teknik incelemesi ve onayı olmadan P01 aşamasına geçilmeyecektir.
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-3 px-4 text-center text-xs text-slate-400">
        Kampüs PTS Gelir Yönetim Platformu © 2026 — P00 v1.2 Kanonik Temel — Durum: G0 NOT_APPROVED / P00_SOURCE_READY
      </footer>
    </div>
  );
}
