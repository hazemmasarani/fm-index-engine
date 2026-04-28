import random
import time

time_comp_dic = {
    1:[],
    2:[],
    3:[],
    4:[],
    5:[],
    6:[],
    7:[],
    8:[],
    9:[],
    10:[],
    11:[],
    12:[],
    13:[],
    14:[],
    15:[]
}

def build_sa_naive(text):
    return sorted(range(len(text)), key=lambda i: text[i:])

def build_sample_indices(n):
    # start = time.time()
    idx = []
    for i in range(1, n - 3, 3):
        idx.append(i)
    idx.append(n - 3)
    for i in range(2, n - 3, 3):
        idx.append(i)
    # end = time.time()
    # time_comp_dic[1].append(end - start)
    return idx

def build_triplets(text, indices):
    # start = time.time()
    triplets = []
    for i in indices:
        triplet = (text[i], text[i+1], text[i+2], i)
        triplets.append(triplet)
    # end = time.time()
    # time_comp_dic[2].append(end - start)
    return triplets

# def counting_sort(triplets, indx):
#     start = time.time()
#     count = {}
#     for triplet in triplets:
#         key = triplet[indx]
#         if key not in count:
#             count[key] = []
#         count[key].append(triplet)
    
#     sorted_triplets = []
#     for key in sorted(count.keys()):
#         sorted_triplets.extend(count[key])
#     end = time.time()
#     time_comp_dic[3].append(end - start)
#     return sorted_triplets

def counting_sort(triplets, index):
    # start = time.time()

    max_val = max(triplet[index] for triplet in triplets)

    # Step 1: Create buckets
    count = [[] for _ in range(max_val + 1)]

    # Step 2: Distribute
    for triplet in triplets:
        key = triplet[index]
        count[key].append(triplet)

    # Step 3: Flatten
    sorted_triplets = []
    for bucket in count:
        sorted_triplets.extend(bucket)
    # end = time.time()
    # time_comp_dic[3].append(end - start)
    return sorted_triplets

# def counting_sort(triplets, index):
#     start = time.time()
#     count = [[] for _ in range(len(triplets)+20)]
#     for triplet in triplets:
#         key = triplet[index]
#         count[key].append(triplet)  
#     sorted_triplets = []
#     for bucket in count:
#         sorted_triplets.extend(bucket)
#     end = time.time()
#     time_comp_dic[3].append(end - start)
#     return sorted_triplets

def radix_sort(triplets, exp):
    # start = time.time()
    for i in range(exp, -1, -1):
        triplets = counting_sort(triplets, i)
    # end = time.time()
    # time_comp_dic[4].append(end - start)
    return triplets

def create_triplet_rank(triplets):
    # start = time.time()
    rank = {}
    current_rank = 0
    prev_triplet = None
    for triplet in triplets:
        if triplet[:3] != prev_triplet:
            current_rank += 1
            prev_triplet = triplet[:3]
        rank[tuple(triplet[:3])] = current_rank
    # end = time.time()
    # time_comp_dic[5].append(end - start)
    return rank

def build_l_1_2_unique_ranks(sorted_triplets):
    # start = time.time()
    l_1_2 = [0] * (len(sorted_triplets) - 1)
    for i, triplet in enumerate(sorted_triplets[1:]):
        l_1_2[i] = triplet[3]
    # end = time.time()
    # time_comp_dic[6].append(end - start)
    return l_1_2

def create_reduced_string(text, indices, triplet_rank):
    # start = time.time()
    reduced_string = []
    for i in indices:
        triplet = (text[i], text[i+1], text[i+2])
        reduced_string.append(triplet_rank[triplet])
    # end = time.time()
    # time_comp_dic[7].append(end - start)
    return reduced_string

def build_l_1_2(sa_reduced, idx_1_2):
    # start = time.time()
    l_1_2 = [0] * (len(sa_reduced) - 1)
    for i, pos in enumerate(sa_reduced[1:]):
        l_1_2[i] = idx_1_2[pos]
    # end = time.time()
    # time_comp_dic[8].append(end - start)
    return l_1_2

def build_r_1_2(l_1_2):
    # start = time.time()
    r_1_2 = {}
    for i, idx in enumerate(l_1_2):
        r_1_2[idx] = i
    # end = time.time()
    # time_comp_dic[9].append(end - start)
    return r_1_2

def build_mod_0_buckets(text, r_1_2):
    # start = time.time()
    mod_0_buckets = []
    for i in range(0, len(text) - 3, 3):
        first_char = text[i]
        mod_0_buckets.append((first_char, r_1_2[i + 1] + 1 if i + 1 in r_1_2 else 0, i))
    # end = time.time()
    # time_comp_dic[10].append(end - start)
    return mod_0_buckets

def create_r_0(mod_0_buckets):
    # start = time.time()
    r_0 = {}
    for rank, bucket in enumerate(mod_0_buckets):
        r_0[bucket[2]] = rank
    # end = time.time()
    # time_comp_dic[11].append(end - start)
    return r_0

def create_l_0(r_0):
    # start = time.time()
    l_0 = [0] * len(r_0)
    for pos, rank in r_0.items():
        l_0[rank] = pos
    # end = time.time()
    # time_comp_dic[12].append(end - start)
    return l_0

