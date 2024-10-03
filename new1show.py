import math

from scipy.optimize import fsolve
from scipy.optimize import root
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp



n1 = 2.321
L = 0.001
c = 3e+8

I1 = 1e+13

lamda1 = 1.06e-6
omiga1 = (2 * math.pi * c) / lamda1
omiga2 = 2 * omiga1
lamda2 = (2 * math.pi * c) / omiga2



alpha = float(input("请输入alpha(角度): "))
beta = float(input("请输入beta(角度): "))

alpha = sp.rad(alpha)
beta = sp.rad(beta)

theta, phi, k = sp.symbols('theta phi k')

eqs = [
    sp.sin(alpha) * sp.sin(beta) - k * sp.sin(theta) * sp.cos(phi),
    sp.sin(alpha) - k * sp.sin(theta) * sp.sin(phi),
    sp.cos(alpha) * sp.cos(beta) - k * sp.cos(theta)
]

b: str = input('请选择你的晶体（1=LiNbO_3，2=β-BaB_2O_4, 3=LiIO_3， 4=LiTaO_3）')
a: str = input('请选择你的匹配类型(其中1=ooe,2=eoe，3=eeo,4=eoo):')
def cal(i, j, l,b,a):

    if b == "1":
        d31 = 3.4e-12
        d33 = 20.3e-12
        d22 = 2.76e-12
        d15 = 5.45e-12

        if a == "1":

            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi/2 and abs(
                    sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1])) <= 0.000001 and abs(
                sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程', sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])
                no_omiga = math.sqrt(4.9048 + 0.11768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 1)
                no_2omiga = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                ne_2omiga = math.sqrt(4.582 + 0.099169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                ne_2omiga_theta = no_2omiga * ne_2omiga / sp.sqrt(no_2omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_2omiga ** 2 * sp.cos(solution[0]) ** 2)
                deta = omiga1 * L / c * (no_omiga - ne_2omiga_theta)

                deff = d31 * sp.sin(solution[0]) - d22 * sp.cos(solution[0]) * sp.sin(3 * solution[1])
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为ooe")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)

                return 1
            else:
                return 0
        elif a ==2:
            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(
                    sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1])) <= 0.000001 and abs(
                sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程', sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])

                no_omiga = math.sqrt(4.9048 + 0.11768 / (lamda1 ** 2 - 0.0475) - 0.027169 * lamda1 ** 1)
                no_2omiga = math.sqrt(4.9048 + 0.011768 / (lamda2 ** 2 - 0.0475) - 0.027169 * lamda2 ** 2)
                ne_2omiga = math.sqrt(4.582 + 0.099169 / (lamda2 ** 2 - 0.04443) - 0.02195 * lamda2 ** 2)
                ne_omiga = math.sqrt(4.582 + 0.099169 / (lamda1 ** 2 - 0.04443) - 0.02195 * lamda1 ** 2)
                ne_omiga_theta = no_omiga ** 2 * ne_omiga ** 2 / math.sqrt(pow(no_omiga * sp.sin(solution[0]),2) + pow(ne_omiga * sp.cos(solution[0]), 2))
                ne_2omiga_theta = no_2omiga ** 2 * ne_2omiga ** 2 / math.sqrt(pow(no_2omiga * sp.sin(solution[0]), 2) + pow(ne_2omiga * sp.cos(solution[0]), 2))
                deta = (omiga1 * L / c) * (1 / 2 * ne_omiga_theta + 1 / 2 * no_omiga - ne_2omiga_theta)
                deff = d31 * sp.sin(solution[0]) * sp.cos(solution[0]) * sp.sin(2 * solution[1])
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为eoe")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)
                return 1
            else:
                return 0

        else:
            print("该晶体没有此种匹配类型")

        print("选择的晶体是铌酸锂晶体")
    elif b ==2:
        d11 = 1.78e-12
        d22 = 0.13e-12
        d31 = 0.13e-12


        if a == "1":

            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(
                    sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(
                    solution[1])) <= 0.000001 and abs(
                sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程',
                      sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])
                no_omiga = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                ne_omiga = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 -0.01816))
                ne_2omiga = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 -0.01816))
                no_2omiga = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                ne_2omiga_theta = no_2omiga * ne_2omiga / sp.sqrt(no_2omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_2omiga ** 2 * sp.cos(solution[0]) ** 2)
                deta = omiga1 * L / c * (no_omiga - ne_2omiga_theta)
                deff = d31 * sp.sin(solution[0]) + sp.cos(solution[0]) * (d11 * sp.cos(3 * solution[1]) - d22 * sp.sin(3 * solution[1]))
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为ooe")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)

                return 1
            else:
                return 0
        elif a ==2:
            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(
                sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(
                solution[1])) <= 0.000001 and abs(sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程',
                      sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])
                no_omiga = math.sqrt(1.9595 + 0.7892 * pow(lamda1, 2) / (lamda1 ** 2 - 0.02163))
                ne_omiga = math.sqrt(1.6932 + 0.6782 * pow(lamda1, 2) / (lamda1 ** 2 - 0.01816))
                ne_2omiga = math.sqrt(1.6932 + 0.6782 * pow(lamda2, 2) / (lamda2 ** 2 - 0.01816))
                no_2omiga = math.sqrt(1.9595 + 0.7892 * pow(lamda2, 2) / (lamda2 ** 2 - 0.02163))
                ne_omiga_theta = no_omiga ** 2 * ne_omiga ** 2 / math.sqrt(pow(no_omiga * sp.sin(solution[0]), 2) + pow(ne_omiga * sp.cos(solution[0]), 2))
                ne_2omiga_theta = no_2omiga ** 2 * ne_2omiga ** 2 / math.sqrt(pow(no_2omiga * sp.sin(solution[0]), 2) + pow(ne_2omiga * sp.cos(solution[0]), 2))
                deta = (omiga1 * L / c) * (1 / 2 * ne_omiga_theta + 1 / 2 * no_omiga - ne_2omiga_theta)
                deff = pow(sp.cos(solution[0]), 2) * (d11 * sp.sin(3 * solution[1]) + d22 * sp.cos(3 * solution[1]))
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为eoe")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)
                return 1
            else:
                return 0
        print("选择的晶体是β-BaB_2O_4")
    elif b == "3":
        d15 = 5.53e-12
        d31 = 4.4e-12


        if a == "1":
            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(
                sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1])) <= 0.000001 and abs(
                sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程', sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])
                no_omiga = math.sqrt(3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                ne_omiga = math.sqrt(2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                no_2omiga = math.sqrt(3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                ne_2omiga = math.sqrt(2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                ne_2omiga_theta = no_2omiga * ne_2omiga / sp.sqrt(no_2omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_2omiga ** 2 * sp.cos(solution[0]) ** 2)
                deta = omiga1 * L / c * (no_omiga - ne_2omiga_theta)
                deff = d31 * sp.sin(solution[0])
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (
                            8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为ooe")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)

                return 1
            else:
                return 0
        elif a ==2:
            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1])) <= 0.000001 and abs(sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程', sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])
                no_omiga = math.sqrt(3.415716 + 0.047031 / (lamda1 ** 2 - 0.035306) - 0.008801 * pow(lamda1, 2))
                ne_omiga = math.sqrt(2.918692 + 0.035145 / (lamda1 ** 2 - 0.028224) - 0.003641 * pow(lamda1, 2))
                no_2omiga = math.sqrt(3.415716 + 0.047031 / (lamda2 ** 2 - 0.035306) - 0.008801 * pow(lamda2, 2))
                ne_2omiga = math.sqrt(2.918692 + 0.035145 / (lamda2 ** 2 - 0.028224) - 0.003641 * pow(lamda2, 2))
                ne_omiga_theta = no_omiga ** 2 * ne_omiga ** 2 / math.sqrt(pow(no_omiga * sp.sin(solution[0]), 2) + pow(ne_omiga * sp.cos(solution[0]), 2))
                ne_2omiga_theta = no_2omiga ** 2 * ne_2omiga ** 2 / math.sqrt(pow(no_2omiga * sp.sin(solution[0]), 2) + pow(ne_2omiga * sp.cos(solution[0]), 2))
                deta = (omiga1 * L / c) * (1 / 2 * ne_omiga_theta + 1 / 2 * no_omiga - ne_2omiga_theta)
                deff = d15 * sp.sin(solution[0])
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为eoe")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)

                return 1
            else:
                return 0

        else:
            print("该晶体不存在此种相位匹配")



        print("选择的晶体类型是LiIO_3")
    elif b == "4":
        d15 = 4.4e-12
        d22 = 4.4e-12



        if a == "3":
            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(
                    sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(
                    solution[1])) <= 0.000001 and abs(
                sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程',
                      sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])
                a1e = 4.5615
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
                a4o = 1.570
                a5o = 8.2517
                a6o = 0.0237
                b1o = 2.0704e-8
                b2o = 1.4449e-8
                b3o = 1.5978e-8
                b4o = 4.7686e-6
                b5o = 1.1127e-5
                f = (25 - 24.5) * (25 + 570.82)
                ne_omiga = math.sqrt(a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                                b4e * f) / (
                                                 lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                no_omiga = math.sqrt(a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                                b4o * f) / (
                                                 lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                ne_2omiga = math.sqrt(a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                                 b4e * f) / (
                                                  lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                no_2omiga = math.sqrt(a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                                 b4o * f) / (
                                                  lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                ne_2omiga_theta = no_2omiga * ne_2omiga / sp.sqrt(
                    no_2omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_2omiga ** 2 * sp.cos(solution[0]) ** 2)
                ne_omiga_theta = no_2omiga * ne_omiga / sp.sqrt(
                    no_omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_omiga ** 2 * sp.cos(solution[0]) ** 2)
                deta = omiga1 * L / c * (ne_omiga_theta - no_2omiga)
                deff = d22 * sp.cos(solution[0] ** 2 * sp.cos(3 * solution[1]))
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (
                        8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为eeo")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)

                return 1
            else:
                return 0

            print("相位匹配类型为eeo")
        elif a == "4":
            symbols = [theta, phi, k]
            solution = sp.nsolve(eqs, symbols, [i, j, l], verify=False)
            if 0 <= solution[0] <= sp.pi / 2 and 0 <= solution[1] <= sp.pi / 2 and abs(
                    sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1])) <= 0.000001 and abs(
                sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(
                    solution[1])) <= 0.000001 and abs(
                sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0])) <= 0.000001:
                print('第一方程',
                      sp.sin(alpha) * sp.sin(beta) - solution[2] * sp.sin(solution[0]) * sp.cos(solution[1]))
                print('第二方程', sp.sin(alpha) - solution[2] * sp.sin(solution[0]) * sp.sin(solution[1]))
                print('第三方程', sp.cos(alpha) * sp.cos(beta) - solution[2] * sp.cos(solution[0]))
                print("Solution (theta, phi, k):", solution)
                print(solution[0])

                a1e = 4.5615
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
                a4o = 1.570
                a5o = 8.2517
                a6o = 0.0237
                b1o = 2.0704e-8
                b2o = 1.4449e-8
                b3o = 1.5978e-8
                b4o = 4.7686e-6
                b5o = 1.1127e-5
                f = (25 - 24.5) * (25 + 570.82)
                ne_omiga = math.sqrt(a1e + b1e * f + (a2e + b2e * f) / (lamda1 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                                b4e * f) / (
                                             lamda1 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda1 ** 2)
                no_omiga = math.sqrt(a1o + b1o * f + (a2o + b2o * f) / (lamda1 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                                b4o * f) / (
                                             lamda1 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda1 ** 2)
                ne_2omiga = math.sqrt(a1e + b1e * f + (a2e + b2e * f) / (lamda2 ** 2 - pow(a3e + b3e * f, 2)) + (a4e +
                                                                                                                 b4e * f) / (
                                              lamda2 ** 2 - pow(a5e + b5e * f, 2)) - a6e * lamda2 ** 2)
                no_2omiga = math.sqrt(a1o + b1o * f + (a2o + b2o * f) / (lamda2 ** 2 - pow(a3o + b3o * f, 2)) + (a4o +
                                                                                                                 b4o * f) / (
                                              lamda2 ** 2 - pow(a5o + b5o * f, 2)) - a6o * lamda2 ** 2)
                ne_2omiga_theta = no_2omiga * ne_2omiga / sp.sqrt(
                    no_2omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_2omiga ** 2 * sp.cos(solution[0]) ** 2)
                ne_omiga_theta = no_2omiga * ne_omiga / sp.sqrt(
                    no_omiga ** 2 * sp.sin(solution[0]) ** 2 + ne_omiga ** 2 * sp.cos(solution[0]) ** 2)
                deta = omiga1 * L / c * (1 /2 * no_omiga + 1 / 2 * ne_omiga_theta - no_2omiga)
                deff = d15 * sp.sin(solution[0]) - d22 * sp.cos(solution[0]) * sp.sin(solution[1] * 3)
                eta = (2 * pow(omiga1 * deff * L * sp.sin(deta) / deta, 2) * I1) / (
                        8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)
                print("theta为：", sp.deg(solution[0]))
                print("phi为：", sp.deg(solution[1]))
                print("效率值为：", eta)
                print("相位匹配类型为eoo")
                print("no_omiga", no_omiga)
                print("no_2omiga", no_2omiga)
                print("ne_2omiga", ne_2omiga)
                print("ne_2omiga_theta", ne_2omiga_theta)

                return 1
            else:
                return 0

        else:
            print("该晶体不存在此种匹配类型")
        print("选择的晶体是LiTaO_3")










def forEach():
    for i in np.arange(0.000001, sp.pi/2, 1):
        for j in np.arange(0.000001, sp.pi/2, 1):
            for l in np.arange(0.0001, 2, 1):
                res = cal(i, j, l, b, a)
                if res == 1:
                    return

forEach()

'''

no_omiga = math.sqrt(4.9048 + 0.11768/(lamda1**2 - 0.0475) - 0.027169 * lamda1**1)
no_2omiga = math.sqrt(4.9048 + 0.011768 / (lamda2**2 - 0.0475) - 0.027169 * lamda2**2)
ne_2omiga = math.sqrt(4.582 + 0.099169 / (lamda2**2 - 0.04443) - 0.02195 * lamda2**2)
ne_2omiga_theta = no_2omiga * ne_2omiga/sp.sqrt(no_2omiga**2 * sp.sin(theta)**2 + ne_2omiga**2 * sp.cos(theta)**2)
deta = omiga1 * L/c * (no_omiga - ne_2omiga_theta)

deff = d31 * sp.sin(theta) - d22 * sp.cos(theta) * sp.sin(3*phi)
eta = (2 * pow(omiga1 * deff * L * sp.sin(deta)/deta, 2) * I1) / (8.85e-12 * c * c * c * no_omiga * no_omiga * ne_2omiga_theta)

#将弧度转化为角度
theta = sp.deg(solution[0])
phi = sp.deg(phi)

print("theta为：", theta)
print("phi为：", phi)
print("效率值为：",deff)
print("no_omiga", no_omiga)
print("no_2omiga",no_2omiga)
print("ne_2omiga", ne_2omiga)
print("ne_2omiga_theta", ne_2omiga_theta)

#theta = np.degrees(theta)

#plt.plot(theta, eta)
#plt.show()

'''