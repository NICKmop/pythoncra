import requests
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Guro_Institutions:
    def mainCra(cnt,numberCnt):
        url = 'https://www.guro.go.kr/www/selectBbsNttList.do?bbsNo=669&&pageUnit=10&key=1804&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.p-subject > a');
            title = soup.select('.p-subject > a');
            registrationdate = soup.select('td:nth-child(4)');
            
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.GURO_BOROUGH_OTHER_INSTITUTIONS," Next Page : {}".format(cnt));
                    return Guro_Institutions.mainCra(cnt, numberCnt);
                else:
                    if numberCnt == commonConstant_NAME.STOPCUOUNT:
                        break;

                    # print(link[i].attrs.get('href'));
                    
                    firebase_con.updateModel(commonConstant_NAME.GURO_BOROUGH_OTHER_INSTITUTIONS,numberCnt,
                        datasModel.toJson(
                            "https://www.gangseo.seoul.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            "구로구_타기관공시송달",
                        )
                    );
        else : 
            print(response.status_code)
            