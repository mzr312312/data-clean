# utils.py
import json
import os


def load_chat_history(file_path='chat_history.json'):
    if not os.path.exists(file_path):
        return []

    # 检查文件是否为空
    if os.path.getsize(file_path) == 0:
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # 如果文件内容不是有效的JSON，则返回空列表
            return []


def save_chat_history(chat_history, file_path='chat_history.json'):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(chat_history, file, indent=4, ensure_ascii=False)

# utils.py
def display_history(history):
    # 在新窗口中显示历史对话
    pass