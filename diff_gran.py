#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta


def main():
    now = datetime.now() - timedelta(days=1)
    now1 = datetime.now() - timedelta(days=2)
    # now = datetime.now()
    # now1 = datetime.now() - timedelta(days=1)
    today = '%02d%02d' % (now.month, now.day)
    yesterday = '%02d%02d' % (now1.month, now1.day)

    wr = 0
    with open(yesterday) as f:
        for line in f:
            if wr == 1:
                print('    ', line.strip())
            if 'Total' in line:
                print('[어제 %s]--------' % yesterday)
                wr = 1

    print()
    wr = 0
    with open(today) as f:
        for line in f:
            if wr == 1:
                print('    ', line.strip())
            if 'Total' in line:
                print('[오늘 %s]--------' % today)
                wr = 1

    # print('\n[Total]----------')
    # print("전체:", total_cnt)
    # print("중복:", total_cnt - len(result))
    # print("현재:", len(result))
    # print("가격:", p_min/10000, "억 ~", p_max/10000, "억")
    # print("거래완료: ", len(sold_result))
    # print('공인중개사사무소: ', len(real_agent))
    sys.exit(1)


if __name__ == '__main__':
    main()
