# 假设输入的代码是一个字符串，每行一个代码
input_data = """
SJ-V-05-000D-GD-0112_PR01_F
SJ-V-05-000D-GD-0119_PR04_F
SJ-V-05-000D-GD-0231_PR01_F

"""

# 将输入数据按行分割
input_codes = input_data.strip().split('\n')

# 打印输出的格式
print("tagCodes = [")
for code in input_codes:
    print(f'    "{code}",')
print("]")
