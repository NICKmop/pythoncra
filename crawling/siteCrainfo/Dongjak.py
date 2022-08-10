import requests
from bs4 import BeautifulSoup
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel

class Dongjak:
    def mainCra(cnt,numberCnt):

        numberCnt = numberCnt;
        cnt  = cnt; # 1
        url = 'https://www.idfac.or.kr/bbs/board.php?bo_table=notice&page={}'.format(cnt);
        response = requests.get(url);

        if response.status_code == 200:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser');
            
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('tbody > tr > td.td_subject > div > a');
            title = soup.select('tbody > tr > td.td_subject');
            registrationdate = soup.select('tbody > tr > td.td_datetime');

            linkCount = len(link) - 1;
            print("linkCount : ", linkCount);

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print("Next Page : {}".format(cnt));
                    return Dongjak.mainCra(cnt, numberCnt);
                else:
                    # print("title : ", title[i].text.strip());
                    # print(link[i].attrs.get('href'))
                    # print("https://www.gbcf.or.kr/{}".format(link[i].attrs.get('href')));
                    # print("registrationdate : ", registrationdate[i].text);
                    
                    # if "2022-07" in registrationdate[i].text:
                    #     break;
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;
                    
                    # firebase_con.updateModel(commonConstant_NAME.DONGJAK_NAME,numberCnt,
                    #     datasModel.toJson(
                    #         link[i].attrs.get('href'),
                    #         numberCnt,
                    #         "",
                    #         title[i].text.strip(),
                    #         "",
                    #         registrationdate[i].text,
                    #         "금천문화재단",
                    #     )
                    # );
        else : 
            print(response.status_code)