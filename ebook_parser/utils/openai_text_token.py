# openai_text_token.py

"""
这段代码采取的方法是调用openai官方的计算token的库“tiktoken”，首先使用这段代码来计算输入文本的token数量，与模型能够承受的最大token数进行比较
如果超过模型能够承受的最大token数量，就删去分组里面的这一段，然后输入到翻译模块进行翻译，反之，没有超过则在分组当中再增加一段，这样既能兼顾API的承受
能力，也能够使得句子的翻译不会被切断。
"""
import logging
import tiktoken

from config.settings import TranslationSettings

# 配置日志
logger = logging.getLogger()

class TextTokenizer:
    def __init__(self):
        self.encoding_name = TranslationSettings.get_default_model()
        self.max_tokens = TranslationSettings.get_max_tokens_for_model(self.encoding_name)
        self.enc = tiktoken.encoding_for_model(self.encoding_name)

    def estimate_tokens(self, text):
        tokens = self.enc.encode(text)
        return len(tokens)

    def group_text_by_tokens(self, text_list):
        grouped_text = []
        current_group = []
        current_tokens = 0
        for text in text_list:
            text_tokens = self.estimate_tokens(text)
            if current_tokens + text_tokens > self.max_tokens:
                grouped_text.append(current_group)
                current_group = []
                current_tokens = 0
            current_group.append(text)
            current_tokens += text_tokens

        if current_group:
            grouped_text.append(current_group)
        logger.info(f"分组完成, 总组数: {len(grouped_text)}")
        return grouped_text

# import tiktoken
#
# # 使用 GPT-3.5-turbo 的编码名称，作为示例
# encoding_name = "gpt-3.5-turbo"
#
# # 获取编码
# enc = tiktoken.encoding_for_model(encoding_name)
#
# # 您的输入文本
# text = ""
#
#
# # 使用编码器计算 token 数量
# tokens = enc.encode(text)
# token_count = len(tokens)
#
# print(token_count)
