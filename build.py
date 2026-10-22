#!/usr/bin/env python3
"""index.src.html → index.html

지오메트리 표 자리({{GEO_*}})를 아래 GEO 데이터로 채웁니다.
  python3 build.py            index.html, en/index.html, ja/index.html 생성
  python3 build.py --preview  preview*.html 생성 (이미지를 설리 CDN 원본 주소로 연결)
번역: i18n/en.json, i18n/ja.json 의 strings는 "한국어 원문": "번역" 쌍입니다.
한국어 원문을 고치면 같은 키를 두 파일에서도 함께 고쳐야 합니다. 빌드 때 번역이 빠진 한국어가 있으면 목록을 출력합니다.
수치 출처: surlybikes.com 각 제품 페이지 지오메트리 차트 (단위 mm, 각도 °, 신장 cm)
"""
import re, sys, html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (행 이름, [사이즈별 값])
GEO = {
    "MIDNIGHT": {
        "sizes": [("40", ""), ("46", ""), ("50", ""), ("54", ""), ("56", ""), ("58", ""), ("60", ""), ("64", "")],
        "rows": [
            ("스택", [531, 538, 544, 560, 580, 599, 620, 641]),
            ("리치", [363, 366, 379, 389, 393, 402, 409, 423]),
            ("탑튜브 길이 (가상)", [500, 520, 540, 555, 570, 585, 605, 625]),
            ("싯튜브 길이", [400, 460, 500, 540, 560, 580, 600, 640]),
            ("헤드튜브 길이", [95, 100, 110, 125, 140, 160, 180, 200]),
            ("헤드 앵글", [71, 71.5, 72, 72.5, 73, 73, 73.5, 74]),
            ("싯튜브 앵글", [75.5, 74, 73.5, 73.5, 73, 73, 72.5, 72.5]),
            ("체인스테이 길이", [425] * 8),
            ("BB 드롭", [70, 70, 65, 65, 65, 65, 65, 65]),
            ("포크 길이 (A-C)", [400] * 8),
            ("포크 오프셋", [50, 50, 50, 50, 40, 40, 40, 40]),
            ("휠베이스", [993, 994, 1007, 1018, 1012, 1027, 1036, 1050]),
            ("스탠드오버", [720, 751, 778, 806, 827, 846, 866, 895]),
            ("권장 신장 (cm)", ["147–158", "155–165", "163–173", "168–178", "173–183", "178–188", "185–196", "193–203"]),
        ],
    },
    "PREAMBLE": {
        "sizes": [("XS", "650B"), ("S", "650B"), ("M", "700C"), ("L", "700C"), ("XL", "700C")],
        "rows": [
            ("스택", [517, 535, 567, 605, 643]),
            ("리치", [352, 381, 391, 404, 421]),
            ("탑튜브 길이 (가상)", [500, 545, 570, 600, 630]),
            ("싯튜브 길이", [410, 505, 565, 605, 645]),
            ("헤드튜브 길이", [120, 135, 130, 170, 210]),
            ("헤드 앵글", [70, 71, 72, 72, 72]),
            ("싯튜브 앵글", [74, 73, 72.5, 72, 72]),
            ("체인스테이 길이", [420, 420, 435, 435, 435]),
            ("BB 드롭", [54, 54, 66, 66, 66]),
            ("포크 길이 (A-C)", [380, 380, 400, 400, 400]),
            ("포크 오프셋", [47, 47, 44, 44, 44]),
            ("휠베이스", [987, 1013, 1030, 1055, 1085]),
            ("스탠드오버", [722, 776, 826, 863, 901]),
            ("권장 신장 (cm)", ["152–165", "163–173", "170–183", "180–191", "188–201"]),
        ],
    },
    "STRAGGLER": {
        "sizes": [("46", "650B"), ("49", "650B"), ("52", "650B"), ("54", "700C"), ("56", "700C"), ("58", "700C"), ("61", "700C"), ("64", "700C")],
        "rows": [
            ("스택", [507.9, 530.4, 554, 570.7, 591.6, 610.6, 639.1, 667.7]),
            ("리치", [363.9, 362.9, 365.3, 391.4, 389.1, 392.5, 403.5, 419.5]),
            ("탑튜브 길이 (가상)", [500, 520, 540, 555, 570, 585, 605, 630]),
            ("싯튜브 길이", [390, 430, 460, 490, 520, 545, 570, 620]),
            ("헤드튜브 길이", [90, 110, 135, 120, 140, 160, 190, 220]),
            ("헤드 앵글", [70, 71, 71, 71.5, 72, 72, 72, 72]),
            ("싯튜브 앵글", [75, 73.5, 72.5, 74, 73, 72.5, 72.5, 72.5]),
            ("체인스테이 길이", [416, 416, 416, 435, 435, 435, 435, 435]),
            ("BB 드롭", [62, 62, 62, 72, 72, 72, 72, 72]),
            ("BB 높이", [277, 277, 277, 285.5, 285.5, 285.5, 285.5, 285.5]),
            ("포크 길이 (A-C)", [387.5, 387.5, 387.5, 407.6, 407.6, 407.6, 407.6, 407.6]),
            ("포크 오프셋", [44] * 8),
            ("휠베이스", [984.4, 982.1, 992.6, 1033.6, 1033.2, 1042.7, 1063, 1088.3]),
            ("스탠드오버", [682, 716, 746, 779, 807, 830, 857, 895]),
            ("권장 신장 (cm)", ["147–157", "155–165", "160–170", "166–177", "173–183", "179–189", "184–194", "193–203"]),
        ],
    },
    "TRUCKER": {
        "sizes": [("42", "26\""), ("46", "26\""), ("50", "26\""), ("52", "26\""), ("54", "26\""),
                  ("56", "700C"), ("58", "700C"), ("60", "700C"), ("62", "700C"), ("64", "700C")],
        "rows": [
            ("스택", [515, 520, 561, 575.5, 594.5, 613, 632, 651.5, 670.5, 685]),
            ("리치", [362, 371, 369, 374.5, 378, 387.5, 391, 400, 402, 412.5]),
            ("탑튜브 길이 (가상)", [500, 515, 530, 545, 560, 575, 590, 605, 620, 635]),
            ("싯튜브 길이", [420, 460, 500, 520, 540, 560, 580, 600, 620, 640]),
            ("헤드튜브 길이", [125, 130, 170, 185, 205, 175, 195, 215, 235, 250]),
            ("헤드 앵글", [70, 70, 71, 71, 71, 72, 72, 72, 72, 72]),
            ("싯튜브 앵글", [75, 74.5, 74, 73.5, 73, 73, 72.5, 72.5, 72, 72]),
            ("체인스테이 길이", [450] * 10),
            ("BB 드롭", [50, 50, 50, 50, 50, 80, 80, 80, 80, 80]),
            ("포크 길이 (A-C)", [376] * 5 + [390] * 5),
            ("포크 오프셋", [45] * 10),
            ("휠베이스", [1026, 1037, 1040, 1050, 1060.5, 1051, 1060, 1075.5, 1084, 1090]),
            ("스탠드오버", [710, 731, 766, 782, 800, 813, 831, 850, 869, 885]),
            ("권장 신장 (cm)", ["152–163", "155–165", "158–168", "163–172", "168–178", "178–188", "178–188", "183–193", "188–198", "193–203"]),
        ],
    },
}


