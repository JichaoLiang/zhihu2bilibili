import asyncio
import os.path

import edge_tts
import sys

TEXT = sys.argv[1] if len(sys.argv) > 1 else "Hello World!"
VOICE = sys.argv[2] if len(sys.argv) > 2 else "en-GB-SoniaNeural"
OUTPUT_FILE = os.path.abspath('../Resource/Product/dev/tts.wav')

async def _main(TEXT, VOICE) -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

def edgeTTS(text: str, voice: str='en-GB-SoniaNeural', to=OUTPUT_FILE)->str:
    async def process(TEXT: str, VOICE: str) -> None:
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save(to)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(process(text, voice))
    except:
        loop.close()
    return to

if __name__ == "__main__":
    edgeTTS('hello, everyone!')
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(_main(TEXT, VOICE))
    # finally:
    #     loop.close()