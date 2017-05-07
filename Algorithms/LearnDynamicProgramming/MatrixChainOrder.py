global inf
inf = 0x3f3f3f3f


def print_matrix(M):
    for row in M:
        for val in row:
            print('{:10}'.format(str(val)), end=' ')
        print()


def matrix_chain(p):
    """Algorithm: buttom up
    Aux space: θ(n^2)
    Time: θ(n^2)"""
    # dimension of Ai is p[i-1]*p[i]
    n = len(p)
    m = [[0 for x in range(n)] for x in range(n)]

    for i in range(1, n):
        m[i][i] = 0
 
    # L is chain length.
    for L in range(2, n):
        for i in range(1, n-L+1):
            j = i+L-1
            m[i][j] = inf
            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
                if q < m[i][j]:
                    m[i][j] = q
 
    return m[1][n-1]


def memo_matrix_chain(p):
    """Algorithm: memoization
    Aux space: θ(n^2)
    Time: θ(n^2)"""
    def rec(m, p, i, j):
        if m[i][j] < inf:
            return m[i][j]

        if i == j:
            m[i][j] = 0
        else:
            for k in range(i, j):
                q = rec(m, p, i, k) + rec(m, p, k+1, j) + p[i-1]*p[k]*p[j]
                if q < m[i][j]:
                    m[i][j] = q
        
        return m[i][j]
    
    n = len(p)
    m = [[inf for x in range(n)] for x in range(n)]
    ans = rec(m, p, 1, n-1)
    # print_matrix(m)
    return ans

if __name__ == '__main__':
    p = [30, 35, 15, 5, 10, 20, 25]
    assert(matrix_chain(p) == memo_matrix_chain(p) == 15125)