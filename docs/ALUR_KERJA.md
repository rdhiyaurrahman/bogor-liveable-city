# Alur Kerja Bogor Liveable City

Dokumen ini memetakan jalan data dari berkas mentah sampai peta choropleth di
layar, dan menandai posisi pekerjaan yang sudah selesai.

## Tech stack

| Lapis | Teknologi | Status |
|---|---|---|
| Pengolahan data | Python 3 (shapely, pyproj, numpy) | sudah jalan |
| Basis data | PostgreSQL 18 + PostGIS | terpasang, belum dipakai |
| Backend | Node.js + Express | belum dimulai |
| Frontend | Next.js | belum dimulai |
| Peta | Leaflet.js | ada di prototipe `fix.html` |

## Enam tahap

```
[1] CSV mentah          dataset/*.csv (8 berkas) + data/penduduk_kelurahan_2022.csv
         |
         v
[2] Pengolahan          scripts/hitung_indikator.py
    (Python/shapely)    reproyeksi, tumpang susun, min-max, agregasi, klasifikasi
         |
         v
[3] Hasil olahan        output/indikator_kelayakhunian_kelurahan.csv
                        output/kelurahan_kelayakhunian.geojson
         |
         v
[4] Basis data          PostgreSQL + PostGIS, tabel kelurahan (geom + atribut)
         |
         v
[5] Backend             Express, GET /api/kelurahan -> FeatureCollection GeoJSON
         |
         v
[6] Frontend            Next.js + Leaflet, choropleth + dashboard + ranking
```

Tahap 1 sampai 3 sudah selesai. Tahap 4 sampai 6 belum.

### Tahap 2 — kenapa perlu Python, bukan langsung PostGIS

Perhitungan indeks butuh tumpang susun puluhan ribu poligon (10.424 badan jalan,
8.901 peruntukan perumahan, 6.634 vegetasi) terhadap 68 kelurahan. Ini bisa saja
dilakukan dengan query PostGIS, tetapi dikerjakan di Python supaya langkah
normalisasi dan agregasinya terbaca sebagai satu berkas yang bisa ditunjukkan ke
dosen sebagai implementasi rumus jurnal. PostGIS tetap menyimpan hasilnya.

Jalankan ulang dengan:

```bash
python scripts/hitung_indikator.py
```

### Tahap 4 — memuat ke PostGIS

Yang dimuat adalah **hasil olahan**, bukan CSV mentah. Satu tabel sudah cukup,
karena unit analisisnya tunggal.

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE kelurahan (
  kode                      text PRIMARY KEY,
  kelurahan                 text NOT NULL,
  kecamatan                 text NOT NULL,
  luas_km2                  double precision,
  penduduk                  integer,
  kepadatan_penduduk        double precision,
  dim_kesehatan             double precision,
  dim_pendidikan            double precision,
  dim_sosial_kependudukan   double precision,
  dim_lingkungan            double precision,
  dim_transportasi          double precision,
  dim_ekonomi               double precision,
  kesesuaian_permukiman_pct double precision,
  indeks_kelayakhunian      double precision,
  kelas                     text,
  rank                      integer,
  geom                      geometry(MultiPolygon, 4326)
);

CREATE INDEX kelurahan_geom_idx ON kelurahan USING GIST (geom);
```

GeoJSON hasil tahap 3 sudah EPSG:4326 dengan urutan bujur-lintang yang benar,
jadi bisa dimuat apa adanya dengan `ogr2ogr` atau skrip Node. Tidak perlu
menukar sumbu lagi di tahap ini; penukaran sudah dikerjakan di tahap 2.

### Tahap 5 — backend Express

Satu endpoint sudah memenuhi kebutuhan peta:

```
GET /api/kelurahan          -> FeatureCollection seluruh kelurahan
GET /api/kelurahan/:kode    -> satu kelurahan, untuk panel detail
```

PostGIS merakit GeoJSON-nya sendiri, jadi backend tidak perlu menyusun ulang:

```sql
SELECT json_build_object(
  'type', 'FeatureCollection',
  'features', json_agg(ST_AsGeoJSON(k.*)::json)
) FROM kelurahan k;
```

### Tahap 6 — frontend Next.js + Leaflet

Leaflet menyentuh `window`, jadi komponen petanya harus dimuat tanpa render di
server:

```js
const Peta = dynamic(() => import('@/components/Peta'), { ssr: false });
```

Pewarnaan choropleth membaca properti GeoJSON dan memakai lima kelas jurnal:

| Rentang | Kelas |
|---|---|
| 0,81 – 1,00 | Sangat Layak Huni |
| 0,61 – 0,80 | Layak Huni |
| 0,41 – 0,60 | Cukup Layak Huni |
| 0,21 – 0,40 | Tidak Layak Huni |
| 0,00 – 0,20 | Sangat Tidak Layak Huni |

Metrik yang bisa dipetakan: `indeks_kelayakhunian`, keenam kolom `dim_`, dan
`kesesuaian_permukiman_pct` sebagai layer analisis tersendiri di luar indeks.

## Urutan pengerjaan yang disarankan

1. Muat GeoJSON ke PostGIS, pastikan `SELECT count(*)` mengembalikan 68.
2. Bangun endpoint `/api/kelurahan`, uji dengan `curl`.
3. Pindahkan tampilan `fix.html` ke Next.js, ganti `bogorRegions` dummy dengan
   hasil `fetch` ke endpoint tadi.
4. Baru kerjakan fitur turunan: ranking, perbandingan dua wilayah, filter,
   simulasi bobot.

Prototipe `fix.html` berisi 14 kelurahan karangan dengan skor yang ditulis
tangan. Tata letaknya dipakai ulang, datanya dibuang.

## Yang masih terbuka

- Arti kolom `ikp` belum dipastikan, padahal pengaruhnya terbesar terhadap indeks.
- Dimensi pendidikan baru memakai proksi luas lahan. BPS punya tabel jumlah
  sekolah per kelurahan yang lebih dekat ke indikator jurnal.
- Pabaton menempati peringkat 1 dengan penduduk 3.225 jiwa, terkecil se-Kota
  Bogor. Indikator per kapita memang labil di wilayah berpenduduk sedikit.
- Dimensi lingkungan berkorelasi negatif terhadap indeks (-0,376), perlu
  dibahas di laporan, bukan dibuang.
