#!/usr/bin/env python3
"""Check a declared research source map against an HTML file; no network or API calls.
This checks structure only. It cannot certify source truth or semantic coverage.
"""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.text = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        ident = dict(attrs).get('id')
        if ident:
            self.ids.add(ident)
    def handle_data(self, data):
        self.text.append(data)

def check(ledger, html):
    errors, gaps = [], []
    doc = Document(html)
    visible = ' '.join(doc.text)
    sources = ledger.get('sources', [])
    by_id = {s.get('id'): s for s in sources}
    if len(by_id) != len(sources):
        errors.append('Duplicate source IDs')
    primary = by_id.get(ledger.get('primary_source_id'))
    if not primary or primary.get('role') != 'primary':
        errors.append('Missing primary source')
    elif primary.get('url') != ledger.get('user_url'):
        errors.append('Primary URL differs from user URL; confirm identity before analysis')
    for source in sources:
        if source.get('role') in {'quoted_article', 'attachment'}:
            if source.get('parent') not in by_id:
                errors.append(f"Unresolved source parent: {source.get('id')}")
        if source.get('read_status') in {'partial', 'unread'}:
            gaps.append(f"{source.get('id')}: {source.get('read_status')}")
            notice = source.get('visible_gap_text', '')
            if not notice or notice not in visible:
                errors.append(f"Missing visible gap notice: {source.get('id')}")
    entries = ledger.get('coverage', [])
    ids = [entry.get('id') for entry in entries]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate coverage IDs')
    expected = set(ledger.get('expected_original_ids', []))
    if not expected:
        errors.append('Original-item inventory is missing')
    present = {e.get('id') for e in entries if e.get('kind') != 'supplementary'}
    for ident in sorted(expected - present):
        errors.append(f'Missing original item: {ident}')
    for entry in entries:
        ident = entry.get('id')
        source = by_id.get(entry.get('source'))
        if not source:
            errors.append(f'Unknown source for {ident}')
        elif source.get('read_status') == 'unread' and entry.get('status') == 'covered':
            errors.append(f'Unread source cannot support covered item: {ident}')
        if not entry.get('locator'):
            errors.append(f'Missing source location: {ident}')
        if entry.get('status') not in {'covered', 'partial', 'missing'}:
            errors.append(f'Invalid coverage state: {ident}')
        if entry.get('status') != 'covered':
            gaps.append(f'{ident}: {entry.get("status")}')
        if entry.get('anchor', '').lstrip('#') not in doc.ids:
            errors.append(f'Missing HTML anchor: {ident}')
    if gaps and ledger.get('claims_complete') is True:
        errors.append('Completeness claim conflicts with declared gaps')
    return errors, gaps

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    parser.add_argument('html', type=Path)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding='utf-8'))
        errors, gaps = check(data, args.html.read_text(encoding='utf-8'))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f'INPUT_ERROR: {exc}')
        return 2
    for message in errors:
        print('ERROR:', message)
    for message in gaps:
        print('GAP:', message)
    if errors or (args.require_complete and gaps):
        return 1
    print('STRUCTURE_OK_WITH_GAPS' if gaps else 'STRUCTURE_OK')
    print('Human source-identity and semantic-coverage review is still required.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
