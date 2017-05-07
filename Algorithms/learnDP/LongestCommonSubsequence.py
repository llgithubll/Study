def print_matrix(M):
    print('\n'.join([''.join(['{:5}'.format(str(val)) for val in row]) for row in M]))


def lcs(X, Y):
    """Algorithm: buttom up dynamic programming
    Aux space: θ(mn)
    Time: θ(mn)"""
    m = len(X)
    n = len(Y)
    L = [[None] * (n+1) for i in range (m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    # print('lcs:')
    # print_matrix(L)
    return L[m][n]


def memo_lcs(X, Y):
    """Algorithm: memoization dynamic programming
    Aux space: θ(mn)
    Time: O(mn)"""
    def rec(L, X, Y, i, j):
        if L[i][j] is not None:
            return L[i][j]

        if i == 0 or j == 0:
            L[i][j] = 0
        elif X[i-1] == Y[j-1]:
            L[i][j] = rec(L, X, Y, i-1, j-1) + 1
        else:
            L[i][j] = max(rec(L, X, Y, i-1, j), rec(L, X, Y, i, j-1))
        return L[i][j]
    
    m = len(X)
    n = len(Y)
    L = [[None] * (n+1) for i in range(m+1)]
    ans = rec(L, X, Y, m, n)
    # print('memo_lcs:')
    # print_matrix(L)
    return ans

if __name__ == '__main__':
    X1 = 'ABCBDAB'
    Y1 = 'BDCABA'
    assert (lcs(X1, Y1) == memo_lcs(X1, Y1) == 4)
    X2 = '10010101'
    Y2 = '010110110'
    assert (lcs(X2, Y2) == memo_lcs(X2, Y2) == 6)