# Product Requirement Document

**Bogor Liveable City: Sistem Informasi Geografis Analisis Kelayakhunian Wilayah Kota Bogor**

| Keterangan | Isi |
|---|---|
| Versi | 2.0 |
| Tanggal | 25 Oktober 2026 |
| Kelompok | Kelompok 3 |
| Project Sponsor | Dr. Sofiyanti Indriasari, S.Kom., M.Kom. |
| Project Manager | M. Karel Putra Shelvion |
| Metodologi | Agile – Scrum |
| Project Start | 24 Agustus 2026 |
| Project Finish | 16 November 2026 |
| Repositori | https://github.com/rdhiyaurrahman/bogor-liveable-city |

**Anggota:** Radithya Dhiyaurrahman (J0403231127), Nur Izza Yarismen
(J0403221006), Muhamad Zaidan (J0403241031), Vezajiva Ariesta Maheswari
(J0403241080), M. Karel Putra Shelvion (J0403241136)

### Perubahan dari versi 1.0

| Hal | Versi 1.0 | Versi 2.0 |
|---|---|---|
| Dasar formula | belum ada | Dewi, Yahya & Situmorang (2025), DOI 10.14710/pwk.v21i3.67908 |
| Unit analisis | belum ditegaskan | 68 kelurahan, dengan agregat tingkat kecamatan |
| Dimensi indikator | 6 aspek tanpa rumus | 6 dimensi, 10 indikator, rumus eksplisit |
| Pola ruang | bagian dari indeks | layer analisis tersendiri di luar indeks |
| Bobot | 0,20/0,20/0,20/0,15/0,15/0,10 tanpa sumber | sama rata mengikuti jurnal, slider jadi analisis sensitivitas |
| Dataset | 11 berkas temuan | 10 berkas terpakai, 3 digugurkan, 2 ditambahkan |
| Aksesibilitas faskes | buffer lingkaran | jarak tempuh melalui jaringan jalan |
| Tech stack | belum ditetapkan | PostgreSQL + PostGIS, Express, Next.js, Leaflet |

---

## 1. Product Overview

Bogor Liveable City GIS adalah WebGIS interaktif untuk memvisualisasikan,
mengeksplorasi, dan menganalisis tingkat kelayakhunian wilayah di Kota Bogor
pada tingkat kelurahan. Sistem mengintegrasikan data spasial dan data atribut
dari berbagai sumber ke dalam satu platform, lalu menyajikannya sebagai peta
interaktif, dashboard statistik, analisis per indikator, peringkat wilayah, dan
perbandingan antarwilayah.

Unit analisis sistem adalah **68 kelurahan** di 6 kecamatan Kota Bogor, dengan
luas total 111,39 km² dan jumlah penduduk 1.114.018 jiwa (2022). Sistem juga
menyajikan agregat pada tingkat kecamatan.

Penilaian kelayakhunian mencakup enam dimensi: kesehatan, pendidikan, sosial
kependudukan, lingkungan, transportasi, dan ekonomi. Analisis kesesuaian
pemanfaatan ruang disajikan sebagai layer tersendiri di luar indeks.

## 2. Background

Kelayakhunian suatu wilayah dipengaruhi oleh ketersediaan fasilitas kesehatan,
akses pendidikan, kepadatan penduduk, kondisi lingkungan, infrastruktur jalan,
dan kondisi ekonomi. Kondisi tersebut berbeda antara satu wilayah dengan wilayah
lainnya, bahkan antarkelurahan yang bertetangga.

Data yang menggambarkan kondisi tersebut tersebar di banyak sumber dengan format
berbeda, sebagian berupa data spasial dan sebagian berupa tabel. Penyajian dalam
bentuk tabel tidak cukup untuk menunjukkan pola keruangan dan hubungan
antarvariabel. Karena itu dibutuhkan sistem yang memungkinkan eksplorasi visual
sekaligus menyajikan hasil analisis.

Penilaian kelayakhunian yang beredar luas di Indonesia, yaitu *Most Livable City
Index* (MLCI) terbitan Ikatan Ahli Perencana, disusun dari persepsi warga dan
berhenti pada tingkat kota. Penilaian berbasis persepsi tidak dapat menunjukkan
perbedaan kondisi antarwilayah di dalam satu kota. Sistem ini mengambil
pendekatan sebaliknya, yaitu mengukur kondisi objektif dari data sekunder pada
unit wilayah yang lebih kecil.

