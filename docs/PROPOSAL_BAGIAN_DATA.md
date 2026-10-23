# Bagian Proposal: Gambaran Aplikasi dan Sumber Data

Kelompok 3 — Bogor Liveable City
Sistem Informasi Geografis Analisis Kelayakhunian Wilayah Kota Bogor

---

## 1. Gambaran Umum Aplikasi yang Akan Dibangun

Bogor Liveable City adalah WebGIS interaktif untuk memvisualisasikan dan
menganalisis tingkat kelayakhunian 68 kelurahan di Kota Bogor. Aplikasi
menggabungkan data spasial (poligon wilayah, titik fasilitas, penggunaan lahan)
dengan data atribut (jumlah penduduk, indikator sosial ekonomi) dalam satu
platform, lalu menyajikannya sebagai peta choropleth, dashboard statistik,
peringkat wilayah, dan perbandingan antarwilayah.

### Masalah yang diselesaikan

Data indikator kelayakhunian Kota Bogor tersebar di banyak sumber dan format,
sebagian spasial dan sebagian tabular, sehingga perbedaan kondisi antarwilayah
sulit dipahami bila hanya disajikan sebagai tabel. Aplikasi ini menyatukannya
dan menampilkan polanya secara keruangan.

### Metode penilaian

Indeks kelayakhunian disusun mengikuti Dewi, L.A.T., Yahya, W., & Situmorang, R.
(2025), *Pengukuran Layak Huni Kota Depok pada Tingkat Meso*, Jurnal Pembangunan
Wilayah dan Kota, 21(3), 387–402, DOI: 10.14710/pwk.v21i3.67908.

Normalisasi min-max (Persamaan 1 jurnal):

> X' = (X − X_min) / (X_max − X_min)

Indikator yang berhubungan negatif terhadap kelayakhunian dibalik urutannya,
sehingga nilai tertinggi menjadi 0. Skor tiap dimensi diperoleh dengan
menjumlahkan sub-indikator ternormalisasi lalu menormalisasi ulang. Skor akhir
diperoleh dengan menjumlahkan keenam skor dimensi lalu menormalisasi ulang,
sehingga berada pada rentang 0 sampai 1.

Klasifikasi memakai interval sama (Persamaan 2 jurnal), menghasilkan lima kelas:

| Rentang skor | Kelas |
|---|---|
| 0,81 – 1,00 | Sangat Layak Huni |
| 0,61 – 0,80 | Layak Huni |
| 0,41 – 0,60 | Cukup Layak Huni |
| 0,21 – 0,40 | Tidak Layak Huni |
| 0,00 – 0,20 | Sangat Tidak Layak Huni |

Enam dimensi yang dipakai mengikuti jurnal: kesehatan, pendidikan, sosial
kependudukan, lingkungan, transportasi, dan ekonomi. Bobot antardimensi sama
rata, sesuai jurnal rujukan.

### Fitur utama

Peta choropleth kelayakhunian per kelurahan, pewarnaan ulang berdasarkan dimensi
tertentu, panel detail per wilayah, peringkat 68 kelurahan, perbandingan dua
wilayah, filter per kecamatan dan per kelas, layer titik fasilitas kesehatan
beserta area jangkauannya, layer kesesuaian permukiman terhadap pola ruang, dan
simulasi bobot indikator sebagai analisis sensitivitas.

### Arsitektur

| Lapis | Teknologi |
|---|---|
| Pengolahan data | Python (shapely, pyproj) |
| Basis data | PostgreSQL + PostGIS |
| Backend | Node.js (Express) |
| Frontend | Next.js |
| Visualisasi peta | Leaflet.js |

PostGIS menyimpan geometri poligon beserta nilai indikatornya. Backend memanggil
data tersebut dan mengembalikan objek GeoJSON. Frontend membaca properti GeoJSON
dengan Leaflet dan memberi gradasi warna berbeda pada setiap kelurahan sesuai
rentang nilainya, sehingga terbentuk peta choropleth.

---

## 2. Sumber Data yang Akan Dipakai

Unit analisis seluruh dataset adalah kelurahan, dengan jumlah 68 kelurahan di
Kota Bogor.

### 2.1 Data spasial

