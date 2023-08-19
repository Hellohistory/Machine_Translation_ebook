# translation_module/translation_interface.py

from abc import ABC, abstractmethod

class TranslationInterface(ABC):
    @abstractmethod
    def translate(self, text, source_lang, target_lang):
        """
        翻译给定的文本从源语言到目标语言。

        :param text: 要翻译的文本
        :param source_lang: 源语言代码
        :param target_lang: 目标语言代码
        :return: 翻译后的文本
        """
        pass
