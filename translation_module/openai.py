import json
import openai
import requests

from config.settings import TranslationSettings
from translation_module.translation_interface import TranslationInterface


class OpenAITranslator(TranslationInterface):
    def __init__(self, selected_model, prompt_template, api_key, max_tokens_for_model, api_proxy=None):
        self.api_key = api_key
        self.api_proxy = api_proxy
        self.selected_model = selected_model
        self.prompt_template = prompt_template
        self.max_tokens_for_model = max_tokens_for_model
        self.requests_and_responses = []  # 用于存储所有请求和响应的列表
        openai.api_key = api_key  # 如果你仍然打算在没有代理的情况下使用 openai 库，你可能还需要设置这个属性

        if api_proxy:
            print("正在使用OpenAI API 代理，代理地址为:", self.api_proxy)


    def translate(self, text, source_lang, target_lang):
        # 使用设置中的prompt模板
        prompt = self.prompt_template.format(sentence=text, source_lang=source_lang, target_lang=target_lang)

        # 调用专门的OpenAI方法
        response = self.call_openai(prompt)

        translated_text = response['choices'][0]['message']['content']
        return translated_text

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.requests_and_responses, json_file, ensure_ascii=False, indent=4)

    def call_openai(self, prompt):
        # Prepare the request payload
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
                print("Error calling OpenAI:", response.text)
                raise Exception(response.text)
            response_data = response.json()
        else:
            response_data = openai.ChatCompletion.create(
                model=self.selected_model,
                messages=[{"role": "user", "content": prompt}]
            )

        # 将请求和响应保存到列表中
        self.requests_and_responses.append({
            "request": request_payload,
            "response": response_data
        })

        # 返回响应数据
        return response_data

    def save_requests_and_responses(self):
        self.save_json('utils/requests_and_responses.json')


# 从设置中获取所需的值
selected_model = TranslationSettings.get_default_model()
prompt_template = TranslationSettings.get_default_prompt()
api_key = TranslationSettings.get_api_key()
max_tokens_for_model = TranslationSettings.get_max_tokens_for_model(selected_model)  # 获取最大token数
api_proxy = TranslationSettings.get_api_proxy()

# 初始化翻译器
translator = OpenAITranslator(selected_model, prompt_template, api_key, max_tokens_for_model, api_proxy)  # 这里要传递 max_tokens_for_model