## 3. Problem Statement

Pengguna membutuhkan cara yang lebih mudah untuk memahami kondisi kelayakhunian
wilayah Kota Bogor karena:

- Data indikator kelayakhunian berasal dari berbagai sumber dan format.
- Data spasial dan data atribut belum tersaji dalam satu media analisis.
- Perbedaan kondisi antarwilayah sulit dipahami hanya melalui tabel.
- Pengguna membutuhkan informasi yang dapat dieksplorasi secara visual
  berdasarkan lokasi.
- Pengguna membutuhkan cara melihat perbandingan dan peringkat kondisi wilayah.
- Penilaian yang tersedia saat ini berhenti pada tingkat kota, sehingga
  perbedaan antarkelurahan tidak terlihat.

## 4. Product Goals

### 4.1 Tujuan Utama

Menyediakan sistem WebGIS interaktif yang mampu memvisualisasikan dan
menganalisis tingkat kelayakhunian wilayah Kota Bogor pada tingkat kelurahan,
berdasarkan indikator spasial dan atribut, dengan formula yang dapat
dipertanggungjawabkan secara akademik.

### 4.2 Tujuan Pendukung

- Mengintegrasikan sepuluh dataset ke dalam satu sistem.
- Menampilkan informasi kelayakhunian melalui peta interaktif.
- Menghasilkan indeks kelayakhunian untuk setiap kelurahan.
- Menyajikan agregat indeks pada tingkat kecamatan.
- Menampilkan kondisi setiap indikator secara terperinci.
- Memudahkan pengguna membandingkan dua wilayah.
- Menampilkan peringkat kelayakhunian wilayah.
- Mengidentifikasi wilayah yang membutuhkan perhatian berdasarkan hasil analisis.
- Menyediakan analisis sensitivitas terhadap bobot indikator.

## 5. Target Users

| User | Kebutuhan Utama |
|---|---|
| Perencana wilayah | Mengevaluasi kondisi dan karakteristik wilayah |
| Akademisi | Mengeksplorasi dan menganalisis data spasial |
| Masyarakat umum | Memahami kondisi kelayakhunian suatu wilayah |
| Pengguna analisis | Membandingkan wilayah dan melihat indikator secara lebih detail |

## 6. Metodologi Penilaian

### 6.1 Dasar rujukan

> Dewi, L.A.T., Yahya, W., & Situmorang, R. (2025). Pengukuran Layak Huni Kota
> Depok pada Tingkat Meso. *Jurnal Pembangunan Wilayah dan Kota*, 21(3),
> 387–402. DOI: 10.14710/pwk.v21i3.67908

Jurnal ini dipilih karena mengukur kota tetangga dengan unit analisis meso,
memakai data sekunder, dipetakan dengan sistem informasi geografis, dan
menuliskan formulanya sebagai persamaan bernomor.

### 6.2 Normalisasi (Persamaan 1, hlm. 392)

```
X' = (X − X_min) / (X_max − X_min)
```

X adalah nilai asli indikator, X_min dan X_max adalah nilai terendah dan
tertinggi indikator tersebut di seluruh wilayah. Hasilnya berada pada rentang 0
sampai 1. Indikator yang berhubungan negatif terhadap kelayakhunian dibalik
urutannya, sehingga nilai tertinggi menjadi 0.

Metode ini dipilih karena indikator memiliki satuan yang berbeda-beda, misalnya
jiwa per km², persen luas, dan meter. Normalisasi dilakukan di dalam satu kolom
indikator terhadap seluruh wilayah, sehingga satuan asli tidak pernah
diperbandingkan secara langsung antarindikator.

### 6.3 Agregasi bertingkat

1. Setiap sub-indikator dinormalisasi ke rentang 0 sampai 1.
2. Sub-indikator dalam satu dimensi dijumlahkan, lalu dinormalisasi ulang,
   menghasilkan skor dimensi 0 sampai 1.
3. Keenam skor dimensi dijumlahkan, lalu dinormalisasi ulang, menghasilkan skor
   kelayakhunian 0 sampai 1.

Bobot antardimensi sama rata. Normalisasi ulang pada setiap tingkat membuat
seluruh dimensi berbobot sama berapa pun jumlah sub-indikatornya.

### 6.4 Klasifikasi (Persamaan 2, hlm. 393)

```
Rentang interval = (nilai tertinggi − nilai terendah) / jumlah kelas
```

