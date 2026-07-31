# T-Book 검사 스크립트 세트 — v19.8.3 (2026-07-31)

NAS 폴더가 이 세션에 연결되지 않아 원본 guard.py·full.js를 못 읽었다.
**HANDOFF 3-2 / 3-4 사양대로 새로 작성**했고, 기준선(v19.8.2)에서
HANDOFF와 같은 수치가 나오는 것으로 동등성을 확인했다.

| 파일 | 용도 | 기준선 v19.8.2 재현 |
|---|---|---|
| `guard.py` | 구조 파수꾼 6종. 브라우저 없이 0.5초 | 페이지 **54/54** · 아이콘 **27/27** · 탭 **51** ✅ HANDOFF와 일치 |
| `extract.py` | `<script>` 추출 + 블록별 SHA-256 | **54개** ✅ |
| `overflow.js` | 🆕 `getBoundingClientRect` 실측 가로넘침 (HANDOFF 3-4) | — |
| `audit.js` | 51탭 × 2모드 × 2폭 = **204 visits** | ✅ |
| `full.js` | 전 버튼 실클릭 + DOM 중첩 + onclick 함수 존재 | ✅ |
| `cmp.js` | 기준선 대비 하단메뉴·페이지·탭 수 | ✅ |
| `patch_v1983.py` + `parts_*.py` | v19.8.2 → v19.8.3 패치 (전 앵커 assert) | — |

⚠️ `guard.py`의 div 수는 **script/style 내부를 제외**하고 센다(1742/1973).
원본 guard.py의 1985와 숫자가 다른 것은 그 때문이며, **검사 내용은 개폐 균형**이라 동일하다.

## 실행 순서 (HANDOFF 3-1)
```bash
python3 patch_v1983.py
python3 guard.py TBook_v19.8.3.html base_v19.8.2.html
python3 extract.py TBook_v19.8.3.html /tmp/b83
for f in /tmp/b83/b*.js; do node --check "$f"; done
diff /tmp/b82/HASHES.txt /tmp/b83/HASHES.txt      # JS 무접촉 증명
(HOME=/root python3 -m http.server 8953 --directory . &)
node audit.js TBook_v19.8.3.html
node full.js  TBook_v19.8.3.html
node cmp.js   base_v19.8.2.html TBook_v19.8.3.html
node overflow.js TBook_v19.8.3.html police_gen 360
```

## 🆕 overflow.js 가 왜 필요한가
`body{overflow-x:hidden}` 때문에 **document.scrollWidth 로는 가로넘침이 영원히 0으로 보인다.**
v19.8.2의 「가로넘침 0」 보고가 그래서 나왔고, 실제로는 표가 **1,129px**까지 늘어나 잘려 있었다.
`overflow.js`는 요소별 `getBoundingClientRect().right` 를 뷰포트와 비교한다 — HANDOFF 3-4 원칙 그대로다.
