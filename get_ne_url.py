#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys
from bs4 import BeautifulSoup
from itertools import count
from selenium import webdriver


def main():
    if len(sys.argv) < 3:
        print('invalid args: ', len(sys.argv))
        sys.exit(1)
    help_factory = (lambda prog: argparse.RawDescriptionHelpFormatter(prog=prog,
                    max_help_position=28))

    parser = argparse.ArgumentParser(prog='get_ne_url',
                                     fromfile_prefix_chars='@',
                                     formatter_class=help_factory)
    parser.add_argument(
              "-n", "--name", metavar='APT name',
              nargs=1, help="검색할 APT 단지 이름 ")
    chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
    driver = webdriver.Chrome(chromedriver_path)
    # 특정 아파트 정보로 검색
    r_url = get_specific_realestate_naver_url(driver, sys.argv[2])
    if r_url is None:
        print('r_url is None')
        return
    url = 'http://land.naver.com/%s' % r_url
    print(url)
    # try:
    #     driver.find_elements_by_css_selector('//*[@id="sale4_type2"]').click()
    # except Exception as e: 
    #     print(e) driver.quit() return
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    return
    sessions = soup.select('div > div > div > div > a')
    for s in sessions:
        print(s)
    driver.quit()
    return


def get_specific_realestate_naver_url(driver, apt_name):
    url = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=B01&tradeTypeCd=&rletNo=114542&cortarNo=&hscpTypeCd=&mapX=&mapY=&mapLevel=&page=&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=536&bbs_tp_cd=&sort=&siteOrderCode=&schlCd=&tradYy=&exclsSpc=&splySpcR=&cmplYn='

    driver.implicitly_wait(3)
    driver.get(url)
    driver.find_element_by_id('queryInputHeader').send_keys(apt_name)
    # driver.find_element_by_xpath('//*[@id="queryInputHeader"]').click()
    driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div[1]/div/fieldset/a[1]/i').click()

    # cur_url = driver.current_url
    # print(cur_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for tbody in soup.find_all('tbody'):
        for tr in tbody.find_all('tr'):
            for td in tr.find_all('td'):
                return td.a['href']
    return None


if __name__ == '__main__':
    main()
