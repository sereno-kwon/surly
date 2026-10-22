# Surly · Rubi Workshop

surly.rubiworkshop.com 원페이지 정적 사이트 (GitHub Pages). crustbikes.co.kr, quoc.rubiworkshop.com과 같은 구조입니다.

- `index.html` 원페이지 본체 (한국어), `en/index.html` 영어, `ja/index.html` 일본어. 모두 빌드 결과물입니다.
- 원페이지 구성 (SURLY · MIDNIGHT SPECIAL · PREAMBLE · STRAGGLER · DISC TRUCKER · SHOWROOM). 루비워크샵 주력 설리 모델 4종 중심입니다.
- `index.src.html` 편집용 원본. 지오메트리 표는 `{{GEO_*}}` 자리에 `build.py`가 채웁니다. 내용을 고칠 때는 `index.src.html`을 수정한 뒤 `python3 build.py`를 실행합니다. `index.html`을 직접 고치면 다음 빌드 때 덮어써집니다.
- `build.py` 지오메트리 데이터와 빌드 스크립트. `python3 build.py`로 세 언어 페이지를 한 번에 생성
- `i18n/en.json`, `i18n/ja.json` 번역. `strings`는 "한국어 원문": "번역" 쌍이라, 한국어 문장을 고치면 두 파일의 같은 키도 함께 고칩니다. 빠진 번역은 빌드 때 목록으로 출력됩니다.
- `404.html` 하위 주소(/midnight-special, /en/straggler, /ja/disc-trucker 등)를 섹션으로 연결
- `images/` 섹션별 이미지 (`hero`, `brand`, `midnight`, `preamble`, `straggler`, `trucker`)
- `.github/image-manifest.txt` + `fetch-images.yml` 설리 공식 사이트(surlybikes.com) CDN 이미지 이전용 워크플로

## 서체
영문 지마켓 산스(GmarketSans), 한글 에스코어 드림(S-Core Dream), 일본어 Noto Sans JP. 지마켓 산스와 에스코어 드림은 jsDelivr(눈누) CDN에서 불러옵니다.

## 이미지
매니페스트를 수정해 main에 푸시하면 Actions가 이미지를 받아 `images/`에 커밋합니다.
이미 받은 파일은 건너뛰므로, 이미지를 교체할 때는 해당 파일을 지우거나 새 파일명으로 추가합니다.
첫 세팅 때 이미지가 비어 있으면 Actions 탭에서 `Fetch images from Surly CDN`을 한 번 실행(Run workflow)하면 됩니다.
루비워크샵에서 직접 찍은 사진으로 바꿀 때는 같은 경로에 파일을 덮어쓰면 됩니다 (파일명 규칙: rubi-surly-lifestyle-상황-숫자).

## 도메인
`CNAME`은 surly.rubiworkshop.com. rubiworkshop.com DNS에 `surly` CNAME 레코드(값 sereno-kwon.github.io)를 추가하고, 저장소 Settings > Pages에서 Custom domain과 Enforce HTTPS를 확인합니다.

## 구글 애널리틱스 (GA4)
루비컴퍼니 브랜드 사이트 공통 코드입니다.

- 측정 ID는 `index.src.html` 맨 위의 `var GA_ID = '';` 한 곳에 넣습니다. 비어 있으면 GA를 불러오지 않습니다. 바꾼 뒤 `python3 build.py`로 세 언어 페이지를 다시 만듭니다.
- 페이지 언어가 콘텐츠 그룹(`content_group`: ko, en, ja)으로 기록됩니다.
- 이벤트
  - `section_view` 섹션 도달 (section_name), 섹션별 1회
  - `consulting_click` 상담 링크(rubiworkshop.com/models) 클릭 (link_location: header, menu, 섹션 id, footer)
  - `language_switch` 언어 전환 (from, to)
  - `social_click` 인스타그램·카카오·유튜브 클릭 (network, link_location)
  - `image_view` 사진 확대 보기 (gallery)
- GA 관리 > 이벤트에서 `consulting_click`을 주요 이벤트로 표시하면 상담 전환을 따로 볼 수 있습니다.

## 운영시간
루비워크샵 쇼룸 운영시간은 모든 브랜드 사이트에서 월~금 12:00~18:00으로 통일합니다.
