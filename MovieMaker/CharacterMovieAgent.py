from MovieMaker import TTS
from Scraper.Enums.Status import taskStatus
from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils

class CharacterMovieAgent:
    @staticmethod
    def process():
        db = DBUtils()
        job = db.fetchTTSJob()
        for jobEntry in job:
            id = jobEntry[0]
            voiceName = jobEntry[4]
            textChunk = jobEntry[5]
            wavId, destpath = DataStorageUtils.generateVoicePathId()
            TTS.edgeTTS(textChunk,voiceName,destpath)
            db.updateVoicePath(id, wavId)
        db.close()
        TTSAgent.checkStatus(set([ele[1] for ele in job]))
        pass

    @staticmethod
    def checkStatus(taskIdSet):
        db = DBUtils()
        job = db.fetchTTSJob()
        for taskid in taskIdSet:
            match = [jb for jb in job if jb[1]==taskid]
            if len(match) == 0:
                db.setTaskStatus(taskid,taskStatus.complete, -1, -1)
        db.close()
        pass


if __name__ == '__main__':
    # result = TTSAgent.splitText('⒈青菜焯水的时候，待水烧开，水中加入油，不需要太多，然后再下入青菜烫熟。这样焯水的青菜不会变色，而且表面因为有油的效果，会显得青翠、明亮。  ⒉糖在菜肴中起到的效果不只是增加甜度。在做一些辣的菜时，放一些糖可以起到中和辣味使辣变得柔和，增加味道上的层次感。还可以起到提鲜的效果。  ⒊肉类焯水一般都是冷水下锅，比如家庭中经常吃的牛羊猪肉等皆是如此。冷水下锅可以有效的去除肉类本身的异味，如果开水下锅的话，会把杂质、血沫等使肉类腥臊的物质封堵在内部无法溢出。  ⒋炖汤所用到鸡肉焯水时，则需要水开后下锅，时间不宜过长，避免鲜味流失。  ⒌料酒在炒菜中的作用是去腥，但是使用时需要注意两点：  ①料酒要“烹”，即锅要热，能瞬间使酒的味道激发出来，而不是料酒倒进去之后跟加了凉水一样，锅中没有一点反应。  ②料酒不要多。  以上两点不注意，菜品中会有一股酒臭味窝在其中，从而毁掉整道菜。  ⒍善于使用鸡粉、鸡精、味精、味粉等以提鲜为主的调料，能够使菜品的味道更上一个层次。  不需要理会“味精有害论”，任何调味料如果不适量使用，用多了都有害。盐每天也有一个建议用量，总没见过有人做菜不放盐的吧？  也不需要理会“味精大厨论”，他们认为外面做菜就是靠多加味精。味精和盐、糖、酱油等等一样，盐加多了会咸，糖加多了会腻，酱油加多了会齁，味精加多了也会苦，调料的用法用量就跟抓药时君臣佐使的配比一样，不是单靠死命的加什么就能让菜变得好吃。  ⒎学会上浆。肉类，家庭常吃的肉丝、肉片等，想要使肉的口感嫩滑，要学会如何上浆，上浆并不单单只是放淀粉，也不只是放蛋清。想要肉吃起来嫩滑，还需要肉的内部有一定的水分存在。如果肉本身就很干，外面包裹的壳子再厚，也达不到很嫩的效果。  肉类在码味之后，这个时候不要急于放入淀粉，先加一点水，顺着一个方向搅拌，让水吸进肉里，然后再加一点水，继续搅拌，重复多次。  直到肉的表面看起来水汪汪的，然后再下入淀粉搅匀，一般在家里做，不需要再放蛋清，浪费。最后在倒一点油，主要的作用是在滑油的时候方便肉散开，否则很容易沾在一起，变成“坨坨”肉。')
    # print(result)
    TTSAgent.process()