import re
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Yangcheon_notice:
    def mainCra(cnt,numberCnt):
        url = 'https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/List.do;jsessionid=hQBUNSnObUA1jLlEVux1s4J1SNRDwXu7lZ6YkRLvSztrEKuMbLgVDg7w93anM7oK.YCWEB_servlet_engine3?cbIdx=254#'.format(cnt);
        soupData = com.pageconnect(cnt, url, "doBbsFPag({});return false;".format(cnt));
        # 타이틀 ,기관, 링크, 등록일, 번호
        
        link = soupData.select('.subject > a');
        title = soupData.select('.subject > a');
        registrationdate = soupData.select('tr > td:nth-child(5)');

        linkCount = len(link) - 1;
        for i in range(len(link)):
            numberCnt += 1;
            if linkCount == i:
                cnt += 1;
                print(commonConstant_NAME.YANGCHEON_BOROUGH_NOTICE," Next Page : {}".format(cnt));
                return Yangcheon_notice.mainCra(cnt, numberCnt);
            else:
                if numberCnt == commonConstant_NAME.STOPCUOUNT:
                    break;
                # print("reg : ", registrationdate[i].text);
                # print("title : ", title[i].text.strip());
                linkAttr = link[i].attrs.get('onclick')
                linkSub = linkAttr.split("(")[1];
                linkSubNt = linkSub.split(")")[0];

                linkSubts = linkSubNt.split(",");
                # print("link : ", linkSubts);
                # replace("'", "")

                firebase_con.updateModel(commonConstant_NAME.YANGCHEON_BOROUGH_NOTICE,numberCnt,
                    datasModel.toJson(
                        "https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/View.do?cbIdx={}&bcIdx={}&parentSeq={}".format(linkSubts[0].replace("'",""), linkSubts[1].replace("'",""), linkSubts[1].replace("'","")),
                        numberCnt,
                        "",
                        title[i].text.strip(),
                        "",
                        registrationdate[i].text,
                        "양천구_공지사항",
                    )
                );
            