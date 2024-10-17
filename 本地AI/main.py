# main.py
import gradio as gr
from ai_client import get_models, generate_response
from utils import load_chat_history, save_chat_history
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载聊天历史
chat_history = load_chat_history()
logger.info("Chat history loaded: %s", chat_history)


def chatbot(input_text, model, system_prompt=None, file=None):
    global chat_history
    # 如果有系统提示，添加到聊天历史
    if system_prompt:
        chat_history.append({"role": "system", "content": system_prompt})

    # 添加用户输入到聊天历史
    chat_history.append({"role": "user", "content": input_text})

    # 处理文件上传
    if file is not None:
        image_path = process_file_upload(file)
        chat_history.append({"role": "file", "path": image_path})

    # 获取AI响应
    response = generate_response(model, chat_history)

    # 将AI响应添加到聊天历史
    chat_history.append({"role": "assistant", "content": response})

    # 保存聊天记录
    save_chat_history(chat_history)

    # 返回AI响应
    return response


def process_file_upload(file):
    # 创建临时目录存放上传的文件
    temp_dir = "./temp_files/"
    os.makedirs(temp_dir, exist_ok=True)

    # 获取文件名和扩展名
    filename, ext = os.path.splitext(file.name)

    # 存储文件到临时目录
    filepath = f"{temp_dir}{filename}_{int(time.time())}{ext}"
    with open(filepath, "wb") as f:
        f.write(file.content)

    return filepath

# main.py
...
from gradio.applications import Button

def display_history(history):
    # 在新窗口中显示历史对话
    pass


# 创建一个简单的按钮
def greet():
    return "Hello, World!"

with gr.Blocks() as demo:
    btn = gr.Button("Greet")
    output = gr.Textbox()
    btn.click(fn=greet, outputs=output)

# 启动 Gradio 界面
demo.launch()

iface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.Textbox(label="Your message"),
        gr.Dropdown(choices=models, label="Select AI Model"),
        gr.Textbox(label="System Prompt (Optional)"),
        gr.FileUploader(label="Upload Image or File")
    ],
    outputs=gr.Textbox(label="Response"),
    actions={
        "Display History": Button(fn=display_history, inputs=[gr.InputType.text], outputs=gr.OutputType.NONE),
    }
)

# 获取可用模型列表
models = get_models()
logger.info("Available models: %s", models)

iface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.Textbox(label="Your message"),
        gr.Dropdown(choices=models, label="Select AI Model"),
        gr.Textbox(label="System Prompt (Optional)"),
        gr.FileUploader(label="Upload Image or File")
    ],
    outputs=gr.Textbox(label="Response")
)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    iface.launch()
    logger.info("Gradio interface started.")