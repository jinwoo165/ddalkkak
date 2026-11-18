# 딸깍 · 키캡 스튜디오 2.0

[앱 열기](https://jinwoo165.github.io/ddalkkak/) · [Android](https://jinwoo165.github.io/ddalkkak/?platform=android) · [iPhone](https://jinwoo165.github.io/ddalkkak/?platform=ios)

APK 없이 브라우저에서 사용하는 설치형 웹앱입니다. GitHub Pages는 main 브랜치의 /docs를 게시합니다.

- 모양 16종, 기존 스위치·효과음 19종 보존
- 모양 전용 창작 합성음 16종, 사각사각 5종 추가: 총 40종
- 모양 선택 시 추천 소리 자동 적용, 이후 수동 선택 가능
- 수직·수평 정렬, 배경음악 4곡, 볼륨·음높이·테마·조합 저장
- 최대 30초 타건 녹음, WAV 다운로드, 지원 기기 파일 공유
- 홈 화면 설치, 전체 음원 오프라인 캐시

## 휴대폰

Android: Chrome에서 앱 주소를 열고 메뉴의 앱 설치/홈 화면에 추가를 사용합니다.
iPhone: Safari에서 앱 주소를 열고 공유 → 홈 화면에 추가를 사용합니다.
첫 방문은 인터넷이 필요하며 '오프라인 사용 준비 완료' 표시 이후 오프라인 사용이 가능합니다. 브라우저 저장 공간 정리/운영체제 삭제로 캐시가 사라지면 온라인 재방문이 필요합니다.

아이폰 웹 진동은 지원되지 않습니다. Android도 브라우저·기기 설정에 따라 진동이 제한될 수 있습니다. 소리는 첫 터치 후 시작하며 다른 앱으로 이동하면 음악이 일시정지합니다.
녹음은 마이크가 아닌 앱의 타건 소리만 담습니다. 닫기 전 WAV로 저장하세요. 설정은 기기/브라우저별로 보관됩니다.

## 개발 / 복구

- 실제 배포 코드: docs/index.html, app.js, style.css, install.js, sw.js
- 음원: docs/audio-data.js (타건·창작 묶음), assets/music (기존 4곡)
- 창작음 재생성: Python + numpy/scipy로 scripts/make_sounds.py 실행 후 scripts/bundle_audio.py 실행
- 변경 시 sw.js의 CACHE 버전을 올리고 파일 목록에 새 파일을 포함합니다.
- 재개할 때 PROJECT_STATUS.md부터 확인하고 현재 main과 비교합니다.
- 기존 이미지·음원 출처는 앱의 '미디어 출처'에 보존합니다. 새 합성음은 이 프로젝트에서 생성했습니다.

검증 수준과 남은 실기기 확인은 PROJECT_STATUS.md에 기록합니다.
