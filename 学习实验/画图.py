# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 解决中文显示问题（需系统安装中文字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块问题

# 定义时间轴（注射后时间，单位：小时）
time = np.linspace(0, 24, 1000)

# 短效胰岛素：高斯函数模拟（起效时间30分钟，高峰2-4小时，持续6小时）
def short_acting(t):
    return np.exp(-((t - 3)/1.5)**2) * 1.2  # 峰值在3小时

# 长效胰岛素：平坦曲线模拟（起效时间3-4小时，持续24小时）
def long_acting(t):
    return np.where(t < 4, 0, 0.4)  # 4小时后维持稳定浓度

# 计算叠加效应
combined = short_acting(time) + long_acting(time)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(time, short_acting(time), label='短效胰岛素', color='blue')
plt.plot(time, long_acting(time), label='长效胰岛素', color='red')
plt.plot(time, combined, label='叠加效应', color='purple', linestyle='--')
plt.axvline(x=0.5, color='gray', linestyle=':', label='短效起效时间 (~0.5h)')
plt.axvline(x=4, color='orange', linestyle=':', label='长效起效时间 (~4h)')
plt.xlabel('注射后时间 (小时)')
plt.ylabel('药效强度 (任意单位)')
plt.title('胰岛素药效曲线及叠加效应模拟')
plt.legend()
plt.grid(True)
plt.show()