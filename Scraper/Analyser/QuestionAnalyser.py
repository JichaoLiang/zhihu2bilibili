from bs4 import BeautifulSoup
import os
import json
import munch

from Utils import CommonUtils
from Scraper.Enums.IdType import IdType

# target url sample
# https://www.zhihu.com/api/v4/questions/323196827/feeds?cursor=6373e526e230cdec97899bab490e96b9&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1695782144302186399
class QuestionAnalyser():
    maxbatch = 4
    @staticmethod
    def buildRequestURL(id)->str:
        qid, batch, cursor, sessionId = IdType.stripQuestionTask(IdType.convertId(IdType.question, id)[0])
        # not first batch
        if batch != 0 and cursor != '' and sessionId !='':
            return f'https://www.zhihu.com/api/v4/questions/{qid}/feeds?cursor={cursor}&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=20&offset=0&order=default&platform=desktop&session_id={sessionId}'
        else:
            return f'https://www.zhihu.com/api/v4/questions/{qid}/feeds?cursor=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=20&offset=0&order=default&platform=desktop&session_id='
        pass
    @staticmethod
    def extractAndDiscover(dataStr: str, taskId: str):
        # extract
        jsonobj = json.loads(dataStr)
        # discover
        data = jsonobj['data']
        title = ''
        if len(data) > 0:
            question = CommonUtils.CommonUtils.tryFetch(data[0], ['target', 'question'])
            id = CommonUtils.CommonUtils.tryFetch(question, ['id'])
        answerlist = [CommonUtils.CommonUtils.tryFetch(item, ['target', 'id']) for item in data]
        lastcursor =  CommonUtils.CommonUtils.tryFetch(data[-1], ['cursor'])
        sessionId = CommonUtils.CommonUtils.tryFetch(jsonobj, ['session', 'id'])
        qid,batch,a,b = IdType.stripQuestionTask(taskId)
        nextbatch = batch + 1
        if batch > QuestionAnalyser.maxbatch:
            nextbatch = -1
        # no next batch
        if sessionId == '' or lastcursor == '':
            nextbatch = -1
        return munch.DefaultMunch.fromDict({
            'questionId': id,
            'answeridlist': answerlist,
            'sessionid':sessionId,
            'lastcursor':lastcursor,
            'batch': nextbatch
        })
        pass

    @staticmethod
    def test():
        path = os.path.abspath('../../')
        html = os.path.join(path, 'resource/questionfeed.json')
        with open(html,encoding='utf-8') as f:
            lines = f.readlines()
            htmlStr = ''.join(lines)
        result = QuestionAnalyser.extractAndDiscover(htmlStr)
        print(result)
        pass

    pass


if __name__ == '__main__':
    QuestionAnalyser.test()