# ebook_parser/epub/epub_translator.py

import json
from bs4 import BeautifulSoup
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

            # 使用传入的翻译服务进行翻译
            translated_html_content = self.translator.translate(html_content, source_lang=source_lang,
                                                                target_lang=target_lang)

            # 保存翻译后的 HTML 内容和标签
            translated_data.append({
                'tag': tag,
                'html_content': translated_html_content
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
