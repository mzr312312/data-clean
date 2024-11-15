import matplotlib.pyplot as plt

# 数据
data = [
    [3555, 4555, 5555, 6555, 7555, 8555],
    [1000, 1000, 1000, 1000, 1000, 1000],
    [-4555, -4555, 0, 0, 0, 0]
]

# 绘制折线图
plt.figure(figsize=(12, 6))
for i in range(3):
    plt.plot(data[0], data[i+1])

# 添加标题和标签
plt.title('示例图表')
plt.xlabel('X轴')
plt.ylabel('Y轴')

# 显示图形
plt.show()