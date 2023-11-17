import json


from Config.Config import Config
from chatglm3.basic_demo.inference import ChatglmClient


class LLMUtils:

    @staticmethod
    def commentFor3qna(question, answer1, answer2, answer3):
        template = f"我会给你一个提问者和三个回答者的对话，请结合提问者的问题，对三个回答者的答案进行一针见血的点评,要求不重复提问者和回答者的叙述，字数少于150字。举例：提问者: '为什么有人嘲笑美国性别很多？'，回答者1：'如果班上有个女生得了癌症，化疗掉光了头发，你会觉得很可怜。但如果有人为了不让这个女生难堪，道德绑架所有人集体剃了光头，你怎么看？'，回答者2：'因为该国最大的宗教明确记载了他们的上帝只创造了两种性别。多出来的95种，如果不是上帝出品，那我建议只能问问撒旦。'，回答者3：'自由世界连嘲笑的自由都没有了吗？'。你点评：第一个把道德绑架形容的淋漓尽致，第二个不知道想表达什么， 第三个，回旋镖打得好！ 下面，我给出正式的问题和三个回答： 提问者: '{question}'，回答者1：'{answer1}'，回答者2：'{answer2}'，回答者3：'{answer3}'"

        response = LLMUtils.askChatGLM3(template)
        return response
        pass

    @staticmethod
    def askChatGLM3(query):
        client = ChatglmClient.getDistance()
        result = client.chatOnce(query)
        return result
        pass


if __name__ == "__main__":
    LLMUtils.quickask("hello")
