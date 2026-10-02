"""T-Book TTS — 한국어 낭독 정규화(숫자·기호를 읽는 글로). 지시서 「T-Book TTS 정비 ver.1」 §3.

ko_normalize.ps1 과 같은 규칙·같은 결과(시험 사례 공유). 표준 라이브러리만 쓴다.
⚠ 법적 고지 문안(channel notice)은 의미를 바꾸지 않는다 — 띄어쓰기·쉼표·숫자 읽기만.
"""
import re

NORMALIZER_VERSION = 'ko-norm-1.0.0'

SINO_D = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
DIGIT_GONG = ['공', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
DIGIT_YEONG = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
NATIVE_1 = ['', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉']
NATIVE_10 = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
ABBR = {'CCTV': '씨씨티비', 'KICS': '킥스', 'BRT': '비알티', 'GPS': '지피에스', 'IC': '아이씨', 'JC': '제이씨',
        'PM': '피엠', 'TAAS': '타스', 'KTX': '케이티엑스', 'SRT': '에스알티'}
NATIVE_UNITS = ['명', '대', '시', '번', '개', '마리', '살', '사람', '장', '잔', '군데', '곳', '시간', '달', '벌', '켤레', '가지']
CIRC = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'


def sino4(n):
    s = ''
    for unit, name in ((1000, '천'), (100, '백'), (10, '십'), (1, '')):
        d, n = divmod(n, unit)
        if d == 0:
            continue
        s += name if (d == 1 and unit > 1) else SINO_D[d] + name
    return s


def sino(n):
    n = int(n)
    if n == 0:
        return '영'
    out = ''
    for unit, name in ((10 ** 12, '조'), (10 ** 8, '억'), (10 ** 4, '만'), (1, '')):
        q, n = divmod(n, unit)
        if q == 0:
            continue
        part = sino4(q)
        if name == '만' and part == '일':  # 일만 → 만
            part = ''
        out += part + name
    return out


def native(n):
    n = int(n)
    if n < 1 or n > 99:
        return sino(n)
    t, o = divmod(n, 10)
    if t == 2 and o == 0:
        return '스무'
    return NATIVE_10[t] + NATIVE_1[o]


def digits(d, zero='공'):
    tbl = DIGIT_GONG if zero == '공' else DIGIT_YEONG
    return ''.join(tbl[int(c)] for c in d)


def month(m):
    return {6: '유월', 10: '시월'}.get(m, sino(m) + '월')


def hour(h, mi, ampm):
    pre = ''
    if ampm:
        pre = '오전 ' if h < 12 else '오후 '
    hh = h - 12 if (ampm and h > 12) else h
    hs = '영 시' if hh == 0 else native(hh) + ' 시'
    ms = ' ' + sino(mi) + ' 분' if mi > 0 else ''
    return pre + hs + ms


def select_josa(word, pair):
    """받침으로 조사 고르기 — (으)로·(이)가·(을)를·(은)는·(과)와·(이)라"""
    c = ord(word.rstrip()[-1])
    has = rieul = False
    if 0xAC00 <= c <= 0xD7A3:
        jong = (c - 0xAC00) % 28
        has, rieul = jong != 0, jong == 8
    return {
        '(으)로': '으로' if (has and not rieul) else '로',
        '(이)가': '이' if has else '가',
        '(을)를': '을' if has else '를',
        '(은)는': '은' if has else '는',
        '(과)와': '과' if has else '와',
        '(이)라': '이라' if has else '라',
    }.get(pair, pair)


def resolve_josa(t):
    return re.sub(r'([가-힣A-Za-z0-9]+)\s?(\(으\)로|\(이\)가|\(을\)를|\(은\)는|\(과\)와|\(이\)라)',
                  lambda m: m.group(1) + select_josa(m.group(1), m.group(2)), t)


def _law(m):
    s = '제' + sino(m.group(1)) + '조'
    if m.group(2):
        s += '의' + sino(m.group(2))
    if m.group(3):
        s += ' 제' + sino(CIRC.index(m.group(3)) + 1) + '항'
    if m.group(4):
        s += ' 제' + sino(m.group(4)) + '호'
    return s


def _won(m):
    n = int(m.group(1).replace(',', ''))
    if m.group(2) == '만':
        n *= 10000
    elif m.group(2) == '억':
        n *= 10 ** 8
    return sino(n) + ' 원'


def _native_unit(m):
    n = int(m.group(1))
    lim = 12 if m.group(2) == '시' else 99   # 13시 이상은 「십삼 시」
    return (native(n) if 1 <= n <= lim else sino(n)) + ' ' + m.group(2)


def normalize(t, warn=None):
    """낭독형으로 바꾼다. warn 에 list 를 주면 사전에 없는 약어를 담는다."""
    if t is None:
        return ''
    t = re.sub(r'§\s?(\d+)(?:의(\d+))?([①-⑳])?(\d+)?', _law, t)
    t = re.sub(r'제\s?(\d+)\s?(조|항|호|장|절)(의\s?(\d+))?',
               lambda m: '제' + sino(m.group(1)) + m.group(2) + ('의' + sino(m.group(4)) if m.group(3) else '') + ' ', t)
    t = re.sub(r'(\d+)\.(\d+)\s?%', lambda m: sino(m.group(1)) + ' 점 ' + digits(m.group(2), '영') + ' 퍼센트', t)
    t = re.sub(r'(\d+)\s?%', lambda m: sino(m.group(1)) + ' 퍼센트', t)
    t = re.sub(r'(\d+)\s?(km/h|㎞/h|킬로미터 매 시)', lambda m: '시속 ' + sino(m.group(1)) + ' 킬로미터', t)
    t = re.sub(r'(?<!\d)(0\d{1,2})[-.\s](\d{3,4})[-.\s](\d{4})(?!\d)',
               lambda m: digits(m.group(1)) + ', ' + digits(m.group(2)) + ', ' + digits(m.group(3)), t)
    t = re.sub(r'(?<!\d)(112|119|182|1393|1366|1388|1577-?\d{4})(?!\d)', lambda m: digits(m.group(1).replace('-', '')), t)
    t = re.sub(r'(?<!\d)(\d{2,3})\s?([가-힣])\s?(\d{4})(?!\d)',
               lambda m: digits(m.group(1)) + ' ' + m.group(2) + ' ' + digits(m.group(3)), t)
    t = re.sub(r'(?<!\d)([01]?\d|2[0-3]):([0-5]\d)(?!\d)', lambda m: hour(int(m.group(1)), int(m.group(2)), True), t)
    t = re.sub(r'(?<!\d)(1[0-2]|[1-9])\s?월', lambda m: month(int(m.group(1))), t)
    t = re.sub(r'(\d{1,3}(?:,\d{3})+|\d+)\s?(만|억)?\s?원', _won, t)
    t = re.sub(r'([가-힣]+(?:대로|로))\s?(\d+)\s?(가)?길',
               lambda m: m.group(1) + ' ' + sino(m.group(2)) + ' ' + ('가 ' if m.group(3) else '') + '길', t)
    t = re.sub(r'(\d+)\s?번\s?(출구|버스|국도|게이트|홈)', lambda m: sino(m.group(1)) + ' 번 ' + m.group(2), t)
    t = re.sub(r'(\d+)\s?(차로|호선|층|회|점|분|초|년|일|호|조|항|킬로미터|미터|센티미터|퍼센트|원)',
               lambda m: sino(m.group(1)) + ' ' + m.group(2), t)
    nu = '|'.join(sorted(NATIVE_UNITS, key=len, reverse=True))
    t = re.sub(r'(?<![\d.])(\d+)\s?(' + nu + ')', _native_unit, t)
    for k, v in ABBR.items():
        t = re.sub(r'(?<![A-Za-z])' + k + r'(?![A-Za-z])', v, t)
    if warn is not None:
        for m in re.finditer(r'(?<![A-Za-z])[A-Z]{2,}(?![A-Za-z])', t):
            if m.group(0) not in warn:
                warn.append(m.group(0))
    t = re.sub(r'\d{1,3}(?:,\d{3})+|\d+', lambda m: sino(m.group(0).replace(',', '')), t)
    t = resolve_josa(t)
    return re.sub(r'[ \t]{2,}', ' ', t).strip()


def long_breaths(t, limit=25):
    """한 호흡(쉼표·마침표 사이)이 limit 자를 넘는 마디 — 렌더 전 점검용(고치지는 않는다)"""
    return [p.strip() for p in re.split(r'[,.?!·]', t) if len(re.sub(r'\s', '', p)) > limit]
