import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import time
import pprint

plt.rcParams['figure.figsize'] = (10.0, 8.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


def load_data(train_file, test_file):
    train_data = open(train_file).read()
    train_data = train_data.split('\n')[1:-1]
    train_data = [line.split(',') for line in train_data]

    X_train = np.array([[int(row[j]) for j in range(1, len(row))] for row in train_data])
    y_train = np.array([int(row[0]) for row in train_data])

    test_data = open(test_file).read()
    test_data = test_data.split('\n')[1:-1]
    test_data = [row.split(',') for row in test_data]

    X_test = np.array([[int(val) for val in row] for row in test_data])

    return X_train, y_train, X_test
    
def visualize_random_samples(X_train, y_train, samples=8):
    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    num_classes = len(classes)

    for y, c in enumerate(classes):
        idxs = np.nonzero([i == y for i in y_train])
        idxs = np.random.choice(idxs[0], samples, replace=False)

        for i, idx in enumerate(idxs):
            plt_idx = i * num_classes + y + 1
            plt.subplot(samples, num_classes, plt_idx)
            plt.imshow(X_train[idx].reshape((28, 28)))
            plt.axis('off')
            if i == 0:
                plt.title(c)
    plt.show()

class knn():

    def __init__(self):
        pass

    def train(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X, k=1):
        dists = self.compute_distances(X)
        
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)

        for i in range(num_test):
            k_closest_y = []
            labels = self.y_train[np.argsort(dists[i, :])].flatten()
            k_closest_y = labels[:k]

            c = Counter(k_closest_y)
            y_pred[i] = c.most_common(1)[0][0]

        return(y_pred)

    def compute_distances(self, X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]

        dot_pro = np.dot(X, self.X_train.T)

        sum_square_test = np.square(X).sum(axis=1)
        sum_square_train = np.square(self.X_train).sum(axis=1)
        dists = np.sqrt(-2 * dot_pro + sum_square_train + np.matrix(sum_square_test).T)

        return (dists)


def test_knn(X, y, k=1, train_rate=0.7):
    "use part of train data to train, and rest of train data to test"
    train_cnt = int(X.shape[0] * train_rate) 
    X_train = np.array(X[:train_cnt])
    y_train = np.array(y[:train_cnt])
    X_test = np.array(X[train_cnt:])
    y_test = np.array(y[train_cnt:])
    
    classifier = knn()
    classifier.train(X_train, y_train)
    predictions = classifier.predict(X_test, k)
    
    error_count = 0
    total = len(predictions)
    for i in range(total):
        if y_test[i] != predictions[i]:
            error_count += 1
    print('accuracy:{0}%'.format((1.0 - error_count / total) * 100))


def get_result(X_train, y_train, X_test, k=3):
    batch_size = 500
    total_size = len(X_test)
    classifier = knn()
    classifier.train(X_train, y_train)
        
    predictions = []
    b = 0
    e = batch_size
    total_time = 0.0
    while e < total_size:
        tic = time.time()
        predts = classifier.predict(X_test[b:e],k)
        toc = time.time()
        predictions += list(predts)
        total_time += toc - tic
        print('batch({0}:{1})...{2} seconds'.format(str(b), str(e), str(toc-tic)))
        b = e
        e += batch_size
    tic = time.time()
    predts = classifier.predict(X_test[b:total_size],k)
    toc = time.time()
    predictions += list(predts)
    total_time += toc - tic
    print('batch({0}:{1})...{2} seconds'.format(str(b), str(e), str(toc-tic)))
        
    print('predictions completed, total time:{0} minutes'.format(str(total_time / 60.0)))
    
    with open('predictions.csv', 'w') as out_file:
        out_file.write('ImageId,Label\n')
        for i in range(len(predictions)):
            out_file.write(str(i+1)+','+str(int(predictions[i]))+'\n')
    
    print('write file complete')