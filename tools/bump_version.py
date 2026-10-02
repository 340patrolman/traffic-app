# -*- coding: utf-8 -*-
"""T-Book 판 번호 표기 7곳을 상수 하나로 맞춘다 + 계약서 머리 「현재 규모」 줄을 실측으로 갱신한다. (2026-09-02)
   사용: python3 bump_version.py <index.html> <새 판 번호 예: v21.80> [날짜 2026.10.2 또는 2026-10-02]
   ※ 2026-10-02 고침: 앱의 날짜 표기는 「2026.10.2」(점·앞 0 없음)인데 도구가 숫자·줄표만 찾아 날짜 두 곳(계약서 머리·현재 규모)에서 멈췄다.
      이제 점·줄표 둘 다 찾고, 쓸 때는 앱 표기(점)로 쓴다.
   7곳: 계약서 머리 · title · APP_VERSION · DEPLOY_TAG · footer · 팝업 · 상단 막대 span.ver
   ※ 발자취(판올림 내역) 항목은 자동으로 만들지 않는다 — 그건 사람이 쓰는 글이다.
   ※ 규모 줄 기준: 만자 = 파이썬 len() (코드포인트) · 줄 = 개행 수 (wc -l) · script/style = 여는 태그 수 · !important 문자열 수"""
import io, re, sys, hashlib, datetime
f = sys.argv[1]; new = sys.argv[2]
_d = datetime.date.fromisoformat(sys.argv[3].replace('.', '-')) if len(sys.argv) > 3 and sys.argv[3].count('-') == 2 else None
if len(sys.argv) > 3 and _d is None:   # 2026.10.2 꼴
    _y, _m, _dd = (int(x) for x in sys.argv[3].split('.')); _d = datetime.date(_y, _m, _dd)
_d = _d or datetime.date.today()
day = '%d.%d.%d' % (_d.year, _d.month, _d.day)   # 앱 표기 — 2026.10.2
s = io.open(f, encoding='utf-8', newline='').read()
print('IN ', len(s.encode('utf-8')), hashlib.sha256(s.encode('utf-8')).hexdigest()[:16])
pats = [
 (r'(코드 계약서\s+ver\.2\s+\()v[\d.]+( · )[\d.\-]+\)', lambda m: m.group(1) + new + m.group(2) + day + ')'),
 (r'(<title>T-Book )v[\d.]+', lambda m: m.group(1) + new),
 (r"(const APP_VERSION=')v[\d.]+(')", lambda m: m.group(1) + new + m.group(2)),
 (r'(DEPLOY_TAG = "T-Book )v[\d.]+', lambda m: m.group(1) + new),
 (r'(🚔 T-Book )v[\d.]+( \(2026 전국 공용판\) · 2026)', lambda m: m.group(1) + new + m.group(2)),
 (r'(🚓 T-Book )v[\d.]+(</div>)', lambda m: m.group(1) + new + m.group(2)),
 (r'(<span class="ver">)v[\d.]+(</span>)', lambda m: m.group(1) + new + m.group(2)),
]
for p, fn in pats:
    s, n = re.subn(p, fn, s, count=1)
    assert n == 1, ('앵커 못 찾음', p)
# 규모 줄
scripts = len(re.findall(r'<script\b', s)); styles = len(re.findall(r'<style\b', s)); imp = s.count('!important'); lines = s.count('\n'); man = '%.1f' % (len(s) / 10000)
s, n = re.subn(r'\d+\.\d만자 / [\d,]+줄 · script \d+개 · style \d+개', '%s만자 / %s줄 · script %d개 · style %d개' % (man, format(lines, ','), scripts, styles), s, count=1); assert n == 1
s, n = re.subn(r'· !important \d+개', '· !important %d개' % imp, s, count=1); assert n == 1
s, n = re.subn(r'현재 규모 \([\d.\-]+ 실측\)', '현재 규모 (%s 실측)' % day, s, count=1); assert n == 1
s, n = re.subn(r'\(v[\d.]+ 에서 코드로 직접 센 값이다\.', '(%s 에서 코드로 직접 센 값이다.' % new, s, count=1); assert n == 1
io.open(f, 'w', encoding='utf-8', newline='').write(s)
print('OUT', len(s.encode('utf-8')), hashlib.sha256(s.encode('utf-8')).hexdigest()[:16], '| 7곳 →', new, '| 규모', man + '만자', lines, 'script', scripts, 'style', styles, '!important', imp)
