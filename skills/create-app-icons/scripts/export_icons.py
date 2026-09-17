#!/usr/bin/env python3
"""Export one icon variant for iOS, Google Play, Android, and marketing.

Requires Pillow. The input master and adaptive background must be opaque square
images of at least 1024 px. The adaptive foreground must be a square transparent
image of at least 1024 px; a white-on-transparent monochrome layer is optional.
"""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageCms, ImageColor, ImageDraw


DENSITIES = {
    "mdpi": 1.0,
    "hdpi": 1.5,
    "xhdpi": 2.0,
    "xxhdpi": 3.0,
    "xxxhdpi": 4.0,
}
LANCZOS = Image.Resampling.LANCZOS
PLAY_MAX_BYTES = 1024 * 1024
SRGB_PROFILE = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))


def read_square(path: Path, label: str, opaque: bool) -> Image.Image:
    with Image.open(path) as opened:
        original = opened.copy()
        source_profile = opened.info.get("icc_profile")
    alpha = original.convert("RGBA").getchannel("A")
    if source_profile:
        try:
            rgb = ImageCms.profileToProfile(
                original.convert("RGB"),
                ImageCms.ImageCmsProfile(BytesIO(source_profile)),
                SRGB_PROFILE,
                outputMode="RGB",
            )
        except ImageCms.PyCMSError as error:
            raise ValueError(f"Cannot convert {label} to sRGB: {error}") from error
    else:
        rgb = original.convert("RGB")  # untagged input is treated as sRGB
    image = Image.merge("RGBA", (*rgb.split(), alpha))
    if image.width != image.height or image.width < 1024:
        raise ValueError(f"{label} must be square and at least 1024 px")
    alpha_min, _ = image.getchannel("A").getextrema()
    if opaque and alpha_min != 255:
        raise ValueError(f"{label} must be fully opaque")
    if not opaque and alpha_min == 255:
        raise ValueError(f"{label} must have a transparent exterior")
    return image


def resized(image: Image.Image, size: int) -> Image.Image:
    return image.resize((size, size), LANCZOS)


def png_bytes(image: Image.Image) -> bytes:
    stream = BytesIO()
    image.save(stream, format="PNG", optimize=True, compress_level=9, icc_profile=SRGB_PROFILE.tobytes())
    return stream.getvalue()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_bytes(image))


def warn_safe_zone(image: Image.Image, label: str) -> None:
    alpha = image.getchannel("A").point(lambda value: 255 if value > 32 else 0)
    box = alpha.getbbox()
    if not box:
        raise ValueError(f"{label} has no visible artwork")
    margin = image.width * 21 / 108  # centered 66 dp area within a 108 dp layer
    if box[0] < margin or box[1] < margin or box[2] > image.width - margin or box[3] > image.height - margin:
        print(f"WARNING: {label} reaches outside the adaptive 66 dp safe zone; inspect launcher masks")


def rounded_legacy(master: Image.Image) -> Image.Image:
    mask = Image.new("L", master.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, master.width - 1, master.height - 1), fill=255)
    result = Image.new("RGBA", master.size, (0, 0, 0, 0))
    result.paste(master, (0, 0), mask)
    return result


def adaptive_xml(with_monochrome: bool) -> str:
    mono = '    <monochrome android:drawable="@drawable/ic_launcher_monochrome" />\n' if with_monochrome else ""
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
        '    <background android:drawable="@drawable/ic_launcher_background" />\n'
        '    <foreground android:drawable="@drawable/ic_launcher_foreground" />\n'
        f"{mono}"
        '</adaptive-icon>\n'
    )


def marketing(master: Image.Image, border_color: str, canvas_color: str) -> Image.Image:
    scale = 2
    width = 1080 * scale
    margin = 28 * scale
    radius = 182 * scale
    border = 4 * scale
    side = width - 2 * margin
    canvas = Image.new("RGB", (width, width), canvas_color)
    icon = resized(master.convert("RGB"), side)
    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, side - 1, side - 1), radius=radius, fill=255)
    canvas.paste(icon, (margin, margin), mask)
    ImageDraw.Draw(canvas).rounded_rectangle(
        (margin, margin, width - margin - 1, width - margin - 1),
        radius=radius,
        outline=border_color,
        width=border,
    )
    return canvas.resize((1080, 1080), LANCZOS)


def export(args: argparse.Namespace) -> None:
    out: Path = args.out
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"Output folder is not empty: {out}")

    master = read_square(args.master, "Color master", opaque=True)
    foreground = read_square(args.foreground, "Adaptive foreground", opaque=False)
    background = read_square(args.adaptive_background, "Adaptive background", opaque=True)
    monochrome = read_square(args.monochrome, "Monochrome foreground", opaque=False) if args.monochrome else None
    ImageColor.getrgb(args.border_color)
    ImageColor.getrgb(args.canvas_color)
    warn_safe_zone(foreground, "Adaptive foreground")
    if monochrome:
        warn_safe_zone(monochrome, "Monochrome foreground")

    master_1024 = resized(master, 1024)
    foreground_1024 = resized(foreground, 1024)
    background_1024 = resized(background, 1024)
    play_bytes = png_bytes(resized(master_1024, 512))
    if len(play_bytes) > PLAY_MAX_BYTES:
        raise ValueError("Google Play PNG exceeds 1024 KB; simplify or optimize the artwork and export again")
    save(master_1024.convert("RGB"), out / "source" / "color-master-1024.png")
    save(foreground_1024, out / "source" / "adaptive-foreground-1024.png")
    save(background_1024.convert("RGB"), out / "source" / "adaptive-background-1024.png")
    if monochrome:
        save(resized(monochrome, 1024), out / "source" / "monochrome-foreground-1024.png")

    save(master_1024.convert("RGB"), out / "apple" / "AppIcon-1024.png")
    play_path = out / "google-play" / "listing-icon-512.png"
    play_path.parent.mkdir(parents=True, exist_ok=True)
    play_path.write_bytes(play_bytes)

    round_icon = rounded_legacy(master_1024)
    for density, factor in DENSITIES.items():
        legacy_size = int(48 * factor)
        layer_size = int(108 * factor)
        mipmap = out / "android" / "res" / f"mipmap-{density}"
        drawable = out / "android" / "res" / f"drawable-{density}"
        save(resized(master_1024, legacy_size), mipmap / "ic_launcher.png")
        save(resized(round_icon, legacy_size), mipmap / "ic_launcher_round.png")
        save(resized(foreground_1024, layer_size), drawable / "ic_launcher_foreground.png")
        save(resized(background_1024, layer_size).convert("RGB"), drawable / "ic_launcher_background.png")
        if monochrome:
            save(resized(monochrome, layer_size), drawable / "ic_launcher_monochrome.png")

    xml_dir = out / "android" / "res" / "mipmap-anydpi-v26"
    xml_dir.mkdir(parents=True, exist_ok=True)
    xml = adaptive_xml(monochrome is not None)
    (xml_dir / "ic_launcher.xml").write_text(xml, encoding="utf-8")
    (xml_dir / "ic_launcher_round.xml").write_text(xml, encoding="utf-8")
    save(marketing(master_1024, args.border_color, args.canvas_color), out / "marketing" / "icon-1080-rounded-border.png")
    print(f"Exported icon files to {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--foreground", type=Path, required=True)
    parser.add_argument("--adaptive-background", type=Path, required=True)
    parser.add_argument("--monochrome", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--border-color", default="#D5D9DF")
    parser.add_argument("--canvas-color", default="#FFFFFF")
    args = parser.parse_args()
    try:
        export(args)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
