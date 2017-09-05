from numpy import *


def load_dataset():
    data_mat = []
    label_mat = []
    with open('testSet.txt') as f:
        for line in f.readlines():
            line_arr = line.strip().split()
            data_mat.append([1.0, float(line_arr[0]), float(line_arr[1])])
            label_mat.append(int(line_arr[2]))
    return data_mat, label_mat


def sigmoid(x):
    return 1.0 / (1 + exp(-x))


def stoc_grad_ascent(data_mat, class_labels, num_iters=150):
    m, n = shape(data_mat)
    weights = ones(n)
    for j in range(num_iters):
        data_index = set([i for i in range(m)])
        for i in range(m):
            alpha = 4 / (1.0+j+i) + 0.01
            rand_index = data_index.pop()
            h = sigmoid(sum(data_mat[rand_index]*weights))
            error = class_labels[rand_index] - h
            weights = weights + alpha*error*data_mat[rand_index]
    return weights


def plot_bestfit(weights):
    import matplotlib.pyplot as plt
    data_mat, label_mat = load_dataset()
    data_arr = array(data_mat)
    n = shape(data_arr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    
    for i in range(n):
        if int(label_mat[i]) == 1:
            xcord1.append(data_arr[i, 1]); ycord1.append(data_arr[i, 2])
        else:
            xcord2.append(data_arr[i, 1]); ycord2.append(data_arr[i, 2])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2')
    plt.show()


if __name__ == '__main__':
    data_mat, label_mat = load_dataset()
    weights = stoc_grad_ascent(array(data_mat), label_mat, 500)
    plot_bestfit(weights)