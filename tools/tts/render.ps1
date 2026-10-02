# T-Book TTS 렌더 — lines.json → Fish Audio(S2-Pro) → masters/ wav(테이크 3) → assets/voice/{id}.ogg·.m4a + manifest.json·manifest.js
# 지시서 「T-Book TTS 정비 ver.1」 §4·§5. render.py 대신 PowerShell(이 PC 에 Python 없음 · 형님 승인 「권고대로」).
# 쓰는 법(형님 PC 에서만 — 앱은 실행 중에 음성을 만들지 않는다):
#   powershell -File render.ps1 -DryRun                       무엇을 만들지·건너뛸지만 보인다(키·ffmpeg 불필요)
#   powershell -File render.ps1 -Only blood_notice_1,blood_notice_2,blood_withdraw    시험 3줄
#   powershell -File render.ps1 -Lock blood_notice_1=2        리뷰에서 고른 테이크로 고정(lines.json locked) → 그 테이크로 다시 인코딩
#   -Force  해시가 같아도 다시 만든다(locked 는 그래도 건너뜀)
# 키: 환경변수 FISH_API_KEY 에서만 읽는다. 파일·로그·화면 어디에도 쓰지 않는다. 이 폴더(tools/)는 Pages 로 공개되므로 .env 를 두지 않는다.
param([switch]$DryRun, [string[]]$Only, [switch]$Force, [string]$Lock)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
. "$PSScriptRoot\ko_normalize.ps1"
$POSTPROC_VERSION = 'pp-1 lead50 tail150 loudnorm-16'
$MODEL = 's2-pro'; $FORMAT = 'wav'; $LATENCY = 'normal'; $NORMALIZE = $false
$U8 = New-Object System.Text.UTF8Encoding($false)
$ROOT = (Resolve-Path "$PSScriptRoot\..\..").Path              # 배포용 폴더(= 저장소 루트와 같은 모양)
$MAST = Join-Path $PSScriptRoot 'masters'; $OUT = Join-Path $ROOT 'assets\voice'
New-Item -ItemType Directory -Force $MAST, $OUT | Out-Null
$linesPath = Join-Path $PSScriptRoot 'lines.json'
$lines = @(([IO.File]::ReadAllText($linesPath, $U8) | ConvertFrom-Json) | ForEach-Object { $_ })   # PS 5.1 은 배열을 한 덩어리로 돌려준다 — 풀어 담는다
$voices = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'voices.json'), $U8) | ConvertFrom-Json
$manPath = Join-Path $OUT 'manifest.json'
$man = @{}
if (Test-Path $manPath) { $mj = [IO.File]::ReadAllText($manPath, $U8) | ConvertFrom-Json; if ($mj.clips) { $mj.clips.PSObject.Properties | ForEach-Object { $man[$_.Name] = $_.Value } } }

function Sha256([string]$t) { $h = [Security.Cryptography.SHA256]::Create(); (($h.ComputeHash($U8.GetBytes($t)) | ForEach-Object { $_.ToString('x2') }) -join '') }
function Need-Ffmpeg { if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { Write-Host 'ffmpeg 가 없습니다. 먼저 설치하십시오:  winget install ffmpeg   (설치 뒤 창을 새로 여십시오)'; exit 2 } }
function Strip-Punct([string]$t) { return ($t -replace '[\s,.·?!]', '') }

# 슬롯 펼치기 — 조합마다 문장 단위로 렌더(클립 이어 붙이기 금지). 200 넘으면 멈춤
function Expand-Line($L) {
  $keys = @(); if ($L.slots) { $keys = @($L.slots.PSObject.Properties | ForEach-Object { $_.Name }) }
  $combos = @(@{})
  foreach ($k in $keys) { $nx = @(); foreach ($c in $combos) { foreach ($v in @($L.slots.$k)) { $d = @{} + $c; $d[$k] = [string]$v; $nx += , $d } }; $combos = $nx }
  if ($combos.Count -gt 200) { throw ("{0}: 슬롯 조합 {1}개 — 200 을 넘어 멈춥니다(지시서 §2)" -f $L.id, $combos.Count) }
  foreach ($c in $combos) {
    $raw = [string]$L.text_raw; $sp = if ([string]$L.text_spoken) { [string]$L.text_spoken } else { $raw }; $vid = $L.id
    foreach ($k in $c.Keys) { $raw = $raw.Replace('{' + $k + '}', $c[$k]); $sp = $sp.Replace('{' + $k + '}', $c[$k]); $vid += '__' + $k + '-' + (Sha256 $c[$k]).Substring(0, 6) }
    [pscustomobject]@{ vid = $vid; raw = $raw; spoken = $sp; slots = $c }
  }
}

