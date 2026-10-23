# Bogor Liveable City

Sistem Informasi Geografis untuk menganalisis tingkat kelayakhunian 68 kelurahan
di Kota Bogor.

Indeks disusun dengan metode dari Dewi, L.A.T., Yahya, W., & Situmorang, R.
(2025), *Pengukuran Layak Huni Kota Depok pada Tingkat Meso*, Jurnal Pembangunan
Wilayah dan Kota 21(3), 387–402,
DOI [10.14710/pwk.v21i3.67908](https://doi.org/10.14710/pwk.v21i3.67908):
normalisasi min-max, agregasi bertingkat berbobot sama, dan klasifikasi lima
kelas dengan interval sama.

## Enam dimensi

Kesehatan, pendidikan, sosial kependudukan, lingkungan, transportasi, ekonomi.

Kesesuaian permukiman terhadap pola ruang tetap dihitung, tetapi berada di luar
indeks dan disajikan sebagai layer analisis tersendiri.

## Struktur

```
data/      DATASET.md (daftar dataset) dan data penduduk BPS 2022
scripts/   hitung_indikator.py, pengolahan dari CSV mentah ke indeks
output/    hasil olahan: CSV indikator dan GeoJSON 68 kelurahan
docs/      ALUR_KERJA.md, peta jalan dari data mentah ke peta di layar
```

Dataset mentah tidak disimpan di repositori ini karena ukurannya ratusan
megabita. Daftar lengkap beserta sumbernya ada di [data/DATASET.md](data/DATASET.md).

## Menjalankan pengolahan data

```bash
pip install shapely pyproj numpy
python scripts/hitung_indikator.py
```

Script membaca dataset mentah dari folder yang ditetapkan pada konstanta
`DATASET` di bagian atas berkas, lalu menulis ulang isi `output/`.

## Tech stack

PostgreSQL + PostGIS, Node.js (Express), Next.js, Leaflet.js. Alur lengkapnya
ada di [docs/ALUR_KERJA.md](docs/ALUR_KERJA.md).

## Kelompok 3

Radithya Dhiyaurrahman, Nur Izza Yarismen, Muhamad Zaidan,
Vezajiva Ariesta Maheswari, M. Karel Putra Shelvion.
