# Sistem Simulasi Gerbang Kereta Api Berbasis Aljabar Boolean

Proyek ini merupakan simulasi interaktif untuk sistem kontrol gerbang kereta api, yang dirancang menggunakan **Python** dengan pustaka **Pygame**. Simulasi ini bertujuan untuk menggambarkan penerapan aljabar Boolean dalam mendesain kontrol logika gerbang kereta api secara aman dan efisien.

---

## Fitur Utama
- **Lintasan Kereta dan Jalan Raya**: Representasi grafis dari jalur kereta dan jalan kendaraan dengan deteksi otomatis persimpangan.
- **Gerbang Otomatis**: Gerbang akan membuka dan menutup berdasarkan posisi kereta dengan kontrol berbasis logika aljabar Boolean.
- **Interaksi Mobil dan Kereta**: Mobil akan berhenti saat gerbang tertutup dan bergerak setelah gerbang terbuka.
- **Simulasi Interaktif**: Gunakan input keyboard untuk menambahkan atau menghapus kereta.

---

## Instalasi

### Prasyarat
- **Python 3.10** atau versi yang lebih baru.
- **Pygame**: Instal dengan perintah berikut:
  ```bash
  pip install pygame
  ```
- **Shapely**: Instal dengan perintah berikut:
  ```bash
  pip install shapely
  ```

### Langkah Instalasi
1. Clone repositori ini ke komputer Anda:
   ```bash
   git clone https://github.com/AgentlReal/SimulasiLintasanKeretaApi.git
   ```
2. Navigasikan ke direktori proyek:
   ```bash
   cd SimulasiLintasanKeretaApi
   ```
3. Jalankan skrip Python untuk memulai simulasi:
   ```bash
   python main.py
   ```

---

## Cara Menggunakan

1. Jalankan skrip **main.py**.
2. Gunakan tombol berikut untuk berinteraksi:
   - **Spasi**: Tambahkan kereta ke lintasan.
   - **R**: Hapus kereta dari lintasan.
3. Perhatikan bagaimana gerbang secara otomatis membuka dan menutup berdasarkan logika kontrol.

---

## Struktur Proyek

```
SimulasiLintasanKeretaApi/
├── images/
│   ├── train.png       # Sprite kereta
│   ├── sedan.png       # Sprite mobil
│   ├── bg.jpg          # Gambar latar
├── main.py             # Skrip utama simulasi
└── README.md           # Dokumentasi ini
```

---

## Prinsip Logika Aljabar Boolean

Proyek ini menggunakan aljabar Boolean untuk mengontrol status gerbang dengan logika berikut:
- **Safety**: Gerbang menutup saat kereta mendekat.
- **Functionality**: Gerbang membuka saat tidak ada kereta di area gerbang.

Rumus logika kontrol:
- **Safety**:
  ```text
  (NOT U1 AND (S1 OR S4)) OR (U1 AND U3 AND S3) OR (U1 AND NOT U3 AND S2)
  ```
- **Functionality**:
  ```text
  (NOT U2 AND (S2 OR S3)) OR (U2 AND (S1 OR S4))
  ```

---

## Kontribusi

Kontribusi terbuka untuk pengembangan lebih lanjut. Silakan fork proyek ini dan ajukan pull request untuk penambahan fitur atau perbaikan.

---

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
