# T-Book TTS — 한국어 낭독 정규화(숫자·기호를 읽는 글로). 지시서 「T-Book TTS 정비 ver.1」 §3.
# 이 PC 에 Python 이 없어 ko_normalize.py 대신 PowerShell 로 만들었다(형님 승인 2026-10-02 「권고대로」).
# 쓰는 법:  . .\ko_normalize.ps1 ;  Convert-KoSpoken '30km/h'   →  시속 삼십 킬로미터
# ⚠ 법적 고지 문안(channel notice)은 의미를 바꾸지 않는다 — 띄어쓰기·쉼표·숫자 읽기만.
$script:NORMALIZER_VERSION = 'ko-norm-1.0.0'

$script:SINO_D = @('', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구')
$script:DIGIT_ZERO_GONG = @('공', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구')
$script:DIGIT_ZERO_YEONG = @('영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구')
$script:NATIVE_1 = @('', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉')
$script:NATIVE_10 = @('', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔')
# 약어 사전 — 없는 약어는 경고 목록으로 낸다
$script:ABBR = [ordered]@{ 'CCTV' = '씨씨티비'; 'KICS' = '킥스'; 'BRT' = '비알티'; 'GPS' = '지피에스'; 'IC' = '아이씨'; 'JC' = '제이씨'; 'PM' = '피엠'; 'TAAS' = '타스'; 'KTX' = '케이티엑스'; 'SRT' = '에스알티' }
# 고유어로 읽는 단위(1~99). 그 밖(분·초·원·점·차로·호선·층·회·km 등)은 한자어
$script:NATIVE_UNITS = @('명', '대', '시', '번', '개', '마리', '살', '사람', '장', '잔', '군데', '곳', '시간', '달', '벌', '켤레', '가지')

function Get-KoSino([long]$n) {
  if ($n -eq 0) { return '영' }
  $out = ''
  $groups = @(@(1000000000000, '조'), @(100000000, '억'), @(10000, '만'), @(1, ''))
  foreach ($g in $groups) {
    $q = [long][Math]::Floor($n / $g[0]); $n = $n % $g[0]
    if ($q -eq 0) { continue }
    $part = Get-KoSino4 $q
    if ($g[1] -eq '만' -and $part -eq '일') { $part = '' }   # 일만 → 만
    $out += $part + $g[1]
  }
  return $out
}
function Get-KoSino4([int]$n) {
  $s = ''; $u = @(@(1000, '천'), @(100, '백'), @(10, '십'), @(1, ''))
  foreach ($x in $u) {
    $d = [int][Math]::Floor($n / $x[0]); $n = $n % $x[0]
    if ($d -eq 0) { continue }
    if ($d -eq 1 -and $x[0] -gt 1) { $s += $x[1] } else { $s += $script:SINO_D[$d] + $x[1] }
  }
  return $s
}
# 고유어 수관형사(1~99). 20 은 단위 앞에서 「스무」
function Get-KoNative([int]$n) {
  if ($n -lt 1 -or $n -gt 99) { return (Get-KoSino $n) }
  $t = [int][Math]::Floor($n / 10); $o = $n % 10
  if ($t -eq 2 -and $o -eq 0) { return '스무' }
  return $script:NATIVE_10[$t] + $script:NATIVE_1[$o]
}
function Get-KoDigits([string]$d, [string]$zero = '공') {
  $tbl = if ($zero -eq '공') { $script:DIGIT_ZERO_GONG } else { $script:DIGIT_ZERO_YEONG }
  return (($d.ToCharArray() | ForEach-Object { $tbl[[int][string]$_] }) -join '')
}
function Get-KoMonth([int]$m) { if ($m -eq 6) { return '유월' }; if ($m -eq 10) { return '시월' }; return (Get-KoSino $m) + '월' }
function Get-KoHour([int]$h, [int]$mi, [bool]$ampm) {
  $pre = ''
  if ($ampm) { if ($h -lt 12) { $pre = '오전 ' } else { $pre = '오후 ' } }
  $hh = $h; if ($ampm -and $h -gt 12) { $hh = $h - 12 }
  $hs = if ($hh -eq 0) { '영 시' } else { (Get-KoNative $hh) + ' 시' }
  $ms = if ($mi -gt 0) { ' ' + (Get-KoSino $mi) + ' 분' } else { '' }
  return $pre + $hs + $ms
}
# 받침으로 조사 고르기 — 「(으)로」·「(이)가」·「(을)를」·「(은)는」·「(과)와」
function Select-KoJosa([string]$word, [string]$pair) {
  $c = [int][char]($word.TrimEnd()[-1])
  $has = $false; $rieul = $false
  if ($c -ge 0xAC00 -and $c -le 0xD7A3) { $jong = ($c - 0xAC00) % 28; $has = ($jong -ne 0); $rieul = ($jong -eq 8) }
  switch ($pair) {
    '(으)로' { if ($has -and -not $rieul) { return '으로' } else { return '로' } }
    '(이)가' { if ($has) { return '이' } else { return '가' } }
    '(을)를' { if ($has) { return '을' } else { return '를' } }
    '(은)는' { if ($has) { return '은' } else { return '는' } }
    '(과)와' { if ($has) { return '과' } else { return '와' } }
    '(이)라' { if ($has) { return '이라' } else { return '라' } }
  }
  return $pair
}
function Resolve-KoJosa([string]$t) {
  return [regex]::Replace($t, '([가-힣A-Za-z0-9]+)\s?(\((?:으)\)로|\((?:이)\)가|\((?:을)\)를|\((?:은)\)는|\((?:과)\)와|\((?:이)\)라)', {
      param($m) $m.Groups[1].Value + (Select-KoJosa $m.Groups[1].Value $m.Groups[2].Value) })
}

function Convert-KoSpoken([string]$t, [ref]$Warn) {
  if ($null -eq $t) { return '' }
  $w = New-Object System.Collections.Generic.List[string]
  $R = { param($p, $f) $script:__t = [regex]::Replace($script:__t, $p, [System.Text.RegularExpressions.MatchEvaluator]$f) }
  $script:__t = $t
  # 법조문: §68③5 → 제육십팔조 제삼항 제오호 / 제44조제1항 → 제사십사조 제일항
  $circ = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
  & $R '§\s?(\d+)(?:의(\d+))?([①-⑳])?(\d+)?' { param($m)
    $s = '제' + (Get-KoSino ([long]$m.Groups[1].Value)) + '조'
    if ($m.Groups[2].Success) { $s += '의' + (Get-KoSino ([long]$m.Groups[2].Value)) }
    if ($m.Groups[3].Success) { $s += ' 제' + (Get-KoSino ($circ.IndexOf($m.Groups[3].Value) + 1)) + '항' }
    if ($m.Groups[4].Success) { $s += ' 제' + (Get-KoSino ([long]$m.Groups[4].Value)) + '호' }
    $s }
  & $R '제\s?(\d+)\s?(조|항|호|장|절)(의\s?(\d+))?' { param($m)
    $s = '제' + (Get-KoSino ([long]$m.Groups[1].Value)) + $m.Groups[2].Value
    if ($m.Groups[3].Success) { $s += '의' + (Get-KoSino ([long]$m.Groups[4].Value)) }
    $s + ' ' }
  # 혈중알코올농도·소수 퍼센트: 0.03% → 영 점 영삼 퍼센트
  & $R '(\d+)\.(\d+)\s?%' { param($m) (Get-KoSino ([long]$m.Groups[1].Value)) + ' 점 ' + (Get-KoDigits $m.Groups[2].Value '영') + ' 퍼센트' }
  & $R '(\d+)\s?%' { param($m) (Get-KoSino ([long]$m.Groups[1].Value)) + ' 퍼센트' }
  # 속도
  & $R '(\d+)\s?(km/h|㎞/h|킬로미터 매 시)' { param($m) '시속 ' + (Get-KoSino ([long]$m.Groups[1].Value)) + ' 킬로미터' }
  # 전화번호(0으로 시작, 하이픈) · 긴급번호 — 자리 단위, 0 = 공
  & $R '(?<!\d)(0\d{1,2})[-.\s](\d{3,4})[-.\s](\d{4})(?!\d)' { param($m) (Get-KoDigits $m.Groups[1].Value) + ', ' + (Get-KoDigits $m.Groups[2].Value) + ', ' + (Get-KoDigits $m.Groups[3].Value) }
  & $R '(?<!\d)(112|119|182|1393|1366|1388|1577-?\d{4})(?!\d)' { param($m) Get-KoDigits ($m.Groups[1].Value -replace '-', '') }
  # 차량번호: 12가3456 → 일이 가 삼사오육
  & $R '(?<!\d)(\d{2,3})\s?([가-힣])\s?(\d{4})(?!\d)' { param($m) (Get-KoDigits $m.Groups[1].Value) + ' ' + $m.Groups[2].Value + ' ' + (Get-KoDigits $m.Groups[3].Value) }
  # 시각: 14:30 → 오후 두 시 삼십 분
  & $R '(?<!\d)([01]?\d|2[0-3]):([0-5]\d)(?!\d)' { param($m) Get-KoHour ([int]$m.Groups[1].Value) ([int]$m.Groups[2].Value) $true }
  # 날짜: N월 → 유월·시월 / N일
  & $R '(?<!\d)(1[0-2]|[1-9])\s?월' { param($m) Get-KoMonth ([int]$m.Groups[1].Value) }
  # 금액: 50,000원 → 오만 원 · 5만원 → 오만 원
  & $R '(\d{1,3}(?:,\d{3})+|\d+)\s?(만|억)?\s?원' { param($m)
    $n = [long]($m.Groups[1].Value -replace ',', ''); $u = $m.Groups[2].Value
    if ($u -eq '만') { $n *= 10000 } elseif ($u -eq '억') { $n *= 100000000 }
    (Get-KoSino $n) + ' 원' }
  # 도로명 길 번호: 서초대로77길 → 서초대로 칠십칠 길
  & $R '([가-힣]+(?:대로|로))\s?(\d+)\s?(가)?길' { param($m) $m.Groups[1].Value + ' ' + (Get-KoSino ([long]$m.Groups[2].Value)) + ' ' + $(if ($m.Groups[3].Success) { '가 ' } else { '' }) + '길' }
  # 출구·차로·호선·층·회·점(벌점) — 한자어
  & $R '(\d+)\s?번\s?(출구|버스|국도|게이트|홈)' { param($m) (Get-KoSino ([long]$m.Groups[1].Value)) + ' 번 ' + $m.Groups[2].Value }
  & $R '(\d+)\s?(차로|호선|층|회|점|분|초|년|일|호|조|항|킬로미터|미터|센티미터|퍼센트|원)' { param($m) (Get-KoSino ([long]$m.Groups[1].Value)) + ' ' + $m.Groups[2].Value }
  # 고유어 단위(1~99) — 100 이상은 한자어
  $nu = ($script:NATIVE_UNITS | Sort-Object Length -Descending) -join '|'
  & $R ('(?<![\d.])(\d+)\s?(' + $nu + ')') { param($m)
    $n = [long]$m.Groups[1].Value
    $lim = if ($m.Groups[2].Value -eq '시') { 12 } else { 99 }   # 13시 이상은 「십삼 시」
    $num = if ($n -ge 1 -and $n -le $lim) { Get-KoNative ([int]$n) } else { Get-KoSino $n }
    $num + ' ' + $m.Groups[2].Value }
  # 약어
  foreach ($k in $script:ABBR.Keys) { $script:__t = $script:__t -creplace ('(?<![A-Za-z])' + $k + '(?![A-Za-z])'), $script:ABBR[$k] }
  foreach ($m in [regex]::Matches($script:__t, '(?<![A-Za-z])[A-Z]{2,}(?![A-Za-z])')) { if (-not $w.Contains($m.Value)) { $w.Add($m.Value) } }
  # 남은 숫자 — 한자어(쉼표 자리수 포함)
  & $R '\d{1,3}(?:,\d{3})+|\d+' { param($m) Get-KoSino ([long]($m.Value -replace ',', '')) }
  $out = Resolve-KoJosa $script:__t
  $out = ($out -replace '[ \t]{2,}', ' ').Trim()
  if ($Warn) { $Warn.Value = $w.ToArray() }
  return $out
}
# 한 호흡(쉼표·마침표 사이) 25자를 넘는 마디 — 렌더 전 점검용(고치지는 않는다)
function Get-KoLongBreaths([string]$t, [int]$max = 25) {
  return @($t -split '[,.?!·]' | ForEach-Object { $_.Trim() } | Where-Object { ($_ -replace '\s', '').Length -gt $max })
}
