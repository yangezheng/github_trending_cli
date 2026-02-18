import json

from .models import Repo
from dataclasses import asdict


def render_text(repos: list[Repo]) -> str:
    lines: list[str] = []
    for i, r in enumerate(repos, 1):
        lang = r.language or "-"
        lines.append(f"{i:>2}. {r.full_name:<35} ⭐ {r.stars:<7} {lang}")
        if r.url:
            lines.append(f" {r.url}")
        lines.append("")  # blank line between entries
    return "\n".join(lines).rstrip()  # avoid trailing newline spam


def render_json(repos: list[Repo]) -> str:
    payload = [asdict(r) for r in repos]
    return json.dumps(payload, ensure_ascii=False, indent=2)
