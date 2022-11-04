import re
from common.common_fnc import fnChnagetype
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Seongdong:
    def mainCra(cnt,numberCnt):
        url = 'https://www.sdfac.or.kr/kor/sdfac/board/noti_list.do?gotoMenuNo=06010000';
        soupData = com.pageconnect(cnt, url, "setPage({})".format(cnt));
        
        link = soupData.select('.listType > li > a');
        title = soupData.select('.listType > li > a');
        registrationdate = soupData.select('.writer > li:nth-child(1)');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                # javascript:pageNum('frm01','200');
                cnt += 10;
                print("Seongdong Next Page : {}".format(cnt));
                return Seongdong.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;
            linkSp = re.sub(r'[^0-9]','',link[i].attrs.get('onclick'));
            changeText= str(registrationdate[i].text);

            firebase_con.updateModel( commonConstant_NAME.SEONGDONG_NAME,numberCnt,
                datasModel.toJson(
                    "https://www.sdfac.or.kr/kor/sdfac/board/noti_view.do?page={}&b_idx={}&bbs_id=noti&article_category=&searchCnd=3&searchWrd=".format(cnt , linkSp),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    fnChnagetype(changeText.strip()),
                    "성동문화재단"
                )
            )