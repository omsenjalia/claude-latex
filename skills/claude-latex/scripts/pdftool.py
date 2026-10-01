#!/usr/bin/env python3
"""Inspect a source PDF before typesetting it.

  pdftool.py info   SRC.pdf                         pages, size, fonts, text layer, images
  pdftool.py render SRC.pdf OUTDIR [--dpi 110] [--pages 1-3,5]
  pdftool.py text   SRC.pdf [--pages 2]             raw text layer (spelling aid only)
  pdftool.py images SRC.pdf OUTDIR                  extract embedded raster images
  pdftool.py crop   SRC.pdf PAGE X0 Y0 X1 Y1 OUT.png [--dpi 300]
                    (coordinates in PDF points, origin top-left; PAGE is 1-based)

Requires: pip install pymupdf
"""
import argparse
import os
import sys

try:
    import pymupdf as fitz
except ImportError:  # older PyMuPDF
    try:
        import fitz
    except ImportError:
        sys.exit("PyMuPDF missing: pip install pymupdf")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def page_list(spec, n):
    if not spec:
        return list(range(n))
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a) - 1, int(b)))
        else:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < n]


def cmd_info(a):
    d = fitz.open(a.src)
    r = d[0].rect
    print(f"file:   {a.src}")
    print(f"pages:  {len(d)}")
    print(f"size:   {r.width:.0f} x {r.height:.0f} pt "
          f"({'A4' if abs(r.width - 595) < 3 and abs(r.height - 842) < 3 else 'Letter' if abs(r.width - 612) < 3 else 'other'})")
    meta = {k: v for k, v in d.metadata.items() if v}
    print(f"meta:   {meta}")
    import re
    fonts = sorted({(re.findall(r"[A-Za-z0-9-]+$", f[3]) or [f[3]])[0] for p in d for f in p.get_fonts()})
    print(f"fonts:  {fonts or 'none (scanned/handwritten image pages)'}")
    for i, p in enumerate(d):
        chars = len(p.get_text().strip())
        imgs = len(p.get_images())
        kind = "typed" if chars > 50 else ("image-only (scan/handwritten)" if imgs else "blank/vector")
        print(f"  p{i + 1}: {chars:5d} text chars, {imgs} images, drawings={len(p.get_drawings())} -> {kind}")


def cmd_render(a):
    d = fitz.open(a.src)
    os.makedirs(a.outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(a.src))[0]
    for i in page_list(a.pages, len(d)):
        out = os.path.join(a.outdir, f"{base}_p{i + 1}.png")
        d[i].get_pixmap(dpi=a.dpi).save(out)
        print(out)


def cmd_text(a):
    d = fitz.open(a.src)
    for i in page_list(a.pages, len(d)):
        print(f"===== page {i + 1} =====")
        print(d[i].get_text())


def cmd_images(a):
    d = fitz.open(a.src)
    os.makedirs(a.outdir, exist_ok=True)
    n = 0
    for i, p in enumerate(d):
        for j, img in enumerate(p.get_images(full=True)):
            xref = img[0]
            info = d.extract_image(xref)
            out = os.path.join(a.outdir, f"p{i + 1}-img{j + 1}.{info['ext']}")
            with open(out, "wb") as f:
                f.write(info["image"])
            bbox = p.get_image_bbox(img)
            print(f"{out}  ({info['width']}x{info['height']}px, on page at {tuple(round(v) for v in bbox)})")
            n += 1
    if not n:
        print("no embedded raster images (figures may be vector drawings: use crop)")


def cmd_crop(a):
    d = fitz.open(a.src)
    p = d[a.page - 1]
    clip = fitz.Rect(a.x0, a.y0, a.x1, a.y1)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    p.get_pixmap(dpi=a.dpi, clip=clip).save(a.out)
    print(a.out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("info"); s.add_argument("src"); s.set_defaults(f=cmd_info)
    s = sub.add_parser("render"); s.add_argument("src"); s.add_argument("outdir")
    s.add_argument("--dpi", type=int, default=110); s.add_argument("--pages"); s.set_defaults(f=cmd_render)
    s = sub.add_parser("text"); s.add_argument("src"); s.add_argument("--pages"); s.set_defaults(f=cmd_text)
    s = sub.add_parser("images"); s.add_argument("src"); s.add_argument("outdir"); s.set_defaults(f=cmd_images)
    s = sub.add_parser("crop"); s.add_argument("src"); s.add_argument("page", type=int)
    for c in ("x0", "y0", "x1", "y1"):
        s.add_argument(c, type=float)
    s.add_argument("out"); s.add_argument("--dpi", type=int, default=300); s.set_defaults(f=cmd_crop)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
