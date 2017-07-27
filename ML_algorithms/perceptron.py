from random import choice
from numpy import array, dot, random

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

for x, y in train_data:
    print("x:{}, y:{}, predict:{}".format(x[:2], y, sign(dot(w, x))))