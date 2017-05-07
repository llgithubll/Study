# Non strict case.
import bisect
from LongestCommonSubsequence import *


def lis(arr):
    """Algorithm: dynamic programing
    Aux Space: θ(n)
    Time: θ(n^2)"""
    n = len(arr)
    L = [1] * n
    max_len = 0

    for i in range(1, n):
        for j in range(0, i):
            if arr[i] >= arr[j] and L[i] < L[j] + 1:
                L[i] = L[j] + 1
                max_len = L[i] if L[i] > max_len else max_len

    return max_len


def lis_by_lcs(arr):
    """Algorithm: lis(arr) == lcs(arr_sorted, arr)
    Aux space: O(n^2) (the same as lcs)
    Time: O(n^2) (the same as lcs)"""
    return lcs(arr, sorted(arr))


def lis_optimal(arr):
    """Algorithm: 优化传统动态规划
    （长度为i的候选子序列的尾元素 >= 长度尾i-1的候选子序列尾元素，
    存储长度为i(1 <= i <= n)的LIS的最小尾元素，通过二分查找相应元素，判断是否满足上述条件）
    Aux space: θ(n)
    Time: O(nlogn)"""

    n = len(arr)
    if n == 0:
        return 0
    
    tail = [None] * n
    length = 1
    tail[0] = arr[0]

    for i in range(1, n):
        if arr[i] >= tail[length-1]:
            tail[length] = arr[i]
            length += 1
        else:
            pos = bisect.bisect(tail, arr[i], 0, length-1)
            tail[pos] = arr[i]
    
    return length
    

if __name__ == '__main__':
    arr1 = [0, 0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    assert(lis(arr1) == lis_by_lcs(arr1) == lis_optimal(arr1) == 7)
