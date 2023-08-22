# translation_module/translation_service_selector.py

from config.settings import TranslationSettings
from translation_module.Chinese import ChineseTranslator
from translation_module.Youdao import YoudaoTranslator
from translation_module.Openai import OpenAITranslator

"""
这个部分是用来调用服务商的接口，之前存在于input_module文件夹当中，现独立成为新模块
"""

def select_translation_service(provider_choice):
    max_tokens_for_model = float('inf')  # 无限制

    if provider_choice == '1':
        translator_service = ChineseTranslator()
    elif provider_choice == '2':
        selected_model = TranslationSettings.get_default_model()
        prompt_template = TranslationSettings.get_default_prompt()
        api_key = TranslationSettings.get_api_key()
        max_tokens_for_model = TranslationSettings.get_max_tokens_for_model(selected_model)
        api_proxy = TranslationSettings.get_api_proxy()
        translator_service = OpenAITranslator(selected_model, prompt_template, api_key, max_tokens_for_model, api_proxy=api_proxy)
    elif provider_choice == '3':
        translator_service = YoudaoTranslator()
        max_tokens_for_model = 4096
    else:
        print("无效的翻译服务提供商选项。")
        return None, None

    return translator_service, max_tokens_for_model
