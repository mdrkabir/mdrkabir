#!/usr/bin/env python3
"""Store five original PNGs (four brands) locally and update README paths.

Run once with Python 3.9+ from any directory. No third-party packages needed.
Only the public URLs in logo-sources.json are fetched. Nothing is uploaded.
All downloads must validate before any README is changed. Existing valid PNGs
are reused; pass --refresh to retrieve fresh copies. The GitHub workflow runs
this same script automatically after a push to the repository's default branch.
"""
from __future__ import annotations
import argparse
import binascii
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib

ROOT = Path(__file__).resolve().parents[1]
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
MAX_BYTES = 8 * 1024 * 1024


def validate_png(data: bytes) -> tuple[int, int]:
    """Check PNG structure, dimensions, CRCs and the compressed image stream."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError('The response is not a PNG image (possibly an error page).')
    offset = 8
    width = height = 0
    image_data = bytearray()
    seen_end = False
    while offset + 12 <= len(data):
        length = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + length + 12
        if end > len(data):
            raise ValueError('Truncated PNG chunk.')
        payload = data[offset + 8:offset + 8 + length]
        expected = struct.unpack('>I', data[offset + 8 + length:end])[0]
        if binascii.crc32(kind + payload) & 0xffffffff != expected:
            raise ValueError('PNG checksum mismatch.')
        if kind == b'IHDR':
            if offset != 8 or length != 13:
                raise ValueError('Invalid PNG header.')
            width, height = struct.unpack('>II', payload[:8])
            if not (1 <= width <= 8192 and 1 <= height <= 8192):
                raise ValueError('Unreasonable PNG dimensions.')
        elif kind == b'IDAT':
            image_data.extend(payload)
        elif kind == b'IEND':
            seen_end = True
            break
        offset = end
    if not seen_end or not image_data or not width or not height:
        raise ValueError('Incomplete PNG image.')
    decoder = zlib.decompressobj()
    decoder.decompress(image_data, 128 * 1024 * 1024)
    if not decoder.eof:
        raise ValueError('Invalid or oversized compressed PNG data.')
    return width, height


def download_png(url: str) -> bytes:
    if urllib.parse.urlparse(url).hostname != 'raw.githubusercontent.com':
        raise ValueError(f'Unexpected source host: {url}')
    request = urllib.request.Request(url, headers={'User-Agent': 'mdrkabir-profile-logo-setup/1.0'})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if urllib.parse.urlparse(response.url).hostname != 'raw.githubusercontent.com':
                    raise ValueError('Unexpected redirect host.')
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError('Logo download exceeds the size limit.')
            validate_png(data)
            return data
        except (OSError, urllib.error.URLError, ValueError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(attempt + 1)
    raise RuntimeError(f'Cannot download {url}: {last_error}')


def setup(root: Path = ROOT, refresh: bool = False) -> int:
    entries = json.loads((root / 'tools/logo-sources.json').read_text(encoding='utf-8'))
    prepared: list[tuple[dict, bytes, tuple[int, int]]] = []
    # Stage and validate ALL images first; no partial README rewrite on failure.
    for item in entries:
        rel = Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts or rel.parts[0] != 'assets':
            raise ValueError(f'Unsafe asset path: {rel}')
        dest = root / rel
        data = None
        if dest.exists() and not refresh:
            try:
                data = dest.read_bytes()
                validate_png(data)
                print(f'Keep  {rel}')
            except (OSError, ValueError, zlib.error):
                data = None
        if data is None:
            print(f'Fetch {rel}', flush=True)
            data = download_png(item['url'])
        dims = validate_png(data)
        prepared.append((item, data, dims))

    (root / 'assets').mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.logo-stage-', dir=root) as stage_name:
        stage = Path(stage_name)
        for item, data, _ in prepared:
            (stage / Path(item['path']).name).write_bytes(data)
        for item, data, _ in prepared:
            dest = root / item['path']
            if not dest.exists() or dest.read_bytes() != data:
                (stage / dest.name).replace(dest)

    for name in ('README.md', 'README-static.md'):
        path = root / name
        if not path.exists():
            continue
        old = path.read_text(encoding='utf-8')
        updated = old
        for item, _, _ in prepared:
            updated = updated.replace(item['url'], item['path'])
        if updated != old:
            path.write_text(updated, encoding='utf-8')
            print(f'Localize image references in {name}')

    manifest = [{**item, 'sha256': hashlib.sha256(data).hexdigest(),
                 'bytes': len(data), 'width': dims[0], 'height': dims[1]}
                for item, data, dims in prepared]
    (root / 'assets/official-logo-manifest.json').write_text(
        json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Done. The five PNG files are local. No prior ZIP or repair page is needed.')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Download again instead of reusing local originals.')
    args = parser.parse_args()
    try:
        return setup(refresh=args.refresh)
    except (OSError, ValueError, RuntimeError, zlib.error) as error:
        print(f'ERROR: {error}\nREADME image references were not changed. Check your internet connection and retry.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