# -Lock id=take : lines.json 의 locked 를 글 그대로 바꾼다(파일 모양을 흐트러뜨리지 않으려고 정규식)
if ($Lock) {
  if ($Lock -notmatch '^([\w-]+)=(\d)$') { throw '-Lock 은 「아이디=테이크번호」 꼴입니다 (예: blood_notice_1=2)' }
  $lid = $Matches[1]; $lt = [int]$Matches[2]
  $txt = [IO.File]::ReadAllText($linesPath, $U8)
  $rx = New-Object regex ('("id":\s*"' + [regex]::Escape($lid) + '"[\s\S]*?"locked":\s*)(null|\d+)')
  if (-not $rx.IsMatch($txt)) { throw "lines.json 에 $lid 가 없습니다" }
  [IO.File]::WriteAllText($linesPath, $rx.Replace($txt, ('${1}' + $lt), 1), $U8)
  $lines = @(([IO.File]::ReadAllText($linesPath, $U8) | ConvertFrom-Json) | ForEach-Object { $_ })   # PS 5.1 은 배열을 한 덩어리로 돌려준다 — 풀어 담는다
  $Only = @($lid); $Force = $true
  "고정: $lid → 테이크 $lt"
}

$todo = @($lines | Where-Object { -not $Only -or ($Only -contains $_.id) })
if (-not $todo.Count) { throw '할 대사가 없습니다(-Only 이름 확인)' }
$chars = 0; $plan = @()
foreach ($L in $todo) {
  $vref = $voices.($L.speaker); $refId = if ($vref) { [string]$vref.reference_id } else { '' }
  foreach ($v in (Expand-Line $L)) {
    $w = $null; $norm = Convert-KoSpoken $v.spoken ([ref]$w)
    # §1-4 — 법적 고지는 원문과 의미가 한 글자도 달라지면 안 된다: 빈칸·쉼표·마침표·가운뎃점을 빼고 같아야 한다
    if ($L.channel -eq 'notice' -and (Strip-Punct $norm) -cne (Strip-Punct $v.raw)) { throw ("{0}: 낭독문이 원문과 다릅니다 — 원문 「{1}」 / 낭독 「{2}」" -f $v.vid, $v.raw, $norm) }
    $final = '[' + $L.emotion + '] ' + $norm
    $key = @("text_final=$final", "speaker=$($L.speaker)", "reference_id=$refId", "model=$MODEL", "format=$FORMAT", "latency=$LATENCY",
      "normalize=$NORMALIZE", "takes=$($L.takes)", "normalizer=$NORMALIZER_VERSION", "postproc=$POSTPROC_VERSION") -join "`n"
    $hash = Sha256 $key
    $have = $man[$v.vid]
    $filesOk = (Test-Path (Join-Path $OUT "$($v.vid).ogg")) -and (Test-Path (Join-Path $OUT "$($v.vid).m4a"))
    $skip = $false; $why = ''
    if ($L.locked -and $filesOk -and -not $Lock) { $skip = $true; $why = "고정됨(테이크 $($L.locked))" }
    elseif (-not $Force -and $have -and $have.hash -eq $hash -and $filesOk) { $skip = $true; $why = '해시 같음' }
    $long = Get-KoLongBreaths $norm
    $plan += [pscustomobject]@{ L = $L; v = $v; final = $final; hash = $hash; skip = $skip; why = $why; refId = $refId }
    if (-not $skip) { $chars += $final.Length * [int]$L.takes }
    "{0,-24} {1}  {2}" -f $v.vid, $(if ($skip) { "건너뜀 · $why" } elseif ($Lock) { "고른 테이크로 다시 인코딩" } else { "만듦 · 테이크 $($L.takes)" }), $final
    if ($DryRun) { "    hash " + $hash }
    if (@($w).Count) { "    ⚠ 사전에 없는 약어: " + (@($w) -join ', ') }
    if ($long.Count) { "    ⚠ 한 호흡 25자 넘음: " + ($long -join ' / ') }
  }
}
"보낼 글자 합계(테이크 포함) {0}자 · 모델 {1} · {2}" -f $chars, $MODEL, $NORMALIZER_VERSION
if ($DryRun) { '(-DryRun — 아무것도 보내거나 만들지 않았습니다)'; exit 0 }

