# Konteks Proyek — Bogor Liveable City

Dokumen ini merangkum seluruh keputusan, temuan, dan status proyek sampai
24 Oktober 2026. Ditulis agar bisa dipakai sebagai konteks awal ketika bertanya
ke asisten AI lain, tanpa perlu mengulang pembahasan dari nol.

---

## 1. Ringkasan proyek

**Nama:** Bogor Liveable City
**Jenis:** Tugas mata kuliah Sistem Informasi Geografis, IPB, Semester 5
**Kelompok:** Kelompok 3 (5 orang), Project Manager M. Karel Putra Shelvion
**Dosen/Sponsor:** Dr. Sofiyanti Indriasari, S.Kom., M.Kom.
**Periode:** 24 Agustus 2026 – 16 November 2026, metodologi Agile Scrum
**Repositori:** https://github.com/rdhiyaurrahman/bogor-liveable-city

WebGIS interaktif untuk menganalisis tingkat kelayakhunian **68 kelurahan di
Kota Bogor**. Menampilkan peta choropleth, dashboard statistik, peringkat
wilayah, perbandingan antarwilayah, dan simulasi bobot indikator.

**Unit analisis: kelurahan, bukan kecamatan.** Kota Bogor punya 68 kelurahan di
6 kecamatan (Bogor Barat 16, Bogor Selatan 16, Bogor Tengah 11, Tanah Sareal 11,
Bogor Utara 8, Bogor Timur 6). Luas total poligon 111,39 km².

---

## 2. Jurnal rujukan dan formula

Dosen mensyaratkan formula indeks berasal dari jurnal. Jurnal yang dipakai:

> Dewi, L.A.T., Yahya, W., & Situmorang, R. (2025). **Pengukuran Layak Huni Kota
> Depok pada Tingkat Meso.** *Jurnal Pembangunan Wilayah dan Kota*, 21(3),
> 387–402. DOI: 10.14710/pwk.v21i3.67908

Alasan dipilih: kota tetangga (Depok), unit analisis meso (kecamatan), memakai
data sekunder, dipetakan dengan GIS, dan formulanya ditulis eksplisit sebagai
persamaan bernomor. Jurnal ini sendiri merupakan kritik atas Most Livable City
Index (MLCI) milik IAP yang berbasis persepsi warga, bukan data objektif.

### Persamaan 1 (halaman 392) — normalisasi min-max

```
X' = (X − X_min) / (X_max − X_min)
```

Indikator yang berhubungan **negatif** terhadap kelayakhunian dibalik urutannya
(*inverse*), sehingga nilai tertinggi menjadi 0.

### Agregasi bertingkat

1. Tiap sub-indikator dinormalisasi ke 0–1.
2. Sub-indikator dalam satu dimensi **dijumlahkan**, lalu **dinormalisasi ulang**
   → skor dimensi 0–1.
3. Keenam skor dimensi **dijumlahkan**, lalu **dinormalisasi ulang** → skor akhir
   0–1.

Bobot antardimensi **sama rata**. Jurnal tidak memakai AHP. Normalisasi ulang di
tiap tingkat membuat setiap dimensi berbobot sama berapa pun jumlah
sub-indikatornya.

### Persamaan 2 (halaman 393) — klasifikasi

```
Rentang interval = (nilai tertinggi − nilai terendah) / jumlah kelas
```

Dengan 5 kelas pada rentang 0–1:

| Rentang | Kelas |
|---|---|
| 0,81 – 1,00 | Sangat Layak Huni |
| 0,61 – 0,80 | Layak Huni |
| 0,41 – 0,60 | Cukup Layak Huni |
| 0,21 – 0,40 | Tidak Layak Huni |
| 0,00 – 0,20 | Sangat Tidak Layak Huni |

Jurnal mengadopsi klasifikasi ini dari Narieswari et al. (2019).

---

## 3. Dimensi dan indikator yang dipakai

Jurnal memakai 6 dimensi dan 15 indikator. Proyek ini memakai **6 dimensi yang
sama** dengan **10 indikator**, disesuaikan ketersediaan data tingkat kelurahan.

| Dimensi | Sub-indikator (nama kolom) | Arah |
|---|---|---|
| Kesehatan | `faskes_per_10k`, `cakupan_faskes_pct` | positif |
| Pendidikan | `luas_pendidikan_pct` | positif |
| Sosial kependudukan | `kepadatan_penduduk` | positif (ikut jurnal) |
| Lingkungan | `rth_aktual_pct`, `rth_per_kapita_m2` | positif |
| Transportasi | `jalan_pct` | positif |
| Ekonomi | `ikp`, `perdagangan_pct` | positif |

