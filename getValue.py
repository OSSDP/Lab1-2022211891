from flask import Flask, request, jsonify
import numpy as np
import sympy as sp
import math
from gevent import pywsgi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




retheta=0
rephi=0
efficiency=0

def cal(i, j, l,alpha,beta):
    d31 = 3.4e-12
    d33 = 20.3e-12
    d22 = 2.76e-12
    d15 = 5.45e-12

    n1 = 2.321
    L = 0.001
    c = 3e+8

    I1 = 1e+13

    lamda1 = 1.06e-6
    omiga1 = (2 * math.pi * c) / lamda1
    omiga2 = 2 * omiga1
    lamda2 = (2 * math.pi * c) / omiga2

    theta, phi, k = sp.symbols('theta phi k')
    symbols = [theta, phi, k]
    print(alpha)
    print(beta)
    print(i)
    print(j)
    print(l)
    print(i)
    print(j)
    print(l)
    print(symbols)
    eqs = [
        sp.sin(alpha) * sp.sin(beta) - k * sp.sin(theta) * sp.cos(phi),
        sp.sin(alpha) - k * sp.sin(theta) * sp.sin(phi),
        sp.cos(alpha) * sp.cos(beta) - k * sp.cos(theta)
    ]
    solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
    print(solution)
    if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi/2 and abs(
            sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
        sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1])) <= 0.000001 and abs(
        sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
        n0_omiga = math.sqrt(4.9048 + 0.11768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 1)
        n0_2omiga = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
        ne_2omiga = math.sqrt(4.582 + 0.099169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
        ne_2omiga_theta = n0_2omiga * ne_2omiga / sp.sqrt(
        n0_2omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_2omiga ** 2 * sp.cos(solution[0]) ** 2)
        deta = omiga1 * L / c * (n0_omiga - ne_2omiga_theta)
        deff = d31 * sp.sin(solution[0]) - d22 * sp.cos(solution[0]) * sp.sin(3 * solution[1])
        eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (8.85e-12 * c * c * c * n0_omiga * n0_omiga * ne_2omiga_theta)
        global retheta
        retheta = float(sp.deg(solution[0]))
        global rephi
        rephi = float(sp.deg(solution[1]))
        global efficiency
        efficiency = eta
        return 1

    else:
        return 0


@app.route('/Ex5getValue', methods=['GET'])
def calculate_efficiency():
    alpha_val = float(request.args.get('alpha', 0))
    beta_val = float(request.args.get('beta', 0))
    alpha = sp.rad(alpha_val)
    beta = sp.rad(beta_val)

    for i in np.arange(0.000001, sp.pi/2, 1):
        for j in np.arange(0.000001, sp.pi/2, 1):
            for l in np.arange(0.0001, 2, 1):
                res = cal(i, j, l,alpha,beta)
                if res == 1:
                    return jsonify({"theta":float(retheta) , "phi": float(rephi) , "efficiency": float(efficiency)})
    return jsonify({"theta":0 , "phi": 0 , "efficiency": 0})



if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 3340), app)
    server.serve_forever()
