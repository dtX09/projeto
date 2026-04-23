from __future__ import annotations

import io
import urllib.request

from PIL import Image, ImageTk
from app.utils.resource_path import resolve_resource_path


def open_pil_image(url_or_path: str) -> Image.Image:
    """Abre uma imagem a partir de URL http(s) ou caminho local (sem redimensionar)."""
    raw = url_or_path.strip()
    lowered = raw.lower()

    if lowered.startswith(("http://", "https://")):
        req = urllib.request.Request(raw, headers={"User-Agent": "CargoNauta/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data))
    else:
        path = resolve_resource_path(raw)
        if not path.is_file():
            raise FileNotFoundError(f"Ficheiro não encontrado: {path}")
        img = Image.open(path)

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    return img


def load_photoimage(url_or_path: str, max_size: tuple[int, int] = (520, 360)) -> ImageTk.PhotoImage:
    """
    Carrega imagem a partir de URL http(s) ou caminho local.
    Redimensiona mantendo proporção para caber em max_size.
    """
    img = open_pil_image(url_or_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)
