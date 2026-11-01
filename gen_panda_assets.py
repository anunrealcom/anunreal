#!/usr/bin/env python3
# Generates panda branding assets, minimal brush style (stdlib only).
import math, struct, zlib, os

BASE = os.path.dirname(os.path.abspath(__file__))
INK = (43, 43, 48)
PAPER = (247, 246, 242)

# Design space: 256x256, all coords in that space.
def in_ellipse(x, y, cx, cy, rx, ry, rot=0.0):
    dx = x - cx
    dy = y - cy
    if rot != 0.0:
        c = math.cos(rot)
        s = math.sin(rot)
        dx, dy = dx * c + dy * s, -dx * s + dy * c
    return (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry) <= 1.0

def in_rrect(x, y, cx, cy, half, r):
    dx = abs(x - cx) - (half - r)
    dy = abs(y - cy) - (half - r)
    if dx > r or dy > r:
        return False
    if dx > 0 and dy > 0:
        return dx * dx + dy * dy <= r * r
    return True

def mouth_dx(y):
    # one side of the mouth: dx = 14*sqrt((y-172)/15), from y=172 to 188
    if y < 172 or y > 188:
        return None
    return 14.0 * math.sqrt((y - 172) / 15.0)

def badge(x, y):
    """Return (r,g,b,a) at design-space coords (0..256)."""
    if not in_rrect(x, y, 128, 128, 120, 52):
        return (0, 0, 0, 0)
    col = PAPER
    d = math.hypot(x - 128, y - 142)
    if abs(d - 72) <= 4.5:  # face brush ring
        col = INK
    if in_ellipse(x, y, 102, 130, 14, 20, 0.244) or in_ellipse(x, y, 154, 130, 14, 20, -0.244):
        col = INK
    if math.hypot(x - 99, y - 125) <= 4.5 or math.hypot(x - 157, y - 125) <= 4.5:
        col = PAPER  # eye highlights
    if in_ellipse(x, y, 128, 160, 10, 7):
        col = INK  # nose
    dx = mouth_dx(y)
    if dx is not None:
        if abs(x - (128 - dx)) <= 3.0 or abs(x - (128 + dx)) <= 3.0:
            col = INK
    if math.hypot(x - 86, y - 74) <= 21 or math.hypot(x - 170, y - 74) <= 21:
        col = INK  # ears on top
    return (col[0], col[1], col[2], 255)

def render(S, SS):
    HR = S * SS
    out = bytearray(S * S * 4)
    for oy in range(S):
        for ox in range(S):
            sr = sg = sb = sa = 0
            for iy in range(SS):
                for ix in range(SS):
                    px = (ox * SS + ix + 0.5) / HR * 256.0
                    py = (oy * SS + iy + 0.5) / HR * 256.0
                    r, g, b, a = badge(px, py)
                    sr += r * a; sg += g * a; sb += b * a; sa += a
            idx = (oy * S + ox) * 4
            if sa > 0:
                out[idx] = sr // sa
                out[idx + 1] = sg // sa
                out[idx + 2] = sb // sa
                out[idx + 3] = sa // (SS * SS)
            else:
                out[idx] = out[idx + 1] = out[idx + 2] = out[idx + 3] = 0
    return out

def splash_bg(x, y, S):
    t = y / S
    r = int(38 + (22 - 38) * t)
    g = int(50 + (28 - 50) * t)
    b = int(74 + (46 - 74) * t)
    d = math.hypot(x / S - 0.5, y / S - 0.52)
    glow = max(0.0, 1.0 - d / 0.5)
    return (int(r + (60 - r) * glow * 0.45),
            int(g + (80 - g) * glow * 0.45),
            int(b + (115 - b) * glow * 0.45))

def render_splash(S, SS):
    HR = S * SS
    scale = S * 0.62 / 256.0  # badge occupies 62% of splash
    off = (S - 256.0 * scale) / 2.0
    out = bytearray(S * S * 4)
    for oy in range(S):
        for ox in range(S):
            sr = sg = sb = 0
            for iy in range(SS):
                for ix in range(SS):
                    hx = ox * SS + ix + 0.5
                    hy = oy * SS + iy + 0.5
                    br, bg, bb = splash_bg(hx, hy, S)
                    px = (hx - off) / scale
                    py = (hy - off) / scale
                    if 0 <= px < 256 and 0 <= py < 256:
                        r, g, b, a = badge(px, py)
                        wa = a / 255.0
                        sr += int(br + (r - br) * wa)
                        sg += int(bg + (g - bg) * wa)
                        sb += int(bb + (b - bb) * wa)
                    else:
                        sr += br; sg += bg; sb += bb
            n = SS * SS
            idx = (oy * S + ox) * 4
            out[idx] = sr // n
            out[idx + 1] = sg // n
            out[idx + 2] = sb // n
            out[idx + 3] = 255
    return out

def write_png(path, W, H, buf):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(buf[y * W * 4:(y + 1) * W * 4])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff))
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", comp))
        f.write(chunk(b"IEND", b""))

def build_ico(buf256, sizes):
    images = []
    for S in sizes:
        sub = bytearray(S * S * 4)
        for ty in range(S):
            sy = min(255, int(ty * 256 / S))
            for tx in range(S):
                sx = min(255, int(tx * 256 / S))
                si = (sy * 256 + sx) * 4
                di = (ty * S + tx) * 4
                sub[di:di + 4] = buf256[si:si + 4]
        xor = bytearray()
        for ty in range(S - 1, -1, -1):
            row = sub[ty * S * 4:(ty + 1) * S * 4]
            for i in range(0, len(row), 4):
                xor += bytes((row[i + 2], row[i + 1], row[i], row[i + 3]))
        andmask = bytes(S * ((S + 31) // 32 * 4))
        dib = struct.pack("<IiiHHIIiiII", 40, S, 2 * S, 1, 32, 0,
                          len(xor) + len(andmask), 0, 0, 0, 0)
        images.append((S, dib + xor + andmask))
    icondir = struct.pack("<HHH", 0, 1, len(images))
    entries = b""
    data = b""
    offset = 6 + 16 * len(images)
    for S, img in images:
        w = 0 if S >= 256 else S
        entries += struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(img), offset)
        data += img
        offset += len(img)
    return icondir + entries + data

print("Rendering brush panda icon buffer (256) ...")
buf256 = render(256, 3)
ico = build_ico(buf256, [16, 32, 48, 64, 128, 256])
with open(os.path.join(BASE, "platform", "windows", "godot.ico"), "wb") as f:
    f.write(ico)
with open(os.path.join(BASE, "platform", "windows", "godot_console.ico"), "wb") as f:
    f.write(ico)
print("Wrote godot.ico / godot_console.ico:", len(ico), "bytes")

# Runtime window icon (main.cpp embeds this and calls DisplayServer::set_icon).
write_png(os.path.join(BASE, "main", "app_icon.png"), 256, 256, buf256)
print("Wrote main/app_icon.png")

print("Rendering splash (512) ...")
buf_sp = render_splash(512, 2)
write_png(os.path.join(BASE, "main", "splash.png"), 512, 512, buf_sp)
write_png(os.path.join(BASE, "main", "splash_editor.png"), 512, 512, buf_sp)
print("Wrote splash.png / splash_editor.png")
print("DONE")
