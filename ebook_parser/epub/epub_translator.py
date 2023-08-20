# ebook_parser/epub/epub_translator.py

import json
import re

from bs4 import BeautifulSoup, NavigableString
from translation_module.translation_interface import TranslationInterface

class EPUBTextTranslator:
    def __init__(self, json_input_path, json_output_path, translator: TranslationInterface):
        self.json_input_path = json_input_path
        self.json_output_path = json_output_path
        self.translator = translator

    def translate_text(self, source_lang, target_lang):
        with open(self.json_input_path, 'r', encoding='utf-8') as json_file:
            text_data = json.load(json_file)

        translated_data = []
        for item in text_data:
            html_content = item['html_content']
            tag = item['tag']

            # 解析 HTML 内容
            soup = BeautifulSoup(html_content, 'html.parser')

            # 遍历所有的可导航字符串，逐个翻译
            for text_node in soup.find_all(text=True):
                if isinstance(text_node, NavigableString) and text_node.strip():
                    # 使用正则表达式分割句子，保留分隔符
                    sentences = re.split(r'(\s*[.!?]\s*)', text_node.strip())

                    # 逐个翻译句子
                    translated_sentences = []
                    for i in range(0, len(sentences) - 1, 2):
                        sentence = sentences[i] + sentences[i + 1]
                        # 检查句子是否包含字母或数字
                        if sentence.strip() and any(char.isalnum() for char in sentence):
                            print("Translating sentence:", sentence)  # 打印句子
                            translated_sentence = self.translator.translate(sentence, source_lang=source_lang,
                                                                            target_lang=target_lang)
                            print("Translated sentence:", translated_sentence)  # 打印翻译后的句子
                            translated_sentences.append(translated_sentence)
                        else:
                            translated_sentences.append(sentence)  # 保留未翻译的标点或空白字符

                    translated_text = ''.join(translated_sentences)
                    text_node.replace_with(translated_text)

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
#                                 translation_function=convert_traditional_to_simplified)
# translator.translate_text()
