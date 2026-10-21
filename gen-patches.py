"""patch 폴더의 이미지 목록을 patches.json과 index.html 안에 적는다.

패치 이미지를 추가/삭제/이름변경한 뒤 한 번 실행:  python gen-patches.py

미리보기 페이지는 세 군데를 차례로 본다.
  1. 서버의 디렉터리 목록  - 로컬 개발 서버에서는 이것만으로 자동 반영된다
  2. patches.json          - 목록을 막아둔 정적 호스팅(카페24 등)
  3. index.html 안의 PATCHES_INLINE
                           - file:// 로 그냥 열면 fetch가 CORS로 전부 막혀 이것만 남는다
2번과 3번이 이 스크립트가 적는 대상이다. 배포본이나 파일을 그냥 더블클릭해서
열 사람에게 넘기기 전에는 반드시 실행할 것.
"""
import glob
import io
import json
import os

DIR = os.path.join("assests", "imagas", "patch")
EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")
HTML = "index.html"
BEGIN = "/* PATCHES:BEGIN */"
END = "/* PATCHES:END */"

names = sorted(os.path.basename(f) for f in glob.glob(os.path.join(DIR, "*"))
               if f.lower().endswith(EXT))
assert names, "patch 폴더에 이미지가 없다"

out = os.path.join(DIR, "patches.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(names, ensure_ascii=False, indent=2))

html = io.open(HTML, encoding="utf-8").read()
i, j = html.index(BEGIN), html.index(END)
block = BEGIN + "\n    var PATCHES_INLINE = " + json.dumps(names, ensure_ascii=False) + ";\n    "
html = html[:i] + block + html[j:]
io.open(HTML, "w", encoding="utf-8").write(html)

print("%d patches -> %s, %s" % (len(names), out, HTML))

# 되읽어서 두 출력이 디스크와 같은지 확인한다
assert json.load(io.open(out, encoding="utf-8")) == names, "patches.json이 목록과 다르다"
again = io.open(HTML, encoding="utf-8").read()
inline = again[again.index(BEGIN) + len(BEGIN):again.index(END)]
assert json.loads(inline.split("=", 1)[1].rsplit(";", 1)[0]) == names, "PATCHES_INLINE이 목록과 다르다"
print("verified")