def num(v):
    if isinstance(v, str):
        return v
    return str(int(v)) if float(v).is_integer() else str(v)


def table(g):
    head = "".join(f"<th>{s}{f'<small>{c}</small>' if c else ''}</th>" for s, c in g["sizes"])
    for name, vals in g["rows"]:
        assert len(vals) == len(g["sizes"]), name
    body = "".join(
        f"<tr><th>{html.escape(name)}</th>" + "".join(f"<td>{num(v)}</td>" for v in vals) + "</tr>"
        for name, vals in g["rows"]
    )
    return f'<table class="geo"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table>'


GEO_LABELS = {
    "en": {"스택": "Stack", "리치": "Reach", "탑튜브 길이 (가상)": "Top tube (effective)", "싯튜브 길이": "Seat tube",
           "헤드튜브 길이": "Head tube", "헤드 앵글": "Head angle", "싯튜브 앵글": "Seat angle", "체인스테이 길이": "Chainstay",
           "BB 드롭": "BB drop", "BB 높이": "BB height", "포크 길이 (A-C)": "Fork length (A-C)", "포크 오프셋": "Fork offset",
           "휠베이스": "Wheelbase", "스탠드오버": "Standover", "권장 신장 (cm)": "Rider height (cm)"},
    "ja": {"스택": "スタック", "리치": "リーチ", "탑튜브 길이 (가상)": "トップチューブ長（水平換算）", "싯튜브 길이": "シートチューブ長",
           "헤드튜브 길이": "ヘッドチューブ長", "헤드 앵글": "ヘッド角", "싯튜브 앵글": "シート角", "체인스테이 길이": "チェーンステー長",
           "BB 드롭": "BBドロップ", "BB 높이": "BBハイト", "포크 길이 (A-C)": "フォーク長（A-C）", "포크 오프셋": "フォークオフセット",
           "휠베이스": "ホイールベース", "스탠드오버": "スタンドオーバー", "권장 신장 (cm)": "推奨身長（cm）"},
}

