# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pylab as plt
import operator
import requests

f = open('result.txt', 'r')
x = list()
y = list()
L = np.zeros((500, 500))

urls = []
while True:
    url = f.readline().rstrip('\n')
    if url:
        urls.append(url)
    else:
        break

url_len = len(urls)
relation_matrix = np.zeros((url_len,url_len))
for i in range(0,url_len):
    try:
        r = requests.get(urls[i])
    except:
        print('timeout')
        continue
    print("{}/500".format(i))
    pattern = plt.re.compile(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')')
    results = pattern.findall(r.content.decode('ISO-8859-1'))
    for j in range(0,url_len):
        if urls[j] in results:
            relation_matrix[i][j] = 1


for i in range(0, 500):
    for j in range(0, 500):
        if relation_matrix[i][j] == 1:
            x.append(i)
            y.append(j)

plt.show()

for i in range(0, len(x)):
    L[x[i]][y[i]] = 1

# translate L into A
for i in range(0, 500):
    sum = 0
    for j in L[:, i]:
        sum += j
    if not sum == 0:
        L[:, i] = L[:, i] / sum
A = L
A = np.array(A)
# power iteration for G
X = np.zeros((500, 1))
# init a random vector
X[0][0] = 1
# init e and k
e = np.ones((500, 1))
k = 0.85

for i in range(0, 5000):
    Y = np.dot(A, X)
    B = 1 - k * np.sum(Y)
    X = k * Y + (B / 500) * e
V = X

V_dic = {}
V = list(V)
for i in range(0, 500):
    V_dic[urls[i]] = float(V[i])

final_result = sorted(V_dic.items(), key=operator.itemgetter(1), reverse=True)
# output the top 20
for i in range(0, 100):
    print(final_result[i][0])