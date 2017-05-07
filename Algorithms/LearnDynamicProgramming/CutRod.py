def cut_rod(prices, n):
    """Algorithm: buttom up dynamic programming
    Aux space: θ(n)
    Time: θ(n^2)"""
    if n == 0:
        return 0
    
    # r[i]为长度为i的钢条可获得的最大利益
    r = [0] * (n+1)
    for j in range(1, (n+1)):
        r[j] = -1
        for i in range(j+1):
            r[j] = max(r[j], prices[i]+r[j-i])
    return r[n]

def memo_cut_rod(prices, n):
    """Algorithm: memoization dynamci programming
    Aux space: θ(n)
    Time: O(n^2)"""
    def rec(prices, r, n):
        if r[n] >= 0:
            return r[n]
        
        if n == 0:
            r[n] = 0
        else:
            for i in range(1, (n+1)):
                r[n] = max(r[n], prices[i]+rec(prices, r, n-i))
        return r[n]
    
    r = [-1] * (n+1)
    return rec(prices, r, n)


if __name__ == '__main__':
    # length=[0, 1, 2, 3, 4, 5,  6,  7,  8,  9,  10]
    prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    assert(cut_rod(prices,  7) == memo_cut_rod(prices,  7)== 18)
    assert(cut_rod(prices, 10) == memo_cut_rod(prices, 10)== 30)