**Di luar indeks:** `kesesuaian_permukiman_pct`, yaitu persentase luas permukiman
yang jatuh pada peruntukan Kawasan Perumahan atau Kawasan Campuran menurut pola
ruang. Tetap dihitung dan diekspor, tetapi disajikan sebagai **layer analisis
tersendiri**, bukan bagian indeks. Alasannya: jurnal hanya punya 6 dimensi, dan
PRD sudah memisahkan "Livability Index" dari "Analisis pola ruang/tata guna
lahan" sebagai dua fitur berbeda.

### Indikator jurnal yang tidak bisa dipenuhi

| Indikator jurnal | Alasan |
|---|---|
| Jumlah murid, jumlah guru, rasio guru-murid, rata-rata lama sekolah | tidak terbit di tingkat kelurahan |
| Jumlah tenaga kesehatan | tidak terbit di tingkat kelurahan |
| Angka harapan hidup, tindakan kriminalitas | hanya tingkat kota |
| Jumlah trayek dan cakupan angkutan umum | tidak tersedia, diganti proksi `jalan_pct` |
| Sumber air minum, jumlah TPS | belum diperoleh di tingkat kelurahan |
| PDRB per wilayah | hanya tingkat kecamatan ke atas |

Jurnal rujukan juga menyatakan keterbatasan serupa, yaitu periode data yang
tidak seragam antarsumber (Tabel 1 jurnal mencampur tahun 2022, 2023, dan 2024).

---

## 4. Dataset

### Dipakai (9 berkas)

| # | Berkas | Tahun | Peran |
|---|---|---|---|
| 1 | `peta_tingkat_persentase_penduduk_dengan_tingkat_kesejahteraan.csv` | — | Batas 68 poligon kelurahan + kolom `ikp` |
| 2 | `PUSKESMAS_PT.csv` | — | 25 titik puskesmas |
| 3 | `RUMAHSAKIT_PT_25K.csv` | — | 22 titik rumah sakit |
| 4 | `JANGKAUAN_PUSKESMAS_ RUMAHSAKIT.csv` | — | 37 poligon jangkauan 1/2/3 km |
| 5 | `PENGGUNAAN_LAHAN_KOTA_BOGOR_TAHUN_2023.csv` | 2023 | 534 poligon pendidikan, 6.634 vegetasi, 1.419 perdagangan |
| 6 | `JALAN_KOTABOGOR_2021_25K_AR.csv` | 2021 | 10.424 poligon badan jalan |
| 7 | `POLARUANG_KOTABOGOR_2021_AR.csv` | 2021 | 8.901 poligon peruntukan perumahan, 1.441 RTH rencana |
| 8 | `PEMUKIMAN_AR_25K.csv` | — | 597 poligon permukiman |
| 9 | `data/penduduk_kelurahan_2022.csv` | 2022 | Penduduk per kelurahan, dari BPS |

Berkas 1–8 berada di folder `dataset/` di luar repositori (total ±213 MB).
Berkas 9 ada di dalam repositori.

### Tidak dipakai (3 berkas)

- `peta_tingkat_persentase_rumah_tangga_tanpa_akses_ke_air_bersih_ (1).csv`
- `peta_tingkat_rata_rata_lama_sekolah_perempuan_umur_diatas_15_ta.csv`

  Keduanya **duplikat identik** berkas #1. Atribut dan geometri sama persis.
  Judulnya menyebut air bersih dan lama sekolah, tetapi **isinya tidak memuat
  data tersebut**. Jadi indikator air bersih dan rata-rata lama sekolah
  sebenarnya tidak pernah ada di dataset awal.

- `penduduk_kelurahan_2021.csv` — digantikan versi 2022 (lihat temuan di bawah).

### Sumber data penduduk

Tabel BPS Kota Bogor *"Jumlah Penduduk dan Laju Pertumbuhan Penduduk menurut
Kelurahan di Kecamatan X"*, tahun data **2022** untuk keenam kecamatan,
diperbarui serentak 3 Januari 2025, sumber asli Disdukcapil Kota Bogor.
Total **1.114.018 jiwa**.

URL: `https://bogorkota.bps.go.id/id/statistics-table/2/<id-base64>/x.html`
dengan id base64 dari `<nomor>#2`:

