# text_processing.py

class TextTokenizer:
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    @staticmethod
    def estimate_tokens(text):
        return len(text.split())

    def group_text_by_tokens(self, text_list):
        grouped_text = []
        current_group = []
        current_tokens = 0
        for text in text_list:
            text_tokens = self.estimate_tokens(text)
            if current_tokens + text_tokens < self.max_tokens:
                current_group.append(text)
                current_tokens += text_tokens
            else:
                grouped_text.append(current_group)
                current_group = [text]
                current_tokens = text_tokens
        if current_group:
            grouped_text.append(current_group)
        return grouped_text
