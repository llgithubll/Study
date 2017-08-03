import numpy as np
import matplotlib.pyplot as plt
import random    



def generate_linear_seperate_points(n):
    x1, y1, x2, y2 = [random.uniform(-1, 1) for i in range(4)]
    W = np.array([y1*x2-y2*x1, y2-y1, x1-x2])
    data_set = []
    
    for i in range(n):
        x1, x2 = [random.uniform(-1, 1) for i in range(2)]
        X = np.array([1, x1, x2])
        y = int(np.sign(W.T.dot(X)))
        data_set.append((X, y))
    return data_set


class Perceptron():
    """
    w1*x1 + w2*x2 + b = 0
    W = [b, w1, w2]
    X = [1, x1, x2]

    data_set = [
        [(X, 1)],
        [(X, -1)],
        etc...
    ]

    f(X) = sign(W.dot(X))
    """
    def __init__(self, data_set, eta=1, iter_num=10):
        self.W = np.zeros(3)
        self.data_set = data_set
        self.eta = eta
        self.iter_num = iter_num
        self.fig = plt.figure()# plt.figure(figsize=(5, 5*iter_num))


    def choose_wrong_point(self, W):
        for X, y in self.data_set:
            if int(np.sign(W.T.dot(X))) != y:
                return (X, y)
        else:
            print('success classify in {} tries'.format(str(self.iter_num)))
            return None


    def PLA(self, draw=False):
        W = np.zeros(3)
        it = 1

        if draw:
            pos_x, pos_y, neg_x, neg_y = [[] for i in range(4)]
            for X, y in self.data_set:
                if y < 0:
                    neg_x.append(X[1])
                    neg_y.append(X[2])
                else:
                    pos_x.append(X[1])
                    pos_y.append(X[2])
            
        while True:
            point = self.choose_wrong_point(W)
            if point is None or it >= self.iter_num:
                break

            X, y = point
            W += self.eta * y * X

            if draw:
                x_coords = np.linspace(-1, 1)
                a, b = -W[1]/W[2], -W[0]/W[2]
                self.fig.add_subplot(self.iter_num, 1, it, xlim=[-1, 1], ylim=[-1, 1])
                plt.plot(x_coords, a*x_coords+b, pos_x, pos_y, 'go', neg_x, neg_y, 'rx')

            it += 1

        self.W = W
        if draw:
            plt.show()


if __name__ == '__main__':
    p = Perceptron(generate_linear_seperate_points(10))
    p.PLA(draw=True)
