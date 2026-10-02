"""ko_normalize.py 시험 — 지시서 §3 의 예 전부. ko_normalize.ps1 의 test_normalize.ps1 과 같은 사례.

pytest 로:   python -m pytest test_normalize.py
pytest 없이: python test_normalize.py      (같은 사례를 돌리고 끝에 「통과 N / N」)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ko_normalize import NORMALIZER_VERSION, normalize, select_josa  # noqa: E402

CASES = [
    ('30km/h', '시속 삼십 킬로미터'),
    ('112', '일일이'), ('119', '일일구'), ('182', '일팔이'),
    ('010-1234-5678', '공일공, 일이삼사, 오육칠팔'),
    ('12가3456', '일이 가 삼사오육'), ('123가4567', '일이삼 가 사오육칠'),
    ('서초대로77길', '서초대로 칠십칠 길'), ('219', '이백십구'),
    ('3번 출구', '삼 번 출구'), ('1차로', '일 차로'), ('2호선', '이 호선'),
    ('3명', '세 명'), ('2대', '두 대'), ('20명', '스무 명'), ('21명', '스물한 명'), ('3시', '세 시'), ('100명', '백 명'),
    ('3번 위반', '세 번 위반'),
    ('14:30', '오후 두 시 삼십 분'), ('09:05', '오전 아홉 시 오 분'),
    ('6월', '유월'), ('10월', '시월'), ('3월 5일', '삼월 오 일'),
    ('0.03%', '영 점 영삼 퍼센트'), ('0.08%', '영 점 영팔 퍼센트'),
    ('제44조제1항', '제사십사조 제일항'), ('§68③5', '제육십팔조 제삼항 제오호'), ('§148의2', '제백사십팔조의이'),
    ('50,000원', '오만 원'), ('5만원', '오만 원'), ('벌점 10점', '벌점 십 점'),
    ('IC', '아이씨'), ('CCTV', '씨씨티비'), ('BRT', '비알티'),
    ('서울(으)로', '서울로'), ('서초(으)로', '서초로'), ('반포동(으)로', '반포동으로'), ('경찰관(이)가', '경찰관이'), ('차(이)가', '차가'),
    ('음주측정은 호흡측정이 원칙입니다.', '음주측정은 호흡측정이 원칙입니다.'),
]


def test_cases():
    bad = [(a, normalize(a), b) for a, b in CASES if normalize(a) != b]
    assert not bad, bad


def test_unknown_abbr_warns():
    w = []
    normalize('XYZ 단속', w)
    assert 'XYZ' in w


def test_rieul_josa():
    assert select_josa('길', '(으)로') == '로' and select_josa('집', '(으)로') == '으로'


if __name__ == '__main__':
    ok = bad = 0
    for a, b in CASES:
        got = normalize(a)
        if got == b:
            ok += 1
        else:
            bad += 1
            print(f'  틀림  {a}  →  「{got}」 (기대 「{b}」)')
    for fn in (test_unknown_abbr_warns, test_rieul_josa):
        try:
            fn()
            ok += 1
        except AssertionError:
            bad += 1
            print('  틀림 ', fn.__name__)
    print(f'NORMALIZER_VERSION {NORMALIZER_VERSION} · 통과 {ok} / {ok + bad}')
    sys.exit(1 if bad else 0)
