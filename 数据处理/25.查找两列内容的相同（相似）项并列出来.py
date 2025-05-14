import os
import pandas as pd
from datetime import datetime

# 输入文件的绝对路径
input_path = r"D:\PycharmProjects\PY\数据处理\25.查找两列内容的相同（相似）项并列出来.xlsx"

# 确保输入文件存在
if not os.path.exists(input_path):
    raise FileNotFoundError(f"未找到输入文件: {input_path}")

# 读取Excel
df = pd.read_excel(input_path)

# 定义函数：查找两个字符串之间的最大公共子串
def find_lcs(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_index = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_index = i

    if max_len == 0:
        return ""
    return s1[end_index - max_len:end_index]

# 处理每一行
results = []
for index, row in df.iterrows():
    col1 = str(row["第1列"])
    col2 = str(row["第2列"])
    common = find_lcs(col1, col2)
    results.append([col1, col2, common])

# 构建输出DataFrame
output_df = pd.DataFrame(results, columns=["第1列", "第2列", "交集项"])

# 获取输入文件所在目录，作为输出目录
output_dir = os.path.dirname(input_path)
# 生成时间戳
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"交集项输出_{timestamp}.xlsx"
output_path = os.path.join(output_dir, output_filename)

# 写入Excel
output_df.to_excel(output_path, index=False)

print(f"✅ 交集项已成功写入：{output_path}")