# 当前对话内容
dialogue = """

"""

# 统计字符数
char_count = len(dialogue)

# 假设每个中文字符约为0.75个token
token_estimate = char_count * 0.75

print(f"总字符数: {char_count}")
print(f"估计的tokens数量: {token_estimate:.2f}")