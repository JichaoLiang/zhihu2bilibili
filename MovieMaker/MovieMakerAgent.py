import moviepy
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *

from MovieMaker.Character import Character
from MovieMaker.Strategy import Strategy
from Scraper.Enums.Status import taskStatus
from Utils.DBUtils import DBUtils
from Utils.DataStorageUtils import DataStorageUtils


class MovieMakerAgent:
    @staticmethod
    def process():
        db = DBUtils()
        job = [j[0] for j in list(db.fetchMovieMakerJob())]
        voicequeue = []
        currentQna = None
        for task in job:
            datalist = db.fetchVideoChunkList(task)
            MovieMakerAgent.processJobByIdlist(datalist)
        db.close()
        MovieMakerAgent.checkStatus(set([ele[1] for ele in job]))
        pass

    @staticmethod
    def processJobByIdlist(datalist):
        host = datalist[0]
        filepath = DataStorageUtils.moviePathById(host[3])
        hostCharacter = Character.fromId(host)
        hostclip = VideoFileClip(filepath)

        endpath = Strategy.getEndScenario()
        endClip = None
        if endpath is not None:
            endClip = VideoFileClip(endpath)

        cliplist = [] # VideoFileClip(filepath)
        for row in datalist:
            actorId = row[0]
            actorCharacter = Character.fromId(actorId)
            waitingVideoChunk = actorCharacter.randomVideoByTag('opening')
            waitingVideoClip = VideoFileClip(waitingVideoChunk)
            videoChunk = DataStorageUtils.getPathById(row[3])
            newClip = VideoFileClip(videoChunk)
            cliplist.append((waitingVideoClip,newClip))
        MovieMakerAgent.directProduct(hostclip, cliplist, endClip)
        pass

    @staticmethod
    def checkStatus(taskIdSet):
        db = DBUtils()
        job = db.fetchVideoChunk(taskIdSet)
        for taskid in taskIdSet:
            match = [jb for jb in job if jb[1]==taskid]
            if len(match[3]) > 0:
                db.setTaskStatus(taskid,-1, taskStatus.complete, -1)
        db.close()
        pass
    @staticmethod
    def test():
        pass

    @staticmethod
    def directProduct(hostclip:VideoFileClip, cliplist, endClip:VideoFileClip):
        startupduration = hostclip.duration
        pass


if __name__ == '__main__':
    MovieMakerAgent.test()