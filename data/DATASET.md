# Daftar Dataset — Bogor Liveable City

Unit analisis: **68 kelurahan Kota Bogor**. Indeks memakai 6 dimensi mengikuti
Dewi, Yahya & Situmorang (2025), *Pengukuran Layak Huni Kota Depok pada Tingkat
Meso*, Jurnal Pembangunan Wilayah dan Kota 21(3), 387–402,
DOI [10.14710/pwk.v21i3.67908](https://doi.org/10.14710/pwk.v21i3.67908).

## A. Dataset yang dipakai (9 berkas)

| # | Berkas | Ukuran | Tahun | Dipakai untuk | Sumber |
|---|---|---|---|---|---|
| 1 | `peta_tingkat_persentase_penduduk_dengan_tingkat_kesejahteraan.csv` | 2,1 MB | — | Batas 68 poligon kelurahan (unit analisis) dan kolom `ikp` untuk dimensi ekonomi | Portal asal **belum terverifikasi** |
| 2 | `PUSKESMAS_PT.csv` | 4 KB | — | 25 titik puskesmas, dimensi kesehatan | Geoportal / Ina-Geoportal |
| 3 | `RUMAHSAKIT_PT_25K.csv` | 4 KB | — | 22 titik rumah sakit, dimensi kesehatan | Geoportal / Ina-Geoportal |
| 4 | `JANGKAUAN_PUSKESMAS_ RUMAHSAKIT.csv` | 0,6 MB | — | 37 poligon area jangkauan 1/2/3 km, dimensi kesehatan | Olahan buffer |
| 5 | `PENGGUNAAN_LAHAN_KOTA_BOGOR_TAHUN_2023.csv` | 53,4 MB | 2023 | Dimensi pendidikan (534 poligon), lingkungan (6.634 poligon vegetasi), ekonomi (1.419 poligon perdagangan) | Pemkot Bogor |
| 6 | `JALAN_KOTABOGOR_2021_25K_AR.csv` | 28,5 MB | 2021 | Dimensi transportasi, 10.424 poligon badan jalan | Pemkot Bogor |
| 7 | `POLARUANG_KOTABOGOR_2021_AR.csv` | 124,5 MB | 2021 | Layer kesesuaian ruang (8.901 poligon peruntukan perumahan) dan RTH rencana | RTRW Kota Bogor 2021–2041 |
| 8 | `PEMUKIMAN_AR_25K.csv` | 1,5 MB | — | Layer kesesuaian ruang, 597 poligon permukiman | Geoportal / Ina-Geoportal |
| 9 | `penduduk_kelurahan_2022.csv` | 2 KB | 2022 | Dimensi sosial kependudukan, dan penyebut semua indikator per kapita | BPS Kota Bogor (lihat di bawah) |
| 10 | `osm/jalan_osm_bogor.geojson` | 7,4 MB | 2026 | Jaringan jalan untuk menghitung jarak tempuh ke fasilitas kesehatan, 21.276 ruas | OpenStreetMap via Overpass API (lihat di bawah) |

Berkas 1–8 ada di folder `dataset/` milik kelompok. Berkas 9 dan 10 dikumpulkan
sendiri dan disimpan di repositori ini.

## B. Dataset yang TIDAK dipakai

| Berkas | Alasan |
|---|---|
| `peta_tingkat_persentase_rumah_tangga_tanpa_akses_ke_air_bersih_ (1).csv` | Duplikat identik berkas #1. Atribut dan geometri sama persis (hash atribut sama, 2.221.662 karakter geometri sama). Tidak memuat data air bersih. |
| `peta_tingkat_rata_rata_lama_sekolah_perempuan_umur_diatas_15_ta.csv` | Duplikat identik berkas #1. Tidak memuat data lama sekolah. |
| `penduduk_kelurahan_2021.csv` | Digantikan versi 2022. Label 11 kelurahan Tanah Sareal tertukar, dan ada dua salah ketik. |

## C. Asal data penduduk (berkas #9)

Tahun data 2022, sumber Dinas Kependudukan dan Catatan Sipil Kota Bogor,
dipublikasikan BPS Kota Bogor pada tabel *"Jumlah Penduduk dan Laju Pertumbuhan
Penduduk menurut Kelurahan di Kecamatan X"*. Keenam tabel diperbarui serentak
3 Januari 2025, jadi tahun datanya seragam. Total 1.114.018 jiwa.

| Kecamatan | Tabel | Total |
|---|---|---|
| Bogor Selatan | [id 937](https://bogorkota.bps.go.id/id/statistics-table/2/OTM3IzI=/x.html) | 216.501 |
| Bogor Timur | [id 938](https://bogorkota.bps.go.id/id/statistics-table/2/OTM4IzI=/x.html) | 108.212 |
| Bogor Utara | [id 939](https://bogorkota.bps.go.id/id/statistics-table/2/OTM5IzI=/x.html) | 200.200 |
| Tanah Sareal | [id 940](https://bogorkota.bps.go.id/id/statistics-table/2/OTQwIzI=/x.html) | 227.341 |
| Bogor Barat | [id 941](https://bogorkota.bps.go.id/id/statistics-table/2/OTQxIzI=/x.html) | 252.433 |
| Bogor Tengah | [id 942](https://bogorkota.bps.go.id/id/statistics-table/2/OTQyIzI=/x.html) | 109.331 |

Keenam total itu diuji ulang oleh script dan akan menghentikan proses bila tidak cocok.

## C2. Asal data jaringan jalan (berkas #10)

Sumber: **OpenStreetMap**, diambil melalui **Overpass API** pada 24 Oktober 2026.
Cap waktu basis data OSM yang terbaca pada respons: `2026-10-24T10:28:36Z`.
Lisensi: **Open Database License (ODbL)**, wajib dicantumkan atribusi
"© OpenStreetMap contributors" pada setiap peta yang memakainya.

Data ini bukan hasil mengunduh berkas jadi dari suatu portal. Data diminta ke
server Overpass dengan query berikut, lalu hasilnya dipotong pada batas
administrasi Kota Bogor:

```
[out:json][timeout:600];
way["highway"](-6.70,106.72,-6.50,106.86);
out geom;
```

Kotak koordinat itu adalah batas wilayah Kota Bogor ditambah margin, diturunkan
dari berkas #1. Perintah pengambilannya:

```bash
curl -A "BogorLiveableCity/1.0 (academic GIS project)" \
     --data-urlencode "data@query.txt" \
     -o osm_jalan_bogor.json https://overpass-api.de/api/interpreter
```

Hasil mentahnya 42.502 ruas berukuran 32,4 MB, mencakup wilayah lebih luas dari
Kota Bogor. Setelah dipotong pada batas administrasi tersisa **21.276 ruas**
yang disimpan sebagai `osm/jalan_osm_bogor.geojson` (EPSG:4326, urutan
bujur-lintang). Atribut yang dipertahankan: `osm_id`, `highway`, `name`,
`oneway`.

Komposisi jenis jalan pada data mentah:

| `highway=` | Jumlah ruas | Keterangan |
|---|---|---|
| residential | 20.628 | jalan permukiman |
| living_street | 9.611 | gang |
| service | 7.078 | jalan akses |
| path | 1.352 | jalan setapak |
| footway | 916 | trotoar / pejalan kaki |
| track | 493 | jalan tanah |
| unclassified | 473 | jalan lokal |
| tertiary | 451 | kolektor sekunder |
| primary | 325 | arteri primer |
| trunk | 298 | jalan nasional |
| secondary | 157 | kolektor primer |
| motorway | 148 | jalan tol |

Catatan: nama Kota Bogor di OSM terdaftar sebagai **"Bogor"** pada
`admin_level=5`, bukan "Kota Bogor". Query yang memakai nama "Kota Bogor" akan
mengembalikan hasil kosong.

### Graf jaringan yang terbentuk

| | |
|---|---|
| Ruas dipakai | 41.859 |
| Simpul | 286.259 |
| Sisi | 300.592 |
| Komponen tersambung terbesar | 283.236 simpul (98,9%) |

Perbandingan jarak lurus dan jarak tempuh melalui jalan, diukur dari titik pusat
tiap kelurahan ke fasilitas terdekat:

| | Jarak lurus (median) | Jarak jaringan (median) | Rasio |
|---|---|---|---|
| Puskesmas | 920 m | 1.273 m | 1,36× |
| Rumah sakit | 955 m | 1.480 m | 1,44× |

## D. Keluaran olahan

| Berkas | Isi |
|---|---|
| `output/indikator_kelayakhunian_kelurahan.csv` | 68 baris: 12 indikator mentah, 12 ternormalisasi (`n_`), 6 skor dimensi (`dim_`), indeks, skor100, kelas, rank |
| `output/kelurahan_kelayakhunian.geojson` | 68 poligon WGS84 (EPSG:4326) berisi seluruh atribut di atas |
| `output/peta_jaringan_jalan.png` | Pratinjau jaringan jalan, batas kelurahan, dan titik fasilitas kesehatan |

## E. Catatan teknis yang wajib dibaca sebelum mengolah ulang

1. **Urutan koordinat terbalik.** Berkas 1, 4, 6, 7, 8 menulis WKT dengan urutan
   lintang-bujur, bukan bujur-lintang. `POINT (-6.62 106.80)` akan dibaca parser
   standar sebagai X=-6.62, Y=106.80 dan melempar peta ke luar Indonesia.
   Harus ditukar saat dimuat.
2. **Beda sistem koordinat.** Berkas 5 memakai UTM Zona 48S (EPSG:32748) dalam
   meter, sisanya derajat WGS84. Semua perhitungan luas di script dilakukan di
   EPSG:32748.
3. **Tahun data tidak seragam**, yaitu 2021, 2022, dan 2023. Pola ruang adalah
   dokumen rencana 2021–2041, jadi memang tidak punya versi tahunan. Jurnal
   rujukan juga mencampur 2022–2024 dan menuliskannya sebagai keterbatasan.
4. **Arti kolom `ikp` belum terverifikasi** karena kolom `METADATA` kosong.
   Kolom ini menyumbang korelasi terbesar terhadap indeks (0,774), jadi arah
   hubungannya harus dipastikan sebelum laporan final. Saklarnya ada di
   `scripts/hitung_indikator.py` (`IKP_POSITIF`).
