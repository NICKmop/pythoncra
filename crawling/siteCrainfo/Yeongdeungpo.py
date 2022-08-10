import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Yeongdeungpo:
    def mainCra(cnt,numberCnt):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'https://www.ydpcf.or.kr/board.do?bid=1&p={}'.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');

            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-subject > a');
            title = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-subject > a');
            registrationdate = soup.select('ul.board-list-wrap > li > ul.board-body > li.board-date'); # board-date

            linkCount = len(link) - 1;
            print("linkCount : ", linkCount);

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return Yeongdeungpo.mainCra(cnt, numberCnt);
                else:
                    print("title : ", title[i].text.strip());
                    print(link[i].attrs.get('href'))
                    # print("https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')));
                    print("registrationdate : ", registrationdate[i].text.strip().split('|')[1].strip());
                    
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break; 
                    
                    firebase_con.updateModel(commonConstant_NAME.YEONGDEUNGPO_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.ydpcf.or.kr/{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text.strip().split('|')[1].strip(),
                            "영등포문화재단",
                        )
                    );
        else : 
            print(response.status_code)