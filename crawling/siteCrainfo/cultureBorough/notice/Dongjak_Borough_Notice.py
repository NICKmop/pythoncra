import requests
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
from bs4 import BeautifulSoup

class Dongjak_notice:
    def mainCra(cnt):

        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.DONGJAK_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.dongjak.go.kr/portal/bbs/B0000022/list.do?menuNo=200641&pageIndex={}'.format(cnt);
        response = requests.get(url);
        if response.status_code == commonConstant_NAME.STATUS_SUCCESS_CODE:
            html = response.text;
            soup = BeautifulSoup(html, 'html.parser')
            # 타이틀 ,기관, 링크, 등록일, 번호
            link = soup.select('.title > a');
            title = soup.select('.title > a');
            registrationdate = soup.select('td:nth-child(4)');

            # print(registrationdate);
            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.DONGJAK_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                    return Dongjak_notice.mainCra(cnt);
                else:
                    if numberCnt == commonConstant_NAME.NOTICE_STOP_COUNT:
                        break;

                    # print("linkK:::: ", link[i].attrs.get('href'));
                    changeText = str(registrationdate[i].text);
                    firebase_con.updateModel(commonConstant_NAME.DONGJAK_NAME,numberCnt,
                        datasModel.toJson(
                            "https://www.dongjak.go.kr{}".format(link[i].attrs.get('href')),
                            numberCnt,
                            "",
                            title[i].text.strip(),
                            "",
                            registrationdate[i].text,
                            fnChnagetype(changeText.strip()),
                            "동작구청",
                        )
                    );
        else : 
            print(response.status_code)
            