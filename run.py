import argparse
import io
import os
from pathlib import Path

from Config.Config import Config
from MovieMaker.CharacterMovieAgent import CharacterMovieAgent
from MovieMaker.MovieMakerAgent import MovieMakerAgent
from MovieMaker.QuestionPicker import QuestionPicker
from MovieMaker.TTSAgent import TTSAgent
from Scraper import zhihu
from Utils.BaidunetdiskUtils import BaidunetdiskUtils
from Utils.DataStorageUtils import DataStorageUtils


def process(tagmark=Config.defaultTagmark):
    if testStop():
        return
    print('question pick start.')
    picked = QuestionPicker.processTag(tagmark)
    if picked == 0:
        return 0
    if testStop():
        return 0
    print('tts job start.')
    TTSAgent.process()
    if testStop():
        return 0
    print('video character job start.')
    CharacterMovieAgent.process()
    if testStop():
        return 0
    print('moviemaker job start')
    MovieMakerAgent.process()
    return picked


def testStop():
    flagfile = Config.stopFlagFilePath
    return Path(flagfile).exists()


def start():
    flagfile = Config.stopFlagFilePath
    if Path(flagfile).exists():
        os.remove(flagfile)
    count = 0
    revertprocesslist = [
        TTSAgent.process,
        CharacterMovieAgent.process,
        MovieMakerAgent.process,
        # QuestionPicker.process
    ]
    if not Path(flagfile).exists():
        print('handling unfinished last rotation')
        for i in range(0, len(revertprocesslist)):
            func = revertprocesslist[i]
            if testStop():
                return
            func()
    print('start regular process.')
    while not Path(flagfile).exists():
        print(f"rotation {count} started. ")
        print('handle search data first.')
        startSearch()
        count += 1
        process()

def startSearchSingle(tagmark='bingsearchkeyword'):
    # tagmark = 'bingsearchkeyword'
    flagfile = Config.stopFlagFilePath
    if Path(flagfile).exists():
        os.remove(flagfile)
    count = 0
    # revertprocesslist = [
    #     TTSAgent.process,
    #     CharacterMovieAgent.process,
    #     MovieMakerAgent.process,
    #     # QuestionPicker.process
    # ]
    # if not Path(flagfile).exists():
    #     print('handling unfinished last rotation')
    #     for i in range(0, len(revertprocesslist)):
    #         func = revertprocesslist[i]
    #         if testStop():
    #             return
    #         func()
    print('scraping keywords')
    keywords = [tagmark]
    zhihu.processSearchKeywords(keywords, tagmark)
    print('start regular process.')
    while not Path(flagfile).exists():
        print(f"rotation {count} started. ")
        count += 1
        process(tagmark)

def startSearch():
    # tagmark = 'bingsearchkeyword'
    flagfile = Config.stopFlagFilePath
    if Path(flagfile).exists():
        os.remove(flagfile)
    count = 0
    print('scraping keywords')
    keywords = BaidunetdiskUtils.popSearchTaskQueue()
    if len(keywords) == 0:
        return
    tagmark = keywords[0]
    zhihu.processSearchKeywords(keywords, tagmark)
    print('start regular process.')
    while not Path(flagfile).exists():
        print(f"rotation {count} started. ")
        count += 1
        picked = process(tagmark)
        if picked == 0:
            break


def stop():
    flagfile = Config.stopFlagFilePath
    open(flagfile, 'w').close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inference code to zhihu2bilibili')
    parser.add_argument('--StartOrStop', type=str, default='start',
                        help='start or stop')
    args = parser.parse_args()
    if str(args.StartOrStop).lower() == 'stop':
        print('stop process begin.')
        stop()
        print('done')
    else:
        print('start process.')
        # startSearch('search20231124')
        # process('search20231125')
        start()
