# 🔄 Workflow — CampusHub

Dokumen ini menjabarkan alur kerja sistem CampusHub dalam bentuk diagram, diturunkan dari algoritma dan alur logika di `DESIGN.md`. Diagram-diagram ini bisa langsung dipakai sebagai dasar **BAB III.2 Perancangan Sistem (Flowchart/Diagram Alir)** pada laporan UAS.

> Sintaks Mermaid — otomatis ter-render di GitHub, banyak editor Markdown, dan sebagian besar viewer modern. Untuk laporan, bisa di-screenshot atau diekspor lewat [mermaid.live](https://mermaid.live).

---

## 1. Alur Sistem Secara Umum

```mermaid
flowchart TD
    Start([Mulai]) --> Home[Halaman Beranda]
    Home --> Role{Pilih Peran}
    Role -->|Pengunjung| G1[Lihat & Cari Layanan]
    Role -->|Penyedia Jasa| P1[Login / Registrasi Provider]
    Role -->|Admin| A1[Login Admin]

    G1 --> G2[Detail Layanan]
    G2 --> G3[Isi Form Pesanan]
    G3 --> DB[(Database)]

    P1 --> P2[Dashboard Provider]
    P2 --> P3[Kelola Jasa]
    P2 --> P4[Lihat Pesanan]
    P4 --> P5[Terima / Tolak]
    P5 --> DB

    A1 --> A2[Dashboard Admin]
    A2 --> A3[Verifikasi Provider]
    A2 --> A4[Kelola Kategori]
    A2 --> A5[Lihat Statistik]

    DB --> Selesai([Selesai])
```

## 2. Alur Pengunjung — Melihat hingga Memesan Layanan

```mermaid
flowchart TD
    A([Mulai]) --> B[Buka Website]
    B --> C[Lihat Daftar Layanan]
    C --> D[Cari / Filter Kategori]
    D --> E[Klik Detail Layanan]
    E --> F["Isi Form: Nama, NIM, Kelas, No. WhatsApp, Catatan"]
    F --> G[Klik Pesan]
    G --> H{Validasi Input}
    H -->|Tidak valid| F
    H -->|Valid| I[(Data tersimpan ke database)]
    I --> J[Status: Menunggu Konfirmasi]
    J --> K([Selesai])
```

*Ref: FR-01, FR-02, FR-03, FR-04 di `PRD.md`*

## 3. Alur Registrasi & Verifikasi Provider

```mermaid
flowchart TD
    A([Mulai]) --> B[Daftar sebagai Provider]
    B --> C[Isi Biodata]
    C --> D[Upload KTM - opsional]
    D --> E[Status: Pending]
    E --> F{Admin Verifikasi}
    F -->|Disetujui| G[Status: Aktif]
    F -->|Ditolak| H[Status: Ditolak]
    G --> I[Provider dapat Login]
    I --> J[Mulai menawarkan jasa]
    J --> K([Selesai])
    H --> K
```

*Ref: FR-05, FR-06, FR-07*

## 4. Alur Provider Mengelola Jasa (CRUD)

```mermaid
flowchart TD
    A([Mulai]) --> B[Login Provider]
    B --> C{Kredensial valid?}
    C -->|Tidak| B
    C -->|Ya| D[Dashboard Provider]
    D --> E[Tambah / Edit / Hapus Jasa]
    E --> F["Isi Data: Judul, Kategori, Harga, Deskripsi, Gambar"]
    F --> G[Simpan]
    G --> H[Menunggu Verifikasi Admin]
    H --> I{Disetujui Admin?}
    I -->|Ya| J[Jasa tampil ke publik]
    I -->|Tidak| K[Jasa tidak ditampilkan]
    J --> L([Selesai])
    K --> L
```

*Ref: FR-08*

## 5. Siklus Status Pesanan (Order Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Pending: Guest membuat pesanan
    Pending --> Accepted: Provider menerima
    Pending --> Rejected: Provider menolak
    Accepted --> Completed: Layanan selesai dikerjakan
    Completed --> [*]
    Rejected --> [*]
```

*Ref: FR-09 — status disederhanakan jadi 4 nilai sesuai catatan "Status Order" di `DESIGN.md`.*

## 6. Alur Admin

```mermaid
flowchart TD
    A([Mulai]) --> B[Login Admin]
    B --> C[Dashboard Admin]
    C --> D[Verifikasi Provider Baru]
    C --> E[Kelola Kategori]
    C --> F[Kelola / Hapus Layanan]
    C --> G[Lihat Statistik & Grafik]
    D --> H([Selesai])
    E --> H
    F --> H
    G --> H
```

*Ref: FR-06, FR-10, FR-11, FR-12, FR-13*

## 7. Sequence Diagram — Guest Memesan Jasa (End-to-End)

```mermaid
sequenceDiagram
    participant G as Guest
    participant W as Web App (Flask)
    participant DB as Database
    participant P as Provider

    G->>W: Buka halaman & cari jasa
    W->>DB: Query daftar jasa
    DB-->>W: Data jasa
    W-->>G: Tampilkan hasil pencarian
    G->>W: Isi form pesanan & submit
    W->>W: Validasi input (client + server)
    W->>DB: Simpan order (status = Pending)
    DB-->>W: OK
    W-->>G: Tampilkan "Menunggu Konfirmasi"
    P->>W: Login & buka daftar pesanan
    W->>DB: Ambil pesanan baru
    DB-->>W: Data pesanan
    P->>W: Accept / Reject pesanan
    W->>DB: Update status
    P-->>G: Hubungi via WhatsApp (manual)
```

## 8. Ringkasan Status & Transisi

| Status | Dipicu Oleh | Status Selanjutnya |
|---|---|---|
| Pending | Guest submit form pesanan | Accepted / Rejected |
| Accepted | Provider menerima | Completed |
| Rejected | Provider menolak | *(akhir)* |
| Completed | Provider menandai selesai | *(akhir)* |

> Status **Pending** juga dipakai sebagai basis badge notifikasi "Pesanan Baru" di dashboard Provider (FR-17) — begitu status berubah, badge otomatis berkurang tanpa perlu kolom tambahan di database. Detail implementasi ada di `FOLDER_STRUCTURE.md`.