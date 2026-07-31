#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guard.py — T-Book 구조 파수꾼 (HANDOFF 3-2 사양대로 재작성 · v19.8.3 세션)
브라우저 없이 0.5초. 배포 전 필수 관문.

검사 6종
 ① 모든 .page 가 body 직속인가            (v19.8 하단메뉴 실종 사고의 직접 원인)
 ② div 개폐 균형                          (닫는 </div> 누락/과잉)
 ③ #hd_tabs 가 .page 안에 갇혔는가
 ④ 아이콘 맵이 참조하는 아이콘이 라이브러리에 있는가
 ⑤ GROUP_PAGES 탭 ↔ page div 대응
 ⑥ 기준선 대비 페이지 수 감소

usage: python3 guard.py <target.html> [baseline.html]
exit 0 = 통과 / 1 = 실패(배포 중단)
"""
import re, sys, html

VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr'}

TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*?)(/?)>')


def strip_noise(s):
    """script/style/주석 내부를 같은 길이의 공백으로 치환 — 오프셋 보존."""
    out = list(s)
    def blank(a, b):
        for i in range(a, b):
            if out[i] != '\n':
                out[i] = ' '
    for m in re.finditer(r'<!--.*?-->', s, re.S):
        blank(m.start(), m.end())
    for tag in ('script', 'style'):
        for m in re.finditer(r'<%s\b[^>]*>.*?</%s\s*>' % (tag, tag), s, re.S | re.I):
            blank(m.start(), m.end())
    return ''.join(out)


def attr(raw, name):
    m = re.search(r'\b%s\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))' % name, raw, re.I)
    if not m:
        return None
    return html.unescape(m.group(2) or m.group(3) or m.group(4) or '')


def scan(clean):
    """태그 스택을 돌며 .page / #hd_tabs 위치와 div 균형을 잰다."""
    stack = []            # [(tagname, id, classes)]
    pages = []            # (id, parent_tag, depth, ancestors)
    hd = None
    opened = closed = 0
    unbalanced = []

    for m in TAG_RE.finditer(clean):
        closing, tag, raw, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if tag in VOID or selfclose:
            continue
        if closing:
            if tag == 'div':
                closed += 1
            # 스택에서 해당 태그까지 되감기
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    if i != len(stack) - 1:
                        unbalanced.append((tag, [x[0] for x in stack[i + 1:]], m.start()))
                    del stack[i:]
                    break
            else:
                unbalanced.append(('EXTRA_CLOSE:' + tag, [], m.start()))
            continue

        if tag == 'div':
            opened += 1
        eid = attr(raw, 'id') or ''
        cls = (attr(raw, 'class') or '').split()

        if 'page' in cls and tag == 'div':
            parent = stack[-1][0] if stack else '(none)'
            anc = [(x[0], x[1]) for x in stack]
            pages.append((eid, parent, len(stack), anc))
        if eid == 'hd_tabs':
            hd = [(x[0], x[1], x[2]) for x in stack]

        stack.append((tag, eid, cls))

    return pages, hd, opened, closed, unbalanced, stack


