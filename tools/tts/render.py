"""T-Book TTS 렌더 — lines.json → Fish Audio(S2-Pro) → masters/ wav(테이크 3) → assets/voice/{id}.ogg·.m4a + manifest.json·manifest.js

지시서 「T-Book TTS 정비 ver.1」 §4·§5. render.ps1 과 같은 동작·같은 해시(어느 쪽으로 만들어도 다시 돌리면 건너뛴다).
표준 라이브러리만 쓴다(설치할 것은 ffmpeg 하나).

  python render.py --dry-run                                  무엇을 만들지·건너뛸지만(키·ffmpeg 불필요)
  python render.py --only blood_notice_1 blood_notice_2 blood_withdraw     시험 3줄
  python render.py --lock blood_notice_1=2                    리뷰에서 고른 테이크로 고정 → 그 테이크로 다시 인코딩
  --force  해시가 같아도 다시 만든다(고정된 것은 그래도 다시 요청하지 않음)

키: 환경변수 FISH_API_KEY → 없으면 지식베이스의 07_API키/keys.json 의 "fish_audio" 를 찾는다(공개 폴더 밖).
    키는 화면·파일·로그 어디에도 쓰지 않는다. 이 tools/ 폴더는 GitHub Pages 로 공개되므로 .env·키 파일을 두지 않는다.
"""
import argparse
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ko_normalize import NORMALIZER_VERSION, long_breaths, normalize  # noqa: E402

POSTPROC_VERSION = 'pp-1 lead50 tail150 loudnorm-16'
MODEL, FORMAT, LATENCY, NORMALIZE = 's2-pro', 'wav', 'normal', False
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))   # 배포용 폴더(= 저장소 루트와 같은 모양)
MAST = os.path.join(HERE, 'masters')
OUT = os.path.join(ROOT, 'assets', 'voice')
LINES = os.path.join(HERE, 'lines.json')
AF = ('silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,'
      'silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.15,areverse,loudnorm=I=-16:TP=-1.5:LRA=11')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def strip_punct(t):
    return re.sub(r'[\s,.·?!]', '', t)


def load(p, default=None):
    if not os.path.exists(p):
        return default
    with open(p, encoding='utf-8-sig') as f:
        return json.load(f)


def find_key():
    k = os.environ.get('FISH_API_KEY', '').strip()
    if k:
        return k
    d = HERE
    for _ in range(6):
        p = os.path.join(d, '07_API키', 'keys.json')
        if os.path.exists(p):
            v = (load(p, {}) or {}).get('fish_audio', '')
            return v.strip() if isinstance(v, str) else ''
        d = os.path.dirname(d)
    return ''


def expand(L):
    """슬롯 조합마다 문장 단위(클립 이어 붙이기 금지). 200 넘으면 멈춤"""
    slots = L.get('slots') or {}
    keys = list(slots.keys())
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*[slots[k] for k in keys])] if keys else [{}]
    if len(combos) > 200:
        sys.exit(f"{L['id']}: 슬롯 조합 {len(combos)}개 — 200 을 넘어 멈춥니다(지시서 §2)")
    for c in combos:
        raw = L['text_raw']
        sp = L.get('text_spoken') or raw
        vid = L['id']
        for k, v in c.items():
            raw = raw.replace('{' + k + '}', str(v))
            sp = sp.replace('{' + k + '}', str(v))
            vid += '__' + k + '-' + sha(str(v))[:6]
        yield vid, raw, sp


def lock(spec):
    m = re.fullmatch(r'([\w-]+)=(\d)', spec or '')
    if not m:
        sys.exit('--lock 은 「아이디=테이크번호」 꼴입니다 (예: blood_notice_1=2)')
    lid, lt = m.group(1), m.group(2)
    with open(LINES, encoding='utf-8-sig') as f:
        txt = f.read()
    rx = re.compile(r'("id":\s*"' + re.escape(lid) + r'"[\s\S]*?"locked":\s*)(null|\d+)')
    if not rx.search(txt):
        sys.exit(f'lines.json 에 {lid} 가 없습니다')
    with open(LINES, 'w', encoding='utf-8', newline='\n') as f:
        f.write(rx.sub(lambda mm: mm.group(1) + lt, txt, count=1))   # 파일 모양을 흐트러뜨리지 않는다
    print(f'고정: {lid} → 테이크 {lt}')
    return lid


