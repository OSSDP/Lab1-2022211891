from flask import Flask, request, jsonify
import pandas as pd
from gevent import pywsgi
import os



app = Flask(__name__)

# 定义路由，监听/readex5路径的GET请求
@app.route('/readex5', methods=['GET'])
def read_excel():
    # 获取URL参数x和y
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)

    if x is None or y is None:
        return jsonify({"error": "Please provide both 'x' and 'y' parameters"}), 400

    try:
        # 读取同目录下的read.xlsx文件
        current_path = os.path.dirname(__file__)
        df = pd.read_excel(current_path +'/read.xlsx', header=None)  # 不处理头部，因为请求是基于位置的
        # 获取指定的单元格内容
        result = df.iloc[x - 1, y - 1]  # pandas是基于0索引的，而请求可能是基于1的
        return jsonify({"value": result})
    except Exception as e:
        # 如果出现任何错误，返回错误信息
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__': # 在服务器上运行，监听所有公网IP
    server = pywsgi.WSGIServer(('0.0.0.0', 3339), app)
    server.serve_forever()