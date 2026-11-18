"""מעתיק את העותקים המוצפנים של הלקוחות (portal/g...) מהמערכת לתיקיית data בדף.
שימוש: python3 -I tools/export.py <תיקיית ההורדה של portal> <תיקיית המאגר>
הקבצים מוצפנים במערכת עצמה; הסקריפט לא רואה סיסמאות ולא מפענח דבר."""
import json, os, re, sys
src, repo = sys.argv[1], sys.argv[2]
out = os.path.join(repo, 'data'); os.makedirs(out, exist_ok=True)
ok = re.compile(r'^g[0-9a-f]{24}(-\d{1,3})?$')
keep = set()
for fn in sorted(os.listdir(src)):
    doc_id = fn[:-5] if fn.endswith('.json') else fn
    if not ok.match(doc_id): continue
    d = json.load(open(os.path.join(src, fn), encoding='utf-8'))
    if '-' in doc_id: rec = {'data': str(d.get('data', ''))}
    else:
        rec = {'v': 1, 'iv': str(d['iv']), 'z': str(d.get('z')).lower() in ('true', '1'), 'n': int(float(d.get('n') or 1)),
               'data': str(d.get('data', '')), 'updated': str(d.get('updated', ''))}
    p = os.path.join(out, doc_id + '.json'); new = json.dumps(rec, separators=(',', ':'))
    if not os.path.exists(p) or open(p, encoding='utf-8').read() != new: open(p, 'w', encoding='utf-8').write(new)
    keep.add(doc_id + '.json')
# לקוח שהגישה שלו בוטלה: הקובץ שלו נמחק מהדף
removed = [f for f in os.listdir(out) if f.endswith('.json') and f not in keep]
for f in removed: os.remove(os.path.join(out, f))
print(f'clients/parts: {len(keep)}, removed: {len(removed)}')
