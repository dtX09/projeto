"""Helpers para resolver caminhos de recursos em dev e em executavel."""

from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def runtime_base_dir() -> Path:
    """Diretorio base dos recursos no runtime atual."""
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
        return Path(sys.executable).resolve().parent
    return project_root()


def resolve_resource_path(path_str: str) -> Path:
    """
    Resolve um caminho de recurso para funcionar em:
    - execucao normal (source)
    - executavel empacotado (ex.: PyInstaller)
    """
    path = Path(path_str)
    if path.is_absolute():
        return path

    candidates: list[Path] = [runtime_base_dir() / path]

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        candidates.append(exe_dir / path)

    candidates.append(project_root() / path)

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    return candidates[0]
