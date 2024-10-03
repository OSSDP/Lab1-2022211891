import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


from flask import Flask, request, jsonify, send_from_directory
import openpyxl
from pylab import *
import matplotlib.pyplot as plt
import os

def convert_angle(angle):
    x, y = angle.replace('′', '').split('°')
    return float(x) + float(y) / 60


plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
current_path = os.path.dirname(__file__)
excel_file_path = os.path.join(current_path, f'127.0.0.1.xlsx')
print(excel_file_path)
directory = os.path.dirname(excel_file_path)
# 读取Excel文件
wb = openpyxl.load_workbook(excel_file_path)
sheet = wb.active

# 读取x轴数据（角度）
x_data = [convert_angle(cell.value) for cell in sheet['B3:AI3'][0]]

# 读取y轴数据（角度）
y_data = [convert_angle(cell.value) for cell in sheet['B4:AI4'][0]]

# 读取z轴数据（值）
z_data = [float(cell.value) for cell in sheet['B5:AI5'][0]]

# 使用numpy arrays进行计算
x = np.array(x_data)
y = np.array(y_data)
z = np.array(z_data)
# # 读取 Excel 文件
# file_path = '127.0.0.1.xlsx'
# data = pd.read_excel(file_path)
#
# # 提取 x, y, z 数据
# x = data.iloc[:, 0].values
# y = data.iloc[:, 1].values
# z = data.iloc[:, 2].values
#
# # 确保 x 和 y 是数值类型
# x = np.array(x, dtype=float)
# y = np.array(y, dtype=float)
# z = np.array(z, dtype=float)

# 创建网格
x_unique = np.unique(x)
y_unique = np.unique(y)
X, Y = np.meshgrid(x_unique, y_unique)
Z = np.zeros_like(X)

# 填充 Z 数据
for i in range(len(x)):
    xi = np.where(x_unique == x[i])[0][0]
    yi = np.where(y_unique == y[i])[0][0]
    Z[yi, xi] = z[i]

# 绘制三维网状图
#fig = plt.figure(figsize=(10, 8))
#ax = fig.add_subplot(111, projection='3d')

#ax.plot_surface(X, Y, Z, cmap='viridis')






# 设置底面颜色，增强对比度
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 使用 plot_wireframe 绘制曲面
ax.plot_wireframe(X, Y, Z, color='black')

# 使用散点图来突出显示顶点，并设置散点颜色为蓝色
ax.scatter(X, Y, Z, color='blue',s=0.5)
#ax.plot(x, y, z, color='red', linewidth=0.5)

# 设置新的视角
#ax.view_init(elev=30, azim=120)

# 调整底面颜色，增强对比度
ax.xaxis.pane.fill = True
ax.yaxis.pane.fill = True
ax.zaxis.pane.fill = False  # 隐藏Z轴底面
ax.xaxis.pane.set_facecolor('lightgray')  # 设置X轴底面颜色
ax.yaxis.pane.set_facecolor('lightgray')  # 设置Y轴底面颜色

# 隐藏XY平面的边框线
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.set_edgecolor('none')
ax.zaxis.pane.set_edgecolor('none')



# 找到最高点
max_z = np.max(z)
max_index = np.argmax(z)
max_x = x[max_index]
max_y = y[max_index]




# 标注最高点的值
ax.text(max_x, max_y, max_z, f'({max_x:.2f}, {max_y:.2f}, {max_z:.2f})', color='red', fontsize=12)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Wireframe Plot with Highlighted Max Point and Contrasting Base')

plt.show()
