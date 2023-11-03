import moviepy
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
from moviepy.editor import VideoClip
from moviepy.editor import VideoFileClip

from Config.Config import Config
from MovieMaker.Character import Character
from MovieMaker.Strategy import Strategy
from Scraper.Enums import Status
from Scraper.Enums.Status import taskStatus
from Utils.BaidunetdiskUtils import BaidunetdiskUtils
from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils
from Utils.MovieMakerUtils import MovieMakerUtils


class MovieMakerAgent:
    @staticmethod
    def process():
        db = DBUtils()
        job = [j[0] for j in list(db.fetchMovieMakerJob())]
        voicequeue = []
        currentQna = None
        for task in job:
            datalist = db.fetchVideoChunkList(task)
            questionText =  MovieMakerAgent.getQuestionTextByTaskId(datalist[0][1])
            try:
                MovieMakerAgent.processJobByIdlist(datalist)
                db.setTaskStatus(task, -1, -1, Status.taskStatus.complete)
                db.updateQnaTaskStatusByQuestionText(questionText, status=Status.taskStatus.complete)
                # db.setQnaStatus([task], Status.taskStatus.complete) # 直接回写到qna
            except Exception as ex:
                print(ex)
                db.setTaskStatus(task, -1, -1, Status.taskStatus.failed)
                db.updateQnaTaskStatusByQuestionText(questionText, status=Status.taskStatus.failed)
        db.close()
        # MovieMakerAgent.checkStatus(set(job))
        pass

    @staticmethod
    def processJobByIdlist(datalist):
        # 主持开场
        host = datalist[0]
        filepath = DataStorageUtils.moviePathById(host[3])
        hostCharacter = Character.fromId(host[2])
        hostclip = VideoFileClip(filepath)

        # 主持结束语
        conclusion = datalist[-1]
        conclusionPath = DataStorageUtils.moviePathById(conclusion[3])
        conclustionCharacter = Character.fromId(conclusion[2])
        conclustionClip = VideoFileClip(conclusionPath)

        # 片尾曲
        endpath = Strategy.getEndScenario()
        endClip = None
        if endpath is not None:
            endClip = VideoFileClip(endpath)

        cliplist = []  # VideoFileClip(filepath)
        for row in datalist[1:-1]:
            actorId = row[2]
            actorCharacter = Character.fromId(actorId)
            waitingVideoChunk = actorCharacter.randomVideoByTag(['opening'])
            waitingVideoClip = VideoFileClip(waitingVideoChunk)
            videoChunk = DataStorageUtils.moviePathById(row[3])
            newClip = VideoFileClip(videoChunk)
            cliplist.append((waitingVideoClip, newClip))

        questionText = MovieMakerAgent.getQuestionTextByTaskId(host[1])
        context = {
            "question": questionText,
            "bgm": Strategy.getBGMFile()
        }

        finalClip = MovieMakerAgent.directProduct(hostclip, cliplist, conclustionClip, endClip, context)
        filetext = f'{questionText}.mp4'
        destpath = os.path.join(Config.productPath, filetext)
        finalClip.write_videofile(destpath)
        BaidunetdiskUtils.upload(destpath)
        pass

    @staticmethod
    def getQuestionTextByTaskId(taskid):
        db = DBUtils()
        answers: str = db.getAnswersByTaskstatusId(taskid)[0]
        answerid = answers[0].split(',')[0]
        qna = db.getQnaByAnswerId(answerid)
        question = qna[0][2]
        return question
        pass

    @staticmethod
    def checkStatus(taskIdSet):
        if len(taskIdSet) == 0:
            return
        db = DBUtils()
        job = db.fetchVideoChunk(taskIdSet)
        for taskid in taskIdSet:
            match = [jb for jb in job if jb[1] == taskid]
            if len(match) > 0:
                db.setTaskStatus(taskid, -1, taskStatus.complete, -1)
                db.setQnaStatus([taskid], Status.taskStatus.failed)
        db.close()
        pass

    @staticmethod
    def test():
        hostpath = 'G:/test/host.mp4'
        pathlist = [
            ('G:/test/opening_p.mp4', 'G:/test/1.mp4'),
            ('G:/test/opening_t2.mp4', 'G:/test/2_1.mp4'),
            ('G:/test/opening_o.mp4', 'G:/test/3.mp4')
        ]
        conclusionpath = 'G:/test/conclusion.mp4'
        endpath = 'G:/test/end.mp4'

        output = f'{hostpath}.mp4'

        host = VideoFileClip(hostpath)
        cliplist = [(VideoFileClip(p[0]), VideoFileClip(p[1])) for p in pathlist]
        # debug
        first = cliplist[0]
        truncated = (first[0], first[1].subclip(0, 5))
        cliplist = cliplist[1:]
        cliplist.insert(0, truncated)

        third = cliplist[2]
        truncated = (third[0], third[1].subclip(0, 5))
        cliplist = cliplist[:-1]
        cliplist.append(truncated)

        # debug
        conclusion = VideoFileClip(conclusionpath)
        # debug
        endClip = VideoFileClip(endpath).subclip(0, 3)
        context = {
            'question': '你的亲戚都提过什么过分的要求？',
            'bgm': 'g:/test/Happy Whistling Ukulele.mp3'
        }
        finalClip = MovieMakerAgent.directProduct(host, cliplist, conclusion, endClip, context)
        finalClip.write_videofile(output)
        pass


    @staticmethod
    def predictTotalDuration(hostclip, cliplist, conclusionClip, endClip, openinglatencyseconds):
        duration = hostclip.duration
        for c in cliplist:
            duration += c[1].duration
        duration += 5 * openinglatencyseconds
        duration += conclusionClip.duration
        duration += endClip.duration

        return duration
        pass

    @staticmethod
    def directProduct(hostclip: VideoClip, cliplist, conclusionClip: VideoClip, endClip: VideoClip,
                      context: dict) -> VideoClip:
        openinglatencyseconds = 2

        totallength = MovieMakerAgent.predictTotalDuration(hostclip, cliplist, conclusionClip, endClip,
                                                           openinglatencyseconds)
        print(f'totallength:{totallength}')
        question = context['question']
        bgmClip: AudioFileClip = None
        if context.keys().__contains__('bgm'):
            bgmpath = context['bgm']
            bgmClip = AudioFileClip(bgmpath)

        # bg_colorClip = ImageClip(Config.bgpicPath).resize((1920, 1080)).set_duration(5)
        # composited = CompositeVideoClip([bg_colorClip, titleClip]).set_fps(24)
        # return composited
        print(Config.bgpicPath)
        bgcolorClip = ImageClip(Config.bgpicPath).resize((1920, 1080)).set_duration(totallength)
        # bgcolorClip: ColorClip = ColorClip((1920, 1080), (0, 0, 0)).set_duration(totallength)
        fittedClip = MovieMakerUtils.extendRotateDuration(hostclip.resize((960, 540)).set_position((0, 0)), totallength,
                                                          True)
        hostclip = MovieMakerUtils.captionTextToVideoClip(hostclip, Config.hostspeech.replace('{question}', question))

        titleClip = TextClip(MovieMakerUtils.seperatetextbynewline(question,charcount=10), font=Config.headerfont, color='yellow2',
                             align='center', stroke_color='black', stroke_width=1, fontsize=80 / 1280 * hostclip.size[0], size=hostclip.size)
        titleClip = titleClip.set_duration(2)
        compostedhost = CompositeVideoClip([hostclip, titleClip])
        headlineClip = compostedhost.resize((1920, 1080)).set_position((0, 0)).without_audio()
        toTopLeftHeadline = MovieMakerUtils.animationsTo(headlineClip, [(0, 0), (0, 0)], [(1920, 1080), (960, 540)],
                                                         [3, 1])

        open1: VideoClip = cliplist[0][0]
        open2: VideoClip = cliplist[1][0]
        open3: VideoClip = cliplist[2][0]

        open1 = MovieMakerUtils.extendRotateDuration(open1, totallength, True).resize((960, 540)).set_position(
            (960, 0)).without_audio()
        open2 = MovieMakerUtils.extendRotateDuration(open2, totallength, True).resize((960, 540)).set_position(
            (0, 540)).without_audio()
        open3 = MovieMakerUtils.extendRotateDuration(open3, totallength, True).resize((960, 540)).set_position(
            (960, 540)).without_audio()

        open1_last = open1.subclip(open1.duration - openinglatencyseconds)
        open2_last = open2.subclip(open2.duration - openinglatencyseconds)
        open3_last = open3.subclip(open3.duration - openinglatencyseconds)

        speech1 = cliplist[0][1].resize((960, 540)).set_position((960, 0))  # .subclip(0, 5)  # debug
        speech2 = cliplist[1][1].resize((960, 540)).set_position((0, 540))
        speech3 = cliplist[2][1].resize((960, 540)).set_position((960, 540))

        concated_speech1 = concatenate_videoclips([open1_last, speech1, open1_last], method='compose').set_start(
            hostclip.duration - openinglatencyseconds).resize((960, 540)).set_position((960, 0))
        # return CompositeVideoClip([bgcolorClip, concated_speech1])
        concated_speech2 = concatenate_videoclips([open2_last, speech2, open2_last], method='compose').set_start(
            hostclip.duration + speech1.duration + openinglatencyseconds).resize((960, 540)).set_position((0, 540))
        concated_speech3 = concatenate_videoclips([open3_last, speech3, open3_last], method='compose').set_start(
            hostclip.duration + speech1.duration + speech2.duration + 3 * openinglatencyseconds).resize(
            (960, 540)).set_position((960, 540))

        animate1 = MovieMakerUtils.animationsTo(concated_speech1, [(0, 0), (0, 0), (960, 0)],
                                                [(1920, 1080), (1920, 1080), (960, 540)],
                                                [open1_last.duration, speech1.duration, open1_last.duration])
        animate2 = MovieMakerUtils.animationsTo(concated_speech2, [(0, 0), (0, 0), (0, 540)],
                                                [(1920, 1080), (1920, 1080), (960, 540)],
                                                [open2_last.duration, speech2.duration, open2_last.duration])
        animate3 = MovieMakerUtils.animationsTo(concated_speech3, [(0, 0), (0, 0), (960, 540)],
                                                [(1920, 1080), (1920, 1080), (960, 540)],
                                                [open3_last.duration, speech3.duration, open3_last.duration])

        conclustionSection = concatenate_videoclips(
            [conclusionClip.resize((1920, 1080)), endClip.resize((1920, 1080)).without_audio()],
            'compose')
        conclustionSection = conclustionSection.set_position((0, 0)).resize((960, 540)).set_start(
            hostclip.duration + speech1.duration + speech2.duration + speech3.duration + 5 * openinglatencyseconds)

        conclustionAnimate = MovieMakerUtils.animationsTo(conclustionSection, [(0, 0), (0, 0)],
                                                          [(1920, 1080), (1920, 1080)],
                                                          [1, conclustionSection.duration - 1])

        composited: VideoClip = CompositeVideoClip(
            [bgcolorClip, fittedClip, open1, open2, open3, toTopLeftHeadline, animate1, animate2, animate3,
             conclustionAnimate])
        if bgmClip is not None:
            composited = MovieMakerUtils.setBGM(composited, bgmClip, Config.bgmvol)
        return composited
        pass

    @staticmethod
    def test2():
        videoclip = VideoFileClip('R:\\workspace\\zhihu2bilibili\\Resource\\Data\\Movie\\2023_10\\29\\2023_10_29_19_28_27_786.mp4')
        videoclip = videoclip.resize((1920,1080))
        videoclip.write_videofile('r:/testreadfile.mp4')


if __name__ == '__main__':
    # MovieMakerAgent.test2()
    MovieMakerAgent.process()
    # MovieMakerAgent.test()