Dengan lima kelas pada rentang 0 sampai 1:

| Rentang skor | Kelas |
|---|---|
| 0,81 – 1,00 | Sangat Layak Huni |
| 0,61 – 0,80 | Layak Huni |
| 0,41 – 0,60 | Cukup Layak Huni |
| 0,21 – 0,40 | Tidak Layak Huni |
| 0,00 – 0,20 | Sangat Tidak Layak Huni |

### 6.5 Dimensi dan indikator

| Dimensi | Sub-indikator | Satuan |
|---|---|---|
| Kesehatan | Cakupan permukiman dalam jangkauan puskesmas; jarak tempuh ke rumah sakit terdekat | % luas permukiman; meter |
| Pendidikan | Luas lahan pendidikan | % luas wilayah |
| Sosial kependudukan | Kepadatan penduduk | jiwa/km² |
| Lingkungan | Tutupan vegetasi; vegetasi per kapita | % luas wilayah; m²/jiwa |
| Transportasi | Kepadatan badan jalan | % luas wilayah |
| Ekonomi | Indeks kesejahteraan; luas kawasan perdagangan | indeks; % luas wilayah |

Di luar indeks terdapat indikator **kesesuaian permukiman terhadap pola ruang**,
yaitu persentase luas permukiman yang berada pada peruntukan Kawasan Perumahan
atau Kawasan Campuran menurut RTRW. Indikator ini tetap dihitung dan dipetakan,
tetapi tidak dimasukkan ke dalam indeks karena jurnal rujukan hanya memuat enam
dimensi.

### 6.6 Pengukuran aksesibilitas fasilitas kesehatan

Aksesibilitas fasilitas kesehatan diukur dengan **jarak tempuh melalui jaringan
jalan**, bukan jarak garis lurus. Alasannya, warga menempuh jalan yang berbelok
dan tidak berhenti di batas administrasi.

Pengujian pada data Kota Bogor menunjukkan jarak lurus meremehkan jarak tempuh
sebenarnya:

| | Jarak lurus (median) | Jarak jaringan (median) | Rasio |
|---|---|---|---|
| Puskesmas | 920 m | 1.273 m | 1,36× |
| Rumah sakit | 955 m | 1.480 m | 1,44× |

Sebanyak 34 dari 68 kelurahan tidak memiliki fasilitas kesehatan di dalam
wilayahnya, tetapi 24 di antaranya berpusat kurang dari 1,5 km dari fasilitas
di kelurahan tetangga. Kelurahan Cibogor berjarak 208 m dan tepi wilayah
Kelurahan Pasir Kuda berjarak 6 m dari fasilitas terdekat. Penghitungan berbasis
jumlah fasilitas di dalam poligon menilai kelurahan tersebut bernilai nol,
sehingga metode tersebut tidak dipakai.

Radius jangkauan ditetapkan 2 km untuk puskesmas. Radius 6 km untuk rumah sakit
tidak dipakai karena menutup seluruh 68 kelurahan tanpa kecuali, sehingga tidak
memiliki daya pembeda dan menyebabkan pembagian nol pada normalisasi.

### 6.7 Agregasi tingkat kecamatan

Indeks dihitung pada tingkat kelurahan. Nilai tingkat kecamatan disajikan sebagai
**rata-rata tertimbang jumlah penduduk** dari kelurahan di dalamnya, dan diberi
label sebagai agregat, bukan sebagai indeks yang dihitung ulang. Penghitungan
ulang normalisasi pada 6 unit akan memaksa satu kecamatan bernilai 0 dan satu
bernilai 1, sehingga sebarannya terlalu kasar.

## 7. Sumber Data

### 7.1 Data spasial

| # | Dataset | Tahun | Dipakai untuk |
|---|---|---|---|
| 1 | Peta tingkat persentase penduduk dengan tingkat kesejahteraan | — | Batas 68 kelurahan; kolom indeks kesejahteraan |
| 2 | Titik Puskesmas (25 titik) | — | Dimensi kesehatan |
| 3 | Titik Rumah Sakit (22 titik) | — | Dimensi kesehatan |
| 4 | Jangkauan Puskesmas dan Rumah Sakit (37 poligon) | — | Pembanding cakupan layanan |
| 5 | Penggunaan Lahan Kota Bogor | 2023 | Dimensi pendidikan, lingkungan, ekonomi |
| 6 | Jalan Kota Bogor 1:25.000 | 2021 | Dimensi transportasi |
| 7 | Pola Ruang Kota Bogor | 2021 | Layer kesesuaian ruang |
| 8 | Permukiman 1:25.000 | — | Layer kesesuaian ruang, penyebut cakupan |
| 10 | Jaringan jalan OpenStreetMap (21.276 ruas) | 2026 | Jarak tempuh ke fasilitas kesehatan |

