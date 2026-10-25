# -*- coding: utf-8 -*-
"""Ubah berkas Markdown jadi PDF A4 lewat Chrome headless.

Pemakaian:
    python scripts/md_ke_pdf.py docs/PRD.md output/PRD_A1_Kelompok3.pdf
"""
import os
import subprocess
import sys

import markdown

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

GAYA = """
@page { size: A4; margin: 20mm 18mm 18mm 18mm; }
body { font-family: "Segoe UI", Calibri, Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.55; color: #1a1a1a; margin: 0; }
h1 { font-size: 20pt; color: #16425b; margin: 0 0 4pt; line-height: 1.25;
     border-bottom: 2.5pt solid #16425b; padding-bottom: 6pt; }
h2 { font-size: 14pt; color: #16425b; margin: 20pt 0 7pt;
     border-bottom: 0.7pt solid #b6c2cc; padding-bottom: 3pt;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #2f6690; margin: 13pt 0 5pt; page-break-after: avoid; }
h4 { font-size: 10.5pt; color: #2f6690; margin: 10pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 7pt; text-align: justify; }
/* Chrome headless salah memilih font untuk penanda daftar bawaan,
   jadi bulletnya digambar sendiri lewat ::before */
ul { margin: 0 0 7pt; padding-left: 4pt; list-style: none; }
ol { margin: 0 0 7pt; padding-left: 18pt; }
li { margin-bottom: 2.5pt; }
ul > li { position: relative; padding-left: 12pt; }
ul > li::before { content: "\\2022"; position: absolute; left: 1pt; top: -0.5pt;
                  color: #2f6690; font-size: 11pt; line-height: 1.5; }
table { border-collapse: collapse; width: 100%; margin: 7pt 0 11pt;
        font-size: 9pt; page-break-inside: avoid; }
th { background: #16425b; color: #fff; text-align: left; padding: 5pt 6pt;
     font-weight: 600; border: 0.5pt solid #16425b; }
td { padding: 4.5pt 6pt; border: 0.5pt solid #c8d2da; vertical-align: top; }
/* tanpa ini kode seperti FR-09 dipecah dua baris pada tanda hubungnya */
td:first-child { white-space: nowrap; }
tr:nth-child(even) td { background: #f4f7f9; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt;
       background: #eef2f5; padding: 1pt 3pt; border-radius: 2pt; }
pre { background: #f4f7f9; border-left: 2.5pt solid #2f6690; padding: 8pt 10pt;
      margin: 7pt 0 11pt; page-break-inside: avoid; overflow-x: hidden; }
pre code { background: none; padding: 0; font-size: 9pt; line-height: 1.4; }
blockquote { border-left: 2.5pt solid #81a4bd; background: #f4f7f9;
             margin: 7pt 0 11pt; padding: 7pt 11pt; font-style: italic; }
blockquote p { margin: 0; }
hr { border: none; border-top: 0.7pt solid #c8d2da; margin: 14pt 0; }
strong { color: #0f2d3f; }
a { color: #2f6690; text-decoration: none; word-break: break-all; }
"""


def main():
    if len(sys.argv) < 3:
        sys.exit("pemakaian: python scripts/md_ke_pdf.py <masukan.md> <keluaran.pdf>")
    md_path, pdf_path = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    teks = open(md_path, encoding="utf-8").read()
    isi = markdown.markdown(teks, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    html_path = os.path.splitext(pdf_path)[0] + ".html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="id"><head><meta charset="utf-8">'
                "<title>%s</title><style>%s</style></head><body>%s</body></html>"
                % (os.path.basename(md_path), GAYA, isi))

    if not os.path.exists(CHROME):
        sys.exit("Chrome tidak ditemukan di %s. Buka %s lalu cetak ke PDF secara manual."
                 % (CHROME, html_path))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--print-to-pdf=" + pdf_path,
                    "--virtual-time-budget=10000", html_path],
                   check=True, capture_output=True, timeout=180)
    print("PDF  -> %s (%.2f MB)" % (pdf_path, os.path.getsize(pdf_path) / 1e6))
    print("HTML -> %s" % html_path)


if __name__ == "__main__":
    main()
