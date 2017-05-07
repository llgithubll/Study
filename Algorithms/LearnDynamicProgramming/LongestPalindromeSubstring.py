def brute_force(s):
    """Algorithm: brute force
    （对每个子串判断是否为回文串，长度为n的字符串，有n^2个子串，平均子串长度n/2）
    Aux Space: θ(1)
    Time: O(n^3)"""
    def is_pal(substr):
        n = len(substr)
        center = n // 2        
        for i in range(center):
            if substr[i] != substr[n - i - 1]:
                break
        else:
            return True
        return False

    n = len(s)
    max_len = 0
    for start in range(n):
        for end in range(start, n):
            if end + 1 - start < max_len:
                continue
            elif is_pal(s[start: end+1]):
                pal_len = end + 1 - start
                max_len = pal_len if pal_len > max_len else max_len
    
    return max_len
                

def dp(s):
    """Algorithm: dynamic programming
    （当子串s[i+1, j-1]是回文串，且s[i] == s[j]，则s[i, j]也是回文串，且len[i, j] == len[i+1, j-1]+2）
    Aux Space: θ(n^2)
    Time: θ(n^2)"""
    n = len(s)
    is_pal = [[False] * n for i in range(n)]
    max_len = 0

    for end in range(n):
        for start in range(end, -1, -1):
            if s[start] == s[end] and \
                (end - start < 2 or is_pal[start+1][end-1]):
                is_pal[start][end] = True
                max_len = max(max_len, end - start + 1)
    
    return max_len


def center_expand(s):
    """Algorithm: center expand
    （以所有字符和字符间的间隙作为回文串的对称轴，同时进行左右扩展，遇到不同字符或边界停止
    长度为n的字符串总共有2n-1个对称轴，每个位置平均要进行n/4次字符比较）
    Aux Space: θ(1)
    Time: O(n^2)"""
    n = len(s)
    max_len = 0
    
    # 以字符为对称轴，寻找最长回文子串
    for center in range(n):
        pal_len = 1
        r = 1
        while center - r >= 0 and center + r < n:
            if s[center - r] == s[center + r]:
                pal_len += 2
            else:
                break
            r += 1
        max_len = pal_len if pal_len > max_len else max_len

    # 以字符间的间隙为对称轴，寻找最长回文子串
    for center in range(n):
        pal_len = 0
        r = 0
        while center - r >= 0 and center + r + 1 < n:
            if s[center - r] == s[center + r + 1]:
                pal_len += 2
            else:
                break
            r += 1
        max_len = pal_len if pal_len > max_len else max_len
    
    return max_len    


def manacher(s):
    """Algorithm: manacher
    Aux Space: θ(n)
    Time: O(n)"""
    #预处理
    s='#'+'#'.join(s)+'#'

    # RL[i] 第i个字符为对称轴的回文串的回文半径
    RL=[0]*len(s)
    MaxRight=0
    pos=0
    MaxLen=0
    for i in range(len(s)):
        if i<MaxRight:
            RL[i]=min(RL[2*pos-i], MaxRight-i)
        else:
            RL[i]=1
        #尝试扩展，注意处理边界
        while i-RL[i]>=0 and i+RL[i]<len(s) and s[i-RL[i]]==s[i+RL[i]]:
            RL[i]+=1
        #更新MaxRight,pos
        if RL[i]+i-1>MaxRight:
            MaxRight=RL[i]+i-1
            pos=i
        #更新最长回文串的长度
        MaxLen=max(MaxLen, RL[i])
    return MaxLen-1


if __name__ == '__main__':
    s1 = 'abbba'
    assert (brute_force(s1) == dp(s1) == center_expand(s1) == manacher(s1) == 5)
    s2 = 'bbbbb'
    assert (brute_force(s2) == dp(s2) == center_expand(s2) == manacher(s2) == 5)
    s3 = 'cbbd'
    assert (brute_force(s3) == dp(s3) == center_expand(s3) == manacher(s3) == 2)
    s4 = 'bananas'
    assert (brute_force(s4) == dp(s4) == center_expand(s4) == manacher(s4) == 5)