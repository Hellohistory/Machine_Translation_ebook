import openai

from config.settings import TranslationSettings
from translation_module.translation_interface import TranslationInterface


class OpenAITranslator(TranslationInterface):
    def __init__(self, selected_model, prompt_template, api_key):
        self.selected_model = selected_model
        self.prompt_template = prompt_template
        openai.api_key = api_key

    def translate(self, text, source_lang, target_lang):
        # 使用设置中的prompt模板
        prompt = self.prompt_template.format(text=text, source_lang=source_lang, target_lang=target_lang)

        # 调用专门的OpenAI方法
        response = self.call_openai(prompt)

        translated_text = response.choices[0].text
        return translated_text

    def call_openai(self, prompt):
        return openai.Completion.create(
            model=self.selected_model,
            prompt=prompt
        )

# 从设置中获取所需的值
selected_model = TranslationSettings.get_default_model()
prompt_template = TranslationSettings.get_default_prompt()
api_key = TranslationSettings.get_api_key()

# 初始化翻译器
translator = OpenAITranslator(selected_model, prompt_template, api_key)
