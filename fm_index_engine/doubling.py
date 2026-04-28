
def build_sa_doubling(s):
    n = len(s)
    # Initial ranks based on characters (prefixes of length 1)
    rank = s
    sa = list(range(n))
    k = 1
    
    while k < n:
        # Key for sorting: (rank[i], rank[i+k] if i+k < n else -1)
        # This sorts suffixes based on prefixes of length 2*k
        key = lambda i: (rank[i], rank[i+k] if i+k < n else -1)
        sa.sort(key=key)
        
        # Recompute ranks based on the sorted order
        new_rank = [0] * n
        for i in range(1, n):
            # If current suffix matches previous suffix for length 2*k
            # they share the same rank
            new_rank[sa[i]] = new_rank[sa[i-1]]
            if key(sa[i]) > key(sa[i-1]):
                new_rank[sa[i]] += 1
        
        rank = new_rank
        # Optimization: stop if all suffixes have unique ranks
        if rank[sa[n-1]] == n - 1:
            break
        k *= 2
        
    return sa

def build_sa_naive(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [index for (suffix, index) in suffixes]

if __name__ == "__main__":
    # Example usage:
    text = [1,2,1,1,2,2,1,1,1,3,3,1,1,2,2,2,1,1,3,1,1,1,1,2,2,2,1,1,1,1,1,3,3,3,2,2,2,1,1,1,1,3,1,1,1,1,1,2,2,2,1,2,2,2,3]
    suffix_array = build_sa_doubling(text)
    sa_naive = build_sa_naive(text)
    # print(f"Suffix Array for '{text}': {suffix_array}")
    if suffix_array == sa_naive:
        print("Suffix arrays match!")
