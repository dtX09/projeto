"""
Mapa mundial (equirectangular) com imagem mundo.png e marcação de rotas.
Vista fixa: mapa completo redimensionado ao canvas (sem zoom nem pan).
"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from typing import Any, Sequence

from PIL import Image, ImageDraw, ImageFont, ImageTk

ROUTE_LINE_RGBA = (90, 176, 232, 240)
PIN_RGBA = (226, 75, 74, 255)


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _resolve_mundo_path() -> Path:
    return _project_root() / "imgs" / "mundo.png"


def lat_lng_to_pixel(lat: float, lng: float, img_w: int, img_h: int) -> tuple[int, int]:
    x = int((lng + 180) / 360 * img_w)
    y = int((90 - lat) / 180 * img_h)
    return x, y


def _map_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if sys.platform == "win32":
        for p in (
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except OSError:
            return ImageFont.load_default()


def draw_pin(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str | None = None,
    color: tuple[int, int, int, int] = PIN_RGBA,
) -> None:
    r = 13
    draw.ellipse([x - r, y - r * 2 - r, x + r, y - r], fill=color[:3], outline="white", width=3)
    draw.ellipse([x - 5, y - r * 2 - r // 2, x + 5, y - r - r // 2 + 5], fill="white")
    draw.polygon([x - 5, y - r, x + 5, y - r, x, y], fill=color[:3], outline="white", width=1)

    if not label:
        return

    font_size = 13
    font = _map_font(font_size)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 8
    tx = x + 16
    ty = y - r * 2 - r - th - pad - 4
    box = [tx - pad, ty - pad, tx + tw + pad, ty + th + pad]
    try:
        draw.rounded_rectangle(
            box,
            radius=8,
            fill=(15, 20, 35, 245),
            outline=(255, 255, 255, 230),
            width=2,
        )
    except AttributeError:
        draw.rectangle(box, fill=(15, 20, 35, 245), outline="white", width=2)
    try:
        draw.text(
            (tx, ty),
            label,
            fill="white",
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )
    except TypeError:
        draw.text((tx, ty), label, fill="white", font=font)


class WorldRouteMapController:
    """Canvas com imagem completa redimensionada, rota desenhada por cima."""

    def __init__(self, canvas: tk.Canvas) -> None:
        self._canvas = canvas
        self._waypoints: list[Any] = []
        self._canvas_w = max(100, canvas.winfo_reqwidth())
        self._canvas_h = max(80, canvas.winfo_reqheight())
        self._photo: ImageTk.PhotoImage | None = None

        path = _resolve_mundo_path()
        self._base_image = Image.open(path).convert("RGBA") if path.is_file() else None

        self._canvas.bind("<Configure>", self._on_configure)

    def set_waypoints(self, waypoints: Sequence[Any]) -> None:
        self._waypoints = list(waypoints)

    def _build_composite_image(self) -> Image.Image:
        if not self._base_image:
            return Image.new("RGBA", (800, 400), (20, 40, 80, 255))

        img = self._base_image.copy()
        draw = ImageDraw.Draw(img, "RGBA")
        iw, ih = img.size

        pixel_points: list[tuple[int, int]] = []
        for wp in self._waypoints:
            px, py = lat_lng_to_pixel(float(wp.latitude), float(wp.longitude), iw, ih)
            pixel_points.append((px, py))

        if len(pixel_points) >= 2:
            draw.line(pixel_points, fill=ROUTE_LINE_RGBA, width=5)

        for i, wp in enumerate(self._waypoints):
            px, py = pixel_points[i]
            short = str(wp.name) if len(str(wp.name)) <= 28 else str(wp.name)[:25] + "…"
            draw_pin(draw, px, py, label=f"{i + 1}. {short}")

        return img

    def refresh(self) -> None:
        self._canvas.delete("all")
        if not self._base_image:
            self._canvas.create_text(
                self._canvas_w // 2,
                self._canvas_h // 2,
                text=f"Coloque mundo.png em:\n{_resolve_mundo_path()}",
                fill="#8a9bb0",
                font=("Helvetica", 9),
                justify="center",
            )
            return

        img = self._build_composite_image()
        display = img.resize((self._canvas_w, self._canvas_h), Image.Resampling.LANCZOS)
        self._photo = ImageTk.PhotoImage(display)
        self._canvas.create_image(0, 0, anchor="nw", image=self._photo)

        if not self._waypoints:
            self._canvas.create_text(
                self._canvas_w // 2,
                32,
                text="Sem portos com coordenadas para esta rota.",
                fill="#ffb060",
                font=("Helvetica", 10, "bold"),
            )

    def _on_configure(self, event: tk.Event) -> None:
        if event.widget is self._canvas and event.width > 10 and event.height > 10:
            self._canvas_w = event.width
            self._canvas_h = event.height
            self.refresh()
