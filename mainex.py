from flask import Flask, request, jsonify, send_from_directory
from gevent import pywsgi
import os
import openpyxl
from pylab import *
from shutil import copyfile
app = Flask(__name__)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域访问
    return response

@app.route('/download-excelmain')
def download_excel():
    ip_address = request.remote_addr
    current_path = os.path.dirname(__file__)
    excel_file_path = os.path.join(current_path, f'{ip_address}.xlsx')
    directory = os.path.dirname(excel_file_path)
    filename = os.path.basename(excel_file_path)
    response = send_from_directory(directory, filename, as_attachment=True)
    return add_cors_headers(response)  # 应用 CORS 头

@app.route('/writetomain', methods=['POST'])
def write_to_excel():
    # 获取请求
    x = request.form.get('x', type=int)
    y = request.form.get('y', type=int)
    value = request.form.get('value')
    ip_address = request.remote_addr

    if x is None or y is None or value is None:
        return jsonify({"error": "Please provide 'x', 'y', and 'value' parameters"}), 400

    try:
        # 检查当前路径下是否存在以IP地址命名的Excel文件
        current_path = os.path.dirname(__file__)
        ip_excel_file = os.path.join(current_path, f'{ip_address}.xlsx')

        if not os.path.exists(ip_excel_file):
            # 如果不存在，则复制模板文件为以IP地址命名的文件
            template_excel_file = os.path.join(current_path, 'ex.xlsx')
            copyfile(template_excel_file, ip_excel_file)

        # 加载以IP地址命名的Excel文件
        wb = openpyxl.load_workbook(ip_excel_file)
        ws = wb.active
        # 将值写入指定的单元格
        ws.cell(row=x, column=y, value=value)
        # 保存文件
        wb.save(ip_excel_file)

        return jsonify({"message": "Value written successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 3355), app)
    server.serve_forever()