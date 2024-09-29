import openai
import requests

# 设置你的OpenAI API密钥
openai.api_key = 'your-api-key'
openai.base_url="https://api.bianxie.ai/v1"


# 读取要编辑的图片文件
with open('path_to_your_image.png', 'rb') as image_file:
    response = openai.Image.create_edit(
        image=image_file,  # 图像文件
        mask=open('path_to_your_mask_image.png', 'rb'),  # 可选的掩码图像文件
        prompt="将天空变为夜晚，并添加闪烁的星星",  # 编辑指令
        n=1,  # 生成一张图像
        size="1024x1024"  # 图像大小
    )

# 获取并保存生成的图像
image_url = response['data'][0]['url']
response = requests.get(image_url)
if response.status_code == 200:
    with open('edited_image.png', 'wb') as f:
        f.write(response.content)
    print("Edited image saved.")
else:
    print("Failed to download the edited image")