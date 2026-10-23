# -*- coding: utf-8 -*-
"""
Hitung indikator kelayakhunian per kelurahan Kota Bogor (68 kelurahan).

Metode mengikuti:
  Dewi, L.A.T., Yahya, W., & Situmorang, R. (2025). Pengukuran Layak Huni Kota
  Depok pada Tingkat Meso. Jurnal Pembangunan Wilayah dan Kota, 21(3), 387-402.
  DOI: 10.14710/pwk.v21i3.67908
  - Persamaan 1: min-max normalization, X' = (X - Xmin) / (Xmax - Xmin)
  - indikator berhubungan negatif dibalik (inverse)
  - skor dimensi = normalisasi ulang dari jumlah sub-indikator ternormalisasi
  - skor akhir  = normalisasi ulang dari jumlah skor dimensi
  - Persamaan 2: 5 kelas dengan interval sama (0.00-0.20 ... 0.81-1.00)

Indeks memakai enam dimensi persis seperti jurnal. Kesesuaian permukiman
terhadap pola ruang tetap dihitung, tetapi sebagai layer analisis tersendiri
di luar indeks, mengikuti pemisahan yang sudah ada di PRD.

Catatan CRS: seluruh CSV sumber menulis WKT dengan urutan LINTANG-BUJUR
(terbalik dari standar), KECUALI PENGGUNAAN_LAHAN yang sudah UTM 48S.
Semua perhitungan luas dilakukan di EPSG:32748 (meter).
"""
import csv
import json
import os

import numpy as np
import shapely
from shapely import wkt as shp_wkt
from shapely.ops import unary_union
from pyproj import Transformer

csv.field_size_limit(10 ** 9)

DATASET = r"C:\Users\User\Documents\IPB 2024\Semester 5\Bogor Liveable City\dataset"
OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")

KELURAHAN_CSV = "peta_tingkat_persentase_penduduk_dengan_tingkat_kesejahteraan.csv"
PENDUDUK_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "data", "penduduk_kelurahan_2022.csv")

# Total per kecamatan yang tercetak di tabel BPS, dipakai sebagai uji silang.
TOTAL_KECAMATAN_BPS = {
    "Bogor Barat": 252433, "Bogor Selatan": 216501, "Bogor Tengah": 109331,
    "Bogor Utara": 200200, "Bogor Timur": 108212, "Tanah Sareal": 227341,
}

# Jurnal Depok menempatkan kepadatan penduduk sebagai indikator berhubungan
# POSITIF terhadap layak huni. Arah ini bisa diperdebatkan untuk konteks hunian
# (padat = sesak), jadi disimpan sebagai saklar, bukan ditanam di rumus.
KEPADATAN_POSITIF = True

# Ejaan nama kelurahan berbeda antara tabel BPS dan atribut peta (wadmkd).
ALIAS_BPS_KE_PETA = {
    "balungbangjaya": "balumbangjaya",
    "batarjati": "bantarjati",
    "barangansiang": "baranangsiang",
    "kebonkelapa": "kebonkalapa",
}

# Arah hubungan `ikp` terhadap kelayakhunian BELUM terverifikasi (kolom METADATA
# kosong). Diasumsikan positif karena ikp lebih tinggi = `rank` lebih baik.
# Ubah ke False bila metadata sumber ternyata menyatakan sebaliknya.
IKP_POSITIF = True

_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32748", always_xy=True)


def _swap(coords):
    return coords[:, ::-1]


def _project(coords):
    x, y = _to_utm.transform(coords[:, 0], coords[:, 1])
    return np.column_stack([x, y])


