#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extract.py — <script> 블록 추출 + 블록별 SHA-256 (계산 로직 무접촉 증명용)"""
import re, sys, hashlib, os, io
src = sys.argv[1]; outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)
s = io.open(src, encoding='utf-8').read()
n = 0; rows = []
for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script\s*>', s, re.S | re.I):
    body = m.group(1)
    h = hashlib.sha256(body.encode('utf-8')).hexdigest()[:16]
    io.open('%s/b%02d.js' % (outdir, n), 'w', encoding='utf-8').write(body)
    rows.append('%02d %s %d' % (n, h, len(body))); n += 1
io.open('%s/HASHES.txt' % outdir, 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
print('blocks=%d' % n)