### 7.2 Data atribut

| # | Dataset | Tahun | Sumber |
|---|---|---|---|
| 9 | Jumlah Penduduk menurut Kelurahan | 2022 | Disdukcapil Kota Bogor, dipublikasikan BPS Kota Bogor |

### 7.3 Dataset yang digugurkan

| Dataset | Alasan |
|---|---|
| Peta persentase rumah tangga tanpa akses air bersih | Duplikat identik dataset #1, tidak memuat data air bersih |
| Peta rata-rata lama sekolah perempuan di atas 15 tahun | Duplikat identik dataset #1, tidak memuat data lama sekolah |
| Penduduk per kelurahan 2021 | Digantikan data 2022; label 11 kelurahan Tanah Sareal tertukar |

Rincian lengkap setiap sumber, termasuk query Overpass, lisensi ODbL, dan catatan
teknis, ada pada `data/DATASET.md`.

## 8. User Journey

```
Akses Website
      ↓
Melihat Peta Kota Bogor
      ↓
Mencari / Memilih Wilayah
      ↓
Melihat Detail Wilayah
      ↓
Melihat Skor Kelayakhunian dan Klasifikasinya
      ↓
Melihat Detail Indikator per Dimensi
      ↓
Melakukan Eksplorasi / Analisis
      ↓
Membandingkan Wilayah / Melihat Peringkat
      ↓
Memperoleh Informasi Hasil Analisis
```

Pengguna dapat mencari kecamatan atau kelurahan, memilih poligon pada peta,
kemudian memperoleh informasi skor, klasifikasi, peringkat, nilai tiap indikator,
sebaran fasilitas kesehatan, serta kesesuaian pemanfaatan ruang.

## 9. Product Scope

### 9.1 In Scope

- WebGIS interaktif
- Peta 68 kelurahan Kota Bogor
- Visualisasi layer spasial
- Filter wilayah per kecamatan dan per kelurahan
- Pencarian wilayah
- Detail informasi wilayah
- Indeks kelayakhunian per kelurahan
- Agregat indeks per kecamatan
- Analisis enam dimensi dan sepuluh indikator
- Analisis fasilitas kesehatan berbasis jarak tempuh jaringan jalan
- Analisis kesesuaian permukiman terhadap pola ruang
- Dashboard statistik
- Peringkat wilayah
- Perbandingan dua wilayah
- Simulasi bobot indikator sebagai analisis sensitivitas
- Ekspor data peringkat
- Visualisasi hasil analisis pada peta

### 9.2 Out of Scope

- Aplikasi mobile native
- Pengumpulan data lapangan secara langsung
- Prediksi berbasis machine learning
- Monitoring IoT real-time
- Integrasi real-time dengan sistem pemerintah
- Pengadaan infrastruktur fisik
- Pengambilan keputusan kebijakan secara otomatis
- Analisis rute perjalanan untuk pengguna akhir

## 10. Functional Requirements

### 10.1 Peta dan navigasi

| ID | Requirement | Aktor | Prioritas |
|---|---|---|---|
| FR-01 | Pengguna dapat mengakses dan bernavigasi pada peta interaktif wilayah Kota Bogor | Pengguna | Tinggi |
| FR-02 | Pengguna dapat melihat visualisasi poligon wilayah pada peta | Pengguna | Tinggi |
| FR-03 | Pengguna dapat memilih wilayah tertentu secara langsung melalui peta | Pengguna | Tinggi |
| FR-04 | Pengguna dapat mengatur zoom dan memusatkan tampilan peta | Pengguna | Tinggi |
| FR-05 | Pengguna dapat membaca legenda peta untuk memahami hasil visualisasi | Pengguna | Tinggi |
| FR-18 | Pengguna dapat memilih dan mengganti jenis peta dasar | Pengguna | Sedang |

### 10.2 Filter dan pencarian

