import plistlib, pathlib, re, sys, json, glob

UUIDRE = re.compile(r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')
# structural keys that legitimately hold UUIDs we mint ourselves
STRUCTURAL = {'UUID','GroupingIdentifier','OutputUUID','WFControlFlowMode','WFSerializationType'}
# text-plumbing keys we already understand
KNOWN_TEXT = {'WFTextTokenString','WFTextTokenAttachment'}

hits = []  # (source, action_id, keypath, kind, value_repr)

def classify(key, val, path):
    """Return (kind, repr) if this looks like a device-minted / picker value."""
    if isinstance(val, str):
        if UUIDRE.match(val) and key not in STRUCTURAL:
            return ('uuid-string', val)
        if val.startswith(('applenotes:','x-apple','shortcuts://','calshow:')):
            return ('uri-identifier', val)
        if key in ('BundleIdentifier','TeamIdentifier','bundleIdentifier','teamIdentifier'):
            return ('app-identity', val)
        if key.lower().endswith('identifier') and key not in STRUCTURAL and len(val) > 0:
            return ('identifier-string', val)
    if isinstance(val, bytes):
        return ('opaque-data', f'<{len(val)} bytes>')
    return None

def walk(node, path, src, aid):
    if isinstance(node, dict):
        for k, v in node.items():
            p = f'{path}.{k}' if path else k
            c = classify(k, v, p)
            if c:
                hits.append((src, aid, p, c[0], c[1]))
            walk(v, p, src, aid)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f'{path}[{i}]', src, aid)

def scan(fp, src):
    try:
        p = plistlib.load(open(fp,'rb'))
    except Exception as e:
        print(f'  !! {src}: {e}', file=sys.stderr); return
    for a in p.get('WFWorkflowActions', []):
        aid = a.get('WFWorkflowActionIdentifier','?')
        walk(a.get('WFWorkflowActionParameters',{}), '', src, aid)

for d in sorted(glob.glob(sys.argv[1] + '/*/Shortcut.xml')):
    scan(d, 'DONOR:' + pathlib.Path(d).parent.name)
for g in sorted(glob.glob(sys.argv[2] + '/*.xml')):
    scan(g, 'GOLDEN:' + pathlib.Path(g).stem[:8])

print(json.dumps(hits, indent=0))
