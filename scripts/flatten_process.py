# -*- coding: utf-8 -*-
"""process プリセットの inherits 連鎖を解決して、1枚の完全なJSONにする。

BambuStudio の CLI は --load-settings で渡した process の inherits を解決しない。
そのため「0.08mm ...」という名前のプリセットを渡しても層厚が既定(0.2mm)に落ちる。
フィラメント側の flatten_filament.py と同じ考え方で、process も平坦化する。
"""
import json, os, sys
DIRS = ["/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/process",
        "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL"]

def find(name):
    for d in DIRS:
        for root, _, files in os.walk(d):
            for f in files:
                if f == name + ".json":
                    return os.path.join(root, f)
    return None

def load(name, seen=None):
    seen = seen or set()
    if name in seen:
        return {}
    seen.add(name)
    p = find(name)
    if not p:
        return {}
    d = json.load(open(p, encoding="utf-8"))
    base = load(d["inherits"], seen) if d.get("inherits") else {}
    base.update({k: v for k, v in d.items() if k != "inherits"})
    return base

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    overlay = json.load(open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else {}
    d = load(name)
    d.update({k: v for k, v in overlay.items()
              if k not in ("type", "name", "from", "setting_id", "instantiation", "inherits")})
    d["type"] = "process"; d["name"] = overlay.get("name", name) + " (flat)"
    d.pop("inherits", None); d["from"] = "User"; d["instantiation"] = "true"
    json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print("平坦化 %s -> %s （%d項目, layer_height=%s, brim=%s）"
          % (name, out, len(d), d.get("layer_height"), d.get("brim_type")))