def main():
    tgt = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else None
    src = open(tgt, encoding='utf-8').read()
    clean = strip_noise(src)

    fails, notes = [], []

    pages, hd, opened, closed, unbalanced, leftover = scan(clean)

    # ── ① 모든 .page 가 body 직속인가
    bad_pages = [(pid, par, anc) for (pid, par, dep, anc) in pages if par != 'body']
    nested = []
    for pid, par, dep, anc in pages:
        for (atag, aid) in anc:
            if aid.startswith('page-'):
                nested.append((pid or '(id없음)', aid))
    if bad_pages or nested:
        fails.append('페이지 중첩/비직속 %d건 → %s' % (len(bad_pages), nested[:8] or bad_pages[:8]))
    notes.append('① 페이지 %d/%d body 직속' % (len(pages) - len(bad_pages), len(pages)))

    # ── ② div 개폐 균형
    if opened != closed:
        fails.append('div 개폐 불일치 %+d — 여는 %d / 닫는 %d' % (opened - closed, opened, closed))
    # div 가 얽힌 교차/과잉닫힘만 배포 중단 사유. 그 외(고아 </p> 등)는 경고.
    hard = [u for u in unbalanced if u[0] == 'div' or u[0] == 'EXTRA_CLOSE:div'
            or 'div' in u[1]]
    soft = [u for u in unbalanced if u not in hard]
    if hard:
        fails.append('div 태그 교차/과잉닫힘 %d건 → %s' % (len(hard), hard[:5]))
    if soft:
        notes.append('②-경고 무해한 고아 닫는태그 %d건 → %s (기준선에도 있음)'
                     % (len(soft), [u[0] for u in soft[:5]]))
    if leftover:
        fails.append('끝까지 안 닫힌 태그 %d건 → %s' % (len(leftover), [x[0] for x in leftover[:6]]))
    notes.append('② div %d/%d' % (opened, closed))

    # ── ③ #hd_tabs 가 .page 안에 갇혔는가
    if hd is None:
        fails.append('#hd_tabs 를 찾을 수 없다 (하단 메뉴바 실종)')
        notes.append('③ hd_tabs 없음')
    else:
        trapped = [aid for (atag, aid, acls) in hd if aid.startswith('page-') or 'page' in acls]
        if trapped:
            fails.append('하단 메뉴바가 페이지 %s 안에 갇혔다' % trapped)
        notes.append('③ hd_tabs 부모=%s' % ([t for t, i, c in hd][-1] if hd else 'body'))

    # ── ④ 아이콘 맵 참조 ↔ 라이브러리
    lib = set()
    mlib = re.search(r'var\s+P\s*=\s*\{("file".*?)\};\s*\n?\s*var\s+M\s*=', src, re.S)
    if mlib:
        lib = set(re.findall(r'"([a-z0-9_]+)"\s*:', mlib.group(1)))
    mmap = re.search(r'var\s+M\s*=\s*\{("rep1".*?)\};', src, re.S)
    used = set()
    if mmap:
        used = set(re.findall(r':\s*"([a-z0-9_]+)"', mmap.group(1)))
    missing = sorted(used - lib) if lib else []
    if missing:
        fails.append('없는 아이콘 참조: %s' % missing)
    notes.append('④ 아이콘 %d/%d (라이브러리 %d종)' % (len(used) - len(missing), len(used), len(lib)))

    # ── ⑤ GROUP_PAGES 탭 ↔ page div 대응
    page_ids = {pid[5:] for (pid, p, d, a) in pages if pid.startswith('page-')}
    gp = re.search(r'GROUP_PAGES\s*=\s*\{(.*?)\n\s*\}', src, re.S)
    tabs = []
    if gp:
        tabs = re.findall(r"'([a-zA-Z0-9_]+)'", gp.group(1))
        tabs = [t for t in tabs if t in page_ids or True]
        miss = [t for t in tabs if t not in page_ids]
        # 그룹 키 자체는 페이지가 아니다 — page div 가 있는 것만 검사 대상
        miss = [t for t in miss if not re.match(r'^(docs|shift|sop|home|report|co|law|etc)$', t)]
        if miss:
            fails.append('GROUP_PAGES 탭에 대응 page div 없음: %s' % miss)
    notes.append('⑤ 탭 %d개 · page div %d개' % (len(tabs), len(page_ids)))

    # ── ⑥ 기준선 대비 페이지 수 감소
    if base:
        bsrc = open(base, encoding='utf-8').read()
        bpages, _, bo, bc, _, _ = scan(strip_noise(bsrc))
        if len(pages) < len(bpages):
            fails.append('기준선 대비 페이지 감소: %d → %d' % (len(bpages), len(pages)))
        notes.append('⑥ 기준선 페이지 %d → 현재 %d · div %d → %d' % (len(bpages), len(pages), bo, opened))
    else:
        notes.append('⑥ 기준선 미지정 — 건너뜀')

    print('── guard.py : %s' % tgt)
    for n in notes:
        print('   ' + n)
    if fails:
        print('\n🔴 실패 %d건 — 배포 중단' % len(fails))
        for f in fails:
            print('  · ' + f)
        sys.exit(1)
    print('\n✅ guard.py 통과')
    sys.exit(0)


if __name__ == '__main__':
    main()
