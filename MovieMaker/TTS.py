import asyncio
import os.path
from pathlib import Path

import edge_tts
import sys

from Config.VoiceModel import VoiceModel
from Utils.CommonUtils import CommonUtils

TEXT = sys.argv[1] if len(sys.argv) > 1 else "Hello World!"
VOICE = sys.argv[2] if len(sys.argv) > 2 else "en-GB-SoniaNeural"
OUTPUT_FILE = os.path.abspath('../Resource/Product/dev/tts.wav')


async def _main(TEXT, VOICE) -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)


def edgeTTS(text: str, voice: str = 'en-GB-SoniaNeural', to=OUTPUT_FILE) -> str:
    async def process(TEXT: str, VOICE: str) -> None:
        communicate = edge_tts.Communicate(TEXT, VOICE)
        dir = os.path.dirname(to)
        if not Path(dir).exists():
            os.makedirs(dir)
        await communicate.save(to)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(process(text, voice))
    except Exception as e:
        print(str(e))
        loop.close()
        raise e
    return to


def getVoices():
    voicesList = asyncio.get_event_loop().run_until_complete(edge_tts.list_voices())
    result = [
        {
            'Locale': voice['Locale'],
            'Gender': voice['Gender'],
            'ShortName': voice['ShortName'],
            'FriendlyName': voice['FriendlyName'],
        } for voice in voicesList if voice['Locale'].lower().startswith('zh-')
    ]
    return result


if __name__ == "__main__":
    # voices = getVoices()
    # CommonUtils.saveList([str(v) for v in voices], 'g:\\voicelist.json')
    for i in range(0, len(VoiceModel.voicelist)):
        edgeTTS(
            '大家好，欢迎来到今天的直播！我是您的数字虚拟主播，为您带来一份令人兴奋的招聘信息。如果你对摄影和摄像充满热情，那么请务必继续关注，因为我们正在寻找一位全职摄影/摄像师！这个岗位有很多精彩的工作职责，让我们一一来看看：首先，作为一名摄影/摄像师，您将负责人像摄影的拍摄工作。您的任务是根据客户的需求，捕捉每一个精彩瞬间，并确保拍摄效果符合要求。这需要您对人像摄影有丰富的经验和深入的理解，以及审美在线！除了拍摄，您还将参与拍摄项目的策划和执行。这意味着您将有机会发挥创造力，为每个项目带来独特的视觉体验。当然，为了确保拍摄顺利进行，您需要负责摄影设备的维护和管理，以确保设备的正常运行。同时，您还将参与后期制作工作，对拍摄素材进行整理和处理，以达到最佳效果。在这个团队中，团队合作精神至关重要。您将与其他团队成员密切合作，以保证项目的顺利进行。因此，具备良好的沟通与协调能力也是必不可少的技能。岗位还有一些具体的要求，如吃苦耐劳的精神、熟练操作各类摄影设备、熟悉后期制作软件等等。而且，我们希望您具备创新思维和敏锐的观察力，能够捕捉到拍摄时的瞬间美，并且是一名踏实认真、诚实可靠、有责任心的职业人员。当然，我们也会给予您丰厚的福利待遇，包括具有竞争力的薪资和福利、良好的工作环境和发展空间、培训机会，以及出差津贴和相关费用报销。其他福利待遇将根据您的个人能力和绩效进行综合考虑。如果您对这个岗位感兴趣，并且认为自己符合要求，那么不要犹豫，赶快提交您的申请吧！这是一个充满挑战和机会的职位，期待您的加入，一起创造精彩的摄影和摄像作品！感谢大家的收看，我们下次再见！'
            , VoiceModel.voicelist[i]['ShortName'], f"r:\\output_{i}.wav")
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(_main(TEXT, VOICE))
    # finally:
    #     loop.close()
