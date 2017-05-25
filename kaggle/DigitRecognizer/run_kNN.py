from kNN import *


# X_train, y_train, X_test = load_data(r'd:/code/kaggle/DigitRecognizer/subtrain30.csv',\
#                                      r'd:/code/kaggle/DigitRecognizer/subtest30.csv')
# test_knn(X_train, y_train, 3)

X_train, y_train, X_test = load_data(r'd:/code/kaggle/DigitRecognizer/train.csv', \
                                     r'd:/code/kaggle/DigitRecognizer/test.csv')
get_result(X_train, y_train, X_test)