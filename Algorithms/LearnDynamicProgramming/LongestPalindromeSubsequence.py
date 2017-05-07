from LongestCommonSubsequence import *


def lps(s):
    """Algorithm: dynamic programming
    Aux space: θ(n^2)
    Time: θ(n^2)"""
    n = len(s)
    L = [[0 for x in range(n)] for x in range(n)]
    
    for i in range(n):
        L[i][i] = 1
    # cl is length of subsequence
    for cl in range(2, n+1):
        for i in range(n-cl+1):
            j = i+cl-1
            if s[i] == s[j] and cl == 2:
                L[i][j] = 2
            elif s[i] == s[j]:
                L[i][j] = L[i+1][j-1] + 2
            else:
                L[i][j] = max(L[i][j-1], L[i+1][j]);
 
    return L[0][n-1]


def lps_by_lcs(s):
    """Algorithm: lps(s) == lcs(s, s.reverse())
    Aux space: θ(n^2) (the same as lcs)
    Time: O(n^2) (the same as lcs)"""
    return lcs(s, s[::-1]) # s[::-1] is s.reverse()


if __name__ == '__main__':
    s1 = 'alfalfa'
    assert(lps(s1) == lps_by_lcs(s1) == 5)
    s2 = 'character'
    assert(lps(s1) == lps_by_lcs(s2) == 5)