def load_geom(wkt_text, latlon_order=True):
    """WKT -> geometry UTM 48S. latlon_order=True untuk file yang menulis (lat lon)."""
    if not wkt_text or not wkt_text.strip():
        return None
    g = shp_wkt.loads(wkt_text)
    if latlon_order:
        g = shapely.transform(g, _swap)
        g = shapely.transform(g, _project)
    if not g.is_valid:
        g = shapely.make_valid(g)
    return g


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- kelurahan
log("[1/8] Memuat 68 poligon kelurahan ...")
kel = []
with open(os.path.join(DATASET, KELURAHAN_CSV), encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        g = load_geom(row["geom"])
        kel.append({
            "kode": row["kdepum"],
            "kelurahan": row["wadmkd"].replace("Kelurahan ", ""),
            "kecamatan": row["wadmkc"],
            "ikp": float(row["ikp"]),
            "geom": g,
            "luas_m2": g.area,
        })
log("      %d kelurahan, luas total %.2f km2" % (len(kel), sum(k["luas_m2"] for k in kel) / 1e6))


def _norm_nama(s):
    return s.lower().replace(" ", "").replace("-", "")


# Penduduk per kelurahan (BPS, tahun data 2022).
penduduk = {}
per_kecamatan = {}
with open(PENDUDUK_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(line for line in f if not line.startswith("#")):
        nama = _norm_nama(row["kelurahan_bps"])
        jml = int(row["penduduk"])
        penduduk[ALIAS_BPS_KE_PETA.get(nama, nama)] = jml
        per_kecamatan[row["kecamatan"]] = per_kecamatan.get(row["kecamatan"], 0) + jml

for kec, total in TOTAL_KECAMATAN_BPS.items():
    assert per_kecamatan[kec] == total, \
        "total %s tidak cocok: %d vs %d di BPS" % (kec, per_kecamatan[kec], total)

hilang = [k["kelurahan"] for k in kel if _norm_nama(k["kelurahan"]) not in penduduk]
assert not hilang, "kelurahan tanpa data penduduk: %s" % hilang
for k in kel:
    k["penduduk"] = penduduk[_norm_nama(k["kelurahan"])]
log("      penduduk tergabung: %d jiwa untuk %d kelurahan"
    % (sum(k["penduduk"] for k in kel), len(kel)))

tree = shapely.STRtree([k["geom"] for k in kel])
N = len(kel)


def acc_area(path, latlon_order, keep, label):
    """Jumlahkan luas irisan poligon sumber terhadap tiap kelurahan (m2)."""
    out = np.zeros(N)
    n_kept = 0
    with open(os.path.join(DATASET, path), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not keep(row):
                continue
            g = load_geom(row["geom"], latlon_order)
            if g is None or g.is_empty:
                continue
            n_kept += 1
            for i in tree.query(g):
                inter = shapely.intersection(kel[i]["geom"], g)
                if not inter.is_empty:
                    out[i] += inter.area
    log("      %s: %d poligon diproses" % (label, n_kept))
    return out


def count_points(path, label):
    out = np.zeros(N)
    with open(os.path.join(DATASET, path), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            x, y = _to_utm.transform(float(row["X_LONG"]), float(row["Y_LAT"]))
            p = shapely.Point(x, y)
            for i in tree.query(p):
                if shapely.contains(kel[i]["geom"], p):
                    out[i] += 1
    log("      %s: %d titik masuk wilayah Kota Bogor" % (label, int(out.sum())))
    return out


# ------------------------------------------------------------------ dimensi
log("[2/8] Fasilitas kesehatan (titik) ...")
n_pkm = count_points("PUSKESMAS_PT.csv", "puskesmas")
n_rs = count_points("RUMAHSAKIT_PT_25K.csv", "rumah sakit")

log("[3/8] Cakupan jangkauan faskes (union buffer) ...")
jangkauan = []
with open(os.path.join(DATASET, "JANGKAUAN_PUSKESMAS_ RUMAHSAKIT.csv"), encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        g = load_geom(row["geom"])
        if g is not None and not g.is_empty:
            jangkauan.append(g)
jangkauan_union = unary_union(jangkauan)
cakupan = np.array([shapely.intersection(k["geom"], jangkauan_union).area for k in kel])
log("      %d poligon jangkauan digabung" % len(jangkauan))

log("[4/8] Penggunaan lahan 2023 (UTM, ~19k poligon) ...")
lahan_pendidikan = acc_area("PENGGUNAAN_LAHAN_KOTA_BOGOR_TAHUN_2023.csv", False,
                            lambda r: r["SUB_KATEGO"] == "Pendidikan", "pendidikan")
lahan_vegetasi = acc_area("PENGGUNAAN_LAHAN_KOTA_BOGOR_TAHUN_2023.csv", False,
                          lambda r: r["KATEGORI"] == "Vegetasi", "vegetasi (RTH aktual)")
lahan_dagang = acc_area("PENGGUNAAN_LAHAN_KOTA_BOGOR_TAHUN_2023.csv", False,
                        lambda r: r["SUB_KATEGO"] == "Kawasan Perdagangan", "kawasan perdagangan")

log("[5/8] Badan jalan ...")
jalan = acc_area("JALAN_KOTABOGOR_2021_25K_AR.csv", True, lambda r: True, "badan jalan")

log("[6/8] Permukiman ...")
permukiman = acc_area("PEMUKIMAN_AR_25K.csv", True, lambda r: True, "permukiman")

log("[7/8] Pola ruang RTRW 2021 (~30k poligon, file besar) ...")
PERUMAHAN = {"Kawasan Perumahan", "Kawasan Campuran"}
pr_perumahan = acc_area("POLARUANG_KOTABOGOR_2021_AR.csv", True,
                        lambda r: r["d_ORDE02"] in PERUMAHAN, "peruntukan perumahan")
pr_rth = acc_area("POLARUANG_KOTABOGOR_2021_AR.csv", True,
                  lambda r: r["d_ORDE02"] == "Ruang Terbuka Hijau", "RTH rencana")

# -------------------------------------------------------------- normalisasi
log("[8/8] Normalisasi min-max, agregasi dimensi, klasifikasi ...")


def minmax(v, inverse=False):
    v = np.asarray(v, dtype=float)
    lo, hi = v.min(), v.max()
    if hi - lo == 0:
        log("      ! indikator konstan (Xmax-Xmin=0) -> diisi 0.5")
        return np.full_like(v, 0.5)
    n = (v - lo) / (hi - lo)
    return 1.0 - n if inverse else n


luas_km2 = np.array([k["luas_m2"] for k in kel]) / 1e6
luas_m2 = luas_km2 * 1e6
ikp = np.array([k["ikp"] for k in kel])
jiwa = np.array([k["penduduk"] for k in kel], dtype=float)

# kesesuaian permukiman terhadap peruntukan ruang (indikator spasial tambahan)
kesesuaian = np.where(permukiman > 0, pr_perumahan / np.maximum(permukiman, 1e-9) * 100, 0.0)

raw = {
    "penduduk": jiwa,
    "kepadatan_penduduk": jiwa / luas_km2,
    "faskes_total": n_pkm + n_rs,
    "faskes_per_km2": (n_pkm + n_rs) / luas_km2,
    "faskes_per_10k": (n_pkm + n_rs) / jiwa * 10000,
    "cakupan_faskes_pct": cakupan / luas_m2 * 100,
    "rth_per_kapita_m2": lahan_vegetasi / jiwa,
    "luas_pendidikan_pct": lahan_pendidikan / luas_m2 * 100,
    "rth_aktual_pct": lahan_vegetasi / luas_m2 * 100,
    "rth_rtrw_pct": pr_rth / luas_m2 * 100,
    "jalan_pct": jalan / luas_m2 * 100,
    "permukiman_pct": permukiman / luas_m2 * 100,
    "perdagangan_pct": lahan_dagang / luas_m2 * 100,
    "kesesuaian_permukiman_pct": np.clip(kesesuaian, 0, 100),
    "ikp": ikp,
}

DIMENSI = {
    "kesehatan": [("faskes_per_10k", False), ("cakupan_faskes_pct", False)],
    "pendidikan": [("luas_pendidikan_pct", False)],
    "sosial_kependudukan": [("kepadatan_penduduk", not KEPADATAN_POSITIF)],
    "lingkungan": [("rth_aktual_pct", False), ("rth_per_kapita_m2", False)],
    "transportasi": [("jalan_pct", False)],
    "ekonomi": [("ikp", not IKP_POSITIF), ("perdagangan_pct", False)],
}

# kesesuaian_permukiman_pct sengaja TIDAK masuk indeks: jurnal rujukan hanya
# punya enam dimensi di atas, dan PRD menempatkan analisis pola ruang sebagai
# fitur tersendiri. Nilainya tetap diekspor (mentah dan ternormalisasi
# n_kesesuaian_permukiman_pct) untuk dipakai sebagai layer analisis terpisah.

norm = {key: minmax(raw[key]) for key in raw}

dim_scores = {}
for dim, subs in DIMENSI.items():
    total = np.zeros(N)
    for name, inv in subs:
        total += minmax(raw[name], inverse=inv)
    dim_scores[dim] = minmax(total)  # normalisasi ulang -> 0..1

indeks = minmax(sum(dim_scores.values()))


def kelas(s):
    if s > 0.80:
        return "Sangat Layak Huni"
    if s > 0.60:
        return "Layak Huni"
    if s > 0.40:
        return "Cukup Layak Huni"
    if s > 0.20:
        return "Tidak Layak Huni"
    return "Sangat Tidak Layak Huni"


order = np.argsort(-indeks)
rank = np.empty(N, dtype=int)
rank[order] = np.arange(1, N + 1)

# ----------------------------------------------------------------- keluaran
os.makedirs(OUTDIR, exist_ok=True)

cols = (["kode", "kelurahan", "kecamatan", "luas_km2"]
        + list(raw.keys())
        + ["n_" + k for k in raw.keys()]
        + ["dim_" + d for d in DIMENSI]
        + ["indeks_kelayakhunian", "skor100", "kelas", "rank"])

csv_path = os.path.join(OUTDIR, "indikator_kelayakhunian_kelurahan.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for i, k in enumerate(kel):
        row = [k["kode"], k["kelurahan"], k["kecamatan"], round(luas_km2[i], 4)]
        row += [round(float(raw[c][i]), 4) for c in raw]
        row += [round(float(norm[c][i]), 4) for c in raw]
        row += [round(float(dim_scores[d][i]), 4) for d in DIMENSI]
        row += [round(float(indeks[i]), 4), round(float(indeks[i]) * 100, 1),
                kelas(indeks[i]), int(rank[i])]
        w.writerow(row)
log("      CSV  -> " + csv_path)

# GeoJSON: kembalikan ke WGS84 dengan urutan bujur-lintang yang benar
_to_wgs = Transformer.from_crs("EPSG:32748", "EPSG:4326", always_xy=True)


def _unproject(coords):
    x, y = _to_wgs.transform(coords[:, 0], coords[:, 1])
    return np.column_stack([x, y])


features = []
for i, k in enumerate(kel):
    props = {
        "kode": k["kode"], "kelurahan": k["kelurahan"], "kecamatan": k["kecamatan"],
        "luas_km2": round(float(luas_km2[i]), 4),
        "indeks_kelayakhunian": round(float(indeks[i]), 4),
        "skor100": round(float(indeks[i]) * 100, 1),
        "kelas": kelas(indeks[i]), "rank": int(rank[i]),
    }
    for d in DIMENSI:
        props["dim_" + d] = round(float(dim_scores[d][i]), 4)
    for c in raw:
        props[c] = round(float(raw[c][i]), 4)
    features.append({
        "type": "Feature",
        "properties": props,
        "geometry": json.loads(shapely.to_geojson(shapely.transform(k["geom"], _unproject))),
    })

gj_path = os.path.join(OUTDIR, "kelurahan_kelayakhunian.geojson")
with open(gj_path, "w", encoding="utf-8") as f:
    json.dump({"type": "FeatureCollection",
               "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
               "features": features}, f)
log("      GeoJSON -> %s (%.1f MB)" % (gj_path, os.path.getsize(gj_path) / 1e6))

log("\n=== 5 TERATAS ===")
for i in order[:5]:
    log("  %2d. %-18s %-14s %.4f  %s" % (rank[i], kel[i]["kelurahan"], kel[i]["kecamatan"],
                                         indeks[i], kelas(indeks[i])))
log("=== 5 TERBAWAH ===")
for i in order[-5:]:
    log("  %2d. %-18s %-14s %.4f  %s" % (rank[i], kel[i]["kelurahan"], kel[i]["kecamatan"],
                                         indeks[i], kelas(indeks[i])))
log("\nSelesai.")
