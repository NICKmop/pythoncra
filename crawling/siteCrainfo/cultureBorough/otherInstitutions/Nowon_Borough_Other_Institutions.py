import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Nowon_Institutions:
    def mainCra(cnt,numberCnt):
        url = 'https://www.nowon.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1011';
        soupData = com.pageconnect(cnt, url, "opMovePage({});return false;".format(cnt));
        
        link = soupData.select('.cell-subject > a');
        title = soupData.select('.cell-subject > a');
        registrationdate = soupData.select('tr > td:nth-child(4)');

        linkCount = len(link) - 1;

        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print("Nowon_Institutions Next Page : {}".format(cnt));
                return Nowon_Institutions.mainCra(cnt, numberCnt),
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break; 
            # linkSp = re.sub(r'[^0-9]','',link[i + 1].attrs.get('onclick'));
            linkAttr = link[i].attrs.get('onclick');
            linkSub = linkAttr.split("('")[1];
            linkSubNt = linkSub.split("')")[0];
            firebase_con.updateModel( commonConstant_NAME.NOWON_BOROUGH_OTHER_INSTITUTIONS,numberCnt,
                datasModel.toJson(
                    "https://www.nowon.kr/www/user/bbs/BD_selectBbs.do?q_bbsCode=1011&q_bbscttSn={}&q_rowPerPage=10&q_currPage={}&q_sortName=&q_sortOrder=&q_searchKeyTy=sj___1002&q_searchVal=&".format(linkSubNt,cnt),
                    numberCnt,
                    "",
                    title[i].text.strip(),
                    "",
                    registrationdate[i].text,
                    "노원구_타기관공시송달"
                )
            )
            