# translation_module/Openai.py

import json
import logging

import openai
import requests


from config.settings import TranslationSettings
from translation_module.translation_interface import TranslationInterface

# 配置日志
logger = logging.getLogger()




class OpenAITranslator(TranslationInterface):
    def __init__(self, selected_model, prompt_template, api_key, max_tokens_for_model, api_proxy=None):
        self.api_key = api_key
        self.api_proxy = api_proxy
        self.selected_model = selected_model
        self.prompt_template = prompt_template
        self.max_tokens_for_model = max_tokens_for_model
        self.requests_and_responses = []  # 用于存储所有请求和响应的列表
        openai.api_key = api_key

        if api_proxy:
            logger.info(f"正在使用OpenAI API 代理，代理地址为: {self.api_proxy}")

    def translate(self, text, source_lang, target_lang):
        logger.info("开始翻译文本")
        prompt = self.prompt_template.format(sentence=text, source_lang=source_lang, target_lang=target_lang)
        response = self.call_openai(prompt)
        translated_text = response['choices'][0]['message']['content']
        logger.info("完成翻译文本")
        return translated_text

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.requests_and_responses, json_file, ensure_ascii=False, indent=4)

    def call_openai(self, prompt):
        logger.info(f"准备调用 OpenAI API，模型为: {self.selected_model}")
        request_payload = {
            "model": self.selected_model,
            "messages": [{"role": "user", "content": prompt}]
        }

        if self.api_proxy:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            response = requests.post(f"{self.api_proxy}/v1/chat/completions", json=request_payload, headers=headers)
            if response.status_code != 200:
                logger.error(f"调用 OpenAI API 出错: {response.text}")
                raise Exception(response.text)
            response_data = response.json()
        else:
            response_data = openai.ChatCompletion.create(
                model=self.selected_model,
                messages=[{"role": "user", "content": prompt}]
            )

        self.requests_and_responses.append({
            "request": request_payload,
            "response": response_data
        })

        logger.info(f"成功调用 OpenAI API，翻译结果为: {response_data}")

        return response_data

    def save_requests_and_responses(self):
        self.save_json('utils/requests_and_responses.json')


# 从设置中获取所需的值
selected_model = TranslationSettings.get_default_model()
prompt_template = TranslationSettings.get_default_prompt()
api_key = TranslationSettings.get_api_key()
max_tokens_for_model = TranslationSettings.get_max_tokens_for_model(selected_model)
api_proxy = TranslationSettings.get_api_proxy()

# 初始化翻译器
translator = OpenAITranslator(selected_model, prompt_template, api_key, max_tokens_for_model, api_proxy)
