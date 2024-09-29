from openai import OpenAI

client = OpenAI(
    # 将这里换成你在便携AI聚合API后台生成的令牌
    api_key="sk-Ilfv84vELSOfknT1Cb827a6eC17843268a3f894f1dE898C7",
    # 这里将官方的接口访问地址替换成便携AI聚合API的入口地址
    base_url="https://api.bianxie.ai/v1"
)
# # 获取所有可用的模型
# models = client.models.list()
#
# # 打印出所有可用的模型
# for model in models.data:
#     print(model.id)

completion = client.chat.completions.create(
    model="chatgpt-4o-latest",
    messages=[
        {
            "role": "user",
            "content": "Who are you",
        }
    ]
)

print(completion.choices[0].message)