| Kecamatan | Nomor tabel | Total |
|---|---|---|
| Bogor Selatan | 937 | 216.501 |
| Bogor Timur | 938 | 108.212 |
| Bogor Utara | 939 | 200.200 |
| Tanah Sareal | 940 | 227.341 |
| Bogor Barat | 941 | 252.433 |
| Bogor Tengah | 942 | 109.331 |

---

## 5. Temuan penting dan jebakan teknis

Lima hal berikut sudah ditemukan dan sudah ditangani. **Jangan diulang dari
nol.**

1. **Urutan koordinat terbalik.** Berkas 1, 4, 6, 7, 8 menulis WKT dengan urutan
   **lintang-bujur**, bukan bujur-lintang standar. `POINT (-6.62 106.80)` akan
   dibaca parser standar sebagai X = −6,62 dan Y = 106,80, melempar peta ke luar
   Indonesia. Harus ditukar saat dimuat.

2. **Beda sistem koordinat.** Berkas 5 (`PENGGUNAAN_LAHAN`) memakai **UTM Zona
   48S (EPSG:32748)** dalam meter. Sisanya derajat WGS84 (EPSG:4326). Seluruh
   perhitungan luas dilakukan di EPSG:32748.

3. **Tiga file CSV kelurahan adalah duplikat identik.** Lihat bagian 4.

4. **Dua salah ketik di tabel BPS 2021.** Pasirmulya tertulis 60.177 padahal
   laki-laki 3.011 + perempuan 3.066 = 6.077. Total perempuan Bogor Tengah
   tertulis 53.890 padahal penjumlahan per kelurahan 53.980, dan kolom "Jumlah"
   di tabel yang sama (108.159) justru membenarkan angka 53.980.

5. **Label 11 kelurahan Tanah Sareal tertukar di tabel BPS 2021.** Lima kecamatan
   lain konsisten antara 2021 dan 2022 (tumbuh wajar 1–3%), hanya Tanah Sareal
   yang kacau: Kedungwaringin 9.943 → 24.183, Kedungjaya 24.945 → 13.475.
   Kumpulan angkanya sama, pasangan labelnya berbeda. Penengahnya memakai tabel
   jumlah RT per kelurahan: rasio penduduk per RT versi 2022 wajar (272–429),
   versi 2021 berantakan (140–608). **Kesimpulan: penamaan versi 2022 yang
   benar.** Belum diverifikasi ke sumber resmi ketiga (*Kecamatan Tanah Sareal
   Dalam Angka*).

6. **Tiga kolom `f*__priori` konstan.** Pada berkas #1, kolom `f4__priori`,
   `f6__priori`, dan `f11__prior` bernilai sama untuk ke-68 kelurahan, sehingga
   X_max − X_min = 0 dan min-max menghasilkan pembagian nol. Kolom-kolom ini
   dibuang, tidak dipakai.

---

## 6. Keputusan yang sudah diambil

| Keputusan | Alasan |
|---|---|
| Unit analisis kelurahan (68), bukan kecamatan (6) | lebih detail dari jurnal, disebut sebagai penyesuaian di metodologi |
| 6 dimensi persis jurnal | struktur bisa dibandingkan dengan rujukan |
| Kesesuaian ruang keluar dari indeks, jadi layer terpisah | jurnal cuma 6 dimensi, dan PRD sudah memisahkannya |
| Bobot sama rata, bukan AHP | mengikuti jurnal |
| Slider simulasi bobot = analisis sensitivitas, bukan formula | bobot 0.20/0.20/0.20/0.15/0.15/0.10 di prototipe lama tidak punya sumber |
| Penduduk pakai 2022, bukan 2021 | satu tahun untuk keenam kecamatan, satu tanggal terbit, dan versi 2021 rusak |
| `ikp` diasumsikan positif | nilai `ikp` lebih tinggi berpasangan dengan `rank` lebih baik; **belum terverifikasi** |
| `kepadatan_penduduk` diasumsikan positif | mengikuti Tabel 1 jurnal; bisa diperdebatkan untuk konteks hunian |

Dua asumsi terakhir disimpan sebagai konstanta `IKP_POSITIF` dan
`KEPADATAN_POSITIF` di bagian atas `scripts/hitung_indikator.py`, bukan ditanam
di dalam rumus, supaya mudah diuji balik.

---

## 7. Hasil perhitungan saat ini