| ID | Requirement | Aktor | Prioritas |
|---|---|---|---|
| FR-06 | Pengguna dapat memfilter data wilayah berdasarkan kecamatan | Pengguna | Tinggi |
| FR-07 | Pengguna dapat memfilter data wilayah berdasarkan kelurahan | Pengguna | Tinggi |
| FR-08 | Pengguna dapat mencari nama kecamatan atau kelurahan secara spesifik | Pengguna | Tinggi |
| FR-15 | Pengguna dapat memfilter data wilayah berdasarkan klasifikasi kelayakhunian | Pengguna | Sedang |
| FR-16 | Pengguna dapat mereset filter yang telah diterapkan kembali ke tampilan awal | Pengguna | Sedang |

### 10.3 Layer dan tematik

| ID | Requirement | Aktor | Prioritas |
|---|---|---|---|
| FR-09 | Pengguna dapat mengaktifkan layer tematik tertentu pada peta | Pengguna | Tinggi |
| FR-10 | Pengguna dapat menonaktifkan layer tematik yang sedang tampil | Pengguna | Tinggi |
| FR-11 | Pengguna dapat melihat titik persebaran layer fasilitas kesehatan | Pengguna | Tinggi |
| FR-12 | Pengguna dapat melihat pewarnaan peta (choropleth) berdasarkan nilai indeks kelayakhunian | Pengguna | Tinggi |
| FR-13 | Pengguna dapat melihat pewarnaan peta berdasarkan skor dimensi tertentu | Pengguna | Tinggi |
| FR-14 | Pengguna dapat melihat perubahan legenda secara otomatis sesuai indikator yang dipilih | Pengguna | Tinggi |
| FR-17 | Pengguna dapat melihat area jangkauan fasilitas kesehatan | Pengguna | Sedang |
| FR-19 | Pengguna dapat melihat layer jaringan jalan sebagai dasar analisis aksesibilitas | Pengguna | Sedang |
| FR-20 | Pengguna dapat melihat layer kesesuaian permukiman terhadap pola ruang secara terpisah dari indeks | Pengguna | Sedang |

### 10.4 Analisis dan penyajian hasil

| ID | Requirement | Aktor | Prioritas |
|---|---|---|---|
| FR-21 | Pengguna dapat melihat skor indeks kelayakhunian dan kelasnya untuk setiap kelurahan | Pengguna | Tinggi |
| FR-22 | Pengguna dapat melihat rincian skor keenam dimensi untuk wilayah yang dipilih | Pengguna | Tinggi |
| FR-23 | Pengguna dapat melihat nilai mentah setiap indikator beserta satuannya | Pengguna | Tinggi |
| FR-24 | Pengguna dapat melihat peringkat seluruh kelurahan berdasarkan indeks kelayakhunian | Pengguna | Tinggi |
| FR-25 | Pengguna dapat membandingkan dua wilayah beserta selisih nilai indikatornya | Pengguna | Tinggi |
| FR-26 | Pengguna dapat melihat agregat indeks pada tingkat kecamatan | Pengguna | Sedang |
| FR-27 | Pengguna dapat melihat dashboard statistik ringkasan kondisi kota | Pengguna | Sedang |
| FR-28 | Pengguna dapat mengubah bobot dimensi untuk melihat perubahan hasil sebagai analisis sensitivitas | Pengguna | Sedang |
| FR-29 | Pengguna dapat mengembalikan bobot ke nilai bawaan sesuai jurnal rujukan | Pengguna | Sedang |
| FR-30 | Pengguna dapat mengekspor data peringkat wilayah | Pengguna | Rendah |
| FR-31 | Pengguna dapat melihat sumber data dan tahun data setiap indikator | Pengguna | Rendah |

## 11. Non Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | Sistem harus memiliki antarmuka yang mudah digunakan untuk melakukan eksplorasi peta dan informasi wilayah |
| NFR-02 | Informasi hasil analisis harus disajikan dalam bentuk visual yang mudah dipahami |
| NFR-03 | Sistem harus dapat menyesuaikan tampilan pada berbagai ukuran perangkat |
| NFR-04 | Sistem harus mampu mengintegrasikan data spasial dan data atribut |
| NFR-05 | Integrasi antara database, backend, dan frontend harus berjalan secara stabil |
| NFR-06 | Sistem harus memiliki mekanisme keamanan pada sisi server dan pengelolaan data |
| NFR-07 | Peta harus tetap responsif saat menampilkan 68 poligon kelurahan beserta layer jaringan jalan |
| NFR-08 | Setiap peta yang menampilkan data OpenStreetMap harus mencantumkan atribusi "© OpenStreetMap contributors" sesuai lisensi ODbL |
| NFR-09 | Perhitungan indeks harus dapat diulang dari data mentah melalui satu perintah |