def is_a_less_than_b(text, i, j, rank):

    if j >= len(text) - 3:
        return False
    if i >= len(text) - 3:
        return True
    
    if i % 3 != 0 and j % 3 != 0:
        return rank[i] < rank[j]
    else:
        if text[i] != text[j]:
            return text[i] < text[j]
        else:
            return is_a_less_than_b(text, i + 1, j + 1, rank)

def merge_mod0_and_mod1_2(text, l_0, l_1_2, r_1_2):
    # start = time.time()
    merged_sa = []
    i0, i1 = 0, 0
    n0, n1 = len(l_0), len(l_1_2)
    while i0 < n0 and i1 < n1:
        pos0, pos1 = l_0[i0], l_1_2[i1]
        
        if is_a_less_than_b(text, pos0, pos1, r_1_2):
            merged_sa.append(pos0)
            i0 += 1
        else:
            merged_sa.append(pos1)
            i1 += 1
    
    while i0 < n0:
        merged_sa.append(l_0[i0])
        i0 += 1
    while i1 < n1:
        merged_sa.append(l_1_2[i1])
        i1 += 1
        
    # end = time.time()
    # time_comp_dic[13].append(end - start)

    return merged_sa


def build_sa_dc3(text):

    # Base case for small strings
    if len(text) <= 3:
        return sorted(range(len(text)), key=lambda i: text[i:])

    ################################################################################################
    # Part 1: Build the suffix array for the sample indices (1 mod 3 and 2 mod 3)
    ################################################################################################

    # Step 1: Add padding to the text
    text += [0, 0, 0]  

    # Step 2: build the sample indices
    idx_1_2 = build_sample_indices(len(text))

    # Step 3: build the triplets for the sample indices
    triplets = build_triplets(text, idx_1_2)

    # Step 4: sort the triplets using radix sort
    sorted_triplets = radix_sort(triplets, 2)

    # Step 5: create the rank for the triplets
    rank = create_triplet_rank(sorted_triplets)
    
    if len(rank) == len(sorted_triplets):
        
        # Step 6: build l_1_2 directly from the sorted triplets
        l_1_2 = build_l_1_2_unique_ranks(sorted_triplets)
    
    else:

        # Step 6: build the reduced string for the recursive call
        reduced_string = create_reduced_string(text, idx_1_2, rank)

        # Step 7: recursively build the suffix array for the reduced string
        sa_reduced = build_sa_dc3(reduced_string)

        # Step 8: build l_1_2
        l_1_2 = build_l_1_2(sa_reduced, idx_1_2)

    # Step 9: build r_1_2
    r_1_2 = build_r_1_2(l_1_2)

    print("idx_1_2: ", idx_1_2)

    print("l_1_2: ", l_1_2)

    print("r_1_2: ", r_1_2)

    ################################################################################################
    # Part 2: Sort the suffixes starting at positions 0 mod 3 using the sorted sample suffixes
    ################################################################################################
    
    # Step 10: Create first character buckets for the 0 mod 3 suffixes
    mod_0_buckets = build_mod_0_buckets(text, r_1_2)

    # Step 11: Sort the 0 mod 3 suffixes using the first character buckets and the ranks of the sample suffixes
    mod_0_buckets = radix_sort(mod_0_buckets, 1)

    # Step 12: Create r_0
    r_0 = create_r_0(mod_0_buckets)

    # Step 13: Create l_0
    l_0 = create_l_0(r_0)
    

    ################################################################################################
    # Part 3: Merge the two suffix arrays (l_0 and l_1_2) to get the final suffix array
    ################################################################################################

    # Step 14: Merge the two sorted lists (l_0 and l_1_2) to get the final suffix array
    sa = merge_mod0_and_mod1_2(text, l_0, l_1_2, r_1_2)

    return sa



if __name__ == "__main__":

    # text = [1,2,2,1,1,2,1,1]
    text = [4,2,1,0,3,3]
    sa_naive = build_sa_naive(text)
    print("Suffix Array:", sa_naive)
    sa_dc3 = build_sa_dc3(text)
    print("Suffix Array (DC3):", sa_dc3)
    print("Match:", sa_naive == sa_dc3)

 
    # Generate random text for testing
    # max_tries = 3
    # same_out = True
    # while max_tries > 0 and same_out:
    #     max_tries -= 1
    #     text = [random.randint(1, 2) for _ in range(1000000)]
        # sa_naive = build_sa_naive(text)
        # sa = build_sa_dc3(text)
        # same_out = (sa_naive == sa)
        # if not same_out:
        #     print("Text:", text)
        #     print("Naive SA:", sa_naive)
        #     print("DC3 SA:", sa)
        #     print("Match:", same_out)
        #     break

    # # save the time comparison results to a file
    # with open("dc3_time_comparison.txt", "w") as f:
    #     for key, times in time_comp_dic.items():
    #         f.write(f"Step {key}: {times}\n")
    
    # # print the mean of each step's times
    # for key, times in time_comp_dic.items():
    #     if times:
    #         mean_time = sum(times) / len(times)
    #         print(f"Step {key}: Mean Time = {mean_time:.6f} seconds, Sum: {sum(times):.6f} seconds, Count: {len(times)}")