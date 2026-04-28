
def build_sa_naive(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [index for (suffix, index) in suffixes]


if __name__ == "__main__":
    text = [1,2,1,1,1,1,1,2,2,2]
    sa = build_sa_naive(text)
    print(sa)  # Output: [5, 3, 1, 0, 4, 2]