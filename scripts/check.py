#!/usr/bin/env python3
"""Validate the project manifest and local HTML links using only the standard library."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(source)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(str(values['id']))
        for key in ('href', 'src'):
            if values.get(key):
                self.links.append(str(values[key]))


def main() -> int:
    errors: list[str] = []
    try:
        sites = json.loads((ROOT / 'sites.json').read_text(encoding='utf-8'))['sites']
        if not isinstance(sites, list) or not sites:
            raise ValueError('sites must be a nonempty list')
    except (OSError, ValueError, KeyError) as exc:
        print(f'Manifest error: {exc}')
        return 1
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for site in sites:
        required = ('id', 'title', 'description', 'category', 'path', 'date', 'tags')
        if not isinstance(site, dict) or any(key not in site for key in required):
            errors.append('Manifest entry is missing required fields')
            continue
        path = site['path']
        if not isinstance(path, str) or not re.fullmatch(r'[a-z0-9][a-z0-9/-]*/', path) or '//' in path:
            errors.append(f'Unsafe project path: {path!r}')
            continue
        if site['id'] in seen_ids or path in seen_paths:
            errors.append(f'Duplicate project: {path}')
        seen_ids.add(site['id'])
        seen_paths.add(path)
        if not (ROOT / path / 'index.html').is_file():
            errors.append(f'Missing project index: {path}')
    pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
    for path, page in pages.items():
        for href in page.links:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            if parts.path.startswith('/'):
                errors.append(f'{path.relative_to(ROOT)}: use a relative URL instead of {href}')
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing local resource {href}')
                continue
            if parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {href}')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: {len(sites)} projects, {len(pages)} HTML pages, all local links valid.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
