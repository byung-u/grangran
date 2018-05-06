# grangran
* 신촌그랑자이 네이버 부동산 매물확인 해주는 python3 스크립트
* 이대입구 바로 옆에 있어서 관심이 가는 단지인데 어느 순간 매물이 너무 많아짐
* 많은건 좋은데 중복 매물들이 섞여 있어서 더 보기 어려워짐

# 실행
## requirements
* 2개의 패키지는 따로 설치해주어야함
* `webdriver.PhantomJS()`를 사용하고 있어서 `phantomjs`도 따로 설치해야함
```
from bs4 import BeautifulSoup
from selenium import webdriver
```

## download
* 실행 파일 다운로드
```
% wget -L https://raw.githubusercontent.com/byung-u/grangran/master/granXi.py
```

## execute
* 단순 실행
```
% python3 granXi.py
```

* 실행 결과 클립보드 복사 (stdout to clipboard)
```
% python3 granXi.py | pbcopy
```


# 보여주는 내용
* 네이버 부동산에 등재된 전체 매물
* 매매 중인 물건들 중복 제거한 후 `동`별로 정렬해서 보여줌
* 매매 완료 물건들 중복 제거한 후 `동`별로 정렬해서 보여줌

# 동작 방식
* 네이버 부동산 웹 페이지를 크롤링 수행
* 몇 페이지까지 추가 될지 몰라서 count 모듈을 사용해서 무한대로 돌림
* 조회한 페이지에 매매가 0건이면 break 수행하고 종료

