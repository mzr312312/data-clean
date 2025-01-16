import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 时间轴（分钟）
time = np.linspace(0, 180, 300)

# 模拟血糖曲线
def blood_glucose_curve(t):
    peak_time = 30  # 血糖峰值时间
    peak_value = 180  # 血糖峰值
    return peak_value * np.exp(-0.02 * (t - peak_time)**2)

# 模拟胰岛素曲线
def insulin_curve(t):
    peak_time = 45  # 胰岛素峰值时间
    peak_value = 100  # 胰岛素峰值
    return peak_value * np.exp(-0.015 * (t - peak_time)**2)

# 计算曲线
glucose = blood_glucose_curve(time)
insulin = insulin_curve(time)

# 绘制曲线
plt.figure(figsize=(10, 6))
plt.plot(time, glucose, label='血糖曲线 (mg/dL)', color='blue')
plt.plot(time, insulin, label='胰岛素曲线 (pmol/L)', color='red')

# 添加标题和标签
plt.title('吃大量高GI食物后的血糖和胰岛素曲线')
plt.xlabel('时间 (分钟)')
plt.ylabel('浓度')
plt.legend()
plt.grid(True)

# 显示图形
plt.show()