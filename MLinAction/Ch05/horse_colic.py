from logistic import *


def classify_vector(x, weights):
    prob = sigmoid(sum(x*weights))
    return (1.0 if prob > 0.5 else 0.0)


def colic_test():
    with open('horseColicTraining.txt') as file_train:
        with open('horseColicTest.txt') as file_test:
            training_set = []; training_labels = []
            for line in file_train.readlines():
                curr_line = line.strip().split('\t')
                line_arr = []
                for i in range(21):
                    line_arr.append(float(curr_line[i]))
                training_set.append(line_arr)
                training_labels.append(float(curr_line[21]))
            
            weights = stoc_grad_ascent(array(training_set), training_labels, 500)
            error_count = 0; num_test_vec = 0.0

            for line in file_test.readlines():
                num_test_vec += 1.0
                curr_line = line.strip().split('\t')
                line_arr = []
                for i in range(21):
                    line_arr.append(float(curr_line[i]))
                if int(classify_vector(array(line_arr), weights)) != int(curr_line[21]):
                    error_count += 1
            
            error_rate = (float(error_count) / num_test_vec)
            print('the error rate of this test is', error_rate)
            return error_rate


def multi_test(num_tests=10):
    error_sum = 0.0
    for i in range(num_tests):
        error_sum += colic_test()
    print('after {0} iterations the average error rage is {1}'.format(str(num_tests), error_sum/float(num_tests)))


if __name__ == '__main__':
    multi_test()