from flask import Flask, request, jsonify, send_from_directory
import openpyxl
from pylab import *
import matplotlib.pyplot as plt
import os

def convert_angle(angle):
    x, y = angle.replace('′', '').split('°')
    return float(x) + float(y) / 60
def upload_file():


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
    x_array = np.array(x_data)
    y_array = np.array(y_data)
    z_array = np.array(z_data)



    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('θ values (degrees)',fontsize=15,labelpad=10)
    ax.set_ylabel('φ values (degrees)',fontsize=15,labelpad=10)
    ax.set_zlabel('Efficiency value',fontsize=15,labelpad=10)
    ax.bar3d(x_array, y_array, np.zeros_like(z_array), 1, 1, z_array, shade=True)

    # 保存图像
    image_path = '实验五图.png'
    plt.savefig(os.path.join(directory, image_path))
upload_file()