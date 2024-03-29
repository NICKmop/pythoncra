import re
from common.common_fnc import fnChnagetype
from common.common_fnc import fnCompareTitle
from dbbox.firebases import firebase_con
from common.common_constant import commonConstant_NAME
from models.datasModel import datasModel
import common.common_fnc  as com

class Sbaseoul:
    def mainCra(cnt):
        try:
            cntNumber = firebase_con.selectModelKeyNumber(commonConstant_NAME.SEOUL_NAME);
            numberCnt = max(cntNumber);
            
            url = 'https://www.sba.seoul.kr/Pages/CustomerCenter/Notice.aspx';
            soupData = com.pageconnect(cnt, url, "javascript:pageMove('{}')".format(cnt));
            
            link = soupData.select('.undefined');
            title = soupData.select('.undefined');
            registrationdate = soupData.select('tr > td:nth-child(3)');

            linkCount = len(link) - 1;

            for i in range(len(link)):
                numberCnt += 1;
                if linkCount == i:
                    cnt += 1;
                    print(commonConstant_NAME.SBASEOUL_NAME,"Next Page : {}".format(cnt));
                    # return Sbaseoul.mainCra(cnt),
                else:
                    # if numberCnt == commonConstant_NAME.SEOUL_STOP_COUNT_FIVE:
                    #     break;
                    changeText= str(registrationdate[i].text);

                    if(fnCompareTitle(commonConstant_NAME.SEOUL_NAME, title[i].text.strip(), changeText) == 1):
                        break;

                    linkAttr = link[i].attrs.get('onclick');
                    if(linkAttr == None):
                        numberCnt -=1;
                    if(linkAttr != None):
                        linkSub = linkAttr.split("(")[1];
                        linkSubNt = linkSub.split(")")[0];
                        linkSubts = linkSubNt.split(",");

                        firebase_con.updateModel( commonConstant_NAME.SEOUL_NAME,numberCnt,
                            datasModel.toJson(
                                "https://www.sba.seoul.kr{}".format(linkSubts[0].replace('"','')),
                                numberCnt,
                                "",
                                title[i].text.strip(),
                                "",
                                fnChnagetype(changeText.strip()),
                                "서울산업진흥원"
                            )
                        )
        except (ValueError, TypeError, TimeoutError, ConnectionError) as e:
            raise ValueError("Argument에 잘못된 값이 전달되었습니다.")