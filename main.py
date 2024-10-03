import requests


data = {
    'x': 4,  # 行数
    'y': 4,  # 列数
    'value': "123,213"  # 要写入的值
}

response = requests.get('http://127.0.0.1:3888/calculate?l=0.0003&alpha1=31.21349&beta1=42.66009&a=1&b=1&d=1&phi2=20&phi3=60')

print(response.json())
#8.149.136.40:3341