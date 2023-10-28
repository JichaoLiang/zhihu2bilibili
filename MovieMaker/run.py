from MovieMaker.CharacterMovieAgent import CharacterMovieAgent
from MovieMaker.MovieMakerAgent import MovieMakerAgent
from MovieMaker.QuestionPicker import QuestionPicker
from MovieMaker.TTSAgent import TTSAgent

def process():
    print('question pick start.')
    QuestionPicker.process()
    print('tts job start.')
    TTSAgent.process()
    print('video character job start.')
    CharacterMovieAgent.process()
    # MovieMakerAgent.process()

if __name__ == '__main__':
    process()