SITE = "https://surly.rubiworkshop.com/"
LANGS = [("ko", "KO", ""), ("en", "EN", "en/"), ("ja", "JA", "ja/")]


def lang_switch(cur):
    depth = "" if cur == "ko" else "../"
    return "".join(
        f'<a href="{depth}{path or "./"}" hreflang="{code}" lang="{code}"{" class=\"on\" aria-current=\"true\"" if code == cur else ""}>{label}</a>'
        for code, label, path in LANGS
    ).replace('href=".././"', 'href="../"')


HREFLANG = "\n".join(
    [f'<link rel="alternate" hreflang="{c}" href="{SITE}{p}">' for c, _, p in LANGS]
    + [f'<link rel="alternate" hreflang="x-default" href="{SITE}">']
)


def translate(html_text, tr):
    out = html_text
    for key in sorted(tr["strings"], key=len, reverse=True):
        val = tr["strings"][key]
        k = re.escape(key)
        out = re.sub(r"(>\s*)" + k + r"(\s*<)", lambda m: m.group(1) + val + m.group(2), out)
        out = out.replace(f'"{key}"', f'"{val}"')
    for pat, rep in tr["patterns"]:
        out = re.sub(pat, rep, out)
    return out


def render(code):
    src = (ROOT / "index.src.html").read_text(encoding="utf-8")
    out = re.sub(r"\{\{GEO_(\w+)\}\}", lambda m: table(GEO[m.group(1)]), src)
    out = out.replace("{{LANG}}", lang_switch(code)).replace("{{HREFLANG}}", HREFLANG)
    assert "{{" not in out, "채워지지 않은 자리표시자가 있습니다"
    if code == "ko":
        return out
    tr = json.loads((ROOT / f"i18n/{code}.json").read_text(encoding="utf-8"))
    for ko, t in GEO_LABELS[code].items():
        out = out.replace(f"<th>{ko}</th>", f"<th>{t}</th>")
    out = translate(out, tr)
    m = tr["meta"]
    out = out.replace('<html lang="ko">', f'<html lang="{m["lang"]}">')
    out = out.replace(f'<link rel="canonical" href="{SITE}">', f'<link rel="canonical" href="{SITE}{m["path"]}">')
    out = out.replace(f'<meta property="og:url" content="{SITE}">', f'<meta property="og:url" content="{SITE}{m["path"]}">')
    out = out.replace('content="ko_KR"', f'content="{m["locale"]}"')
    out = out.replace('"inLanguage": "ko-KR"', f'"inLanguage": "{m["lang"]}"')
    if m.get("fonts"):
        out = re.sub(r"family=Noto\+Sans\+KR[^\"]*display=swap", m["fonts"], out, count=1)
    # 하위 폴더에서 이미지 경로
    out = re.sub(r'((?:src|href)=")images/', r"\1../images/", out)
    out = out.replace("url(images/", "url(../images/")
    left = sorted(set(re.findall(r"[^<>\"]*[가-힣][^<>\"]*", out)))
    left = [x.strip() for x in left if x.strip() and "/*" not in x and "//" not in x]
    if left:
        print(f"[{code}] 번역되지 않은 한국어 {len(left)}개:", left[:30])
    return out


def main():
    manifest = (ROOT / ".github/image-manifest.txt").read_text().splitlines()
    cdn = dict(reversed(l.split()) for l in manifest if l.strip() and not l.startswith("#"))
    for code, _, path in LANGS:
        out = render(code)
        used = set(re.findall(r"images/[\w/.-]+\.(?:jpg|png|svg)", out))
        for u in sorted(used - set(cdn)):
            print("매니페스트에 없는 이미지:", u)
        if "--preview" in sys.argv:
            out = re.sub(r"(?:\.\./)?images/[\w/.-]+\.(?:jpg|png|svg)", lambda m: cdn.get(m.group(0).replace("../", ""), m.group(0)), out)
            name = f"preview{'-' + code if code != 'ko' else ''}.html"
            (ROOT / name).write_text(out, encoding="utf-8")
            print(name)
        else:
            dest = ROOT / path / "index.html"
            dest.parent.mkdir(exist_ok=True)
            dest.write_text(out, encoding="utf-8")
            print(dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
