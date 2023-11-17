
class IdType:
    answer:str = 'answer'
    question:str = 'question'
    topic:str = 'topic'
    favorlist:str = 'favorlist'
    relatedquestion:str = 'relatedquestion'
    search:str = 'search'
    baidusearch:str = 'baidusearch'
    fullset = [answer,question,topic,favorlist,relatedquestion, search]

    @staticmethod
    def getType(qid: str):
        for tp in IdType.fullset:
            if qid.startswith(tp):
                return tp
        pass
    @staticmethod
    def convertId(type:str, id)->list:
        return [f'{type}_{id}']

    @staticmethod
    def convertAnswer(questionId:str, answerId:str, remainingRelAnsTest:int=-1):
        id = f'{questionId}_{answerId}'
        if remainingRelAnsTest >= 0:
            id = f'{questionId}_{answerId}_{str(remainingRelAnsTest)}'
        return IdType.convertId(IdType.answer,id)[0]

    @staticmethod
    def convertQuestion(questionId, batch, cursor, sessionId):
        if batch > 0:
            id = f'{questionId}_{batch}_{cursor}_{sessionId}'
        else:
            id = f'{questionId}'
        return IdType.convertId(IdType.question, id)[0]

    @staticmethod
    def stripId(rawId: str):
        return '_'.join(rawId.split('_')[1:])
    @staticmethod
    def stripQuestionTask(rawId: str):
        striped = IdType.stripId(rawId)
        tokens = striped.split('_')
        # not first batch
        if len(tokens) > 1 and tokens[1] != '0':
            qid = tokens[0]
            batch = int(tokens[1])
            cursor = tokens[2]
            sessionId = tokens[3]
        else:
            qid = tokens[0]
            batch = 0
            cursor = ''
            sessionId = ''
        return qid,batch,cursor,sessionId
    pass

