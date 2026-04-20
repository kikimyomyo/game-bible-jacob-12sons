#!/bin/bash
# bash _dl.sh <name>
# 1) ChatGPT 공유 다이얼로그에서 "링크 복사"를 누른 직후 실행
# 2) pbpaste의 share URL → 공유 HTML → sediment 없는 enc URL → 1024x1024 원본 PNG 다운로드
set -e
NAME="${1:?usage: bash _dl.sh <name>}"
IMG_DIR="$(cd "$(dirname "$0")" && pwd)/assets/images"
SHARE_URL="$(pbpaste | tr -d '\n' | tr -d ' ')"
if [[ "$SHARE_URL" != https://chatgpt.com/s/* ]]; then
  echo "❌ 클립보드가 공유 URL이 아닙니다: $SHARE_URL"
  exit 1
fi
echo "▶ share = $SHARE_URL"
curl -sL "$SHARE_URL" > /tmp/sp_${NAME}.html
ENC_URL=$(NAME="$NAME" python3 - <<'PY'
import re, base64, json, sys, os
name = os.environ.get('NAME','x')
html = open(f'/tmp/sp_{name}.html').read()
urls = list(dict.fromkeys(re.findall(r'backend-api/estuary/public_content/enc/[A-Za-z0-9+/=]+', html)))
for u in urls:
    try:
        d = json.loads(base64.b64decode(u.split('/enc/')[1] + '===').decode())
        if 'sediment' not in d.get('id',''):
            print(u); break
    except: pass
PY
)
if [[ -z "$ENC_URL" ]]; then echo "❌ 원본 enc URL 추출 실패"; exit 1; fi
mkdir -p "$IMG_DIR"
curl -sSL -o "$IMG_DIR/${NAME}.png" "https://chatgpt.com/$ENC_URL"
FILE_INFO=$(file "$IMG_DIR/${NAME}.png")
SIZE=$(ls -la "$IMG_DIR/${NAME}.png" | awk '{print $5}')
echo "✓ $IMG_DIR/${NAME}.png ($SIZE bytes)"
echo "  $FILE_INFO"