| # | Dataset | Format | Tahun | Sumber | Dipakai untuk |
|---|---|---|---|---|---|
| 1 | Peta tingkat persentase penduduk dengan tingkat kesejahteraan | CSV (WKT MultiPolygon) | — | Portal data spasial | Batas administrasi 68 kelurahan sebagai unit analisis, dan kolom indeks (`ikp`) untuk dimensi ekonomi |
| 2 | Titik Puskesmas Kota Bogor | CSV (WKT Point) | — | Geoportal | Dimensi kesehatan, 25 titik |
| 3 | Titik Rumah Sakit Kota Bogor | CSV (WKT Point) | — | Geoportal | Dimensi kesehatan, 22 titik |
| 4 | Jangkauan Puskesmas dan Rumah Sakit | CSV (WKT MultiPolygon) | — | Olahan buffer 1/2/3 km | Dimensi kesehatan, cakupan layanan, 37 poligon |
| 5 | Penggunaan Lahan Kota Bogor | CSV (WKT MultiPolygon) | 2023 | Pemerintah Kota Bogor | Dimensi pendidikan (534 poligon area pendidikan), dimensi lingkungan (6.634 poligon vegetasi), dimensi ekonomi (1.419 poligon kawasan perdagangan) |
| 6 | Jalan Kota Bogor skala 1:25.000 | CSV (WKT MultiPolygon) | 2021 | Pemerintah Kota Bogor | Dimensi transportasi, 10.424 poligon badan jalan |
| 7 | Pola Ruang Kota Bogor | CSV (WKT MultiPolygon) | 2021 | RTRW Kota Bogor 2021–2041 | Layer kesesuaian ruang, 8.901 poligon peruntukan perumahan |
| 8 | Permukiman skala 1:25.000 | CSV (WKT MultiPolygon) | — | Geoportal | Layer kesesuaian ruang, 597 poligon permukiman |

### 2.2 Data atribut

| # | Dataset | Tahun | Sumber |
|---|---|---|---|
| 9 | Jumlah Penduduk menurut Kelurahan | 2022 | Dinas Kependudukan dan Catatan Sipil Kota Bogor, dipublikasikan BPS Kota Bogor pada tabel "Jumlah Penduduk dan Laju Pertumbuhan Penduduk menurut Kelurahan di Kecamatan X" untuk keenam kecamatan |

Data penduduk dipakai sebagai indikator kepadatan penduduk pada dimensi sosial
kependudukan, sekaligus sebagai penyebut seluruh indikator per kapita, yaitu
fasilitas kesehatan per 10.000 jiwa dan ruang terbuka hijau per kapita.
Totalnya 1.114.018 jiwa, dan jumlah per kecamatan sudah diuji silang terhadap
angka yang tercantum di tabel BPS.

### 2.3 Indikator yang terbentuk

| Dimensi | Sub-indikator | Dari dataset |
|---|---|---|
| Kesehatan | Fasilitas kesehatan per 10.000 jiwa; persentase luas wilayah dalam jangkauan fasilitas kesehatan | 2, 3, 4, 9 |
| Pendidikan | Persentase luas lahan pendidikan | 5 |
| Sosial kependudukan | Kepadatan penduduk | 1, 9 |
| Lingkungan | Persentase tutupan vegetasi; luas vegetasi per kapita | 5, 9 |
| Transportasi | Persentase luas badan jalan | 6 |
| Ekonomi | Indeks kesejahteraan (`ikp`); persentase luas kawasan perdagangan | 1, 5 |
| *(di luar indeks)* | Persentase permukiman yang sesuai peruntukan pola ruang | 7, 8 |

### 2.4 Keterbatasan ketersediaan data

Jurnal rujukan memakai 15 indikator, sedangkan penelitian ini memakai 10
indikator yang tersebar pada enam dimensi yang sama. Penyesuaian dilakukan
karena tidak seluruh indikator jurnal tersedia pada tingkat kelurahan di Kota
Bogor.

| Indikator jurnal | Status |
|---|---|
| Jumlah murid, jumlah guru, rasio guru-murid, rata-rata lama sekolah | Tidak tersedia pada tingkat kelurahan |
| Jumlah tenaga kesehatan | Tidak tersedia pada tingkat kelurahan |
| Angka harapan hidup, tindakan kriminalitas | Hanya tersedia pada tingkat kota |
| Jumlah trayek angkutan umum, cakupan area terlayani angkutan umum | Belum tersedia pada tingkat kelurahan, digantikan proksi kepadatan badan jalan |
| Sumber air minum, jumlah tempat pembuangan sampah | Belum diperoleh pada tingkat kelurahan |
| PDRB per wilayah | Hanya tersedia pada tingkat kecamatan ke atas |

Jurnal rujukan menyatakan keterbatasan serupa, yaitu ketidaksamaan periode data
antarsumber. Pada penelitian ini tahun data berkisar antara 2021 sampai 2023,
dengan catatan bahwa pola ruang merupakan dokumen rencana periode 2021–2041
sehingga tidak memiliki versi tahunan.

### 2.5 Rencana penambahan data

BPS Kota Bogor menerbitkan tabel jumlah sekolah dan murid menurut kelurahan per
jenjang pendidikan. Data tersebut direncanakan ditambahkan agar dimensi
pendidikan memakai indikator ketersediaan sekolah sebagaimana jurnal rujukan,
menggantikan proksi luas lahan pendidikan yang dipakai saat ini.

---

## 3. Contoh Tampilan Data pada QGIS

*(Lampirkan tangkapan layar di bagian ini.)*

Berkas yang ditampilkan: `output/kelurahan_kelayakhunian.geojson`, berisi 68
poligon kelurahan beserta seluruh nilai indikator, sistem koordinat EPSG:4326.
