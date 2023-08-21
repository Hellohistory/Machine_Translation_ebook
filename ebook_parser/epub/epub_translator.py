import json
import time
from bs4 import BeautifulSoup, NavigableString

from config.settings import TranslationSettings
from translation_module.translation_interface import TranslationInterface
from ebook_parser.text_processing import TextTokenizer

class EPUBTextTranslator:
    def __init__(self, json_input_path, json_output_path, translator: TranslationInterface, max_tokens_for_model):
        self.json_input_path = json_input_path
        self.json_output_path = json_output_path
        self.translator = translator
        self.tokenizer = TextTokenizer(max_tokens_for_model)
        self.max_requests_per_minute = TranslationSettings.get_max_requests_per_minute()  # 从设置中获取最大请求次数
        self.requests_count = 0
        self.start_time = time.time()

    def _check_rate_limit(self):
        if self.requests_count >= self.max_requests_per_minute:
            elapsed_time = time.time() - self.start_time
            if elapsed_time < 60:
                sleep_time = 60 - elapsed_time
                print(f"达到速率限制，将等待 {sleep_time:.2f} 秒")
                time.sleep(sleep_time)
            self.requests_count = 0
            self.start_time = time.time()

    def translate_text(self, source_lang, target_lang):
        with open(self.json_input_path, 'r', encoding='utf-8') as json_file:
            text_data = json.load(json_file)

        translated_data = []
        for item in text_data:
            html_content = item['html_content']
            tag = item['tag']

            # 解析 HTML 内容
            soup = BeautifulSoup(html_content, 'html.parser')

            # 获取所有文本节点
            text_nodes = [text_node for text_node in soup.find_all(text=True) if isinstance(text_node, NavigableString) and text_node.strip()]

            # 将文本节点组合为符合最大token限制的组
            text_groups = self.tokenizer.group_text_by_tokens(text_nodes)  # 使用 TextTokenizer 对象进行分组

            # 遍历文本组并翻译
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
                translated_text = self.translator.translate(text_to_translate, source_lang, target_lang)
                self.requests_count += 1
                print("Translated sentence:", translated_text)  # 打印翻译后的句子

                # 用翻译后的文本替换原始节点
                for original_text_node, (start, end) in zip(group, positions):
                    translated_part = translated_text[start:end]
                    original_text_node.replace_with(translated_part)

            # 保存翻译后的 HTML 内容和标签
            translated_data.append({
                'tag': tag,
                'html_content': str(soup)
            })

        # 将翻译后的文本和标签保存到新的 JSON 文件中
        with open(self.json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(translated_data, json_file, ensure_ascii=False, indent=4)

        print(f"已将翻译后的文本保存到 {self.json_output_path}")

# 以下代码可用于测试，你可以从 translation_services 导入所需的翻译函数
# from translation_services.custom_translator import convert_traditional_to_simplified
# translator = EPUBTextTranslator(json_input_path='extracted_text.json',
#                                 json_output_path='translated_text.json',
#                                 translation_function=convert_traditional_to_simplified, max_tokens_for_model=4096)
# translator.translate_text('zh', 'en')