def post_tts(final, ref, dst, key):
    body = json.dumps({'text': final, 'reference_id': ref, 'format': FORMAT, 'normalize': NORMALIZE, 'latency': LATENCY},
                      ensure_ascii=False).encode('utf-8')
    for t in range(4):
        req = urllib.request.Request('https://api.fish.audio/v1/tts', data=body, method='POST', headers={
            'Authorization': 'Bearer ' + key, 'model': MODEL, 'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=180) as r, open(dst, 'wb') as f:
                shutil.copyfileobj(r, f)
            return
        except urllib.error.HTTPError as e:
            if (e.code == 429 or e.code >= 500) and t < 3:
                s = 2 ** (t + 1)
                print(f'    {e.code} — {s}초 뒤 다시({t + 1}/3)')
                time.sleep(s)
                continue
            sys.exit(f'Fish 요청 실패(HTTP {e.code}) — {os.path.basename(dst)}')   # 키는 메시지에 넣지 않는다
        except urllib.error.URLError as e:
            sys.exit(f'Fish 에 닿지 못함({e.reason}) — 이 환경이 api.fish.audio 로 나가는지 확인하십시오')


def ff(*args):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args])
    if r.returncode:
        sys.exit('ffmpeg 실패: ' + ' '.join(args[:2]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--lock')
    a = ap.parse_args()
    if a.lock:
        a.only, a.force = [lock(a.lock)], True
    lines = load(LINES)
    voices = load(os.path.join(HERE, 'voices.json'), {})
    man_path = os.path.join(OUT, 'manifest.json')
    man = (load(man_path, {}) or {}).get('clips', {}) or {}
    todo = [L for L in lines if not a.only or L['id'] in a.only]
    if not todo:
        sys.exit('할 대사가 없습니다(--only 이름 확인)')
    plan, chars = [], 0
    for L in todo:
        ref = (voices.get(L['speaker']) or {}).get('reference_id', '')
        for vid, raw, sp in expand(L):
            w = []
            norm = normalize(sp, w)
            # §1-4 — 법적 고지는 원문과 한 글자도 달라지면 안 된다: 빈칸·쉼표·마침표·가운뎃점을 빼고 같아야 한다
            if L.get('channel') == 'notice' and strip_punct(norm) != strip_punct(raw):
                sys.exit(f'{vid}: 낭독문이 원문과 다릅니다 — 원문 「{raw}」 / 낭독 「{norm}」')
            final = '[' + L['emotion'] + '] ' + norm
            key = '\n'.join([f'text_final={final}', f"speaker={L['speaker']}", f'reference_id={ref}', f'model={MODEL}',
                             f'format={FORMAT}', f'latency={LATENCY}', f'normalize={NORMALIZE}', f"takes={L['takes']}",
                             f'normalizer={NORMALIZER_VERSION}', f'postproc={POSTPROC_VERSION}'])   # render.ps1 과 같은 글 → 같은 해시
            h = sha(key)
            files_ok = all(os.path.exists(os.path.join(OUT, f'{vid}.{x}')) for x in ('ogg', 'm4a'))
            skip, why = False, ''
            if L.get('locked') and files_ok and not a.lock:
                skip, why = True, f"고정됨(테이크 {L['locked']})"
            elif not a.force and (man.get(vid) or {}).get('hash') == h and files_ok:
                skip, why = True, '해시 같음'
            plan.append(dict(L=L, vid=vid, final=final, hash=h, skip=skip, ref=ref))
            if not skip:
                chars += len(final) * int(L['takes'])
            print(f"{vid:<24} {'건너뜀 · ' + why if skip else ('고른 테이크로 다시 인코딩' if a.lock else '만듦 · 테이크 ' + str(L['takes']))}  {final}")
            if a.dry_run:
                print('    hash ' + h)
            if w:
                print('    ⚠ 사전에 없는 약어: ' + ', '.join(w))
            lb = long_breaths(norm)
            if lb:
                print('    ⚠ 한 호흡 25자 넘음: ' + ' / '.join(lb))
    print(f'보낼 글자 합계(테이크 포함) {chars}자 · 모델 {MODEL} · {NORMALIZER_VERSION}')
    if a.dry_run:
        print('(--dry-run — 아무것도 보내거나 만들지 않았습니다)')
        return
    work = [p for p in plan if not p['skip']]
    os.makedirs(MAST, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    key = ''
    if work:
        if not shutil.which('ffmpeg'):
            sys.exit('ffmpeg 가 없습니다. Windows: winget install ffmpeg · Linux: apt-get install -y ffmpeg · mac: brew install ffmpeg')
        if not a.lock and any(not p['L'].get('locked') or a.force for p in work):
            key = find_key()
            if not key:
                sys.exit('Fish 키가 없습니다 — 환경변수 FISH_API_KEY 또는 07_API키/keys.json 의 "fish_audio" (형님이 직접 넣는다)')
            if any(not p['ref'] for p in work):
                sys.exit('voices.json 의 reference_id 가 비어 있습니다 — 목소리 ID 를 넣은 뒤 다시 실행하십시오')
    for p in work:
        L, vid = p['L'], p['vid']
        if (not L.get('locked') or a.force) and not a.lock:   # 고정(--lock)은 다시 요청하지 않고 고른 테이크로 인코딩만
            for k in range(1, int(L['takes']) + 1):
                raw = os.path.join(MAST, f'{vid}_t{k}.raw.wav')
                wav = os.path.join(MAST, f'{vid}_t{k}.wav')
                print(f"  {vid} 테이크 {k}/{L['takes']} 요청")
                post_tts(p['final'], p['ref'], raw, key)
                ff('-i', raw, '-af', AF, '-ac', '1', '-ar', '48000', wav)
        take = int(L.get('locked') or 1)
        src = os.path.join(MAST, f'{vid}_t{take}.wav')
        if not os.path.exists(src):
            sys.exit('테이크 파일이 없습니다: ' + src)
        ogg, m4a = os.path.join(OUT, vid + '.ogg'), os.path.join(OUT, vid + '.m4a')
        ff('-i', src, '-c:a', 'libopus', '-b:a', '32k', '-ac', '1', ogg)
        ff('-i', src, '-c:a', 'aac', '-b:a', '64k', '-ac', '1', '-movflags', '+faststart', m4a)
        dur = 0
        if shutil.which('ffprobe'):
            r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', m4a],
                               capture_output=True, text=True)
            try:
                dur = int(float(r.stdout.strip()) * 1000)
            except ValueError:
                pass
        man[vid] = {'hash': p['hash'], 'duration_ms': dur, 'take': take, 'locked': bool(L.get('locked')),
                    'files': {'m4a': vid + '.m4a', 'ogg': vid + '.ogg'}, 'channel': L['channel'],
                    'priority': int(L['priority']), 'interruptible': bool(L['interruptible'])}
        print(f'  → {vid} · 테이크 {take} · {dur}ms')
    # manifest — json(기록용) + js(앱이 읽는 것: CSP connect-src 가 같은 출처 fetch 도 막아서 script 로 읽는다)
    mobj = {'version': 1, 'normalizer': NORMALIZER_VERSION, 'postproc': POSTPROC_VERSION, 'model': MODEL,
            'updated': time.strftime('%Y-%m-%d %H:%M'), 'clips': dict(sorted(man.items()))}
    with open(man_path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(mobj, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, 'manifest.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('/* T-Book 음성 목록 — render 가 만든다. 손으로 고치지 않는다 */\nwindow.TB_VOICE_MANIFEST='
                + json.dumps(mobj, ensure_ascii=False, separators=(',', ':')) + ';\n')
    lines = load(LINES)
    rv = [{'vid': vid, 'text': sp, 'takes': int(L['takes']), 'locked': L.get('locked')} for L in lines for vid, _, sp in expand(L)]
    with open(os.path.join(HERE, 'review_data.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('window.TTS_REVIEW=' + json.dumps(rv, ensure_ascii=False) + ';')
    print(f'끝 — manifest {len(mobj["clips"])}개 · 테이크 고르기: tools/tts/review.html')


if __name__ == '__main__':
    main()