**5 teratas:** Pabaton 1,0000 · Babakan 0,8829 · Bantarjati 0,8564 ·
Gudang 0,8499 · Babakan Pasar 0,7561

**5 terbawah:** Genteng 0,1251 · Balumbang Jaya 0,1150 · Semplak 0,1084 ·
Situ Gede 0,1053 · Pasir Mulya 0,0000

**Sebaran kelas:** Cukup Layak Huni 25 · Tidak Layak Huni 23 · Sangat Tidak
Layak Huni 9 · Layak Huni 7 · Sangat Layak Huni 4

**Korelasi dimensi terhadap indeks:**

| Dimensi | Korelasi |
|---|---|
| Ekonomi | 0,774 |
| Kesehatan | 0,623 |
| Transportasi | 0,589 |
| Pendidikan | 0,544 |
| Sosial kependudukan | 0,333 |
| Lingkungan | **−0,376** |

Polanya: pusat kota (Bogor Tengah) unggul, pinggiran barat tertinggal.

**Catatan penting soal hasil:** skor bersifat **relatif di antara 68 kelurahan
Kota Bogor**, bukan absolut. Normalisasi ulang di tahap akhir memaksa satu
kelurahan bernilai tepat 1,0000 dan satu lagi tepat 0,0000. Pasir Mulya bukan
"tidak layak huni" dalam arti mutlak, dia hanya terendah di antara 68.

---

## 8. Masalah yang masih terbuka

1. **Arti kolom `ikp` belum dipastikan.** Kolom `METADATA` kosong. Kolom ini
   penyumbang korelasi terbesar (0,774), jadi kalau arahnya ternyata terbalik,
   peringkat teratas dan terbawah bisa bertukar. **Prioritas tertinggi.**

2. **Pabaton peringkat 1 dengan 3.225 jiwa**, penduduk terkecil se-Kota Bogor,
   luas 0,634 km². Unggul karena 2 faskes dibagi penduduk sedikit = 6,2 per
   10.000 jiwa (tertinggi) dan `jalan_pct` 13,26% (tertinggi). Pabaton adalah
   kawasan perkantoran, bukan kawasan hunian. Indikator per kapita labil di
   wilayah berpenduduk sedikit.

3. **Dimensi lingkungan berlawanan arah** (−0,376). Wilayah hijau justru minim
   layanan. Ini temuan nyata pola pusat-pinggiran, harus dibahas di laporan,
   bukan dibuang.

4. **Indikator kesehatan lemah.** `faskes_total` bernilai 0 di 34 dari 68
   kelurahan, dan `cakupan_faskes_pct` bernilai 100% di 43 dari 68 karena buffer
   1–3 km menutup hampir seluruh kota yang luasnya cuma 111 km². Alternatif yang
   lebih baik: ganti ke **jarak ke faskes terdekat**, yang kontinu dan tidak
   peduli batas administrasi.

5. **Dimensi pendidikan masih proksi.** Memakai luas lahan pendidikan. BPS punya
   tabel *"Jumlah Sekolah dan Murid ... menurut Kelurahan di Kecamatan X"* per
   jenjang (contoh nomor tabel 943, 945, 946 untuk Madrasah Ibtidaiyah) yang
   lebih dekat ke indikator jurnal. **Belum diambil.**

6. **`rth_per_kapita_m2` sebarannya sangat miring** (0,8 sampai 408,3 m²/jiwa),
   sehingga min-max polos menumpuk hampir semua kelurahan di dekat nol. Jurnal
   memang memakai min-max polos tanpa transformasi.

7. **Luas total poligon 111,39 km²** belum dibandingkan dengan luas resmi BPS
   Kota Bogor. Kalau selisihnya besar, poligon sumber tergeneralisasi di skala
   1:25.000 dan semua indikator berbasis persentase luas ikut bergeser.

8. **`rth_aktual_pct` adalah tutupan vegetasi, bukan RTH publik.** Diambil dari
   `KATEGORI='Vegetasi'` yang mencakup kebun, sawah, dan pekarangan privat.
   Jangan dibandingkan dengan target 20% RTH publik Permen PUPR.

---

## 9. Tech stack dan alur sistem

| Lapis | Teknologi | Status |
|---|---|---|
| Pengolahan data | Python 3 (shapely 2.2, pyproj 3.8, numpy) | **selesai** |
| Basis data | PostgreSQL 18 + PostGIS | terpasang, belum dipakai |
| Backend | Node.js v24 + Express | belum dimulai |
| Frontend | Next.js | belum dimulai |
| Peta | Leaflet.js | ada di prototipe `fix.html` |

