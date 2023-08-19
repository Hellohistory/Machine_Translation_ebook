# config/settings.py

class TranslationSettings:
    AVAILABLE_MODELS = [
        "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-3.5-turbo",
        # 其他可用模型
    ]

    DEFAULT_MODEL = "gpt-4"
    DEFAULT_PROMPT = "Please translate the following text from {source_lang} to {target_lang}: {text}"


    # OpenAI的API密钥
    OPENAI_API_KEY = "your-api-key-here"

    @staticmethod
    def get_api_key():
        return TranslationSettings.OPENAI_API_KEY

    @staticmethod
    def get_model_choices():
        return TranslationSettings.AVAILABLE_MODELS

    @staticmethod
    def get_default_model():
        return TranslationSettings.DEFAULT_MODEL

    @staticmethod
    def get_default_prompt():
        return TranslationSettings.DEFAULT_PROMPT
