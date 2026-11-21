from pathlib import Path
from weasyprint import HTML
import mistune
ROOT=Path(__file__).resolve().parent.parent
src=ROOT/'reports/Scientific_Gate_Report_20261119.md'
md=mistune.create_markdown(plugins=['table'])
body=md(src.read_text())
style='''
@page { size:A4; margin:17mm 17mm 18mm 17mm; @bottom-left {content: "LEAP Paper 7 · Scientific Gate · 19 Nov 2026"; color:#667382; font:8pt DejaVu Sans;} @bottom-right {content: "Page " counter(page) " of " counter(pages); color:#667382; font:8pt DejaVu Sans;} }
body {font-family:"DejaVu Sans",Arial,sans-serif; color:#1c2836; font-size:9.4pt; line-height:1.42;}
h1{font-size:20pt; line-height:1.22; margin:0 0 8pt; font-weight:700; letter-spacing:-.2pt;}
h2{font-size:12.5pt; border-bottom:.6pt solid #bfc7d0; padding-bottom:3pt; margin:12pt 0 5pt; color:#253747; page-break-after:avoid;}
h3{font-size:11pt; margin:11pt 0 5pt; page-break-after:avoid;}
p{margin:0 0 6pt; orphans:3;widows:3;}
strong {font-weight:700;}
blockquote{margin:9pt 0 11pt 12pt; border-left:2pt solid #4e6b84; padding:3pt 0 3pt 9pt; color:#30475c;}
code{font-family:DejaVu Sans Mono,monospace;font-size:8.2pt; overflow-wrap:anywhere;color:#23395c;}
a {color:#26486d;text-decoration:none;}
table {width:100%; table-layout:fixed; border-collapse:collapse; margin:8pt 0 12pt; font-size:7.9pt; line-height:1.33;}
thead {display:table-header-group;}
tr{page-break-inside:avoid;}
th{color:#162839;font-weight:700;background:#e9edf0;}
th,td {padding:2.9pt 4.5pt; border-bottom:.5pt solid #b9c4ce; text-align:left; overflow-wrap:anywhere;word-break:normal;vertical-align:top;}
li {margin:0 0 3pt;}
hr{height:.5pt;background:#b9c4ce;border:0;}
'''
html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{style}</style></head><body>{body}</body></html>'
(ROOT/'reports/Scientific_Gate_Report_20261119.html').write_text(html)
HTML(string=html,base_url=str(ROOT)).write_pdf(ROOT/'reports/Scientific_Gate_Report_20261119.pdf')
print('wrote',ROOT/'reports/Scientific_Gate_Report_20261119.pdf')
