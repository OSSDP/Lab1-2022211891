import math
import numpy as np
import sympy as sp
from flask import Flask, request, jsonify
from gevent import pywsgi

app = Flask(__name__)

c = 3e+8

I1 = 1e+13
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域访问
    return response

@app.route('/calculate', methods=['GET'])
def calculate():

    try:

        # 从请求参数中获取值
        L = float(request.args.get('l'))
        alpha1 = float(request.args.get('alpha1'))
        beta1 = float(request.args.get('beta1'))
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        d = int(request.args.get('d'))
        phi2 = float(request.args.get('phi2'))
        phi3 = float(request.args.get('phi3'))

        # 将角度转换为弧度
        alpha1 = sp.rad(alpha1)
        beta1 = sp.rad(beta1)

        # 定义符号变量
        theta1, phi1, k = sp.symbols('theta1 phi1 k')

        # 定义方程
        eqs = [
            sp.sin(alpha1) * sp.sin(beta1) - k * sp.sin(theta1) * sp.cos(phi1),
            sp.sin(alpha1) - k * sp.sin(theta1) * sp.sin(phi1),
            sp.cos(alpha1) * sp.cos(beta1) - k * sp.cos(theta1)
        ]

        ang = forEach(alpha1,beta1,a, b, d,theta1, phi1, k,eqs)
        truetheta1=ang[7]
        truephi1 = ang[8]
        theta2 = ang[0]
        theta3 = ang[1]
        if ang[2] == 1:
            d31 = 3.4e-12
            d33 = 20.3e-12
            d22 = 2.76e-12
            d15 = 5.45e-12
            m2 = np.array([[0, 0, 0, 0, d15, -d22],
                           [-d22, d22, 0, d15, 0, 0],
                           [d31, d31, d33, 0, 0, 0]])
            if ang[3] == 1:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * sp.sin(phi2)],
                               [sp.cos(ang[8]) * sp.cos(phi2)],
                               [0],
                               [0],
                               [0],
                               [-sp.sin(ang[8]) * sp.cos(phi2) - sp.sin(phi2) * sp.cos(ang[8])]
                               ])

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] == 2:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]])

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] == 3:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[7]) * sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * sp.sin(theta2)],
                               [-1 * sp.cos(ang[7]) * sp.sin(ang[8]) * sp.sin(theta2) + sp.sin(ang[7]) * (-1) * sp.cos(
                                   theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * (-1) * sp.cos(theta2) * sp.cos(phi2) + (-1) * sp.cos(ang[7]) * sp.cos(
                                   ang[8]) * sp.sin(theta2)],
                               [sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(
                                   ang[7]) * sp.sin(
                                   ang[8]) * sp.cos(theta2) * sp.cos(phi2)]
                               ])

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])
            elif ang[3] == 4:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1 * 0.3) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方

            else:
                print("错误")


        elif ang[2] ==2:
            d11 = 1.78e-12
            d22 = 0.13e-12
            d31 = 0.13e-12
            d33 = 1e-12
            m2 = np.array([[d11, -d11, 0, 0, -d11, -d22],
                           [-d22, d22, 0, -d11, 0, -d11],
                           [d31, d31, d33, 0, 0, 0]])
            if ang[3] ==1:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * sp.sin(phi2)],
                               [sp.cos(ang[8]) * sp.cos(phi2)],
                               [0],
                               [0],
                               [0],
                               [-sp.sin(ang[8]) * sp.cos(phi2) - sp.sin(phi2) * sp.cos(ang[8])]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==2:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==3:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[7]) * sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * sp.sin(theta2)],
                               [-1 * sp.cos(ang[7]) * sp.sin(ang[8]) * sp.sin(theta2) + sp.sin(ang[7]) * (-1) * sp.cos(
                                   theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * (-1) * sp.cos(theta2) * sp.cos(phi2) + (-1) * sp.cos(ang[7]) * sp.cos(
                                   ang[8]) * sp.sin(theta2)],
                               [sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(
                                   ang[7]) * sp.sin(
                                   ang[8]) * sp.cos(theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==4:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            else:
                print("错误")
        elif ang[2] ==3:
            d15 = 5.53e-12
            d31 = 4.4e-12
            d33 = 1e-12
            m2 = np.array([[0, 0, 0, 0, d15, 0],
                           [0, 0, 0, d15, 0, 0],
                           [d31, d31, d33, 0, 0, 0]])
            if ang[3] ==1:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * sp.sin(phi2)],
                               [sp.cos(ang[8]) * sp.cos(phi2)],
                               [0],
                               [0],
                               [0],
                               [-sp.sin(ang[8]) * sp.cos(phi2) - sp.sin(phi2) * sp.cos(ang[8])]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==2:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==3:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[7]) * sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * sp.sin(theta2)],
                               [-1 * sp.cos(ang[7]) * sp.sin(ang[8]) * sp.sin(theta2) + sp.sin(ang[7]) * (-1) * sp.cos(
                                   theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * (-1) * sp.cos(theta2) * sp.cos(phi2) + (-1) * sp.cos(ang[7]) * sp.cos(
                                   ang[8]) * sp.sin(theta2)],
                               [sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(
                                   ang[7]) * sp.sin(
                                   ang[8]) * sp.cos(theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==4:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1 * 0.3) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方


            else:
                print("错误")
        elif ang[2] ==4:
            d15 = 4.4e-12
            d22 = 4.4e-12
            d31 = 1e-12
            d33 = 1e-12
            m2 = np.array([[0, 0, 0, 0, d15, -d22],
                           [-d22, d22, 0, d15, 0, 0],
                           [d31, d31, d33, 0, 0, 0]])
            if ang[3] ==1:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * sp.sin(phi2)],
                               [sp.cos(ang[8]) * sp.cos(phi2)],
                               [0],
                               [0],
                               [0],
                               [-sp.sin(ang[8]) * sp.cos(phi2) - sp.sin(phi2) * sp.cos(ang[8])]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==2:
                m1 = np.array([-1 * sp.cos(theta3) * sp.cos(phi3), -1 * sp.cos(theta3) * sp.sin(phi3), sp.sin(theta3)])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==3:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[7]) * sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * sp.sin(theta2)],
                               [-1 * sp.cos(ang[7]) * sp.sin(ang[8]) * sp.sin(theta2) + sp.sin(ang[7]) * (-1) * sp.cos(
                                   theta2) * sp.sin(phi2)],
                               [sp.sin(ang[7]) * (-1) * sp.cos(theta2) * sp.cos(phi2) + (-1) * sp.cos(ang[7]) * sp.cos(
                                   ang[8]) * sp.sin(theta2)],
                               [sp.cos(ang[7]) * sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(
                                   ang[7]) * sp.sin(
                                   ang[8]) * sp.cos(theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
            elif ang[3] ==4:
                m1 = np.array([sp.sin(phi3), -1 * sp.cos(phi3), 0])
                m3 = np.array([[sp.sin(ang[8]) * (-1) * sp.cos(theta2) * sp.cos(phi2)],
                               [sp.cos(ang[8]) * sp.cos(theta2) * sp.sin(phi2)],
                               [0],
                               [-sp.cos(ang[8]) * sp.sin(theta2)],
                               [sp.sin(ang[8]) * sp.sin(theta2)],
                               [-sp.sin(ang[8]) * sp.cos(theta2) * sp.sin(phi2) + sp.cos(ang[8]) * sp.cos(
                                   theta2) * sp.cos(phi2)]
                               ])
                # n1 = ang[4]
                # n2 = ang[5]
                # omiga1 = ang[6]

                deff = m1 @ m2 @ m3
                eta = (2 * pow(ang[6] * deff * L, 2) * I1 * 0.3) / (
                        8.85e-12 * c * c * c * ang[4] * ang[5])  # n1代表平方
                print("效率值为：", eta)

            else:
                print("错误")
        else:
            print("材料库中没有这种晶体")
        # 求解alpha和beta
        alpha2, beta2, k3 = sp.symbols('alpha2 beta2 k3')
        alpha3, beta3, k4 = sp.symbols('alpha3 beta3 k4')
        eqs3 = [
            sp.sin(alpha2) * sp.sin(beta2) - k3 * sp.sin(theta2) * sp.cos(phi2),
            sp.sin(alpha2) - k3 * sp.sin(theta2) * sp.sin(phi2),
            sp.cos(alpha2) * sp.cos(beta2) - k3 * sp.cos(theta2)
        ]
        eqs4 = [
            sp.sin(alpha3) * sp.sin(beta3) - k4 * sp.sin(theta3) * sp.cos(phi3),
            sp.sin(alpha3) - k4 * sp.sin(theta3) * sp.sin(phi3),
            sp.cos(alpha3) * sp.cos(beta3) - k4 * sp.cos(theta3)
        ]
        myarr=forAngle(alpha2, beta2,k3,eqs3,alpha3, beta3,k4,eqs4,theta2,phi2,theta3,phi3)
        print(myarr)
        alpha2=myarr[0]
        beta2=myarr[1]
        alpha3=myarr[2]
        beta3=myarr[3]
        # 返回结果
        response = {
            'eta': float(eta),
            'alpha2': float(alpha2),
            'beta2': float(beta2),
            'alpha3': float(alpha3),
            'beta3': float(beta3),
            'theta1':float(truetheta1),
            'phi1': float(truephi1),
            'theta2': float(theta2),
            'theta3': float(theta3)
        }
        return add_cors_headers(jsonify(response))

    except Exception as e:
        return jsonify({'error': str(e)}), 400


def cal(alpha1,beta1,i, j, l, a, b, d, s, p,theta1, phi1, k,eqs):
        if a == 1:
            if b == 1:
                if d == 1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(2.9048 + 0.011768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 2)
                    ne_omiga1 = math.sqrt(2.582 + 0.019169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                    no_omiga2 = math.sqrt(2.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                    ne_omiga2 = math.sqrt(2.582 + 0.019169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                    no_omiga3 = math.sqrt(2.9048 + 0.011768 / (lamda3 ** 2 - 0.0475) - 0.027169 * lamda3 ** 2)
                    ne_omiga3 = math.sqrt(2.582 + 0.019169 / (lamda3 ** 2 - 0.04443) - 0.02195 * lamda3 ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)

                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= \
                            solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                        solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiNbO_3")
                        print("进行的是倍频过程")
                        print('相位匹配类型为ooe')

                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(4.9048 + 0.011768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 2)
                    ne_omiga1 = math.sqrt(4.582 + 0.019169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                    no_omiga2 = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                    ne_omiga2 = math.sqrt(4.582 + 0.019169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                    no_omiga3 = math.sqrt(4.9048 + 0.011768 / (lamda3 ** 2 - 0.0475) - 0.027169 * lamda3 ** 2)
                    ne_omiga3 = math.sqrt(4.582 + 0.019169 / (lamda3 ** 2 - 0.04443) - 0.02195 * lamda3 ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程', ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiNbO_3")
                        print("进行的是倍频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            elif b ==2:



                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(4.9048 + 0.011768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 2)
                    ne_omiga1 = math.sqrt(4.582 + 0.019169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                    no_omiga2 = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                    ne_omiga2 = math.sqrt(4.582 + 0.019169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                    no_omiga3 = math.sqrt(4.9048 + 0.011768 / (lamda3 ** 2 - 0.0475) - 0.027169 * lamda3 ** 2)
                    ne_omiga3 = math.sqrt(4.582 + 0.019169 / (lamda3 ** 2 - 0.04443) - 0.02195 * lamda3 ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiNbO_3")
                        print("进行的是和频过程")
                        print('相位匹配类型为ooe')

                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(4.9048 + 0.011768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 2)
                    ne_omiga1 = math.sqrt(4.582 + 0.019169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                    no_omiga2 = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                    ne_omiga2 = math.sqrt(4.582 + 0.019169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                    no_omiga3 = math.sqrt(4.9048 + 0.011768 / (lamda3 ** 2 - 0.0475) - 0.027169 * lamda3 ** 2)
                    ne_omiga3 = math.sqrt(4.582 + 0.019169 / (lamda3 ** 2 - 0.04443) - 0.02195 * lamda3 ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)

                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程',
                              ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiNbO_3")
                        print("进行的是和频过程")
                        print("相位匹配类型为eoe")

                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                else:
                    print("该晶体不存在此种相位匹配")
            elif b ==3:



                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 1e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(4.9048 + 0.011768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 2)
                    ne_omiga1 = math.sqrt(4.582 + 0.019169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                    no_omiga2 = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                    ne_omiga2 = math.sqrt(4.582 + 0.019169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                    no_omiga3 = math.sqrt(4.9048 + 0.011768 / (lamda3 ** 2 - 0.0475) - 0.027169 * lamda3 ** 2)
                    ne_omiga3 = math.sqrt(4.582 + 0.019169 / (lamda3 ** 2 - 0.04443) - 0.02195 * lamda3 ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 * no_omiga1
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if (0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and
                            abs(
                        solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1):
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[2]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[3]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[0] - (solution_1[0] + solution_2[1]) / 2)
                        print('[2]第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiNbO_3")
                        print("进行的是差频过程")
                        print('相位匹配类型为ooe')

                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 1e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(4.9048 + 0.011768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 2)
                    ne_omiga1 = math.sqrt(4.582 + 0.019169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                    no_omiga2 = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                    ne_omiga2 = math.sqrt(4.582 + 0.019169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                    no_omiga3 = math.sqrt(4.9048 + 0.011768 / (lamda3 ** 2 - 0.0475) - 0.027169 * lamda3 ** 2)
                    ne_omiga3 = math.sqrt(4.582 + 0.019169 / (lamda3 ** 2 - 0.04443) - 0.02195 * lamda3 ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]
                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 1 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 1 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 1 and 0 <= \
                            solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                        solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))


                        print('[2]第一方程', solution_1[0] - (solution_2[0] + solution_2[1]) / 2)
                        print('[2]第二方程', ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiNbO_3")
                        print("进行的是差频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            else:
                print("填写错误")
        elif a ==2:

            if b ==1:

                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                    ne_omiga1 = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                    ne_omiga2 = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                    no_omiga2 = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                    no_omiga3 = math.sqrt(1.9595 + 0.7892 * pow(lamda3, 2) / (lamda3 ** 2 - 0.02163))
                    ne_omiga3 = math.sqrt(1.6932 + 0.6782 * pow(lamda3, 2) / (lamda3 ** 2 - 0.01816))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是β-BaB_2O_4")
                        print("进行的是倍频过程")
                        print("相位匹配类型为ooe")

                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                    ne_omiga1 = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                    ne_omiga2 = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                    no_omiga2 = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                    no_omiga3 = math.sqrt(1.9595 + 0.7892 * pow(lamda3, 2) / (lamda3 ** 2 - 0.02163))
                    ne_omiga3 = math.sqrt(1.6932 + 0.6782 * pow(lamda3, 2) / (lamda3 ** 2 - 0.01816))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程',
                              ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是β-BaB_2O_4")
                        print("进行的是倍频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            elif b ==2:

                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                    ne_omiga1 = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                    ne_omiga2 = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                    no_omiga2 = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                    no_omiga3 = math.sqrt(1.9595 + 0.7892 * pow(lamda3, 2) / (lamda3 ** 2 - 0.02163))
                    ne_omiga3 = math.sqrt(1.6932 + 0.6782 * pow(lamda3, 2) / (lamda3 ** 2 - 0.01816))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('[1]第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('[1]第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('[2]第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[0]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是β-BaB_2O_4")
                        print("进行的是和频过程")
                        print("相位匹配类型为ooe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                    ne_omiga1 = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                    ne_omiga2 = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                    no_omiga2 = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                    no_omiga3 = math.sqrt(1.9595 + 0.7892 * pow(lamda3, 2) / (lamda3 ** 2 - 0.02163))
                    ne_omiga3 = math.sqrt(1.6932 + 0.6782 * pow(lamda3, 2) / (lamda3 ** 2 - 0.01816))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程',
                              ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是β-BaB_2O_4")
                        print("进行的是和频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                else:
                    print("该晶体不存在此种相位匹配")
            elif b ==3:


                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 1e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                    ne_omiga1 = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                    ne_omiga2 = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                    no_omiga2 = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                    no_omiga3 = math.sqrt(1.9595 + 0.7892 * pow(lamda3, 2) / (lamda3 ** 2 - 0.02163))
                    ne_omiga3 = math.sqrt(1.6932 + 0.6782 * pow(lamda3, 2) / (lamda3 ** 2 - 0.01816))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_1[0] - (solution_2[0] + solution_2[1]) / 2)
                        print('第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是β-BaB_2O_4")
                        print("进行的是差频过程")
                        print('相位匹配类型为ooe')
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:

                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 1e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                    ne_omiga1 = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                    ne_omiga2 = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                    no_omiga2 = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                    no_omiga3 = math.sqrt(1.9595 + 0.7892 * pow(lamda3, 2) / (lamda3 ** 2 - 0.02163))
                    ne_omiga3 = math.sqrt(1.6932 + 0.6782 * pow(lamda3, 2) / (lamda3 ** 2 - 0.01816))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n1 = ne_omiga1_theta1 * no_omiga1
                    n2 = ne_omiga3_theta3
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_1[0] - (solution_2[0] + solution_2[1]) / 2)
                        print('第二方程',
                              ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))

                        print("选择的晶体是β-BaB_2O_4")
                        print("进行的是差频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need

                else:
                    print("填写错误")
        elif a ==3:

            if b ==1:

                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(
                        3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                    ne_omiga1 = math.sqrt(
                        2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                    no_omiga2 = math.sqrt(
                        3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                    ne_omiga2 = math.sqrt(
                        2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                    no_omiga3 = math.sqrt(
                        3.415716 + 0.047031 / (lamda3 ** 2 - 0.035306) - 0.008801 * pow(lamda3, 2))
                    ne_omiga3 = math.sqrt(
                        2.918692 + 0.035145 / (lamda3 ** 2 - 0.028224) - 0.003641 * pow(lamda3, 2))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)

                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiIO_3")
                        print("进行的是倍频过程")
                        print("相位匹配类型为ooe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(
                        3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                    ne_omiga1 = math.sqrt(
                        2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                    no_omiga2 = math.sqrt(
                        3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                    ne_omiga2 = math.sqrt(
                        2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                    no_omiga3 = math.sqrt(
                        3.415716 + 0.047031 / (lamda3 ** 2 - 0.035306) - 0.008801 * pow(lamda3, 2))
                    ne_omiga3 = math.sqrt(
                        2.918692 + 0.035145 / (lamda3 ** 2 - 0.028224) - 0.003641 * pow(lamda3, 2))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程',
                              ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiIO_3")
                        print("进行的是倍频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            elif b ==2:

                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(
                        3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                    ne_omiga1 = math.sqrt(
                        2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                    no_omiga2 = math.sqrt(
                        3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                    ne_omiga2 = math.sqrt(
                        2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                    no_omiga3 = math.sqrt(
                        3.415716 + 0.047031 / (lamda3 ** 2 - 0.035306) - 0.008801 * pow(lamda3, 2))
                    ne_omiga3 = math.sqrt(
                        2.918692 + 0.035145 / (lamda3 ** 2 - 0.028224) - 0.003641 * pow(lamda3, 2))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)

                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiIO_3")
                        print("进行的是和频过程")
                        print('相位匹配类型为ooe')
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(
                        3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                    ne_omiga1 = math.sqrt(
                        2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                    no_omiga2 = math.sqrt(
                        3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                    ne_omiga2 = math.sqrt(
                        2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                    no_omiga3 = math.sqrt(
                        3.415716 + 0.047031 / (lamda3 ** 2 - 0.035306) - 0.008801 * pow(lamda3, 2))
                    ne_omiga3 = math.sqrt(
                        2.918692 + 0.035145 / (lamda3 ** 2 - 0.028224) - 0.003641 * pow(lamda3, 2))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1

                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程',
                              ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiIO_3")
                        print("进行的是和频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                else:
                    print("该晶体不存在此种相位匹配")
            elif b ==3:


                if d ==1:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 1e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(
                        3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                    ne_omiga1 = math.sqrt(
                        2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                    no_omiga2 = math.sqrt(
                        3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                    ne_omiga2 = math.sqrt(
                        2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                    no_omiga3 = math.sqrt(
                        3.415716 + 0.047031 / (lamda3 ** 2 - 0.035306) - 0.008801 * pow(lamda3, 2))
                    ne_omiga3 = math.sqrt(
                        2.918692 + 0.035145 / (lamda3 ** 2 - 0.028224) - 0.003641 * pow(lamda3, 2))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = no_omiga1 ** 2

                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_1[0] - (solution_2[0] + solution_2[1]) / 2)
                        print('第二方程', no_omiga1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiIO_3")
                        print("进行的是差频过程")
                        print('相位匹配类型为ooe')
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==2:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 1e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    no_omiga1 = math.sqrt(
                        3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                    ne_omiga1 = math.sqrt(
                        2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                    no_omiga2 = math.sqrt(
                        3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                    ne_omiga2 = math.sqrt(
                        2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                    no_omiga3 = math.sqrt(
                        3.415716 + 0.047031 / (lamda3 ** 2 - 0.035306) - 0.008801 * pow(lamda3, 2))
                    ne_omiga3 = math.sqrt(
                        2.918692 + 0.035145 / (lamda3 ** 2 - 0.028224) - 0.003641 * pow(lamda3, 2))
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = ne_omiga3_theta3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                theta2) - ne_omiga3_theta3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_1[0] - (solution_2[0] + solution_2[1]) / 2)
                        print('第二方程', ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - ne_omiga3_theta3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiIO_3")
                        print("进行的是差频过程")
                        print("相位匹配类型为eoe")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            else:
                print("填写错误")

        elif a ==4:

            if b ==1:

                if d ==3:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-4
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    a1e = 4.6415
                    a2e = 0.08488
                    a3e = 0.1927
                    a4e = 5.5832
                    a5e = 8.3067
                    a6e = 0.021696
                    b1e = 4.782e-7
                    b2e = 3.0913e-8
                    b3e = 2.7326e-8
                    b4e = 1.4837e-5
                    b5e = 1.3647e-7
                    a1o = 4.5082
                    a2o = 0.084888
                    a3o = 0.19552
                    a4o = 1.157
                    a5o = 8.2517
                    a6o = 0.0237
                    b1o = 2.0704e-8
                    b2o = 1.4449e-8
                    b3o = 1.5978e-8
                    b4o = 4.7686e-6
                    b5o = 1.1127e-5
                    f = (25 - 24.5) * (25 + 570.82)
                    ne_omiga1 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                    no_omiga1 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                    ne_omiga2 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                    no_omiga2 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                    ne_omiga3 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda3 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda3 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda3 ** 2)
                    no_omiga3 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda3 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda3 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda3 ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga2_theta2 = no_omiga2 * ne_omiga2 / sp.sqrt(
                        no_omiga2 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga2 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = no_omiga3
                    n1 = ne_omiga1_theta1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + ne_omiga2_theta2 * omiga2 * sp.cos(
                                theta2) - no_omiga3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                        solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <=1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + ne_omiga2_theta2 * omiga2 * sp.cos(
                            solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程', ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + ne_omiga2_theta2 * omiga2 * sp.cos(
                                solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiTaO_3")
                        print("进行的是倍频过程")
                        print("相位匹配类型为eeo")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==4:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-4
                    omiga1 = (2 * math.pi * c) / lamda1
                    omiga2 = omiga1
                    lamda2 = (2 * math.pi * c) / omiga2
                    omiga3 = 2 * omiga1
                    lamda3 = (2 * math.pi * c) / omiga3
                    a1e = 4.6415
                    a2e = 0.08488
                    a3e = 0.1927
                    a4e = 5.5832
                    a5e = 8.3067
                    a6e = 0.021696
                    b1e = 4.782e-7
                    b2e = 3.0913e-8
                    b3e = 2.7326e-8
                    b4e = 1.4837e-5
                    b5e = 1.3647e-7
                    a1o = 4.5082
                    a2o = 0.084888
                    a3o = 0.19552
                    a4o = 1.157
                    a5o = 8.2517
                    a6o = 0.0237
                    b1o = 2.0704e-8
                    b2o = 1.4449e-8
                    b3o = 1.5978e-8
                    b4o = 4.7686e-6
                    b5o = 1.1127e-5
                    f = (25 - 24.5) * (25 + 570.82)
                    ne_omiga1 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                    no_omiga1 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                    ne_omiga2 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                    no_omiga2 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                    ne_omiga3 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda3 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda3 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda3 ** 2)
                    no_omiga3 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda3 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda3 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda3 ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga2_theta2 = no_omiga2 * ne_omiga2 / sp.sqrt(
                        no_omiga2 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga2 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = no_omiga3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - no_omiga3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('[1]第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('[2]第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程',ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                  solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiTaO_3")
                        print("进行的是倍频过程")
                        print("相位匹配类型为eoo")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            elif b ==2:

                if d ==3:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-5
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    a1e = 4.6415
                    a2e = 0.08488
                    a3e = 0.1927
                    a4e = 5.5832
                    a5e = 8.3067
                    a6e = 0.021696
                    b1e = 4.782e-7
                    b2e = 3.0913e-8
                    b3e = 2.7326e-8
                    b4e = 1.4837e-5
                    b5e = 1.3647e-7
                    a1o = 4.5082
                    a2o = 0.084888
                    a3o = 0.19552
                    a4o = 1.157
                    a5o = 8.2517
                    a6o = 0.0237
                    b1o = 2.0704e-8
                    b2o = 1.4449e-8
                    b3o = 1.5978e-8
                    b4o = 4.7686e-6
                    b5o = 1.1127e-5
                    f = (25 - 24.5) * (25 + 570.82)
                    ne_omiga1 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                    no_omiga1 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                    ne_omiga2 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                    no_omiga2 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                    ne_omiga3 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda3 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda3 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda3 ** 2)
                    no_omiga3 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda3 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda3 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda3 ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga2_theta2 = no_omiga2 * ne_omiga2 / sp.sqrt(
                        no_omiga2 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga2 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = no_omiga3
                    n1 = ne_omiga1_theta1 ** 2
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + ne_omiga2_theta2 * omiga2 * sp.cos(
                                theta2) - no_omiga3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + ne_omiga2_theta2 * omiga2 * sp.cos(
                            solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print('第一方程',
                              sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                                  solution_1[1]))
                        print('第二方程',
                              sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(solution_1[1]))
                        print('第三方程', sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0]))
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print('第一方程', solution_2[1] - (solution_1[0] + solution_2[0]) / 2)
                        print('第二方程', ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + ne_omiga2_theta2 * omiga2 * sp.cos(
                                solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("Solution (theta2, theta3):", solution_2)
                        print("选择的晶体是LiTaO_3")
                        print("进行的是和频过程")
                        print('相位匹配类型为eeo')
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==4:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-5
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-5
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 + omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    a1e = 4.6415
                    a2e = 0.08488
                    a3e = 0.1927
                    a4e = 5.5832
                    a5e = 8.3067
                    a6e = 0.021696
                    b1e = 4.782e-7
                    b2e = 3.0913e-8
                    b3e = 2.7326e-8
                    b4e = 1.4837e-5
                    b5e = 1.3647e-7
                    a1o = 4.5082
                    a2o = 0.084888
                    a3o = 0.19552
                    a4o = 1.157
                    a5o = 8.2517
                    a6o = 0.0237
                    b1o = 2.0704e-8
                    b2o = 1.4449e-8
                    b3o = 1.5978e-8
                    b4o = 4.7686e-6
                    b5o = 1.1127e-5
                    f = (25 - 24.5) * (25 + 570.82)
                    ne_omiga1 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                    no_omiga1 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                    ne_omiga2 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                    no_omiga2 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                    ne_omiga3 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda3 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda3 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda3 ** 2)
                    no_omiga3 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda3 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda3 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda3 ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga2_theta2 = no_omiga2 * ne_omiga2 / sp.sqrt(
                        no_omiga2 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga2 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = no_omiga3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [theta3 - (solution_1[0] + theta2) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                                theta2) - no_omiga3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_2[1] - (solution_1[0] + solution_2[0]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) + no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiTaO_3")
                        print("进行的是和频过程")
                        print("相位匹配类型为eoo")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                else:
                    print("该晶体不存在此种相位匹配")
            elif b ==3:


                if d ==3:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    a1e = 4.6415
                    a2e = 0.08488
                    a3e = 0.1927
                    a4e = 5.5832
                    a5e = 8.3067
                    a6e = 0.021696
                    b1e = 4.782e-7
                    b2e = 3.0913e-8
                    b3e = 2.7326e-8
                    b4e = 1.4837e-5
                    b5e = 1.3647e-7
                    a1o = 4.5082
                    a2o = 0.084888
                    a3o = 0.19552
                    a4o = 1.157
                    a5o = 8.2517
                    a6o = 0.0237
                    b1o = 2.0704e-8
                    b2o = 1.4449e-8
                    b3o = 1.5978e-8
                    b4o = 4.7686e-6
                    b5o = 1.1127e-5
                    f = (25 - 24.5) * (25 + 570.82)
                    ne_omiga1 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                    no_omiga1 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                    ne_omiga2 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                    no_omiga2 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                    ne_omiga3 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda3 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda3 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda3 ** 2)
                    no_omiga3 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda3 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda3 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda3 ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga2_theta2 = no_omiga2 * ne_omiga2 / sp.sqrt(
                        no_omiga2 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga2 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = no_omiga3
                    n1 = ne_omiga1_theta1 ** 2

                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - ne_omiga2_theta2 * omiga2 * sp.cos(
                                theta2) - no_omiga3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - ne_omiga2_theta2 * omiga2 * sp.cos(
                            solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiTaO_3")
                        print("进行的是差频过程")
                        print('相位匹配类型为eeo')
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
                elif d ==4:
                    symbols = [theta1, phi1, k]
                    solution_1 = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
                    lamda1 = 1.06e-6
                    omiga1 = (2 * math.pi * c) / lamda1
                    lamda2 = 4.06e-4
                    # omiga1 > omiga2
                    omiga2 = (2 * math.pi * c) / lamda2
                    omiga3 = omiga1 - omiga2
                    lamda3 = (2 * math.pi * c) / omiga3
                    a1e = 4.6415
                    a2e = 0.08488
                    a3e = 0.1927
                    a4e = 5.5832
                    a5e = 8.3067
                    a6e = 0.021696
                    b1e = 4.782e-7
                    b2e = 3.0913e-8
                    b3e = 2.7326e-8
                    b4e = 1.4837e-5
                    b5e = 1.3647e-7
                    a1o = 4.5082
                    a2o = 0.084888
                    a3o = 0.19552
                    a4o = 1.157
                    a5o = 8.2517
                    a6o = 0.0237
                    b1o = 2.0704e-8
                    b2o = 1.4449e-8
                    b3o = 1.5978e-8
                    b4o = 4.7686e-6
                    b5o = 1.1127e-5
                    f = (25 - 24.5) * (25 + 570.82)
                    ne_omiga1 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                    no_omiga1 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                    ne_omiga2 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                    no_omiga2 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                    ne_omiga3 = math.sqrt(
                        a1e + b1e * f + (a2e + b2e * f) / (lamda3 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                   b4e * f) / (
                                lamda3 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda3 ** 2)
                    no_omiga3 = math.sqrt(
                        a1o + b1o * f + (a2o + b2o * f) / (lamda3 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                   b4o * f) / (
                                lamda3 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda3 ** 2)
                    ne_omiga1_theta1 = no_omiga1 * ne_omiga1 / sp.sqrt(
                        no_omiga1 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga1 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga2_theta2 = no_omiga2 * ne_omiga2 / sp.sqrt(
                        no_omiga2 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga2 ** 2 * sp.cos(solution_1[0]) ** 2)
                    ne_omiga3_theta3 = no_omiga3 * ne_omiga3 / sp.sqrt(
                        no_omiga3 ** 2 * sp.sin(solution_1[0]) ** 2 + ne_omiga3 ** 2 * sp.cos(solution_1[0]) ** 2)
                    n2 = no_omiga3
                    n1 = ne_omiga1_theta1 * no_omiga1
                    theta2, theta3 = sp.symbols('theta2 theta3')
                    eqs2 = [solution_1[0] - (theta2 + theta3) / 2,
                            ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                                theta2) - no_omiga3 * omiga3 * sp.cos(theta3)]

                    symbols2 = [theta2, theta3]
                    solution_2 = sp.nsolve(eqs2, symbols2, [s, p], verify=False)
                    if 0 <= solution_1[0] <= sp.pi / 2 and 0 <= solution_1[1] <= sp.pi / 2 and abs(
                            sp.sin(alpha1) - solution_1[2] * sp.sin(solution_1[0]) * sp.sin(
                                solution_1[1])) <= 0.00001 and abs(
                        sp.sin(alpha1) * sp.sin(beta1) - solution_1[2] * sp.sin(solution_1[0]) * sp.cos(
                            solution_1[1])) <= 0.00001 and abs(
                        sp.cos(alpha1) * sp.cos(beta1) - solution_1[2] * sp.cos(solution_1[0])) <= 0.00001 and 0 <= solution_2[0] <= sp.pi / 2 and 0 <= solution_2[1] <= sp.pi / 2 and abs(
                            solution_1[0] - (solution_2[0] + solution_2[1]) / 2) <= 1 and abs(
                        ne_omiga1_theta1 * omiga1 * sp.cos(solution_1[0]) - no_omiga2 * omiga2 * sp.cos(
                            solution_2[0]) - no_omiga3 * omiga3 * sp.cos(solution_2[1])) <= 1:
                        print("theta1", sp.deg(solution_1[0]))
                        print("phi1", sp.deg(solution_1[1]))
                        print("theta2", sp.deg(solution_2[0]))
                        print("theta3", sp.deg(solution_2[1]))
                        print("选择的晶体是LiTaO_3")
                        print("进行的是差频过程")
                        print("相位匹配类型为eoo")
                        need = (1, solution_1[0], solution_1[1], solution_2[0], solution_2[1], a, d, n1, n2, omiga1)
                        return need
                    else:
                        need = (0, 0, 0, 0, 0, a, d, n1, n2, omiga1)
                        return need
            else:
                print("填写错误")



def forEach(alpha1,beta1,a, b, d,theta1, phi1, k,eqs):
    for i in np.arange(0.00001, sp.pi/2, 1):
        for j in np.arange(0.00001, sp.pi/2, 1):
            for l in np.arange(0.0001, 2, 1):
                for s in np.arange(0.00001, sp.pi / 2, 1):
                    for p in np.arange(0.00001, sp.pi / 2, 1):
                        print('循环一次')
                        res = cal(alpha1,beta1,i, j, l, a, b, d, s, p,theta1, phi1, k,eqs)
                        if res[0] == 1:

                            theta = (res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[1], res[2])
                            return theta




def angle(a31, a32, a33, a41, a42, a43,alpha2, beta2,k3,eqs3,alpha3, beta3,k4,eqs4,theta2,phi2,theta3,phi3):

    symbols3 = [alpha2, beta2,k3]
    solution_3 = sp.nsolve(eqs3, symbols3, [a31, a32, a33], verify=False)
    symbols4 = [alpha3, beta3,k4]
    solution_4 = sp.nsolve(eqs4, symbols4, [a41, a42, a43], verify=False)
    if 0<= solution_3[0]<=sp.pi/2 and 0<= solution_3[1]<=sp.pi/2 and 0<= solution_4[0]<=sp.pi/2 and 0<= solution_4[1]<=sp.pi/2 and abs(sp.sin(solution_3[0]) * sp.sin(solution_3[1]) - solution_3[2] * sp.sin(theta2) * sp.cos(phi2)) <= 1 and abs(
        sp.sin(solution_3[0]) - solution_3[2] * sp.sin(theta2) * sp.sin(phi2)) <= 1 and abs(
        sp.cos(solution_3[0]) * sp.cos(solution_3[1]) - solution_3[2] * sp.cos(theta2)) <= 1 and abs(
            sp.sin(solution_4[0]) * sp.sin(solution_4[1]) - solution_4[2] * sp.sin(theta3) * sp.cos(phi3)) <= 1 and abs(
        sp.sin(solution_4[0]) - solution_4[2] * sp.sin(theta3) * sp.sin(phi3)) <= 1 and abs(
        sp.cos(solution_4[0]) * sp.cos(solution_4[1]) - solution_4[2] * sp.cos(theta3)) <= 1:
        while solution_3[0]<0:
            solution_3[0] += 2 * sp.pi
        while solution_3[0] > 2*sp.pi:
            solution_3[0] -= 2 * sp.pi

        while solution_3[1]<0:
            solution_3[1] += 2 * sp.pi
        while solution_3[1] > (2 * sp.pi):
            solution_3[1] -= 2 * sp.pi

        while solution_4[0]<0:
            solution_4[0] += 2 * sp.pi
        while solution_4[0] > 2 * sp.pi:
            solution_4[0] -= 2 * sp.pi

        while solution_4[1]<0:
            solution_4[1] += 2 * sp.pi
        while solution_4[1] > 2 * sp.pi:
            solution_4[1] -= 2 * sp.pi

        print("eqs31", sp.sin(solution_3[0]) * sp.sin(solution_3[1]) - solution_3[2] * sp.sin(theta2) * sp.cos(phi2))
        print("eqs32", sp.sin(solution_3[0]) - solution_3[2] * sp.sin(theta2) * sp.sin(phi2))
        print("eqs33", sp.cos(solution_3[0]) * sp.cos(solution_3[1]) - solution_3[2] * sp.cos(theta2))
        print("eqs41", sp.sin(solution_4[0]) * sp.sin(solution_4[1]) - solution_4[2] * sp.sin(theta3) * sp.cos(phi3))
        print("eqs42", sp.sin(solution_4[0]) - solution_4[2] * sp.sin(theta3) * sp.sin(phi3))
        print("eqs43", sp.cos(solution_4[0]) * sp.cos(solution_4[1]) - solution_4[2] * sp.cos(theta3))
        print("alpha2", sp.deg(solution_3[0]))
        print("beta2", sp.deg(solution_3[1]))
        print("alpha3", sp.deg(solution_4[0]))
        print("beta3", sp.deg(solution_4[1]))
        angle2 = (1, solution_3[0], solution_3[1], solution_4[0], solution_4[1])
        return angle2


    else:
        angle2 = (0, solution_3[0], solution_3[1], solution_4[0], solution_4[1])
        return angle2



def forAngle(alpha2, beta2,k3,eqs3,alpha3, beta3,k4,eqs4,theta2,phi2,theta3,phi3):
    for a31 in np.arange(0.00001, sp.pi/2, 1):
        for a32 in np.arange(0.00001, sp.pi/2, 1):
            for a33 in np.arange(-5, 5, 1):
                for a41 in np.arange(0.00001, sp.pi / 2, 1):
                    for a42 in np.arange(0.00001, sp.pi / 2, 1):
                        for a43 in np.arange(-5, 5, 1):
                            res2 = angle(a31, a32, a33, a41, a42, a43,alpha2, beta2,k3,eqs3,alpha3, beta3,k4,eqs4,theta2,phi2,theta3,phi3)
                            if res2[0] == 1:
                                return res2[1],res2[2],res2[3],res2[4]






if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 3888), app)
    server.serve_forever()
