import json

from bs4 import BeautifulSoup, NavigableString

from translation_module.translation_interface import TranslationInterface


def estimate_tokens(text):
    return len(text.split())

def group_text_by_tokens(text_list, max_tokens):
    grouped_text = []
    current_group = []
    current_tokens = 0
    for text in text_list:
        text_tokens = estimate_tokens(text)
        if current_tokens + text_tokens < max_tokens:
            current_group.append(text)
            current_tokens += text_tokens
        else:
            grouped_text.append(current_group)
            current_group = [text]
            current_tokens = text_tokens
    if current_group:
        grouped_text.append(current_group)
    return grouped_text

class EPUBTextTranslator:
    def __init__(self, json_input_path, json_output_path, translator: TranslationInterface, max_tokens_for_model):
        self.json_input_path = json_input_path
        self.json_output_path = json_output_path
        self.translator = translator
        self.max_tokens_for_model = max_tokens_for_model

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
            text_groups = group_text_by_tokens(text_nodes, self.max_tokens_for_model)

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

                # 翻译整体文本
                translated_text = self.translator.translate(text_to_translate, source_lang, target_lang)
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

