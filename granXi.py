#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from bs4 import BeautifulSoup
from itertools import count
from selenium import webdriver
from re import sub
from decimal import Decimal, InvalidOperation

chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')


def naver_realestate_remove_dups():
    p_min, p_max = 0, 0
    sold_result = set()
    temp_real = dict()
    real_agent = set()
    result = set()
    print('네이버부동산')
    print('신촌그랑자이 매물')
    total_cnt = 0

    # org_url = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=B01&tradeTypeCd=&rletNo=114542&cortarNo=&hscpTypeCd=&mapX=&mapY=&mapLevel=&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=536&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=&exclsSpc=&splySpcR=&cmplYn='
    for i in count(1):
        hscpTypeCd = 'hscpTypeCd=B01%3AB02%3AB0'
        url = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=B01&tradeTypeCd=&rletNo=114542&cortarNo=1144010800&%s3&mapX=&mapY=&mapLevel=&page=%d&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=2397&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=&exclsSpc=&splySpcR=&cmplYn=#_content_list_target' % (hscpTypeCd, i)
        driver = webdriver.Chrome(chromedriver_path)
        # driver = webdriver.PhantomJS()
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
                        try:
                            value = int(Decimal(sub(r'[^\d.]', '', res)))
                            if p_min == 0:
                                p_min = value
                            if p_max == 0:
                                p_max = value
                            if p_min > value:
                                p_min = value
                            if p_max < value:
                                p_max = value
                        except InvalidOperation:
                            continue
                    if idx == 7:
                        infos = '%s' % td.text.split()
                        if infos.find(',') == -1:
                            pos = infos.split('02')
                            rname = '%s,' % pos[0][2:]
                            info = '02%s' % pos[1]
                            # if temp_real[info.replace('[', '').replace(']', '').replace("'", "")] is None:
                            temp_real[info.replace('[', '').replace(']', '').replace("'", "")] = rname
                            # real_info = '%s %s' % (rname, info.replace('[', '').replace(']', '').replace("'", ""))
                        else:
                            infos = '%s' % td.text.split()
                            temp = infos.replace('[', '').replace(']', '').replace("'", "").split(',')
                            temp_real[temp[1]] = temp[0].strip()
                            # real_info = '%s' % (infos.replace('[', '').replace(']', '').replace("'", ""))
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
    print('\n[현재매물]-----------------')
    for r in result:
        print(r)
    print('\n[거래완료]-----------------')
    sold_result = list(sold_result)
    sold_result = sorted(sold_result)
    for r in sold_result:
        print(r)
    for r_phone, r_name in temp_real.items():
        real_info = '%s, %s' % (r_name, r_phone.strip())
        real_agent.add(real_info)
    print('\n[공인중개사사무소]----------')
    real_agent = list(real_agent)
    real_agent = sorted(real_agent)
    for r in real_agent:
        print(r)
    print('\n[Total]----------')
    print("전체:", total_cnt)
    print("중복:", total_cnt - len(result))
    print("현재:", len(result))
    print("가격:", p_min / 10000, "억 ~", p_max / 10000, "억")
    print("거래완료: ", len(sold_result))
    print('공인중개사사무소: ', len(real_agent))
    sys.exit(1)


if __name__ == '__main__':
    naver_realestate_remove_dups()
