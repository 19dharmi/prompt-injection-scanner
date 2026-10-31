import json
import html

with open("results.json") as f:
    results = json.load(f)

rows = ""
for r in sorted(results, key=lambda r: r["leaks"], reverse=True):
    rate = 100 * r["leaks"] // r["runs"]
    color = "#d9534f" if rate >= 60 else "#f0ad4e" if rate >= 20 else "#5cb85c"
    text = r["example_leak"] or "-"
    i = text.lower().find("bluebird")
    start = max(0, i - 100) if i >= 0 else 0
    example = html.escape(text[start:start + 300])
    rows += f"""<tr>
<td>{html.escape(r['category'])}</td>
<td>{html.escape(r['prompt'])}</td>
<td style="color:{color};font-weight:bold">{r['leaks']}/{r['runs']} ({rate}%)</td>
<td>{example}</td></tr>"""

total = sum(r["leaks"] for r in results)
tries = sum(r["runs"] for r in results)

page = f"""<html><head><meta charset="utf-8"><title>Prompt Injection Scan Report</title>
<style>body{{font-family:sans-serif;margin:2rem}}
table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top}}
th{{background:#eee}}</style></head>
<body><h1>Prompt Injection Scan Report</h1>
<p>Overall: {total}/{tries} attempts leaked ({100 * total // tries}%)</p>
<table><tr><th>Category</th><th>Attack prompt</th><th>Leak rate</th><th>Example leaked reply</th></tr>{rows}</table>
</body></html>"""

with open("report.html", "w") as f:
    f.write(page)
print("Saved report.html")