$work = @($plan | Where-Object { -not $_.skip })
if ($work.Count) {
  Need-Ffmpeg
  $key = $env:FISH_API_KEY
  if (-not $Lock -and @($work | Where-Object { -not $_.L.locked }).Count) {
    if (-not $key) { Write-Host '환경변수 FISH_API_KEY 가 없습니다. 형님 PC 에서:  setx FISH_API_KEY "키"  (창을 새로 연 뒤 다시 실행)'; exit 2 }
    if (@($work | Where-Object { -not $_.refId }).Count) { Write-Host 'voices.json 의 reference_id 가 비어 있습니다 — 목소리 ID 를 넣은 뒤 다시 실행하십시오.'; exit 2 }
  }
}
function Post-Tts($p, [string]$dst) {
  $body = @{ text = $p.final; reference_id = $p.refId; format = $FORMAT; normalize = $NORMALIZE; latency = $LATENCY } | ConvertTo-Json -Compress
  $hdr = @{ Authorization = ('Bearer ' + $env:FISH_API_KEY); model = $MODEL }
  for ($try = 0; $try -le 3; $try++) {
    try { Invoke-WebRequest -Uri 'https://api.fish.audio/v1/tts' -Method Post -Headers $hdr -ContentType 'application/json; charset=utf-8' -Body $U8.GetBytes($body) -OutFile $dst -UseBasicParsing -TimeoutSec 180; return }
    catch {
      $code = 0; try { $code = [int]$_.Exception.Response.StatusCode } catch {}
      if (($code -eq 429 -or $code -ge 500) -and $try -lt 3) { $s = [Math]::Pow(2, $try + 1); "    {0} — {1}초 뒤 다시({2}/3)" -f $code, $s, ($try + 1); Start-Sleep -Seconds $s; continue }
      throw ("Fish 요청 실패(HTTP {0}) — {1}" -f $code, $p.v.vid)   # 키는 메시지에 넣지 않는다
    }
  }
}
function Post-Proc([string]$src, [string]$dst) {
  $af = 'silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.15,areverse,loudnorm=I=-16:TP=-1.5:LRA=11'
  & ffmpeg -hide_banner -loglevel error -y -i $src -af $af -ac 1 -ar 48000 $dst; if ($LASTEXITCODE) { throw "ffmpeg 후처리 실패: $src" }
}
foreach ($p in $work) {
  $vid = $p.v.vid; $takes = [int]$p.L.takes
  if ((-not $p.L.locked -or $Force) -and -not $Lock) {   # 고정(-Lock)은 다시 요청하지 않고 고른 테이크로 인코딩만
    for ($k = 1; $k -le $takes; $k++) {
      $raw = Join-Path $MAST ("{0}_t{1}.raw.wav" -f $vid, $k); $wav = Join-Path $MAST ("{0}_t{1}.wav" -f $vid, $k)
      "  {0} 테이크 {1}/{2} 요청" -f $vid, $k, $takes
      Post-Tts $p $raw; Post-Proc $raw $wav
    }
  }
  $take = if ($p.L.locked) { [int]$p.L.locked } else { 1 }
  $src = Join-Path $MAST ("{0}_t{1}.wav" -f $vid, $take)
  if (-not (Test-Path $src)) { throw "테이크 파일이 없습니다: $src" }
  $ogg = Join-Path $OUT "$vid.ogg"; $m4a = Join-Path $OUT "$vid.m4a"
  & ffmpeg -hide_banner -loglevel error -y -i $src -c:a libopus -b:a 32k -ac 1 $ogg; if ($LASTEXITCODE) { throw 'ogg 인코딩 실패' }
  & ffmpeg -hide_banner -loglevel error -y -i $src -c:a aac -b:a 64k -ac 1 -movflags +faststart $m4a; if ($LASTEXITCODE) { throw 'm4a 인코딩 실패' }
  $dur = 0; try { $dur = [int]([double](& ffprobe -v error -show_entries format=duration -of csv=p=0 $m4a) * 1000) } catch {}
  $man[$vid] = [pscustomobject]@{ hash = $p.hash; duration_ms = $dur; take = $take; locked = [bool]$p.L.locked; files = [pscustomobject]@{ m4a = "$vid.m4a"; ogg = "$vid.ogg" }
    channel = $p.L.channel; priority = [int]$p.L.priority; interruptible = [bool]$p.L.interruptible }
  "  → {0} · 테이크 {1} · {2}ms" -f $vid, $take, $dur
}
# manifest — json(기록용) + js(앱이 읽는 것: CSP connect-src 가 같은 출처 fetch 도 막아서 script 로 읽는다)
$clips = [ordered]@{}; foreach ($k in ($man.Keys | Sort-Object)) { $clips[$k] = $man[$k] }
$mobj = [ordered]@{ version = 1; normalizer = $NORMALIZER_VERSION; postproc = $POSTPROC_VERSION; model = $MODEL; updated = (Get-Date -Format 'yyyy-MM-dd HH:mm'); clips = $clips }
$json = $mobj | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($manPath, $json, $U8)
[IO.File]::WriteAllText((Join-Path $OUT 'manifest.js'), ("/* T-Book 음성 목록 — render.ps1 이 만든다. 손으로 고치지 않는다 */`nwindow.TB_VOICE_MANIFEST=" + ($mobj | ConvertTo-Json -Depth 6 -Compress) + ";`n"), $U8)
# 리뷰 화면 자료(로컬 전용)
$rv = @($lines | ForEach-Object { $L = $_; Expand-Line $L | ForEach-Object { [ordered]@{ vid = $_.vid; text = $_.spoken; takes = [int]$L.takes; locked = $L.locked } } })
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'review_data.js'), ('window.TTS_REVIEW=' + ($rv | ConvertTo-Json -Depth 4 -Compress) + ';'), $U8)
"끝 — manifest {0}개 · 테이크 고르기: tools\tts\review.html" -f $clips.Count
