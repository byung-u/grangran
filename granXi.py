#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
from itertools import count
from selenium import webdriver


def naver_realestate_remove_dups():
    sold_result = set()
    result = set()
    print('네이버부동산')
    print('신촌그랑자이 매물')
    total_cnt = 0

    for i in count(1):
        hscpTypeCd = 'hscpTypeCd=B01%3AB02%3AB0'
        url = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=B01&tradeTypeCd=&rletNo=114542&cortarNo=1144010800&%s3&mapX=&mapY=&mapLevel=&page=%d&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=2397&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=&exclsSpc=&splySpcR=&cmplYn=#_content_list_target' % (hscpTypeCd, i)
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(3)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cnt = 0
        for tbody in soup.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                is_sold = None
                detail_info = None
                for idx, td in enumerate(tr.find_all('td')):
                    if idx == 1:
                        cnt += 1
                        try:
                            mark = td.find('span')
                            try:
                                img = mark.find('img')
                                is_sold = '%s' % (img['alt'])
                            except AttributeError:
                                pass
                            except (KeyError, TypeError):
                                print('error')
                                break
                        except (KeyError, TypeError):
                            print('error')
                            break
                    if idx == 3:
                        room_size = td.text.strip().split()
                        res = '%sm²' % (room_size[0])
                        detail_info = '%s' % res
                    if idx == 4:
                        res = '%s' % td.text.strip()
                        detail_info = '%s %s' % (res, detail_info)
                    if idx == 5:
                        res = '%s층' % td.text.strip()
                        detail_info = '%s %s' % (detail_info, res)
                    if idx == 6:
                        res = '%s' % td.text.strip()
                        temp = res.split('\n')
                        detail_info = '%s %s' % (detail_info, temp[0])
                # print(is_sold)
                # print(detail_info)
                if detail_info is None:
                    continue
                if is_sold is None:
                    result.add(detail_info)
                    continue
                if is_sold.startswith('확'):  # 확인한지 1개월 이내인 매물
                    result.add(detail_info)
                else:  # 거래가 완료된 매물
                    sold_result.add(detail_info)
        if cnt == 0:
            break
        total_cnt += cnt
    result = list(result)
    result = sorted(result)
    print('[현재매물]-----------------')
    for r in result:
        print(r)
    print('[거래완료]-----------------')
    sold_result = list(sold_result)
    sold_result = sorted(sold_result)
    for r in sold_result:
        print(r)
    print("\n네이버 전체 매물 : ", total_cnt)
    print("현재매물: ", len(result))
    print("거래완료: ", len(sold_result))
    sys.exit(1)


if __name__ == '__main__':
    naver_realestate_remove_dups()
