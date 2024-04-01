import subprocess
import os

from Config.Config import Config


class Wav2lipCli:
    @staticmethod
    def wav2lip(audioPath: str, faceVideoPath: str, toPath):
        cmdPath = os.path.join(Config.basePath, 'Shell/wav2lipsh.bat')
        os.system(f'{cmdPath} {faceVideoPath} {audioPath} {toPath}')
        # completedproc = subprocess.run([cmdPath, faceVideoPath, audioPath, toPath])
        # print(f'process finished. code: {completedproc.returncode}')
        pass

    pass

    @staticmethod
    def test():
        audio = 'r:/xTTS_zgr_open1.wav'
        video = r'R:\zgr_video1.mp4'
        to = 'r:/zgr_open1.mp4'
        Wav2lipCli.wav2lip(audio, video, to)

    @staticmethod
    def batchTest():
        i = 0
        inputTemp = r'r:\xTTS_zgr_speech{0}.wav.converted.wav'
        video = r'R:\zgr_video1.mp4'

        while True:
            audio = inputTemp.replace('{0}', str(i))
            if not os.path.exists(audio):
                break
            to = audio + '.mp4'
            Wav2lipCli.wav2lip(audio, video, to)
            i += 1



if __name__ == '__main__':
    # Wav2lipCli.test()
    Wav2lipCli.batchTest()
