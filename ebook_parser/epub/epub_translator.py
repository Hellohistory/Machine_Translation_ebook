# ebook_parser/epub/epub_translator.py

import json
import logging
import time
from bs4 import BeautifulSoup, NavigableString

from config.settings import TranslationSettings
from ebook_parser.utils.openai_text_token import TextTokenizer
from translation_module.translation_interface import TranslationInterface

# 配置日志
logger = logging.getLogger()

class EPUBTextTranslator:
    def __init__(self, json_input_path, json_output_path, translator: TranslationInterface):
        self.json_input_path = json_input_path
        self.json_output_path = json_output_path
        self.translator = translator
        self.tokenizer = TextTokenizer()  # 不需要传递任何参数
        self.max_requests_per_minute = TranslationSettings.get_max_requests_per_minute()  # 从设置中获取最大请求次数
        self.requests_count = 0
        self.start_time = time.time()

    def _check_rate_limit(self):
        if self.requests_count >= self.max_requests_per_minute:
            elapsed_time = time.time() - self.start_time
            if elapsed_time < 60:
                sleep_time = 60 - elapsed_time
                logger.info(f"达到速率限制，将等待 {sleep_time:.2f} 秒")
                time.sleep(sleep_time)
            self.requests_count = 0
            self.start_time = time.time()

    def translate_text(self, source_lang, target_lang):
        global translated_text
        with open(self.json_input_path, 'r', encoding='utf-8') as json_file:
            text_data = json.load(json_file)

        translated_data = []
        success_count = 0

        logger.info(f"开始翻译，共有 {len(text_data)} 项文本")
        for item in text_data:
            text_tag = item['text_tag']
            html_content = item['html_content']

            # 解析 HTML 内容
            soup = BeautifulSoup(html_content, 'html.parser')

            # 获取所有原始文本节点
            original_text_nodes = [text_node for text_node in soup.find_all(text=True) if
                                   isinstance(text_node, NavigableString) and text_node.strip()]

            # 组合文本节点和 text_tag
            text_nodes = [text_tag + str(text_node) for text_node in original_text_nodes]

            # 将文本节点组合为符合最大token限制的组
            text_groups = self.tokenizer.group_text_by_tokens(text_nodes)  # 使用 TextTokenizer 对象进行分组

            logger.info(f"共有 {len(text_groups)} 组文本进行翻译")
            for group in text_groups:
                # 准备整体文本和位置信息
                text_to_translate = ''
                positions = []
                start_pos = 0
                for text_node in group:
                    text_length = len(text_node)
                    text_to_translate += text_node
                    positions.append((start_pos, start_pos + text_length))
                    start_pos += text_length

                self._check_rate_limit()
                try:
                    translated_text = self.translator.translate(text_to_translate, source_lang, target_lang)
                    success_count += 1
                    # print("Translated sentence:", translated_text)  # 打印翻译后的句子
                except Exception as e:  # 您可以替换为可能的具体异常类型
                    logger.error(f"翻译失败: {e}")

                # 用翻译后的文本替换原始节点
                for original_text_node, (start, end) in zip(original_text_nodes, positions):
                    translated_part = NavigableString(translated_text[start:end].strip())
                    original_text_node.replace_with(translated_part)

            # 替换text_tag中的尖括号为HTML实体
            text_tag = text_tag.replace('<', '&lt;').replace('>', '&gt;')

            # 然后进行替换操作
            translated_html_content = str(soup).replace(text_tag, '')

            # 保存翻译后的 HTML 内容和标签
            translated_data.append({
                'tag': item['tag'],
                'html_content': translated_html_content
            })

        # 将翻译后的文本和标签保存到新的 JSON 文件中
        with open(self.json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(translated_data, json_file, ensure_ascii=False, indent=4)

        logger.info(f"已将翻译后的文本保存到 {self.json_output_path}，成功翻译 {success_count} 组文本")


# 以下代码可用于测试，你可以从 translation_services 导入所需的翻译函数
# from translation_services.custom_translator import convert_traditional_to_simplified
# translator = EPUBTextTranslator(json_input_path='extracted_text.json',
#                                 json_output_path='translated_text.json',
#                                 translation_function=convert_traditional_to_simplified, max_tokens_for_model=4096)
# translator.translate_text('zh', 'en')

