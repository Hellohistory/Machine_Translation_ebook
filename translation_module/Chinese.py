# translation_module/Chinese.py

from translation_module.translation_interface import TranslationInterface
import zhconv

class ChineseTranslator(TranslationInterface):
    def translate(self, text, source_lang, target_lang):
        # 检查是否从繁体中文转换为简体中文
        if source_lang == 'zh-tw' and target_lang == 'zh-cn':
            return zhconv.convert(text, 'zh-cn')
        elif source_lang == 'zh-cn' and target_lang == 'zh-tw':
            return zhconv.convert(text, 'zh-tw')
        else:
            raise ValueError("不支持的语言转换")
