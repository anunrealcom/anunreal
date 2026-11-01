#!/usr/bin/env python3
# Scan compiled objs for stale branding: old "Godot Engine" strings and old PNG-based ico bytes.
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(ROOT, "bin", "obj")
OLD_STR = b"Godot Engine"
NEW_STR = b"AnUnreal Engine"
CN_STR = "一幻 Engine".encode("utf-8")
PNG_SIG = b"\x89PNG\r\n\x1a\n"          # old godot.ico embeds PNG-compressed 256px
BMP256_HDR = bytes.fromhex("280000000001000000020000")  # new all-BMP ico 256px header

stale_str, stale_ico, ok_ico = [], [], []
for dirpath, _, files in os.walk(OBJ):
    for fn in files:
        if not fn.endswith(".obj"):
            continue
        p = os.path.join(dirpath, fn)
        try:
            d = open(p, "rb").read()
        except OSError:
            continue
        has_old = OLD_STR in d
        has_png_ico = PNG_SIG in d
        has_bmp_ico = BMP256_HDR in d
        if has_old or CN_STR in d:
            stale_str.append((os.path.relpath(p, ROOT), d.count(OLD_STR), d.count(CN_STR)))
        if "godot_res" in fn:
            (ok_ico if (has_bmp_ico and not has_png_ico) else stale_ico).append(os.path.relpath(p, ROOT))

print("=== objs containing stale 'Godot Engine' / '一幻 Engine' strings ===")
for p, n, c in sorted(stale_str):
    print(f"  {p}  (Godot Engine x{n}, 一幻 x{c})")
print(f"total: {len(stale_str)}")
print("=== godot_res objs icon check ===")
for p in ok_ico:
    print("  NEW-ICON ok:", p)
for p in stale_ico:
    print("  OLD-ICON stale:", p)

if "--delete" in sys.argv:
    removed = 0
    for p, _, _ in stale_str:
        full = os.path.join(ROOT, p)
        if os.path.isfile(full):
            os.remove(full)
            removed += 1
    print(f"DELETED {removed} stale objs (they will be recompiled with current branding)")

