import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Gangnam_notice:
    def mainCra(cnt):
        
        cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.GANGNAM_NAME);
        numberCnt = max(cntNumber);

        url = 'https://www.gangnam.go.kr/board/B_000001/list.do?mid=ID05_040101';
        soupData = com.pageconnect(cnt, url, "selectPage_func({})".format(cnt));
        
        link = soupData.select('.grid-item > td > a');
        title = soupData.select('.grid-item > td > a');
        registrationdate = soupData.select('.grid-item > td:nth-child(5)');

        print("firebases Nct : {}".format(cnt));

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 1;
                print("Gangnam_notice Next Page : {}".format(cnt));
                return Gangnam_notice.mainCra(cnt),
            else:
                if numberCnt == 40:
                    break;
            linkSp = link[i].attrs.get('href');

            firebase_con.updateModel( commonConstant_NAME.GANGNAM_NAME,numberCnt,
                datasModel.toJson(
                    "https://www.gangnam.go.kr{}".format(linkSp),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "강남구_공지사항"
                )
            )
            