```
[1] CSV mentah  ->  [2] Python/shapely  ->  [3] CSV + GeoJSON
                                                   |
[6] Next.js + Leaflet  <-  [5] Express  <-  [4] PostGIS
```

Tahap 1–3 selesai. Tahap 4–6 belum.

**Penting:** GeoJSON hasil tahap 3 sudah EPSG:4326 dengan urutan bujur-lintang
yang benar. Penukaran sumbu sudah dikerjakan di tahap 2, jadi **jangan ditukar
lagi** saat memuat ke PostGIS.

Rencana endpoint:

```
GET /api/kelurahan        -> FeatureCollection seluruh kelurahan
GET /api/kelurahan/:kode  -> satu kelurahan untuk panel detail
```

Leaflet menyentuh `window`, jadi komponen peta harus dimuat tanpa render server:
`dynamic(() => import('@/components/Peta'), { ssr: false })`.

---

## 10. Struktur repositori

```
data/
  DATASET.md                        daftar dataset + catatan teknis
  penduduk_kelurahan_2022.csv       penduduk 68 kelurahan dari BPS
scripts/
  hitung_indikator.py               pengolahan CSV mentah -> indeks (359 baris)
output/
  indikator_kelayakhunian_kelurahan.csv   68 baris x 41 kolom
  kelurahan_kelayakhunian.geojson         68 poligon + seluruh atribut, 2,4 MB
docs/
  ALUR_KERJA.md                     peta alur data mentah -> peta di layar
  PROPOSAL_BAGIAN_DATA.md           bagian proposal untuk dikumpulkan
  KONTEKS_PROYEK.md                 dokumen ini
README.md
.gitignore                          dataset/ dikecualikan, ratusan MB
```

### Kolom di `output/indikator_kelayakhunian_kelurahan.csv`

- Identitas: `kode`, `kelurahan`, `kecamatan`, `luas_km2`
- 12 indikator mentah: `penduduk`, `kepadatan_penduduk`, `faskes_total`,
  `faskes_per_km2`, `faskes_per_10k`, `cakupan_faskes_pct`,
  `rth_per_kapita_m2`, `luas_pendidikan_pct`, `rth_aktual_pct`,
  `rth_rtrw_pct`, `jalan_pct`, `permukiman_pct`, `perdagangan_pct`,
  `kesesuaian_permukiman_pct`, `ikp`
- Versi ternormalisasi 0–1: sama dengan di atas, berawalan `n_`
- 6 skor dimensi: berawalan `dim_`
- Hasil: `indeks_kelayakhunian` (0–1), `skor100` (0–100), `kelas`, `rank`

Kolom `faskes_per_km2`, `faskes_total`, `permukiman_pct`, `rth_rtrw_pct`, dan
`penduduk` hanya pembanding, tidak masuk perhitungan indeks.

---

## 11. Prototipe lama

`fix.html` adalah prototipe kasar berisi Leaflet + choropleth + ranking +
perbandingan + modal simulasi bobot. Tata letaknya sudah sejalan dengan FR-01
sampai FR-18 di PRD dan layak dipakai ulang, **tetapi datanya karangan**: 14
kelurahan dummy dengan skor ditulis tangan dan poligon buatan 5 titik.

Dua catatan: bobot 0.20/0.20/0.20/0.15/0.15/0.10 di dalamnya tidak punya sumber,
dan ada bug di `fix.html:2239` di mana total bobot dihitung dari 5 slider
sedangkan `applySimWeights()` memberikan sisanya ke dimensi keenam, sehingga
saat tertulis "Total 100%" bobot dimensi keenam justru 0%.

Prototipe ini **belum** diganti dengan data asli.

---

## 12. Cara menjalankan ulang pengolahan

```bash
pip install shapely pyproj numpy
python scripts/hitung_indikator.py
```

Script membaca dataset mentah dari konstanta `DATASET` di bagian atas berkas,
lalu menulis ulang isi `output/`. Ada uji silang bawaan: total penduduk per
kecamatan dicocokkan dengan angka tabel BPS, dan proses dihentikan bila ada
kelurahan yang tidak dapat pasangan data penduduk.

Catatan lingkungan: di laptop ini ada dua interpreter Python (laragon 3.13 dan
Python312). Pastikan library terpasang di interpreter yang sama dengan yang
menjalankan script.
