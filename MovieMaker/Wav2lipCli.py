import subprocess
import os


class Wav2lipCli:
    @staticmethod
    def wav2lip(audioPath: str, faceVideoPath: str, toPath):
        cmdPath = os.path.abspath('../Shell/wav2lipsh.bat')
        os.system(f'{cmdPath} {faceVideoPath} {audioPath} {toPath}')
        # completedproc = subprocess.run([cmdPath, faceVideoPath, audioPath, toPath])
        # print(f'process finished. code: {completedproc.returncode}')
        pass

    pass

    @staticmethod
    def test():
        audio = 'g:\\shortsample_shanxi.wav'
        video = 'D:/MyWork/data/sucai/dushuai/talk.mp4'
        to = 'r:/shuai.mp4'
        Wav2lipCli.wav2lip(audio, video, to)


if __name__ == '__main__':
    Wav2lipCli.test()
