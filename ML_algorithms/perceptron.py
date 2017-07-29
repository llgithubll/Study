from random import choice
from numpy import array, dot, random, arange
import matplotlib.pyplot as plt


def draw(w, cnt, iter_num, train_data):
    pos_x1 = []
    pos_x2 = []
    neg_x1 = []
    neg_x2 = []
    for x, y in train_data:
        if y < 0:
            neg_x1.append(x[0])
            neg_x2.append(x[1])
        else:
            pos_x1.append(x[0])
            pos_x2.append(x[1])
    
    x1 = arange(-5, 5, 0.1)
    x2 = [-(w[0] * x + w[2]) / w[1] for x in x1]
    plt.plot(x1, x2, color=str(cnt/iter_num))
    plt.plot(pos_x1, pos_x2, 'bo', neg_x1, neg_x2, 'rx')
    plt.ylim(0, 6)


sign = lambda x : -1 if x < 0 else 1

train_data = [
    (array([3, 3, 1]), 1),
    (array([4, 3, 1]), 1),
    (array([1, 1, 1]), -1)
]

w = random.rand(3)
errors = []
eta = 0.2
iter_num = 100


for i in range(iter_num):
    x, y = choice(train_data)
    if y * dot(w, x) <= 0:
        w = w + eta * y * x
    draw(w, i, iter_num, train_data)
plt.show()


for x, y in train_data:
    print("x:{}, y:{}, predict:{}".format(x[:2], y, sign(dot(w, x))))