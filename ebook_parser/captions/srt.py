# config/logger_config.py

from translation_module.translation_interface import TranslationInterface
from ebook_parser.epub.utils.text_processing import TextTokenizer  # 导入新的 TextTokenizer 类

class SRTTranslator:
    def __init__(self, srt_file_path, translator: TranslationInterface, max_tokens_for_model):
        self.srt_file_path = srt_file_path
        self.translator = translator
        self.tokenizer = TextTokenizer(max_tokens_for_model)  # 创建 TextTokenizer 对象

    def read_srt(self):
        with open(self.srt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    def group_text_by_tokens(self, lines):
        return self.tokenizer.group_text_by_tokens(lines)  # 使用 TextTokenizer 对象进行分组

    def translate_srt(self, source_lang, target_lang):
        lines = self.read_srt()
        text_groups = self.group_text_by_tokens(lines)

        translated_lines = []
        for group in text_groups:
            text_to_translate = ' '.join(group)
            translated_text = self.translator.translate(text_to_translate, source_lang, target_lang)
            print("正在翻译的文本:",translated_text)
            translated_lines.extend(translated_text.split(' '))

        with open('translated.srt', 'w', encoding='utf-8') as out_file:
            out_file.writelines(translated_lines)

        print("SRT文件已翻译！")

# 使用示例:
# translator = SRTTranslator(srt_file_path='path/to/srtfile.srt', translator=your_translation_function, max_tokens_for_model=4096)
# translator.translate_srt('zh', 'en')
