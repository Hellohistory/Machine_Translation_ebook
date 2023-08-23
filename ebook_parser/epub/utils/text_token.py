# text_token.py

import tiktoken
from config.logger_config import setup_logger
from config.settings import TranslationSettings

logger = setup_logger()

class TextTokenizer:
    def __init__(self, model_name):
        self.encoding_name = model_name
        self.max_tokens = TranslationSettings.get_max_tokens_for_model(model_name)
        self.enc = tiktoken.encoding_for_model(self.encoding_name)

    def estimate_tokens(self, text):
        tokens = self.enc.encode(text)
        return len(tokens)

    def group_text_by_tokens(self, text_list):
        grouped_text = []
        current_group = []
        current_tokens = 0
        for text in text_list:
            text_tokens = self.estimate_tokens(text) # 调用已修改的实例方法
            logger.info(f"处理文本: '{text[:30]}...', token 数量: {text_tokens}, 当前组 token 总数: {current_tokens}")
            if current_tokens + text_tokens <= self.max_tokens:
                current_group.append(text)
                current_tokens += text_tokens
            else:
                logger.info(f"新组开始, 当前组 token 总数: {current_tokens}")
                grouped_text.append(current_group)
                current_group = [text]
                current_tokens = text_tokens
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
