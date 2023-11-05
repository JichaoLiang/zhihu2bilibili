import json

import chatgpt
import openai


class LLMUtils:
    @staticmethod
    def quickask(content):
        # openai.api_key = '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'
        openai.api_key = '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'
        obj = [
            {
                "id": "aaa258e0-6028-45b0-bbe0-ecd3dbb848e7",
                "author": {
                    "role": "user"
                },
                "content": {
                    "content_type": "text",
                    "parts": [
                        content
                    ]
                },
                "metadata": {}
            }
        ]
        jsString = json.dumps(obj)
        res = chatgpt.complete(messages=jsString, model='gpt-3.5-turbo')
        print(res)
        pass


if __name__ == "__main__":
    LLMUtils.quickask("hello")
