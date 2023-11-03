import argparse
import io
import os
from pathlib import Path

from Config.Config import Config
from MovieMaker.CharacterMovieAgent import CharacterMovieAgent
from MovieMaker.MovieMakerAgent import MovieMakerAgent
from MovieMaker.QuestionPicker import QuestionPicker
from MovieMaker.TTSAgent import TTSAgent
from Utils.DataStorageUtils import DataStorageUtils


def process():
    print('question pick start.')
    QuestionPicker.process()
    print('tts job start.')
    TTSAgent.process()
    print('video character job start.')
    CharacterMovieAgent.process()
    print('moviemaker job start')
    MovieMakerAgent.process()

def start():
    flagfile = Config.stopFlagFilePath
    if Path(flagfile).exists():
        os.remove(flagfile)
    count = 0
    revertprocesslist = [
        MovieMakerAgent.process,
        CharacterMovieAgent.process,
        TTSAgent.process,
        # QuestionPicker.process
    ]
    if not Path(flagfile).exists():
        print('handling unfinished last rotation')
        for i in range(0, len(revertprocesslist)):
            func = revertprocesslist[i]
            func()
    print('start regular process.')
    while not Path(flagfile).exists():
        print(f"rotation {count} started. ")
        count += 1
        process()

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
        start()