import os

from transformers import AutoTokenizer, AutoModel

from Config.Config import Config


class ChatglmClient:
    distance = None
    @staticmethod
    def getDistance():
        if ChatglmClient.distance is None:
            ChatglmClient.distance = ChatglmClient()
        return ChatglmClient.distance

    @staticmethod
    def clearDistance():
        del ChatglmClient.distance

    def __init__(self):
        model_path = Config.glmModelPath
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(4).cuda()
        self.model.eval()

    def chatOnce(self, query):
        past_key_values, history = None, []
        responseText = ''
        for response, history, past_key_values in self.model.stream_chat(self.tokenizer, query, history=history,
                                                                         past_key_values=past_key_values,
                                                                         return_past_key_values=True):
            responseText = response
        return response

    def chatSequence(self, query, past, history):
        past_key_values, historylist = past, history
        responseText = ''
        for response, history, past_key_values in self.model.stream_chat(self.tokenizer, query, history=history,
                                                                         past_key_values=past_key_values,
                                                                         return_past_key_values=True):
            responseText = response

        return responseText, past_key_values, historylist

    pass

if __name__ == '__main__':
    client = ChatglmClient.getDistance()
    response = client.chatOnce("你好，你是谁？")
    print(response)