from pydub import AudioSegment
class AudioUtils:
    @staticmethod
    def concatewavlist(wavlist:list, toPath:str):
        result = None
        for wavPath in list:
            seg = AudioSegment.from_file(wavPath)
            if result is None:
                result = seg
            else:
                result += seg
        result.export(toPath, format='wav')
    pass