## 12. Arsitektur Sistem

| Lapis | Teknologi |
|---|---|
| Pengolahan data | Python 3 (shapely, pyproj, numpy, networkx) |
| Basis data | PostgreSQL 18 + PostGIS |
| Backend | Node.js + Express |
| Frontend | Next.js |
| Visualisasi peta | Leaflet.js |

### 12.1 Alur data

```
[1] CSV mentah  →  [2] Pengolahan Python  →  [3] CSV + GeoJSON
                                                    ↓
[6] Next.js + Leaflet  ←  [5] Express  ←  [4] PostgreSQL + PostGIS
```

PostGIS menyimpan geometri poligon beserta nilai indikatornya. Backend memanggil
data tersebut dan mengembalikan objek GeoJSON. Frontend membaca properti GeoJSON
dengan Leaflet dan memberi gradasi warna berbeda pada setiap kelurahan sesuai
rentang nilainya, sehingga terbentuk peta choropleth.

### 12.2 Endpoint

```
GET /api/kelurahan         FeatureCollection seluruh kelurahan
GET /api/kelurahan/:kode   satu kelurahan untuk panel detail
GET /api/kecamatan         agregat tertimbang penduduk per kecamatan
GET /api/jalan             layer jaringan jalan
```

### 12.3 Catatan implementasi

Berkas GeoJSON hasil pengolahan sudah memakai EPSG:4326 dengan urutan
bujur-lintang yang benar, karena penukaran sumbu dikerjakan pada tahap
pengolahan. Data tersebut tidak boleh ditukar sumbunya lagi saat dimuat ke
PostGIS.

Leaflet mengakses objek `window`, sehingga komponen peta pada Next.js harus
dimuat tanpa render sisi server.

## 13. Keterbatasan

1. Jurnal rujukan memakai 15 indikator, sistem ini memakai 10 indikator pada
   enam dimensi yang sama. Indikator jumlah murid, jumlah guru, rasio
   guru-murid, rata-rata lama sekolah, jumlah tenaga kesehatan, angka harapan
   hidup, tindakan kriminalitas, trayek angkutan umum, sumber air minum, jumlah
   tempat pembuangan sampah, dan PDRB tidak tersedia pada tingkat kelurahan.
2. Tahun data tidak seragam, berkisar 2021 sampai 2023, dengan data jaringan
   jalan 2026. Pola ruang merupakan dokumen rencana periode 2021–2041 sehingga
   tidak memiliki versi tahunan. Jurnal rujukan menyatakan keterbatasan serupa.
3. Skor bersifat relatif di antara 68 kelurahan Kota Bogor, bukan absolut.
   Normalisasi memaksa satu kelurahan bernilai 0 dan satu bernilai 1.
4. Indikator per kapita tidak stabil pada kelurahan berpenduduk sedikit.
   Kelurahan Pabaton berpenduduk 3.225 jiwa dan merupakan kawasan perkantoran,
   sehingga rasio fasilitas per penduduknya tertinggi di Kota Bogor meskipun
   bukan kawasan hunian.
5. Tutupan vegetasi yang dipakai mencakup kebun, sawah, dan pekarangan privat,
   sehingga tidak sebanding dengan target ruang terbuka hijau publik.
6. Jaringan jalan OpenStreetMap merupakan data sukarelawan, bukan data resmi
   pemerintah, dan diperlakukan sebagai jaringan dua arah sehingga mengabaikan
   2.949 ruas satu arah.
7. Arti kolom indeks kesejahteraan pada dataset #1 belum terverifikasi karena
   kolom metadata sumbernya kosong, padahal kolom tersebut menyumbang korelasi
   terbesar terhadap indeks.
8. Dimensi lingkungan berkorelasi negatif terhadap indeks, karena wilayah hijau
   di Kota Bogor cenderung berada di pinggiran yang minim layanan. Kondisi ini
   merupakan temuan, bukan kesalahan perhitungan.

## 14. Status Pengerjaan

| Tahap | Status |
|---|---|
| Pengumpulan dan verifikasi data | selesai |
| Pengolahan indikator dan indeks | selesai |
| Pemuatan ke PostGIS | belum |
| Backend Express | belum |
| Frontend Next.js | belum |
| Integrasi jarak jaringan ke dimensi kesehatan | belum |
